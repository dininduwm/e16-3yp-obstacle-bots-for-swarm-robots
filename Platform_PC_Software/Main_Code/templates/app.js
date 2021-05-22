
let devices = null
let response = null
var xhttp = new XMLHttpRequest();



// xhttp.open("GET", document.URL + 'search', true);
// xhttp.send();

// xhttp.onreadystatechange = function () {
//     if (this.readyState == 4 && this.status == 200) {
//         response = xhttp.responseText;
//         console.log(response)
//     }
// };

// document.getElementById("blur").addEventListener('change',()=>{
//     xhttp.open("POST", document.URL + 'submit_data', true);    
//     xhttp.send( JSON.stringify({"blur": document.getElementById("blur").value}));

// } )

// document.getElementById("color").addEventListener('change',()=>{

//     xhttp.open("POST", document.URL + 'submit_data', true);    
//     xhttp.send( JSON.stringify({"color":document.getElementById("color").value}));

// } )

// document.getElementById("refresh").addEventListener("click", ()=>{
//     console.log("refresh")
//     xhttp.open("GET", document.URL + 'refresh', true);
//     xhttp.send();

// })


function start() {
    // console.log("starting");
    xhttp.open("GET", document.URL + 'start', true);
    xhttp.send();
}

function pause() {
    // console.log("pausing");
    xhttp.open("GET", document.URL + 'pause', true);
    xhttp.send();
}

function home() {
    // console.log("home");
    xhttp.open("GET", document.URL + 'home', true);
    xhttp.send();
}

function stop() {
    // console.log("starting");
    xhttp.open("GET", document.URL + 'pause', true);
    xhttp.send();
}

function HomeBot1() {
    // console.log("home 1");
    xhttp.open("GET", document.URL + 'home_1', true);
    xhttp.send();
}

function HomeBot2() {
    // console.log("home 1");
    xhttp.open("GET", document.URL + 'home_2', true);
    xhttp.send();
}