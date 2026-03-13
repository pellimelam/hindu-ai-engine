# generate_report.py
import subprocess, json, datetime

context="\n".join(json.load(open("context.json")))

prompt=f"""
Generate a detailed Hindu daily knowledge report.

Context:
{context}

Sections:

Date
Panchang significance
Festivals
Scriptural insight
Temple traditions
Dharma guidance
"""

result=subprocess.run(
["./llama.cpp/build/bin/llama-cli","-m","models/llama.gguf","-p",prompt,"-n","600"],
capture_output=True,text=True
)

open("draft.txt","w").write(result.stdout)
