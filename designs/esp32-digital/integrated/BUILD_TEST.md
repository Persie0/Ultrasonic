# Build and test the integrated USB board

## Before ordering
Open integrated.kicad_pro in KiCad 9. Run ERC and DRC; cross-check all pads, USB connector variant and package mechanical drawings. Inspect ground return, regulator thermal copper, antenna overhang, exposed-pad paste and USB routing. Native checks and physical verification are required before fabrication. No Gerbers are released. Use standard two-layer FR4, 1.6 mm, 1 oz copper.

## Assembly
Use the BOM. Fit the original ESP32-WROOM-32E-N4, fixed AP7361C-33E-13 (not SOT223R), CH340C, USB-B connector, reset/boot switches and passive parts. Fit C7 as the dummy capacitor. Leave TX1 unpopulated and JP1 open. Verify orientation and solder bridges before power. Use a suitable 5 V USB supply or powered data host. No external DevKit, UART programmer, DDS, clock or audio module needed. Check 3.3 V rail and USB enumeration before flashing.

## Firmware
Use ESP-IDF 5.4.2 and the existing firmware folder. With JP1 open, hold BOOT, press/release RESET, release BOOT; use the enumerated CH340 serial port and manual boot mode to flash. Use `idf.py -p PORT flash` or esptool with manual reset, then reset normally. Pair with Ultrasonic Rev A. Keep the transmitter absent.

## Electrical acceptance
Run power_sweep.py and the existing RC sweeps. Measure USB input, 3.3 V rail and current at boot, idle and Bluetooth playback, with calibrated instruments. Confirm no brownouts, rail below-limit excursions, excessive heating or unexpected sustained output. Verify actual regulator junction temperature indirectly using suitable thermal measurement and datasheet guidance; modeled limits are not a release. Power down and bridge JP1 only for an isolated dummy-load measurement. Probe both output nodes relative to ground using two channels and math subtraction; never ground a differential terminal. Confirm pause/disconnect muting and bounded output. Remove the bridge after test. Do not fit an acoustic transmitter until qualified exposure assessment and physical review. No increase in output, array or external amplifier is included.
