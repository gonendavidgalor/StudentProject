from utils.shared_functions import get_openai_client


# Temporary function
def create_file(client, file_path):
    file = client.files.create(
        file=open(file_path, "rb"),
        purpose='assistants'
    )

    return file.id

# Temporary function
def get_file_id():
    client = get_openai_client()
    file_id = create_file(client, "utils\md_files\ps1.md")
    print(file_id)

    return file_id




# TODO: should be the real one, need to understand why it is not recognizing the .md suffix
# async def get_file_id(file):
#     client = get_openai_client()
#     file_stream = await file.read()
#     file_id = create_file(client, file_stream)
#     print(file_id)

#     return file_id

# TODO: should be the real function
# def create_file(client, file_stream):
#     file = client.files.create(
#         file=file_stream,
#         purpose='assistants'
#     )
#     return file.id





