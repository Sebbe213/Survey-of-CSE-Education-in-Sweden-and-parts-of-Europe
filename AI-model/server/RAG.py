import os
import numpy as np
import openai
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import pickle

# ----------------------------------------------------------
# Configuration and Caching/ for faster operation
# ----------------------------------------------------------
CACHE_FILE = "embeddings_cache.pkl"

def load_embeddings_cache():
    """Load cached embeddings if available."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as f:
            return pickle.load(f)
    return None

def save_embeddings_cache(embeddings):
    """Save embeddings to a cache file."""
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(embeddings, f)

def get_or_compute_embeddings(data_list):
    """Return cached embeddings or compute them in batch if not cached."""
    cached = load_embeddings_cache()
    if cached is not None:
        print("Loaded embeddings from cache.")
        return cached
    else:
        embeddings = get_embedded_batch(data_list)
        save_embeddings_cache(embeddings)
        return embeddings


openai.api_key="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"


def get_api_key():
    """Loads your OpenAI API key from .env."""
    # Assumes .env is in the same folder or a parent folder
    #load_dotenv()

    #openai.api_key = os.getenv('API_KEY')
    return openai.api_key

def get_embedded_batch(data_list, model="text-embedding-ada-002", max_length=2000):
    # Filter out empty strings and truncate each valid string to max_length characters
    valid_data = [text.strip()[:max_length] for text in data_list if text.strip()]
    
    # Debug print to see what you’re sending to the API
    print("Sample inputs for embeddings:", valid_data[:3])
    
    get_api_key()
    response = openai.Embedding.create(input=valid_data, model=model)
    embeddings = [item["embedding"] for item in response["data"]]
    return embeddings





def cosine_similarity(a, b):
    """
    Computes cosine similarity between two vectors.
    """
    vec1 = np.array(a)
    vec2 = np.array(b)
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

def ai_model(prompt, tokens=50):
    """
    Sends a prompt to the OpenAI chat model (gpt-3.5-turbo) and returns its response.
    """
    get_api_key()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are an expert on the given data. Answer the question based solely on the provided data without revealing internal processes."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=tokens
    )
    return response.choices[0].message.content

def load_csv_data(file_path):
    """
    Loads a CSV file into a list of strings.
    Each row is converted to a string with fields separated by " | ".
    """
    try:
        df = pd.read_csv(file_path, on_bad_lines='skip')
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []
    text_data = df.astype(str).apply(lambda row: ' | '.join(row), axis=1).tolist()
    return text_data

def load_all_csv_data(csv_file_paths):
    """
    Loads data from multiple CSV files.
    Each row is prefixed with the CSV file name (without extension) for context.
    """
    all_data = []
    for file_path in csv_file_paths:
        data = load_csv_data(file_path)
        labeled_data = [f"[{file_path.stem}] {row}" for row in data]
        all_data.extend(labeled_data)
    return all_data

def answer_query(user_query, combined_data, combined_embeddings):
    """
    Retrieves the most relevant data row for a user query and generates an AI response.
    """
    query_embedding = get_embedded_batch([user_query])[0]
    similarities = [cosine_similarity(query_embedding, emb) for emb in combined_embeddings]
    
    best_match_index = np.argmax(similarities)
    best_match_row = combined_data[best_match_index]
    
    final_prompt = (
        f"User question: {user_query}\n"
        f"Relevant data: {best_match_row}"
    )
    answer = ai_model(final_prompt, tokens=50)
    return answer

def main():
    # Adjust the path: go one level up from server, then into data
    csv_file_path = Path(__file__).parent.parent / "data" / "test_alla_input_data.csv"
    csv_file_paths = [csv_file_path]
    
    combined_data = load_all_csv_data(csv_file_paths)
    print("CSV data loaded successfully.")
    
    combined_embeddings = get_or_compute_embeddings(combined_data)
    
    while True:
        init_input = input("Type 'Hi Ai' to start: ").strip()
        if init_input.lower() == "hi ai":
            print("Hello! How can I assist you today?")
            break
        else:
            print("Please type 'Hi Ai' to begin.")
    
    while True:
        user_query = input("Enter your query (or type 'done' to quit): ").strip()
        if user_query.lower() == "done":
            print("Exiting the program.")
            break
        
        answer = answer_query(user_query, combined_data, combined_embeddings)
        print("\nAI Model's Response:")
        print(answer)
        print("-" * 50)

if __name__ == "__main__":
    main()
