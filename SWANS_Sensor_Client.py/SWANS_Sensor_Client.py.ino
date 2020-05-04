/*
    This sketch establishes a TCP connection to a "quote of the day" service.
    It sends a "hello" message, and then prints received data.
*/
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ESP8266WiFi.h>
#include <MD5.h>


#ifndef STASSID
#define STASSID "TiliquaGigas"
#define STAPSK  "Zorb@1983"
#endif

#include <string.h>
#if defined(ESP8266) || defined(ESP32)
#include <pgmspace.h>
#else
#include <avr/pgmspace.h>
#endif

#define MAX_PLAINTEXT_LEN 64

String pad(String str){
  String paddedString = str;
  while (paddedString.length() < 16){
    paddedString += " ";
  }
  return paddedString;
}

String convertToByteString(uint8_t * bytes, int length){
  String hexString = "";
  for (int i = 0; i < length; i++){
    byte save = bytes[i];
    if (bytes[i] < 0x10){
      hexString += "0";
    }
    else if (bytes[i] < 0x20){
      hexString += "1";
      save -= 0x10;
    }
    else if (bytes[i] < 0x30){
      hexString += "2";
      save -= 0x20;
    }
    else if (bytes[i] < 0x40){
      hexString += "3";
      save -= 0x30;
    }
    else if (bytes[i] < 0x50){
      hexString += "4";
      save -= 0x40;
    }
    else if (bytes[i] < 0x60){
      hexString += "5";
      save -= 0x50;
    }
    else if (bytes[i] < 0x70){
      hexString += "6";
      save -= 0x60;
    }
    else if (bytes[i] < 0x80){
      hexString += "7";
      save -= 0x70;
    }
    else if (bytes[i] < 0x90){
      hexString += "8";
      save -= 0x80;
    }
    else if (bytes[i] < 0xA0){
      hexString += "9";
      save -= 0x90;
    }
    else if (bytes[i] < 0xB0){
      hexString += "A";
      save -= 0xA0;
    }
    else if (bytes[i] < 0xC0){
      hexString += "B";
      save -= 0xB0;
    }
    else if (bytes[i] < 0xD0){
      hexString += "C";
      save -= 0xC0;
    }
    else if (bytes[i] < 0xE0){
      hexString += "D";
      save -= 0xD0;
    }
    else if (bytes[i] < 0xF0){
      hexString += "E";
      save -= 0xE0;
    }
    else{
      hexString += "F";
      save -= 0xF0;
    }
    if (save == 0x00){
      hexString += "0";
    }
    else if (save == 0x01){
      hexString += "1";
    }
    else if (save == 0x02){
      hexString += "2";
    }
    else if (save == 0x03){
      hexString += "3";
    }
    else if (save == 0x04){
      hexString += "4";
    }
    else if (save == 0x05){
      hexString += "5";
    }
    else if (save == 0x06){
      hexString += "6";
    }
    else if (save == 0x07){
      hexString += "7";
    }
    else if (save == 0x08){
      hexString += "8";
    }
    else if (save == 0x09){
      hexString += "9";
    }
    else if (save == 0x0A){
      hexString += "A";
    }
    else if (save == 0x0B){
      hexString += "B";
    }
    else if (save == 0x0C){
      hexString += "C";
    }
    else if (save == 0x0D){
      hexString += "D";
    }
    else if (save == 0x0E){
      hexString += "E";
    }
    else{
      hexString += "F";
    }
  }
  return hexString;
}

long gcd(long a, long b) 
{ 
  long r, i;
  while(b!=0){
    r = a % b;
    a = b;
    b = r;
  }
  return a;
} 

