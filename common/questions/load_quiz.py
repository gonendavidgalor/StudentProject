from fastapi import FastAPI
from typing import List
import os

app = FastAPI()

PATH_PATTERN = "quiz_ps*.json"

import glob

def list_quiz_files(directory: str) -> List[str]:
    # path_pattern = os.path.join(directory, PATH_PATTERN)
    # files = glob.glob(path_pattern)
    # quiz_names = [os.path.basename(f).replace('.json', '') for f in files]
    files = os.listdir(directory)
    quiz_names = [os.path.basename(f).replace('.json', '').replace('_', ' ') for f in files]

    return quiz_names
