import requests
import json
import datetime

data = json.load(open("context.json"))

context = "\n".join(data["context"])

p = data["panchang"]

today = datetime.datetime.now(datetime.UTC).strftime("%A, %d %B %Y")

prompt = f"""
Create a TELEGRAM FRIENDLY message.

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

📿 Mantra for Today
Provide a simple mantra appropriate for today's tithi.

━━━━━━━━━━━━━━━━━━

📜 Wisdom from Hindu Scriptures
Give one short teaching explained simply.

━━━━━━━━━━━━━━━━━━

🪔 Simple Dharma Practice
Give 3 simple actions anyone can follow today.

━━━━━━━━━━━━━━━━━━

🧘 Quiet Reflection
Provide a short meditation idea.

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

result = response.json()["response"]

open("draft.txt","w").write(result)
