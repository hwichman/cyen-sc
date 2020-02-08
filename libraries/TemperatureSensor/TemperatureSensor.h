#include <OneWire.h>
#include <DallasTemperature.h>

class TemperatureSensor {
public:
TemperatureSensor();
DeviceAddress thermometer;
DallasTemperature sensors(&OneWire);
OneWire oneWire;

private:
update();

};
