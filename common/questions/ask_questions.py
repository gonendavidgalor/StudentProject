import json
from utils.shared_functions import get_openai_client


class AnswerObject():
    def __init__(self, content, assistant_id, thread_id):
        self.content = content
        self.thread_id = thread_id
        self.assistant_id = assistant_id

FILES_ID_JSON_PATH = 'db\\files_id.json'

def extract_file_ids():
    with open(FILES_ID_JSON_PATH, 'r') as file:
        data = json.load(file)  # Load the JSON content
        file_ids = [item['file_id'] for item in data]  # Extract file_ids
    return file_ids

def get_thread(client, file_id):
    thread = client.beta.threads.create(
      messages=[
        {
          "role": "user",
          "content": "based on a question asked I want to generate an answer from the information of that file. Can you help me with that",
          "file_ids": [file_id]
        }
      ]
    )

    return thread

def get_thread_for_files(client, file_ids):
    thread = client.beta.threads.create(
      messages=[
        {
          "role": "user",
          "content": "Please use the information in the provided files to help me answer a question.",
          "file_ids": file_ids
        }
      ]
    )
    print(thread, "thread")

    return thread


def get_data_content(client, thread_id, assistant_id, question):
    
    print("check12345")
    run = client.beta.threads.runs.create_and_poll(
      thread_id=thread_id,
      assistant_id=assistant_id,
      instructions = f""" Based on the content of the uploaded files, answer this {question}. 
      Format the output as follows:
        Answer: ...
      
      don't add any other information in the output
      """
      )

    if run.status == 'completed': 
      messages = client.beta.threads.messages.list(
        thread_id=thread_id
      )
    
    content = messages.data[0].content[0].text.value
    
    return content



def generate_answer(client, thread_id, assistant_id, question):
  try:
    content = get_data_content(client, thread_id, assistant_id, question)
    return AnswerObject(content, thread_id=thread_id, assistant_id=assistant_id)
    
  except Exception as e:
    print(f"Try again")


def make_infrustructure_for_questions(client, question):
    # thread = get_thread(client, file_id)
    print("check123")
    file_ids = extract_file_ids()
    print(file_ids)
    thread = get_thread_for_files(client, file_ids)
    assistant = client.beta.assistants.create(
    instructions=f"Based on the content of the uploaded files, answer the following question: {question}",
    model="gpt-4-turbo",
    tools=[{"type": "retrieval"}],
    # file_ids=file_ids
    file_ids=file_ids
  )
    
    return thread, assistant

# def make_infrustructure_for_questions(file_id, client, question):
#     # thread = get_thread(client, file_id)
#     file_ids = extract_file_ids()
#     print(file_ids)
#     thread = get_thread_for_files(client, file_ids)
#     assistant = client.beta.assistants.create(
#     instructions=f"Based on the content of the uploaded files, answer the following question: {question}",
#     model="gpt-4-turbo",
#     tools=[{"type": "retrieval"}],
#     file_ids=file_ids[2]
#   )
    
#     return thread, assistant
    
def ask_a_question(question, thread_id, assistant_id):
    print("check123")
    client = get_openai_client()
    print("check1234")

    if thread_id == None or assistant_id == None:
      thread, assistant = make_infrustructure_for_questions(client, question)
      print("check1234", thread, assistant)
      # thread, assistant = make_infrustructure_for_questions(file_id, client, question)
      answer_object = generate_answer(client, thread.id, assistant.id, question)
    else: 
      answer_object = generate_answer(client, thread_id, assistant_id, question)
    
    if answer_object.content is not None:
      answer_object.content = answer_object.content.replace("Answer: ", "", 1)  

    return answer_object