import json
from pathlib import Path

def delete_question(file_name, id):
    Path('db').mkdir(parents=True, exist_ok=True)

    file_json_path = f'db/quiz_ps/{file_name}.json'
    print(file_json_path)

    try:
        with open(file_json_path, 'r') as file:
            questions = json.load(file)
        
        # Find the object with the specified id and remove it
        questions = [question for question in questions if str(question['id']) != id]
        ids = [question['id'] for question in questions if str(question['id']) != id]
        check = [print(type(id), type(question['id']), question['id'] != str(id)) for question in questions if question['id'] != str(id)]
        print(ids)
        print(check)
        print(id)
        
        # Save the updated list back to the JSON file
        with open(file_json_path, 'w') as file:
            json.dump(questions, file, indent=4)
    
    except FileNotFoundError:
        print(f"No file found at {file_json_path}.")
    except json.JSONDecodeError:
        print("Error decoding JSON from the file.")

    return "Question saved"

