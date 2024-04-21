import os
import openai # type: ignore
from dotenv import load_dotenv # type: ignore

def get_openai_client():
    load_dotenv()

    api_key = os.getenv("API_KEY")

    if api_key is None:
        raise ValueError("API_KEY not found in environment variables")

    client = openai.OpenAI(api_key=api_key)

    return client

def create_file(client, file_stream):
    print("check")
    print("check")
    file = client.files.create(
        file=file_stream,
        purpose='assistants'
    )
    return file.id

# TODO: should be the real one, need to understand why it is not recognizing the .md suffix
# async def get_file_id(file):
#     client = get_openai_client()
#     file_stream = await file.read()
#     file_id = create_file(client, file_stream)
#     print(file_id)

#     return file_id

# Temporary function
def create_file(client, file_path):
    file = client.files.create(
        file=open(file_path, "rb"),
        purpose='assistants'
    )

    return file.id

def get_file_id():
    client = get_openai_client()
    file_id = create_file(client, "utils\md_files\ps1.md")
    print(file_id)

    return file_id

# def get_file_id(file):
#     client = get_openai_client()
#     file_id = create_file(client, file_path)
#     print(file_id)

#     return file_id




