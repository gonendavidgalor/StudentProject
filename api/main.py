from fastapi import FastAPI
# from common.upload_file import get_file_id
from check import generate_questions
# from common.generate_questions import generate_questions
# from check import get_file_id
# from common.generate_questions import generate_questions

app = FastAPI()

# TODO: Add a route to upload a file from UI
@app.get("/upload_file")
def upload_file():
    return generate_questions()

@app.get("/generate_questions")
def generate_questions():
    return generate_questions()
