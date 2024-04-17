import os
import openai # type: ignore

from dotenv import load_dotenv # type: ignore

class AnswerObject:
    def __init__(self, content_type, answer):
        self.content_type = content_type
        self.answer = answer


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


def get_data_content(client, thread, assistant, question):
    run = client.beta.threads.runs.create_and_poll(
      thread_id=thread.id,
      assistant_id=assistant.id,
      instructions = f""" Based on the content of the document, answer this {question}. 
      Format the output as follows:
        Answer: ...
      
      don't add any other information in the output
      """
      )

    if run.status == 'completed': 
      messages = client.beta.threads.messages.list(
        thread_id=thread.id
      )
    
    content = messages.data[0].content[0].text.value
    
    return content


def get_answer_data(content):
    answers_array = []

    # Check if the content starts with 'Answer: ```typescript'
    if content.startswith("Answer: ```typescript"):
        # Find the start and end of the TypeScript block
        start = content.find("```typescript\n") + len("```typescript\n")
        end = content.rfind("\n```")
        if start != -1 and end != -1:
            # Extract the code between these markers
            code = content[start:end]
            # Create an AnswerObject with the extracted code
            answer_object = AnswerObject(content_type='typescript', answer=code)
            answers_array.append(answer_object)

    return answers_array



def generate_answer(client, thread, assistant, question):
  try:
    content = get_data_content(client, thread, assistant, question)
    answers = get_answer_data(content)
    return answers
    
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
    model="gpt-4-turbo",
    tools=[{"type": "retrieval"}],
    file_ids=[file_id]
  )
    print("four")
    
    return client, thread, assistant
    
def ask_a_question(file_id, question):
    print("one")
    client, thread, assistant = make_infrustructure_for_questions(file_id, question)
    answer = generate_answer(client, thread, assistant, question)    
    print("Answer generated successfully")
    return answer


def main():
    # print(ask_a_question('file-SZMmhLtdAoPmNbSAiMY66nIG', 'Can you show me the part of code of typescript of forEach in the document?'))
    print(get_answer_data('Answer: ```typescript\nlet movieIds = []\nmovieLists.forEach(category => category.videos.forEach(video => movieIds.push(video.id)));\nconsole.log(`movieIds=${movieIds}`); // ==> movieIds=70111470,654356453,65432445,675465\n```【7†source】'))
if __name__ == "__main__":
    main()