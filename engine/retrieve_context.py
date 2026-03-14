import json
import numpy as np
import datetime
import swisseph as swe
from sentence_transformers import SentenceTransformer

# Location (Hyderabad example — change if needed)
LAT = 17.3850
LON = 78.4867

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

MANTRA_MAP = {
11: "Om Namo Bhagavate Vasudevaya",
14: "Om Namah Shivaya",
15: "Om Shanti Shanti Shanti",
30: "Om Pitru Devaya Namah"
}

FESTIVAL_RULES = {
11: "Ekadashi fasting day observed by many devotees",
14: "Chaturdashi – traditionally associated with Shiva worship",
15: "Purnima – Full Moon spiritual observances",
30: "Amavasya – day for ancestor remembrance"
}

# -----------------------------
# Sunrise / Sunset
# -----------------------------

def get_sun_times():

    now = datetime.datetime.now(datetime.UTC)

    jd = swe.julday(now.year, now.month, now.day)

    rise = swe.rise_trans(
        jd,
        swe.SUN,
        lon=LON,
        lat=LAT,
        rsmi=swe.CALC_RISE
    )[1][0]

    set_ = swe.rise_trans(
        jd,
        swe.SUN,
        lon=LON,
        lat=LAT,
        rsmi=swe.CALC_SET
    )[1][0]

    sunrise = swe.revjul(rise)[3]
    sunset = swe.revjul(set_)[3]

    return {
        "sunrise": f"{int(sunrise):02d}:{int((sunrise%1)*60):02d}",
        "sunset": f"{int(sunset):02d}:{int((sunset%1)*60):02d}"
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

    mantra = MANTRA_MAP.get(tithi_num + 1, "Om Shanti")

    sun_times = get_sun_times()

    return {

        "tithi_name": TITHI_NAMES[tithi_num],
        "nakshatra_name": NAKSHATRA_NAMES[nak_num],
        "paksha": paksha,
        "festival": festival,
        "mantra": mantra,
        "sunrise": sun_times["sunrise"],
        "sunset": sun_times["sunset"]
    }

# -----------------------------
# Context retrieval
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
