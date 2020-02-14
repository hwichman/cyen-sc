
#include <OneWire.h>
#include <DallasTemperature.h>
char junk;
String inputString="";
OneWire oneWire(3);
DallasTemperature sensors(&oneWire);

DeviceAddress thermometer = { 0x28, 0x5A, 0x22, 0x5E, 0x1A, 0x19, 0x01, 0x69 };
void setup()                    // run once, when the sketch starts
{
 Serial.begin(9600);            // set the baud rate to 9600, same should be of your Serial Monitor
 pinMode(13, OUTPUT);
 Serial.println("you are connected");
 sensors.begin();
 sensors.setResolution(thermometer, 10);
}
void loop()
{
  sensors.requestTemperatures();
  Serial.println("temperature: ");
  printTemperature(thermometer);
  //Serial.println(String(TempC));
  if(Serial.available()){
   
  while(Serial.available())
    {
      char inChar = (char)Serial.read(); //read the input
      inputString += inChar;        //make a string of the characters coming on serial
    }
    Serial.println(inputString);
    while (Serial.available() > 0)  
    { junk = Serial.read() ; }      // clear the serial buffer
    inputString = "";
  }
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
