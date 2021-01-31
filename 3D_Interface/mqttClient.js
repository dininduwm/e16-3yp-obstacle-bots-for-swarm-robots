import MQTT from 'paho-mqtt';



let TOPIC_SEVER_BOT_POS = ''; // topic that server publishes bot positions - [unidirectional]
let TOPIC_SEVER_COM = '' //topic that server and a client communicate - [bidirectional]
const TOPIC_COM = 'swarm/common' // common data line for all the clients and servers - [bidirectional]

const mqtt_server = "broker.mqttdashboard.com";
const mqtt_port = 8000;
let mqtt_client;
let client_id = null;
let connected = false

let battStat_callback = null

var messages = require('./protobuf/MQTT_msg_pb.js');
var message = new messages.BotPositionArr()

export let mqtt_data, newData = false, serverList = {}, serverData = null, pingAck = true;

export function mqttClient() {

    //generate a random id for the client
    client_id = 'client_' + Math.random().toString(36).substring(2, 15); // create a random client Id
    // connect to the broker
    mqtt_client = new MQTT.Client(mqtt_server, mqtt_port, client_id);
    mqtt_client.connect({ reconnect: true, onSuccess: onConnect, onFailure: onFailure });
    return mqtt_client;

}

export function onConnect() {

    connected = true
    console.log('MQTT: connected');

    mqtt_client.onMessageArrived = onMessageArrived;
    mqtt_client.onConnectionLost = onConnectionLost;

    // Subscribe to topics
    mqtt_client.subscribe(TOPIC_COM);

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

        if (message_.topic == TOPIC_COM) {
            if (messageString[0] == "server_name_response") {
                serverList[messageString[1]] = [messageString[1], messageString[2]]
                
            }
        }

        if (message_.topic == TOPIC_SEVER_COM) {
            if (messageString[0] == "server_response") {
                if (messageString[1] == "success") {
                    console.log("server connecion success", messageString[2])
                    serverData = JSON.parse(messageString[2])
                } else {
                    serverData = null
                    console.log("server connecion refused")
                }
            }
            if(messageString[0] == "ping"){
                pingAck = true
            }

            if(messageString[0] == "battStat"){
                battStat_callback(messageString[1])
            }
        }
    }


}

// this functions id used to connect to a specific server
export function connenctToServer(serverIdx) {
    if (Object.keys(serverList).length != 0) {

        TOPIC_SEVER_BOT_POS = 'swarm/' + serverList[serverIdx][0] + '/bot_pos'
        TOPIC_SEVER_COM = 'swarm/' + serverList[serverIdx][0] + '/com'

        mqtt_client.subscribe(TOPIC_SEVER_BOT_POS)
        mqtt_client.subscribe(TOPIC_SEVER_COM)

        console.log("subscribed to server: " + serverList[serverIdx][0] +' name: '+ serverList[serverIdx][1])
        publish(TOPIC_SEVER_COM, client_id + ";connection_req")
    }

}

export function searchServers(){
    publish(TOPIC_COM, client_id + ";get_servers"); // request for platform pc names
}

export function ping(){
    publish(TOPIC_SEVER_COM, client_id + ";ping");
}

export function battStat(callback){
    battStat_callback = callback
    publish(TOPIC_SEVER_COM, client_id + ";battStat");
}

export function resetServerData(){
    serverData = null
}
export function onConnectionLost(response) {
    console.log(response.errorMessage);
}

export function publish(topic, message) {
    if (connected){
        var payload = new MQTT.Message(message);
        payload.destinationName = topic;
        mqtt_client.send(payload);
    }
}
export function setNewDataState(state) {
    newData = false;
}

export function setPingAck(state){
    pingAck = state
}

export function sendDestinations(destinations) {
    if (serverData != null && destinations != null) {
        var dest = []
        destinations.forEach((element) => {
            dest.push({ x: element.mesh.position.x + 0.5 + serverData.areana_dim / 2, y: element.mesh.position.z + 0.5 + serverData.areana_dim / 2 });
        })
        publish(TOPIC_SEVER_COM, client_id + ";set_dest;" + JSON.stringify(dest))
        console.log(dest)
    }
}


