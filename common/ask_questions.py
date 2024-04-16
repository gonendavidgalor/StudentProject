import os
import openai # type: ignore

from dotenv import load_dotenv # type: ignore
# Check it
# from utils.questions import AmericanQuestionObject

class AmericanQuestionObject:
    def __init__(self, question, answers, right_answer):
        self.question = question
        self.answers = answers
        self.right_answer = right_answer

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


def get_data_content(client, thread, assistant):
    run = client.beta.threads.runs.create_and_poll(
      thread_id=thread.id,
      assistant_id=assistant.id,
      instructions = """Generate a solid answer for the asked question"""
      )

    if run.status == 'completed': 
      messages = client.beta.threads.messages.list(
        thread_id=thread.id
      )
    
    content = messages.data[0].content[0].text.value
    
    return content


def get_answer_data(content):
    print(content)
    parts = content.split("\n")
    print(parts)
  
    return content


# def generate_answer(client, thread, assistant):
#     while True:
#       user_input = input("Do you want to generate a question? (y/n): ")
#       if user_input == 'n':
#           break
#       elif user_input == 'y':
#         try:
#           content = get_data_content(client, thread, assistant)
#           question, answers, right_answer = get_answer_data(content)
#           print(question, answers, right_answer)
#         except Exception as e:
#            print(f"Try again")

def generate_answer(client, thread, assistant):
  try:
    content = get_data_content(client, thread, assistant)
    question, answers, right_answer = get_answer_data(content)
    return AmericanQuestionObject(question, answers, right_answer)
    
  except Exception as e:
    print(f"Try again")


def make_infrustructure_for_questions(file_id, question):
    client = get_openai_client()
    thread = get_thread(client, file_id)
    print("three")
    print(question)
    print("three")
    assistant = client.beta.assistants.create(
    instructions=f"Based on the content of the uploaded file, answer the following question: {question}",
    model="gpt-3.5-turbo",
    tools=[{"type": "retrieval"}],
    file_ids=[file_id]
  )
    print("four")
    
    return client, thread, assistant
    
def ask_a_question(file_id, question):
    print("one")
    client, thread, assistant = make_infrustructure_for_questions(file_id, question)
    answer = generate_answer(client, thread, assistant)    
    print("Answer generated successfully")
    return answer
