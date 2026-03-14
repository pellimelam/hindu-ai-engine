import json
import numpy as np
import datetime
import swisseph as swe
from sentence_transformers import SentenceTransformer

LAT=17.3850
LON=78.4867

TITHI_NAMES=[
"Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami","Shashthi",
"Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi",
"Trayodashi","Chaturdashi","Purnima",
"Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami","Shashthi",
"Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi",
"Trayodashi","Chaturdashi","Amavasya"
]

NAKSHATRA_NAMES=[
"Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra",
"Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni",
"Uttara Phalguni","Hasta","Chitra","Swati","Vishakha",
"Anuradha","Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha",
"Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada",
"Uttara Bhadrapada","Revati"
]

MONTH_NAMES=[
"Chaitra","Vaishakha","Jyeshtha","Ashadha",
"Shravana","Bhadrapada","Ashwin","Kartika",
"Margashirsha","Pausha","Magha","Phalguna"
]

MANTRA_MAP={
11:"Om Namo Bhagavate Vasudevaya",
14:"Om Namah Shivaya",
15:"Om Shanti Shanti Shanti",
30:"Om Pitru Devaya Namah"
}

FESTIVAL_RULES={
11:"Ekadashi fasting observed by many devotees",
14:"Shiva worship day",
15:"Purnima full moon observances",
30:"Amavasya ancestor remembrance rituals"
}

REGIONAL_FESTIVALS={
("Chaitra","Shukla","Pratipada"):
"Ugadi / Gudi Padwa Hindu New Year",

("Shravana","Shukla","Panchami"):
"Naga Panchami serpent worship",

("Bhadrapada","Shukla","Chaturthi"):
"Ganesh Chaturthi festival",

("Kartika","Shukla","Ekadashi"):
"Dev Uthani Ekadashi",

("Ashwin","Krishna","Amavasya"):
"Diwali preparations in many regions"
}

def approximate_lunar_month(date):

    m=date.month

    return MONTH_NAMES[(m-3)%12]


def get_sun_times():

    now = datetime.datetime.now(datetime.UTC)

    jd = swe.julday(now.year, now.month, now.day)

    geopos = (LON, LAT, 0)

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

    return {
        "sunrise": f"{int(sunrise):02d}:{int((sunrise%1)*60):02d}",
        "sunset": f"{int(sunset):02d}:{int((sunset%1)*60):02d}"
    }


def calculate_panchang():

    now=datetime.datetime.now(datetime.UTC)

    jd=swe.julday(now.year,now.month,now.day,now.hour)

    moon=swe.calc_ut(jd,swe.MOON)[0][0]
    sun=swe.calc_ut(jd,swe.SUN)[0][0]

    diff=(moon-sun)%360

    tithi_num=int(diff/12)

    nak_num=int(moon/(360/27))

    paksha="Shukla Paksha" if diff<180 else "Krishna Paksha"

    festival=FESTIVAL_RULES.get(tithi_num+1,"No major festival today")

    mantra=MANTRA_MAP.get(tithi_num+1,"Om Shanti")

    sun_times=get_sun_times()

    month=approximate_lunar_month(now)

    regional=REGIONAL_FESTIVALS.get(
        (month,paksha.split()[0],TITHI_NAMES[tithi_num]),
        "No major regional festival today"
    )

    return{
        "tithi_name":TITHI_NAMES[tithi_num],
        "nakshatra_name":NAKSHATRA_NAMES[nak_num],
        "paksha":paksha,
        "month":month,
        "festival":festival,
        "regional_festival":regional,
        "mantra":mantra,
        "sunrise":sun_times["sunrise"],
        "sunset":sun_times["sunset"]
    }

texts=json.load(open("corpus.json"))
embeddings=np.load("embeddings.npy")

model=SentenceTransformer("all-MiniLM-L6-v2")

panchang=calculate_panchang()

query=f"""
Hindu calendar context
Tithi {panchang['tithi_name']}
Nakshatra {panchang['nakshatra_name']}
"""

q=model.encode([query])[0]

scores=np.dot(embeddings,q)

idx=scores.argsort()[-10:]

context=[texts[i] for i in idx]

json.dump(
{"panchang":panchang,"context":context},
open("context.json","w"),
indent=2
)
