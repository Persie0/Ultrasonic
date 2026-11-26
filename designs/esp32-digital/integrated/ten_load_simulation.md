# Ten-position electrical load model

The integrated board has ten optional unpopulated load positions sharing the existing passive differential output. TP1 is a measurement location. No new amplifier, power rail or change to PWM firmware/current-limiting resistors is included. Default assembly remains a single C7 dummy capacitor and an open arm bridge.

Simulated 4860 cases (486 per count), with 1–10 ideal capacitors, each 2.04–3.06 nF, optional 2.7 nF C7, existing 3.0–3.6 V source and resistor tolerance, assumed GPIO resistance and existing pulse-width limits. Murata MA40S4S datasheet gives 2.55 nF ±20% measured at 1 kHz; this is a **capacitance proxy**, not a 40 kHz impedance or acoustic model. [Datasheet](https://www.murata.com/-/media/webrenewal/products/sensor/ultrasonic/open/datasheet_maopn.ashx).

| Count | Nominal dummy capacitance (nF), excluding C7 | Nominal differential Vpp | Maximum modeled peak current (mA) |
|---:|---:|---:|---:|
| 1 | 2.55 | 1.894 | 2.074 |
| 2 | 5.10 | 0.867 | 2.074 |
| 3 | 7.65 | 0.535 | 2.064 |
| 4 | 10.20 | 0.382 | 2.043 |
| 5 | 12.75 | 0.295 | 2.024 |
| 6 | 15.30 | 0.240 | 2.008 |
| 7 | 17.85 | 0.202 | 1.996 |
| 8 | 20.40 | 0.174 | 1.985 |
| 9 | 22.95 | 0.153 | 1.977 |
| 10 | 25.50 | 0.136 | 1.970 |

Increasing capacitance lowers the voltage in this current-limited circuit. Ten positions do not imply ten times the useful sound, and the circuit is not validated to drive ten acoustic emitters at once. The ideal RC equations completed within the existing modeled electrical bounds. Do not extrapolate to resonance, sound pressure, directivity, exposure, physical GPIO protection or a manufacturing release. No acoustic array power/phase optimization was performed.

Run `python3 ten_load_sweep.py` from this directory. It writes ten-load-results.csv and prints the maxima. The JSON summary records the independent JS calculation; Python CI independently reproduced all 4,860 cases in [run 45846640684](https://github.com/Persie0/Playground/actions/runs/45846640684). Existing regulator thermal/transient blockers remain.
