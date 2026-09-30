#!/usr/bin/env python3
"""Apply the reviewed browser-only fix after the original source hash gate."""
import hashlib
import json
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / 'scripts/browser/browser.js'
original = path.read_bytes()
expected = 'a8f3d627d88c134d9e47c4e35578a42725c6354d48997c529079162236134abb'
if hashlib.sha256(original).hexdigest() != expected:
    raise SystemExit('Unexpected original browser source; do not patch it blindly')
text = original.decode('utf-8')
old_tab = ' if(tab==="model")requestAnimationFrame(()=>showModel(selected));'
new_tab = ''' if(tab==="model"){
  // A missing model must clear the previous preview before returning to the UI.
  if(!selected?.model)showModel(selected);
  else requestAnimationFrame(()=>{if(state.tab==="model")showModel(selected);});
 }'''
old_empty = ' if(!m){\n  $("no-model").textContent='
new_empty = ''' if(!m){
  clearObject();loadedId=null;
  delete $("viewer").dataset.ready;delete $("viewer").dataset.error;
  $("no-model").textContent='''
for before, after in ((old_tab, new_tab), (old_empty, new_empty)):
    if text.count(before) != 1:
        raise SystemExit('Browser patch target is not unique')
    text = text.replace(before, after, 1)
changed = text.encode('utf-8')
after = hashlib.sha256(changed).hexdigest()
if after != '1154d83cb73dd3dbd5d77b63812ab3afef553b564290c0d7cdadaea3a19b52a1':
    raise SystemExit('Unexpected resulting browser bytes')
path.write_bytes(changed)
receipt = {
    'schema_version': 1,
    'original_corpus_source_tree_verified_before_changes': True,
    'changes': [{
        'path': 'scripts/browser/browser.js',
        'before_sha256': expected,
        'after_sha256': after,
        'reason': 'The missing-model state was deferred to requestAnimationFrame, leaving the previous model visible to immediate state checks. Clear geometry/readiness synchronously and guard queued renders when changing tabs.',
        'failed_evidence_run': 'https://github.com/Takazudo/gh-zudo-synth-components/actions/runs/36746481281',
        'scope': 'UI state transition only. No profile, source PDF, original CAD or evidence verdict changed.'
    }],
    'generated_followup': 'Rebuild the standalone browser using the pinned corpus generator.',
    'verification': 'This receipt describes the patch, not its test result. The workflow must run all checks afterward.'
}
(root/'provenance/repository-adjustments.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('Applied reviewed missing-model state fix:', after)
