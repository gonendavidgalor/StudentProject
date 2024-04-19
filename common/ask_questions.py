import os
import openai # type: ignore

from dotenv import load_dotenv # type: ignore

class AnswerObject:
    def __init__(self, content, assistant_id, thread_id):
        self.content = content
        self.assistant_id = assistant_id
        self.thread_id = thread_id

def get_openai_client():
    load_dotenv()

    api_key = os.getenv("API_KEY")

    if api_key is None:
        raise ValueError("API_KEY not found in environment variables")

    client = openai.OpenAI(api_key=api_key)

    return client


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


def get_data_content(client, thread_id, assistant_id, question):
    run = client.beta.threads.runs.create_and_poll(
      thread_id=thread_id,
      assistant_id=assistant_id,
      instructions = f""" Based on the content of the document, answer this {question}. 
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
    print(type(content))

    return AnswerObject(content, thread_id, assistant_id)
    
  except Exception as e:
    print(f"Try again")


def make_infrustructure_for_questions(file_id, client, question):
    thread = get_thread(client, file_id)
    print("three")
    print(question)
    print("three")
    assistant = client.beta.assistants.create(
    instructions=f"Based on the content of the uploaded file, answer the following question: {question}",
    model="gpt-4-turbo",
    tools=[{"type": "retrieval"}],
    file_ids=[file_id]
  )
    print("four")
    
    return thread, assistant
    
def ask_a_question(file_id, question, thread_id, assistant_id):
    print("one")
    client = get_openai_client()
    if thread_id == None or assistant_id == None:
      thread, assistant = make_infrustructure_for_questions(file_id, client, question)
      answer_object = generate_answer(client, thread.id, assistant.id, question)
    else: 
      answer_object = generate_answer(client, thread_id, assistant_id, question)
    if answer_object.content is not None:
      answer_object.content = answer_object.content.replace("Answer: ", "", 1)  

    print("Answer generated successfully")
    print(answer_object)
    return answer_object

# def ask_a_question(file_id, question):
#     print("one")
#     client, thread, assistant = make_infrustructure_for_questions(file_id, question)
#     answer = generate_answer(client, thread, assistant, question)
#     if answer is not None:
#       answer = answer.replace("Answer: ", "", 1)  

#     print("Answer generated successfully")
#     print(answer)
#     return answer


# def ask_a_question(file_id, question):
#     answer = get_answer_data('Answer: ```typescript\nlet movieIds = []\nmovieLists.forEach(category => category.videos.forEach(video => movieIds.push(video.id)));\nconsole.log(`movieIds=${movieIds}`); // ==> movieIds=70111470,654356453,65432445,675465\n```【7†source】')
#     # answer[0].content_type = "text"
#     print(answer[0])
#     print(answer[0].answer)
#     print(answer[0].content_type)
#     return answer

# def main():
#     # print(ask_a_question('file-SZMmhLtdAoPmNbSAiMY66nIG', 'Can you show me the part of code of typescript of forEach in the document?'))
#     print(get_answer_data('Answer: ```typescript\nlet movieIds = []\nmovieLists.forEach(category => category.videos.forEach(video => movieIds.push(video.id)));\nconsole.log(`movieIds=${movieIds}`); // ==> movieIds=70111470,654356453,65432445,675465\n```【7†source】'))
# if __name__ == "__main__":
#     main()