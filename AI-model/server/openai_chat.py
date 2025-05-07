import openai
from context import context

def generate_answer(prompt, tokens=50):
    system_prompt = context()

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=tokens
    )
    return response.choices[0].message.content