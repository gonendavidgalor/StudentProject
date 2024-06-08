from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
from pathlib import Path

app = FastAPI()

FILES_JSON_PATH = 'db\\files.json'
Path(FILES_JSON_PATH).touch(exist_ok=True)
FILES_ID_JSON_PATH = 'db\\files_id.json'
Path(FILES_ID_JSON_PATH).touch(exist_ok=True)

async def add_file_to_db(file):
        content = await file.read()
        file_details = {
            'name': file.filename,
            'content': content.decode('utf-8')
        }

        print("check7")

        save_file_details(file_details)
        return JSONResponse(status_code=200, content={"message": "File uploaded successfully", "filename": file.filename})

        
async def add_file_id_to_db(file, file_id):
    print("check22")
    file_id_details = {
        'name': file.filename,
        'file_id': file_id
    }
    print("check3")

    save_file_id_details(file_id_details)

async def add_file(file, file_id):
    if file:
        if not is_file_exist(file.filename):
            await add_file_id_to_db(file, file_id)
            return await add_file_to_db(file)
            
        else:
            return JSONResponse(status_code=400, content={"message": "File already exists", "filename": file.filename})
        
    return JSONResponse(status_code=400, content={"message": "No file uploaded"})

def save_file_details(file_details):
    """ Save file details to a JSON file """
    with open(FILES_JSON_PATH, 'r+') as f:
        files = json.load(f)
        files.append(file_details)
        f.seek(0)
        f.truncate()
        json.dump(files, f, indent=4)

def save_file_id_details(file_details):
    """ Save file_id details to a JSON file """
    with open(FILES_ID_JSON_PATH, 'r+') as f:
        print("check5")
        files = json.load(f)
        files.append(file_details)
        f.seek(0)
        f.truncate()
        json.dump(files, f, indent=4)
        print("check6")

def is_file_exist(filename):
    """ Check if a file with the given name already exists in the JSON storage """
    with open(FILES_JSON_PATH, 'r+') as f:
        files = json.load(f)
        for file in files:
            if file['name'] == filename:
                return True
    return False