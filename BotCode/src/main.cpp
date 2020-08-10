#include <Arduino.h>
#include <SoftwareSerial.h>  // including the software serial library

// creating software serial object
SoftwareSerial mySerial(6, 12);

void setup()
{
  mySerial.begin(9600);   // Setting the baud rate of HC-12 Module
  Serial.begin(9600);    // Setting the baud rate of Serial Monitor (Arduino)
}

void loop()
{
  if (Serial.available() > 0){
    mySerial.write(Serial.read());
  }
  if (mySerial.available() > 0)
    Serial.write(mySerial.read());
}