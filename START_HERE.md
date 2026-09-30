# Start here

## Inspect the corpus now

1. Extract the full package and open a terminal in `zudo-modular-component-corpus`.
2. Run `python3 scripts/serve.py`.
3. Open `http://127.0.0.1:8765/docs/project/`.
4. Compare the Parts, Guides, Models, and Evidence sections.
5. The standalone `doc/public/assets/corpus-browser.html` also opens without a server.

The built site and the source are the same edition. See `VALIDATION.md` for tests
actually run and `provenance/` for exact source scope.

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
downloads until the rights review is complete. Initialize a new Git repository
locally to track further authored edits; never point this directory at the
instrument's existing worktree.
