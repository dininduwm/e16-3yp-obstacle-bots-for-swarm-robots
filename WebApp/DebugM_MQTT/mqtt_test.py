import paho.mqtt.client as mqtt #import the client1
import time

# inporting the protobuff to serialize and deserialize the data
from MQTT_msg_pb2 import *

# swarm id
swarm_id = 0

# creating new bot position
newBot = BotPosition()
newBot.bot_id = 1
newBot.x_cod = 12
newBot.y_cod = 15
newBot.angle = 12.85

# creating a sample array
newBotPosArr = BotPositionArr()
newBotPosArr.positions.append(newBot)
newBot.bot_id = 2;
newBotPosArr.positions.append(newBot)
#print(newBotPosArr)


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
broker_address="54.163.154.240"
print("creating new instance")

# client Name
client = mqtt.Client("Platform_PC") #create new instance
client.on_message=on_message # attach function to callback

print("connecting to broker")
client.connect(broker_address, 1883, 60) #connect to broker

client.loop_start() #start the loop
# subscribing to the current postion topic
client.subscribe("swarm/{}/currentPos".format(swarm_id))

print("Publishing message to topic", "swarm/{}/currentPos".format(swarm_id))
# serializing data using protobuff before sending data to the server 
data = newBotPosArr.SerializeToString()

# pulishing the msg to the topic
client.publish("swarm/{}/currentPos".format(swarm_id), data)

time.sleep(4) # wait

client.loop_stop() #stop the loop
client.disconnect()