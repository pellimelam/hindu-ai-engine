import json
import numpy as np
import datetime
import swisseph as swe
from sentence_transformers import SentenceTransformer

# -----------------------------
# Panchang Calculation
# -----------------------------

def calculate_panchang():

    now = datetime.datetime.utcnow()

    jd = swe.julday(now.year, now.month, now.day, now.hour)

    moon = swe.calc_ut(jd, swe.MOON)[0][0]
    sun = swe.calc_ut(jd, swe.SUN)[0][0]

    diff = (moon - sun) % 360

    # 30 tithis
    tithi = int(diff / 12) + 1

    # 27 nakshatras
    nakshatra = int(moon / (360/27)) + 1

    paksha = "Shukla" if diff < 180 else "Krishna"

    return {
        "tithi": tithi,
        "nakshatra": nakshatra,
        "paksha": paksha
    }

# -----------------------------
# Load Vector Index
# -----------------------------

texts = json.load(open("corpus.json"))
embeddings = np.load("embeddings.npy")

model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Get Panchang Context
# -----------------------------

panchang = calculate_panchang()

query = f"""
Hindu calendar context

Tithi: {panchang["tithi"]}
Nakshatra: {panchang["nakshatra"]}
Paksha: {panchang["paksha"]}

Find relevant Hindu scripture verses explaining this context.
"""

# -----------------------------
# Retrieve Relevant Verses
# -----------------------------

q = model.encode([query])[0]

scores = embeddings @ q

idx = scores.argsort()[-10:]

context = [texts[i] for i in idx]

# -----------------------------
# Save Context
# -----------------------------

output = {
    "panchang": panchang,
    "context": context
}

json.dump(output, open("context.json", "w"), indent=2)
