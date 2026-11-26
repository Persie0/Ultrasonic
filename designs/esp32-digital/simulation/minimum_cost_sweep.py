"""Compare existing driver and current-limited GPIO using ideal RC dummy loads.
No motional branch, acoustic model or component-specific output model.
"""
from itertools import product
from math import exp, expm1
from csv import writer
from pathlib import Path
CONFIGS = {
    "baseline": ((4.75,5,5.25),(95,100,105),(0,7,15)),
    "passive": ((3,3.3,3.6),(950,1000,1050),(0,40,80)),
}
CAPS = (2.04e-9,2.55e-9,3.06e-9)
def model(v,c,r,ro,a,b,initial=0.0):
    rt=2*(r+ro)
    tau=rt*c
    x=initial
    for i in range(30):
        if i==29:
            peak,lo,hi,energy=0,float("inf"),-float("inf"),0
        for s,t in ((v,a*1e-7),(0,(125-a)*1e-7),(-v,b*1e-7),(0,(125-b)*1e-7)):
            current=(s-x)/rt
            y=s+(x-s)*exp(-t/tau)
            if i==29:
                peak=max(peak,abs(current))
                lo=min(lo,x,y)
                hi=max(hi,x,y)
                energy+=current*current*r*tau/2*(-expm1(-2*t/tau))
            x=y
    return hi-lo,peak*1000,energy*40000*1000,x

def main():
    rows=[]
    for name,(vs,rs,ros) in CONFIGS.items():
        for v,c,r,ro in product(vs,CAPS,rs,ros):
            for a,b in [(w,w) for w in range(5,36)]:
                rows.append((name,"matched",v,c*1e9,r,ro,a,b,*model(v,c,r,ro,a,b)))
            for a,b in product((5,20,35),repeat=2):
                rows.append((name,"mismatch",v,c*1e9,r,ro,a,b,*model(v,c,r,ro,a,b)))
    assert len(rows)==6480
    for name in CONFIGS:
        group=[r for r in rows if r[0]==name]
        print(name,len(group),"cases")
        for col in (8,9,10):
            print(col,min(r[col] for r in group),max(r[col] for r in group))
        assert all(0<=r[8]<=(7.2 if name=="passive" else 10.5)+1e-8 for r in group)
        assert all(r[9]<(4 if name=="passive" else 30) for r in group)
        assert all(r[10]<10 for r in group)
    # Conservative DC/initial-condition estimates, not measured hardware faults.
    pin_short=3.6/950*1000+3.6/9500*1000
    full_reversal=7.2/1900*1000+3.6/9500*1000
    short_resistor=3.6**2/950*1000
    assert max(pin_short,full_reversal)<5 and short_resistor<15
    print("conservative GPIO current bounds including pull-down (mA)",pin_short,full_reversal)
    print("single resistor rail-short dissipation (mW)",short_resistor)
    with Path(__file__).with_name("minimum-cost-results.csv").open("w",newline="") as f:
        w=writer(f)
        w.writerow(("variant","scenario","supply_V","capacitance_nF","series_ohm","assumed_driver_ohm","a_ticks","b_ticks","Vpp","peak_mA","each_resistor_mW","final_cap_V"))
        w.writerows(rows)
    print(len(rows),"cases passed")
if __name__=="__main__":
    main()
