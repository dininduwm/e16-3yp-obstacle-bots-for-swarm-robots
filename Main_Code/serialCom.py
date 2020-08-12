import time

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
    data = data + '\n'
    ser.write(data.encode())

# this function is triggered periodicaly to broadcast data
def serialAutoSend(ser, sharedData):
    frequency = 1   # frequency the data to be sent in seconds
    while True:
        sendToSerial(ser, sharedData[0])
        time.sleep(frequency)