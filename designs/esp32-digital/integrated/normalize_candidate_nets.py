"""Canonicalize candidate net names against KiCad's exported XML netlist.

No geometry edits. Refuse any real pin/net discrepancy. Explicit singleton
unconnected nets are assigned only where the original PCB had no net.
Never edit the validated baseline in place.
"""
import argparse
import re
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent
NET = re.compile(r'\(net (\d+) "([^"]*)"\)')
REF = re.compile(r'\(fp_text reference "([^"]+)"')
PAD = re.compile(r'^\s*\(pad "([^"]+)"')
STAMP = re.compile(r'\(tstamp [^()]+\)')

def normalize(source, xml):
    nodes = {}
    members = {}
    for net in ET.fromstring(xml).findall("./nets/net"):
        name = net.attrib["name"]
        for node in net.findall("node"):
            key = (node.attrib["ref"], node.attrib["pin"])
            if key in nodes:
                raise ValueError(f"duplicate schematic pin {key}")
            nodes[key] = name
            members.setdefault(name, set()).add(key)
    if not nodes:
        raise ValueError("empty exported netlist")
    old = {name:int(number) for number,name in NET.findall(source) if name}
    aliases = {}
    for name, number in old.items():
        canonical = "/" + name
        if canonical not in members:
            raise ValueError(f"missing root net {canonical}")
        aliases[name] = canonical
    result = []
    visited = set()
    next_code = max(old.values())+1
    nc_codes = {}
    ref = None
    for line in source.splitlines(keepends=True):
        if line.startswith("(footprint "):
            ref = None
        match = REF.search(line)
        if match:
            ref = match.group(1)
        match = PAD.match(line)
        if match:
            key = (ref, match.group(1))
            if key not in nodes:
                raise ValueError(f"PCB pad not in exported schematic {key}")
            visited.add(key)
            expected = nodes[key]
            present = NET.search(line)
            if present:
                number, name = present.groups()
                if aliases.get(name) != expected or old[name] != int(number):
                    raise ValueError(f"real net discrepancy {key}: {name} vs {expected}")
            else:
                if not expected.startswith("unconnected-(") or members[expected] != {key}:
                    raise ValueError(f"PCB unassigned pad has real schematic net {key}: {expected}")
                if expected not in nc_codes:
                    nc_codes[expected] = next_code
                    next_code += 1
                if not STAMP.search(line):
                    raise ValueError(f"missing pad timestamp {key}")
                line = STAMP.sub(lambda m: f'(net {nc_codes[expected]} "{expected}") '+m.group(0),line,count=1)
        line = NET.sub(lambda m: f'(net {m.group(1)} "{aliases.get(m.group(2),m.group(2))}")',line)
        line = re.sub(r'\(net_name "([^"]+)"\)',lambda m:f'(net_name "{aliases.get(m.group(1),m.group(1))}")',line)
        result.append(line)
    if visited != set(nodes):
        raise ValueError(f"missing PCB pins: {set(nodes)-visited}")
    output = "".join(result)
    declarations = "".join(f'(net {code} "{name}")\n' for name,code in nc_codes.items())
    marker = '(net 0 "")\n'
    if output.count(marker)!=1:
        raise ValueError("unexpected net table")
    output = output.replace(marker,marker+declarations,1)
    print(f"Verified {len(visited)} unique pin IDs; normalized {len(aliases)} root nets; assigned {len(nc_codes)} singleton NC nets")
    return output

def main():
    p=argparse.ArgumentParser()
    p.add_argument("candidate",type=Path)
    p.add_argument("netlist",type=Path)
    args=p.parse_args()
    if args.candidate.resolve()==(ROOT/"integrated.kicad_pcb").resolve():
        p.error("refusing to overwrite baseline")
    args.candidate.write_text(normalize(args.candidate.read_text(),args.netlist.read_text()))

if __name__=="__main__":
    main()
