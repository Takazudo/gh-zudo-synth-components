# Exact component candidates and physical fit

## Honest status of R05

The previous panel was not a mechanically locked layout. There were concrete ALPS pot and fader
candidates, but the artwork used unselected 14/9 mm knob caps, an unverified 8.3 mm dress-nut
outline, and an invented fader cap. It represented 20 mm slider travel without the full body or
mounting stack. R06 preserves the layout and makes those distinctions visible.

Listing observations below are retrieved public pages/search records, which may be cached. They
are not live inventory reservations, an accepted assembly quotation, or evidence that every part
can be ordered together. No prices or inventory guarantees are used to approve this design.

## Jack: QingPu WQP-WQP518MA

[JLCPCB C9900052034](https://jlcpcb.com/partdetail/8460744-WQPWQP518MA/C9900052034)

This entry explicitly names Wenzhou QingPu and is a Global Sourcing entry. The retrieved page says
unavailable for purchase and offers consignment. It is a concrete factory-assembly lead, not a
normally stocked approved component. External procurement with prior factory acceptance is
compatible with the project's no-home-soldering requirement.

[Thonk family reference](https://www.thonk.co.uk/shop/thonkiconn/)

The retained drawing is labeled PJ398SM. It supplies a 9 × 10.5 mm nominal front body projection,
a 9 mm body depth and 5.5 mm projecting barrel, excluding leads. Its barrel is drawn Ø6 mm, but
the drawing does not establish thread pitch. The included STEP is a community/family reference,
not manufacturer CAD qualified against an exact incoming WQP518MA lot.

R06 rotates the nominal body 90 degrees in the panel plane, placing its 9 mm direction along the
dense vertical jack pitch. This changes neither the jack centre nor the front-entry direction.
The pad pattern, fixing/support tabs, pin identity and insertion clearance require the full exact
part drawing before PCB placement. Never infer a routable footprint from the front circle.

The earlier generic `C9900079089` record named JLCPCB Assembly rather than QingPu; it is not used
as identity evidence. [LCSC C53058333](https://www.lcsc.com/product-detail/C53058333.html) separately
names QingPu but does not establish JLC assembly acceptance.

The SHOU HAN PJ-313 from early research is not the threaded front-entry jack represented by this
panel. A side-entry socket cannot silently substitute for the selected panel-mount direction.

## EARS dress nuts

[User-selected product](https://ears-modular.com/products/%E9%9B%BB%E7%BE%8E%E3%83%8A%E3%83%83%E3%83%88-3-5-%E3%82%B8%E3%83%A3%E3%83%83%E3%82%AF%E7%94%A8%E3%83%89%E3%83%AC%E3%82%B9%E3%83%8A%E3%83%83%E3%83%88-100%E5%80%8B-1)

The exact product page could not be retrieved in R06. The [supplier collection](https://ears-modular.com/collections/%E3%83%8A%E3%83%83%E3%83%88)
warns that some larger-diameter jacks are incompatible. Neither that warning nor matching color
establishes this jack/nut pairing. R05's 8.3 mm outside diameter remains a drawing placeholder.

Obtain OD, thickness, thread, and seated fit before freezing all 157 jack openings. The HTML trial
nut/plug diameter slider is intentionally labeled an assumption. Black IN / red OUT remain fixed.

## Rotary baseline: ALPS RK09L1140A5L

[JLCPCB C7419101](https://jlcpcb.com/partdetail/ALPSALPINE-RK09L1140A5L/C7419101) ·
[manufacturer product and drawings](https://tech.alpsalpine.com/e/products/detail/RK09L1140A5L/) ·
[manufacturer PDF](https://tech.alpsalpine.com/cms.media/product_catalog_rv_01_rk09l_en_b8437bd47d.pdf)

The exact product is 10 kΩ linear, no detent, vertical operation, with a flat Ø6 mm shaft and
nominal 15 mm shaft length from the drawing's datum. The threaded bushing is M9×0.75. Drawing No.3
shows a 12.1 mm main front width; the body extends 4.85 mm on one side of the shaft centre and
6.5 mm on the other. Those dimensions do not include every terminal/courtyard requirement.

The attached hardware drawing is particularly important: **11 mm-across-flats nut; Ø14 mm washer**.
The washer ID is 9.1 mm and thickness 0.5 mm. The 9 mm small knob drawn on the panel is not the pot
body, nut, or washer. Cap bore, fixing method and depth remain unselected.

### A real MIX5 conflict

If the supplied 14 mm washers are used on the same panel plane at all pot sites, there are ten
nominal overlaps across the two MIX5 strips. Four adjacent input pairs per strip have 13.5 mm
centres and overlap 0.5 mm. Input 5 to LEVEL is 12.5 mm and overlaps 1.5 mm. This mounting scenario
is not approved. The project has not silently deleted the washers or moved the controls.

## Small-control alternative: Bourns PTV09A-4020F-B103

[JLCPCB C5848782](https://jlcpcb.com/partdetail/BOURNS-PTV09A_4020FB103/C5848782) ·
[manufacturer PDF](https://www.bourns.com/docs/product-datasheets/PTV09.pdf)

The retrieved exact listing offers pre-order rather than establishing available stock. Configuration
4 is rear-mount and bushingless, with a nominal 20 mm flat insulated shaft; B103 is 10 kΩ linear.
It avoids a top-side M9 panel nut/14 mm washer. This is a promising alternative for the closely
spaced low-priority controls, but not yet a fitted substitute. Resolve cap/shaft fit, mounting
height, support forces and actual footprint first. R06's default pot-body overlay remains the
explicit ALPS baseline, so the alternative is not portrayed as already verified.

Large and small visible knobs need not imply different resistive elements. A final actuator system
could use one pot family with two cap sizes or a supported shaft-operated small control plus capped
large controls. Do not let an assumed decorative diameter choose the hardware without evidence.

## Faders: ALPS RS20H111C009

[JLCPCB C470622](https://jlcpcb.com/partdetail/ALPSALPINE-RS20H111C009/C470622) ·
[manufacturer product](https://tech.alpsalpine.com/e/products/detail/RS20H111C009/) ·
[manufacturer PDF](https://tech.alpsalpine.com/cms.media/product_catalog_rv_06_rs_h_en_c18c7ded81.pdf)

C470622 was identified in prior research. The exact JLC page could not be retrieved again in R06;
no present stock or order acceptance is asserted. The manufacturer page and dimensional drawing
were retrieved and inspected.

| Feature | Manufacturer drawing / R06 interpretation |
| --- | --- |
| Electrical variant | 50 kΩ linear, no detent; top-operated C lever |
| Travel | 20 mm |
| Body length | 35 mm nominal; general drawing tolerance ±0.1 mm |
| Main side-view body width | 6 mm; nominal top projection including side features is 7.3 mm |
| Body height | 12.5 ±0.3 mm from mounting surface |
| Lever L1 | 14.5 ±0.3 mm from its marked datum |
| Nominal total tip reach | L1+13 = 27.5 mm; total dimension tolerance ±0.5 mm |
| Lever tip | 4 mm along travel × 1.8 mm across travel |
| Support-hole pitch | 32.5 mm along the body |

RISE/FALL centres in every R05/R06 AR strip are 36 mm apart. Two nominal 35 mm bodies leave 1 mm.
Considering body length alone at 35.1 mm each leaves 0.9 mm. Placement error, support tabs, leads,
board/cap tolerance and wiring are not included in that number.

The default front graphic now shows the bare lever. A 4 mm-long lever moving 20 mm sweeps a 24 mm
length before clearance. The illustrated 24.6 × 2.4 mm slot adds a nominal 0.3 mm each side; this
is an unqualified planning cutout, not a manufacturer-recommended machining aperture. The actual
panel height and the manufacturer's lever-wobble limit can require more clearance.

## Electrical and vertical-stack boundaries

These mechanical candidates do not freeze every resistance value in the synth. The ALPS pot and
fader have 10 V DC operating limits; spanning -12 V to +12 V would exceed them. Review actual
control-voltage ranges, wiper loading and the manufacturer's DC-use guidance at schematic design.
The Bourns family has its own limits and does not automatically substitute electrically.

A flat faceplate does not require every underside PCB to share one mounting plane. The pot,
fader and jack have different seating/shaft heights. Separate factory-assembled daughterboards
and preassembled connectors are possible, but their exact mating and fastening geometry must
be designed. No bending of the playing surface is proposed.

Five OCT controls remain indexed switches, with exact switch-body and terminal geometry open.
Other switch/button variants and caps are also not newly qualified by R06.
