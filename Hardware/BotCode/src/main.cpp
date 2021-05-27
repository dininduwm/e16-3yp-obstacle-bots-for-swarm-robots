#include <PID_v1.h>
#include <Wire.h>

#define EN_R 9  // right motor enable
#define EN_L 10 // left motor enable

#define ML_A1 5 // left motor in 1
#define ML_A2 4 // left motor in 2

#define MR_A1 3 // right motor in 1
#define MR_A2 2 // right motor in 2

#define led_r 11 // status leds
#define led_g 12
#define led_b 13

const float turningThresh = 0.15; // threshold to stop turning
const double distThresh = 20;     // threshold to stop moving
const int MPU = 0x68;             // MPU6050 I2C address
float GyroX, GyroY, GyroZ;
float angle;                                  // Gyro angle
float GyroErrorX;                             // Gyro error
float elapsedTime, currentTime, previousTime; // time stamps for gyro calculaions
int c = 0;

bool idflag = false;
String id = "";
double arr[3]{};   // arr to hold startAngle, travelDis, endAngle
int idx = 0;     // index to track the arr index
bool good = false; // bool to check the correct id

//json decoded
double startAngle, endAngle, travelDis;

//PID variables
double Setpoint, Input, Output;
bool newData = false;

// id of the bot
String myID = "1";

// creating software serial object


// variables to hold temp data
String reciveStr = "";

//PID configuration
PID myPID(&Input, &Output, &Setpoint, 16, 0, 0.23, DIRECT);

void ML(int val)
{ // motor function left(val : speed value)

  //handle overflow in val
  if (val < -255)
  {
    val = -255;
  }
  else if (val > 255)
  {
    val = 255;
  }

  if (val > 0) // if the motor speed is positive
  {
    digitalWrite(ML_A2, HIGH); // set the motor control signals
    digitalWrite(ML_A1, LOW);
    analogWrite(EN_L, val); // give pwm signal to motor enable
  }
  else
  {
    digitalWrite(ML_A2, LOW); // set the motor control signals
    digitalWrite(ML_A1, HIGH);
    analogWrite(EN_L, abs(val)); // give pwm signal to motor enable
  }
}

void MR(int val)
{ // motor function right(val : speed value)

  //handle overflow in val
  if (val < -255)
  {
    val = -255;
  }
  else if (val > 255)
  {
    val = 255;
  }

  if (val > 0) // if the motor speed is positive
  {

    digitalWrite(MR_A1, HIGH); // set the motor control signals
    digitalWrite(MR_A2, LOW);
    analogWrite(EN_R, val); // give pwm signal to motor enable
  }
  else
  {
    digitalWrite(MR_A1, LOW); // set the motor control signals
    digitalWrite(MR_A2, HIGH);
    analogWrite(EN_R, abs(val)); // give pwm signal to motor enable
  }
}


void setup()
{
  pinMode(EN_R, OUTPUT);
  pinMode(EN_L, OUTPUT);
  pinMode(MR_A1, OUTPUT);
  pinMode(MR_A2, OUTPUT);
  pinMode(ML_A1, OUTPUT);
  pinMode(ML_A2, OUTPUT);
  pinMode(led_r, OUTPUT);
  pinMode(led_g, OUTPUT);
  pinMode(led_b, OUTPUT);

  // begining the serial commiunication



  myPID.SetOutputLimits(-255, 255); // limits of the PID output
  myPID.SetSampleTime(20);          // refresh rate of the PID
  myPID.SetMode(AUTOMATIC);
  Setpoint = 0;

  calculate_IMU_error(); // calculate the Gyro module error
  delay(20);
//  Serial.println("Bot initiated");

  intShow();
}

bool turningDone = false; // flag true if tuning is done
bool movingDone = false;  // flag true if robot at the destination
double prvstartAngle = 0; // vaiable used to track start angle changes
double spd = 125;         // speed of the movements: [-255, 255]

int tcount = 0;
double dirCorrection = -1;
double prevDist = 0;

void loop()
{
//  Setpoint = PI/2;  
//  
  while(true){
    for(int i =1; i<8; i++){
      LED(i);
      delay(100);
      LED(0);
      delay(100);
      LED(i);
      delay(100);
      LED(0);
      delay(1000);
      }  
    }
  if (Serial.available() > 0)
  {

    dataDecoder(Serial.read()); // parsing the json string
    LED(0);
  }

  // start turning process if the start angle is above the "turningThresh"
  if ((-turningThresh > startAngle) || (turningThresh < startAngle))
  {

    turn();
    LED(0);
  }

  // set the movingDone flag if the robo is at the destination
  if (travelDis < distThresh)
  {

    movingDone = true;
  }
  else
  {

    movingDone = false;
  }

  if ((tcount < 40) && turningDone && newData && !movingDone) //run motors with PID if conditions are satisfied
  {
    Setpoint = 0; // set the gyro setpoint to 0
    updateGyro();
    Input = (double)angle;
    myPID.Compute();
    ML(spd - Output);
    MR(spd + Output);
  }
  else
  {
    LED(0);
    newData = false;
    ML(0);
    MR(0);
  }

  tcount++;
  delay(5);
}

