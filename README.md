# Ultrasonic speaker prototypes

Two experimental low-voltage designs, with separate KiCad projects and build/test tutorials. Neither is an exposure-certified or manufacturing-released speaker.

| Design | Description | Guides |
|---|---|---|
| [ESP32 digital](designs/esp32-digital/) | Bluetooth Classic A2DP, digitally generated carrier, TC4427A | [Build](designs/esp32-digital/BUILD.md) · [Test](designs/esp32-digital/TEST.md) |
| [Analog DDS](designs/analog-dds/) | Independent GreatScott-inspired DDS/comparator experiment, analog Bluetooth line input, single-ended low-voltage driver | [Build](designs/analog-dds/BUILD.md) · [Test](designs/analog-dds/TEST.md) |

The original project files were moved without modifying their electrical design. The analog design is not a reproduction of GreatScott's attachments. Keep both prototypes disarmed until appropriate instrumented testing; no acoustic output or safety guarantee.
