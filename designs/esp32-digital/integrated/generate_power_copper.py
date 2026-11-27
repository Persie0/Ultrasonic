"""Generate a separate local ground-copper candidate, not fabrication output.

The validated PCB is never overwritten. The only proposed geometry additions
are two local GND zones. Native KiCad must fill and validate the candidate.
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "integrated.kicad_pcb"
ZONES = "(zone (net 1) (net_name \"GND\") (layer \"F.Cu\") (tstamp 34d667ac-a1b5-4b52-9000-000000000001)\n  (hatch edge 0.5)\n  (connect_pads yes (clearance 0.25))\n  (min_thickness 0.25)\n  (fill yes (thermal_gap 0.3) (thermal_bridge_width 0.3))\n  (polygon (pts (xy 51 60) (xy 63.5 60) (xy 63.5 75.5) (xy 51 75.5)))\n)\n(zone (net 1) (net_name \"GND\") (layer \"B.Cu\") (tstamp 34d667ac-a1b5-4b52-9000-000000000002)\n  (hatch edge 0.5)\n  (connect_pads yes (clearance 0.25))\n  (min_thickness 0.25)\n  (fill yes (thermal_gap 0.3) (thermal_bridge_width 0.3))\n  (polygon (pts (xy 51 60) (xy 63.5 60) (xy 63.5 75.5) (xy 51 75.5)))\n)"

def candidate(source):
    if not re.search(r'\(net 1 "GND"\)', source):
        raise ValueError("expected GND net 1; review changed PCB")
    if re.search(r'^\s*\(zone\s', source, re.M):
        raise ValueError("existing zones found; review before generating candidate")
    source = source.rstrip()
    if not source.startswith("(kicad_pcb") or not source.endswith(")"):
        raise ValueError("unexpected PCB format")
    output = source[:-1] + "\n" + ZONES + "\n)\n"
    assert output.replace("\n" + ZONES + "\n", "", 1).rstrip() == source
    return output

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.output.resolve() == SOURCE.resolve():
        p.error("refusing to overwrite the validated PCB")
    if args.output.exists():
        p.error("output already exists; choose a new candidate path")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    text = candidate(SOURCE.read_text())
    args.output.write_text(text)
    print("Two local GND zone outlines generated; existing PCB unchanged.")
    print("193.75 mm² outline per layer; actual filled area is not yet known.")
    print("Native fill and DRC required; no manufacturing approval.")

if __name__ == "__main__":
    main()
