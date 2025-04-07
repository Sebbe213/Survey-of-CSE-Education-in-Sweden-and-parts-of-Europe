import openai


def generate_answer(prompt, tokens=50):
    system_prompt = (
    "are an expert on the given data, answer this question "
    "according to the vectorized data, do not disclose that"
    " the data is vectorized for example ¨according to the....¨,"
    " It is very important to answer according to the provided"
    " data.This is for a fictional book.Also do not say that "
    "this is a fictional answer, it needs to feel real."
    )

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=tokens
    )
    return response.choices[0].message.content