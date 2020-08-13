#include <Arduino.h>
#include <SoftwareSerial.h> // including the software serial library
#include <ArduinoJson.h>    // json phrasing library
#include <PID_v1.h>
#include <Wire.h>

#define EN_R 9  // right motor enable 
#define EN_L 10 // left motor enable

#define ML_A1 5 // left motor in 1
#define ML_A2 4 // left motor in 2

#define MR_A1 3 // right motor in 1
#define MR_A2 2 // right motor in 2
  
void calculate_IMU_error();
void updateGyro();
void MR(int val);
void ML(int val);
double radToDegree(double rads);

const int MPU = 0x68; // MPU6050 I2C address
float GyroX, GyroY, GyroZ;
float angle;
float GyroErrorX;
float elapsedTime, currentTime, previousTime;
int c = 0;

// id of the bot
String myID = "1";

// creating software serial object
SoftwareSerial mySerial(6, 12);

// variables after decoding
double startAngle;
double endAngle;
double travelDis;
double Setpoint, Input, Output;
double mov_Setpoint, mov_Input, mov_Output;

// variables to hold temp data
String reciveStr = "";
StaticJsonDocument<250> doc; // json Doc
PID myPID(&Input, &Output, &Setpoint, 7, 0, 0.35, DIRECT);
PID moving(&Input, &Output, &Setpoint, 2, 0, 0.3, DIRECT);


void setup()
{
  pinMode(EN_R, OUTPUT);
  pinMode(EN_L, OUTPUT);
  pinMode(MR_A1, OUTPUT);
  pinMode(MR_A2, OUTPUT);
  pinMode(ML_A1, OUTPUT);
  pinMode(ML_A2, OUTPUT);

  // begining the serial commiunication
  mySerial.begin(9600); // Setting the baud rate of HC-12 Module
  Serial.begin(9600);   // Setting the baud rate of Serial Monitor (Arduino)

  myPID.SetOutputLimits(-255, 255);
  myPID.SetSampleTime(20);
  myPID.SetMode(AUTOMATIC);
  Setpoint = 0;

  moving.SetOutputLimits(-255, 255);
  moving.SetSampleTime(20);
  moving.SetMode(AUTOMATIC);
  Setpoint = 0;

  calculate_IMU_error();
  delay(20);
}


bool flag = false;
double prvstartAngle = 0;
void loop()
{
  
   if (mySerial.available() > 0)
  {
    // parsing the json string
    parseJson(mySerial.read());
  }

  if(prvstartAngle != startAngle){
    Setpoint -= 1*radToDegree(startAngle);
  }
  prvstartAngle = startAngle;
  
  updateGyro();
  Input = (double)angle;
  myPID.Compute();

  ML(Output);
  MR(-Output);
  
}

void ML(int val)
{ // motor function left(val == speed value)

  if (val > 0)// if the motor speed is positive
  {
    digitalWrite(ML_A2, HIGH); // set the motor control signals
    digitalWrite(ML_A1, LOW);
    analogWrite(EN_L, val);    // give pwm signal to motor enable 
  }
  else
  {
    digitalWrite(ML_A2, LOW); // set the motor control signals
    digitalWrite(ML_A1, HIGH);
    analogWrite(EN_L, abs(val)); // give pwm signal to motor enable 
  }
}

void MR(int val)
{ // motor function right(val == speed value)

  if (val > 0)// if the motor speed is positive
  {

    digitalWrite(MR_A1, HIGH);// set the motor control signals
    digitalWrite(MR_A2, LOW);
    analogWrite(EN_R, val);// give pwm signal to motor enable 
  }
  else
  {
    digitalWrite(MR_A1, LOW); // set the motor control signals
    digitalWrite(MR_A2, HIGH);
    analogWrite(EN_R, abs(val)); // give pwm signal to motor enable 
  }
}

void movStraight(int spd)
{
  MR(spd);
  ML(spd);
}

void updateGyro()
{
  previousTime = currentTime;                        // Previous time is stored before the actual time read
  currentTime = millis();                            // Current time actual time read
  elapsedTime = (currentTime - previousTime) / 1000; // Divide by 1000 to get seconds
  Wire.beginTransmission(MPU);
  Wire.write(0x43); // Gyro data first register address 0x43
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 6, true);                   // Read 4 registers total, each axis value is stored in 2 registers
  GyroX = (Wire.read() << 8 | Wire.read()) / 32.75; // For a 1000deg/s range we have to divide first the raw value by 131.0, according to the datasheet
  GyroY = (Wire.read() << 8 | Wire.read()) / 131.0;
  GyroZ = (Wire.read() << 8 | Wire.read()) / 131.0;

  GyroX = GyroX - GyroErrorX; // GyroErrorX ~(-0.56)

  angle = angle + GyroX * elapsedTime; // deg/s * s = deg
  Serial.println(angle);
}

double radToDegree(double rads)
{
  return (float)(rads * 180 / PI);
}

// function to calculate the gyro error
void calculate_IMU_error()
{
  // init the gyro0
  Wire.begin();                // Initialize comunication
  Wire.beginTransmission(MPU); // Start communication with MPU6050 // MPU=0x68
  Wire.write(0x6B);            // Talk to 0 register 6B
  Wire.write(0x00);            // reset 
  Wire.endTransmission(true);  

  Wire.beginTransmission(MPU);
  Wire.write(0x1B); // Talk to the GYRO_CONFIG register (1B hex)
  Wire.write(0x10); // Set the register bits as 00010000 (1000deg/s full scale)
  Wire.endTransmission(true);
  delay(20);

  // Read gyro values 200 times
  while (c < 200)
  {
    Wire.beginTransmission(MPU);
    Wire.write(0x43);
    Wire.endTransmission(false);
    Wire.requestFrom(MPU, 6, true);
    GyroX = Wire.read() << 8 | Wire.read();
    GyroY = Wire.read() << 8 | Wire.read();
    GyroZ = Wire.read() << 8 | Wire.read();
    // Sum all readings
    GyroErrorX = GyroErrorX + (GyroX / 32.75);
    c++;
  }
  //Divide the sum by 200 to get the error value
  GyroErrorX = GyroErrorX / 200;

  // Print the error values on the Serial Monitor
  Serial.print("GyroErrorX: ");
  Serial.println(GyroErrorX);
}

int count = 0;//temp

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
    if(count == 3){
      startAngle = doc[myID][0];
      count = 0;
    }
    count++;
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
