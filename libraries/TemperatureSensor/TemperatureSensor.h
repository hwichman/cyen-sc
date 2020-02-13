#ifndef TemperatureSensor_h
#define TemperatureSensor_h

#include <OneWire.h>
#include <DallasTemperature.h>
#include "Arduino.h"

class TemperatureSensor {
public:
TemperatureSensor(int pin);
float getTemperature();

private:
DallasTemperature sensors;
DeviceAddress thermometer;
void setup();

};

#endif
