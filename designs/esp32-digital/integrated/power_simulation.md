# Integrated power sensitivity simulation

648 cases: 324 steady-state thermal and 324 simplified load-transient estimates. Executed with the equations below; Python script included for reproduction. Not a calibrated regulator model.

| Case | Results |
|---|---|
| Steady thermal | 292/324 at or below 125°C assumed design limit |
| Continuous 80–250 mA | All modeled cases within 125°C |
| 500 mA continuous | Some corners fail; NOT rated for continuous 500 mA |
| Worst modeled junction | 181.0°C |
| Nominal 150 mA, 40°C, 90°C/W | 63.0°C |
| Load transient | 250/324 at or above 3.1 V |
| Nominal rail minimum | 3.240 V |
| Worst modeled rail | 2.499 V |

Thermal: P=(Vin−Vout)I, Tj=Ta+PθJA. Vin 4.75–5.25 V, nominal regulator output ±2%, load 80–500 mA, ambient 25–60°C, assumed θJA 60–120°C/W. Thermal resistance depends on actual board copper/enclosure; The regulator's nominal 1 A rating and supply capability are not proof of continuous thermal capability. PCB thermal copper and ground return require review.

Transient: minimum rail≈Vinitial−ΔI(ESR+tresponse/Ceff). Effective 10–30 µF, ESR 0.02–0.1 Ω, step 0.1–0.35 A, assumed regulator response delay 2–20 µs. 3.1 V is the lower stated CH340C 3.3 V supply limit and is used here as a screening threshold, not a validated margin; the actual ESP32 brownout threshold and regulator response are not modeled. Nominal example: 20 µF effective, 0.2 A step, 5 µs, 0.05 Ω. Worst corners fail; measure with a scope under Bluetooth startup/streaming, verify effective MLCC capacitance at DC bias, and revise regulator/copper/capacitance if the rail is not stable. No fabricated board measurements.

Output stage remains the same conservative passive topology; [6,480-case comparison](../simulation/minimum_cost.md) applies to the ideal dummy capacitor and does not establish acoustic performance or exposure safety.

Run `python3 power_sweep.py`. Failing corners are reported deliberately; a successful script means calculations ran, not that hardware meets all corner limits.

## Interpretation

Native CI reproduced the 292/324 and 250/324 counts. **32 thermal + 74 transient corners are outside the assumptions.** 181°C is a mathematical extrapolation; real thermal protection or other failure may intervene. It is not a predicted sustainable junction temperature. 2.499 V is likewise a simplified estimate, not a measured waveform. No actual USB/RF load profile or board-specific thermal resistance is available. Do not change the output stage based on these calculations.
