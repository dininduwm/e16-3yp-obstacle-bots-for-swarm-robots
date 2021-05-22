import time
import json

# function to read the data from the serial
def readSerialData(ser, sharedData):   
    while True:                        # infinite loop
        if ser.in_waiting:
            data = ser.readline()
            if not (data == b'\r\n'):
                print(data)

                # data decoding
                if (data == b'OK\r\n'):
                    sharedData[0] = True
                    print("Sending Confirmed")
                elif (data == b'ERROR\r\n'):
                    sharedData[1] = True
        time.sleep(0.01)

def sendToSerial(ser, data):
    # sending data throug the serial port
    data = data + "\n"
    ser.write(data.encode())

# this function is triggered periodicaly to broadcast data
def serialAutoSend(ser, sharedData):
    interval = 0.25 # frequency the data to be sent in seconds

    while True:
        # send if the operator GUI enabled
        if sharedData[2]:
            # sendToSerial(ser, sharedData[0])
            for key in sharedData[0]:
                #print(key, sharedData[0][key])

                # creating a String
                data = str(key) + ',' + ','.join(map(str, sharedData[0][key])) + ','
                print("data ",data)

                # sending data through serial
                sendToSerial(ser, data)

                time.sleep(interval)
