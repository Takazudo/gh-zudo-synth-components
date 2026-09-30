# R15 component decisions

All new entries are proposals. The existing panel is not retroactively qualified by listing a real part. No source is a stock reservation.

## 99 continuous controls

**Bourns PTV09A-4020F-B103 / C5848782** — Existing mechanical reference

**Recommendation:** Keep this body/shaft family

Capless nominal 6 mm F-shaft; body does not shrink with the actuator. The B103 orderable is 10 kΩ linear.

Quantity context: 99. Not a purchase quantity or finalized BOM.

Open: Assign value/taper per circuit. 99 controls does not prove 99 × B103 is the final electrical BOM.
Open: 12 × 12 mm body boxes are planning reservations, not qualified footprints.
Open: Bourns shaft is not a separate 6 mm knob-cap SKU.

- [manufacturer datasheet](https://www.bourns.com/docs/product-datasheets/PTV09.pdf)
- [supplier identity](https://www.lcsc.com/product-detail/C5848782.html)
- [assembly catalogue; current fetch unavailable](https://jlcpcb.com/partdetail/BOURNS-PTV09A_4020FB103/C5848782)

## OSC RANGE / AR SHAPE / AR STAGE

**Dailywell 2MS1T1B1M2QES-5 / C908280** — User-selected

**Recommendation:** Keep

Two maintained positions, SPDT ON–ON; T1 actuator family.

Quantity context: 17. Not a purchase quantity or finalized BOM.

Open: Final pad map, nut, washer, lever sweep and panel stack must still be checked.

- [assembly catalogue](https://jlcpcb.com/partdetail/C908280)
- [supplier identity](https://www.lcsc.com/product-detail/C908280.html)

## OSC SYNC / AR MODE

**Dailywell 2MS3T1B1M2QES / Thonk DW2** — Selected design intent; externally procured

**Recommendation:** Keep matching T1 counterpart

SPDT ON–OFF–ON; the centre-open contact is deliberately decoded for the required middle function.

Quantity context: 11. Not a purchase quantity or finalized BOM.

Open: No verified matching JLC number assigned. Arrange authorized sourcing or consignment.

- [supplier orderable](https://www.thonk.co.uk/shop/sub-mini-toggle-switches/)
- [manufacturer drawing hosted by supplier](https://www.thonk.co.uk/wp-content/uploads/2017/05/DW2-SPDT-ON-OFF-ON-2MS3T1B1M2QES.pdf)

## 180 signal jacks

**QingPu WQP518MA / Thonkiconn** — Existing candidate

**Recommendation:** Use one qualified batch for the whole panel

Front-entry threaded 3.5 mm jack is consistent with the existing panel concept. JLC has a QingPu global-sourcing record.

Quantity context: 180. Not a purchase quantity or finalized BOM.

Open: JLC record is not evidence of normal local-stock availability; retained snapshot offered consignment.
Open: Test black/red EARS dress nuts against the actual jack batch. Nut OD, height and thread engagement are not qualified.
Open: Do not use the switch contact to add hidden normals.

- [supplier](https://www.thonk.co.uk/shop/thonkiconn/)
- [global sourcing record](https://jlcpcb.com/partdetail/8460744-WQPWQP518MA/C9900052034)

## Five OCT selectors

**ALPS SRBM160700 / C278332** — New candidate

**Recommendation:** First compact-layout sample to qualify

Six positions, non-shorting, 30° changeover; manufacturer W×D×H is 10.0 × 12.5 × 11.5 mm. 15 mm long, 18-tooth serrated actuator.

Quantity context: 5. Not a purchase quantity or finalized BOM.

Open: Horizontal operating type: for a front-facing axis on a flat panel it needs a perpendicular PCB/daughterboard and mechanical support. Not a drop-in for the current parallel UI PCB assumption.
Open: Formal drawing, pin network/common connections, shaft diameter, knob cap and daughterboard retention remain open. The manufacturer page notes external wiring of common terminals.
Open: This is a candidate, not an approved 14 mm lane fit. The preview OCT remains a placeholder.
Open: Manufacturer minimum contact rating 50 μA at 3 V must be considered for any resistor ladder or sensing scheme.

- [manufacturer specifications](https://tech.alpsalpine.com/e/products/detail/SRBM160700/)
- [assembly catalogue](https://jlcpcb.com/partdetail/ALPSALPINE-SRBM160700/C278332)

## Five OCT selectors, simpler PCB orientation

**ALPS SRBV160803 / C470374** — Alternative; current pitch conflict

**Recommendation:** Only if local OCT spacing can widen

Exact orderable has six positions despite the eight-position series title. Vertical operation; 16.2 × 18.5 × 7.5 mm body; 15 mm flat actuator.

Quantity context: 5. Not a purchase quantity or finalized BOM.

Open: 16.2 mm body width cannot be assumed to fit adjacent 14 mm centres in one coplanar row.
Open: Do not shrink the model to make it fit. No widening was applied in R15.

- [manufacturer specifications](https://tech.alpsalpine.com/e/products/detail/SRBV160803/)
- [assembly catalogue](https://jlcpcb.com/partdetail/ALPSALPINE-SRBV160803/C470374)

## OCT alternative, premium procurement

**Grayhill 56P36-01-1-06N** — External-sourcing alternative

**Recommendation:** Fallback; not the low-cost first choice

Exact supplier record identifies six positions, non-shorting contacts and PC-pin termination; 3.17 mm flatted shaft, not a 6 mm Bourns shaft.

Quantity context: 5. Not a purchase quantity or finalized BOM.

Open: Distributor snapshot was available-to-order rather than stocked, with a 25-piece minimum; do not assume five-piece prototype availability.
Open: Exact package drawing and compatible cap must be qualified before considering 14 mm pitch.
Open: No exact model downloaded or applied.

- [manufacturer family](https://grayhill.com/products/rotational-controls/rotary-switches/56/)
- [exact supplier orderable](https://www.digikey.com/en/products/detail/grayhill-inc/56P36-01-1-06N/4115368)

## Magnitude indicators and optional stage indicators

**KENTO KT-0603W / C2290** — New sample recommendation

**Recommendation:** Low-cost 0603 white reference

JLC catalogue identifies a white top-emitting 0603 LED and SMT assembly. Use current-limited, low-current visual trials.

Quantity context: 94. Not a purchase quantity or finalized BOM.

Open: 82 magnitude sites + 12 stage sites = 94 if all use this emitter; stage amber option is not yet a selected MPN.
Open: White is not automatically warm white. Ignore unverified catalogue CCT anomalies; check exact bin and samples.
Open: LED aperture, diffuser/lightpipe and PCB-to-panel optical path are separate dimensions. A 0603 on a recessed PCB is not automatically visible.
Open: Do not attach directly to an audio or timing node; buffered detector/driver required.

- [assembly catalogue with datasheet link](https://jlcpcb.com/partdetail/C2290)

## Ten clipping indicators

**KENTO KT-0603R / C2286** — New sample recommendation

**Recommendation:** Use red for CLIP

Same 0603 footprint class as the white candidate; separate detector rather than changing the output nut colour.

Quantity context: 10. Not a purchase quantity or finalized BOM.

Open: Four mixer sums and six AO outputs. Monitor mixer pre-VCA clipping as well as output clipping.
Open: Rated/test current is not the recommended panel drive current. Brightness balance and current limit need measurement.

- [assembly catalogue with datasheet link](https://jlcpcb.com/partdetail/C2286)

## Six trigger buttons

**Omron B3F-1020 / C722171** — New candidate

**Recommendation:** Compare this with the XUNPU on a UI coupon

JLC lists a 6 × 6 mm through-hole tactile SPST. Better to qualify a real button/stack now than retain the decorative circle.

Quantity context: 6. Not a purchase quantity or finalized BOM.

Open: Actuator height, finger cap or plunger and panel opening are unresolved. The existing Ø5 mm drawing is not this part’s full geometry.
Open: No unverified B32 cap pairing is assumed.

- [assembly catalogue](https://jlcpcb.com/partdetail/C722171)

## Six trigger buttons, low-cost alternative

**XUNPU TS-1088-AR02016 / C720477** — Alternative

**Recommendation:** Use only with a near-panel UI PCB and qualified plunger

JLC identifies 3.9 × 3 mm plan, 2 mm height, SMT tactile switch.

Quantity context: 6. Not a purchase quantity or finalized BOM.

Open: 2 mm total switch height will be buried if placed on the same low board as tall pots.
Open: Factory fitting of a plunger or a separate UI board is part of the assembly plan.

- [assembly catalogue](https://jlcpcb.com/partdetail/TS-1088-AR02016/C720477)

## Audio SUM, shaping and general buffers

**ST TL074CDT / C6963** — Electronic candidate

**Recommendation:** General-purpose low-cost analogue workhorse

Quad FET-input amplifier, SOIC-14. Use conditioned signal amplitudes on the designed bipolar rails.

Open: Not a precision pitch-mult approval. Budget input offset and output series-resistor/load errors for 1 V/oct fan-out; qualify a precision alternative where needed.
Open: Channel count, supply current and final quantity require a circuit graph.

- [assembly catalogue](https://jlcpcb.com/partdetail/STMicroelectronics-TL074CDT/C6963)
- [manufacturer datasheet link; retrieval not completed this pass](https://www.st.com/resource/en/datasheet/tl074.pdf)

## MIX4 VCAs and VCF/VCA blocks

**TI LM13700M/NOPB / C1346265** — Electronic candidate

**Recommendation:** Use OTA-based stages for the first circuit prototype

Two independent transconductance cells, linearizing diodes and buffers. VCA/filter behavior requires surrounding circuits and appropriate input scaling.

Open: An LM13700 is not two complete plug-and-play synth VCAs.
Open: DC feedthrough, distortion, resonance stability and per-output buffering remain design tasks.

- [manufacturer](https://www.ti.com/product/LM13700)
- [assembly catalogue](https://jlcpcb.com/partdetail/TexasInstruments-LM13700MNOPB/C1346265)

## Five independent oscillator cores

**ALFA AS3340D (SOIC-16)** — External component candidate

**Recommendation:** Prototype one complete oscillator before replicating five

Manufacturer-authored AS3340/3345 document identifies exponential and linear control, sync inputs and triangle/saw/pulse capabilities. Sine requires another shaping stage.

Quantity context: 5. Not a purchase quantity or finalized BOM.

Open: Manufacturer website retrieval failed this pass; exact current datasheet and lot identity need review. No verified JLC code assigned.
Open: Do not connect the negative supply pin directly to −12 V. Use the exact revision’s specified limiting/regulation arrangement.
Open: No through-zero FM promise. Wide LFO range, 1 V/oct tracking, calibration and sine distortion need measured prototype tests.

- [manufacturer-authored datasheet mirror](https://www.alldatasheet.com/html-pdf/1159052/ALFA/AS3340D/111/1/AS3340D.html)
- [external supplier lead](https://www.banzaimusic.com/as3340d.html)

## White/Pink basis for the four-colour noise block

**Electric Druid NOISE2** — External preprogrammed option

**Recommendation:** Recommended first prototype when pseudo-random noise is acceptable

Preprogrammed noise chip supplies separate white and pink outputs. Brown and blue still need band-limited analogue shaping and individual output buffers.

Quantity context: 1. Not a purchase quantity or finalized BOM.

Open: This is digital pseudo-random generation internally, not an all-analogue noise source.
Open: No direct JLC stock record confirmed; supply the programmed chip through approved external sourcing/consignment. A blank PIC is not equivalent.
Open: Avoid assuming all four outputs are statistically independent.
Open: Pink output requires buffering; final levels are not automatically Eurorack signal levels.

- [creator shop](https://electricdruid.net/product/noise2-white-pink-generator/)
- [creator technical article](https://electricdruid.net/noise2-white-pink-noise-source/)

## White/Pink/Blue/Brown alternative

**Analogue junction-noise source + filter network** — Topology candidate; exact source MPN open

**Recommendation:** Choose this only if an all-analogue noise source is a requirement

One qualified broadband source feeds four finite-band shaping/buffer paths. Uses common analogue supporting components but needs source/noise and offset qualification.

Quantity context: 1. Not a purchase quantity or finalized BOM.

Open: No transistor is nominated for reverse base-emitter avalanche merely because it is common; breakdown/noise lifetime and batch behavior need qualification.
Open: This is not yet an orderable complete design, and is not claimed cheaper overall than NOISE2.

- [comparison: creator discusses analogue pink-filter alternative](https://electricdruid.net/noise2-white-pink-noise-source/)
