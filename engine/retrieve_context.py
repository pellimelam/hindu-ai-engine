import json
import numpy as np
import datetime
import swisseph as swe
from sentence_transformers import SentenceTransformer

def calculate_panchang():

    now = datetime.datetime.now(datetime.UTC)

    jd = swe.julday(now.year, now.month, now.day, now.hour)

    moon = swe.calc_ut(jd, swe.MOON)[0][0]
    sun = swe.calc_ut(jd, swe.SUN)[0][0]

    diff = (moon - sun) % 360

    tithi = int(diff / 12) + 1
    nakshatra = int(moon / (360 / 27)) + 1

    paksha = "Shukla" if diff < 180 else "Krishna"

    return {
        "tithi": tithi,
        "nakshatra": nakshatra,
        "paksha": paksha
    }

texts = json.load(open("corpus.json"))
embeddings = np.load("embeddings.npy")

model = SentenceTransformer("all-MiniLM-L6-v2")

panchang = calculate_panchang()

query = f"""
Hindu calendar context

Tithi {panchang['tithi']}
Nakshatra {panchang['nakshatra']}
Paksha {panchang['paksha']}
"""

q = model.encode([query])[0]

scores = np.dot(embeddings, q)

idx = scores.argsort()[-10:]

context = [texts[i] for i in idx]

json.dump(
    {"panchang": panchang, "context": context},
    open("context.json", "w"),
    indent=2
)
