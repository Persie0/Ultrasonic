"""Power-budget sensitivity model, not an LDO SPICE simulation.

Assumed thermal resistance and effective capacitor values are explicitly swept.
Failing corners are release blockers, not test failures of the model.
"""
from itertools import product
from pathlib import Path
import csv, json

def main():
    thermal=[]
    for vin,vout,current,ambient,theta in product((4.75,5,5.25),(3.234,3.3,3.366),(.08,.15,.25,.5),(25,40,60),(60,90,120)):
        watts=(vin-vout)*current
        tj=ambient+watts*theta
        thermal.append(dict(vin=vin,vout=vout,current=current,ambient=ambient,theta=theta,watts=watts,tj=tj,passes=tj<=125))
    transient=[]
    for v,c,delta,delay,esr in product((3.234,3.3,3.366),(10,20,30),(.1,.2,.35),(2,5,10,20),(.02,.05,.1)):
        low=v-delta*(esr+delay/c)
        transient.append(dict(v=v,c=c,delta=delta,delay=delay,esr=esr,low=low,passes=low>=3.1))
    assert len(thermal)==324 and len(transient)==324
    assert all(r["passes"] for r in thermal if r["current"]<=.25)
    assert any(not r["passes"] for r in thermal)
    assert any(not r["passes"] for r in transient)
    for name,rows in (("thermal",thermal),("transient",transient)):
        with Path(__file__).with_name(name+"-results.csv").open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        print(name, sum(r["passes"] for r in rows),"/",len(rows),"within assumed limits")
    print("worst junction C",max(r["tj"] for r in thermal))
    print("worst rail V",min(r["low"] for r in transient))
if __name__=="__main__":main()
