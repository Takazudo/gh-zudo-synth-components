# Modular Synth Component Corpus

A reusable component knowledge library for modular and patchable synthesizer development,
created with `create-zudo-circuit-doc@0.1.0` and `@takazudo/zudo-circuit-doc@0.1.0`.
The package name remains `zudo-modular-component-corpus`; its repository is
[Takazudo/gh-zudo-synth-components](https://github.com/Takazudo/gh-zudo-synth-components).

## Run from a fresh clone

Requires Node.js >=22.18, Python 3, and pnpm 11.5.2.

```sh
git clone https://github.com/Takazudo/gh-zudo-synth-components.git
cd gh-zudo-synth-components
pnpm install --frozen-lockfile
pnpm build
python3 scripts/serve.py
```

Open `http://127.0.0.1:8765/docs/project/`. The server binds to your own computer
only; stop it with Ctrl-C. For live authoring, use `pnpm dev` after installation.

**A Git clone does not include `doc/dist` or `node_modules`.** Build it first.
The original delivered ZIP was different: it included a prebuilt reading site.

The standalone `doc/public/assets/corpus-browser.html` can also be opened locally
without a server. Research and its scoped viewing assets are embedded: no CDN,
external font, model or JavaScript requests. The supplementary viewer uses
geometric SVG projection when WebGL is unavailable. Native circuit-doc component
pages retain their own WebGL viewer. Full documentation links need the local site;
original source links need internet access. GitHub's file page displays HTML
source, not the running application.

## First edition

| Material | Coverage |
| --- | ---: |
| Component, family and accessory profiles | 86 |
| Application guides | 15 |
| Distinct retained PDFs | 53 |
| Inherited identity/evidence records | 49 |
| Selected native circuit-doc records | 35 |
| Shared native WRL package models | 22 |
| Additional retained STEP-derived viewing meshes | 3 |

The profiles combine 49 inherited instrument records and 37 historical,
alternative or unresolved research leads. The three detailed STEP viewing assets
are ALPS rotary-pot geometry, an ALPS slider and a community PJ398SM-family jack.
Exact manufacturer CAD, family geometry, community assets and simplified body
envelopes remain explicitly distinguished.

This is **not a fitted BOM, a stock guarantee or a manufacturing release**. All
49 imported inventory records are not fitted, with zero declared placements.
Their identities and evidence verdicts retain their original scope; the original
instrument inventory is preserved separately. There is no model for every part.

## Source and import provenance

- Instrument: `Takazudo/zudo-osc-hole-field` at
  `fac99297702eabd97bbc3fae58876af4017fcaea`.
- Framework: `Takazudo/zudo-circuit-doc` at
  `5d0e2b630776489d394be341586b889dfe0d1cb8`.
- Available conversation research spans R06–R21; 60 historical registry/note files
  and the source Git log are retained. Unpublished local issue-38 work is outside
  this corpus's reviewed source boundary.

`provenance/repository-import.json` records the 798-file original source baseline,
verified against the delivered ZIP's source-tree hash. Generated outputs are
rebuilt. `provenance/repository-adjustments.json` separately records the small
missing-model UI correction applied after that verification. Repository setup
and CI changes are visible in Git history. One-time transport scripts/chunks are
not part of this source tree.

Earlier parts remain useful even when removed from the compact instrument. Their
profiles explain why they were considered, why that particular layout moved on,
and what another synth still needs to verify. The instrument repository is a
read-only reference, not this project's working tree.

## Author and check

```sh
pnpm corpus:generate
pnpm circuit:check
pnpm circuit:generate
pnpm check
pnpm build
pnpm check:site
pnpm corpus:check
```

The canonical editing agreement is `circuit/WORKFLOW.md`. Authored profile and
guide source is in `corpus/catalog.json` and `corpus/guides.json`.
`scripts/build_corpus.py` renders corpus-owned pages; `scripts/build_browser.mjs`
bundles the standalone viewer using the locked runtime dependencies.
`notes-current.json` and `notes-history.json` preserve editorial intake, but the
normalized catalog is the editing authority.

Do not hand-edit native `doc/src/content/docs/components/**`, native preview
outputs or `circuit/generated/preflight.json`. Update their evidence or selection
and run the framework generator. The retained KiCad library is still named
`zudo-osc-hole-field` to preserve original footprint/model references and their
evidence chain. This does not imply a new PCB design.

## Automated checks

Pull requests and pushes to `main` run the read-only **Corpus checks** workflow:
evidence validation, generated-output drift, documentation build, publication
scope, internal links, corpus integrity and embedded-browser regression checks.
The workflow retains test reports and a built reading site as artifacts. It does
not deploy a website, acquire new component evidence or place orders.

Browser results record the actual WebGL or SVG renderer. Native framework model
bindings and files are checked by the framework; this does not replace a native
viewer visual review or any hardware qualification.

## CAD and evidence acquisition

Viewing the supplied models does not require CAD software. To intentionally
rederive the three meshes, use CadQuery 2.8.0 / OCP 7.9.3.1 in a separate Python
environment and run:

```sh
python scripts/derive_step_meshes.py
pnpm corpus:generate
```

Original STEP files remain unchanged. The script combines all imported shapes,
not only the first solid. Native KiCad footprint rendering is optional and uses
the pinned Docker oracle; this import does not claim a new native CAD render.

`python3 scripts/acquire_sources.py` lists the open queue without network requests.
An explicit `--id ITEM --apply` downloads into an unreviewed incoming area and
records bytes and redirect origin. It never promotes evidence automatically.

## Rights and publication

See `SOURCE-RIGHTS.md`. Third-party datasheets and CAD keep their original rights
and notices; they are not relicensed under a blanket project license. The source
repository includes retained reference files. The built site omits raw source-PDF
downloads and includes only the allowed viewing assets. Review applicable asset
terms before a website deployment or further redistribution.

No website is deployed by this import, no order is placed, and no physical fit or
electrical performance is qualified. See `START_HERE.md`, `LOCAL_AGENT_PROMPT.md`,
`VALIDATION.md` and the repository workflow results for scope and continuation.
