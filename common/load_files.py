from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

app = FastAPI()

FILES_JSON_PATH = 'files.json'

async def load_content():
    try:
        with open(FILES_JSON_PATH, 'r') as f:
            files = json.load(f)
            for file in files:
                print(f"File Name: {file['name']}")
                print(f"Content: {file['content'][:100]}...") 
            return JSONResponse(status_code=200, content=files)
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"message": "File not found"})
    except json.JSONDecodeError:
        return JSONResponse(status_code=500, content={"message": "Error decoding JSON"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
