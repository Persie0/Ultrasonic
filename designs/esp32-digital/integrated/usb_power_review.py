"""USB supply screening for an isolated, disarmed electronics prototype.

No acoustic load, no regulator SPICE macromodel, no USB compliance claim.
Run: python3 usb_power_review.py
"""
from itertools import product
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parent

def thermal_cases():
    for vin, cable, i, ambient, theta in product(
        (4.75, 5, 5.25), (.1, .3, .6, 1), (.08, .15, .25, .3, .5),
        (25, 40, 60), (70, 110, 150)
    ):
        terminal = vin - i*cable
        # Conservative dissipation at assumed low output rail; no dropout model.
        p = (terminal - 3.234)*i + terminal*.00008
        t = ambient + p*theta
        yield dict(vin=vin, cable=cable, i=i, ambient=ambient, theta=theta,
                   terminal=terminal, p=p, t=t, thermal=t<=110,
                   headroom=terminal>=4.366)

def transient_cases():
    for c, esr, delay, step in product(
        (10,20,30,40,50,60), (.02,.05,.1), (2,5,10,20), (.1,.2,.35)
    ):
        low = 3.234-step*(esr+delay/c)
        yield dict(c=c,esr=esr,delay=delay,step=step,low=low,passes=low>=3.1)

def summarize(rows,caps):
    return {
        "thermal": {
            "total":len(rows),
            "within":sum(r["thermal"] for r in rows),
            "headroom":sum(r["headroom"] for r in rows),
            "combined":sum(r["thermal"] and r["headroom"] for r in rows),
            "worst":max(r["t"] for r in rows)
        },
        "rail": {
            "total":len(caps),
            "within":sum(r["passes"] for r in caps),
            "byCap":[dict(effective_uF=c,within=sum(r["passes"] for r in caps if r["c"]==c),
                          total=sum(r["c"]==c for r in caps),
                          worst=min(r["low"] for r in caps if r["c"]==c))
                     for c in (10,20,30,40,50,60)]
        }
    }

def main():
    rows=list(thermal_cases())
    caps=list(transient_cases())
    assert len(rows)==540 and len(caps)==216
    result=summarize(rows,caps)
    expected=json.loads((ROOT/"usb-power-summary.json").read_text())
    from math import isclose
    def compare(a,b):
        if isinstance(a,dict):
            assert a.keys()==b.keys()
            for k in a: compare(a[k],b[k])
        elif isinstance(a,list):
            assert len(a)==len(b)
            for x,y in zip(a,b): compare(x,y)
        elif isinstance(a,float):
            assert isclose(a,b,rel_tol=1e-9,abs_tol=1e-9), (a,b)
        else: assert a==b,(a,b)
    compare(result,expected)
    for name,data in (("usb-thermal-generated.csv",rows),("usb-transient-generated.csv",caps)):
        with (ROOT/name).open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(data[0])); w.writeheader(); w.writerows(data)
    print(json.dumps(result,indent=2))
    print("756 cases reproduced; passing simulation is NOT hardware approval")

if __name__=="__main__":
    main()
