import json
import os
from pathlib import Path

def delete_question(file_name, id):
    Path('db').mkdir(parents=True, exist_ok=True)

    file_json_path = f'db/quiz_ps/{file_name}.json'
    print(file_json_path)

    try:
        with open(file_json_path, 'r') as file:
            questions = json.load(file)
        
        questions = [question for question in questions if str(question['id']) != id]
        
        if len(questions) == 0:
            os.remove(file_json_path)

        else:
            with open(file_json_path, 'w') as file:
                json.dump(questions, file, indent=4)
    
    except FileNotFoundError:
        print(f"No file found at {file_json_path}.")
    except json.JSONDecodeError:
        print("Error decoding JSON from the file.")

    return "Question deleted"

