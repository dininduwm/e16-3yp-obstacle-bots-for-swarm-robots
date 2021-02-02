import paho.mqtt.client as mqtt #import the client1
from robot import robot
from encrypt import  aesEncrypt, aesEncryptString
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

def initialize():
    global robots_data
    destX = set()
    destY = set()

    for i in range(BOT_COUNT):
        robots_data.append(
            robot(
                (random.randint(5, ARENA_DIM-5 ),random.randint(5, ARENA_DIM-5 )), #TODO the corner bug should be resolved at the client
                0,
                (random.randint(5, ARENA_DIM-5 ),random.randint(5, ARENA_DIM-5 )),
                0
            )
        )
    arrageBot(robots_data, [])
    
        

# on message function
def on_message(client, userdata, message):
    # newBotDecode = BotPositionArr.FromString(message.payload)
    # messageString = message.payload.decode('utf-8').split(';')
    
    try:
        
        if message.topic == TOPIC_SEVER_COM:
            if messageString[1] == 'connection_req':
                print('client requests connection')
                client.publish(TOPIC_SEVER_COM, 'server_response;success;'+ json.dumps({'bot_count':BOT_COUNT, 'areana_dim':ARENA_DIM}))

            if messageString[1] == 'set_dest':
                print("Destination reset")
                destinations = json.loads(messageString[2])
                print(destinations)
                arrageBot(robots_data , destinations)

            if messageString[1] == 'ping':
                client.publish(TOPIC_SEVER_COM, 'ping')
            
            if messageString[1] == 'battStat':
                client.publish(TOPIC_SEVER_COM, 'battStat;' + battStat())
    except :
        print("message format error")
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
    

    newBotPosArr = BotPositionArr()
    for i, robot in enumerate(robots_data):

        newBot = BotPosition()
        newBot.bot_id = i
        newBot.x_cod = robots_data[i].init_pos[0]
        newBot.y_cod = robots_data[i].init_pos[1]
        newBot.angle = 0
        newBotPosArr.positions.append(newBot)        
        

       
    data = newBotPosArr.SerializeToString()
    client.publish(TOPIC_COM, aesEncryptString("asd"))
    time.sleep(1)
    break
    
client.loop_stop() #stop the loop

client.disconnect()