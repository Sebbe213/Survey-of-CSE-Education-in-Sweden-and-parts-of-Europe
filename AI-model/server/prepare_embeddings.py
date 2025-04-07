import os
import json
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from openai_embed import embed_texts

load_dotenv(Path(".env.local"))
import openai
openai.api_key = os.getenv("API_KEY")


def build_text(row):
    time_frame = (
    f"{row['Time Frame (Months)']} months"
    if pd.notna(row['Time Frame (Months)']) else "an unspecified time frame"
    )
    return (
        f"{row['University']} in {row['Country']} offers {row['Degree Level (UG,PG,PhD)']} "
        f"programs in {row['Field Specificity']} with an employment rate of "
        f"{row['Employment Rate (%)']}% as reported in {row['Year of Reporting']}."
        f" The data covers {time_frame} and is based on {row['Scope of Employment Rate']} scope."
    )

def prepare():

    print("Loading university data from CSV...")
    df = pd.read_csv("Employment_rates.csv")

    print("Building text + metadata for each row...")
    records = []

    for _,row in df.iterrows():
        item = {
            "text": build_text(row),
            "meta": {
                "University": row["University"],
                "Country": row["Country"],
                "Degree Level": row["Degree Level (UG,PG,PhD)"],
                "Field": row["Field Specificity"],
                "Employment Rate": row["Employment Rate (%)"],
                "Year of Reporting": row["Year of Reporting"],
            },
            "embedding": None  # A temporary placeholder
        }
        records.append(item)

    print("Embedding university descriptions...")

    texts = [item["text"] for item in records]
    embeddings = embed_texts(texts)

    print("Attaching embeddings to records...")

    for item, emb in zip(records, embeddings):
        item["embedding"] = emb

    os.makedirs("data", exist_ok=True)
    output_path = "Employment_rates_with_embeddings.json"

    print(f"Saving to {output_path}")

    with open(output_path, "w") as f:
        json.dump(records, f, indent=2)

    print("Embedding complete! Ready to use in main.py")



if __name__ == "__main__":
    prepare()


