import paho.mqtt.client as mqtt #import the client1
import time
import random

# inporting the protobuff to serialize and deserialize the data
from MQTT_msg_pb2 import *

# swarm id
swarm_id = 0
bot_count = 20;
arena_dim = 30;


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
    #print("message received " ,str(message.payload.decode("utf-8")))
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)
    # decoding the recieved msg using proto buff
    newBotDecode = BotPositionArr.FromString(message.payload)
    print(newBotDecode)

# brocker ip address (this brokeris running inside our aws server)
broker_address= "broker.mqttdashboard.com"
print("creating new instance")

# client Name
client = mqtt.Client("Platform_PC", transport='websockets') #create new instance
client.on_message = on_message # attach function to callback

print("connecting to broker")
client.connect(broker_address, 8000, 60) #connect to broker

client.loop_start() #start the loop
# subscribing to the current postion topic
client.subscribe("swarm/{}/currentPos".format(swarm_id))

print("Publishing message to topic", "swarm/{}/currentPos".format(swarm_id))
# serializing data using protobuff before sending data to the server 

# pulishing the msg to the topic
while(True):
    time.sleep(4)
    
    newBotPosArr = BotPositionArr()
# initalize bots
    for i in range(bot_count):
        newBot = BotPosition()
        newBot.bot_id = i
        newBot.x_cod = newBot.x_cod + random.randint(5, arena_dim-5 )
        newBot.y_cod = newBot.y_cod + random.randint(5, arena_dim-5)
        newBot.angle = random.random()*360
        newBotPosArr.positions.append(newBot)

    data = newBotPosArr.SerializeToString()
    client.publish("swarm/{}/currentPos".format(swarm_id), data)


client.loop_stop() #stop the loop

client.disconnect()