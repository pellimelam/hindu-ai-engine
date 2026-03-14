import json
import requests
from sentence_transformers import SentenceTransformer
import numpy as np

LAT = 17.3850
LON = 78.4867
TZ = 5.5

def get_panchang():

    r = requests.get(
        "https://api.drikpanchang.com/v1/panchang",
        params={
            "lat": LAT,
            "lon": LON,
            "tz": TZ
        },
        timeout=30
    )

    data = r.json()

    return {
        "tithi": data["tithi"]["name"],
        "nakshatra": data["nakshatra"]["name"],
        "paksha": data["paksha"],
        "sunrise": data["sunrise"],
        "sunset": data["sunset"],
        "festival": data.get("festival","No major festival today")
    }

# Load corpus embeddings
texts = json.load(open("corpus.json"))
embeddings = np.load("embeddings.npy")

model = SentenceTransformer("all-MiniLM-L6-v2")

panchang = get_panchang()

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
"panchang":panchang,
"context":context
},
open("context.json","w"),
indent=2
)
