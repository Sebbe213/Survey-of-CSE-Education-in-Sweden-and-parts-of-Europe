from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import numpy as np
env_path = ".env.local"
from dotenv import load_dotenv
load_dotenv(env_path)
import openai

# Import your existing modules
from openai_embed import embed_text
from prepare_embeddings import get_all_data
from similarity import cosine_similarity
from context import context as get_system_prompt

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for development

# Set OpenAI API key
openai.api_key = os.getenv("API_KEY")

# Load precomputed embeddings and original data
with open("embedded_data.json", "r") as f:
    embedded_vectors = json.load(f)
original_data = get_all_data()

# Helper to find top N similar entries
def find_top_matches(query_embedding, vectors, data, top_n=2):
    sims = [cosine_similarity(query_embedding, vec) for vec in vectors]
    idxs = np.argsort(sims)[::-1][:top_n]
    return [data[i] for i in idxs]

# Build prompt for LLM
def build_prompt(question, matches):
    lines = [f"- {item}" for item in matches]
    match_text = "\n".join(lines)
    return (
        f"The user asked: '{question}'\n"
        f"The most relevant data found:\n{match_text}\n"
        f"Based on this data, provide a detailed answer."
    )

@app.route('/ask', methods=['POST'])
def ask():
    payload = request.get_json(force=True)
    question = payload.get('question', '').strip()
    if not question:
        return jsonify({'error': 'No question provided.'}), 400

    # Embed and retrieve
    q_vec = embed_text(question)
    top_matches = find_top_matches(q_vec, embedded_vectors, original_data)
    prompt = build_prompt(question, top_matches)

    # Query OpenAI
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        answer = response.choices[0].message.content
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'answer': answer,
        'matches': top_matches
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
