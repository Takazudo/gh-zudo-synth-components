#!/usr/bin/env python3
"""Render corpus-owned research pages from authored JSON; never edit native evidence output."""
from __future__ import annotations
import collections, csv, hashlib, html, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/"doc/src/content/docs"
def load(p): return json.loads((ROOT/p).read_text())
def inline(s):
    return str(s).replace("|","\\|").replace("\n"," ").replace("`","'").replace("<","&lt;").replace(">","&gt;")
def front(title,description,position=1):
    return "---\ntitle: "+json.dumps(title,ensure_ascii=False)+"\ndescription: "+json.dumps(description,ensure_ascii=False)+"\nsidebar_position: "+str(position)+"\n---\n\n"
def write(rel,text):
    p=DOCS/rel;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(text,encoding="utf-8")
def model_descriptor(m):
    tr=m["transform"]
    xyz=lambda v:dict(zip(("x","y","z"),v))
    d={"version":1,"packageId":m["package"],"packageLabel":m["package"],
       "modelUrl":m["url"],"offset":xyz(tr["offset"]),"rotation":xyz(tr["rotate"]),"scale":xyz(tr["scale"])}
    return json.dumps(d,separators=(",",":")).encode().hex()
def main():
    rows=load("corpus/catalog.json")
    guides=load("corpus/guides.json")
    sources=load("corpus/source-records.json")
    files=load("provenance/source-files.json")
    categories={"controls":"Pots, faders, switches and buttons","patching":"Jacks, nuts and patch access",
      "analog":"Analog ICs and signal building blocks","logic":"Trigger and state logic","indicators":"LEDs and optical indicators",
      "interconnects":"Board and cable interconnects","power":"Power and rail components","protection":"Fault protection",
      "discretes":"Diodes and transistors","passives":"Resistors and capacitors"}
    grouped=collections.defaultdict(list)
    native=0
    for row in rows:
        grouped[row["category"]].append(row)
        path=f'parts/{row["category"]}/{row["slug"]}.mdx'
        row["doc_url"]="/docs/parts/"+row["category"]+"/"+row["slug"]+"/"
        md=front(row["mpn"],row["role"]+" — "+row["manufacturer"])
        md+=f'**{row["role"]}**\n\n'
        md+='This is a reusable research profile, not a fitted BOM line or an approval to manufacture.\n\n'
        md+='| Field | Corpus record |\n| --- | --- |\n'
        for key,value in [
            ("Manufacturer",row["manufacturer"]),("Part / family",row["mpn"]),
            ("Identity scope",row["identity_scope"]),("Evidence state",row.get("source_state","Research only")),
            ("LCSC code",row.get("lcsc") or "Not established for this identity"),
            ("Use in this corpus","Not fitted; no PCB placement declared")]:
            md+=f'| {key} | {inline(value)} |\n'
        md+='\n## Why it is useful\n\n'+row["why"]+'\n\n## Design cautions\n\n'+row["cautions"]+'\n\n'
        md+='## What the project taught us\n\n'+row["history"]+'\n\n'
        md+='The originating instrument’s acceptance/rejection is contextual. It does not define a universal recommendation for another synth.\n\n'
        source_by={s["source_id"]:s for s in row.get("sources",[])}
        useful=[f for f in row.get("facts",[]) if not any(term in f["fact_id"] for term in [
            "manufacturer","project-selection","product-function","procurement-status","negative-rail-budget","output-stability","mechanical-fit"])]
        if useful:
            md+='## Retained evidence highlights\n\nThese are **inherited scoped facts**, not newly measured values. Follow the exact source and conditions before reuse.\n\n'
            md+='| Recorded claim | Value and conditions | Source / original verdict |\n| --- | --- | --- |\n'
            for f in useful[:7]:
                value=json.dumps(f["value"],ensure_ascii=False) if isinstance(f["value"],(dict,list)) else str(f["value"])
                if len(value)>500:value=value[:497]+'...'
                src=source_by.get(f.get("source_id"),{})
                url=src.get("authoritative_url","")
                label=src.get("document_number") or src.get("document_title") or f.get("source_id","record")
                link=f'[{inline(label)}]({url})' if url.startswith(("http://","https://")) else '`'+inline(label)+'`'
                md+=f'| `{inline(f["fact_id"])}` | `{inline(value)}` {inline(f.get("unit",""))}; {inline(f.get("conditions",""))} | {link}; {inline(f.get("verdict",""))} |\n'
            md+='\n'
        m=row.get("model")
        md+='## 3D / mechanical assets\n\n'
        if m and m["kind"]=="wrl":
            md+='**Inherited family/derived package preview.** Many imported models are intentionally coarse body envelopes, not complete manufacturer solids. Check the original receipt, drawing and mounting stack; the rendered shape does not qualify fit.\n\n'
            md+=f'<PackageModelViewer descriptor="{model_descriptor(m)}" />\n\n'
            md+=f'Local model: `{m["path"]}`. Native rendering is supplied by `zudo-circuit-doc`.\n\n'
            native+=1
        elif m:
            md+='**STEP-derived viewing mesh.** The original STEP is unchanged. Tessellation, input/output hashes and bounds are recorded in `provenance/step-derivation.json`. Manufacturer/family scope is retained, not upgraded by conversion.\n\n'
            md+=f'[Open the interactive hardware viewer](/assets/corpus-browser.html?part={row["id"]}&tab=model).\n\n'
        else:
            md+='**No usable part-specific model published in this edition.** A document or a footprint may exist without a qualified 3D model. No unrelated shape is substituted.\n\n'
        if row.get("native_record_url"):
            md+='[Open the native generated evidence record]('+row["native_record_url"]+'). It preserves original claim wording, locators and verdicts.\n\n'
        elif row.get("owner_skill"):
            md+='The complete inherited owner bundle is retained locally at `.claude/skills/'+row["owner_skill"]+'/`. It is not in the native preview selection because complete publishable model coverage is absent for some records in this group.\n\n'
        md+='## Datasheets, drawings and source leads\n\n'
        seen=set()
        for s in row.get("sources",[]):
            url=s.get("authoritative_url","")
            if not url or url in seen:continue
            seen.add(url)
            if url.startswith(("http://","https://")):
                md+=f'- [{inline(s.get("document_title") or "Source lead")}]({url})'
            else:md+='- Context source: `'+inline(url)+'`'
            if s.get("retained_path"):
                md+=f' — retained local bytes: `{s["retained_path"]}`; SHA-256 `{s.get("sha256","")}`'
            else:md+=' — source metadata/link only in this edition; no local download implied'
            md+='.\n'
        if row.get("supplier_url") and row["supplier_url"] not in seen:
            md+=f'\n[Recorded supplier lead]({row["supplier_url"]}).\n'
        elif row.get("lcsc"):
            md+=f'\n[Recorded LCSC identity C-number](https://www.lcsc.com/product-detail/{row["lcsc"]}.html).\n'
        md+='\nStock, price, lead time and PCBA acceptance are **not refreshed or reserved** by retaining a URL. Source PDFs and vendor CAD retain their original rights; review redistribution before deploying the site publicly.\n'
        write(path,md)
    alltable='| Component | Use | Evidence / model |\n| --- | --- | --- |\n'
    for pos,(category,title) in enumerate(categories.items(),1):
        md=front(title,"Component profiles and reusable decisions",pos)
        md+='Every item links to application notes, exact source identity and the current model boundary. A research candidate is not a manufacturing selection.\n\n'
        md+='| Component | Reusable role | Model |\n| --- | --- | --- |\n'
        for r in grouped[category]:
            badge='STEP-derived' if r.get("model",{} ) and r["model"]["kind"]=="step-mesh" else 'Family/derived preview' if r.get("model") else 'Not published'
            md+=f'| [{inline(r["mpn"])}]({r["doc_url"]}) | {inline(r["role"])} | {badge} |\n'
            alltable+=f'| [{inline(r["mpn"])}]({r["doc_url"]}) | {inline(r["role"])} | {inline(r.get("source_state","Research"))}; {badge} |\n'
        write(f'parts/{category}/index.mdx',md)
    intro=front("Component profiles","A reusable modular-synth component corpus",1)
    intro+=f'**{len(rows)} profiles**: 49 identities from the committed instrument evidence and 37 earlier alternatives, accessories and later research leads. Not all are verified exact components, and none is fitted in this standalone corpus.\n\n'
    intro+='[Open the searchable component browser](/assets/corpus-browser.html) · [Application guides](/docs/guides/) · [Model coverage](/docs/models/) · [Source archive](/docs/evidence/)\n\n'
    intro+='## Browse by purpose\n\n'
    for c,title in categories.items(): intro+=f'- [{title}](/docs/parts/{c}/) — {len(grouped[c])} profiles.\n'
    write('parts/index.mdx',intro+'\n## Full index\n\n'+alltable)
    for i,(s,g) in enumerate(guides.items(),1):
        write(f'guides/{s}.mdx',front(g["title"],"Reusable component-led synth design note",i)+g["body"]+'\n')
    guideindex=front("Application guides","Practical design lessons independent of one instrument",2)
    guideindex+='\n'.join(f'- [{g["title"]}](/docs/guides/{s}/)' for s,g in guides.items())+'\n'
    write('guides/index.mdx',guideindex)
    modelpage=front("Model library and fidelity","Native package previews and recovered detailed hardware CAD",3)
    modelpage+='The native framework publishes **22 shared WRL package previews across 35 evidence records**. Many are deliberately coarse drawing-derived envelopes. Three additional retained STEP assets have tessellated viewing meshes in the supplementary browser. There is no claim of exact 3D coverage for all 86 profiles.\n\n'
    modelpage+='[Open the model browser](/assets/corpus-browser.html?models=1&tab=model) · [Read the model-fidelity policy](/docs/guides/model-fidelity/)\n\n'
    modelpage+='| Profile | Rendering | Scope |\n| --- | --- | --- |\n'
    for r in rows:
        if r.get("model"):
            modelpage+=f'| [{inline(r["mpn"])}]({r["doc_url"]}) | {r["model"]["kind"]} | {inline(r["model"]["fidelity"])} |\n'
    modelpage+='\nOriginal STEP and native WRL paths, hashes, provenance and derived-mesh bounds are in the package. The original manufacturer and community notices remain attached. No threads, joints, stiffness or assembled fit are inferred from a rendered surface.\n'
    write('models/index.mdx',modelpage)
    evidence=front("Sources and provenance","Retained documents, exact-byte receipts and inherited scope",4)
    evidence+=f'This edition retains **{len(files)} distinct PDF files**. It contains {len(sources)} inherited/historical source-metadata records; some records share a file, and others are links or project-state sources only. A PDF count is not a count of qualified components.\n\n'
    evidence+='Every retained PDF passed a magic-header, SHA-256 and parser-open check. That is an acquisition/usability check, not a renewed audit of every figure and rating. Source facts keep their originating locators and conditions. Original acquisition dates are not changed to today.\n\n'
    evidence+='`provenance/source-files.json` maps each hash to a local path and original source location. `corpus/source-records.json` maps component source IDs to retained bytes where a hash match exists. Raw PDFs stay outside `doc/public`; the site links their original URLs.\n\n'
    evidence+='[Research/evidence workflow](/docs/guides/source-workflow/) · [History and corrections](/docs/history/)\n\n'
    evidence+='| Retained PDF | Pages | SHA-256 prefix |\n| --- | --- | --- |\n'
    for f in sorted(files,key=lambda x:x['path']):
        evidence+=f'| `{inline(Path(f["path"]).name)}` | {f["pages"]} | `{f["sha256"][:16]}` |\n'
    write('evidence/index.mdx',evidence)
    history=front("Source history and corrections","Preserve alternatives without preserving mistakes as facts",5)
    history+='This corpus is based on the available conversation archives and the committed instrument snapshot `fac99297702eabd97bbc3fae58876af4017fcaea`. The framework was read at `5d0e2b630776489d394be341586b889dfe0d1cb8`. The 149-line Git history export records published branches at export time; it does not include uncommitted local work.\n\n'
    history+='## Decisions preserved\n\n| Stage | Reusable lesson |\n| --- | --- |\n| Early component collection / R06 | Standard synth-shop parts are acceptable; all electrical soldering must be completed by the factory. Separate pot cap, shaft, washer and body envelopes. |\n| R08–R12 | Correct the small Bourns shaft scale; distinguish toggle contact states; investigate LED faders, then retain them as alternatives when the instrument changes to pots and separate stage LEDs. |\n| R13–R17 | Dense packing cannot replace the panel/PCB Z-stack. Jack bushings must clamp through normal holes. Separate interface boards can accommodate different depths. |\n| R18–R19 | A 3D gap is not a required enclosure depth. Place actual component envelopes and the power assembly before claiming thickness. |\n| R20–R21 | A shared grid needs real package limits. New S&H and slew functions need separate storage and lag circuits, not just another knob. |\n| Later committed circuit work | Exact pin/footprint evidence, compact LEDs, source requirements and connector/return accounting supersede earlier provisional selections. |\n\n'
    history+='## Corrections that must not be lost\n\nC908280 is the two-position toggle candidate, not the three-position counterpart. SRBV160803 is a rotary selector, not an illuminated fader. LF398M/NOPB is SOIC-14, not the eight-pin DIP geometry. Bourns PTL lever-height options are not slider-travel options. A PJ398SM community model is not exact WQP518MA manufacturer CAD. An arbitrary 8.3 mm dress-nut envelope is not a verified EARS dimension. A blank microcontroller is not programmed NOISE2. Replacing ALPS or faders in one instrument does not invalidate them for all synths.\n\n'
    history+='The corpus does not overwrite the instrument. Source project decisions remain under `provenance/instrument-decisions/`, and old research registers under `provenance/history/`. New prose separates reusable advice from those contextual results.\n'
    write('history/index.mdx',history)
    home=front("Modular Synth Component Corpus","Component evidence and reusable design knowledge from a patchable instrument project",1)
    home+='**Choose parts by electrical function, physical mounting and evidence—not by a familiar name or a convincing render.**\n\n'
    home+=f'This first edition collects **{len(rows)} profiles**, **{len(guides)} application guides**, **{len(files)} retained PDFs**, native package previews and recovered detailed hardware CAD. It is a standalone research library built with the official `zudo-circuit-doc` initializer, not a new instrument BOM.\n\n'
    home+='[Browse the components](/docs/parts/) · [Open the interactive browser](/assets/corpus-browser.html) · [Read the application guides](/docs/guides/) · [Inspect model coverage](/docs/models/)\n\n'
    home+='## What is different from the instrument documents\n\nThe instrument remains ongoing. Here, earlier ALPS controls, illuminated sliders, alternate toggles, jack families, caps and connector leads remain useful even when no longer selected for that panel. Later exact-component records are retained with their source scope, rather than rewriting the entire conversation as a final approval.\n\n'
    home+='The delivery constraint remains central: **no electrical soldering at home**. Ordinary external parts are allowed when factory sourcing/assembly is agreed. A source URL is not a stock reservation, a schema pass is not circuit validation, and a mesh is not an installed-fit result.\n\n'
    home+='## Start with the decision you are making\n\n- Choosing hands-on controls: [pots](/docs/guides/potentiometers/), [faders](/docs/guides/faders/) and [toggles](/docs/guides/toggle-functions/).\n- Designing a patchable circuit: [sample/hold and slew](/docs/guides/sample-hold-slew/), [mixers and VCAs](/docs/guides/mixers-attenuverters/) and [amplifier choice](/docs/guides/amplifier-choice/).\n- Making it physically buildable: [panel stack](/docs/guides/panel-stack/), [interconnects](/docs/guides/interconnects/) and [factory assembly](/docs/guides/factory-assembly/).\n\n'
    home+='[Sources and provenance](/docs/evidence/) explains which bytes are retained and which links remain acquisition leads. [History](/docs/history/) records decisions and corrected assumptions. No site deployment, component purchase or fabrication release is included.\n'
    write('project/index.mdx',home)
    write('project/next-actions.mdx',front("Next corpus tasks","A local-agent continuation point")+
        "Continue the corpus independently of PCB development.\n\n1. Review the profiles most relevant to the next instrument. Keep unknown suffixes, stock and physical fit open.\n2. Retrieve missing original sources such as the PTL PDF and exact alternate-control drawings using `scripts/acquire_sources.py`; retain headers/hash/date and inspect the document before updating claims.\n3. Obtain exact or better-family models for bushingless pots, toggle nuts/levers, jack lots, button/plungers and complete connectors. Do not upgrade the existing envelope proxies by naming alone.\n4. Add more precise application notes and measured coupons as evidence becomes available. Attribute each result to its actual board, population and setup.\n5. Run the corpus validator and official generator/check/build/site checks before publication. Review third-party asset rights first.\n\nThe instrument's open protection/routing issues are not tasks to silently solve inside this documentation project. No hardware coordinates, circuit limits or manufacturing scope are changed here.\n")
    write('architecture/index.mdx',front("Corpus architecture","How authored research, source evidence and previews fit together")+
        "This is a reusable documentation corpus, not another instrument circuit. [Architecture overview](./overview.mdx) explains the authored catalogue, inherited evidence, generated native pages, source archives and model derivation. No PCB population or manufacturing release is selected here.\\n")
    write('architecture/overview.mdx',front("Corpus architecture","Authored notes, inherited evidence, local sources and generated pages")+
        "`corpus/catalog.json` and `corpus/guides.json` are the authored content inputs. `scripts/build_corpus.py` renders their profile and guide pages. `.claude/skills/component-*/` preserves inherited exact-component bundles; the standard generator owns `/docs/components/`. `sources/` and `provenance/` retain documents, hashes, history and original CAD notices. `corpus/models/` contains only recorded STEP tessellations.\n\nThe public native preview directory remains framework-owned. The supplementary single-file component browser is generated as a separately allowlisted asset, using the same catalogue and model receipts. Missing models are explicit, not replaced with arbitrary components.\n\nThis project has no schematic or board binding and no fitted inventory. Source-context facts and diagram proposals must not be treated as new component approvals.\n")
    write('decisions/index.mdx',front("Corpus decisions","Scope, identity and publication policy")+
        "The corpus is independent of the instrument repository. English is retained from the source engineering documents. Current exact identities and historical alternatives are both searchable. All inventory lines are not fitted; the original inventory is kept in provenance. Existing evidence verdicts remain inherited and scoped. Raw manufacturer documents are local archive files, not automatically published downloads. Native model coverage is limited to the supported package selection; additional detailed STEP meshes have separate derivation receipts. No factory order or deployment is authorized.\n")
    write('research/index.mdx',front("Research collection","Choose a component or a reusable application problem")+
        "[Component profiles](/docs/parts/) collect all first-edition entries. [Application guides](/docs/guides/) connect those entries to synth functions and mechanical construction. [Source history](/docs/history/) preserves alternatives and corrects earlier assumptions. The raw inherited evidence remains separately inspectable in the [native evidence catalogue](/docs/components/).\n")
    write('verification/index.mdx',front("Verification boundary","Checks that establish corpus integrity, not hardware performance")+
        "The validation report supplied with this edition records actual command exits, source hashes, model conversion receipts and browser tests. The native engine checks the inherited manual inventory and pin assets; it does not bind this corpus to a schematic or PCB. No new native KiCad rendering, circuit simulation or physical coupon has been performed by the corpus build. Existing footprint previews are retained origin artifacts, not newly claimed measurements.\n\nRun `python3 scripts/check_corpus.py` for corpus integrity and the package scripts for framework/evidence/build checks. A green documentation build is not authorization to energize or fabricate the original instrument.\n")
    (ROOT/"corpus/catalog.json").write_text(json.dumps(rows,indent=2,ensure_ascii=False)+"\n")
    report={"profiles":len(rows),"guides":len(guides),"categories":len(categories),"native_preview_profile_pages":native,
            "native_selected_records":35,"native_shared_models":22,"detailed_step_models":3,
            "retained_distinct_pdfs":len(files),"inventory_fitted":0,"scope":"documentation only"}
    (ROOT/"provenance/content-build.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
if __name__=="__main__":main()
