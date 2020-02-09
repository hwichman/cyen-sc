#ifndef TemperatureSensor_h
#define TemperatureSensor_h

#include <OneWire.h>
#include <DallasTemperature.h>
#include "Arduino.h"

class TemperatureSensor {
public:
TemperatureSensor(int pin);
DallasTemperature sensors;
DeviceAddress thermometer;
float getTemperature();

private:
void setup();
float getTemperature(DeviceAddress);

};

#endif
