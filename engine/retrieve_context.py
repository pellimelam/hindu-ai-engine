import json
import numpy as np
import datetime
import swisseph as swe
from sentence_transformers import SentenceTransformer

# -----------------------------
# Panchang names
# -----------------------------

TITHI_NAMES = [
"Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami","Shashthi",
"Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi",
"Trayodashi","Chaturdashi","Purnima",
"Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami","Shashthi",
"Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi",
"Trayodashi","Chaturdashi","Amavasya"
]

NAKSHATRA_NAMES = [
"Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra",
"Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni",
"Uttara Phalguni","Hasta","Chitra","Swati","Vishakha",
"Anuradha","Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha",
"Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada",
"Uttara Bhadrapada","Revati"
]

# -----------------------------
# Festival rules
# -----------------------------

FESTIVAL_RULES = {

11: "Ekadashi fasting day observed by many devotees",

14: "Chaturdashi – often associated with Shiva worship",

15: "Purnima – Full Moon spiritual observances",

30: "Amavasya – day for ancestor remembrance and reflection"
}

# -----------------------------
# Panchang calculation
# -----------------------------

def calculate_panchang():

    now = datetime.datetime.now(datetime.UTC)

    jd = swe.julday(now.year, now.month, now.day, now.hour)

    moon = swe.calc_ut(jd, swe.MOON)[0][0]
    sun = swe.calc_ut(jd, swe.SUN)[0][0]

    diff = (moon - sun) % 360

    tithi_num = int(diff / 12)

    nak_num = int(moon / (360 / 27))

    paksha = "Shukla Paksha" if diff < 180 else "Krishna Paksha"

    festival = FESTIVAL_RULES.get(tithi_num + 1, "No major festival today")

    return {

        "tithi_number": tithi_num + 1,
        "tithi_name": TITHI_NAMES[tithi_num],
        "nakshatra_name": NAKSHATRA_NAMES[nak_num],
        "paksha": paksha,
        "festival": festival
    }

# -----------------------------
# Load corpus embeddings
# -----------------------------

texts = json.load(open("corpus.json"))
embeddings = np.load("embeddings.npy")

model = SentenceTransformer("all-MiniLM-L6-v2")

panchang = calculate_panchang()

query = f"""
Hindu calendar context
Tithi {panchang['tithi_name']}
Nakshatra {panchang['nakshatra_name']}
"""

q = model.encode([query])[0]

scores = np.dot(embeddings, q)

idx = scores.argsort()[-10:]

context = [texts[i] for i in idx]

json.dump(
{"panchang": panchang, "context": context},
open("context.json","w"),
indent=2
)
