# Sources, retained files and reuse

`parts/assets-manifest.json` records the original URLs, SHA-256 hashes and retention provenance
of 21 source files. These bytes were recovered from the earlier user-requested v03 component
pack and inspected for this revision. They are not represented as freshly downloaded source
files or as guaranteed identical to the latest online version. The R06 research record separately
records the current retrieval limitations of each supplier entry.

## ALPS Alpine

The pot/fader directories include the original STEP models, companion drawings, source GIF
figures and manufacturer PDFs. Their original `Read-me-first.rtf` files are retained. The rotary
STEP has a family geometry filename, as delivered from the exact-product research; the exact
resistive variant is identified separately. Manufacturer dimensions and approval limitations
remain authoritative. Do not relabel supplier CAD as an original project design.

## QingPu / PJ398SM reference

`PJ398SM-family.step` is a community model from Barwise's AudioJacks library, not exact-lot
manufacturer CAD. `AudioJacks-LICENSE` retains the MIT notice; `AudioJacks-DATA.md` retains the
creator's metadata, including its untested status. The associated Thonk drawing is labeled
PJ398SM and is used as related-family mechanical evidence. Neither proves the EARS nut fit.
The metadata file mentions other library items; those unrelated assets are not included here.

## Bourns

The PTV09 manufacturer family PDF is retained. There is no new exact-part Bourns STEP in this
pack. The bushingless candidate remains separate from the ALPS overlay.

## Project files

Panel SVGs, scripts and record prose created for this revision may be edited for this project.
That does not change rights in manufacturer/creator documents. Before publishing retained vendor
binaries on a public documentation site, review their terms or link to the original source
instead. No blanket redistribution licence for vendor assets is asserted.

No font binaries are included. Rendering uses locally installed fonts or Pillow's fallback.
