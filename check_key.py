from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

if key:
    print("API key found.")
    print("Starts with:", key[:8])
    print("Ends with:", key[-6:])
else:
    print("No API key found. Check your .env file.")