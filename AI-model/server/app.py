from flask import Flask, render_template, request
from prepare_embeddings import get_all_data
from openai_embed import embed_text
from similarity import cosine_similarity
from openai_chat import generate_answer
from main import build_prompt, find_most_similar_entry, load_data

# Load data and embeddings once at startup
data = load_data()            # list of embeddings
original_texts = get_all_data()  # list of source texts

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    if request.method == 'POST':
        user_input = request.form.get('question')
        if user_input:
            # 1. Embed the user question
            query_emb = embed_text(user_input)
            # 2. Find top matches
            best_texts = find_most_similar_entry(query_emb, data, original_texts)
            # 3. Build prompt and query the model
            prompt = build_prompt(user_input, best_texts)
            answer = generate_answer(prompt, tokens=150)
    return render_template('index.html', answer=answer)

if __name__ == '__main__':
    # For development; in production use a WSGI server
    app.run(host='0.0.0.0', port=5000, debug=True)


