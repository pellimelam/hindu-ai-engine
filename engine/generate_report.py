import subprocess
import json
import datetime

MODEL="models/model.gguf"

data=json.load(open("context.json"))

context="\n".join(data["context"])

today=datetime.datetime.utcnow().strftime("%A %d %B %Y")

prompt=f"""
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

result=subprocess.run(
[
"./llama.cpp/build/bin/llama-cli",
"-m",MODEL,
"-p",prompt,
"-n","500"
],
capture_output=True,
text=True
)

open("draft.txt","w").write(result.stdout)
