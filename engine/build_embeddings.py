from sentence_transformers import SentenceTransformer
import json
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = json.load(open("corpus.json"))

emb = model.encode(texts)

print("Embeddings shape:", len(emb))

np.save("embeddings.npy", emb)
