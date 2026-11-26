# Ultrasonic speaker prototypes

Two experimental low-voltage designs, with separate KiCad projects and build/test tutorials. Neither is an exposure-certified or manufacturing-released speaker.

| Design | Description | Guides |
|---|---|---|
| [ESP32 digital](designs/esp32-digital/) | Bluetooth Classic A2DP, digitally generated carrier, TC4427A | [Build](designs/esp32-digital/BUILD.md) · [Test](designs/esp32-digital/TEST.md) |
| [Analog DDS](designs/analog-dds/) | Independent GreatScott-inspired DDS/comparator experiment, analog Bluetooth line input, single-ended low-voltage driver | [Build](designs/analog-dds/BUILD.md) · [Test](designs/analog-dds/TEST.md) |

The original project files were moved without modifying their electrical design. The analog workspace contains both a fixed-bias low-voltage alternative and a [reference-derived PWM logic controller](designs/analog-dds/reference-pwm/) based on the supplied GreatScott schematic. See the [source inventory](designs/analog-dds/SOURCE_FILES.md). The repository owner confirms the creator permits redistribution. The original sketch is included; the PDF and ZIP are pending binary upload. Keep both prototypes disarmed until appropriate instrumented testing; no acoustic output or safety guarantee.

## Validation

[Public Playground run 45840044890](https://github.com/Persie0/Playground/actions/runs/45840044890): all three KiCad projects passed ERC and DRC with zero violations, all three Arduino sketches compiled, the ESP32 firmware compiled, and all 243 digital dummy-load simulation cases passed. See [validation details](designs/analog-dds/VALIDATION.md). These checks are not a physical or acoustic release.
