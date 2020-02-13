#include "FlowrateSensor.h"
#include "Arduino.h"

public FlowrateSensor::FlowrateSensor(int pin){
	pinMode(pin, INPUT);
	digitalWrite(pin, HIGH);
	this.statusLed = 13;
	this.sensorInterrupt = 0;
	this.sensorPin = 2;
	this.calibrationFactor = 4.5;
	this.setup();
}


public float FlowrateSensor::getFlowRate(){
	if((millis() - oldTime) > 1000)    // Only process counters once per second
  { 
    // Disable the interrupt while calculating flow rate and sending the value to
    // the host
    detachInterrupt(sensorInterrupt);
    this.flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;
    this.oldTime = millis();
    this.flowMilliLitres = (flowRate / 60) * 1000;  //conversion into mm/sec
    // Add the millilitres passed in this second to the cumulative total
    this.totalMilliLitres += this.flowMilliLitres;
    unsigned int frac;
    // Print the flow rate for this second in litres / minute
   // Serial.print("Flow rate: ");
    //Serial.print(int(flowRate));  // Print the integer part of the variable
    //Serial.print(".");             // Print the decimal point
    // Determine the fractional part. The 10 multiplier gives us 1 decimal place.
    frac = (this.flowRate - int(this.flowRate)) * 10;
    //Serial.print(frac, DEC) ;      // Print the fractional part of the variable
    //Serial.print("L/min");
    // Print the number of litres flowed in this second
    //Serial.print("  Current Liquid Flowing: ");             // Output separator
    //Serial.print(flowMilliLitres);
    //Serial.print("mL/Sec");

    // Print the cumulative total of litres flowed since starting
    //Serial.print("  Output Liquid Quantity: ");             // Output separator
    //Serial.print(totalMilliLitres);
    //Serial.println("mL"); 

    // Reset the pulse counter so we can start incrementing again
    this.pulseCount = 0;
    
    // Enable the interrupt again now that we've finished sending output
    attachInterrupt(this.sensorInterrupt, this.pulseCounter, FALLING);
  }
  return flowRate;
	
}


private FlowrateSensor::setup(){
	this.pulseCount = 0;
	this.flowRate = 0.0;
	this.flowMilliLitres = 0;
	this.totalMilliLitres = 0;
	this.oldTime = 0;
	attachInterrupt(this.sensorInterrupt, this.pulseCounter, FALLING);
}

private FlowrateSensor::pulseCounter(){
	this.pulseCount++;
}