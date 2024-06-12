from utils.shared_functions import get_openai_client

NO_INFORMATION_SUPPLIED = "No information supplied in the file."

class AnswerObject():
    def __init__(self, content, assistant_id, thread_id):
        self.content = content
        self.thread_id = thread_id
        self.assistant_id = assistant_id


def get_thread(client, file_id):
    print("check2")
    thread = client.beta.threads.create(
      messages=[
        {
          "role": "user",
          "content": "based on a question asked I want to generate an answer from the information of the provided files, it can be just one of the files",
          "attachments": [
          {
            "file_id": file_id,
            "tools": [{"type": "file_search"}]
          } 
         ]       
        }
      ]
      
    )
    print("check22")

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
      instructions = f""" Based on the content of the uploaded file, answer this {question}. 
      Format the output as follows:
        Based on the content of the uploaded file: ...

      If you don't find the answer in the file, type "No information supplied in the file."

        If you see steps, for example 1. 2. 3. etc, before each one of the steps should be for having a linegap
      
      don't add any other information in the output
      """
      )

    if run.status == 'completed': 
      messages = client.beta.threads.messages.list(
        thread_id=thread_id
      )
    
    content = messages.data[0].content[0].text.value
    
    return content


def generate_fallback_answer(client, question):
  print("check7")
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": f"""Answer the following question: {question}. start with the following: 
        'Based on the chatGPT engine:...'"""}
    ],
    max_tokens=200

  )
  print(completion, "completion")
  return completion.choices[0].message.content



    # response = client.chat.completions.create(
    #     engine="text-davinci-003",
    #     prompt=f"""Answer the following question: {question}. start with the following: 
    #     'No information found in the file, based on chatGPT engine here is the answer:...'""",
    #     max_tokens=150
    # )


def generate_answer(client, thread_id, assistant_id, question):
  print("check5")
  try:
    content = get_data_content(client, thread_id, assistant_id, question)
    print("check6")
    print(NO_INFORMATION_SUPPLIED not in content, "NO_INFORMATION_SUPPLIED not in content:")
    if NO_INFORMATION_SUPPLIED not in content:
      return AnswerObject(content, thread_id=thread_id, assistant_id=assistant_id)

    else:
      fallback_content = generate_fallback_answer(client, question)
      return AnswerObject(fallback_content, thread_id=thread_id, assistant_id=assistant_id)
    
  except Exception as e:
    fallback_content = generate_fallback_answer(client, question)
    return AnswerObject(fallback_content, thread_id=thread_id, assistant_id=assistant_id)


def make_infrustructure_for_questions(file_id, client, question):
    thread = get_thread(client, file_id)
    print("check3")
    assistant = client.beta.assistants.create(
    instructions=f"Based on the content of the uploaded files, answer the following question: {question}",
    model="gpt-3.5-turbo",
    tools=[{"type": "file_search"}],
  #   tool_resources={
  #   "file_search": {
  #     "file_ids": [file_id]
  #   }
  # }
    # file_ids=[file_id]
  )
    
    print("check44")
    
    return thread, assistant
    
def ask_a_question(file_id, question):
    client = get_openai_client()
    print("check1")
    thread, assistant = make_infrustructure_for_questions(file_id, client, question)
    print("check4")
    answer_object = generate_answer(client, thread.id, assistant.id, question)
  # def ask_a_question(question, thread_id, assistant_id):
    # client = get_openai_client()
    # if thread_id == None or assistant_id == None:
    #   # thread, assistant = make_infrustructure_for_questions(client, question)
    #   # print("check1234", thread, assistant)
    #   print("current file id", file_id)
    #   thread, assistant = make_infrustructure_for_questions(file_id, client, question)
    #   answer_object = generate_answer(client, thread.id, assistant.id, question)
    # else: 
    #   answer_object = generate_answer(client, thread_id, assistant_id, question)
    
    if answer_object.content is not None:
      answer_object.content = answer_object.content.replace("Answer: ", "", 1)  

    return answer_object