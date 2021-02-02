import paho.mqtt.client as mqtt #import the client1
from encrypt import aesEncrypt, aesEncryptString, aesDecrypt
import random 
import math
import time
import json
import string


# inporting the protobuff to serialize and deserialize the data
SWARM_ID = 0
TOPIC_COM = 'swarm/common'
TOPIC_ECHO = 'ecr/echo'
TOPIC_SEVER_COM = 'swarm/' + str(SWARM_ID) + '/com'
TOPIC_SEVER_BOT_POS = 'swarm/'+ str(SWARM_ID) + '/bot_pos'
client = None
count = 0
sent = []
recieved = []
def send():
    global client, count
   
    chars = "".join([random.choice(string.ascii_lowercase) for i in range(50)] )
    sent.append(chars)

    client.publish(TOPIC_COM, aesEncryptString(chars))


# on message function
def on_message(client, userdata, message):
    # newBotDecode = BotPositionArr.FromString(message.payload)
    print('recieved')
    if message.topic == TOPIC_ECHO:
        decrypted = aesDecrypt(message.payload).decode('utf-8')
        recieved.append(decrypted)
        

# brocker ip address (this brokeris running inside our aws server)
broker_address= "broker.mqttdashboard.com"
print("creating new instance")

# client Name
client = mqtt.Client("Platformasd_PC", transport='websockets') #create new instance
client.on_message = on_message # attach function to callback

print("connecting to broker")
client.connect(broker_address, 8000, 60) #connect to broker


# subscribing to the current postion topic
client.subscribe("swarm/{}/currentPos".format(SWARM_ID))
client.subscribe(TOPIC_COM)
client.subscribe(TOPIC_ECHO)

print("Publishing message to topic", "swarm/{}/currentPos".format(SWARM_ID))
# serializing data using protobuff before sending data to the server 
client.loop_start() 

flagFirst = True
# pulishing the msg to the topic
stableCount = 0
send()
for i in range(100):
    send()

time.sleep(2)

for i in range(100):
    if recieved[i] == sent[i]:
        print("SUCCESS => ", sent[i])
    else:
        print("FAIL => ", sent[i])
client.loop_stop() #stop the loop

client.disconnect()