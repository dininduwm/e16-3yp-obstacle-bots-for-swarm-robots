import { Item } from "./Item.js"
import { mqttClient, mqtt_data, newData, setNewDataState, serverData, sendDestinations, connenctToServer } from "./mqttClient.js";
import * as THREE from "three";
import config from "./config.js";

import { AxesHelper, Loader, Mesh, Scene, Vector3 } from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
import { animateInternetIcon, findServer } from "./servers.js"
import {drawLable, createLable, show_BattStat} from "./screenLables.js"

import arenaImg from "./resources/images/simbot_back-02.jpg";
import lightMap from "./resources/images/simbot_back_lightmap-02.jpg";
import botSTL from "./resources/3DModels/Cover.STL"

import TWEEN, { Tween } from "tween";

let scene, renderer, camera, root, controls, rayCaster, mouse, prevCameraPos;
let plane, cursor, botLight, controlsAtWork, mouse_arena_cordinates;
let destOpacity = { value: 1 }; // variables need for destination animation
let click = false, setDestMode = false;
let mqtt;
let bots = [];// an array to hold the collection of Bot instances
let destinations = null // this dictionary keeps destination objects with the reference of UUID 
let bots_initialized = false;
let botGroundClearence = 0.3

let WINDOW_HEIGHT = document.getElementById("root").getBoundingClientRect().height;
let WINDOW_WIDTH = document.getElementById("root").getBoundingClientRect().width;


function init() {
    //create a mqttClient
    mqtt = mqttClient();
    //initalte a scene 
    scene = new THREE.Scene();
    scene.background = (new THREE.Color(0xccdbd8));

    //initate a rendering object and set domentions
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(WINDOW_WIDTH, WINDOW_HEIGHT);
    // Enable Shadows in the Renderer
    renderer.shadowMap.type = THREE.PCFShadowMap;
    renderer.shadowMap.enabled = true;

    //initalize a raycaster
    rayCaster = new THREE.Raycaster();
    // raycasting only applied on layer 1 objects (this is done to avoid the curson being raycasted)
    rayCaster.layers.set(1);
    mouse = new THREE.Vector2();

    //initate a camera object 
    camera = new THREE.PerspectiveCamera(30, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 1000);
    camera.position.set(30, 30, 30);

    // append the rendering element to the html by the id of "root"
    root = document.getElementById("root");
    root.appendChild(renderer.domElement);

    //create a orbit controller 
    controls = new OrbitControls(camera, renderer.domElement);
    controls.update();

    //add a point light
    const light1 = new THREE.PointLight(0xffffff, 2, 1000);
    light1.position.set(-15, 20, -15);
    light1.shadow.bias = 0.00001;
    light1.shadow.mapSize.width = 1024 * 2;
    light1.shadow.mapSize.height = 1024 * 2;
    light1.shadow.camera.near = 0.1;
    light1.shadow.camera.far = 500;
    light1.castShadow = true;
    scene.add(light1);


    // create the arena 
    let texture = new THREE.TextureLoader().load(arenaImg);
    let lightmap = new THREE.TextureLoader().load(lightMap);
    //create the geometry and the materila for the arena
    let planeMat = new THREE.MeshPhongMaterial({ map: texture, lightMap: lightmap, shininess: 20 });//{map:texture, normalMap:texture});
    let PlaneGeo = new THREE.PlaneGeometry(config.AREANA_DIM, config.AREANA_DIM, 10, 10);
    plane = new THREE.Mesh(PlaneGeo, planeMat);
    plane.receiveShadow = true;
    plane.castShadow = true;
    plane.name = "arena";
    plane.layers.enable(1); // enable in layer 1 to get raycasted
    plane.rotateX(-Math.PI / 2);
    plane.position.set(0, 0, 0);
    scene.add(plane);



    //the light used to highlight the bot
    botLight = new THREE.PointLight(0x05f3ff, 20, 2);
    botLight.position.set(0, 1.5, 0);
    botLight.shadow.bias = 0.00001;
    // scene.add(botLight);

    scene.add(new AxesHelper(50));
    renderer.render(scene, camera);

    //create a temp box 
    let g = new THREE.BoxGeometry(1, 0.1, 1);
    let m = new THREE.MeshPhongMaterial({ color: 0x02f7ca, opacity: 0.5 });
    cursor = new THREE.Mesh(g, m);
    cursor.castShadow = true;
    cursor.material.transparent = true;
    cursor.position.set(0, 0.3, 0);
    console.log(cursor.layers);
    scene.add(cursor);

    setTimeout(updateBots, 1000);


    //handles the connection with the server
    findServer();

    //add thw event listner
    addEventListeners()

    //camera intro anomation
    animateCamera({ x: 40, y: 40, z: 40 }, 1000, TWEEN.Easing.Quintic.Out);

    // start animating the GUI
    animate();

    // start the animation of the internet Icon
    animateInternetIcon()

    
}



