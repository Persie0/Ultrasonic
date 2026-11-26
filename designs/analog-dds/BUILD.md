# Build the analog DDS prototype

This guide is for the fixed-bias sibling board, not the original GreatScott controller. For the reference-derived circuit, use [reference-pwm/BUILD_TEST.md](reference-pwm/BUILD_TEST.md). The original sketch requires [SimpleAD9833](https://github.com/TheSpaceEgg/SimpleAD9833); the fixed-bias board's default sketch uses direct SPI instead. A compatible library example is provided under firmware/simplead9833_setup.

## 1. Parts and compatibility

Use [BOM](hardware/bom.csv). Required external modules: 5 V Arduino Nano (ATmega328P), AD9833 breakout with a documented 25 MHz reference clock and 5 V-compatible interface, Bluetooth A2DP receiver with ground-referenced analog line output (not amplified bridge-tied speaker outputs), a regulated 5 V supply. Use a common ground. The board is designed for a low-voltage raw DDS triangle output; verify your exact breakout documentation. No potentiometers are provided. A different DDS output amplitude/offset is incompatible until the design is reviewed.

Tools: KiCad 9, multimeter, soldering iron, two-channel oscilloscope or differential probe, current-limited supply, dummy capacitor ~2.55 nF. Do not connect an acoustic emitter for the initial tests.

## 2. PCB review and assembly

Open the local KiCad project, run ERC and DRC, inspect all footprints against actual components and confirm the routing against the netlist. Do not fabricate until native checks and mechanical review pass. Specify ordinary 2-layer FR4, 1.6 mm, 1 oz copper. Solder resistors first, DIP sockets (optional), ceramic/film capacitors and headers; insert LM393 and TC4427A with their notches aligned to pin 1. Leave arm jumper J4 open. Check all solder joints and resistance between supply and ground. The coupling capacitors are nonpolar. The electrolytic bulk capacitor is polarized.

## 3. Configure the carrier module

Install Arduino IDE and select Arduino Nano with the actual processor/bootloader. Flash [dds_setup.ino](firmware/dds_setup/dds_setup.ino). For a verified 5 V-compatible AD9833 module, connect Nano D13 to SCLK, D11 to SDATA, D10 to FSYNC, ground to ground, and power according to the module datasheet. Do not connect 5 V logic to a module that only accepts 3.3 V. Verify the module waveform with a scope before connecting it to J2. If the waveform is not compatible, do not adjust the board blindly.

## 4. Connect modules

J1 supplies 5 V and GND. J2 accepts raw DDS triangle and GND. J3 accepts one ground-referenced Bluetooth line-out channel and GND. Never join L and R directly or attach bridge-tied speaker outputs. J4 is the removable normally-open arm shunt. J5 is a ground-referenced, AC-coupled output intended initially for a dummy capacitor. The unused LM393 comparator and TC4427A channel are held at defined input levels. Use one regulated supply with the modules' documented power paths; avoid simultaneous USB and external supply on Nano unless isolated. Pair the external Bluetooth receiver using its vendor instructions. No phone app needed. Proceed to [TEST.md](TEST.md).
