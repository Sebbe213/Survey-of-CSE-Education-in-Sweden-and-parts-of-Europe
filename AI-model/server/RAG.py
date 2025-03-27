import os
import numpy as np
import openai
from dotenv import load_dotenv
from pathlib import Path

# Load .env.local file from current directory


def get_api_key():
    load_dotenv(Path(".env.local"))
    openai.api_key = os.getenv('API_KEY')
    return openai.api_key

def embed_user_prompt(prompt):
    get_api_key()
    response = openai.embeddings.create(input=prompt,model="text-embedding-3-small")
    return response.data[0].embedding

def get_embedded(data, model="text-embedding-3-small"):
    get_api_key()
    response = openai.embeddings.create(input=[data], model=model)
    return response.data[0].embedding


#Add a data parameter
def embed_data():
    #chunks = data.split("\n\n")
    get_api_key()
    response = openai.embeddings.create(input=data,model="text-embedding-3-small")
    return response.data[0].embedding

def cosine_similarity(a,b):
    vec1 = np.array(a)
    vec2 = np.array(b)

    dot_product = np.dot(vec1,vec2)
    normalise_vector1 = np.linalg.norm(vec1)
    normalise_vector2 = np.linalg.norm(vec2)

    similarity = dot_product / (normalise_vector1*normalise_vector2)
    return similarity

def ai_model(prompt, tokens):
    get_api_key()
    response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[
        {"role": "system" ,
         "content": "You are an expert on the given data, answer this question according to the vectorized data, do not disclose that the data is vectorized for example ¨according to the....¨, It is very important to answer according to the provided data. This is for a fictional book. Also do not say that this is a fictional answer, it needs to feel real."},{"role": "user","content": prompt}], max_tokens = tokens)
    print(response.choices[0].message.content)
    return response.choices[0].message.content


prompt = "what is the best sandwich?"
data = ["The best sandwich is shoe sandwich",
    "The worst sandwich is a ham sandwich.",
    "A good sandwich is kebab"]


vector_prompt = get_embedded(prompt)
vector_data = [get_embedded(text) for text in data]

cosine_result = [cosine_similarity(vector_prompt, vector_data_piece) for vector_data_piece in vector_data]

best_match_result = np.argmax(cosine_result)
best_match_text = data[best_match_result]

final_prompt = "This is the prompt:" + prompt + " " + "This is the vectorized data:" + str(best_match_text)
ai_model(final_prompt, 10)