long modInverse(long a, long m) 
{ 
    long g = gcd(a,m);
    if (g != 1){
      return -1;
    }
    else {
      long m0 = m; 
      long y = 0, x = 1; 
    
      if (m == 1) 
        return 0; 
    
      while (a > 1) 
      { 
          // q is quotient 
          long q = a / m; 
          long t = m; 
    
          // m is remainder now, process same as 
          // Euclid's algo 
          m = a % m, a = t; 
          t = y; 
    
          // Update y and x 
          y = x - q * y; 
          x = t; 
      } 
    
      // Make x positive 
      if (x < 0) 
         x += m0; 
    
      return x; 
    }
} 

long modDivisionOverAPrimeField(long a, long b, long m){
  while (a < 0){
    a = (a + m)%m;
  }
  while (b < 0){
    b = (b+m)%m;
  }
  a = a%m;
  long inv = modInverse(b,m);
  if (inv == -1){
    return -1;
  }
  else{
    return (inv*a) % m;
  }
}

class Point{
  private:
    long x;
    long y;
  public:
    Point();
    Point(long x, long y);
    long getX();
    long getY();
    void setX();
    void setY();
    Point add(Point point, long a, long field, bool fallback = true);
    Point negate();
    Point addToSelfNTimes(long n, long a, long field);
};
Point::Point(){
  this->x = -1;
  this->y = -1;
}
Point::Point(long x, long y){
  this->x = x;
  this->y = y;
}
long Point::getX(){
  return this->x;
}
long Point::getY(){
  return this->y;
}
Point Point::add(Point point, long a, long field, bool fallback){
  if (this->x == -1){
    return point;
  }
  else if (point.getX() == -1){
    return *this;
  }
  else{
    if (this->x == point.getX() and this->y == -point.getY()){
      return Point(-1,-1);
    }
    else{
      long lamb = 0;
      if (this->x == point.getX() and this->y == point.getY()){
        lamb = modDivisionOverAPrimeField(3*sq(this->x) + a, 2*this->y, field);
      }
      else {
        lamb = modDivisionOverAPrimeField(point.getY() - this->y, point.getX() - this->x, field);
      }
      if (lamb == -1){
        if (fallback){
          return point.add(*this, a, field, false);
        }
        else{
          return Point(-1, -1);
        }
      }
      else {
        long x_three = (sq(lamb) - this->x - point.getX()) % field;
        while (x_three < 0){
          x_three = (x_three + field) % field;
        }
        long y_three = (lamb*(this->x - x_three) - this->y) % field;
        while (y_three < 0){
          y_three = (y_three + field) % field;
        }
        return Point(x_three, y_three);
      }
    }
  }
}

Point Point::negate(){
  if (this->x == -1){
    return Point(-1,-1);
  }
  else{
    return Point(this->x, this->y);
  }
}
Point Point::addToSelfNTimes(long n, long a, long field){
  Point q = *this;
  Point r = Point(-1, -1);
  while (n > 0){
    if (n % 2 == 1){
      r = r.add(q, a, field);
    }
    q = q.add(q, a, field);
    n = (n/2);
  }
  return r;
}
class FiniteEllipticCurve {
  private:
    long a;
    long b;
    long prime;
  public:
    FiniteEllipticCurve(long, long, long);
    FiniteEllipticCurve();
    long getA();
    long getB();
    long getPrime();
    void setA(long a);
    void setB(long b);
    void setPrime(long prime);
    Point getRandomPoint();
};

FiniteEllipticCurve::FiniteEllipticCurve(){
  this->a = -1;
  this->b = -1;
  this->prime = -1;
}

FiniteEllipticCurve::FiniteEllipticCurve(long a, long b, long prime){
  this->a = a;
  this->b = b;
  this->prime = prime;
}
long FiniteEllipticCurve::getA(){
  return this->a;
}
long FiniteEllipticCurve::getB(){
  return this->b;
}
long FiniteEllipticCurve::getPrime(){
  return this->prime;
}
Point FiniteEllipticCurve::getRandomPoint(){
  Point startingPoint = Point(-1, -1);
  for (int x = 0; x < this->prime; x++){
    long y_square = pow(x,3)+this->a*x + this->b;
    for (int y = 0; y < this->prime; y++){
      if (sq(y) % this->prime == y_square % this->prime){
        startingPoint = Point(x, y);
        break;
      }
    }
    if (startingPoint.getX() != -1){
      break;
    }
  }
  Point randomPoint = startingPoint.addToSelfNTimes(random(30,90),this->a, this->prime);
  while (randomPoint.getX() == -1){
    randomPoint = randomPoint.add(startingPoint, this->a, this->prime);
  }
  return randomPoint;
}

