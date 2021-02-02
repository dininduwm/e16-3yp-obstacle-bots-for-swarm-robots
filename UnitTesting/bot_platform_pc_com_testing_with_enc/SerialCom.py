import time
import serial
import json
import random
from writeToFile import writeData
from multiprocessing import Process, Manager

# function to read the data from the serial
def readSerialData(ser):   
    while True:                        # infinite loop
        if ser.in_waiting:
            data = ser.readline()
            if not (data == b'\r\n'):
                print(data)
                writeData(str(data), "test_data_2.txt")
        time.sleep(0.01)

def sendToSerial(ser, data):
    # sending data throug the serial port
    data = data + "\n"
    ser.write(data.encode())

# this function is triggered periodicaly to broadcast data
def serialSend(ser, sharedData):
    interval = 0.15  # frequency the data to be sent in seconds
    # sendToSerial(ser, sharedData[0])
    for key in sharedData[0]:
        #print(key, sharedData[0][key])

        # creating a String
        data = str(key) + ',' + ','.join(map(str, sharedData[0][key])) + ','
        #print(data)

        # sending data through serial
        sendToSerial(ser, data)

        time.sleep(interval)

def main(ser):
    time.sleep(5)
    print('Connected')
    # loop to do test cases
    for _ in range(10):
        sharedData = [{
            '1':[
            random.randint(0,500),
            random.randint(0,360),
            random.randint(0,500),
            random.randint(0,360),
            ],
            '2':[
            random.randint(0,500),
            random.randint(0,360),
            random.randint(0,500),
            random.randint(0,360),
            ],
        }] 
        writeData(str(sharedData[0]), "test_data_1.txt")
        serialSend(ser, sharedData)

# com port of the device
comPort = '/dev/cu.usbserial-14440'

# making the connection with the seral port
ser = serial.Serial(comPort, 9600, timeout=1, rtscts=1) # connecting to the serial port
ser.flushInput() 

p1 = Process(target=readSerialData, args=(ser,))
p2 = Process(target=main, args=(ser,))
p1.start() 
p2.start() 
p1.join()
p2.join()


