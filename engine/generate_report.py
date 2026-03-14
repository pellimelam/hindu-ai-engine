import requests
import json
import datetime

data = json.load(open("context.json"))

context = "\n".join(data["context"])
p = data["panchang"]

today = datetime.datetime.utcnow().strftime("%A, %d %B %Y")

prompt = f"""
Create a clean Telegram message.

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
Paksha: {p['paksha']}

━━━━━━━━━━━━━━━━━━

🎉 Festival / Observance
{p['festival']}

━━━━━━━━━━━━━━━━━━

📿 Mantra for Today
Provide a simple mantra related to today's tithi.

━━━━━━━━━━━━━━━━━━

📜 Wisdom from Scriptures
Short teaching in simple language.

━━━━━━━━━━━━━━━━━━

🪔 Simple Dharma Practice
3 simple actions people can do today.

━━━━━━━━━━━━━━━━━━

🧘 Reflection
One short meditation idea.

Context:
{context}
"""

response = requests.post(
"http://localhost:11434/api/generate",
json={
"model":"phi3",
"prompt":prompt,
"stream":False
}
)

open("draft.txt","w").write(response.json()["response"])
