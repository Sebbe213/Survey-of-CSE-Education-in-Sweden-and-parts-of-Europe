from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai
from internet_search import search
import urllib.parse

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

# Utility to decide if local data is missing
def no_local_data(chunks):
    return all((not chunk or 'n/a' in chunk.lower() or 'not specified' in chunk.lower()) for chunk in chunks)

# ---- UI route ----
@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    if request.method == 'POST':
        user_input = request.form.get('question', '').strip()
        if user_input:
            # Embed, retrieve, build prompt, and call the model
            query_emb     = embed_text(user_input)
            search_result = search(user_input)
            best_texts    = find_most_similar_entry(query_emb, data_embeddings, original_texts)

            # Fallback to online-only if no local data
            if no_local_data(best_texts):
                prompt = (
                    f"The user asked: '{user_input}'.\n"
                    f"I have no relevant local data. Here are internet search results:\n"
                    f"{search_result}\n\n"
                    f"Please answer the question based solely on these results."
                )
            else:
                prompt = build_prompt(user_input, search_result, best_texts)

            raw_answer = generate_answer(prompt, tokens=1000)

            # Replace placeholder [URL] with clickable DuckDuckGo search link
            #if '[URL]' in raw_answer:
                #query_enc = urllib.parse.quote_plus(user_input)
                #link = f"https://duckduckgo.com/?q={query_enc}"
                # wrap the URL as hyperlink visible
                #answer = raw_answer.replace(
                    #'[URL]', f"<a href=\"{link}\" target=\"_blank\">{link}</a>"
                #)
            #else:
                #answer = raw_answer

    return render_template('index.html', answer=answer)

# ---- JSON API endpoint ----
@app.route('/api/ask', methods=['POST'])
def api_ask():
    data = request.get_json() or {}
    question = data.get('question', '').strip()
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Embed, retrieve, build prompt, and query the model
    query_emb     = embed_text(question)
    search_result = search(question)
    best_texts    = find_most_similar_entry(query_emb, data_embeddings, original_texts)

    # Fallback to online-only if no local data
    if no_local_data(best_texts):
        prompt = (
            f"The user asked: '{question}'.\n"
            f"I have no relevant local data. Here are internet search results:\n"
            f"{search_result}\n\n"
            f"Please answer the question based solely on these results."
        )
    else:
        prompt = build_prompt(question, search_result, best_texts)

    raw_answer = generate_answer(prompt, tokens=1000)
    # For JSON, include the link directly if needed
    #if '[URL]' in raw_answer:
       # query_enc = urllib.parse.quote_plus(question)
        #link = f"https://duckduckgo.com/?q={query_enc}"
        #answer_text = raw_answer.replace('[URL]', link)
   # else:
        #answer_text = raw_answer

    return jsonify({'answer': raw_answer})

if __name__ == '__main__':
    # For development; in production use a proper WSGI server
    app.run(host='0.0.0.0', port=5000, debug=True)
