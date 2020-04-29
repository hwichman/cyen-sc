
#include <OneWire.h>
#include <DallasTemperature.h>
char junk;
String inputString="";
OneWire oneWire(4);
DallasTemperature sensors(&oneWire);


byte statusLed    = 13;

byte sensorInterrupt = 4;  // 0 = digital pin 2
byte sensorPin       = 4; //D5

// The hall-effect flow sensor outputs approximately 4.5 pulses per second per
// litre/minute of flow.
float calibrationFactor = 4.5;

volatile byte pulseCount;  

float flowRate;
unsigned int flowMilliLitres;
unsigned long totalMilliLitres;

unsigned long oldTime;
// The ID of the thermometer
DeviceAddress thermometer = { 0x28, 0x5A, 0x22, 0x5E, 0x1A, 0x19, 0x01, 0x69 };
void setup()              // run once, when the sketch starts
{
 Serial.begin(9600);     // set the baud rate to 9600, same should be of your Serial Monitor
 pinMode(13, OUTPUT);
 Serial.println("you are connected");
 sensors.begin();
 sensors.setResolution(thermometer, 10);
    
  // Set up the status LED line as an output
  pinMode(statusLed, OUTPUT);
  digitalWrite(statusLed, HIGH);  // We have an active-low LED attached
  
  pinMode(sensorPin, INPUT_PULLUP);
  digitalWrite(sensorPin, HIGH);

  pulseCount        = 0;
  flowRate          = 0.0;
  flowMilliLitres   = 0;
  totalMilliLitres  = 0;
  oldTime           = 0;
  pulseCount        = 0;

  // The Hall-effect sensor is connected to pin 2 which uses interrupt 0.
  // Configured to trigger on a FALLING state change (transition from HIGH
  // state to LOW state)
  attachInterrupt(digitalPinToInterrupt(sensorInterrupt), pulseCounter, FALLING);
}
void loop()
{
  
   if((millis() - oldTime) > 1000)    // Only process counters once per second
  { 
    detachInterrupt(sensorInterrupt);
    flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;
    oldTime = millis();
    flowMilliLitres = (flowRate / 60) * 1000;  //conversion into mm/sec
    // Add the millilitres passed in this second to the cumulative total
    totalMilliLitres += flowMilliLitres;  
    unsigned int frac; 
    frac = (flowRate - int(flowRate)) * 10;
    Serial.println();
    Serial.print(int(flowRate));  // Print the integer part of the variable
    Serial.print(".");
    Serial.print(frac, DEC) ;      // Print the fractional part of the variable
    Serial.print(" L/min");
    sensors.requestTemperatures();
    //Serial.println("temperature: ");
    printTemperature(thermometer);
    //Serial.println(String(TempC));
    pulseCount = 0;
    
    // Enable the interrupt again now that we've finished sending output
    attachInterrupt(digitalPinToInterrupt(sensorInterrupt), pulseCounter, FALLING);
  }
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
    Serial.println();
    Serial.print("C: ");
    Serial.print(tempC);
    Serial.print(" F: ");
    Serial.print(DallasTemperature::toFahrenheit(tempC));
  }
}

ICACHE_RAM_ATTR void pulseCounter()
{
  // Increment the pulse counter
  pulseCount++;
}
