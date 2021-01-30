import MQTT from 'paho-mqtt';



let TOPIC_SEVER_BOT_POS = ''; // topic that server publishes bot positions - [unidirectional]
let TOPIC_SEVER_COM = '' //topic that server and a client communicate - [bidirectional]
const TOPIC_COM = 'swarm/common' // common data line for all the clients and servers - [bidirectional]

const mqtt_server = "broker.mqttdashboard.com";
const mqtt_port = 8000;
let mqtt_client;
let client_id;

var messages = require('./protobuf/MQTT_msg_pb.js');
var message = new messages.BotPositionArr()

export let mqtt_data, newData = false, serverList = [], serverData;

export function mqttClient() {

    //generate a random id for the client
    client_id = 'client_' + Math.random().toString(36).substring(2, 15); // create a random client Id
    // connect to the broker
    mqtt_client = new MQTT.Client(mqtt_server, mqtt_port, client_id);
    mqtt_client.connect({ reconnect: true, onSuccess: onConnect, onFailure: onFailure });
    return mqtt_client;

}

export function onConnect() {

    console.log('MQTT: connected');

    mqtt_client.onMessageArrived = onMessageArrived;
    mqtt_client.onConnectionLost = onConnectionLost;

    // Subscribe to topics
    mqtt_client.subscribe(TOPIC_COM);

    publish(TOPIC_COM, client_id + ";get_servers"); // request for platform pc names

}
export function onFailure() {
    console.log('MQTT: connection failed');
}

export function onMessageArrived(message_) {

    if (message_.topic == TOPIC_SEVER_BOT_POS) {
        let s = messages.BotPositionArr.deserializeBinary(message_.payloadBytes);
        mqtt_data = s.getPositionsList()
        newData = true;
    } else {
        let messageString = message_.payloadString.split(';')
        if (messageString[0] == "server_name_response") {
            serverList.push(messageString[1])
            // console.log("Server name recieved; " + messageString[2])

            connenctToServer(0);
        }
        if (message_.topic == TOPIC_SEVER_COM) {
            if (messageString[0] == "server_response") {
                if (messageString[1] == "success") {
                    console.log("server connecion success", messageString[2])
                    serverData = JSON.parse(messageString[2])
                } else {
                    console.log("server connecion refused")
                }
            }
        }
    }


}

// this functions id used to connect to a specific server
export function connenctToServer(serverIdx) {
    if (serverList.length != 0) {

        TOPIC_SEVER_BOT_POS = 'swarm/' + serverList[serverIdx] + '/bot_pos'
        TOPIC_SEVER_COM = 'swarm/' + serverList[serverIdx] + '/com'

        mqtt_client.subscribe(TOPIC_SEVER_BOT_POS)
        mqtt_client.subscribe(TOPIC_SEVER_COM)

        console.log("subscribed to server: " + serverList[serverIdx])
        publish(TOPIC_SEVER_COM, client_id + ";connection_req")
    }

}

export function onConnectionLost(response) {
    console.log(response.errorMessage);
}

export function publish(topic, message) {
    var payload = new MQTT.Message(message);
    payload.destinationName = topic;
    mqtt_client.send(payload);
    console.log('MQTT: published');
}
export function setNewDataState(state) {
    newData = false;
}


