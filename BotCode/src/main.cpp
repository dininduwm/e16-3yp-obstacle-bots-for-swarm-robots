#include <Arduino.h>
#include <SoftwareSerial.h> // including the software serial library
#include <ArduinoJson.h>    // json phrasing library

// id of the bot
String myID = "33";

// creating software serial object
SoftwareSerial mySerial(6, 12);

// variables after decoding
double startAngle;
double endAngle;
double travelDis;

// variables to hold temp data
String reciveStr = "";
StaticJsonDocument<250> doc; // json Doc

// function to decode
void parseJson(char c)
{
  if (c == '\n')
  {
    Serial.println(reciveStr);
    // declaring character array
    char char_array[reciveStr.length() + 1];
    // copying the contents of the
    // string to char array
    strcpy(char_array, reciveStr.c_str());

    // Deserialize the JSON document
    DeserializationError error = deserializeJson(doc, char_array);

    // writing data to variables
    startAngle = doc[myID][0];
    endAngle = doc[myID][2];
    travelDis = doc[myID][1];

    // printing data
    Serial.print("Start Angle = ");
    Serial.print(startAngle);
    Serial.print("; End Angle = ");
    Serial.print(endAngle);
    Serial.print("; Travel Dis = ");
    Serial.println(travelDis);

    // Test if parsing succeeds.
    if (error)
    {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.c_str());
    }

    // clearing the recieved Str
    reciveStr = "";
  }
  else
  {
    reciveStr += c; // add the new string to the total string
  }
}

void setup()
{
  // begining the serial commiunication
  mySerial.begin(9600); // Setting the baud rate of HC-12 Module
  Serial.begin(9600);   // Setting the baud rate of Serial Monitor (Arduino)
}

void loop()
{
  /*
  if (Serial.available() > 0)
  {
    mySerial.write(Serial.read());
  }
  if (mySerial.available() > 0)
    Serial.write(mySerial.read());
    */

  if (Serial.available() > 0)
  {
    // parsing the json string
    parseJson(Serial.read());
  }
}