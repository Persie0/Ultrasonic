# Static PCB geometry checks

- 28 plated pads, 44 trace segments, 9 named nets.
- All pads of each named net reachable using trace endpoints and plated pads.
- Minimum calculated pad/trace or trace/trace clearance: 0.500 mm, target 0.25 mm.
- Calculation uses circular pad bounds; square pin-1 corners require independent KiCad DRC. No official KiCad ERC/DRC or fabrication outputs were generated. Verify library footprints, courtyard, silkscreen and actual dimensions before manufacture.
