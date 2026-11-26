# Analog DDS prototype (GreatScott-inspired)

Independent low-voltage analog comparator experiment, based on the general architecture discussed in [GreatScott's directional speaker video](https://www.youtube.com/watch?v=B8ss4KqcuXU) and [project post](https://www.patreon.com/GreatScott/posts/directional-119558088). The original schematic PDF, Arduino sketch and transmitter Gerbers were subsequently supplied and inspected. See [source inventory](SOURCE_FILES.md). The fixed-bias board below remains an independent alternative, not the creator's circuit. A separate [reference-derived PWM controller PCB](reference-pwm/) preserves the original analog topology and adjustments.

The supplied schematic uses Arduino Nano, AD9833, MCP602, LM393 and potentiometers, and ends at PWMOUT. The H-bridge power stage is not included in the supplied schematic. This independent version instead uses an external Nano + AD9833 module, external Bluetooth line-out module, fixed passive bias/attenuation, LM393 comparator and TC4427A single-ended 5 V output. The second comparator and driver channels are unused and defined. No trimmers, no high-voltage power stage, no array. An output coupling capacitor blocks steady DC; J4 is a normally-open arm jumper. The fixed bias is only appropriate for a verified raw low-voltage triangle output; not all DDS modules expose the same waveform. Audio compatibility and audible output are not demonstrated.

- [KiCad PCB and schematic](hardware/)
- [Build tutorial](BUILD.md)
- [Test tutorial](TEST.md)
- [BOM](hardware/bom.csv)
- [Nano DDS sketch](firmware/dds_setup/dds_setup.ino)

Experimental single-transmitter/dummy-load design only. Native EDA, physical and acoustic validation are outstanding; do not fabricate or use until the release gates are reviewed.
