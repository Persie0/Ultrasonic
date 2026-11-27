# Integrated USB-powered ESP32 bench board

One PCB, no external development board, DDS, audio receiver or programmer. Original ESP32-WROOM-32E-N4 module soldered directly to PCB, AP7361C-33E-13 SOT223 regulator, CH340C USB-UART with built-in clock, USB-B power/data connector, boot/reset switches, current-limited passive output and ten optional on-board 40 kHz load footprints (all DNP). Default assembly is the 2.7 nF electrical dummy load with arm solder bridge open. Ten positions share the same current-limited differential circuit; they are not independent amplifier channels. TP1 is an unpopulated probe location. USB only for power and firmware flashing; Bluetooth Classic A2DP after flashing. No change to existing firmware or drive limits. Actual audible output and acoustic safety not established; do not fit transmitter until qualified testing. No external power amplifier, oscillator, or adjustment needed.

Board 68 × 87 mm, two layers, 31 footprints, 123 pads, 312 segments, 38 vias. Source-derived pad geometries from KiCad ESP32-WROOM-32, SOT-223, SOIC-16, TE USB-B vertical, 0805/1206 and TL3342; local simplified footprints; verify package dimensions, connector variant, exposed-pad stencil, thermal copper, antenna clearance and solder mask against datasheets. The antenna overhangs top edge; keep metal/enclosure away. Native KiCad 9 ERC/DRC passed with zero violations in [run 45846640684](https://github.com/Persie0/Playground/actions/runs/45846640684); 118 unique schematic pin IDs matched PCB nets. RF/USB/thermal/mechanical review remains pending. No fabrication release.

## Power and programming

USB power is a regulated 5 V input. The ESP32 supply design needs burst-current capability; this board is not verified to meet USB enumeration current limits or regulator thermal limits. Do not assume an arbitrary computer port is suitable. A powered data host does not by itself establish USB compliance. AP7361C fixed SOT223 pin 1 input, pin 2 ground, pin 3 output, tab ground; do not substitute the reversed SOT223R pinout. CH340C is powered at 3.3 V (V3 tied to VCC), RX/TX crossed; R232 has an internal pull-down in the documented device. Verify the exact device lot/datasheet. The regulator is nominally rated 1 A, but this PCB is not thermally qualified at 500 mA or 1 A. Hold BOOT, pulse RESET, release BOOT, then flash using esptool/ESP-IDF with manual reset (no automatic DTR/RTS circuit). For programming use a suitable powered USB host; unplug after flashing, use USB supply and pair Bluetooth. Keep JP1 open. Fit C7 dummy only for electrical testing. Never connect external voltage or grounded test clip to either differential terminal.

## References

- https://documentation.espressif.com/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.html
- https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/schematic-checklist.html
- https://www.diodes.com/datasheet/download/AP7361C.pdf
- https://www.wch-ic.com/products/CH340.html
- https://www.murata.com/-/media/webrenewal/products/sensor/ultrasonic/open/datasheet_maopn.ashx

No full-power acoustic mode. The ten positions remain unpopulated by default. See [ten-load model](ten_load_simulation.md). See [build/test](BUILD_TEST.md) and [power model](power_simulation.md).

## Review status

See [overall release gates](../../../VALIDATION.md). A native DRC pass does not establish a verified RF ground plane, USB impedance/ESD compliance, regulator transient response or acoustic operation.

## Power-only diagnostic and revised USB review

Start with [POWER_TEST.md](POWER_TEST.md), not the audio firmware. [POWER_REVIEW.md](POWER_REVIEW.md) documents 756 additional screening cases, verified datasheet conditions and USB limitations. No PCB or output change in this review; no hardware release.

## Local ground-copper candidate

See [layout audit and candidate generation](POWER_COPPER.md). The existing validated PCB is retained; the proposed local ground zones are generated separately and require native fill and DRC. They are not a fabrication release or a measured thermal improvement.
