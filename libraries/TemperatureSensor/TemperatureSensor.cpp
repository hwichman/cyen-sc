#include "Arduino.h"
#include "TemperatureSensor.h"

public TemperatureSensor::TemperatureSensor(int pin){
	this.oneWire = oneWire(pin);
	this.sensors = sensors(&oneWire);
	this.thermometer = { 0x28, 0x5A, 0x22, 0x5E, 0x1A, 0x19, 0x01, 0x69 };
	this.setup();
}

private void TemperatureSensor::setup(){
	this.sensors.begin();
	this.sensors.setResolution(thermometer, 10);
}

public float TemperatureSensor::getTemperature(){
	this.sensors.requestTemperatures();
	//return this.sensors.getTempC(this.thermometer);
	if (tempC == -127.00) {
		return 0.0;
	} else {
		return this.sensors.getTempC(this.thermometer);
	}
}