#!/usr/bin/env python3
"""
atelier dispatch engine — LLM-as-tool, no subagents, no API key.

Reads contract.md + units.jsonl from cwd. For each unit, makes ONE bare
`claude -p --model <tier> --bare` completion (subscription OAuth, ~no harness),
captures the text, writes any <FILE path="..."> blocks to disk, records per-call
cost. Emits manifest.json. The orchestrator never ingests unit outputs — only the
manifest.

units.jsonl: one JSON object per line:
  {"id":"UNIT-001","tier":"haiku","kind":"generate","brief":"...","deps":[]}
    kind: "generate" -> model emits <FILE> blocks, script writes them
          "brief"    -> model emits markdown, script saves to out (default briefs/<id>.md)
"""
import json, subprocess, re, os, sys, pathlib, concurrent.futures

def call_model(prompt, model):
    p = subprocess.run(
        ["claude","-p",prompt,"--model",model,"--bare","--output-format","json"],
        capture_output=True, text=True, timeout=900)
    try:
        d = json.loads(p.stdout)
        return d.get("result",""), float(d.get("total_cost_usd",0) or 0)
    except Exception:
        sys.stderr.write(f"[dispatch] parse fail: {p.stdout[:200]} {p.stderr[:200]}\n")
        return p.stdout, 0.0

FILE_RE = re.compile(r'<FILE path="([^"]+)">\r?\n?(.*?)\r?\n?</FILE>', re.DOTALL)
def write_files(text, root):
    written = []
    for m in FILE_RE.finditer(text):
        rel, content = m.group(1), m.group(2)
        path = os.path.join(root, rel)
        pathlib.Path(os.path.dirname(path) or ".").mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            f.write(content if content.endswith("\n") else content + "\n")
        written.append(rel)
    return written

def build_prompt(contract, unit):
    if unit.get("kind") == "brief":
        return (f"Write a terse build brief (bullets + concrete acceptance criteria) "
                f"for a capable executor model. Output ONLY the brief markdown, no preamble.\n\n"
                f"CONTRACT (shared decisions — reference, do not restate):\n{contract}\n\n"
                f"UNIT SPEC:\n{json.dumps(unit, indent=2)}\n")
    return (f"You are an expert programmer building ONE unit of a larger project. Honor "
            f"the CONTRACT exactly (it pins the cross-unit interfaces). Output ONLY the "
            f"file(s) for your unit, each wrapped EXACTLY as:\n"
            f'<FILE path=\"relative/path.ext\">\n...file contents...\n</FILE>\n'
            f"No prose, no markdown fences, nothing outside FILE blocks.\n\n"
            f"CONTRACT:\n{contract}\n\nYOUR UNIT BRIEF:\n{unit.get('brief','')}\n")

def main():
    root = os.getcwd()
    contract = open("contract.md").read() if os.path.exists("contract.md") else ""
    units = [json.loads(l) for l in open("units.jsonl") if l.strip()]
    pending = {u["id"]: u for u in units}
    done, manifest, total = set(), [], 0.0
    while pending:
        ready = [u for u in pending.values() if all(d in done for d in u.get("deps", []))]
        if not ready:  # break deadlock
            ready = list(pending.values())
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            futs = {ex.submit(call_model, build_prompt(contract, u), u.get("tier","haiku")): u for u in ready}
            for fut in concurrent.futures.as_completed(futs):
                u = futs[fut]; text, cost = fut.result(); total += cost
                if u.get("kind") == "brief":
                    out = u.get("out", f"briefs/{u['id']}.md")
                    pathlib.Path(os.path.dirname(out) or ".").mkdir(parents=True, exist_ok=True)
                    open(out, "w").write(text); files = [out]
                else:
                    files = write_files(text, root)
                manifest.append({"id": u["id"], "tier": u.get("tier"), "kind": u.get("kind","generate"),
                                 "cost_usd": round(cost,5), "files": files})
                done.add(u["id"]); del pending[u["id"]]
    json.dump({"units": manifest, "dispatch_cost_usd": round(total,4)}, open("manifest.json","w"), indent=2)
    print(f"dispatched {len(manifest)} units · dispatch tier cost ${total:.4f}")
    for m in sorted(manifest, key=lambda x:x["id"]):
        print(f"  {m['id']:9} [{m['tier']:6}] ${m['cost_usd']:.4f} -> {m['files']}")

if __name__ == "__main__":
    main()
