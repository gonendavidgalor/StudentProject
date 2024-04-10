from fastapi import FastAPI
from common.upload_file import get_file_id
from common.generate_questions import generate_questions

app = FastAPI()

# TODO: Add a route to upload a file from UI
@app.get("/upload_file")
def upload_file():
    return get_file_id()

@app.get("/generate_questions")
def upload_file():
    return get_file_id()
