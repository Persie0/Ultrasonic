# Circuit design notes

Board 66.04 × 42.545 mm, two-layer, 18 footprints, 48 plated pads, 143 orthogonal trace segments, no vias. Grid routing uses 0.25 mm nominal clearance; no official KiCad DRC yet. Local project libraries included. Native checks and mechanical review outstanding.

Input: raw DDS triangle on J2; one Bluetooth line channel on J3. R1/R2 nominal bias 0.3125 V; C1/R3 AC couple and attenuate audio into bias. LM393 compares this node with carrier. R4 pulls open collector output high. TC4427A buffers channel A; R5 limits edge current, C5 blocks steady DC, J4 physically disconnects load and R6 provides a DC bleed. J5 is ground-referenced, unlike the digital design's differential output. Spare comparator inputs are fixed, spare driver input grounded. No automatic mute. No acoustic performance validation; only isolated dummy-load tests until qualified acoustic assessment. No original GreatScott attachments retrieved or copied.
