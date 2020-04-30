/*
    This sketch establishes a TCP connection to a "quote of the day" service.
    It sends a "hello" message, and then prints received data.
*/
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ESP8266WiFi.h>
//#include <eccrypto.h>

#ifndef STASSID
#define STASSID "TiliquaGigas"
#define STAPSK  "Zorb@1983"
#endif
char junk;
String inputString="";
OneWire oneWire(4); //D2 on NodeMCU
DallasTemperature sensors(&oneWire);
byte pressureSensorAnalogPin = A0;

byte flowrateSensorInterrupt = 14; //D3 on NodeMCU
byte flowrateSensorPin = 14; //D1 on NodeMCU
float calibration = 4.5;
volatile byte pulseCount;
float flowrate;
unsigned int flowMilliLitres;
unsigned long totalMilliLitres;
unsigned long oldTime;

DeviceAddress thermometer = { 0x28, 0x5A, 0x22, 0x5E, 0x1A, 0x19, 0x01, 0x69 };

const char* ssid     = STASSID;
const char* password = STAPSK;

const char* host = "192.168.0.2";
const uint16_t port = 23435;

void setup() {
  Serial.begin(115200);

  // We start by connecting to a WiFi network
  pinMode(3, INPUT);
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  /* Explicitly set the ESP8266 to be a WiFi-client, otherwise, it by default,
     would try to act as both a client and an access-point and could cause
     network-issues with your other WiFi-devices on your WiFi-network. */
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  sensors.begin();
  sensors.setResolution(thermometer, 10);
  pulseCount = 0;
  flowrate = 0.0;
  flowMilliLitres = 0;
  totalMilliLitres = 0;
  oldTime = 0;
  
  attachInterrupt(digitalPinToInterrupt(flowrateSensorInterrupt), pulseCounter, FALLING);
}

void loop() {
  Serial.print("connecting to ");
  Serial.print(host);
  Serial.print(':');
  Serial.println(port);

  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    delay(5000);
    return;
  }

  // This will send a string to the server
  Serial.println("sending data to server");
  while (client.connected()) {
    delay(3000);
    sensors.requestTemperatures();
    client.println(getTemperature(thermometer));
    delay(1000);
    client.println(getFlowrate());
    delay(1000);
    client.println(getPressure());
  }

  // wait for data to be available
  unsigned long timeout = millis();
  //while (client.available() == 0) {
    //if (millis() - timeout > 5000) {
      //Serial.println(">>> Client Timeout !");
      //client.stop();
      //delay(60000);
      //return;
    //}
  //}

  // Read all the lines of the reply from server and print them to Serial
  //Serial.println("receiving from remote server");
  // not testing 'client.connected()' since we do not need to send data here
  //while (client.available()) {
    //char ch = static_cast<char>(client.read());
    //Serial.print(ch);
  //}

  // Close the connection
  Serial.println();
  Serial.println("closing connection");
  client.stop();

  delay(300000); // execute once every 5 minutes, don't flood remote service
}

String getTemperature(DeviceAddress deviceAddress)
{
 float tempC = sensors.getTempC(deviceAddress);
 if (tempC == -127.00) {
    Serial.println();
    Serial.print("Error getting temperature");
    return ("T:N/A");
  } else {
    Serial.println();
    Serial.print("C: ");
    Serial.print(tempC);
    Serial.print(" F: ");
    Serial.print(DallasTemperature::toFahrenheit(tempC));
    return ("T:"+String(tempC));
  }
}

ICACHE_RAM_ATTR void pulseCounter(){
  pulseCount++;
}

String getFlowrate(){
  if((millis() - oldTime) > 1000){ 
      detachInterrupt(flowrateSensorInterrupt);
      flowrate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibration;
      oldTime = millis();
      flowMilliLitres = (flowrate / 60) * 1000;  //conversion into mm/sec
      // Add the millilitres passed in this second to the cumulative total
      totalMilliLitres += flowMilliLitres;  
      unsigned int frac; 
      frac = (flowrate - int(flowrate)) * 10;
      //Serial.println();
      String flowrateString = "";
      flowrateString = "F:"+String(int(flowrate))+"."+(frac, DEC);
      attachInterrupt(digitalPinToInterrupt(flowrateSensorInterrupt), pulseCounter, FALLING);
      pulseCount = 0;
      return flowrateString;
  }
}

String getPressure(){
  float voltage = analogRead(pressureSensorAnalogPin);
  Serial.println("voltage:"+String(voltage));
  if (voltage < 30){
    voltage = 30;
  }
  float pressurePSI = map(voltage, 30, 1023, 0, 1200000);
  return String("P:"+String(pressurePSI));
}
