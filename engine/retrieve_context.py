import json
import numpy as np
import datetime
import swisseph as swe
from sentence_transformers import SentenceTransformer

LAT = 17.3850
LON = 78.4867
ALT = 0

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


def format_time(decimal_hour):

    h = int(decimal_hour)
    m = int((decimal_hour - h) * 60)

    return f"{h:02d}:{m:02d}"


def get_sun_times():

    now = datetime.datetime.now(datetime.UTC)

    jd = swe.julday(now.year, now.month, now.day)

    geopos = (LON, LAT, ALT)

    rise = swe.rise_trans(
        jd,
        swe.SUN,
        swe.CALC_RISE,
        geopos=geopos
    )[1][0]

    set_ = swe.rise_trans(
        jd,
        swe.SUN,
        swe.CALC_SET,
        geopos=geopos
    )[1][0]

    sunrise = swe.revjul(rise)[3]
    sunset = swe.revjul(set_)[3]

    return format_time(sunrise), format_time(sunset)


def calculate_panchang():

    now = datetime.datetime.utcnow()

    jd = swe.julday(now.year, now.month, now.day, now.hour)

    moon = swe.calc_ut(jd, swe.MOON)[0][0]
    sun = swe.calc_ut(jd, swe.SUN)[0][0]

    diff = (moon - sun) % 360

    tithi_index = int(diff / 12)

    nak_index = int(moon / (360 / 27))

    paksha = "Shukla Paksha" if diff < 180 else "Krishna Paksha"

    sunrise, sunset = get_sun_times()

    return {
        "tithi": TITHI_NAMES[tithi_index],
        "nakshatra": NAKSHATRA_NAMES[nak_index],
        "paksha": paksha,
        "sunrise": sunrise,
        "sunset": sunset
    }


# Load corpus
texts = json.load(open("corpus.json"))
embeddings = np.load("embeddings.npy")

model = SentenceTransformer("all-MiniLM-L6-v2")

panchang = calculate_panchang()

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
