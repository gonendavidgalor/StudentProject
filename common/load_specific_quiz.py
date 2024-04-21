from fastapi import HTTPException
from pydantic import BaseModel
import json
from typing import List, Optional

class QuizQuestion(BaseModel):
    question: str
    answers: List[str]
    right_answer: int

def load_american_questions_from_quiz(file_name):
    print("hey")
    try:
        file_json_path = f'db/quiz_ps/{file_name}.json'
        with open(file_json_path, 'r') as file:
            # Load JSON data
            quiz_data = json.load(file)
            # Convert list of dictionaries to list of QuizQuestion models
            quiz_questions = [QuizQuestion(**data) for data in quiz_data]
        return quiz_questions
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON")