#ifndef TemperatureSensor_h
#define TemperatureSensor_h
#include "Arduino.h"

class FlowrateSensor{
	public:
		FlowrateSensor(int pin);
		float getFlowRate();
	private:
		byte sensorInterrupt;
		volatile byte pulseCount;
		unsigned int flowMilliLitres;
		unsigned long totalMilliletres;
		unsigned long oldTime;
		float calibrationFactor;
		void setup();
		void pulseCounter();
	
}

#endif