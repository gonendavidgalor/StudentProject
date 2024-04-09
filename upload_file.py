import os
import openai # type: ignore

from dotenv import load_dotenv # type: ignore

load_dotenv()

api_key = os.getenv("API_KEY")

if api_key is None:
    raise ValueError("API_KEY not found in environment variables")

client = openai.OpenAI(api_key=api_key)

file = client.files.create(
  file=open("ps1.md", "rb"),
  purpose='assistants'
)

thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "I want to generate a question about this file. Can you help me with that",
      "file_ids": [file.id]
    }
  ]
)

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="can you help me generate questions about this file?",
  file_ids=[file.id]
)


# Create an assistant using the file ID
assistant = client.beta.assistants.create(
  instructions=("You should generate a question about the file."),
  model="gpt-4-turbo-preview",
  tools=[{"type": "retrieval"}],
  file_ids=[file.id]
)


run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions=("Generate one question about the content of the file and supply 4 answers to that question."
    # "the question should start with __Question and end with Question__" 
    # "and the answers should start with __Answer 1__, __Answer 2__, __Answer 3__, __Answer 4__ and end with __Answer__"
    # "The correct answer should be added after and start with __Correct Answer__ and end with __Correct Answer__"),
  ),
)

if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )


questions = []

# Iterate through the messages
for message in messages.data:
    if message.role == 'assistant':
        content = message.content[0].text.value
        print(content)


print("Done")
# print(message)

# print(assistant['choices'][0]['message']['content'])

