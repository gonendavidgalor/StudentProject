from fastapi import HTTPException
from pydantic import BaseModel
import json
from typing import List

class QuizQuestion(BaseModel):
    id: int
    question: str
    answers: List[str]
    right_answer: int

def load_american_questions_from_quiz(file_name):
    print(file_name)
    try:
        # full_file_name = file_name.replace(' ', '_')
        print(file_name)
        file_json_path = f'db/quiz_ps/{file_name}.json'
        with open(file_json_path, 'r') as file:
            quiz_data = json.load(file)
            quiz_questions = [QuizQuestion(**data) for data in quiz_data]
        return quiz_questions
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON")