import json


FILES_ID_JSON_PATH = 'db\\files_id.json'

def extract_file_ids():
    with open(FILES_ID_JSON_PATH, 'r') as file:
        data = json.load(file)  # Load the JSON content
        items = {}
        items = {item['name']: item['file_id'] for item in data if item['file_id'] != "0"}  
        # Extract file_ids except of the one that represent all files )
    
    return items
