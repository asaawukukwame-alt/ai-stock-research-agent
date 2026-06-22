import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-4o")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing. Check your .env file.")

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model=model,
    input="In one sentence, explain what a stock research AI agent does."
)

print(response.output_text)