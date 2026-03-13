# retrieve_context.py
import numpy as np, json, requests, datetime
from sentence_transformers import SentenceTransformer

texts=json.load(open("corpus.json"))
emb=np.load("embeddings.npy")

model=SentenceTransformer("all-MiniLM-L6-v2")

panchang=requests.get(
"https://api.drkalendar.com/panchang?lat=17.3850&lon=78.4867"
).json()

query=f"""
Hindu calendar context
Tithi {panchang.get("tithi")}
Nakshatra {panchang.get("nakshatra")}
Festival {panchang.get("festival")}
"""

q=model.encode([query])[0]

scores=emb@q

idx=scores.argsort()[-10:]

context=[texts[i] for i in idx]

json.dump(context,open("context.json","w"))
