"""Ten-position ideal capacitive dummy-load sweep. No acoustic or resonant model."""
from itertools import product
from math import exp, expm1
import csv
from pathlib import Path

def model(v, c, r, ro, ticks):
    rt = 2*(r+ro)
    tau = rt*c
    x = 0.0
    for k in range(200):
        if k == 199:
            lo, hi, peak, energy = float("inf"), -float("inf"), 0., 0.
        for source, duration in ((v,ticks*1e-7),(0,(125-ticks)*1e-7),(-v,ticks*1e-7),(0,(125-ticks)*1e-7)):
            i = (source-x)/rt
            y = source+(x-source)*exp(-duration/tau)
            if k == 199:
                lo, hi = min(lo,x,y), max(hi,x,y)
                peak = max(peak,abs(i))
                energy += i*i*r*tau/2*(-expm1(-2*duration/tau))
            x = y
    return hi-lo, peak*1000, energy*40000*1000

def main():
    rows=[]
    for n,per,dummy,v,r,ro,t in product(range(1,11),(2.04,2.55,3.06),(0,2.7),(3,3.3,3.6),(950,1000,1050),(0,40,80),(5,20,35)):
        cap=n*per+dummy
        rows.append((n,per,dummy,v,r,ro,t,cap,*model(v,cap*1e-9,r,ro,t)))
    assert len(rows)==4860
    assert all(0<=r[8]<=7.2 and r[9]<4 and r[10]<15 for r in rows)
    with Path(__file__).with_name("ten-load-results.csv").open("w",newline="") as f:
        w=csv.writer(f)
        w.writerow(("count","per_nF","dummy_nF","supply_V","series_ohm","output_ohm","ticks","total_nF","Vpp","peak_mA","each_resistor_mW"))
        w.writerows(rows)
    for n in range(1,11):
        g=[r for r in rows if r[0]==n]
        print(n,len(g),"cases; max Vpp",max(r[8] for r in g),"max mA",max(r[9] for r in g))
    print(len(rows),"ideal RC cases evaluated")
if __name__=="__main__":
    main()
