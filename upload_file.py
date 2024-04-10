import os
import openai # type: ignore

from dotenv import load_dotenv # type: ignore

def get_openai_client():
    load_dotenv()

    api_key = os.getenv("API_KEY")

    if api_key is None:
        raise ValueError("API_KEY not found in environment variables")

    client = openai.OpenAI(api_key=api_key)

    return client


def create_file(client, file_path):
    file = client.files.create(
        file=open(file_path, "rb"),
        purpose='assistants'
    )

    return file

def get_thread(client, file):
    thread = client.beta.threads.create(
      messages=[
        {
          "role": "user",
          "content": "I want to generate a question about this file. Can you help me with that",
          "file_ids": [file.id]
        }
      ]
    )

    return thread


def get_a_question(client, thread, assistant):
    run = client.beta.threads.runs.create_and_poll(
      thread_id=thread.id,
      assistant_id=assistant.id,
      instructions = """Generate a multiple-choice question based on the content of the file. The question should be specific to the content and avoid generic or obvious answers. Format the output as follows:

    Question: '...'
    Answers:
    1) '...'
    2) '...'
    3) '...'
    4) '...'

    Right answer: [number]

    Ensure all answer choices are plausible and related to the file content, with only one correct answer. Exclude generic answers like 'Null' or 'All of the above'.
    and don't add any other information in the output.
    """

      )


    if run.status == 'completed': 
      messages = client.beta.threads.messages.list(
        thread_id=thread.id
      )
    
    return messages


def main():
    client = get_openai_client()
    file = create_file(client, "ps1.md")
    thread = get_thread(client, file)
    assistant = client.beta.assistants.create(
    instructions=("You should generate a question about the file."),
    model="gpt-4-turbo-preview",
    tools=[{"type": "retrieval"}],
    file_ids=[file.id]
  )
  
    messages = get_a_question(client, thread, assistant)

  


    questions = []

    for message in messages.data:
        if message.role == 'assistant':
            content = message.content[0].text.value
            print(content)


    print("Done")


if __name__ == "__main__":
    main()