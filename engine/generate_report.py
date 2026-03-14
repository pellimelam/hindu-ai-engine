import requests
import json
import datetime

data = json.load(open("context.json"))

context = "\n".join(data["context"])

today = datetime.datetime.now(datetime.UTC).strftime("%A, %d %B %Y")

p = data["panchang"]

prompt = f"""
Create a TELEGRAM FRIENDLY message.

Rules:
- very easy language
- short paragraphs
- use symbols
- useful for common people
- no long essays

Format exactly like this:

🔆 DIGITAL DAILY HINDU GUIDE
━━━━━━━━━━━━━━━━━━

📅 Date
{today}

🌙 Panchang
Tithi: {p['tithi_name']}
Nakshatra: {p['nakshatra_name']}
Paksha: {p['paksha']}

Meaning:
Explain what this lunar day represents in simple language.

━━━━━━━━━━━━━━━━━━

🎉 Festival / Observance
{p['festival']}

Explain briefly.

━━━━━━━━━━━━━━━━━━

📜 Wisdom from Hindu Scriptures
Give one short teaching and explain it simply.

━━━━━━━━━━━━━━━━━━

🏛 Temple Traditions
What rituals people may see in temples today.

━━━━━━━━━━━━━━━━━━

🪔 Simple Dharma Practice Today
Give 3 simple actions people can do today.

━━━━━━━━━━━━━━━━━━

🧘 Quiet Reflection
Short meditation idea for peace of mind.

━━━━━━━━━━━━━━━━━━

🌱 Living with Nature
One simple action that respects nature.

━━━━━━━━━━━━━━━━━━

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