class ECC {
  public:
    ECC();
    ECC(FiniteEllipticCurve, Point, Point, long);
    FiniteEllipticCurve ellipticCurve;
    Point P;
    Point Qa;
    long prime;
};
ECC::ECC(){
  ECC(FiniteEllipticCurve(),Point(),Point(), -1);
}
ECC::ECC(FiniteEllipticCurve ec, Point P, Point Qa, long prime){
  this->ellipticCurve = ec;
  this->P = P;
  this->Qa = Qa;
  this->prime = prime;
}

String publicECCDataCode = "[ECC0]";
ECC ecc;
void getData(String line){
  if (line.indexOf('[') >= 0){
    if (line.indexOf(']') >= 0){
      String instruction = line.substring(line.indexOf('['), line.indexOf(']') + 1);
      String data = line.substring(line.indexOf(']') + 1);
      if (data.indexOf('[') >= 0){
        getData(data);
        data = data.substring(0,data.indexOf('['));
      }
      if (instruction == publicECCDataCode){
        String iv = "";
        long prime = -1;
        long a = -1;
        long b = -1;
        long Px = -1;
        long Py = -1;
        long Qax = -1;
        long Qay = -1;
        String toFill = "";
        for (int i = 0; i < data.length(); i++){
          if (data[i] == ',' or i == data.length()-1){
            if (iv == ""){
              iv = toFill;
            }
            else if (prime == -1){
              prime = (toFill).toInt();
            }
            else if (a == -1){
              a = (toFill).toInt();
            }
            else if (b == -1){
              b = (toFill).toInt();
             }
            else if (Px == -1){
              Px = (toFill).toInt();
              
            }
            else if (Py == -1){
              Py = (toFill).toInt();
            }
            else if (Qax == -1){
              Qax = (toFill).toInt();
            }
            else if (Qay == -1){
              toFill+=data[i];
              Qay = (toFill).toInt();
            }
            toFill = "";
          }
          else {
            toFill = toFill + data[i];
          }
          Serial.println("------------Data Received from Server---------------");
          Serial.println("Elliptic curve: y**2 = x**3 + "+String(a)+"x + "+String(b));
          Serial.println("on the prime field = "+String(prime));
          Serial.println("Containing the starting point P = ("+String(Px)+", "+String(Py)+")");
          Serial.println("and a random point Qa = ("+String(Qax)+", "+String(Qay)+")");
          ecc = ECC(FiniteEllipticCurve(a, b, prime),Point(Px,Py),Point(Qax,Qay),prime);
        }        
      }
    }
  }
}

char junk;
String inputString="";
OneWire oneWire(4); //D2 on NodeMCU
DallasTemperature sensors(&oneWire);
byte pressureSensorAnalogPin = A0;
int state = 0;
byte flowrateSensorInterrupt = 14; //D3 on NodeMCU
byte flowrateSensorPin = 14; //D1 on NodeMCU
float calibration = 4.5;
volatile byte pulseCount;
float flowrate;
unsigned int flowMilliLitres;
unsigned long totalMilliLitres;
unsigned long oldTime;
MD5Builder md5;

DeviceAddress thermometer = { 0x28, 0x5A, 0x22, 0x5E, 0x1A, 0x19, 0x01, 0x69 };

const char* ssid     = STASSID;
const char* password = STAPSK;

