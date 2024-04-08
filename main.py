import os
import openai # type: ignore

from dotenv import load_dotenv # type: ignore

# Load the environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("API_KEY")

# Ensure the API key is loaded
if api_key is None:
    raise ValueError("API_KEY not found in environment variables")

client = openai.OpenAI(api_key=api_key)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)


print(completion.choices[0].message)
    