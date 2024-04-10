import os
import openai # type: ignore

from dotenv import load_dotenv # type: ignore
# Check it
# from utils.questions import AmericanQuestionObject

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
          "content": "I want to generate a question about this file. Can you help me with that",
          "file_ids": [file_id]
        }
      ]
    )

    return thread


def get_data_content(client, thread, assistant):
    run = client.beta.threads.runs.create_and_poll(
      thread_id=thread.id,
      assistant_id=assistant.id,
      instructions = """Generate a multiple-choice question based on the content of the file. The question should be specific to the content and avoid generic or obvious answers. Format the output as follows:

    Question: ...
    Answers:
    1) ...
    2) ...
    3) ...
    4) ...

    Right answer: [number]

    Ensure all answer choices are plausible and related to the file content, with only one correct answer. Exclude generic answers like 'Null' or 'All of the above'.
    and don't add any other information in the output.
    """

      )

    if run.status == 'completed': 
      messages = client.beta.threads.messages.list(
        thread_id=thread.id
      )
    
    content = messages.data[0].content[0].text.value
    
    return content


def get_message_data(content):
    parts = content.split("\n")
  
    # Extract the question
    question = parts[0].replace("Question: ", "").strip()
  
    # Extract the answers
    answers_start = parts.index("Answers:")+1
    answers_end = answers_start + 4
    answers = [part[3:].strip() for part in parts[answers_start:answers_end]]

    # Extract the correct answer number
    right_answer = int(parts[answers_end+1].replace("Right answer: ", "").strip()[0])

    return question, answers, right_answer


def generate_american_questions(client, thread, assistant):
    while True:
      user_input = input("Do you want to generate a question? (y/n): ")
      if user_input == 'n':
          break
      elif user_input == 'y':
        try:
          content = get_data_content(client, thread, assistant)
          question, answers, right_answer = get_message_data(content)
          print(question, answers, right_answer)
        except Exception as e:
           print(f"Try again")

def generate_american_question(client, thread, assistant):
    while True:
      user_input = input("Do you want to generate a question? (y/n): ")
      if user_input == 'n':
          break
      elif user_input == 'y':
        try:
          content = get_data_content(client, thread, assistant)
          question, answers, right_answer = get_message_data(content)
          print(question, answers, right_answer)
          return AmericanQuestionObject(question, answers, right_answer)
          
        except Exception as e:
           print(f"Try again")

def make_infrustructure_for_questions(file_id):
    client = get_openai_client()
    thread = get_thread(client, file_id)
    assistant = client.beta.assistants.create(
    instructions=("You should generate a question about the file."),
    model="gpt-3.5-turbo",
    tools=[{"type": "retrieval"}],
    file_ids=[file_id]
  )
    
    return client, thread, assistant
    
# def generate_questions():
#     file_id = 'file-IXD1QpgQiJoS9TmhIjOI94Pf'
#     client, thread, assistant = make_infrustructure_for_questions(file_id)
#     american_question = generate_american_question(client, thread, assistant)    
#     print(american_question.question, american_question.answers, american_question.right_answer)
#     print("Question generated successfully")


def main():
    file_id = 'file-HbOl7TwfrLvLwAzdi1ya0GZB'
    client, thread, assistant = make_infrustructure_for_questions(file_id)
    generate_american_questions(client, thread, assistant)    

  
if __name__ == "__main__":
    main()