const char* host = "192.168.0.4";
const uint16_t port = 23435;
Point privateSharedKey;
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
  long k = random(0,99999);
  while (true){
  Serial.println("sending data to server");
  if (client.connected()) {
    if (state == 1){
          Serial.println("Client calculations");
          Serial.println("Shared key = md5 of the x coordinate(casted to String) of a random point on the given curve.");
          privateSharedKey = ecc.ellipticCurve.getRandomPoint();
          Serial.println("The random point is ("+String(privateSharedKey.getX())+", "+String(privateSharedKey.getY())+")");
          md5.begin();
          md5.add(String(privateSharedKey.getX()));
          md5.calculate();
          Serial.println("Shared key = "+ md5.toString());
          Serial.println("Using server info and random k = "+String(k));
          Point C1 = ecc.P.addToSelfNTimes(k, ecc.ellipticCurve.getA(), ecc.prime);
          Serial.println("C1 = ("+String(C1.getX())+", "+String(C1.getY())+")");
          Point C2_0 = ecc.Qa.addToSelfNTimes(k,ecc.ellipticCurve.getA(),ecc.prime);
          Point C2 = privateSharedKey.add(C2_0,ecc.ellipticCurve.getA(),ecc.prime);
          Serial.println("C2 = ("+String(C2.getX())+", "+String(C2.getY())+")");
          Serial.println("Sending C1 and C2 to server...");
          client.println("[C1-2]"+String(C1.getX())+","+String(C1.getY())+","+String(C2.getX())+","+String(C2.getY()));
          
          state++;
    }
    else if (state == 2){
      uint8_t msgBuffer[16];
      uint8_t md5Buffer[16];
      String msg = "Hello Server!  ";
      md5.getBytes(md5Buffer);
      uint8_t enc_message [16];
      delay(3000);
      sensors.requestTemperatures();
      msg = (getTemperature(thermometer));
      msg.getBytes(msgBuffer, 16);
      Serial.println("Encrypting the data using shared key ="+ md5.toString());
      for (int i = 0; i < 16; i++){
            enc_message[i] = md5Buffer[i]^msgBuffer[i];
      }
      client.println(convertToByteString(enc_message, 16));
      delay(1000);
      msg = (getFlowrate());
      msg.getBytes(msgBuffer, 16);
      for (int i = 0; i < 16; i++){
            enc_message[i] = md5Buffer[i]^msgBuffer[i];
      }
      client.println(convertToByteString(enc_message, 16));
      delay(1000);
      msg = (getPressure());
      msg.getBytes(msgBuffer, 16);
      for (int i = 0; i < 16; i++){
            enc_message[i] = md5Buffer[i]^msgBuffer[i];
      }
      client.println(convertToByteString(enc_message, 16));
    }
  }

  // wait for data to be available
  if (client.available()|| client.connected()) {
      String line = client.readStringUntil('\n');
      getData(line);
      if (state == 0 && ecc.P.getX() != -1){
        Serial.println("receiving from remote server");
        state++;
      }
      if (state == 2){
        if(line.indexOf("close") > 0){
          //NOP
        }
      }
    }
  }
}

String getTemperature(DeviceAddress deviceAddress)
{
 float tempC = sensors.getTempC(deviceAddress);
 if (tempC == -127.00) {
    return (pad("[T]N/A"));
  } else {
    return (pad("[T]"+String(tempC)));
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
      flowrateString = "[F]"+String(int(flowrate))+"."+(frac, DEC);
      attachInterrupt(digitalPinToInterrupt(flowrateSensorInterrupt), pulseCounter, FALLING);
      pulseCount = 0;
      return pad(flowrateString);
  }
}

String getPressure(){
  float voltage = analogRead(pressureSensorAnalogPin);
  //Serial.println("voltage:"+String(voltage));
  if (voltage < 30){
    voltage = 30;
  }
  float pressurePSI = map(voltage, 30, 1023, 0, 1200000);
  return pad("[P]"+String(pressurePSI));
}
