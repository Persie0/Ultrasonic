# Rev A audit update

Baseline build passed; native DRC/ERC unavailable in KiCad 7.0.11. Corrected the board-symbol instance path and local library names; enlarged PCB to 52 x 29 mm, moving the transmitter terminal 5 mm away from the arm shunt to improve mechanical separation. External supply header pins now model power outputs. Firmware now buffers 20 ms before playback, mutes on queue overflow/underflow, checks stream epochs, bounds queue draining and detects delayed timer callbacks. No increase in drive settings or output power.

The old PCB preview depicts the earlier 47 mm revision and is superseded; do not use it for manufacturing. The custom geometry report is also from the earlier revision; native validation remains mandatory. Physical part fit, native DRC/ERC, transient measurements and calibrated acoustic exposure checks are outstanding.
