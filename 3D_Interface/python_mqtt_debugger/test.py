import paho.mqtt.client as mqtt #import the client1
import time
import random
import json

# inporting the protobuff to serialize and deserialize the data
from MQTT_msg_pb2 import *

# swarm id
swarm_id = 0;
swarm_name = "platformPC UOP"
bot_count = 10;
arena_dim = 30;

TOPIC_COM = 'swarm/common'
TOPIC_SEVER_COM = 'swarm/' + str(swarm_id) + '/com'
TOPIC_SEVER_BOT_POS = 'swarm/'+ str(swarm_id) + '/bot_pos'
connected_clients = []

newBotPosArr = BotPositionArr()

# initalize bots
for i in range(bot_count):
    newBot = BotPosition()
    newBot.bot_id = 1
    newBot.x_cod = random.randint(0, arena_dim )
    newBot.y_cod = random.randint(0, arena_dim)
    newBot.angle = random.random()*360
    newBotPosArr.positions.append(newBot)



# on message function
def on_message(client, userdata, message):
    # newBotDecode = BotPositionArr.FromString(message.payload)
    messageString = message.payload.decode('utf-8').split(';')
    
    if message.topic == TOPIC_COM:
        if messageString[1] == 'get_servers':
            print('client requests server name')
            client.publish(TOPIC_COM, 'server_name_response;'+str(swarm_id)+';'+swarm_name)
    
    if message.topic == TOPIC_SEVER_COM:
        if messageString[1] == 'connection_req':
            print('client requests connection')
            client.publish(TOPIC_SEVER_COM, 'server_response;success;'+ json.dumps({'bot_count':bot_count, 'areana_dim':arena_dim}))


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
client.subscribe("swarm/{}/currentPos".format(swarm_id))
client.subscribe(TOPIC_COM)
client.subscribe(TOPIC_SEVER_COM)

print("Publishing message to topic", "swarm/{}/currentPos".format(swarm_id))
# serializing data using protobuff before sending data to the server 


# pulishing the msg to the topic
while(True):
    time.sleep(1)
    
    newBotPosArr = BotPositionArr()
# initalize bots
    for i in range(bot_count):
        newBot = BotPosition()
        newBot.bot_id = i
        newBot.x_cod = random.randint(0, arena_dim )
        newBot.y_cod = random.randint(0, arena_dim)
        newBot.angle = random.random()*360
        newBotPosArr.positions.append(newBot)

    data = newBotPosArr.SerializeToString()
    client.publish(TOPIC_SEVER_BOT_POS, data)


client.loop_stop() #stop the loop

client.disconnect()