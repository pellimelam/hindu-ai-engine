import requests
import json
import datetime

data = json.load(open("context.json"))

context = "\n".join(data["context"])

today = datetime.datetime.now(datetime.UTC).strftime("%A, %d %B %Y")

p = data["panchang"]

prompt = f"""
Create a TELEGRAM FRIENDLY message.

Use clear sections and simple language.

Format exactly like this:

🔆 DIGITAL DAILY HINDU GUIDE
━━━━━━━━━━━━━━━━━━

📅 Date
{today}

🌅 Sunrise / Sunset
Sunrise: {p['sunrise']}
Sunset: {p['sunset']}

🌙 Panchang
Tithi: {p['tithi_name']}
Nakshatra: {p['nakshatra_name']}
Paksha: {p['paksha']}

Meaning
Explain this lunar day in simple language.

━━━━━━━━━━━━━━━━━━

🎉 Festival / Observance
{p['festival']}

━━━━━━━━━━━━━━━━━━

📿 Mantra for Today
{p['mantra']}

Explain its meaning.

━━━━━━━━━━━━━━━━━━

📜 Wisdom from Hindu Scriptures
Short teaching and explanation.

━━━━━━━━━━━━━━━━━━

🏛 Temple Traditions
What rituals people may see today.

━━━━━━━━━━━━━━━━━━

🪔 Simple Dharma Practice
Give 3 practical actions people can follow today.

━━━━━━━━━━━━━━━━━━

🧘 Quiet Reflection
Short meditation idea.

━━━━━━━━━━━━━━━━━━

🌱 Respect Nature
One simple action for environmental harmony.

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
