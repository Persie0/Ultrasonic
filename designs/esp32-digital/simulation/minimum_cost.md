# Minimum-cost comparison — electrical dummy-load simulation

6,480 cases executed using exact piecewise RC equations: 3,240 per topology, all 31 existing matched pulse widths, and nine representative paired-width mismatch combinations (including the extremes). Supply, capacitance, resistor tolerance and assumed output resistance varied. No drive settings changed.

| Quantity | TC4427A baseline | Passive GPIO |
|---|---:|---:|
| Supply (V) | 4.75–5.25 | 3.0–3.6 |
| Series resistance per leg (ohm) | 95–105 | 950–1050 |
| Assumed output resistance per leg (ohm) | 0–15 | 0–80 |
| Peak modeled differential Vpp | 10.499 | 4.118 |
| Peak modeled current (mA) | 27.632 | 2.077 |
| Peak average resistor dissipation (mW) | 3.365 | 0.779 |
| Nominal case Vpp | 9.744 | 1.894 |

At 3.6 V and minimum 950-ohm series / 9.5k pull-down resistances, conservative pin-current estimates are 4.168 mA for one output-side terminal short to ground and 4.168 mA for an assumed fully charged capacitor reversal through both series resistors. Per-resistor sustained rail-short dissipation estimate 13.642 mW. These calculations assume intact resistors, no external power and source voltage confined to the rails; they do not prove hardware fault safety or justify intentionally creating shorts. Never connect an external voltage source to either GPIO or output.

Run `python3 simulation/minimum_cost_sweep.py` from the digital design folder. CSV contains each case. Results recorded from the equivalent JavaScript calculation; native Python CI is required for independent reproduction.

Limitations: ideal capacitance only; assumed series output resistance not an ESP32 SPICE model; no resonant piezo branch, wiring inductance, thermal transient, real GPIO pad behavior, ESD or acoustic propagation. The lower-voltage higher-resistance board reduces electrical excitation and may not produce useful audible output. No acoustical/exposure certification, and no claim of equivalent performance. Do not increase output or attach arrays based on this analysis.
