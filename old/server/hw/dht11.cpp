#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "dht11.h"

const uint8_t HALFWAVES = 85;
const uint8_t MAXZEROLENGTH = 16;


dht11::dht11(GPIO_PIN p, uint8_t e)
: PIN(p),
  MAXERRORS(e)
{
}

void dht11::InitializeCommunication()
{
    pinMode( PIN, OUTPUT );
    digitalWrite( PIN, LOW );
    delay( 18 );
    digitalWrite( PIN, HIGH );
    delayMicroseconds( 40 );
    pinMode( PIN, INPUT );
}

int dht11::ReadValue(uint8_t& humidity, uint8_t& temprature, uint8_t& errors)
{
    for (errors = 0 ; errors < MAXERRORS ; ++errors) {
        InitializeCommunication();

        uint8_t bit = 0;
        uint8_t crc = 0;
        uint8_t laststate = HIGH;
        humidity = temprature = 0;

        for (uint8_t i = 0 ; i < HALFWAVES ; ++i) {
            uint8_t length = 0;
            while (digitalRead(PIN) == laststate && ++length != 255) {
                delayMicroseconds( 1 );
            }
            laststate = digitalRead( PIN );

            // ignore first 2 waves and measure only HIGH part of waves as that means ONE or ZERO
            if ((i >= 4) && (laststate == LOW)) {
                // ignore byte 1 and 3 (byte 0, 2, 4 are humidity, temprature and crc)
                if ((bit & 0x8) == 0) {
                    switch (bit>>4) {
                        case 0:     humidity    = humidity  <<1 | (length > MAXZEROLENGTH);   break;
                        case 1:     temprature  = temprature<<1 | (length > MAXZEROLENGTH);   break;
                        case 2:     crc         = crc       <<1 | (length > MAXZEROLENGTH);   break;
                    }
                }
                ++bit;
                delayMicroseconds( 10 );
            }
        }

        if ((bit >= 40) && (((humidity + temprature) & 0xFF) == crc))
            return 0;
        delay( 500 );
    }
    return 1;
}

