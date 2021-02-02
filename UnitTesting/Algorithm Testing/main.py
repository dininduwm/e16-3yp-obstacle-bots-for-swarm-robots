import paho.mqtt.client as mqtt #import the client1
import movements
from robot import robot
from encrypt import aesEncrypt, aesEncryptString, aesDecrypt
from roboArrangement import  arrageBot
import random 
import math
import time
import json



# inporting the protobuff to serialize and deserialize the data
from MQTT_msg_pb2 import *

# swarm id
SWARM_ID = 0;
swarm_name = "platformPC UOP"
BOT_COUNT = 10;
ARENA_DIM = 30;

TOPIC_COM = 'swarm/common'
TOPIC_SEVER_COM = 'swarm/' + str(SWARM_ID) + '/com'
TOPIC_SEVER_BOT_POS = 'swarm/'+ str(SWARM_ID) + '/bot_pos'
connected_clients = []
robots_data = []
newBotPosArr = BotPositionArr()

power_factor = 1.0

def initialize():

    destX = set()
    destY = set()

    # for i in range(BOT_COUNT):
    #     robots_data.append(
    #         robot(
    #             (random.randint(5, ARENA_DIM-5 ),random.randint(5, ARENA_DIM-5 )), #TODO the corner bug should be resolved at the client
    #             0,
    #             (random.randint(5, ARENA_DIM-5 ),random.randint(5, ARENA_DIM-5 )),
    #             0
    #         )
    #     )
    arrageBot(robots_data, [])
    
        
def setDestinations(destinations):
    for dest in destinations:
        botId = int(dest[0])        
        if (botId)<BOT_COUNT:
            robots_data[botId].des_pos = (dest[1]['x'], dest[1]['y'])

def battStat():
    batt_lvls = {}
    for i in range(BOT_COUNT):
        batt_lvls[i] =  random.randint(0,100)
    return json.dumps(batt_lvls)

# on message function
def on_message(client, userdata, message):

    global power_factor

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
                print('client requests connection')
                client.publish(TOPIC_SEVER_COM, aesEncryptString('server_response;success;'+ json.dumps({'bot_count':BOT_COUNT, 'areana_dim':ARENA_DIM})))

            if messageString[1] == 'set_dest':
                print("Destination reset")
                destinations = json.loads(messageString[2])
                print(destinations)
                power_factor = 1.0
                arrageBot(robots_data , destinations)

            if messageString[1] == 'ping':
                client.publish(TOPIC_SEVER_COM, aesEncryptString('ping'))
            
            if messageString[1] == 'battStat':
                client.publish(TOPIC_SEVER_COM, aesEncryptString('battStat;' + battStat()))
    except :
        #print("message format error")
        pass

def Test(data_list, test_case_obj):
    
    global robots_data, power_factor
    robots_data = data_list
    # brocker ip address (this brokeris running inside our aws server)
    broker_address= "broker.mqttdashboard.com"
    print("creating new instance")

    # client Name
    client = mqtt.Client("Platform_PC", transport='websockets') #create new instance
    client.on_message = on_message # attach function to callback

    print("connecting to broker")
    client.connect(broker_address, 8000, 60) #connect to broker

    client.loop_start() 

    # subscribing to the current postion topic
    client.subscribe("swarm/{}/currentPos".format(SWARM_ID))
    client.subscribe(TOPIC_COM)
    client.subscribe(TOPIC_SEVER_COM)

    print("Publishing message to topic", "swarm/{}/currentPos".format(SWARM_ID))
    # serializing data using protobuff before sending data to the server 

    initialize()
    flagFirst = True
    # pulishing the msg to the topic
    stableCount = 0
    while(True):
        maxForce = 0.0
        time.sleep(0.2)
        
        
        if stableCount<2*BOT_COUNT:
            newBotPosArr = BotPositionArr()
            result = movements.action(robots_data, power_factor, test_case_obj)
            for i, robot in enumerate(result):
                F = robot[0]*100  # resultant force
                F = min(0.5, F)

                Dir = robot[1]  # relustant force direction
                

                dx = F*math.cos((Dir/180*math.pi))
                dy = F*math.sin((Dir/180*math.pi))
                
                robots_data[i].init_pos = (robots_data[i].init_pos[0] + dx, robots_data[i].init_pos[1] + dy)

                newBot = BotPosition()
                newBot.bot_id = i
                newBot.x_cod = robots_data[i].init_pos[0]
                newBot.y_cod = robots_data[i].init_pos[1]
                newBot.angle = 0
                newBotPosArr.positions.append(newBot)        
                

                if maxForce < F:
                    maxForce = F
            data = newBotPosArr.SerializeToString()
            client.publish(TOPIC_SEVER_BOT_POS, aesEncrypt(data))
            print("maxForce: " , maxForce)
        else:
            power_factor *= 10
            stableCount -= BOT_COUNT
            print("Reducing repulsion...")
        
        
        if maxForce < 0.002:
            stableCount = stableCount + 1

        if maxForce < 1e-10:
            for each_robot in robots_data:
                x_var = abs(each_robot.des_pos[0] - each_robot.init_pos[0])
                y_var = abs(each_robot.des_pos[1] - each_robot.init_pos[1])
                if x_var > 2 and y_var > 2:
                    test_case_obj.unstable_destinations += 1
            power_factor = 1
            return    

        if flagFirst:
            time.sleep(3)
            flagFirst = False

    client.loop_stop() #stop the loop

    client.disconnect()