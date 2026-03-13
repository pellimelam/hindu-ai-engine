import json
import pathlib

texts = []

for file in pathlib.Path("scriptures").glob("*.txt"):
    with open(file, "r", encoding="utf-8") as f:

        content = f.read()

        chunks = content.split("\n\n")

        for chunk in chunks:

            t = chunk.strip()

            if len(t) > 50:
                texts.append(t)

print("Corpus size:", len(texts))

if len(texts) == 0:
    raise Exception("Corpus empty. Check scripture files.")

json.dump(texts, open("corpus.json", "w"))
