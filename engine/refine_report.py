import subprocess

MODEL = "models/model.gguf"

draft = open("draft.txt").read()

prompt = f"""
Improve the following Hindu daily report.

Make it clearer and better structured.

{draft}
"""

result = subprocess.run(
[
"./llama.cpp/build/bin/llama-cli",
"-m", MODEL,
"-p", prompt,
"-n", "400"
],
capture_output=True,
text=True
)

open("final.txt","w").write(result.stdout)
