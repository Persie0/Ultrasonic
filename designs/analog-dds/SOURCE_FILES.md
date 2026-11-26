# Original GreatScott source inventory

Author: GreatScott. [Original project post](https://www.patreon.com/GreatScott/posts/directional-119558088). Files supplied by the repository owner in the conversation and inspected locally. The repository owner confirms that GreatScott explicitly permits resharing these attachments. The original Arduino sketch is included byte-for-byte; the original PDF and ZIP are pending binary upload due to a connector limitation. The newly generated KiCad projects are not the original Gerber archive.

| Original filename | Role | SHA-256 |
|---|---|---|
| Schematic_40kHz-PWM-Audio_2024-12-30.pdf | One-page PWM controller schematic, title block dated 2024-12-29 | 8e3e693f47fcf776663158008feaf2aafa122590cf1cd309e17801977a3b9215 |
| AD9833.ino | Arduino sketch, 40 kHz triangle using SimpleAD9833 | 53adc17a4b32e0e816b2b57ea8a18462a5a85b9c2093db4e4d57e70ff9a4e40d |
| Gerber_40kHz-Transmitter_PCB_40kHz-Transmitter_2025-01-08.zip | Separate transmitter PCB fabrication archive | 56d34a3f870ebe9b0822e8a57dab3c99f5f14744ca83191832edfc5feeb802ef |

## Findings

The PDF shows Arduino Nano and AD9833, MCP602, LM393, two 50k potentiometers, 100k and 20k amplifier feedback resistors, 1k comparator pull-up, and 1uF audio coupling. It terminates at PWMOUT. It does not specify a power bridge, complete power supply or acoustic exposure limits. No original editable controller CAD was supplied.

The Arduino sketch includes SimpleAD9833.h, sets chip select to D10, initializes SPI and selects TRIANGLE at 40000. The loop is empty. The required library is [TheSpaceEgg/SimpleAD9833](https://github.com/TheSpaceEgg/SimpleAD9833). The repository includes the original sketch, an equivalent initialization example and an independent direct-SPI alternative; it does not vendor the library.

The original ZIP passed CRC validation and contains ten files: two copper layers, top silkscreen, two solder mask layers, a board outline, separate plated/non-plated/via drill files and an ordering note. These are manufacturing data for the transmitter board, not the PWM controller schematic or a power-stage design. Do not treat the controller PCB and this ZIP as interchangeable. Use a Gerber viewer for inspection; the original archive is pending upload.

## Local originals

The original files belong in [original-files/](original-files/). Compare SHA-256 checksums using sha256sum (Linux), shasum -a 256 (macOS), or Get-FileHash (PowerShell). Keep the creator attribution. No physical test or fabrication approval is implied.

The original sketch's Git blob SHA-1 is `d031e9ae3a76ead566b81d1ea90f4bb4ef8ad365`. The PDF and ZIP SHA-256 values above were rechecked against the supplied local files; all ten ZIP members passed CRC verification. A locally generated Git patch was applied in an empty test repository and reproduced both binary files byte-for-byte. Binary upload remains outstanding; do not mistake the inventory for actual committed attachments.
