#Note demo scripts have limited or no error detection and use
#timers to wait for events. They assume everything works ok
#www.steves-internet-guide.com
#contact steve@steves-internet-guide.com
##Free to use for any purpose
##If you like and use this code you can
##buy me a drink here https://www.paypal.me/StepenCope
##Grateful for any feedback
#uses websockets publish-subscribe and receive message
import paho.mqtt.client as paho
import time
broker="broker.mqttdashboard.com"

#port= 80
#port=1883
port= 8000
sub_topic="house/#"
def on_subscribe(client, userdata, mid, granted_qos):   #create function for callback
   print("subscribed with qos",granted_qos, "\n")
   pass
def on_message(client, userdata, message):
    print("message received  "  ,str(message.payload.decode("utf-8")))
def on_publish(client,userdata,mid):   #create function for callback
   print("data published mid=",mid, "\n")
   pass
def on_disconnect(client, userdata, rc):
   print("client disconnected ok") 
client= paho.Client("client-socks",transport='websockets')       #create client object
#client= paho.Client("control1")
client.on_subscribe = on_subscribe       #assign function to callback
client.on_publish = on_publish        #assign function to callback
client.on_message = on_message        #assign function to callback
client.on_disconnect = on_disconnect
print("connecting to broker ",broker,"on port ",port)
client.connect(broker,port)           #establish connection
client.loop_start()
print("subscribing to ",sub_topic)
client.subscribe(sub_topic)

while(True):

   a = input()
   client.publish("house/bulb1","on")    #publish

client.disconnect()

