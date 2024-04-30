from typing import List
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

from pydantic import BaseModel

app = FastAPI()

FILES_JSON_PATH = 'db/files.json'

class FileDetails(BaseModel):
    name: str
    content: str

async def load_content():
    print("check1")
    return "hey"
    # try:
    #     with open(FILES_JSON_PATH, 'r') as f:
    #         print("check")
    #         files = json.load(f)
    #         # quiz_questions = [FileDetails(**data) for data in files]
    #         quiz_questions = []
    #         return quiz_questions

    # except FileNotFoundError:
    #     return JSONResponse(status_code=404, content={"message": "File not found"})
    # except json.JSONDecodeError:
    #     return JSONResponse(status_code=500, content={"message": "Error decoding JSON"})
    # except Exception as e:
    #     return JSONResponse(status_code=500, content={"message": str(e)})
