# USB / regulator review — 2026-11-27

**Scope:** disarmed electronics, not speaker performance. The PCB and output stage are unchanged. This review adds measurement tooling and replaces generic power assumptions with explicit datasheet-based reference points. No new parts cost.

## Confirmed facts and remaining design gaps

- AP7361C-33E-13 SOT223: 1 input, 2 ground (including tab), 3 output. The PCB's separately numbered tab pad is electrically ground; the existing assignment matches.
- The manufacturer lists typical SOT223 junction-to-ambient thermal resistance of 110 °C/W for its reference PCB. This is not the thermal resistance of our PCB. The 1 A regulator rating alone is not a continuous-current rating for the assembly.
- At 300 mA and 3.3 V output the dropout table gives 140 mV maximum; at 1 A it only gives a typical value, not a maximum. The new headroom check uses the more conservative 1 V separation of the electrical-characteristics test conditions rather than inventing a worst-case dropout curve.
- Espressif recommends a 3.3 V source capable of at least 500 mA. This is a supply-design requirement, not proof of 500 mA continuous load or USB compliance.
- USB 2.0 enumeration, inrush and permitted current are separate requirements. The 4.7 µF VBUS capacitor alone does not establish compliance; charging downstream capacitance and startup of the ESP32 also matter.
- ESD protection, actual ground return, antenna clearance, thermal copper, connector mechanical fit and power sequencing are not qualified. No change is released for fabrication.

## New screening results

| Screen | Cases | Inside screening condition |
|---|---:|---:|
| Thermal (110°C engineering target) | 540 | 426 |
| Regulator headroom (1 V above highest assumed rail) | 540 | 531 |
| Both conditions | 540 | 420 |
| Ideal load transient | 216 | 173 |

The thermal and headroom rows are different checks on the same 540 cases, not additional cases. 216 transient cases bring the total to 756. 110°C is an engineering screening target below the earlier 125°C screen, not a new manufacturer rating. The reference temperature rise model uses the connector voltage after cable drop and includes the regulator's assumed maximum 80 µA no-load quiescent current. Load current, cable resistance, board thermal resistance and ambient are hypotheses, not measurements. The input headroom check is intentionally conservative, not a dropout guarantee.

The transient model uses effective capacitance after DC bias, not nominal label value. It omits control loop stability and inrush. Do not select a larger capacitor solely from this model, since startup current and actual regulator stability still require review. Results and source are reproducible; no acoustic excitation is modeled.

## Power-only diagnostic

Use the separate [power-diagnostic](power-diagnostic/) project before any audio firmware. It contains no radio stack and no waveform generator; both output GPIOs are set low. Its heartbeat records uptime progression and reset reason, not actual rail voltage or temperature. The physical arm must remain open and all transmitter sites unpopulated. See [bring-up guide](POWER_TEST.md). A successful idle test is necessary, but cannot establish worst-case Bluetooth current behavior or production release.

## References

- Diodes AP7361C datasheet DS37274 Rev 5-2, pp. 1–6, 11: https://www.diodes.com/datasheet/download/AP7361C.pdf
- Espressif ESP32 schematic checklist: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/schematic-checklist.html
- USB-IF electrical compliance updates: https://compliance.usb.org/index.asp?UpdateFile=Electrical
- Analog Devices USB charging overview: https://www.analog.com/en/resources/technical-articles/2022/07/16/09/15/usb-battery-charging-overview--maxim-integrated.html

## Evidence handling

Use the [measurement template](power-measurements.csv) for actual results. No physical board records are provided. The heartbeat log cannot sense the arm jumper, rail or junction temperature. Surface temperature is not junction temperature; do not enter it as such. A model prediction, component rating or empty measurement cell is not proof of compliance. Keep idle diagnostic results separate from later qualified power and radio tests.
