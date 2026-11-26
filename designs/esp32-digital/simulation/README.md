# Electrical dummy-load simulation

Run python3 simulation/rc_sweep.py. 243 parameter combinations were executed with the same piecewise RC equations in JavaScript; CSV recorded. Supply 4.75–5.25 V, capacitance 2.04–3.06 nF, series resistors 95–105 ohm each, assumed driver resistance 0–15 ohm per channel, existing pulse width limits. Bounds: differential 4.691 to 10.499 Vpp; peak current 19.792 to 27.632 mA; each resistor 1.031 to 3.365 mW.

This is an ideal differential RC model, not a manufacturer driver SPICE model and not a piezo motional equivalent circuit. It cannot establish acoustic output, exposure, resonance behavior, supply ringing, or actual failure safety. Use a dummy capacitor for bench tests. Do not increase output limits based on these results.
