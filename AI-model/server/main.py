import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import os
import json
import numpy as np
from dotenv import load_dotenv
from prepare_embeddings import get_all_data
from openai_embed import embed_text
from openai_chat import generate_answer
from similarity import cosine_similarity

load_dotenv(".env.local")
import openai
openai.api_key = os.getenv("API_KEY")

def load_data():
    with open('embedded_data.json', "r") as file:
        result_list = json.load(file)
        return result_list


def find_most_similar_entry(query_embedding, all_embeddings, original_data):
    similarities = [
        cosine_similarity(query_embedding, item) for item in all_embeddings
    ]
    top_n = 3
    sorted_indices = np.argsort(similarities)[::-1][:top_n]
    top_matches = [original_data[i] for i in sorted_indices]
    return top_matches

def build_prompt(user_question,search_results, best_match):
    match_text = "\n".join([f"- {text}" for text in best_match])
    final_prompt = (
        f"The user asked: '{user_question}'\n"
        f"The most relevant data found:\n{match_text}\n"
        f"The data sourced from the internet:\n{search_results}\n"
        f"Based on this data, provide a detailed answer."
    )
    return final_prompt

def main():
    user_input = ""
    while user_input != "quit":
        user_input = input("What is your question dear user? Write quit to exit the program \n").strip()

        if not user_input or user_input == "quit":
            print("No input provided")
            break

        query_embedding = embed_text(user_input)

        print("hmm... good question, let me think!")
        data = load_data()


        best_match = find_most_similar_entry(query_embedding, data, get_all_data())

        print("Querying the LM")
        final_prompt = build_prompt(user_input, best_match)
        response = generate_answer(final_prompt, tokens=400)
        print(response)


if __name__ == "__main__":
    main()

