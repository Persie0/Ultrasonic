# Rev A audit update

Baseline build passed; native DRC/ERC unavailable in KiCad 7.0.11. Corrected the board-symbol instance path and local library names; enlarged PCB to 52 x 29 mm, moving the transmitter terminal 5 mm away from the arm shunt to improve mechanical separation. External supply header pins now model power outputs. Firmware now buffers 20 ms before playback, mutes on queue overflow/underflow, checks stream epochs, bounds queue draining and detects delayed timer callbacks. No increase in drive settings or output power.

The PCB preview and custom geometry report have been regenerated from the revised board; native validation remains mandatory. Physical part fit, native DRC/ERC, transient measurements and calibrated acoustic exposure checks are outstanding.

## Native KiCad 9.0.9 review

Playground run 45835103893: firmware and RC simulation passed. Native ERC reported 0 errors and 20 warnings (all library discovery); native DRC reported 0 errors, 0 unconnected pads and 11 warnings (10 library discovery, one C2 polarity silkscreen overlap). Moved polarity mark away from capacitor outline and added the KiCad project file for library discovery. A strict rerun is required; this is still not fabrication approval.
