import os
import openai # type: ignore

from dotenv import load_dotenv # type: ignore

load_dotenv()

api_key = os.getenv("API_KEY")

if api_key is None:
    raise ValueError("API_KEY not found in environment variables")

client = openai.OpenAI(api_key=api_key)

user_question = input("Enter your question: ")

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "you are a helpful assist"},
    {"role": "user", "content": user_question}
  ]
) 

print(response.choices[0].message.content)
    