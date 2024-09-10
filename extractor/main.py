import os
import time
import sys
import json
import threading
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from find_empty_row import find_empty_monster_type_row

# Global variable to stop the script
stop_script = False

# Function to monitor the kill switch
def kill_switch_listener():
    global stop_script
    while True:
        user_input = input("Press 'q' to quit the script: ")
        if user_input.lower() == 'q':
            stop_script = True
            print("Script stopping...")
            break

# Start the kill switch listener in a separate thread
kill_switch_thread = threading.Thread(target=kill_switch_listener)
kill_switch_thread.start()

# Function to normalize text and remove illegal csv characters from the data. 
def normalize_text(text):
    # Define a dictionary of incorrect characters and their replacements
    replacements = {
        '−': '-',  # Replace the incorrect minus sign with a standard hyphen
        '–': '-',  # Replace en dash with a standard hyphen
        '—': '-',  # Replace em dash with a standard hyphen
        '’': "'",  # Replace typographic apostrophe with straight apostrophe
        '‘': "'",  # Replace left single quote with straight apostrophe
        '“': '"',  # Replace left double quote with straight quote
        '”': '"',  # Replace right double quote with straight quote
    }
    
    # Normalize line breaks within entries (e.g., replace internal line breaks with spaces)
    text = text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    
    # Iterate over the replacements and apply them
    for wrong_char, correct_char in replacements.items():
        text = text.replace(wrong_char, correct_char)
    
    return text


#
# Welcome message with instructions
print("""
*******************************************
* WELCOME TO dndGPT MONSTER EXTRACTOR!    *
*                                         *
* This script will loop through the       *
* spreadsheet, processing each empty row. *
*                                         *
* Press 'q' anytime to stop the script.   *
*******************************************
""")

# Record the start time
start_time = datetime.now()
print(f"Script started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# Create an OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Lookup assistant IDs from .env
assistant1 = os.getenv('DNDGPT_MONSTER_ASSISTANT_ID')
assistant2 = os.getenv('DNDGPT_MONSTER_ASSISTANT_STRUCTURED_OUTPUT_ID')

# Function to wait on the run to complete with a spinner
def wait_on_run(run, thread): 
    spinner = ['|', '/', '—', '\\']
    spinner_count = 0

    print(f" dndGPT Assistant working on thread. Thread ID: {thread.id}...", end='')
    while run.status in ["queued", "in_progress"]:
        # Spinner Visual
        sys.stdout.write("\r" + spinner[spinner_count % len(spinner)])
        sys.stdout.flush()
        spinner_count += 1

        # Check run status
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.1)

    # Clear spinner
    sys.stdout.write("\r \r")
    sys.stdout.flush()

    return run

# Start loop to process each empty row
while True:
    if stop_script:
        break

    # Load the monster lookup (next empty row)
    row_lookup = find_empty_monster_type_row()

    # If no empty row found, break the loop
    if not row_lookup:
        print("No more empty rows found.")
        break

    # Parse JSON and load the monster_name and monster_unique_id fields into variables
    row_data = json.loads(row_lookup)
    monster_name = row_data['monster_name']
    monster_unique_id = row_data['monster_unique_id']
    monster_parent = row_data['monster_parent']
    monster_index = row_data['index']

    # Print the info being looked up
    print(f'*******************************************\n'
          f'* MONSTER BEING EXTRACTED:\n'
          f'* monster_name: {monster_name}\n'
          f'* monster_unique_id: {monster_unique_id}\n'
          f'* monster_parent: {monster_parent}\n'
          f'******************************************'
          f'\n\n\n\n\n')

    # Create a new thread
    thread = client.beta.threads.create()

    # Create the initial user message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"Fully extract this monster, the {monster_name} "
                f"The following are unique fields from our database, output first in your answer, "
                f"monster_unique_id: {monster_unique_id}, monster_parent: {monster_parent}) from your files. "
                f"Don't summarize your output."
    )

    # Create a Run (Returns an initial queued status)
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant1
    )

    run = wait_on_run(run, thread)

    # Capture the message and only show the Assistant's response in a readable format
    response = client.beta.threads.messages.list(thread_id=thread.id, order="desc")

    # Display the Assistant's response
    print(f'Assistant: {response.data[0].content[0].text.value}')

    # Retrieve the second assistant for structuring the response
    second_assistant = client.beta.assistants.retrieve(assistant2)

    # Create a Run (Returns an initial queued status)
    run2 = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=second_assistant.id
    )

    run2 = wait_on_run(run2, thread)

    # Print the second response
    response2 = client.beta.threads.messages.list(thread_id=thread.id, order="asc")

    # Prepare the desired string from the second Response as a dictionary
    prepare_json_string = response2.data[-1].content[0].text.value

    # Parse the JSON string into a Python dictionary
    monster_dictionary = json.loads(prepare_json_string)

    # Normalize the dictionary values
    for key in monster_dictionary:
        monster_dictionary[key] = normalize_text(str(monster_dictionary[key]))

    # Print the formatted dictionary
    pretty_dictionary = json.dumps(monster_dictionary, indent=4)
    print(pretty_dictionary)


    # UPDATE THE CSV
    # Load the filepath
    csv_file_path = os.path.join('..', 'data', 'dndgpt_monsters.csv')

    # Create a dataframe
    df = pd.read_csv(csv_file_path)

    # Update the row with the data from the dictionary and the monster_index identified above
    for key, value in monster_dictionary.items():
        # Handle empty strings and type casting
        if value == '' and pd.api.types.is_numeric_dtype(df[key]):
            df.at[monster_index, key] = float('nan')  # Replace with NaN for numeric columns
        else:
            df.at[monster_index, key] = value

    # Save the updated DataFrame back to the CSV
    df.to_csv(csv_file_path, index=False)

    # Delete the thread to clean up
    client.beta.threads.delete(thread.id)

print("Processing complete.")

# Record the end time
end_time = datetime.now()
print(f"Script ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n\n\n\n")

# Calculate and print the total execution time
execution_time = end_time - start_time
print(f"Total execution time: {execution_time}")

# Terminate the script after the full loop has executed.
stop_script = True
