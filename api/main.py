from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from common.upload_file import get_file_id
from common.generate_questions import generate_a_question
from common.ask_questions import ask_a_question
from typing import Optional


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],  # The origins permitted to make requests, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Just basic for checking the UI
@app.get("/upload_file")
def upload_file():
    return get_file_id()

# Should be the real one
@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    # return await get_file_id(file)
    return get_file_id()

@app.post("/generate_question")
def generate_questions(file_id: str = Form(...), thread_id: Optional[str] = Form(None), assistant_id: Optional[str] = Form(None) ):
    print(file_id)
    return generate_a_question(file_id, thread_id, assistant_id)

@app.get("/generate_question")
def generate_questions():
    file_id = 'file-cvwILzT6xpvF5PiPoFr51Kck'
    return generate_a_question(file_id)


# @app.post("/ask_question")
# def ask_questions(file_id: str = Form(...), question: str = Form(...)):
#     return ask_a_question(file_id, question)

@app.post("/ask_question")
def ask_questions(file_id: str = Form(...), question: str = Form(...), thread_id: Optional[str] = Form(None), assistant_id: Optional[str] = Form(None) ):
    return ask_a_question(file_id, question, thread_id, assistant_id)