void turn()
{ 
  
  turningDone = false;
  angle = 0;                               //set the current angle to zer0
  Setpoint = -1 * radToDegree(startAngle); // set the setpoint as the startAngle

  prvstartAngle = startAngle; // update the prvstartAngle
//  Serial.println("started turning PID " + String(startAngle));

  while (!turningDone)
  {
    LED(2); //green
    if (Serial.available() > 0)
    {
      // parsing the json string
      dataDecoder(Serial.read());
    }

    if (prvstartAngle != startAngle) // if there any changes in startAngle, set the current angle to zero and set the set point
    {
      Setpoint = -1 * radToDegree(startAngle);
      angle = 0;
      prvstartAngle = startAngle;
    }
    updateGyro();
    Input = (double)angle;
    myPID.Compute();

    // Serial.println(String(startAngle) + ", " + String(Setpoint) + ", " + String(Input) + ", " + String(Output) + ", ");

    ML(-Output);
    MR(Output);
    if ((-turningThresh < startAngle) && (turningThresh > startAngle)) // exit form the loop if the startAngle is bounded in threshold
    {
//      Serial.println("turning done");
      turningDone = true;
    }
    LED(0); //off
  }
  angle = 0;
  ML(0);
  MR(0);




 
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
  GyroZ = (Wire.read() << 8 | Wire.read()) / 32.75;
  GyroZ = GyroZ - (-0.25); //GyroErrorX; // GyroErrorX ~(-0.56)

  angle = angle + GyroZ * elapsedTime; // deg/s * s = deg
  // Serial.println(GyroX);
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
    GyroErrorX = GyroErrorX + (GyroZ / 32.75);
    c++;
  }
  //Divide the sum by 200 to get the error value
  GyroErrorX = GyroErrorX / 200;

  // Print the error values on the Serial Monitor
//  Serial.print("GyroErrorZ: ");
//  Serial.println(GyroErrorX);
}

int count = 0; //temp

// function to decode
void dataDecoder(char c)
{
  LED(4);        //red
  if (c == '\n') // if the endline char
  {
    idflag = true; // start to read the id
    good = false;  // id is not good
    idx = 0;     // reset the index
  }
  else
  {
    if (c == ',') // if comma found
    {
      if (good) // if id is good
      {

        arr[idx] = id.toDouble(); // update the arr
        if (idx == 2)
        {
          newData = true; // set the newdata flag
          tcount = 0;     //when tcount < delay_constant the motor PID will start

//          Serial.println("data recieved");
          startAngle = arr[0]; // do what you want
          endAngle = arr[2];
          travelDis = arr[1];
//          Serial.println("data:" + String(st  artAngle) + " , " + String(endAngle) + " , " + String(travelDis) + ", " + String(angle));
        }
        idx = (idx + 1) % 3; // increment the index
      }
      if (idflag) // if id is getting
      {
        if (id == myID){
          LED(1); //blue
          good = true; // id is good
          delay(20);
          LED(0); //blue
        }
      }
      id = "";        // reset the id
      idflag = false; // id reading done`
    }
    else
      id += c; // append char to the id
  }
  if (Serial.available() > 0)
  {
    dataDecoder(Serial.read());
  }
}

void LED(byte color)
{
  digitalWrite(led_r, color & 1);
  digitalWrite(led_g, (color >> 1) & 1);
  digitalWrite(led_b, (color >> 2) & 1);
}

void intShow()
{

  LED(1); //blue
  pulse(200, 400);
  LED(2); //green
  pulse(200, 400);
  pulse(100, 800);
  LED(4); //red
  pulse(200, 200);
  LED(0);
  delay(1000);
  Serial.begin(9600);  // Setting the baud rate of Serial Monitor (Arduino)
}

void pulse(int pulsetime, int time)
{

  digitalWrite(ML_A1, HIGH);
  digitalWrite(ML_A2, LOW);
  digitalWrite(MR_A1, HIGH);
  digitalWrite(MR_A2, LOW);

  for (int i = 0; i < time; i++)
  {
    digitalWrite(EN_L, HIGH);
    digitalWrite(EN_R, HIGH);
    delayMicroseconds(pulsetime / 10);

    digitalWrite(EN_L, LOW);
    digitalWrite(EN_R, LOW);
    delayMicroseconds(pulsetime * 9 / 10);
  }
}