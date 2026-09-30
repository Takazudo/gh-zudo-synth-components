# Component decision register — R20

Not an order-ready BOM. New research is separated from inherited selections. Source pages may carry cached availability; no inventory is reserved.

## Two analogue S&H cells

**LF398M/NOPB** — LCSC C1346172; quantity scope: 2.

Status: LCSC identity verified; JLC assembly listing not verified.

First-prototype recommendation: one dedicated S&H IC per channel, with local hold capacitor and protected trigger pulse.

**Qualification:** SOIC-14, not SOIC-8. It tracks while SAMPLE is asserted: provide a short pulse for edge sampling. Acquisition time, offset, hold step and droop require tests with the actual capacitor. No precision-pitch or long-hold guarantee.

[TI product and datasheet](https://www.ti.com/product/LF398-N) · [LCSC exact part](https://www.lcsc.com/product-detail/C1346172.html) · [JLC Global Sourcing process](https://jlcpcb.com/help/article/how-to-use-jlcpcb-global-sourcing-parts-service)

## One-shot for both S&H trigger inputs

**CD74HC221M96** — C133954; quantity scope: 1.

Status: Exact part visible in JLC monostable category; order review pending.

Dual non-retriggerable one-shot: clean rising edge → bounded acquisition pulse. Set unused pins and reset explicitly.

**Qualification:** Use conditioned logic-level inputs, not raw modular voltages. Pulse width must exceed worst-case acquisition/settling; 50–100 us is a test range, not a qualified setting. Triggers during a busy pulse are intentionally not new samples.

[TI product](https://www.ti.com/product/CD74HC221) · [JLC monostable category](https://jlcpcb.com/parts/2nd/Logic/Monostable_Multivibrators_2176)

## Trigger conditioning and optional clip detectors

**LM393DR** — C67470; quantity scope: 1 for two trigger comparators; more for other detectors.

Status: JLC exact catalogue entry verified.

Dual comparator with designed hysteresis and a 5 V pull-up domain for trigger conditioning.

**Qualification:** Comparator output is open collector. Choose divider/clamp/threshold and protect unpowered conditions. This is not direct ±12 V-to-logic wiring.

[JLC exact part](https://jlcpcb.com/partdetail/TexasInstruments-LM393DR/C67470) · [TI datasheet](https://www.ti.com/lit/gpn/lm393)

## S&H hold capacitor starting candidate

**C0805C103J5GACTU** — C2167597; quantity scope: 2.

Status: JLC exact catalogue entry verified.

10 nF, 50 V, C0G, ±5%, 0805. Start with this part in the acquisition/droop test.

**Qualification:** A larger hold capacitor can reduce leakage-related droop but needs longer acquisition. Low absorption and PCB cleanliness matter more than tight nominal capacitance tolerance. Do not use X7R as an unexplained replacement.

[JLC exact part](https://jlcpcb.com/partdetail/KEMET-C0805C103J5GACTU/C2167597) · [LF398 application guidance](https://www.ti.com/lit/gpn/lf398-n)

## Six MULT outputs plus two S&H post-buffers

**OPA4197IPWR** — C2057327; quantity scope: 2 quad packages for these eight buffer slots.

Status: JLC entry verified; retrieved page offered pre-order / no allocated stock.

Precision, wide-supply quad amplifier candidate. Use six channels for two 1-to-3 MULTs and two for S&H output/indicator isolation.

**Qualification:** This count excludes input conditioners and A/B buffers. An output isolation resistor outside feedback can introduce load-dependent pitch error. Stability, protection, calibration and signal headroom need qualification.

[TI specification](https://www.ti.com/product/OPA4197) · [JLC exact part](https://jlcpcb.com/partdetail/TexasInstruments-OPA4197IPWR/C2057327)

## Alternative discrete S&H topology

**TMUX6111PWR** — no verified JLC code; quantity scope: Alternative, not fitted.

Status: Manufacturer identity verified; no JLC code assigned.

Low-leakage analogue-switch alternative if LF398 procurement is unsuitable.

**Qualification:** Needs separate input/output amplifiers and local hold capacitors. Charge injection, source impedance, settling and switch timing must be designed. Not a drop-in replacement for LF398.

[TI product](https://www.ti.com/product/TMUX6111)

## Two-position selectors, including new A/B pair

**2MS1T1B1M2QES-5** — C908280; quantity scope: 19.

Status: Previously user-selected; JLC identity rechecked.

Keep 5 RANGE + 6 SHAPE + 6 STAGE, and add 2 manual A/B controls.

**Qualification:** A/B signal path should isolate its two source inputs with designed buffers/resistors. The exact contact transition must be verified; do not promise clickless switching or assume source-short protection from the word ON–ON.

[JLC exact part](https://jlcpcb.com/partdetail/Dailywell-2MS1T1B1M2QES5/C908280) · [LCSC exact part](https://www.lcsc.com/product-detail/C908280.html)

## Three-position SYNC and envelope MODE

**2MS3T1B1M2QES / Thonk DW2** — no verified JLC code; quantity scope: 11.

Status: Selected design intent; external procurement.

Retain matching T1-lever counterpart. No functional change from R17.

**Qualification:** Factory sourcing/consignment still needs acceptance. Nut, pivot, actual throw, panel engagement and support datum remain unqualified.

[Thonk orderable family](https://www.thonk.co.uk/shop/sub-mini-toggle-switches/) · [Exact drawing](https://www.thonk.co.uk/wp-content/uploads/2017/05/DW2-SPDT-ON-OFF-ON-2MS3T1B1M2QES.pdf)

## Six TRIG + two manual SAMPLE buttons

**B3F-1020** — C722171; quantity scope: 8.

Status: Candidate; JLC exact catalogue entry verified.

Compare this 6×6 mm tactile switch with a guided panel plunger on a near-panel board.

**Qualification:** 5 mm catalogue height is not an approved exposed button height. The drawing uses a 5 mm circle as the finger target; cap/plunger, mounting plane and stroke are still open.

[JLC exact part](https://jlcpcb.com/partdetail/OmronElectronics-B3F1020/C722171)

## All continuous controls

**PTV09A-4020F-B103** — C5848782; quantity scope: 99.

Status: Existing mechanical reference; manufacturer drawing rechecked.

Keep the nominal Ø6 mm capless F-shaft. B103 is the 10 kΩ linear starting value.

**Qualification:** Each circuit still needs its own value/taper decision. Body width, side lugs and 20 mm shaft-length datum are not a 6 mm footprint or a PCB-to-tip measurement. The viewer reserves 12×12 mm, not a qualified courtyard.

[Bourns drawing](https://www.bourns.com/docs/product-datasheets/PTV09.pdf) · [JLC catalogue](https://jlcpcb.com/partdetail/BOURNS-PTV09A_4020FB103/C5848782)

## Five indexed octave controls

**SRBV160803** — C470374; quantity scope: 5.

Status: Existing selected direction; manufacturer specification rechecked.

Six positions; retain actual 16.2×18.5×7.5 mm body envelope. The proposed 17 mm column grid leaves 0.8 mm body gap.

**Qualification:** Actuator/cap and full panel mounting stack remain open. Do not confuse 15 mm actuator L datum with installed PCB-to-panel spacing. The 8 mm visible actuator in this study remains an unselected cap envelope.

[ALPS exact product](https://tech.alpsalpine.com/e/products/detail/SRBV160803/) · [JLC catalogue](https://jlcpcb.com/partdetail/ALPSALPINE-SRBV160803/C470374)

## All patch points

**WQP518MA / Thonkiconn** — C9900052034 (earlier sourcing record); quantity scope: 180.

Status: Carry-forward candidate, not new stock verification.

Use one mechanically qualified jack lot with black IN and red OUT dress nuts.

**Qualification:** 8.3 mm nut envelope is a trial assumption. Exact EARS nut OD/thread, jack shoulder, panel thickness, engagement, pin assignment and plug clearance remain open. JLC record does not prove normal-stock availability.

[Thonk product](https://www.thonk.co.uk/shop/thonkiconn/) · [JLC sourcing record](https://jlcpcb.com/partdetail/8460744-WQPWQP518MA/C9900052034)

## Magnitude and stage indicators

**KT-0603W** — C2290; quantity scope: 104 sites = 92 magnitude + 12 stage.

Status: Carry-forward sample recommendation.

Use low-current visual evaluation with buffered detector/driver; never attach to the hold capacitor or envelope timing node.

**Qualification:** White bin, optical path, lightpipe/diffuser and package-height arrangement remain unqualified. The 1.32 mm drawn aperture is not an exact part. No OSC lamps.

[JLC catalogue](https://jlcpcb.com/partdetail/C2290)

## Clip indicators at four SUM and six OFFSET outputs

**KT-0603R** — C2286; quantity scope: 10.

Status: Carry-forward sample recommendation.

Independent red CLIP detectors; pre-VCA mixer clipping must also be visible.

**Qualification:** Illustrative ±10 V demo threshold is not circuit headroom. Set real thresholds from output swing, load and supply limits.

[JLC catalogue](https://jlcpcb.com/partdetail/C2286)

## General mixers / filters / folders / A/B support

**TL074CDT** — C6963; quantity scope: Circuit-dependent.

Status: Carry-forward analogue candidate.

Low-cost general buffer, summing and shaping amplifier. A/B planning uses two input buffers and an output buffer per cell.

**Qualification:** Do not assign a quantity from empty rectangles. Input range, headroom, grounding and exact analogue circuit remain design work. Precision pitch paths use a separate error budget.

[JLC catalogue](https://jlcpcb.com/partdetail/STMicroelectronics-TL074CDT/C6963) · [ST manufacturer datasheet](https://www.st.com/resource/en/datasheet/tl074.pdf)

## MIX4 gain cells and three filter/VCA blocks

**LM13700M/NOPB** — C1346265; quantity scope: Circuit-dependent.

Status: Carry-forward analogue candidate.

Dual OTA building block; use external input scaling, current control and output buffering.

**Qualification:** One OTA is not a complete synth VCA. Offset, feedthrough, resonance, loading and noise need circuit tests.

[TI manufacturer](https://www.ti.com/product/LM13700) · [JLC catalogue](https://jlcpcb.com/partdetail/TexasInstruments-LM13700MNOPB/C1346265)

## Five analogue oscillator cores

**AS3340D** — no verified JLC code; quantity scope: 5.

Status: Carry-forward external candidate; not requalified in this pass.

Build and calibrate one complete oscillator before replicating five. Separate sine shaping required.

**Qualification:** Exact current manufacturer datasheet, negative-supply arrangement and component lot need qualification. No through-zero FM claim; SOIC-16 version is intended. This is not a completed oscillator circuit.

[Retained manufacturer-authored datasheet mirror](https://www.alldatasheet.com/html-pdf/1159050/ALFA/AS3340/110/1/AS3340.html)

## Four noise outputs, shared source basis

**NOISE2** — no verified JLC code; quantity scope: 1.

Status: Carry-forward external programmed-component candidate.

White/pink outputs plus proposed band-limited analogue shaping for blue/brown; each output buffered.

**Qualification:** Pseudo-random digital source internally. Programmed part required. Four outputs need not be statistically independent. No internal S&H normal connection.

[Creator product](https://electricdruid.net/product/noise2-white-pink-generator/) · [Creator technical notes](https://electricdruid.net/noise2-white-pink-noise-source/)

## Interface / core interconnections

**Exact keyed header + socket / terminated harness set** — no verified JLC code; quantity scope: Derived from circuit boundary, not jack count.

Status: Not selected.

Use supported, factory-populated mating pairs. Keep S&H storage and oscillator timing nodes local.

**Qualification:** No socket-body height is a PCB-to-PCB stack guarantee. Define signals, ground returns, mating retention and each board plane before routing.

[JLC consignment process](https://jlcpcb.com/help/article/how-to-consign-parts-to-jlcpcb) · [Reference mating connector families](https://www.samtec.com/products/ssw)

## Power supply

**Existing zudo-pd Board P + Board B** — no verified JLC code; quantity scope: One qualified assembly.

Status: User project reuse; not a new electrical design.

Retain separate power assembly and model a reserved pocket, not a taller full-width core stack.

**Qualification:** The latest depth study is only a target. Need current populated power model, regulator heat, service access, true return paths and verified 15 V-only configuration for the exact board revision.

[User project](https://github.com/Takazudo/zudo-pd)
