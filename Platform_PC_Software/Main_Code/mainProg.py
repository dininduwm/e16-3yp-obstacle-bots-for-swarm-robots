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
import paho.mqtt.client as mqtt #import the client1
from encrypt import aesEncrypt, aesEncryptString, aesDecrypt
import json
from roboArrangement import  arrageBot
from MQTT_msg_pb2 import *
from flaskServing import *
from helpFunc import *

# swarm id
SWARM_ID = 0;
swarm_name = "platformPC UOP"
BOT_COUNT = 2;
ARENA_DIM = 30;

TOPIC_COM = 'swarm/common'
TOPIC_SEVER_COM = 'swarm/' + str(SWARM_ID) + '/com'
TOPIC_SEVER_BOT_POS = 'swarm/'+ str(SWARM_ID) + '/bot_pos'
connected_clients = []
robots_data = []
newBotPosArr = BotPositionArr()

# image resolutions
img_x = 640
img_y = 480 

# parameters for saving the video
frameRate = 21
dispWidth = 640
dispHeight = 480

# Settings section
serialComEn = True
ipCamEn = True
kalmanEn = False
flaskEn = True
cv2WindowEn = False

# TODO: to be used in future 
# important variables
manager = Manager()
sharedData = manager.list()
sharedData.append("") # json string
sharedData.append("") # json string
sharedData.append(False) # sharedData[2] is the serial broatcasting enable
sharedData.append("")

# com port of the device
comPort = '/dev/ttyUSB0'

# flags
desReachedFlag = False

# making the connection with the seral port
if serialComEn:
    ser = serial.Serial(comPort, 9600, timeout=1, rtscts=1) # connecting to the serial port
    ser.flushInput()   

if ipCamEn:
    cam = cv2.VideoCapture('http://192.168.1.5:8081/video') # video source to capture images
else:
    cam = cv2.VideoCapture(0) # video source to capture images

# robot datas
robotData = {} 
robotDataSet = set()

# position dictonary to bradcast
broadcastPos = {}

#Load the dictionary that was used to generate the markers.
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

# Initialize the detector parameters using default values
parameters =  cv2.aruco.DetectorParameters_create()

def battStat():
    batt_lvls = {}
    
    batt_lvls[0] = 85
    batt_lvls[1] = 79 
    
    return json.dumps(batt_lvls)

# on message function
def on_message(client, userdata, message):
    global BOT_COUNT
    # newBotDecode = BotPositionArr.FromString(message.payload)
    decrypted = aesDecrypt(message.payload).decode('utf-8')

    try:
        messageString = decrypted.split(';')
        if message.topic == TOPIC_COM:
            if messageString[1] == 'get_servers':
                print('client requests server name')
                client.publish(TOPIC_COM, aesEncryptString('server_name_response;'+str(SWARM_ID)+';'+swarm_name))
        
        if message.topic == TOPIC_SEVER_COM:
            if messageString[1] == 'connection_req':
                BOT_COUNT = len(robotData)
                print('client requests connection', {'bot_count':BOT_COUNT, 'areana_dim':ARENA_DIM})
                client.publish(TOPIC_SEVER_COM, aesEncryptString('server_response;success;'+ json.dumps({'bot_count':BOT_COUNT, 'areana_dim':ARENA_DIM})), qos = 2)

            if messageString[1] == 'set_dest':
                print("Destination reset")
                destinations = json.loads(messageString[2])
                remapDes(destinations)
                print(destinations)
                arrageBot(robotData , destinations)

            if messageString[1] == 'ping':
                client.publish(TOPIC_SEVER_COM, aesEncryptString('ping;'))
            
            if messageString[1] == 'battStat':
                client.publish(TOPIC_SEVER_COM, aesEncryptString('battStat;' + battStat()))
    except Exception as e :
        # pass
        print("message format error", e)

# saving to a video
#outVid = cv2.VideoWriter('videos/recordings.avi', cv2.VideoWriter_fourcc(*'XVID'),  frameRate, (dispWidth, dispHeight))

# homing sequence
def homeBots():
    homing_seq = sharedData[3]
    if homing_seq:
        # print('home', homing_seq)
        destinations = json.loads(homing_seq)
        arrageBot(robotData , destinations)
        sharedData[3] = ""

