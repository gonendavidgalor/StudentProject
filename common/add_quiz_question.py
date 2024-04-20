import json
from pathlib import Path  # Importing Path from pathlib for path operations

def save_quiz_question(american_question_object):
    # Convert the object to a dictionary that can be serialized to JSON
    question_dict = {
        "question": american_question_object.question,
        "answers": american_question_object.answers,
        "right_answer": american_question_object.right_answer,
    }

    # Ensure the file path directory exists
    Path('db').mkdir(parents=True, exist_ok=True)

    # Handle '.md' suffix in file_name if present
    if american_question_object.file_name.endswith('.md'):
        file_base_name = american_question_object.file_name[:-3]  # Remove the last three characters '.md'
    else:
        file_base_name = american_question_object.file_name

    # Construct the full path for the file with .json extension
    file_json_path = f'db/quiz_{file_base_name}.json'

    # Load existing data from the file, if it exists, or initialize an empty list
    try:
        with open(file_json_path, 'r') as file:
            questions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        questions = []

    # Append the new question to the list of questions
    questions.append(question_dict)

    # Save the updated list back to the file
    with open(file_json_path, 'w') as file:
        json.dump(questions, file, indent=4)
    
    print("Question generated and saved successfully")
    return "Question saved"

# Example usage:
# Assuming you have an instance of AmericanQuestionObject
# question_obj = AmericanQuestionObject("What is the capital of USA?", ["New York", "Washington D.C.", "Los Angeles"], 1, "assistant123",
