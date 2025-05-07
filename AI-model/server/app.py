from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai

# Load environment variables and set API key
load_dotenv('.env.local')
openai.api_key = os.getenv('OPENAI_API_KEY') or os.getenv('API_KEY')

# Import your RAG components
from prepare_embeddings import get_all_data
from openai_embed import embed_text
from similarity import cosine_similarity
from openai_chat import generate_answer
from main import build_prompt, find_most_similar_entry, load_data

# Load embeddings and source texts once at startup
data_embeddings = load_data()            # list of vector embeddings
original_texts   = get_all_data()        # list of corresponding source strings

app = Flask(__name__)
CORS(app)  # enable CORS for all routes (Dev only; adjust in production)

# ---- UI route ----
@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    if request.method == 'POST':
        user_input = request.form.get('question', '').strip()
        if user_input:
            # Embed, retrieve, build prompt, and call the model
            query_emb = embed_text(user_input)
            best_texts = find_most_similar_entry(query_emb, data_embeddings, original_texts)
            prompt     = build_prompt(user_input, best_texts)
            answer     = generate_answer(prompt, tokens=400)
    return render_template('index.html', answer=answer)

# ---- JSON API endpoint ----
@app.route('/api/ask', methods=['POST'])
def api_ask():
    data = request.get_json() or {}
    question = data.get('question', '').strip()
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Embed, retrieve, build prompt, and query the model
    query_emb   = embed_text(question)
    best_texts  = find_most_similar_entry(query_emb, data_embeddings, original_texts)
    prompt      = build_prompt(question, best_texts)
    answer_text = generate_answer(prompt, tokens=400)

    return jsonify({ 'answer': answer_text })

if __name__ == '__main__':
    # For development; in production use a proper WSGI server
    app.run(host='0.0.0.0', port=5000, debug=True)
