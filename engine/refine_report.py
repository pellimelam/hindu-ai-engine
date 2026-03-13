# refine_report.py
import subprocess

draft=open("draft.txt").read()

prompt=f"""
Improve the following Hindu knowledge report.

Make it clearer, deeper, and better structured.

{draft}
"""

result=subprocess.run(
["./llama.cpp/build/bin/llama-cli","-m","models/model.gguf","-p",prompt,"-n","600"],
capture_output=True,text=True
)

open("final.txt","w").write(result.stdout)
