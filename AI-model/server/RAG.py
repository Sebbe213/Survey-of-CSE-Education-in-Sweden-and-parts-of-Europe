import os
import openai
from dotenv import load_dotenv
from pathlib import Path

# Load .env.local file from current directory
def ai_model(prompt, tokens ):
    load_dotenv(Path(".env.local"))
    # Set the API key
    openai.api_key = os.getenv('API_KEY')


    # Make a request using a chat model
    response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "system" ,"content": "....."},{"role": "user","content": prompt}], max_tokens = tokens)

    print(response.choices[0].message.content)
