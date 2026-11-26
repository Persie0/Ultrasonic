# Test the ESP32 digital prototype

## Stage A — software and design checks

Run `python3 simulation/rc_sweep.py` from this design folder. It checks 243 dummy-load combinations, not acoustic output. Run native KiCad 9 ERC and DRC and verify the schematic against [netlist.csv](hardware/netlist.csv). Confirm no unintended changes to the PCB. Build the ESP-IDF project and retain the log. The earlier public CI run is linked in [audit.md](hardware/audit.md).

## Stage B — power and idle

With J3 open and no transducer, inspect for shorts. Connect a regulated current-limited 5 V source and measure the driver supply and ESP32 rails. Stop on unexpected heating, current, reset or voltage droop. Use a two-channel oscilloscope with both probe ground clips connected only to PCB GND; use math CH1−CH2 for the differential waveform. Never ground a J2 terminal. Check that both driver outputs are low at boot and while disconnected.

## Stage C — playback on a dummy load

Power down. Fit a suitable dummy capacitor in place of the transmitter. Connect the measurement probes and close J3 only for the instrumented electrical check. Pair the phone, play a quiet known test clip, observe the carrier and the differential signal; confirm approximately 40 kHz, bounded voltage, and no unexpected sustained output on pause, silence, disconnect or data loss. The ideal RC model predicts at most about 10.5 Vpp over its defined tolerance sweep, not a guaranteed hardware limit. Record measured supply, waveform, current and temperature. If the observed values differ materially, stop and investigate. Power down and remove J3 after testing.

## Stage D — release gate

No acoustic test around people or animals. A single ranging transmitter may not provide useful audible audio. An isolated, instrumented environment with calibrated airborne-ultrasound measurement and appropriate exposure assessment is required before any acoustic operation. The electrical measurements do not establish safe acoustic exposure. Do not expand the array or increase voltage based on the simulation. Consult a qualified acoustics/safety specialist for an acoustic test protocol.

| Test | Result | Evidence / instrument | Date |
|---|---|---|---|
| ERC/DRC | | | |
| Firmware build | | | |
| Dummy load waveform | | | |
| Idle / pause / disconnect | | | |
| Current and temperature | | | |
| Acoustic exposure review | | | |
