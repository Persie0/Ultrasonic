#include <SimpleAD9833.h>

const uint8_t CS_PIN = 10;
SimpleAD9833 myWaveform(CS_PIN);

void setup() {
    Serial.begin(115200);
    SPI.begin();
    myWaveform.begin();
    myWaveform.setWaveform(TRIANGLE, 40000); 
}

void loop() {
   
}