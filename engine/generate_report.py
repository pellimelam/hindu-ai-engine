import requests
import json
import datetime

data = json.load(open("context.json"))

p = data["panchang"]
context = "\n".join(data["context"])

today = datetime.datetime.now(datetime.UTC).strftime("%A, %d %B %Y")

prompt = f"""
You are generating a DAILY HINDU GUIDE for Telegram.

IMPORTANT RULES:
- Do NOT modify the Panchang values.
- Do NOT change times or names.
- Only explain them.

LOCKED DATA:
Sunrise: {p['sunrise']}
Sunset: {p['sunset']}
Tithi: {p['tithi']}
Nakshatra: {p['nakshatra']}
Festival: {p['festival']}

Create this format:

🔆 DIGITAL DAILY HINDU GUIDE
━━━━━━━━━━━━━━━━━━

📅 Date
{today}

🌅 Sunrise / Sunset
Sunrise: {p['sunrise']}
Sunset: {p['sunset']}

🌙 Panchang
Tithi: {p['tithi']}
Nakshatra: {p['nakshatra']}

🎉 Festival / Observance
{p['festival']}

📿 Mantra for Today
Provide one suitable mantra.

📜 Wisdom from Scriptures
Explain one teaching simply.

🪔 Simple Dharma Practice
Give 3 practical actions for daily life.

Context for scriptural insight:
{context}
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model":"phi3","prompt":prompt,"stream":False},
    timeout=60
)

text = response.json()["response"]

open("draft.txt","w").write(text)
