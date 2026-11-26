# Integrated USB-powered ESP32 bench board

One PCB, no external development board, DDS, audio receiver or programmer. Original ESP32-WROOM-32E-N4 module soldered directly to PCB, AP7361C-33E-13 SOT223 regulator, CH340C USB-UART with built-in clock, USB-B power/data connector, boot/reset switches, current-limited passive output and optional on-board 40 kHz transmitter footprint (DNP). Default assembly is the 2.7 nF electrical dummy load with arm solder bridge open. USB only for power and firmware flashing; Bluetooth Classic A2DP after flashing. No change to existing firmware or drive limits. Actual audible output and acoustic safety not established; do not fit transmitter until qualified testing. No external power amplifier, oscillator, or adjustment needed.

Board 58 × 57 mm, two layers, 21 footprints, 103 pads, 286 segments, 36 vias. Source-derived pad geometries from KiCad ESP32-WROOM-32, SOT-223, SOIC-16, TE USB-B vertical, 0805/1206 and TL3342; local simplified footprints; verify package dimensions, connector variant, exposed-pad stencil, thermal copper, antenna clearance and solder mask against datasheets. The antenna overhangs top edge; keep metal/enclosure away. Grid routing completed, native KiCad ERC/DRC and RF/USB/thermal/mechanical review pending. No fabrication release.

## Power and programming

Use regulated 5 V USB supply rated at least 0.5 A; do not assume a legacy low-power USB host port can supply radio bursts. AP7361C fixed SOT223 pin 1 input, pin 2 ground, pin 3 output, tab ground; do not substitute the reversed SOT223R pinout. CH340C is powered at 3.3 V (V3 tied to VCC), RX/TX crossed. Hold BOOT, pulse RESET, release BOOT, then flash using esptool/ESP-IDF with manual reset (no automatic DTR/RTS circuit). For programming use a suitable powered USB host; unplug after flashing, use USB supply and pair Bluetooth. Keep JP1 open. Fit C7 dummy only for electrical testing. Never connect external voltage or grounded test clip to either differential terminal.

## References

- https://documentation.espressif.com/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.html
- https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/schematic-checklist.html
- https://www.diodes.com/datasheet/download/AP7361C.pdf
- https://www.wch-ic.com/products/CH340.html
- https://www.murata.com/-/media/webrenewal/products/sensor/ultrasonic/open/datasheet_maopn.ashx

No full-power acoustic mode. See [build/test](BUILD_TEST.md) and [power model](power_simulation.md).
