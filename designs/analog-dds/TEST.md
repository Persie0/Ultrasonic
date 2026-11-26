# Test the analog DDS prototype

## 1. Design and electrical prerequisites

Run KiCad ERC/DRC and compare the schematic, PCB and pin map. Verify the real part footprints. Keep J4 open and do not connect a transducer. With power off check supply shorts and component polarity. Apply current-limited 5 V. Confirm 5 V at both ICs and absence of unexpected heating or resets.

## 2. Test source modules independently

Use an oscilloscope on the AD9833 module output before connection. Confirm the intended triangle waveform and approximately 40 kHz. The raw signal must remain within the LM393 input common-mode range and cross the fixed bias; an amplified module may not be compatible. Verify Bluetooth module output is ground-referenced line level (not BTL), with no unexpected DC or clipping. Do not use an ordinary speaker amplifier output. Stop if incompatible.

## 3. Verify analog stage with no load

Connect J2 and J3 with common ground. Measure the bias at the LM393 noninverting input with no audio; nominal divider voltage is about 0.31 V at 5 V. Check the comparator output on its pin 1 with a scope, then the driver output on pin 7. Confirm the comparator switches only as intended, no unstable oscillation or unexplained DC, and the output remains within supply rails. This design does not implement automatic mute or authenticated pairing; disconnect the source and remove J4 when not actively testing. Do not use this as an unattended speaker.

## 4. Dummy-load test

Power off, attach a suitable nonpolar dummy capacitor to J5, connect oscilloscope ground only to board ground, then fit J4 and reapply power for a supervised test. Observe output voltage, supply current and component temperature with and without audio. Verify the output coupling capacitor blocks sustained DC. Stop on excessive heating, ringing, unexplained voltage or unexpected output. Compare with the schematic and record the actual waveform; no measured waveform is supplied with this design. Power down and remove J4 after the test.

## 5. Acoustic release gate

Do not run a transmitter around people or animals. Airborne ultrasonic energy can be hazardous even when inaudible. A qualified acoustics/safety specialist and isolated setup with calibrated ultrasound measurement are required before acoustic operation. This low-power circuit is not demonstrated to produce intelligible directional audio. Do not increase voltage, add arrays or extrapolate the dummy-load test to acoustic safety. Consult [Health Canada Safety Code 24](https://www.canada.ca/en/health-canada/services/environmental-workplace-health/reports-publications/radiation/guidelines-safe-use-ultrasound-part-industrial-commercial-applications-safety-code-24.html).

| Test | Result | Evidence | Date |
|---|---|---|---|
| Native ERC/DRC | | | |
| DDS waveform | | | |
| Bluetooth line output | | | |
| Comparator and driver waveform | | | |
| Dummy load / DC blocking | | | |
| Acoustic exposure review | | | |
