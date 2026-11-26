# Ultrasonic Bluetooth audio — Rev A

A low-voltage **bench prototype** for experimenting with parametric ultrasonic audio. Assumes a directional audible-audio experiment, not a general-purpose ultrasonic generator. No analog adjustment, transformer, high-voltage rail, external Bluetooth decoder or separate microcontroller. Not a production or exposure-certified speaker. One transmitter only: intelligible audible playback and directionality are **not demonstrated**.

## Architecture

Original ESP32-WROOM-32 development board (external, four wires) receives Bluetooth Classic A2DP SBC audio. ESP32 MCPWM produces a 40 kHz carrier digitally; the TC4427A dual non-inverting DIP-8 driver buffers the two outputs from a regulated 5 V supply. A single passive 40 kHz transmitter connects across the differential output. The 100-ohm resistors limit edge current. The two 10k pull-downs keep driver inputs low while the ESP32 boots. J3 is a removable physical arm jumper and is normally open.

The 52 x 29 mm two-layer PCB is hand-solderable. It deliberately uses an external development board to avoid variation in clone board width and pin arrangements. No dedicated USB circuit on the driver PCB. Both devices require a common ground.

## Hardware

- [Editable KiCad schematic](hardware/ultrasonic.kicad_sch)
- [Routed KiCad PCB](hardware/ultrasonic.kicad_pcb)
- [Bill of materials](hardware/bom.csv)
- [Pin/net reference](hardware/netlist.csv)
- [Static geometry check](hardware/static-checks.md)
- [Assembly and validation](hardware/assembly.md)

## Cost estimate (EUR, indicative, not a quote)

| Item | Low-cost estimate |
|---|---:|
| Original ESP32 development board | 3–6 |
| TC4427A EPA | 1–3 |
| Resistors, capacitors, connectors and shunt | 1–2 |
| One documented 40 kHz transmitter | 1–6 |
| Bare PCB, per board in a small batch | 1–3 |
| Total | 7–20 |

Shipping, taxes, power adapter, programming cable and tools excluded. Cheap transmitter prices depend on sourcing; only use a genuine transmitter with a documented continuous drive rating of at least 10 Vpp. Murata MA40S4S is a documented example (20 Vpp continuous limit); inexpensive generic parts cannot be assumed equivalent.

## Firmware

Use ESP-IDF **v5.4.2**, target esp32 (not C3, S3, S2, C6). With ESP-IDF installed and activated:

```sh
cd firmware
idf.py set-target esp32
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor
```

Keep J3 open and the acoustic load disconnected during programming and electrical validation. The Bluetooth device advertises as **Ultrasonic Rev A**. Firmware accepts normal SBC stereo 44.1/48 kHz PCM and uses a fixed speech-band downsampling and modulation path. It attempts to mute when paused, disconnected, underflowing or silent. No app is needed. Pair only in a controlled lab; the simple no-input/no-output pairing does not provide authenticated peer selection.

## Validation status

PCB traces checked by custom geometry/connectivity logic. Baseline ESP-IDF v5.4.2 compilation passed (Playground run 45834141773). KiCad 9.0.9 subsequently reported no ERC/DRC errors or unconnected pads, but library discovery and silkscreen warnings remained. Revised firmware and RC simulation passed. The final pre-move firmware, simulation, native KiCad ERC and DRC all passed in [Playground run 45835738098](https://github.com/Persie0/Playground/actions/runs/45835738098). The source files have been moved without electrical changes and revalidated in [Playground run 45840044890](https://github.com/Persie0/Playground/actions/runs/45840044890): zero ERC/DRC violations, successful firmware build and 243/243 RC cases. See [dummy-load simulation](simulation/README.md). Firmware timing, Bluetooth interoperability and acoustic response have not been measured. Do not order boards or operate with a transducer before reviewing and completing the checklist. No exposure or loudness guarantee; narrow-band ranging transmitters may provide very weak, distorted or no audible demodulated output.

## References

- https://www.microchip.com/en-us/product/tc4427a
- https://ww1.microchip.com/downloads/en/DeviceDoc/20001423J.pdf
- https://www.digikey.at/en/products/detail/murata-electronics/MA40S4S/4358147
- https://docs.espressif.com/projects/esp-idf/en/v5.4.2/esp32/api-reference/bluetooth/esp_a2dp.html
- https://docs.espressif.com/projects/esp-idf/en/release-v5.4/esp32/api-reference/peripherals/mcpwm.html
- https://www.canada.ca/en/health-canada/services/environmental-workplace-health/reports-publications/radiation/guidelines-safe-use-ultrasound-part-industrial-commercial-applications-safety-code-24.html

## Minimum-cost alternative

[Passive-only GPIO interface](minimum-cost/) is a lower-output experimental variant using four resistors and no extra driver IC. [Comparison simulation](simulation/minimum_cost.md) covers 6,480 RC dummy-load cases. Keep the validated TC4427A version as the reference; the passive board is not equivalent in acoustic performance.
