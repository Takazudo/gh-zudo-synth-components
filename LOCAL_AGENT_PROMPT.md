# Local agent task: Modular Synth Component Corpus

Continue this standalone component corpus; do not continue the instrument routing
work or change its main branch. Read README.md, VALIDATION.md, provenance/scope.json
and the canonical circuit/WORKFLOW.md before editing.

The owner wants reusable modular-synth development knowledge: exact-component
datasheets, practical circuit/mechanical research, and honest 3D previews.
Factory-complete electrical soldering is a priority. External standard parts are
acceptable; JLCPCB stock and acceptance are separate order-time questions.

## Preservation rules

- Keep the 49 imported evidence identities and their original source scope.
  All are not fitted in this corpus, with zero declared placements.
- Keep historical alternatives, including controls and faders dropped from the
  compact instrument. Rejection there is not universal rejection.
- Edit normalized corpus/catalog.json and corpus/guides.json for authored pages.
  Run corpus:generate. Never hand-edit generated native components pages,
  preflight or native preview outputs.
- Original CAD/PDF bytes remain immutable, hash-recorded with preserved source paths.
  Add a new source/version rather than overwriting reviewed bytes.
- Keep exact-part, family, community, envelope and derived-model states distinct.
  A manufacturer drawing-derived body box is not an exact solid CAD model.
- Do not copy upstream fitted/DNP quantities into this library as a build BOM.
- Source rights are per asset; do not apply a blanket MIT label to vendor PDFs.
- No purchase, quote, supplier contact, deployment, PCB fabrication exports or
  physical qualification without a separate owner task.

## Work order

1. Install pinned dependencies; run corpus:check, circuit:check and check.
2. Inspect acquisition-queue.json. Prioritize actual PTL slider datasheet/CAD,
   exact Dailywell suffix evidence, QingPu/EARS mating dimensions, and complete
   Bourns shaft/lug geometry. Resolve identity before inventing a model.
3. Each new exact part gets an authored useful profile first. Promote into native
   evidence only with exact identity and source records; maintain publication
   counts explicitly. A missing model is allowed and must remain visible.
4. Expand the function guides through component comparisons and measured-context
   examples. Avoid presenting untested circuits or typical values as guaranteed.
5. Run models/generate/check/build/check:site and browser-check a profile, a native
   model and a supplementary STEP mesh. Record failed/unavailable steps honestly.
6. Review third-party model/source publication rights before any deployment.

Do not re-run the old instrument CAD/routing recipes merely because they appear
inside inherited raw evidence. Those are historical context, not instructions
for this new corpus.
