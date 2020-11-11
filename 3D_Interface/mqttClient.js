import MQTT from 'paho-mqtt';

const TOPIC_BOT_POS = 'a';
const mqtt_server =  "0.0.0.0";
const mqtt_port = 9001;
let mqtt_client;

export function mqttClient(){

        //generate a random id for the client
        const client_id = 'client_' + Math.random().toString(36).substring(2, 15); // create a random client Id
        // connect to the broker
        mqtt_client = new MQTT.Client(mqtt_server, mqtt_port, client_id);
        mqtt_client.connect({reconnect: true, onSuccess: onConnect, onFailure:onFailure});
        
        return mqtt_client;
    }

export function onConnect(){
    
    console.log('MQTT: connected');

    // Subscribe to topics
    mqtt_client.subscribe(TOPIC_BOT_POS);
    
    mqtt_client.onMessageArrived = onMessageArrived;
    mqtt_client.onConnectionLost = onConnectionLost;

    
}
export function onFailure(){
    console.log('MQTT: connection failed');
}

export function onMessageArrived(message){
    console.log(message.payloadString);
} 
export function onConnectionLost(response){
    console.log(response.errorMessage);
}

export function publish(topic, message) {
    var payload = new MQTT.Message(message);
    payload.destinationName = topic;
    mqtt_client.send(payload);
    console.log('MQTT: published');
}


