import requests
import json
import datetime

data = json.load(open("context.json"))

context = "\n".join(data["context"])

today = datetime.datetime.now(datetime.UTC).strftime("%A %d %B %Y")

prompt = f"""
Create a Hindu Daily Knowledge Report.

DATE
{today}

PANCHANG
{data['panchang']}

SCRIPTURE CONTEXT
{context}

Generate sections:

🕉 DAILY HINDU KNOWLEDGE REPORT
Date
Meaning of today's tithi
Festivals
Scriptural insight
Temple traditions
Daily dharma guidance
"""

response = requests.post(
"http://localhost:11434/api/generate",
json={
"model": "phi3",
"prompt": prompt,
"stream": False
}
)

result = response.json()["response"]

open("draft.txt","w").write(result)
