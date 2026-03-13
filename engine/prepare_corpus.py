# prepare_corpus.py
import json, pathlib

texts=[]

for file in pathlib.Path("scriptures").glob("*.txt"):
    texts+=open(file).read().split("\n")

texts=[t.strip() for t in texts if len(t)>40]

json.dump(texts,open("corpus.json","w"))
