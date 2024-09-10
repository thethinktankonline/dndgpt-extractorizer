import os
import pandas as pd
import json

def find_empty_monster_type_row(filename='dndgpt_monsters.csv'):
    # Load the CSV file
    file_path = os.path.join('..', 'data', filename)
    df = pd.read_csv(file_path)
    
    # Find the first row where 'monster_type' is empty
    empty_row = df[df['monster_type'].isna()].head(1)
    
    if empty_row.empty:
        print("No empty rows found in 'monster_type'.")
        return None
    
    # Get the index of this row
    row_index = empty_row.index[0]
    
    # Convert the row to a dictionary with standard Python types
    row_data = empty_row.iloc[0].astype(object).to_dict()
    row_data['index'] = int(row_index)  # Ensure index is a standard Python int
    
    # Convert the dictionary to a JSON string
    monster_row_json = json.dumps(row_data, indent=4)
    
    return monster_row_json

def print_empty_monster_type_row_as_json():
    # Set the filename variable
    filename = 'dndgpt_monsters.csv'
    
    # Call the function and print the JSON result
    result = find_empty_monster_type_row(filename)
    
    if result:
        print("The first row with an empty 'monster_type' is:")
        print(result)

if __name__ == "__main__":
    print_empty_monster_type_row_as_json()
