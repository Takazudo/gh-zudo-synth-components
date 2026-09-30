# Modular Synth Component Corpus

A standalone, reusable component knowledge library for modular and patchable synthesizer development.
Created with the official `create-zudo-circuit-doc@0.1.0` initializer and
`@takazudo/zudo-circuit-doc@0.1.0`, on zudo-doc 5.27.0 / zfb 2.21.0.

## Read immediately

The package includes a built site. With Python 3:

```sh
python3 scripts/serve.py
```

Open `http://127.0.0.1:8765/docs/project/`.
The server binds to loopback only. Stop it with Ctrl-C.

`doc/public/assets/corpus-browser.html` is a separate single-file browser that can
be opened directly. It embeds its research and scoped 3D viewing assets, with no
external font, model or JavaScript requests. The supplementary viewer falls back to Three.js SVG projection when WebGL is
unavailable. Native circuit-doc model pages retain their normal WebGL viewer.
Full documentation links require
the local site; original source URLs require internet access.

## First edition

- 86 component, family and accessory profiles: 49 imported instrument identities
  and 37 historical/alternative/research leads.
- 15 authored application guides and a searchable category index.
- 53 distinct retained PDFs, with source origins and SHA-256 manifests.
- Circuit-doc's native evidence catalogue: 35 published records, 22 shared WRL
  package previews and inherited footprint previews.
- Three retained STEP assets with derived browser meshes: the ALPS rotary
  potentiometer, ALPS slide potentiometer, and a community PJ398SM-family jack.
- Original drawings/CAD, acquisition queue, source notices, source and model
  fidelity records, and local-agent instructions.

This is not a fitted BOM, a list of guaranteed-stock parts, or a completed circuit.
All 49 imported inventory records are deliberately **not fitted**, with zero
declared placements. Their source-project identities and evidence verdicts retain
their original scope. The original inventory is preserved separately.

## Source boundary

Instrument: `Takazudo/zudo-osc-hole-field` at
`fac99297702eabd97bbc3fae58876af4017fcaea`.
Framework reference: `Takazudo/zudo-circuit-doc` at
`5d0e2b630776489d394be341586b889dfe0d1cb8`.

Available conversation research spans R06–R21. The package retains 60 historical
registry/note files and the source Git log. It does not contain the unpublished
local issue-38 worktree or assert that all work after the snapshot was inspected.

Earlier parts remain useful even when removed from the compact instrument:
the library records *why they were considered*, *why that particular layout
moved on*, and *what another synth still needs to verify*.

## Develop the docs locally

Requires Node >=22.18 and the package-pinned pnpm 11.5.2.

```sh
pnpm install --frozen-lockfile
pnpm corpus:generate
pnpm circuit:check
pnpm circuit:generate
pnpm check
pnpm build
pnpm check:site
pnpm corpus:check
```

`pnpm dev` starts the framework's authoring workflow.
Do not edit `doc/src/content/docs/components/**`, native preview outputs, or
`circuit/generated/preflight.json` by hand.

Authored profile and guide source is in `corpus/catalog.json` and
`corpus/guides.json`. `scripts/build_corpus.py` renders only corpus-owned pages.
The `notes-current.json` / `notes-history.json` files preserve the editorial
intake that produced this edition; **the normalized catalog is the editing
authority**. The browser is bundled by `scripts/build_browser.mjs` from the
locked Three.js/esbuild packages already required by the documentation runtime.

The retained KiCad library is still named `zudo-osc-hole-field`. That preserves
original footprint/model references and their evidence chain. It does not mean
this corpus has a new board design.

## CAD and sources

Reading the supplied meshes does not require CAD software.
To intentionally rederive them, install CadQuery 2.8.0 / its OCP 7.9.3.1 backend
in a separate Python environment, then run:

```sh
python scripts/derive_step_meshes.py
pnpm corpus:generate
```

Original STEP files remain unchanged. The script combines **all imported shapes**,
not only the first solid. Native KiCad footprint rendering remains optional and
requires the pinned Docker oracle; it was not rerun in this edition.

`python3 scripts/acquire_sources.py` lists the open source queue without network
requests. An explicit `--id ITEM --apply` downloads a direct PDF into the
unreviewed incoming area, recording its bytes and redirect origin. It never
promotes evidence automatically.

## Rights and publishing

See `SOURCE-RIGHTS.md`. Third-party datasheets/CAD keep their original rights.
The supplied public site omits source-PDF downloads but includes viewing assets.
Review their terms before public deployment. This edition is delivered for local
research and editing; no site is deployed, order placed, or hardware qualified.

See `START_HERE.md`, `LOCAL_AGENT_PROMPT.md`, and `VALIDATION.md`.