function initRobots() {
    //load the STL object to the scene
    let sltloader = new STLLoader();
    sltloader.load(botSTL, robotsLoader, undefined, function (error) {
        console.log("Error loading STL file");
    });

}

// function for loaging the slt, adding material ,creating the mesh, scale the model to proper dimentions 
function robotsLoader(stl) {
    // create the robot collection and create Bot instances
    // TODO -- convert this into a web request, rather than creating them with a random initila 
    stl.center()
    for (let i = 0; i < serverData.bot_count; i++) {
        let bot = new Item("obstacle")
        bot.id = bots.length
        //set the model parameter with new Mesh instance
        let material = new THREE.MeshPhongMaterial({
            color: 0xff5533,
            // specular: 100, 
            shininess: 500,
        });

        
        bot.setMesh(new Mesh(stl, material));

        // set a random position on the arena  float:0 - 1
        bot.setPos({ x: Math.random(), y: Math.random() })
        // the loaded stl file must be scaled down to fit the global scene,
        bot.mesh.geometry.computeBoundingBox(); // calculate the bounding box of the loaded bot


        let boundings = bot.mesh.geometry.boundingBox;
        // get the scaling ratio to scale the imported STL model to fit in the arena
        let ratio = Math.abs(config.BOT_DIM / (boundings.max.x - boundings.min.x));

        bot.mesh.scale.set(ratio, ratio, ratio);

        bot.mesh.castShadow = true;
        bot.mesh.receiveShadow = true;
        bot.mesh.name = "obstacle";
        bot.mesh.layers.enable(1); // enable in layer 1 to get raycasted    
        bot.tweens["position"] = new TWEEN.Tween(bot.mesh.position);
        scene.add(bot.mesh);
        
        bot.screenLable = createLable(bot.id)
        
        bots.push(bot)
        // push the bot mesh to an array

    }

}

//this is tempory funtion to simulate a robot movement
function updateBots() {

    //if new data is available
    if (!bots_initialized) {

        
        //initiate robots
        // server data will be available when the connection to the server is established
        if (serverData != undefined) {
            console.log(serverData.bot_count)
            bots_initialized = true
            initRobots();
        }
    } else {
        
        drawLable(WINDOW_WIDTH, WINDOW_HEIGHT, bots, camera); // draw the lables above bots

        if (newData) {
            for (let i = 0; i < bots.length; i++) {
                let pos = { x: mqtt_data[i].getXCod() - (config.AREANA_DIM / 2), y: mqtt_data[i].getYCod() - (config.AREANA_DIM / 2) };
                bots[i].mesh.lookAt((pos.x - 0.5), botGroundClearence, (pos.y - 0.5));
                bots[i].tweens["position"].to({ x: (pos.x - 0.5), y: botGroundClearence, z: (pos.y - 0.5) }, 500).start();
            }
            setNewDataState(false);
        }
    }

    // setTimeout(updateBots, 1000);
}


