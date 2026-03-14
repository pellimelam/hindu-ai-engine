import requests

draft = open("draft.txt").read()

prompt = f"""
Improve readability for Telegram.

Use short sections, spacing, and clear bullet points.

Keep all factual data unchanged.

{draft}
"""

response = requests.post(
"http://localhost:11434/api/generate",
json={"model":"phi3","prompt":prompt,"stream":False}
)

open("final.txt","w").write(response.json()["response"])
