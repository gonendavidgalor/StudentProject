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

def create_file(client, file_stream, file_name):
    print("check")
    print("File name", file_name)
    print("check")
    file = client.files.create(
        file=file_stream,
        purpose='assistants'
    )
    return file.id


async def get_file_id(file):
    client = get_openai_client()
    file_stream = await file.read()
    file_id = create_file(client, file_stream, file.filename)
    print(file_id)

    return file_id

# async def get_file_id(file):
#     client = get_openai_client()
#     response = client.files.create(file=file.file.read(), purpose='answers')
#     return {"file_id": response['id']}

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

# def get_file_id(file_path):
#     client = get_openai_client()
#     file_id = create_file(client, file_path)
#     print(file_id)

#     return file_id




