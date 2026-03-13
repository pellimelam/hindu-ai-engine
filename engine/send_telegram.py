import requests
import os

text=open("final.txt").read()

requests.post(
f"https://api.telegram.org/bot{os.environ['TELEGRAM_TOKEN']}/sendMessage",
json={
"chat_id":os.environ["TELEGRAM_CHAT_ID"],
"text":text
})
