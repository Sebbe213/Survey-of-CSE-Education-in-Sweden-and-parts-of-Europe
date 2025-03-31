import os
import numpy as np
import openai
from dotenv import load_dotenv
from pathlib import Path
from context import context

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
         "content": context()},{"role": "user","content": prompt}], max_tokens = tokens)
    print(response.choices[0].message.content)
    return response.choices[0].message.content


prompt = "How many international students does MIT have?"
data = ["""University, Total Students, % International Students
Chalmers University of Technology (Sweden), 10.999, 17
University of Gothenburg (Sweden), 57.959, 13
KTH Royal Institute of Technology (Sweden), 13.955, 26
Norwegian University of Science and Technology (Norway), 43.550, 9
Universitat Politècnica de València (Spain), 28.000 , 15
Gdańsk University of Technology (Poland), 15.622, 7
Warsaw University of Technology (Poland), 20.851, 8
Politecnico di Milano (Italy), 48.383, 18
RWTH Aachen University (Germany), 44.892, 34
Technische Universität Berlin (Germany), 33.933, 28
Technical University of Munich (Germany), 52.931, 45
ETH Zurich (Switzerland), 25.380, 35
EPFL (Switzerland), 13.445, 64
University of Copenhagen (Denmark), 36.528, 15
University of Helsinki (Finland), 31.465, 6
University of Cambridge (England), 24.000, 38
University of Oxford (England), 26.595, 46
University College London (England), 51.058, 54
Institut Polytechnique de Paris (France), 10.000, 41
Riga Technical University (Latvia), 14.000, 29
University of Tartu (Estonia), 15.206, 10"""]


vector_prompt = get_embedded(prompt)
vector_data = [get_embedded(text) for text in data]

cosine_result = [cosine_similarity(vector_prompt, vector_data_piece) for vector_data_piece in vector_data]

best_match_result = np.argmax(cosine_result)
best_match_text = data[best_match_result]

final_prompt = "This is the prompt:" + prompt + " " + "This is the vectorized data:" + str(best_match_text)
ai_model(final_prompt, 50)

