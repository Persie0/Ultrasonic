# Assembly and release gates

## Wiring and power

J1 pin 1: regulated 5 V, pin 2: common GND, pin 3: ESP32 GPIO25, pin 4: ESP32 GPIO26. Use a current-limited regulated 5 V supply, sized for the development board and PCB. Verify the exact development board's documented 5 V input and power it from the same supply. Do not connect USB and external 5 V to the development board simultaneously unless the board explicitly provides safe power-path isolation. Do not feed 5 V into an ESP32 GPIO or 3.3 V rail. Keep J3 open. J2 is differential; neither terminal is a ground connection. Do not connect an ordinary loudspeaker or a grounded oscilloscope clip to either output.

## Assembly

All parts are through-hole. Check actual footprint sizes and polarity before fabrication. TC4427A: pin 1 is upper-left when viewed from above with notch up; pin 8 upper-right. C2 positive is the pad marked +. Use a standard straight 2-pin header and removable shunt for J3, oriented along the PCB X axis. The PCB has local project footprint and symbol libraries; use the included library tables. Check physical part dimensions and courtyards before fabrication. Use the editable schematic and pin/net CSV to verify layout manually. The board uses a 5.08 mm-pitch two-way terminal for an external single transmitter.

## Before manufacture

1. Open both files in KiCad 8 or later and verify loading and net equivalence against netlist.csv.
2. Run ERC, checking expected power-input warnings for the external supply, and resolve all unexpected issues. Check schematic footprint identifiers, terminal orientation and exact purchased mechanical footprints; resolve any library-update differences.
3. Run DRC, inspect front/back copper, mask, annular ring, edge clearance, courtyard and silkscreen. No independent official DRC has been run.
4. Export and inspect Gerbers plus plated drill data only after signoff. Use standard 1.6 mm FR4, 2 copper layers, 1 oz copper; no controlled impedance.

## Electrical tests (no acoustic load)

With J3 open and the transducer disconnected, check resistance between 5 V and GND before applying power. Use a current-limited source, inspect 5 V and ESP32 rail stability. On a dummy capacitive load within the transmitter's specified capacitance, measure both outputs relative to PCB ground with two oscilloscope channels or a suitable differential probe. Never clip a ground lead to a driver output. Verify low output on boot, pause, disconnect, loss of data and silence; confirm carrier frequency, matched pulse widths, bounded differential voltage and that the output shuts down. Baseline firmware compiled, revised firmware has not been flashed; verify against ESP-IDF v5.4.2 and test timing under Bluetooth load before connecting any acoustic device.

## Acoustic safety / acceptance

Airborne ultrasound can be hazardous even when inaudible. Electrical limits alone do not establish safe acoustic exposure. No exposure-certified output level is established. Keep the jumper open until an appropriate instrumented, isolated test environment is available. Measure audible and ultrasonic bands with suitable calibrated equipment; ordinary phone microphones do not reliably measure 40 kHz. Do not test on people or animals; do not aim the emitter at ears. Do not use as an unattended or public speaker. Do not increase voltage, add emitters, or bypass the fixed bench limits. A small ranging transmitter is narrow-band; audible performance may be poor. Stop if the intended performance cannot be demonstrated safely. See Health Canada Safety Code 24 in README.

## Release status

Prototype only: native EDA checks, firmware build, oscilloscope tests, acoustic measurements, and actual part fit remain outstanding.
