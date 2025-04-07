import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))


import os
import json
import numpy as np
from dotenv import load_dotenv

from openai_embed import embed_text
from openai_chat import generate_answer
from similarity import cosine_similarity

load_dotenv(".env.local")
import openai
openai.api_key = os.getenv("API_KEY")

def load_employment_rates_data(path="Employment_rates_with_embeddings.json"):
    with open(path, "r") as f:
        return json.load(f)


def find_most_similar_entry(query_embedding, data):
    similarities = [
        cosine_similarity(query_embedding, item["embedding"]) for item in data
    ]
    best_index = int(np.argmax(similarities))
    return data[best_index]

def build_prompt(user_question, best_match):
    return (
        f"User question: {user_question}\n"
        f"University data: {best_match["text"]}\n"
        f"Answer the question based on the university data above."
    )

def main():
    user_input = input("What is your question dear user? \n").strip()

    if not user_input:
        print("No input provided")
        return

    print("Embedding your question")
    query_embedding = embed_text(user_input)

    print("Crunching employment rates just for you ...")
    data = load_employment_rates_data()


    print("Finding the best matching rates for you ..")
    best_match = find_most_similar_entry(query_embedding, data)

    print(f"Best match: {best_match["meta"]["University"]} ({best_match["meta"]["Country"]})")

    print("Querying the LM")
    final_prompt = build_prompt(user_input, best_match)
    response = generate_answer(final_prompt, tokens=150)

    print(response)


if __name__ == "__main__":
    main()

