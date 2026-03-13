# build_embeddings.py
from sentence_transformers import SentenceTransformer
import json, numpy as np

model=SentenceTransformer("all-MiniLM-L6-v2")

texts=json.load(open("corpus.json"))

emb=model.encode(texts)

np.save("embeddings.npy",emb)
