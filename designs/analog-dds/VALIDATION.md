# Multi-design validation

Public Playground run [45837291140](https://github.com/Persie0/Playground/actions/runs/45837291140): ESP32 build and 243-case RC simulation passed. KiCad 9.0.9: all three ERC reports passed with zero warnings; digital and reference PWM DRC passed with zero violations; fixed-bias analog DRC reported only two silkscreen clipping warnings and zero unconnected pads. The Arduino direct-SPI example failed due to collision with the Arduino word() macro.

Fixes: removed the conflicting bottom DIP silkscreen edge in the PCB and local footprint library, moved R3 label, renamed the direct SPI helper, included original sketch verified against its Git blob SHA. Rerun required. Physical testing and acoustic safety remain unverified. No change to output voltage or power.

## Final software/EDA validation

Public Playground [45840044890](https://github.com/Persie0/Playground/actions/runs/45840044890), tested source e3e46937227e10eec7d55b05a6c3ea09260d0d4c: all three KiCad projects passed ERC/DRC with zero errors, warnings, unconnected pads and footprint errors. All three Nano sketches compiled (960, 2344 and 3300 bytes respectively). ESP-IDF firmware compiled with 38% app partition free. All 243 digital RC cases passed. This is source integration approval only. Physical assembly, analog waveform behavior, acoustic exposure and manufacturing release remain unverified. Original PDF and Gerber ZIP are not present in this repository; original sketch is included.