function createDestination(x, z) {
    // if there are no destinations assinged, first of all create the blinking animation 
    if (destinations == null) {
        destinations = new Map();
        //fade out animation

        let destinationTween = new TWEEN.Tween(destOpacity).to({ value: 0 }, 500).easing(TWEEN.Easing.Exponential.In);
        //fade in animation
        let destinationTween_reverse = new TWEEN.Tween(destOpacity).to({ value: 1 }, 500).easing(TWEEN.Easing.Exponential.Out);

        destinationTween.chain(destinationTween_reverse);
        destinationTween_reverse.chain(destinationTween);

        destinationTween.onUpdate(() => {
            destinations.forEach((element) => {
                element.mesh.material.opacity = destOpacity.value
            })
        });
        destinationTween_reverse.onUpdate(() => {
            destinations.forEach((element) => {
                element.mesh.material.opacity = destOpacity.value;
            })
        });

        destinationTween.start();
    }

    if (destinations.size < serverData.bot_count) {
        let dest = new Item("destination");
        let mesh = new THREE.Mesh(new THREE.BoxGeometry(2, 0.1, 2),
            new THREE.MeshBasicMaterial({ color: 0x00ff91, specular: 30, shininess: 100, opacity: 1 }));

        mesh.material.transparent = true;
        mesh.name = "destination";
        mesh.layers.enable(1);
        mesh.position.set(x, 0.1, z);
        dest.mesh = mesh;

        try {
            bots.forEach((bot) => {
                if (bot.status == "Idle") {
                    console.log(bot.id)
                    dest.id = bot.id
                    bot.status = "Busy"
                    throw BreakException;
                }
            })
        } catch {

        }


        scene.add(mesh);
        destinations.set(mesh.uuid, dest); // stores the destination object with the reference of mesh UUID 

        new TWEEN.Tween(mesh.scale).to({ x: 0.5, y: 0.5, z: 0.5 }, 800).easing(TWEEN.Easing.Elastic.Out).start()

    } else {
        console.log("All bots are occupied")
    }
}

function deleteDestination(object) {
    scene.remove(object)
    //release the bot from destination

    bots.forEach((bot) => {
        try {
            if (bot.id == destinations.get(object.uuid).id) {
                bot.status = "Idle"
                console.log("bot released: ", bot.id)
                throw BreakException
            }
        } catch { }
    })

    destinations.delete(object.uuid)
}




function animate() {

    controls.update();
    //updates bots
    updateBots();
    //mouse interactions
    mouseInteractions();


    //update tween animator    
    TWEEN.update();
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
    
}



// get actions for mouse interactions
function mouseInteractions() {
    //update the raycaster
    rayCaster.setFromCamera(mouse, camera);

    // get the intersetions
    const intersects = rayCaster.intersectObjects(scene.children);
    // if the orbitcontrols are not busy
    if (!controlsAtWork & (intersects.length != 0)) {


        // set the parameters of the bots to defauls, 
        bots.forEach((bot, index) => {
            bot.mesh.material.color.set(0xff5533);
        });


        // handle the interactions with the arena plane
        if (intersects[0].object.name == "arena") {
            let x = intersects[0].uv.x * config.AREANA_DIM - (config.AREANA_DIM / 2);
            let z = intersects[0].uv.y * config.AREANA_DIM - (config.AREANA_DIM / 2);

            x = Math.ceil(x) - 0.5;
            z = Math.ceil(-z) - 0.5;

            cursor.position.set(x, 0.01, z);

            // stores the cordinates on the arena in the  
            mouse_arena_cordinates = { x: x, y: z };

            // if a click happens on the plane and setDestMode if true, place a destination
            if (click & setDestMode) {
                createDestination(x, z);
                click = false;
            }

        }


        //handle the interactions with bots
        if (intersects[0].object.name == "obstacle") {
            intersects[0].object.material.color.set(0x05ffa3);

            
        }
        //handle the interactions with destinations
        if ((intersects[0].object.name == "destination") & click) {
            deleteDestination(intersects[0].object)
            click = false;
        }


    }

}





