import json
from pathlib import Path

def save_quiz_question(american_question_object):
    question_dict = {
        "id": american_question_object.id,
        "question": american_question_object.question,
        "answers": american_question_object.answers,
        "right_answer": american_question_object.right_answer,
    }

    Path('db').mkdir(parents=True, exist_ok=True)

    if american_question_object.file_name.endswith('.md'):
        file_base_name = american_question_object.file_name[:-3]
    else:
        file_base_name = american_question_object.file_name

    file_json_path = f'db/quiz_ps/quiz_{file_base_name}.json'

    try:
        with open(file_json_path, 'r') as file:
            questions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        questions = []

    questions.append(question_dict)

    with open(file_json_path, 'w') as file:
        json.dump(questions, file, indent=4)
    
    print("Question generated and saved successfully")
    return "Question saved"

# Example usage:
# Assuming you have an instance of AmericanQuestionObject
# question_obj = AmericanQuestionObject("What is the capital of USA?", ["New York", "Washington D.C.", "Los Angeles"], 1, "assistant123",
