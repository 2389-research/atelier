import sys, os, subprocess, time, json
sys.path.insert(0, "/Users/michaelsugimura/Documents/GitHub/atelier/skills/atelier-dispatch")
import dispatch
TASKS="/Users/michaelsugimura/Documents/GitHub/atelier/eval/tasks"
GATE="python3 -m pytest -q"; FN="06-ledger-v2.md"

def basic(num):
    d=f"/Users/michaelsugimura/Documents/GitHub/atelier-{num}-basic"
    os.system(f"rm -rf {d}; mkdir -p {d}; cp {TASKS}/{FN} {d}/spec.md"); os.chdir(d)
    _o=subprocess.run
    def p(*a,**k): k['timeout']=3000; return _o(*a,**k)
    subprocess.run=p; t=time.time()
    try: dispatch.run_pipeline(GATE)
    except SystemExit as e: print(f"[{num} BASIC] ABORT {e}")
    subprocess.run=_o
    rm=json.load(open(d+"/run_manifest.json")) if os.path.exists(d+"/run_manifest.json") else {}
    print(f"[{num} BASIC] {int(time.time()-t)}s | plan ${rm.get('plan_cost_usd',0):.3f}+exec ${rm.get('dispatch_cost_usd',0):.3f}+fix ${rm.get('fix_cost_usd',0):.3f}({rm.get('fix_rounds',0)}r)=${rm.get('total_cost_usd',0):.3f} | gate={rm.get('gate_pass')}")

def two_pass(num):
    d=f"/Users/michaelsugimura/Documents/GitHub/atelier-{num}-2pass"
    os.system(f"rm -rf {d}; mkdir -p {d}; cp {TASKS}/{FN} {d}/spec.md"); os.chdir(d)
    _o=subprocess.run
    def p(*a,**k):
        k['timeout']=3000
        if a and isinstance(a[0],list) and 'claude' in a[0] and '--effort' not in a[0]:
            a=(list(a[0])+['--effort','low'],)+a[1:]
        return _o(*a,**k)
    subprocess.run=p
    spec=open("spec.md").read(); t=time.time()
    draft=("You are the architect. From the TASK SPEC, produce EXACTLY two files, each wrapped <FILE path=\"...\">"
     "...</FILE>, nothing else:\n1) contract.md — cross-sprint surface under clear `## ` headers.\n2) sprints.jsonl — "
     "one JSON/line {\"id\":\"SPRINT-001\",\"tier\":\"haiku\",\"kind\":\"generate\",\"deps\":[],\"brief\":\"...\"}. "
     "ONE file per sprint; modules not monoliths.\n\nTASK SPEC:\n"+spec)
    d1,c1=dispatch.call_model(draft,"sonnet",dispatch.SYS_PLAN); dispatch.write_files(d1)
    ct=open("contract.md").read() if os.path.exists("contract.md") else ""
    sp=open("sprints.jsonl").read() if os.path.exists("sprints.jsonl") else ""
    refine=("Lead architect REFINEMENT pass. Make the plan executable by a SMALL model (Haiku) with ZERO judgment: "
     "commit every architectural decision; PIN every cross-sprint convention (shared shapes, exact signatures+return "
     "shapes, ordering/edge-cases/invariants); fix wrong/missing details; flesh each brief with concrete approach + "
     "acceptance criteria; ONE file per sprint. Output improved <FILE path=\"contract.md\">...</FILE> and "
     "<FILE path=\"sprints.jsonl\">...</FILE>, nothing else.\n\nTASK SPEC:\n"+spec+"\n\nDRAFT contract.md:\n"+ct+
     "\n\nDRAFT sprints.jsonl:\n"+sp)
    d2,c2=dispatch.call_model(refine,"sonnet",dispatch.SYS_PLAN); dispatch.write_files(d2)
    dc=dispatch.execute()
    ok,out=dispatch.run_gate(GATE); fc=0.0; r=0
    while not ok and r<2: r+=1; fc+=dispatch.fix(out); ok,out=dispatch.run_gate(GATE)
    subprocess.run=_o
    json.dump({"plan_draft":round(c1,4),"plan_refine":round(c2,4),"dispatch_cost_usd":round(dc,4),
     "fix_cost_usd":round(fc,4),"fix_rounds":r,"gate_pass":ok,"total_cost_usd":round(c1+c2+dc+fc,4)},
     open("run_manifest.json","w"),indent=2)
    print(f"[{num} 2PASS] {int(time.time()-t)}s | draft ${c1:.3f}+refine ${c2:.3f}+exec ${dc:.3f}+fix ${fc:.3f}({r}r)=${c1+c2+dc+fc:.3f} | gate={'PASS' if ok else 'FAIL'}")

basic("06v2"); two_pass("06v2")
