#!/usr/bin/env python3
"""Offline corpus/source integrity checks; no circuit or installed-fit qualification."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def main():
    count=0;fail=[]
    def check(ok,name):
        nonlocal count
        count+=1
        if not ok:fail.append(name)
    rows=load("corpus/catalog.json");guides=load("corpus/guides.json")
    check(len(rows)==86,"first-edition profile coverage")
    check(len(guides)==15,"first-edition guides")
    check(len({p["id"] for p in rows})==len(rows),"unique profile ids")
    check(len({p["doc_url"] for p in rows})==len(rows),"unique profile routes")
    for p in rows:
        for key in ["id","mpn","manufacturer","identity_scope","why","cautions","history","doc_url"]:
            check(bool(p.get(key)),p["id"]+": "+key)
        check((ROOT/"doc/src/content"/(p["doc_url"].strip("/")+".mdx")).is_file(),p["id"]+": rendered profile")
        check(bool(p["sources"]),p["id"]+": explicit sources/leads")
        m=p.get("model")
        if m:check((ROOT/m["path"]).is_file(),p["id"]+": model bytes")
        for s in p["sources"]:
            if s.get("retained_path"):
                path=ROOT/s["retained_path"]
                check(path.is_file(),p["id"]+": retained source")
                if path.is_file() and s.get("sha256"):
                    check(hashlib.sha256(path.read_bytes()).hexdigest()==s["sha256"],p["id"]+": source hash")
    files=load("provenance/source-files.json")
    check(len(files)==53,"retained distinct PDF coverage")
    check(len({f["sha256"] for f in files})==len(files),"PDFs deduplicated by hash")
    for f in files:
        p=ROOT/f["path"]
        check(p.is_file(),f["path"]+": exists")
        if p.is_file():
            b=p.read_bytes()
            check(b.lstrip().startswith(b"%PDF-"),f["path"]+": PDF bytes")
            check(len(b)==f["bytes"],f["path"]+": byte length")
            check(hashlib.sha256(b).hexdigest()==f["sha256"],f["path"]+": sha256")
    for r in load("provenance/step-derivation.json"):
        for which in ["input","output"]:
            p=ROOT/r[which]
            check(p.is_file(),r["id"]+": "+which)
            if p.is_file():
                check(hashlib.sha256(p.read_bytes()).hexdigest()==r[which+"_sha256"],r["id"]+": "+which+" hash")
        mesh=load(r["output"]);n=len(mesh["positions"])
        check(n==r["vertex_count"],r["id"]+": vertex count")
        check(len(mesh["triangles"])==r["triangle_count"],r["id"]+": triangle count")
        check(all(len(t)==3 and all(type(i)is int and 0<=i<n for i in t) for t in mesh["triangles"]),r["id"]+": indices")
        check(r["solid_count"]>=r["imported_top_level_shapes"],r["id"]+": imported whole compound")
        if r["id"]=="pj398sm":check(r["solid_count"]==5,"PJ398SM retained five-solid assembly")
    inv=load(".claude/skills/component-spec-audit/references/inventory.json")
    check(len(inv["lines"])==49,"49 inherited inventory records")
    check(all(p["dnp"] is True and p["placements"]==[] for p in inv["lines"]),"corpus not fitted")
    check(inv["assertions"]["fitted_lines"]==0,"zero fitted assertion")
    sourceinv=load("provenance/instrument-inventory.original.json")
    check({p["mpn"] for p in inv["lines"]}=={p["mpn"] for p in sourceinv["lines"]},"all original identities retained")
    native=[p for p in rows if (p.get("model") or {}).get("kind")=="wrl"]
    check(len(native)==35,"35 native-viewable profiles")
    check(len({p["model"]["id"] for p in native})==22,"22 shared native model files")
    check(sum((p.get("model") or {}).get("kind")=="step-mesh" for p in rows)==3,"3 derived STEP profiles")
    browser=ROOT/"doc/public/assets/corpus-browser.html"
    check(browser.is_file(),"offline browser built")
    if browser.is_file():
        html=browser.read_text()
        check("__DATA__" not in html and "__SCRIPT__" not in html,"browser placeholders replaced")
        match=re.search(r'<script id="corpus-data" type="application/json">(.*?)</script>',html,re.S)
        check(match is not None,"embedded browser data")
        if match:
            data=json.loads(match.group(1))
            check(len(data["profiles"])==len(rows),"browser profile coverage")
            check(len(data["wrl"])==22 and len(data["mesh"])==3,"browser mesh coverage")
    check(not any(p.suffix.lower() in (".ttf",".otf",".woff",".woff2")
       for p in (ROOT/"doc/public").rglob("*")),"no published font files")
    check(not any(p.suffix.lower()==".pdf" for p in (ROOT/"doc/public").rglob("*")),"source PDFs not public")
    queue=load("corpus/acquisition-queue.json")
    check(len({r["id"] for r in queue})==len(queue),"unique acquisition tasks")
    check(all(r["profile_id"] in {p["id"] for p in rows} for r in queue),"acquisition profile references")
    report={"checks":count,"failed":len(fail),"failures":fail,"scope":"Offline documentation/source integrity only"}
    print(json.dumps(report,indent=2))
    return 1 if fail else 0
if __name__=="__main__":raise SystemExit(main())
