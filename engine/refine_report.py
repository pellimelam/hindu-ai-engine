import requests

draft = open("draft.txt").read()

prompt = f"""
Improve formatting and readability.

Make it clear, structured, and friendly for Telegram readers.

{draft}
"""

response = requests.post(
"http://localhost:11434/api/generate",
json={
"model":"phi3",
"prompt":prompt,
"stream":False
}
)

open("final.txt","w").write(response.json()["response"])
