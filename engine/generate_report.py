import requests
import json
import datetime

data=json.load(open("context.json"))

context="\n".join(data["context"])

today=datetime.datetime.now(datetime.UTC).strftime("%A, %d %B %Y")

p=data["panchang"]

prompt=f"""
Create a TELEGRAM FRIENDLY message.

🔆 DIGITAL DAILY HINDU GUIDE
━━━━━━━━━━━━━━━━━━

📅 Date
{today}

🌅 Sunrise / Sunset
Sunrise: {p['sunrise']}
Sunset: {p['sunset']}

🌙 Panchang
Month: {p['month']}
Tithi: {p['tithi_name']}
Nakshatra: {p['nakshatra_name']}
Paksha: {p['paksha']}

Meaning
Explain in simple language.

━━━━━━━━━━━━━━━━━━

🎉 Festival
{p['festival']}

🏵 Regional Observance
{p['regional_festival']}

━━━━━━━━━━━━━━━━━━

📿 Mantra for Today
{p['mantra']}

Explain meaning simply.

━━━━━━━━━━━━━━━━━━

📜 Wisdom from Scriptures
Short teaching.

━━━━━━━━━━━━━━━━━━

🏛 Temple Traditions
Explain briefly.

━━━━━━━━━━━━━━━━━━

🪔 Simple Dharma Practice
Give 3 simple actions.

━━━━━━━━━━━━━━━━━━

🧘 Quiet Reflection
Short meditation idea.

━━━━━━━━━━━━━━━━━━

🌱 Respect Nature
One simple environmental action.

Context:
{context}
"""

response=requests.post(
"http://localhost:11434/api/generate",
json={
"model":"phi3",
"prompt":prompt,
"stream":False
}
)

open("draft.txt","w").write(response.json()["response"])
