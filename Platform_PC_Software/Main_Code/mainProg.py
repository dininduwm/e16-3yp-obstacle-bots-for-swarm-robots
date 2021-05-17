import cv2
import numpy as np
import time
import math
from math import atan
from kalman import kalman
from positioning_algo import positions  
import json
import serial
from multiprocessing import Process, Manager
from serialCom import readSerialData, sendToSerial, serialAutoSend
import movements
from robot import robot

# Settings section
serialComEn = False
ipCamEn = True
kalmanEn = False

# TODO: to be used in future 
# important variables
manager = Manager()
sharedData = manager.list()
sharedData.append("") # json string

# com port of the device
comPort = '/dev/ttyUSB0'

# making the connection with the seral port
if serialComEn:
    ser = serial.Serial(comPort, 9600, timeout=1, rtscts=1) # connecting to the serial port
    ser.flushInput()   

if ipCamEn:
    cam = cv2.VideoCapture('http://192.168.1.4:8080/video') # video source to capture images
else:
    cam = cv2.VideoCapture(0) # video source to capture images

# robot datas
robotData = {} 
robotDataSet = set()

# position dictonary to bradcast
broadcastPos = {}

# finction to convert for points to center point + angle
def convert(points):
    # grabing the points
    p1 = points[0]
    p2 = points[1]
    p3 = points[2]
    p4 = points[3]

    # calculating the center point
    center = [int((p1[0]+p2[0]+p3[0]+p4[0])/4), int((p1[1]+p2[1]+p3[1]+p4[1])/4)]
    
    return [center, [p2, p3]]

# parameters for saving the video
frameRate = 21
dispWidth = 640
dispHeight = 480

#Load the dictionary that was used to generate the markers.
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

# Initialize the detector parameters using default values
parameters =  cv2.aruco.DetectorParameters_create()

# saving to a video
#outVid = cv2.VideoWriter('videos/recordings.avi', cv2.VideoWriter_fourcc(*'XVID'),  frameRate, (dispWidth, dispHeight))

# calculate destinations
def desCalc(robots, broadcastPos):
    # need to optimize
    # print(robots)
    print(broadcastPos)
    global robot
    des = (3, 4)
    robots_data = []
    keys = []
    for key, robot_i in robots.items():
        keys.append(key)
        robots_data.append(
            robot(
                robot_i[0], 0, (3, 4), 0
            )
        )
    
    result = movements.action(robots_data)
    # print(result)

    for i, robot_i in enumerate(result):
        # calculate the direction
        F = robot_i[0]*100  # resultant force
        F = min(0.5, F)
        Dir = robot_i[1]  # relustant force direction
        dx = F*math.cos((Dir/180*math.pi))
        dy = F*math.sin((Dir/180*math.pi))
        # calculate the broadcast positions
        broadcastPos[keys[i]] = positions(robots[keys[i]][0], robots[keys[i]][3], [robots_data[i].init_pos[0] + dx, robots_data[i].init_pos[1] + dy], 0)
    
    return broadcastPos


def camProcess():

    # destination point
    desX = 400
    desY = 50

    global sharedData, broadcastPos
    print("Cam Process Started")
    while True:
        ret, frame = cam.read()    

        # Detect the markers in the image8
        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)

        # current marker id set
        markerSet = set()
        
        for i in range(len(markerCorners)):
            # ploting rectangles around the markers
            pts = np.array([markerCorners[i][0][0],markerCorners[i][0][1],markerCorners[i][0][2],markerCorners[i][0][3]], np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(frame,[pts],True,(0,255,255))

            # converting to center point
            conData = convert(markerCorners[i][0])
            frame = cv2.circle(frame, tuple(conData[0]), 1, (255,0,0), 2)

            frame = cv2.circle(frame, tuple(markerCorners[i][0][1]), 1, (0,255,0), 2)
            frame = cv2.circle(frame, tuple(markerCorners[i][0][2]), 1, (0,0,255), 2)

            # add to the marker id set
            markerSet.add(markerIds[i][0])

            # adding data to the dictionary
            if (markerIds[i][0] in robotData):
                if kalmanEn:
                    # adding data to the kalman obj
                    k_obj = robotData[markerIds[i][0]][2]       # grabbing the kalman object
                    kalVal = k_obj(conData[0], conData[1][0] , conData[1][1], True)    # calculating the kalman value

            else:
                if kalmanEn:
                    # add new key to the set
                    robotDataSet.add(markerIds[i][0])
                    # adding data to the kalman algo
                    k_obj = kalman(conData[0], conData[1][0], conData[1][1]) 
                    robotData[markerIds[i][0]][2] = k_obj   # adding kalman object to the array
                               # creating the kalman object                
                robotData[markerIds[i][0]] = [0,0,0,0,0]
            # adding data to the dictionary    
            robotData[markerIds[i][0]][0] = conData[0]
            robotData[markerIds[i][0]][1] = conData[1]
            robotData[markerIds[i][0]][3] = [tuple(markerCorners[i][0][1]), tuple(markerCorners[i][0][2])]

            # adding data to be broadcasted
            # TODO Changed
            # broadcastPos[int(markerIds[i][0])] = positions(conData[0], [tuple(markerCorners[i][0][1]), tuple(markerCorners[i][0][2])], [desX,desY], 0)

        if kalmanEn:
            # updating the not detected objects through kalman algo
            differentSet = robotDataSet - markerSet
                    
            for id in differentSet:
                k_obj = robotData[id][2]       # grabbing the kalman object
                k_obj([0,0],[0,0],[0,0],False)    # calculating the kalman value

                kalVal = k_obj.x.transpose()

                # setting data to the dataset
                robotData[id][0] = [kalVal[0], kalVal[1]]            
                robotData[id][1] = [[kalVal[2], kalVal[3]] , [kalVal[4], kalVal[5]]]

                # adding data to be broadcasted
                broadcastPos[id] = positions([kalVal[0], kalVal[1]], [[kalVal[2], kalVal[3]] , [kalVal[4], kalVal[5]]], [desX, desY], 0)

        # calculate destinations    
        broadcastPos = desCalc(robotData, broadcastPos)

        try:
            # print(broadcastPos[1][0], desX, desY)

            # add destination
            if (19 in robotData and True):
                desX = robotData[19][0][0]
                desY = robotData[19][0][1]
        except:
            pass
                
        #print(jsonEncodedData)

        # addig to the shared variable
        sharedData[0] = broadcastPos

        cv2.imshow('Cam', frame)

        #saving to the file
        #outVid.write(frame)

        if (cv2.waitKey(1) == ord('q')):
            break

    cam.release()
    #outVid.release()
    cv2.destroyAllWindows()

# main programme
if __name__ == '__main__':
    # adding the cam process to the pool
    p1 = Process(target=camProcess)
    # reading recived data from the arduino
    # p2 = Process(target=readSerialData, args=(ser,sharedData))
    # send data to the arduino
    if serialComEn:
        p3 = Process(target=serialAutoSend, args=(ser, sharedData))

    p1.start()   
    # p2.start() 
    if serialComEn:
        p3.start()   

    p1.join()   
    # p2.join() 
    if serialComEn:
        p3.join()