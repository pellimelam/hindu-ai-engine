import requests

draft = open("draft.txt").read()

prompt = f"""
Improve the following Hindu daily report.

Make it clearer and more insightful.

{draft}
"""

response = requests.post(
"http://localhost:11434/api/generate",
json={
"model": "phi3",
"prompt": prompt,
"stream": False
}
)

open("final.txt","w").write(response.json()["response"])
