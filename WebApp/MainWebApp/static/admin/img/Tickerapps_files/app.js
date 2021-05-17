// importing mqtt 
let mqtt;
// defining variable to connect with mqtt brocker
const reconnectTimeout = 2000;
//const mqtt_server = "broker.mqttdashboard.com";
const mqtt_server = "tickerapps.com";
const mqtt_port = 801;
let mqtt_client;

// genaral varible seciton
let client_id = null;
let connected = false
let authDateObj = '';

// money formating 
function formatMoney(amount, decimalCount = 2, decimal = ".", thousands = ",") {
    try {
      decimalCount = Math.abs(decimalCount);
      decimalCount = isNaN(decimalCount) ? 2 : decimalCount;
  
      const negativeSign = amount < 0 ? "-" : "";
  
      let i = parseInt(amount = Math.abs(Number(amount) || 0).toFixed(decimalCount)).toString();
      let j = (i.length > 3) ? i.length % 3 : 0;
  
      return negativeSign + (j ? i.substr(0, j) + thousands : '') + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + thousands) + (decimalCount ? decimal + Math.abs(amount - i).toFixed(decimalCount).slice(2) : "");
    } catch (e) {
      console.log(e)
    }
  };

// decode and update the dom
function decodeAndUpdateDOM(message) {
    try {
        let decodedMsg = JSON.parse(message);
        // console.log(decodedMsg);
        // document.querySelector('.usd_val').childNodes[0].nodeValue = formatMoney(decodedMsg.last);
        // spliting the number
        let splited = formatMoney(decodedMsg.last).split(',');
        let dotsplit = splited[1].split('.');
        document.querySelector('.usd_val_1').childNodes[0].nodeValue = splited[0];
        document.querySelector('.usd_val_2').childNodes[0].nodeValue = dotsplit[0];
        document.querySelector('.usd_val_3').childNodes[0].nodeValue = dotsplit[1];
        document.querySelector('.current_high_val').childNodes[1].nodeValue = formatMoney(decodedMsg.ask);
        document.querySelector('.current_low_val').childNodes[1].nodeValue = formatMoney(decodedMsg.bid);
        if (decodedMsg.change_price_day > 0){
            document.querySelector('.h24_change_usd').childNodes[0].nodeValue = '+'
            document.querySelector('.h24_change_usd').childNodes[2].nodeValue = formatMoney(Math.abs(decodedMsg.change_price_day));
            document.querySelector('.h24_change_percentage').childNodes[0].nodeValue = '+' + formatMoney(Math.abs(decodedMsg.change_percent_day))+'%';
            document.querySelector('.h24_change_usd').style.color = 'green';
            document.querySelector('.h24_change_percentage').style.color = 'green';
        } else {
            document.querySelector('.h24_change_usd').childNodes[0].nodeValue = '-'
            document.querySelector('.h24_change_usd').childNodes[2].nodeValue = formatMoney(Math.abs(decodedMsg.change_price_day));
            document.querySelector('.h24_change_percentage').childNodes[0].nodeValue = '-' + formatMoney(Math.abs(decodedMsg.change_percent_day))+'%';
            document.querySelector('.h24_change_usd').style.color = 'red';
            document.querySelector('.h24_change_percentage').style.color = 'red';
        }
        // 24h high and low value
        document.querySelector('.h24_high_val_val').childNodes[1].nodeValue = formatMoney(decodedMsg.high);
        document.querySelector('.h24_low_val_val').childNodes[1].nodeValue = formatMoney(decodedMsg.low);
    
        // genarate ath data 
        let ath = decodedMsg.ath;
        let athTime = decodedMsg.ath_date;
        authDateObj = new Date(athTime);

        // put the ath to the dom
        document.querySelector('.ath_time_high_text_val').childNodes[1].nodeValue = formatMoney(ath);
        document.querySelector('.ath_time_high_date').childNodes[0].nodeValue = 'on ' + formatDate(authDateObj);
    } catch (e) {
        console.log(e);
    }
}

