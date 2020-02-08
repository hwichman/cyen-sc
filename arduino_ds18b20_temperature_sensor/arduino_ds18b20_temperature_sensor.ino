#include <OneWire.h>
#include <DallasTemperature.h>

OneWire oneWire(3);
DallasTemperature sensors(&oneWire);

DeviceAddress thermometer = { 0x28, 0x5A, 0x22, 0x5E, 0x1A, 0x19, 0x01, 0x69 };

void setup(void)
{
  // start serial port
  Serial.begin(9600);
  sensors.begin();
  sensors.setResolution(thermometer, 10);
}

void printTemperature(DeviceAddress deviceAddress)
{
  float tempC = sensors.getTempC(deviceAddress);
 if (tempC == -127.00) {
    Serial.print("Error getting temperature");
  } else {
    Serial.print("C: ");
    Serial.print(tempC);
    Serial.print(" F: ");
    Serial.print(DallasTemperature::toFahrenheit(tempC));
  }
}

void loop(void)
{ 
  delay(2000);
  sensors.requestTemperatures();
  Serial.print("temperature: ");
  printTemperature(thermometer);
  Serial.print("\n\r\n\r");
}
