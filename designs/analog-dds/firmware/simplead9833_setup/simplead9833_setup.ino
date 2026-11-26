// Reference-compatible initialization; GreatScott project attribution in SOURCE_FILES.md.
// Requires TheSpaceEgg/SimpleAD9833. Keep acoustic hardware disconnected.
#include <SPI.h>
#include <SimpleAD9833.h>
SimpleAD9833 dds(10);
void setup() {
  SPI.begin();
  dds.begin();
  dds.setWaveform(TRIANGLE, 40000);
}
void loop() {}
