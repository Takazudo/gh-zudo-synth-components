# Validation — Modular Synth Component Corpus 0.1.0

Date: 2026-09-30. This is documentation and source-integrity work, not a PCB or
physical component qualification.

## Input boundary

- Instrument main rechecked: `fac99297702eabd97bbc3fae58876af4017fcaea`.
- Framework main rechecked: `5d0e2b630776489d394be341586b889dfe0d1cb8`.
- Official initializer/runtime: 0.1.0. The exported scaffold was initialized and
  dependency-installed on GitHub Actions run 36701568494. Its exported source
  checksums were verified before extraction.
- Available R06–R21 research archives: 60 retained registry/note files.
- Unpublished local issue-38 work was not inspected or imported.
- Instrument main was not changed. The earlier isolated export branch only
  generated the read-only seed; no corpus deployment or new remote repository
  was created.

## Completed checks

| Check | Actual result |
| --- | --- |
| Offline corpus/source integrity | PASS: 1,291 assertions |
| PDF bytes and hashes | PASS: 53 distinct retained documents; PDF magic/hash/parser-open checks |
| STEP conversion | PASS: all imported shapes included, originals unchanged; 3 receipts with exact input/output hashes |
| Original shared package model publication | PASS: 22 selected models; no unexpected native-preview files |
| Canonical circuit-doc validation | PASS: 49 manual identities, 0 fitted, 0 declared placements; pin-asset check performed |
| Native generation/check | PASS: 35 published records, 74 selected sources, 39 generated pages; outputs current |
| Documentation type check | PASS |
| Documentation site build | PASS: 251 generated pages reported by zfb |
| Built component-reference check | PASS: 35 records, 22 footprint SVGs and 22 models |
| Publication scope/denied-value scan | PASS: no denied value reached a published artifact; no unapproved raw source/CAD exposure |
| Internal built links and anchors | PASS: 36,614 internal links and 2,738 ID attributes inspected |
| Supplementary browser | PASS: 43 checks, including all 25 unique mesh assets and mobile layout |
| Browser unhandled JavaScript errors | 0 in successful final run |
| Supplementary browser network requests | 0 in successful final run |
| Repeated authored-page generation | PASS: byte-identical generated content in the inspected source-page set |
| No font files in delivery | Checked again by package builder |

The native inventory provider explicitly reports that schematic/placement binding
is not performed. Its PASS does not establish electrical suitability, stock,
assembly acceptance or installed geometry.

## Browser/graphics boundary

Managed browser policy blocks local URL/file navigation in this container.
The supplementary browser was tested with **its exact standalone HTML bytes**
through `page.set_content`, not by claiming a successful local-file launch.

WebGL context creation was unavailable in this environment. The delivered
supplementary viewer therefore used its real Three.js **SVGRenderer fallback**.
Geometry projection, all 25 imported mesh assets, camera changes, wireframe,
search/filter/source tabs and mobile width were exercised. The fallback preserves
model geometry; it is not a screenshot substituted for a live viewer.

Native circuit-doc WebGL rendering was NOT RUN successfully. Its built component
bindings, model references and descriptors passed the framework checks; 35
authored pages contain the native model surface. A guide page was visually
inspected using its built HTML with local CSS inlined and scripts omitted:
that is a static-layout check, not full-site hydration testing.

## Not performed

- No new native KiCad footprint rendering or CAD-oracle geometry validation.
- No circuit simulation, bench measurement, factory coupon or thermal test.
- No live supplier stock/price reservation or assembly quotation.
- No complete fresh audit of every inherited component fact.
- No automatic source promotion from an acquisition URL.
- No deployment, purchase, fabrication file generation or changes to the
  instrument's unpublished worktree.

Inherited footprint renders and source verdicts are labeled as inherited.
The earlier failures while developing the browser/public-data projection are
recorded in the command logs; only the final successful artifacts are packaged.
An unrelated Python environment startup warning appears in the mesh/browser
subprocess logs; both completed with exit 0 and explicit output receipts.

## Reproduce

Use README.md's pinned install/build/check commands.
For the extra browser smoke test, install Playwright in a separate Python
environment and run:

```sh
python scripts/test_browser.py --chromium /path/to/chromium
```

Reading the prebuilt site requires only `python3 scripts/serve.py`. Local network
navigation itself was not testable here; the server is intentionally loopback-only.

Detailed logs: `provenance/validation/`.
Model derivation: `provenance/step-derivation.json`.
Source identities/hashes: `provenance/source-files.json`.
