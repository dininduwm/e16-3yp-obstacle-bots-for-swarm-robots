import { connenctToServer, serverData, pingAck, ping, setPingAck, resetServerData } from './mqttClient'



let icons = ['fas fa-globe-americas', 'fas fa-globe-europe', 'fas fa-globe-africa', 'fas fa-globe-asia']
let count = 0;
var online = false
var serverIdx = 0; //the index of the server that needed to be connected
export var serverList = {}
export function animateInternetIcon() {

    if (online) {
        setTimeout(() => {
            document.getElementById('InternetIcon').style.color = '#21f873'
            
            document.getElementById("online").style.color = '#21f873'
            document.getElementById("online").textContent = "online"

            document.getElementById("InternetIcon").className = icons[count]
            count++;
            count = count % 4;
            animateInternetIcon();
        }, 1000)
    }else{
        document.getElementById('InternetIcon').style.color = '#9da7a1'
        document.getElementById("online").style.color = '#9da7a1'
        document.getElementById("online").textContent = "offline"

    }
}

export function setOnline() {

}

export function findServer() {
    
    //search for available servers
    if (Object.keys(serverList).length == 0) {
        console.log("ServerList Empty");
        updateServerList();
        document.getElementById('serverName').textContent = 'No Servers'
        setTimeout(findServer, 2000);
    } else {
        if (serverData != null) {
            // if there are any online servers
            document.getElementById('serverName').textContent = serverList[serverIdx][1]
            online = true;
            pingServer()
            animateInternetIcon()
        } else {
            // connect to a specified server by the index, following is set to "0" for now
            connenctToServer(serverIdx);
            console.log("Trying to connect: "+serverList[serverIdx][1]);
            setTimeout(findServer, 2000);
        }

    }

}

// ping the server
function pingServer(){
    if(online){
        setTimeout(()=>{
            online = pingAck 
            setPingAck(false) //set the pingAck = false to detect if it will be true after pinging the server
            ping()  // ping the server 
            pingServer() // recurse the function
        },1000)
    }else{
        //this block run in a disconnection 
        setPingAck(true) // pingAck should be true to initiate the pinging 
        document.getElementById('serverName').textContent = "Reconnecting..."
        resetServerData(); // server data is set to null to force the findServer() function to call connectToServer() function
        findServer();
    }
}

export function updateServerList(){
    serverList = {0:[0, "platform PC UOP"]}
}