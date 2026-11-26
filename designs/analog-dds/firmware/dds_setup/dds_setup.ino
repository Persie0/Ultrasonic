// Independent example for a documented 25 MHz AD9833 module.
// Program with acoustic output disconnected. Not GreatScott's code.
#include <SPI.h>
constexpr uint8_t FSYNC=10;
void word(uint16_t value){
  digitalWrite(FSYNC, LOW);
  SPI.transfer16(value);
  digitalWrite(FSYNC, HIGH);
}
void setup(){
  pinMode(FSYNC, OUTPUT); digitalWrite(FSYNC,HIGH);
  SPI.begin();
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE2));
  const uint32_t f=(40000ULL*(1ULL<<28)+12500000ULL)/25000000ULL;
  word(0x2100); // reset, B28
  word(0x4000 | (f & 0x3fff));
  word(0x4000 | ((f >> 14) & 0x3fff));
  word(0xc000); // phase zero
  word(0x2002); // triangle, reset released
  SPI.endTransaction();
}
void loop(){}
