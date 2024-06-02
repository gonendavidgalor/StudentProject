import io
from utils.shared_functions import get_openai_client
import aiofiles # type: ignore

from fastapi import FastAPI, File, UploadFile
import openai

# app = FastAPI()


# async def get_file_id(file: UploadFile):
#     client = get_openai_client()
#     file_id = await create_file(client, file)
#     # print(file_id)
#     return file_id

# async def create_file(client, file: UploadFile):
#     file_content = await file.read()  # Read the file content into memory
#     file_stream = io.BytesIO(file_content)  # Create an in-memory file-like object from the content

#     response = client.File.create(
#         file=(file.filename, file_stream),
#         purpose='assistants'
#     )
#     return response['id']



#     with open(file.filename, 'rb') as f:
#         file_data = f.read()

#     response = client.File.create(
#         file=(file.filename, file_data),
#         purpose='assistants'
#     )
#     return response.id

# async def get_file_id(file):
#     client = get_openai_client()
#     file_id = await create_file(client, file)
#     print(file_id)
#     return file_id

# async def create_file(client, file):
#     async with aiofiles.open(file, 'rb') as f:
#         file_stream = await f.read()
#     file = client.files.create(
#         file=(file, file_stream),  # Include the filename here
#         purpose='assistants'
#     )
#     return file.id

# # Temporary function
# def create_file(client, file_path):
#     file = client.files.create(
#         file=open(file_path, "rb"),
#         purpose='assistants'
#     )

#     return file.id

# # Temporary function
# def get_file_id():
#     client = get_openai_client()
#     file_id = create_file(client, "utils\md_files\ps1.md")
#     print(file_id)

#     return file_id




# TODO: should be the real one, need to understand why it is not recognizing the .md suffix
async def get_file_id(file):
    client = get_openai_client()
    file_stream = await file.read()
    file_id = create_file(client, file_stream, file.filename)
    print(file_id)

    return file_id

# # TODO: should be the real function
def create_file(client, file_stream, file_name):
    file = client.files.create(
    file=(file_name, io.BytesIO(file_stream)),
    purpose='assistants',
    )
    return file.id
