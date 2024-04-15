from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from common.upload_file import get_file_id
from common.generate_questions import generate_a_question


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
    return await get_file_id(file)

@app.post("/generate_question")
def generate_questions(file_id: str = Form(...)):
    print(file_id)
    return generate_a_question(file_id)

# @app.get("/generate_question")
# def generate_questions():
#     file_id = 'file-SQztHzqhqbjZfs6wsNX4ux44'
#     return generate_a_question(file_id)


