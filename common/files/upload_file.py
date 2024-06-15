import io
from utils.shared_functions import get_openai_client


# TODO: should be the real one, need to understand why it is not recognizing the .md suffix
async def get_file_id(file):
    client = get_openai_client()
    file_stream = await file.read()
    file_id = create_file(client, file_stream, file.filename)

    return file_id

# TODO: should be the real function
def create_file(client, file_stream, file_name):
    file = client.files.create(
        file=(file_name, io.BytesIO(file_stream)),
        purpose='assistants'
    )
    
    return file.id
