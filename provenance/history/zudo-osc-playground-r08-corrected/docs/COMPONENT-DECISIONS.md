# Actuators and component evidence

## A — ALPS RK09L1140A5L + user-selected cap

The exact manufacturer page specifies the 15 mm nominal flat-shaft variant. The user-selected Alibaba URL supplies a **nominal 15 mm cap outside diameter**, a different dimension from shaft length. The listing itself could not be retrieved, so bore shape, bore depth, height, set screw, tolerance and seating remain unverified. A 6 mm bore label alone does not prove fit on the ALPS flat shaft.

A is assigned to the ten OSC TUNE/FINE controls and six VCF FREQ/RES controls. The proposed layout uses 15 mm cap outlines. The former ALPS washer is 14 mm nominal diameter. At the retained 16 mm oscillator-column pitch, neighboring 15 mm caps have just **1 mm nominal edge clearance**. This is not generous finger space and is not a tolerance-qualified fit.

OCT also has a 15 mm cap envelope but remains a separately unselected six-position rotary switch. Never assign the ALPS pot to OCT just to complete a BOM.

Manufacturer: https://tech.alpsalpine.com/e/products/detail/RK09L1140A5L/

User cap: https://www.alibaba.com/product-detail/15mm-Diameter-Black-Full-Aluminum-6_1601503932880.html

## B — Bourns PTV09A-4020F-B103

The F shaft is **6.0 +0/-0.1 mm in diameter and 4.5 mm across its flat**. R08 depicts that shaft capless; it no longer draws an invented 9 mm cap on it. The ordering configuration is bushingless with a nominal 20 mm shaft length. Exact visible shaft height depends on the panel-to-PCB distance.

The small shaft does not shrink the body: the manufacturer front view includes a 10 mm body and an 11.4 mm terminal/body span. The 12 × 12 mm overlay remains an initial reservation, not the complete pad courtyard or a guaranteed collision test. Capless grip, shaft wobble, rotational torque and an actual pointer marking need physical review. The white line on the rotating mockup is a visual cue, not a promised factory marking.

The same mechanical choice is assigned to 73 secondary pots; 10 kOhm is not automatically the correct value for every circuit.

Manufacturer: https://www.bourns.com/docs/product-datasheets/PTV09.pdf

JLC sourcing lead: https://jlcpcb.com/partdetail/BOURNS-PTV09A_4020FB103/C5848782

## AR — illuminated Bourns PTL20 candidate

JLCPCB has an exact public entry for **Bourns PTL20-10G0-103B2 / C17491098**, a 10 kOhm through-hole variant. This is evidence of a catalog identity, not reserved stock or accepted assembly. G denotes the green LED; the warm amber preview is a preferred color alternative that still needs its own exact orderable and sourcing acceptance.

The manufacturer 20 mm family drawing specifies:

| Geometry | Value |
|---|---|
| Travel | 20 ±0.5 mm |
| Body length | 35 ±0.5 mm |
| Body width | 9 ±0.5 mm |
| Body height | 7 ±0.5 mm |
| Lever tip, along travel | 6.0 ±0.1 mm |
| Lever tip, across travel | 2.05 ±0.1 mm |

At 38 mm RISE/FALL centre spacing, two 35.5 mm maximum bodies leave **2.5 mm nominal gap**, before placement tolerance and all solder-pad/tail allowances. The proposed 27.4 × 3.0 mm slot is a study based on maximum travel 20.5 + tip 6.1 + 0.8 clearance along travel, and maximum width 2.15 + 0.85 across. Mounting, wobble, screw access and stack height can require more clearance.

PTL is a different footprint from the former ALPS RS20H111C009. Its old ALPS STEP remains historical only; there is no pretend PTL STEP in this package.

Manufacturer soldering conditions: manual 300 ±5°C for 3 s; wave 260 ±5°C for 5 s; washing not recommended. The factory must accept the actual control, soldering and cleaning sequence. Its LED connections need numerical pin mapping, polarity and current-limiting design before schematic capture.

The user's Alibaba slider URL could not be retrieved; its identity is not asserted. The Bourns part is a researched alternative, not a claim about the unknown listing.

Manufacturer: https://www.bourns.com/docs/product-datasheets/PTL.pdf

JLCPCB: https://jlcpcb.com/partdetail/BOURNS-PTL20_10G0103B2/C17491098

User reference: https://www.alibaba.com/product-detail/IN-STOCK-100-ORIGINAL-BRAND-NEW_1601698938117.html

The PTL PDF was inspected through the web renderer. Direct download of its bytes failed; the URL is retained rather than a fabricated or substituted PDF.

## Indicator package and jack hardware

The jack and EARS nuts retain their earlier unresolved exact-part fit status. Mid-right LED positions remove the original graphic collision with upper-right corner keys, but do not certify clearance below the panel. A 1.2 mm apparent light opening and 0.8 × 1.6 mm component reservation are hypotheses. Select an exact LED, lens/light-pipe, pads and mounting stack before release. The copper bridge is decoration, not a signal trace.

## Factory-only soldering

All LEDs, sliders, pots, connectors, board interconnects and programming interfaces must be factory soldered. External sourcing through an accepted PCBA route is allowed. No vendor request, purchase or production order was sent. zudo-pd is carried forward unchanged and must be re-budgeted after detector/LED currents and analog circuitry are known.
