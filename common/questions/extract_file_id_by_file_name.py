import json


FILES_ID_JSON_PATH = 'db\\files_id.json'

def extract_file_ids():
    with open(FILES_ID_JSON_PATH, 'r') as file:
        data = json.load(file)  # Load the JSON content
        items = {}
        items = {item['name']: item['file_id'] for item in data}  # Extract file_ids
    
    return items
