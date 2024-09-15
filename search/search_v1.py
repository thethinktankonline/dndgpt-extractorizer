#The goal of this script is to use an Assistant to look up values in it's knoweldge base, then report on those values. 

import os
import json
import sys
import time
from dotenv import load_dotenv
from openai import OpenAI
from pprint import pprint

# Quick Introduction
print("\n********************************************************\n*\n*\n*   Welcome to the dndGPT Name Search \n*\n*\n********************************************************")

# Makes things look nice. Repeated here for practice. 
def pretty_json(obj):
    # Assuming obj is a dictionary or an object that can be converted to a dictionary
    if hasattr(obj, "to_dict"): 
        obj = obj.to_dict() # Convert to dictionary if possible
    elif hasattr(obj, "json"):
        obj = json.loads(obj.json()) #Convert from Json string if available. 
    
    # Pretty print the json. 
    pprint(obj)

# Load Environment variables. 
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# Create an OpenAI Client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Get Assistant ID From .env
assistant = os.getenv('DNDGPT_NAME_LOOKUP_ID')

# Retrieve Assistant from Open AI
#reference: https://platform.openai.com/docs/api-reference/assistants/getAssistant
assistant_1 = client.beta.assistants.retrieve(assistant)

# Create a thread. 
thread = client.beta.threads.create()

# Create the first Message, that defines the file, and etc. 
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Please search for the list of creatures sequentially from the Crab onward in the appendix_miscellaneous_creatures pdf. Make sure to follow the exact order in which the creatures are listed without skipping any entries. Return each name as it appears in the document, continuing until for 5 entries. There are two columns per page, make sure to search both columns for names."
    #content= "What is the next monster after the Brown Bear in the appendix_miscellaneous_creatures.pdf? "
)   

# Create a run.
# Tried create_and_poll() which auto polls, but it didn't look like it was doing anything, so opted for the spinner below. 
# Reference: https://github.com/openai/openai-python/blob/main/examples/assistant.py
# Reference for ranking options: https://platform.openai.com/docs/api-reference/runs/createRun
run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant_1.id,
    model="gpt-4o-2024-08-06",
    temperature = .1,
    top_p = 0,
    tools=[
        {
            "type": "file_search",
            "file_search" :  {
                "max_num_results" : 3,
                "ranking_options" : { 
                    "ranker" : "auto",
                    "score_threshold" : 0.6 #Increasing Score Threshold to 0.75. 
                }
            }
        }
    ]
)

#Define a Spinner. 
def wait_on_run(run, thread): 
    spinner = ['|', '/', '—', '\\']
    spinner_count = 0

    print(f" Assistant working on thread. Thread ID: {thread.id}...", end='')
    while run.status == "queued" or run.status == "in_progress":
        #Spinner Visual. 
        sys.stdout.write("\r" + spinner[spinner_count % len(spinner)])
        sys.stdout.flush()
        spinner_count += 1
        
        #Check run status. 
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.1)

    #clear spinner
    sys.stdout.write("\r \r")
    sys.stdout.flush() 

    return run

run = wait_on_run(run, thread)

#When run stops, print only the response.  
if run.status == "completed": 
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    print("\n\n\n****************************\n*   Results:\n****************************\n\n")
    pretty_json(messages.data[0].content[0].text.value)

# When the run is over, list and print the run steps for troubleshooting. 
run_steps = client.beta.threads.runs.steps.list(
    thread_id=thread.id,
    run_id=run.id
    
)

print("\n\n\n****************************\n*    Analysis:\n****************************\n\n")

#Print Assistant Details 
print ("Model Used:", run.model, "Temperature:", run.temperature, "Top_p:", run.top_p)

#Chunks are determined during file upload. 
print("Chunking Strategy: 300 input, 150 overlap\n")

#print usage
pretty_json(run_steps.data[0].usage)
pretty_json(run_steps.data[1].usage)
print("\n\n")
pretty_json(run_steps.data[1].step_details.tool_calls[0].file_search)

# Delete the thread.
delete_thread = client.beta.threads.delete(thread_id=thread.id)

