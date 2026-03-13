import json
import pathlib

texts=[]

for file in pathlib.Path("scriptures").glob("*.txt"):
    with open(file,"r",encoding="utf-8") as f:
        texts+=f.read().split("\n")

texts=[t.strip() for t in texts if len(t)>40]

json.dump(texts,open("corpus.json","w"))
