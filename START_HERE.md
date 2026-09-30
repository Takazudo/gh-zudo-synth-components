# Start here

## Read the corpus from this repository

1. Clone `Takazudo/gh-zudo-synth-components` and open a terminal in that directory.
2. With Node >=22.18, pnpm 11.5.2 and Python 3, run `pnpm install --frozen-lockfile`.
3. Run `pnpm build`, then `python3 scripts/serve.py`.
4. Open `http://127.0.0.1:8765/docs/project/` and compare Parts, Guides, Models and Evidence.
5. The standalone `doc/public/assets/corpus-browser.html` also opens locally without a server.

A Git clone excludes dependencies and `doc/dist`; build it first. The original
ZIP was different: it bundled a prebuilt site. No GitHub Pages or other site
deployment is performed by the repository's checking workflow.

The build is derived from the checked-out source. `VALIDATION.md` preserves the
original edition's test scope; the repository workflow records new results.
See `provenance/` for exact source scope and the original import hash manifest.

## Continue with an agent

Give the agent `LOCAL_AGENT_PROMPT.md`, then let it read `circuit/WORKFLOW.md`.
This is a documentation corpus, not the instrument PCB worktree.

Prioritize missing exact mechanical drawings and complete assembly models for
the Bourns pots, Dailywell toggles, QingPu jack/nut combination and selected
connectors. Recover the illuminated-fader evidence because it remains useful
outside the final instrument. Existing family/envelope previews stay explicitly
labeled until better scoped assets are retained.

Do not promote a source because a URL resolves or a file has a .pdf suffix.
Check manufacturer, exact suffix, document/revision, page locator, pin numbering,
conditions, CAD origin, model units and rights before changing an evidence verdict.

## Rebuild

Use the commands in README.md. `pnpm build` regenerates authored corpus pages,
the standalone browser, native component pages, selected models and the site.
`pnpm corpus:check` verifies local source hashes and corpus invariants.
The initial install needs package-registry access; the installed build is offline.

No production domain or deployment is configured. Do not enable public source
downloads until the rights review is complete. Commit new work to this corpus
repository; never point this directory at the instrument's existing worktree.
