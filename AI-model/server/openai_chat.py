import openai
from context import context

def generate_answer(prompt, tokens=50):
    system_prompt = context()

    response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": context()},
        {"role": "user",   "content": prompt}
    ],
    max_tokens=tokens
)


    return response.choices[0].message.content