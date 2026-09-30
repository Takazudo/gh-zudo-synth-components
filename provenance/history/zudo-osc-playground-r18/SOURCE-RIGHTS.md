# Sources and rights

## Project inputs

R17 front-panel layout, artwork and board-domain data were supplied in this conversation. The retained inputs in `source/r17-*` are unchanged; their hashes are recorded in `mechanical/assembly.json`. R18 geometry and viewer code are new development resources for this project.

## Interaction reference

[Takazudo/zudo-case, R8 preview app](https://github.com/Takazudo/zudo-case/blob/main/engineering/r8-preview/app.js), Git blob `0aef9b62cb9bf3fe724038d6bb06dc821f102914`, was read through the GitHub connection. Relevant ideas: orbit inspection, component/layer visibility, lift controls, separate detail views and neutral studio presentation. No case geometry or case app source is bundled in this pack.

## Third-party engine

Three.js r180 and OrbitControls are included as local source modules under the MIT license. Retain `vendor/THREE-LICENSE.txt` when redistributing this viewer. No font files are included. Engine geometry/rendering primitives are not manufacturer CAD.

## Component references

- [ALPS SRBV160803 manufacturer page](https://tech.alpsalpine.com/e/products/detail/SRBV160803/): nominal 16.2 × 18.5 × 7.5 mm case and six-position identity. Installed shaft/bushing datum remains open.
- [Bourns PTV09 manufacturer datasheet](https://www.bourns.com/docs/product-datasheets/PTV09.pdf), page 2 PTV09A-4: nominal 6 mm F shaft and body dimensions. The screenshot/drawing was inspected; the simplified geometry is not an exact imported model or completed installation check.
- Other selected-family jack, toggle and indicator references are inherited from the supplied R17 records and remain qualified exactly as described there.

Manufacturer PDFs and exact manufacturer model files are not newly redistributed by this pack. All case, fastener, nut, connector and optical-path models are described as envelopes where exact dimensions have not been established.
