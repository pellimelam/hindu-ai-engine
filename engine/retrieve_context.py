import json
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import numpy as np

PANCHANG_URL = "https://www.drikpanchang.com/panchang/day-panchang.html"

def fetch_panchang():
    r = requests.get(PANCHANG_URL, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(separator="\n")

    def find(label):
        for line in text.splitlines():
            if label.lower() in line.lower():
                return line.split(label)[-1].strip()
        return None

    data = {
        "sunrise": find("Sunrise"),
        "sunset": find("Sunset"),
        "tithi": find("Tithi"),
        "nakshatra": find("Nakshatra"),
        "festival": find("Festival")
    }

    # Hard validation so bad data never propagates
    for k,v in data.items():
        if not v:
            raise RuntimeError(f"Panchang value missing: {k}")

    return data


# Load scripture embeddings
texts = json.load(open("corpus.json"))
embeddings = np.load("embeddings.npy")

model = SentenceTransformer("all-MiniLM-L6-v2")

panchang = fetch_panchang()

query = f"""
Hindu calendar context
Tithi {panchang['tithi']}
Nakshatra {panchang['nakshatra']}
"""

q = model.encode([query])[0]

scores = np.dot(embeddings, q)

idx = scores.argsort()[-10:]
context = [texts[i] for i in idx]

json.dump(
{
    "panchang": panchang,
    "context": context
},
open("context.json","w"),
indent=2
)
