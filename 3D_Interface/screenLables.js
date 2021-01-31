import {battStat} from './mqttClient.js'


var isShowing = false;
let bots = null
export function drawLable(width, height, bots, camera) {

    bots.forEach((bot => {
        var object = bot.mesh
        var widthHalf = width / 2, heightHalf = height / 2;

        var pos = object.position.clone();
        pos.project(camera);
        pos.x = (pos.x * widthHalf) + widthHalf;
        pos.y = - (pos.y * heightHalf) + heightHalf;

        bot.screenLable.style.left = pos.x
        bot.screenLable.style.top = pos.y - 10
    }))

    // console.log(pos.x, pos.y)
}

// return a HTML lable 
export function createLable(id) {
    var parent = document.getElementById('root')
    var lableContainer = document.createElement('div')
    lableContainer.id = "lableContainer" + String(id)
    lableContainer.className = "lableContainer"

    lableContainer.appendChild(lableText(id));// create a HTML text element
    lableContainer.appendChild(battryBar(id)) // create a HTML batteryBar

    parent.insertBefore(lableContainer, parent.firstChild)
    return lableContainer
}

//return a HTML label
function lableText(id) {
    var text = document.createElement('label');
    text.id = 'labelText' + String(id)
    text.className = "labelText"
    text.textContent = '100%'
    return text
}
//return the HTML baterry bar
function battryBar(id) {
    var batterybar = document.createElement('div');
    batterybar.id = 'batteryBar' + String(id)
    batterybar.className = 'batterybar'

    var batterybarChild = document.createElement('div');
    batterybarChild.className = 'batterybarChild'
    batterybar.appendChild(batterybarChild);

    return batterybar;
}

//this function sets the baterry level of a specific bot
export function setBatteryLevel(bot, level, fullview) {
    var label = bot.screenLable

    //set the color
    var red = String((100 - level) * 0.01 * 255)
    var green = String((level) * 0.01 * 255)
    var color = 'rgba(' + red + ',' + green + ', 20, 0.966)'

    var text = label.children[0];
    var batteryBar = label.children[1].children[0]

    //make visible the battery label
    label.style.opacity = 1
    if (fullview) {
        text.style.opacity = 1
        label.style.backgroundColor = 'rgba(0, 8, 8, 0.185);'

        //sets the text label to the value of the level
        text.textContent = String(level) + '%'
        text.style.color = color
    } else {
        text.style.opacity = 0
        label.style.backgroundColor = 'rgba(0, 8, 8, 0)'
    }


    //set the battery level bar 
    batteryBar.style.width = String(level) + '%'
    batteryBar.style.backgroundColor = color


}// hides all the battery stats
export function hideAll_BattStat(bots) {
    bots.forEach((bot) => {
        bot.screenLable.style.opacity = 0
    })
}

// handles the show and hide functionality,
// battery state buttons onclick is handled by this function
export function show_BattStat(_bots) {
    if (_bots.length != 0) {
        if (isShowing) {
            hideAll_BattStat(_bots)
        } else {
            bots = _bots
            //publish a battery level request to the server
            battStat(callback)            
        }
        isShowing = !isShowing;
    }
}

export function callback(data){
    data = JSON.parse(data)
    console.log(data)
    if(bots!=null){
        bots.forEach((bot)=>{
            setBatteryLevel(bot, data[bot.id], true)
            console.log(data[bot.id])
        })
    }
}

