import json
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from common.questions.load_quiz import list_quiz_files
from common.questions.load_specific_quiz import load_american_questions_from_quiz
from common.files.upload_file import get_file_id
from common.questions.generate_questions import generate_a_question
from common.questions.ask_questions import ask_a_question
from typing import Optional
from common.files.add_file_to_db import add_file
from common.files.load_files import load_content
from utils.shared_objects import AmericanQuestionObjectWithFileName
from common.questions.add_quiz_question import save_quiz_question



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],  # The origins permitted to make requests, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Just basic for checking the UI
# @app.get("/upload_file")
# def upload_file():
#     return get_file_id()


# TODO: Should be the real one
@app.post("/upload_file")
# async def upload_file(file: UploadFile = File(...)):
#     return await get_file_id(file)
async def upload_file(file: UploadFile = File(...)):
    return get_file_id()

@app.post("/generate_question")
def generate_questions(file_id: str = Form(...), thread_id: Optional[str] = Form(None), assistant_id: Optional[str] = Form(None) ):
    print(file_id)
    return generate_a_question(file_id, thread_id, assistant_id)

# @app.get("/generate_question")
# def generate_questions():
#     file_id = 'file-cvwILzT6xpvF5PiPoFr51Kck'
#     return generate_a_question(file_id)


# @app.post("/ask_question")
# def ask_questions(file_id: str = Form(...), question: str = Form(...)):
#     return ask_a_question(file_id, question)

@app.post("/ask_question")
def ask_questions(file_id: str = Form(...), question: str = Form(...), thread_id: Optional[str] = Form(None), assistant_id: Optional[str] = Form(None) ):
    print(thread_id, "thread_id5")
    print(assistant_id, "assistant_id5")
    return ask_a_question(file_id, question, thread_id, assistant_id)


@app.post("/save_file")
async def save_file(file: UploadFile = File(...)):
    await add_file(file)


class FileDetails(BaseModel):
    name: str
    content: str

# Try to make it look better
@app.get("/load_files")
async def load_files():
    print("wow")
    FILES_JSON_PATH = 'db/files.json'

    try:
        print("check1")

        with open(FILES_JSON_PATH, 'r') as f:
            print("check")
            files = json.load(f)
            quiz_questions = [FileDetails(**data) for data in files]


    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"message": "File not found"})
    
    return quiz_questions

@app.post("/add_question_to_quiz")
async def add_question_to_quiz(american_question_object: AmericanQuestionObjectWithFileName):
    print("hey")
    print(american_question_object.answers, american_question_object.question)
    return save_quiz_question(american_question_object)


@app.get("/load_quiz_names")
async def load_quiz():
    print("hey")
    list_quizes = list_quiz_files("db/quiz_ps")
    print(list_quizes)
    return list_quizes


@app.post("/load_specific_quiz")
async def load_specific_quiz(file_name: str = Form(...)):
    print(file_name)
    american_questions = load_american_questions_from_quiz(file_name)
    print(american_questions)
    return american_questions 



