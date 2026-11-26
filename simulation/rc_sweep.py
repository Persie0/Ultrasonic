"""Exact piecewise RC transient model, no acoustic load or resonance."""
from itertools import product
from math import exp
from csv import DictWriter
from pathlib import Path

def simulate(v, c, r, ro, ticks):
    # differential source (+V, 0, -V, 0); total series resistance
    rt = 2*(r+ro)
    tau = rt*c
    t = ticks*1e-7
    intervals = ((v,t),(0,12.5e-6-t),(-v,t),(0,12.5e-6-t))
    x = 0.0
    vmax = imax = energy = 0.0
    for cycle in range(20):
        if cycle == 19:
            vmax = imax = energy = 0.0
        for source, duration in intervals:
            i = (source-x)/rt
            y = source+(x-source)*exp(-duration/tau)
            if cycle == 19:
                vmax = max(vmax, abs(x),abs(y))
                imax = max(imax,abs(i))
                energy += i*i*r*tau/2*(1-exp(-2*duration/tau))
            x = y
    return dict(supply_V=v, capacitance_nF=c*1e9, resistor_ohm=r,
                driver_ohm=ro, pulse_ticks=ticks, differential_Vpp=2*vmax,
                peak_mA=imax*1e3, resistor_mW=energy*40000*1000)

def main():
    rows = [simulate(*p) for p in product((4.75,5,5.25),(2.04e-9,2.55e-9,3.06e-9),
             (95,100,105),(0,7,15),(5,20,35))]
    assert len(rows)==243
    assert all(0 <= a["differential_Vpp"] <= 10.500001 for a in rows)
    assert all(a["peak_mA"] < 28 for a in rows)
    assert all(a["resistor_mW"] < 10 for a in rows)
    path=Path(__file__).with_name("rc-results.csv")
    with path.open("w",newline="") as f:
        w=DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    for key in ("differential_Vpp","peak_mA","resistor_mW"):
        print(key, min(a[key] for a in rows),max(a[key] for a in rows))
    print(len(rows),"corners passed")
if __name__=="__main__": main()
