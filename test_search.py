from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the current price of Bitcoin?",
    config=types.GenerateContentConfig(
        tools=[types.Tool(
            google_search=types.GoogleSearch()
        )]
    )
)

print(response.text)
