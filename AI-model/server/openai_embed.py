import openai



def embed_text(text, model="text-embedding-3-small"):
    response = openai.embeddings.create(input=[text],model=model)
    return response.data[0].embedding


def embed_texts(texts, model="text-embedding-3-small"):
    response = openai.embeddings.create(input=texts, model=model)
    return [item.embedding for item in response.data]



