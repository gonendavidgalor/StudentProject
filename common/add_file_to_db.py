from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import json
from pathlib import Path

app = FastAPI()

FILES_JSON_PATH = 'db\\files.json'
Path(FILES_JSON_PATH).touch(exist_ok=True)
print("hey")
async def add_file(file):
    print("hey1")
    print(file)
    print("hey2")
    if file:
        content = await file.read()  # Read file content as bytes
        print("hey3")
        file_details = {
            'name': file.filename,
            'content': content.decode('utf-8')  # Assuming file content is utf-8 text
        }

        # Save file details to JSON
        print(file_details)
        print("right!")
        if not is_file_exist(file.filename):
            save_file_details(file_details)
            return JSONResponse(status_code=200, content={"message": "File uploaded successfully", "filename": file.filename})
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

def is_file_exist(filename):
    """ Check if a file with the given name already exists in the JSON storage """
    with open(FILES_JSON_PATH, 'r+') as f:
        files = json.load(f)
        for file in files:
            print(file['name'])
            if file['name'] == filename:
                return True
    return False