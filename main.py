import os
import openai # type: ignore
# from dotenv import load_dotenv

# load_dotenv()
# api_key = os.getenv("API_KEY")
# print(api_key)

client = openai.OpenAI(api_key='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')  # Changed 'API-KEY' to 'api_key'

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)


print(completion.choices[0].message)
    