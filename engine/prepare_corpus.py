import json
import pathlib
import re

texts=[]

path=pathlib.Path("scriptures")

for file in path.glob("*.txt"):

    with open(file,"r",encoding="utf-8") as f:

        content=f.read()

        content=content.replace("\n"," ")

        sentences=re.split(r'[.!?]',content)

        for s in sentences:

            t=s.strip()

            if len(t)>40:
                texts.append(t)

print("Corpus size:",len(texts))

if len(texts)==0:
    raise Exception("Corpus empty")

json.dump(texts,open("corpus.json","w"))
