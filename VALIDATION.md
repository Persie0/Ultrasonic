# Final prototype review — 26 November 2026

Tested electrical source: `a9f62638212586e965aaa4c7c801fdfa8a1194b6`. Documentation-only follow-up.

| Board | Unique schematic pins / PCB pad IDs | Mismatches | Native ERC | Native DRC |
|---|---:|---:|---|---|
| Original ESP32 | 28 | 0 | 0 | 0 |
| Passive ESP32 | 15 | 0 | 0 | 0 |
| Integrated ESP32 | 118 | 0 | 0 | 0 |
| Analog DDS | 48 | 0 | 0 | 0 |
| Reference PWM | 54 | 0 | 0 | 0 |
| Total | 263 | 0 | | |

The independent source-level check traversed labeled schematic wires from pin coordinates and compared each reference/pin pair against PCB pad nets. Multiple pads with the same pin number were checked for consistent net assignments. It is not a general KiCad parser, nor a physical continuity test. Native KiCad reports zero unconnected pads and footprint errors in both validation runs.

## Simulation accounting

| Dataset | Cases | Inside modeled limits |
|---|---:|---:|
| Original RC | 243 | 243 |
| Comparison RC | 6480 | 6480 |
| Ten-load RC | 4860 | 4860 |
| Regulator thermal sensitivity | 324 | 292 |
| Rail transient sensitivity | 324 | 250 |

These are 12,231 case evaluations, not 12,231 statistically independent measurements; the original RC sweep overlaps the comparison. All scripts executed in CI. 106 power sensitivity cases exceed assumed limits; no hardware acceptance is claimed. The model cannot determine acoustic output or exposure.

## Hardware release gates (not passed)

1. Integrated regulator: actual board thermal resistance, effective DC-biased capacitance, radio-load rail droop, inrush, connector/ESD and USB power behavior. Verify against manufacturer specs with acoustic loads absent.
2. RF/mechanical: verify the exact ESP32-WROOM-32E land pattern, antenna overhang and enclosure clearance, exposed-pad assembly and USB connector orientation. Simplified local footprints lack a complete mechanical release review. A two-layer board with routed ground is not by itself proof of an adequate RF return path.
3. Physical assembly: inspect polarity/orientation and test actual hardware. Measure the rail and compare electrical behavior on the dummy load; firmware builds do not establish real-time fail-safe behavior.
4. Acoustic performance and safety: the ten DNP positions are not a qualified array. No actual speaker performance, SPL, directivity or exposure certification is provided. Keep all acoustic positions unpopulated and the arm link open outside supervised electrical tests.
5. Original binaries: PDF and Gerber archive verified locally but not in GitHub; source inventory documents checksums. Original Arduino sketch is present.

## CI evidence

- [Run 45840044890](https://github.com/Persie0/Playground/actions/runs/45840044890)
- [Run 45846640684](https://github.com/Persie0/Playground/actions/runs/45846640684)

All Actions used public Playground. Source merge is not a fabrication release.
