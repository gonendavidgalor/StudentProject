from utils.shared_functions import get_openai_client


class AmericanQuestionObject:
    def __init__(self, question, answers, right_answer, assistant_id, thread_id):
        self.question = question
        self.answers = answers
        self.right_answer = right_answer
        self.assistant_id = assistant_id
        self.thread_id = thread_id



def get_thread(client, file_id):
    thread = client.beta.threads.create(
      messages=[
        {
          "role": "user",
          "content": "I want to generate a question about this file. Can you help me with that",
          # "file_ids": [file_id]
          "attachments": [
          {
            "file_id": file_id,
            "tools": [{"type": "file_search"}]
          } 
          ]
        }
      ]
    )

    return thread


def get_data_content(client, thread_id, assistant_id):
    run = client.beta.threads.runs.create_and_poll(
      thread_id=thread_id,
      assistant_id=assistant_id,
      instructions = """Generate a multiple-choice question based on the content of the file.
        The question should be about the content and avoid questions about specific examples.
        
        Format the output as follows:

        Question: ...
        Answers:
        1) ...
        2) ...
        3) ...
        4) ...

        Right answer: [number]

        Ensure all answer choices are plausible and related to the file content, with only one correct answer. Exclude generic answers like 'Null' or 'All of the above'.
        and don't add any other information in the output.

        If I ask you to generate one more question, please generate a different question than the previous one.
        """

      )

    if run.status == 'completed': 
      messages = client.beta.threads.messages.list(
        thread_id=thread_id
      )
    
    content = messages.data[0].content[0].text.value
    
    return content


def get_message_data(content):
    print(content)
    parts = content.split("\n")
    question = parts[0].replace("Question: ", "").strip()
  
    answers_start = parts.index("Answers:")+1
    answers_end = answers_start + 4
    answers = [part[3:].strip() for part in parts[answers_start:answers_end]]

    right_answer = int(parts[answers_end+1].replace("Right answer: ", "").strip()[0])

    return question, answers, right_answer


def generate_american_question(client, file_id, assistant, thread):
  tries = 3
  while tries > 0:
    try:
      thread_id, assistant_id = thread.id, assistant.id
      content = get_data_content(client, thread_id, assistant_id)
      question, answers, right_answer = get_message_data(content)
      print("check1")
      return AmericanQuestionObject(question, answers, right_answer, assistant_id, thread_id)
      
    except Exception as e:
      tries -= 1
      thread, assistant = make_infrustructure_for_questions(file_id, client)
      print("failed to generate a question, trying again")
    
  print("failed to generate a question, exiting")


def make_infrustructure_for_questions(file_id, client):
    thread = get_thread(client, file_id)
    assistant = client.beta.assistants.create(
    instructions=("You should generate a question about the file. the question should be not about a specific example, but about general topic"),
    model="gpt-3.5-turbo",
    # tools=[{"type": "retrieval"}],
    # file_ids=[file_id]
    tools=[{"type": "file_search"}],
  )
    
    return thread, assistant
    
def generate_a_question(file_id, thread_id, assistant_id):
    client = get_openai_client()
    thread, assistant = make_infrustructure_for_questions(file_id, client)
    american_question = generate_american_question(client, file_id, assistant, thread)  
    print("check2")
    
    # if thread_id == None or assistant_id == None:
    #   thread, assistant = make_infrustructure_for_questions(file_id, client)
    #   american_question = generate_american_question(client, assistant.id, thread.id)    
    # else:
    #   american_question = generate_american_question(client, assistant_id, thread_id)

    return american_question
