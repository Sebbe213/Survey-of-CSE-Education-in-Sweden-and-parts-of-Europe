import os
import openai
from dotenv import load_dotenv
from pathlib import Path

# Load .env.local file from current directory
def ai_model(prompt, tokens ):
    load_dotenv(Path(".env.local"))
    openai.api_key = os.getenv('API_KEY')


    response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "system" ,"content": "....."},{"role": "user","content": prompt}], max_tokens = tokens)
    print(response.choices[0].message.content)
    return response.choices[0].message.content

