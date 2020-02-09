#include "Arduino.h"
#include "TemperatureSensor.h"

TemperatureSensor::TemperatureSensor(int pin){
	this.oneWire = oneWire(pin);
	this.sensors = sensors(&oneWire);
	this.thermometer = { 0x28, 0x5A, 0x22, 0x5E, 0x1A, 0x19, 0x01, 0x69 };
	this.setup();
}

void TemperatureSensor::setup(){
	this.sensors.begin();
	this.sensors.setResolution(thermometer, 10);
}

float TemperatureSensor::getTemperature(DeviceAddress deviceAddress){
	this.sensors.requestTemperatures();
	return this.sensors.getTempC(deviceAddress);
	if (tempC == -127.00) {
		return 0.0;
	} else {
		return this.sensors.getTempC(deviceAddress);
	}
}