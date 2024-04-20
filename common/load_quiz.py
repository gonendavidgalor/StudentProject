from fastapi import FastAPI
from typing import List
import os

app = FastAPI()

@app.get("/load_quiz")
async def load_quiz() -> List[str]:
    return list_quiz_files("db/quiz_ps")


import glob

def list_quiz_files(directory: str) -> List[str]:
    # Create the full path pattern to match files
    path_pattern = os.path.join(directory, "quiz_ps*.json")
    # List all files matching the pattern
    files = glob.glob(path_pattern)
    # Extract quiz names from filenames
    quiz_names = [os.path.basename(f).replace('.json', '') for f in files]
    return quiz_names