// function to trigger when the mqtt client gets connected
function onConnect() {
    console.log('Connectd');

    // subscribe to the topic
    mqtt_client.onMessageArrived = onMessageArrived;
    mqtt_client.onConnectionLost = onConnectionLost;

    // Subscribe to topics
    mqtt_client.subscribe(topic);
}

// function to trigger whtn the the connection faild
function onFailure() {
    console.log('MQTT: connection failed');
}

// on message recieved function
function onMessageArrived(message) {
    // let messageStr = message._getPayloadString();
    try{
    let messageBytes = message.payloadBytes;
    let decryptedText = decrypt(messageBytes);
    // console.log(decryptedText);
    decodeAndUpdateDOM(decryptedText);
    } catch {
        console.log('decryption error');
    }
}

// on connection lost function
function onConnectionLost(response) {
    console.log(response.errorMessage);
}

// connect to the mqtt client
function connectToMQTT() {
    //generate a random id for the client
    client_id = 'client_' + Math.random().toString(36).substring(2, 15); // create a random client Id
    mqtt_client = new Paho.MQTT.Client(mqtt_server, mqtt_port, client_id);
    mqtt_client.connect({ onSuccess: onConnect, onFailure: onFailure, useSSL:true });
    return mqtt_client;
}

// format the date 
function formatDate(d){
    const ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(d);
    const mo = new Intl.DateTimeFormat('en', { month: 'short' }).format(d);
    const da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(d);
    return (`${da} ${mo.toUpperCase()} ${ye}`);
}

// calculte the time
function formatTime(time) {
    let seconds = Math.round(time/1000);
    let days = Math.floor(seconds/(3600*24));
    let left = seconds - (days*3600*24);
    let hours = Math.floor(left/(3600));
    left -= hours*3600;  
    let mins = Math.floor(left/60);
    left -= mins*60;
    let secs = left;
    return (`${String(days).padStart(2, '0')}:${String(hours).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`);
}

// tick the time since ath clock
function tickClock() {
    let nowObj = Date.now();
    let timeSinceATH = nowObj - authDateObj;
    document.querySelector('.ath_time_high_time_val').childNodes[0].nodeValue = formatTime(timeSinceATH);
}

function inintVals() {
    console.log(document.querySelector('.usd_val'));
}

// decryption library
let key = JSON.parse(document.getElementById('key').value);


function decrypt(data) {
    try {
        var iv = data.slice(0, 16)
        var cipher = data.slice(16, data.length)
        var aesofb = new aesjs.ModeOfOperation.ofb(key, iv);
        var decryptedBytes = aesofb.decrypt(cipher);
    } catch {
        console.log('decryption error')
    }
    // return decryptedBytes
    return aesjs.utils.utf8.fromBytes(decryptedBytes);
}

// remove bold from safari
var isSafari = /constructor/i.test(window.HTMLElement) || (function (p) { return p.toString() === "[object SafariRemoteNotification]"; })(!window['safari'] || (typeof safari !== 'undefined' && window['safari'].pushNotification));
if (isSafari) {
    var r = document.querySelector(':root');
    r.style.setProperty('--fontSize', 0.88);
    // document.querySelector('body').style.fontWeight = 'normal';
}
var userAgent = window.navigator.userAgent;
if (userAgent.match(/iPad/i) || userAgent.match(/iPhone/i)) {
    var r = document.querySelector(':root');
    r.style.setProperty('--fontSize', 0.88);
    // document.querySelector('body').style.fontWeight = 'normal';
}
// var isFirefox = typeof InstallTrigger !== 'undefined';
// if (isFirefox) {
//     document.querySelector('body').style.fontWeight = 'normal';
// }
mqtt_client = connectToMQTT();
// get data from congeco
setInterval(tickClock, 1000);
const d = new Date(2010, 7, 5);
let topic = document.getElementById('topic').value;