//add Event listners
function addEventListeners() {

    // these two event listner are needed to update a flag that denotes the orbitcontrols is at action
    // this flag is used to prevent unwanted mouse events while orbitcontrols are working 

    controls.addEventListener("change", () => { controlsAtWork = true; click = false; }); // if the mouse draged it click = false
    controls.addEventListener("end", () => { click = !controlsAtWork; controlsAtWork = false; });

    controls.addEventListener("mouseup", () => { console.log("oops") });

    //add the mouse moveEvent listner to get the ray casted cordinates
    document.getElementById("root").addEventListener("mousemove", (event) => {

        var rect = event.target.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / WINDOW_WIDTH) * 2 - 1;
        mouse.y = - ((event.clientY - rect.top) / WINDOW_HEIGHT) * 2 + 1;
    })


    // add setDestMode listner
    document.getElementById("setDestination").addEventListener("click", () => {

        if (!setDestMode) {
            // starting the destination setting mode
            // prevCameraPos = { x: camera.position.x, y: camera.position.y, z: camera.position.z };
            // // if its initiating the  setDestMode ,set the camera to the top view
            // animateCamera({ x: 0.01, y: camera.position.y, z: 30 }, 100, TWEEN.Easing.Linear.None).onComplete(() => {
            //     animateCamera({ x: 0, y: 70, z: 0 }, 1000, TWEEN.Easing.Exponential.Out)
            // });
            controls.rotateSpeed = 0;
        } else {
            // ending the destination setting 
            controls.rotateSpeed = 1;
            // animateCamera({ x: prevCameraPos.x, y: prevCameraPos.y, z: prevCameraPos.z }, 1000, TWEEN.Easing.Exponential.Out)

            // send the destinaion to the server
            sendDestinations(destinations);
        }


        setDestMode = !setDestMode;
    });

    // show battery status
    document.getElementById("batStat").addEventListener("click",()=>{
        show_BattStat(bots)
    });

    //add delete all destinations listener
    document.getElementById("deleteAllDestinations").addEventListener("click", () => {
        destinations.forEach((value, key) => {
            scene.remove(value.mesh);
            destinations.delete(key);
            console.log(destinations.size);
        });
    })



    // camera reset listner
    document.getElementById("CameraReset").addEventListener("click", () => {
        new TWEEN.Tween(camera.position).to({ x: 30, y: 30, z: 30 }, 1000).onUpdate(() => {
            controls.update()
        }).easing(TWEEN.Easing.Exponential.Out).start();
    });

    //camera top view listner
    document.getElementById("CameraTopView").addEventListener("click", () => {
        //get the camera to the position of x = 0.01, z = 30
        let animater = animateCamera({ x: 0.01, y: camera.position.y, z: 30 }, 100, TWEEN.Easing.Linear.None);
        animater.onComplete(() => {
            animateCamera({ x: 0, y: 70, z: 0 }, 1000, TWEEN.Easing.Exponential.Out)
        });
    });

    // add event listner to resize the viewport 
    window.addEventListener('resize', () => {
        WINDOW_HEIGHT = document.getElementById("root").getBoundingClientRect().height;
        WINDOW_WIDTH = document.getElementById("root").getBoundingClientRect().width;

        renderer.setSize(WINDOW_WIDTH, WINDOW_HEIGHT);
        camera.aspect = WINDOW_WIDTH / WINDOW_HEIGHT;
        camera.updateProjectionMatrix();
        console.log(WINDOW_HEIGHT, WINDOW_WIDTH);
    });

}

function animateCamera(pos, duration, easing) {
    return new TWEEN.Tween(camera.position).to(pos, duration).onUpdate(() => {
        controls.update()
    }).easing(easing).start();

}

init();


