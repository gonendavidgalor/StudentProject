from typing import List
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

from pydantic import BaseModel

app = FastAPI()

class FileDetails(BaseModel):
    name: str
    content: str

async def load_content():
    FILES_JSON_PATH = 'db/files.json'

    try:
        with open(FILES_JSON_PATH, 'r') as f:
            print("check")
            files = json.load(f)
            quiz_questions = [FileDetails(**data) for data in files]


    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"message": "File not found"})
    
    return quiz_questions
