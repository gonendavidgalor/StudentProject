from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from common.questions.extract_file_id_by_file_name import extract_file_ids
from common.questions.load_quiz import list_quiz_files
from common.questions.load_specific_quiz import load_american_questions_from_quiz
from common.files.upload_file import get_file_id
from common.files.load_files import load_content
from common.questions.generate_questions import generate_a_question
from common.questions.ask_questions import ask_a_question
from typing import Optional
from common.files.add_file_to_db import save_file_content_for_filename
from utils.shared_objects import AmericanQuestionObjectWithFileName
from common.questions.add_quiz_question import save_quiz_question
from common.questions.delete_question import delete_question
import asyncio




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],  # The origins permitted to make requests, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    print("file", file)
    return await get_file_id(file)

@app.post("/generate_question")
def generate_questions(file_id: str = Form(...), thread_id: Optional[str] = Form(None), assistant_id: Optional[str] = Form(None) ):
    print(file_id)
    return generate_a_question(file_id, thread_id, assistant_id)

@app.get("/filename_to_fileid")
def generate_questions():
    return extract_file_ids()


@app.post("/ask_question")
def ask_questions(file_id: str = Form(...), question: str = Form(...), thread_id: Optional[str] = Form(None), assistant_id: Optional[str] = Form(None) ):
    print(thread_id, "thread_id5")
    print(assistant_id, "assistant_id5")
    return ask_a_question(file_id, question)


@app.post("/save_file")
async def save_file(file: UploadFile = File(...), file_id: str = Form(...)):
    await save_file_content_for_filename(file, file_id)


# Try to make it look better
@app.get("/load_files")
async def load_files():
    return await load_content()
    

@app.post("/add_question_to_quiz")
async def add_question_to_quiz(american_question_object: AmericanQuestionObjectWithFileName):
    return save_quiz_question(american_question_object)


@app.get("/load_quiz_names")
async def load_quiz():
    print("hey")
    list_quizes = list_quiz_files("db/quiz_ps")
    print(list_quizes)
    return list_quizes


@app.post("/load_specific_quiz")
async def load_specific_quiz(file_name: str = Form(...)):
    return load_american_questions_from_quiz(file_name)


@app.delete("/delete_question_from_archive")
async def delete_question_from_archive(file_name: str = Form(...), quiz_id: str = Form(...)):
    return delete_question(file_name, quiz_id)
