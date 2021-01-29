import paho.mqtt.client as mqtt #import the client1
import movements
from robot import robot
import random 
import math
import time
import json


# inporting the protobuff to serialize and deserialize the data
from MQTT_msg_pb2 import *

# swarm id
SWARM_ID = 0;
swarm_name = "platformPC UOP"
BOT_COUNT = 8;
ARENA_DIM = 30;

TOPIC_COM = 'swarm/common'
TOPIC_SEVER_COM = 'swarm/' + str(SWARM_ID) + '/com'
TOPIC_SEVER_BOT_POS = 'swarm/'+ str(SWARM_ID) + '/bot_pos'
connected_clients = []
robots_data = []
newBotPosArr = BotPositionArr()

def initialize():
    global robots_data

    robots_data.append(
            robot(
                (0,0), #TODO the corner bug should be resolved at the client
                0,
                (30, 30),
                0
            )
    )

    robots_data.append(
            robot(
                (15,15), #TODO the corner bug should be resolved at the client
                0,
                (15, 15),
                0
            )
    )

    robots_data.append(
            robot(
                (30,0), #TODO the corner bug should be resolved at the client
                0,
                (1, 30),
                0
            )
    )

    robots_data.append(
            robot(
                (30,30), #TODO the corner bug should be resolved at the client
                0,
                (10, 10),
                0
            )
    )

    robots_data.append(
            robot(
                (0,30), #TODO the corner bug should be resolved at the client
                0,
                (30, 0),
                0
            )
    )

    robots_data.append(
            robot(
                (10,0), #TODO the corner bug should be resolved at the client
                0,
                (1, 20),
                0
            )
    )

    robots_data.append(
            robot(
                (7,25), #TODO the corner bug should be resolved at the client
                0,
                (10, 5),
                0
            )
    )

    robots_data.append(
            robot(
                (13,25), #TODO the corner bug should be resolved at the client
                0,
                (30, 7),
                0
            )
    )

    
        


# on message function
def on_message(client, userdata, message):
    # newBotDecode = BotPositionArr.FromString(message.payload)
    messageString = message.payload.decode('utf-8').split(';')
    
    if message.topic == TOPIC_COM:
        if messageString[1] == 'get_servers':
            print('client requests server name')
            client.publish(TOPIC_COM, 'server_name_response;'+str(SWARM_ID)+';'+swarm_name)
    
    if message.topic == TOPIC_SEVER_COM:
        if messageString[1] == 'connection_req':
            print('client requests connection')
            client.publish(TOPIC_SEVER_COM, 'server_response;success;'+ json.dumps({'bot_count':BOT_COUNT, 'areana_dim':ARENA_DIM}))


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

# pulishing the msg to the topic
while(True):
    time.sleep(0.2)
    
    newBotPosArr = BotPositionArr()
    

    result = movements.action(robots_data)
    for i, robot in enumerate(result):
        F = robot[0]*50  # resultant force
        F = min(0.5, F)

        Dir = robot[1]  # relustant force direction
        

        dx = F*math.cos((Dir/180*math.pi))
        dy = F*math.sin((Dir/180*math.pi))
        robots_data[i].init_pos = (robots_data[i].init_pos[0] + dx, robots_data[i].init_pos[1] + dy)

        newBot = BotPosition()
        newBot.bot_id = i
        newBot.x_cod = round(robots_data[i].init_pos[0])
        newBot.y_cod = round(robots_data[i].init_pos[1])
        newBot.angle = 0
        newBotPosArr.positions.append(newBot)        
        
        print(robots_data[i].init_pos, robots_data[i].des_pos, "Force: " , F, "Angle: ", Dir)
    

    data = newBotPosArr.SerializeToString()
    client.publish(TOPIC_SEVER_BOT_POS, data)


client.loop_stop() #stop the loop

client.disconnect()