# calculate destinations
def destinationCalculation(robots, broadcastPos, frame, client):
    # check homing sequence
    homeBots()
    # create a array to store protobuf information
    newBotPosArr = BotPositionArr()

    # need to optimize
    # print(robots)
    # print(broadcastPos)
    global robot, desReachedFlag
    robots_data = []
    keys = []
    for key, robot_i in robots.items():
        keys.append(key)
        robots_data.append(
            robot(
                    robot_i[0], 0, robot_i[4], 0
            )
        )
    # print(robots_data)
    result = movements.action(robots_data)
    # print('fin',result)

    # count the bots who have reached the destination
    countDesReach = 0

    for i, robot_i in enumerate(result):
        # calculate the direction
        F = robot_i[0]*150000  # resultant force
        # F = min(0.5, F)
        Dir = robot_i[1]  # relustant force direction
        dx = F*math.cos((Dir/180*math.pi))
        dy = F*math.sin((Dir/180*math.pi))
        # print(dx,dy)

        # add the destination circle
        frame = cv2.circle(frame, tuple(robots_data[i].des_pos), 1, (0,255,0), 2)
        # print(frame.shape)
        #print((int(robots_data[i].init_pos[0] + dx), int(robots_data[i].init_pos[1] + dy)))
        frame = cv2.line(frame, (int(robots_data[i].init_pos[0]), int(robots_data[i].init_pos[1])), tuple(robots_data[i].des_pos), (0,255,0), 2)
        frame = cv2.line(frame, (int(robots_data[i].init_pos[0]), int(robots_data[i].init_pos[1])), (int(robots_data[i].init_pos[0]+dx), int(robots_data[i].init_pos[1]+dy)), (0,0,255), 2)

        # calculate the broadcast positions
        broadcastPos[keys[i]] = positions(robots[keys[i]][0], robots[keys[i]][3], [robots_data[i].init_pos[0] + dx, robots_data[i].init_pos[1] + dy], 0)

        # prepare data to send through mqtt
        newBot = BotPosition()
        newBot.bot_id = i
        newBot.x_cod = robots_data[i].init_pos[0]/img_x*30 
        newBot.y_cod = robots_data[i].init_pos[1]/img_y*30
        newBot.angle = 0
        newBotPosArr.positions.append(newBot)

        # print(distanceTwoPoints((int(robots_data[i].init_pos[0]), int(robots_data[i].init_pos[1])), tuple(robots_data[i].des_pos)))
        if 40<distanceTwoPoints((int(robots_data[i].init_pos[0]), int(robots_data[i].init_pos[1])), tuple(robots_data[i].des_pos)):
            countDesReach += 1

    # find if the destination reached
    if (countDesReach == 0):
        if desReachedFlag:            
            # print('All the bots reached the destinations')
            for i, robot_i in enumerate(result):
                broadcastPos[keys[i]] = positions(robots[keys[i]][0], robots[keys[i]][3], [robots_data[i].init_pos[0], robots_data[i].init_pos[1] + 5], 0)
        else:
            temp = []
            for i, robot_i in enumerate(result):
                broadcastPos[keys[i]] = positions(robots[keys[i]][0], robots[keys[i]][3], [robots_data[i].des_pos[0], robots_data[i].des_pos[1]], 0)
            for key in robotData:
                temp.append({'x':int(robotData[key][0][0]), 'y': int(robotData[key][0][1])})
            
            
            arrageBot(robotData, temp)
            desReachedFlag = True
    else:
        desReachedFlag = False

    # publishing data to mqtt
    data = newBotPosArr.SerializeToString()
    # print(data)
    client.publish(TOPIC_SEVER_BOT_POS, aesEncrypt(data))
    
    return broadcastPos


def camProcess():
    # brocker ip address (this brokeris running inside our aws server)
    broker_address= "broker.mqttdashboard.com"
    print("creating new instance")

    # client Name
    client = mqtt.Client("Platform_PC", transport='websockets') #create new instance
    client.on_message = on_message # attach function to callback

    print("connecting to broker")
    client.connect(broker_address, 8000, 60) #connect to broker
    # starting the mqtt client loop
    client.loop_start() 

    # subscribing to the current postion topic
    client.subscribe("swarm/{}/currentPos".format(SWARM_ID))
    client.subscribe(TOPIC_COM)
    client.subscribe(TOPIC_SEVER_COM)

    print("Publishing message to topic", "swarm/{}/currentPos".format(SWARM_ID))

    # destination point
    # desX = 400
    # desY = 50

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
                robotData[markerIds[i][0]] = [0,0,0,0,conData[0],True] # [center_point,top_two_cord,kalman,top_two_cord,destination,idle]
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
        broadcastPos = destinationCalculation(robotData, broadcastPos, frame, client)

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

        if cv2WindowEn:
            cv2.imshow('Cam', frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        img = buffer.tobytes()
        sharedData[1] = img
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
    # flask Thread
    if flaskEn:
        p2 = Process(target=flaskThread, args=(sharedData,))
    # send data to the arduino
    if serialComEn:
        p3 = Process(target=serialAutoSend, args=(ser, sharedData))

    p1.start()  
    if flaskEn: 
        p2.start() 
    if serialComEn:
        p3.start()   

    p1.join()  
    if flaskEn: 
        p2.join() 
    if serialComEn:
        p3.join()