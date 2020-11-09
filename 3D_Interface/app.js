import * as THREE from "three";
import { AxesHelper, Loader, Mesh, Scene, Vector3 } from "three";
import {OrbitControls} from "three/examples/jsm/controls/OrbitControls.js";
import {STLLoader} from "three/examples/jsm/loaders/STLLoader.js";

import arenaImg from "./resources/images/simbot_back.jpg";
import normalMap from "./resources/images/normal.jpg";
import botSTL from "./resources/3DModels/Cover.STL"

import TWEEN, { Tween } from "tween";
import { Clock } from "three/build/three.module";

let scene, renderer, camera, root, controls, pointLight, rayCaster, mouse, plane, cursor, botLight, controlsAtWork;

let bots = [];// an array to hold the collection of Bot instances
let botCount = 10; //this must be removed after implementing the communication protocal with the server

const AREANA_DIM = 30 // width or height of the arena
const WINDOW_HEIGHT = 900//window.innerHeight; 
const WINDOW_WIDTH = 1500//window.innerWidth;
const BOT_DIM = 1 // width or height of the bot

console.log(WINDOW_HEIGHT);
const camSpeed = 2 // speed constant fo the camera transit

function init(){
    //initalte a scene 
    scene = new THREE.Scene()
    scene.background = (new THREE.Color(0xf0f5f5));

    //initate a rendering object and set domentions
    renderer = new THREE.WebGLRenderer({antialias : true});
    renderer.setSize(WINDOW_WIDTH, WINDOW_HEIGHT);
    // Enable Shadows in the Renderer
	renderer.shadowMap.type = THREE.PCFShadowMap;
	renderer.shadowMap.enabled = true;
    
    //initalize a raycaster
    rayCaster = new THREE.Raycaster();
    mouse =  new THREE.Vector2();
    //add the mouse moveEvent listner to get the ray casted cordinates
    window.addEventListener("mousemove", (event)=>{

        var rect = event.target.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left)/ WINDOW_WIDTH ) * 2 - 1;
        mouse.y = - ( (event.clientY - rect.top) / WINDOW_HEIGHT ) * 2 + 1;
    })

   
    //initate a camera object 
    camera = new THREE.PerspectiveCamera(30, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 1000);
    camera.position.set(30,30,30);

    // append the rendering element to the html by the id of "root"
    root = document.getElementById("root");
    root.appendChild(renderer.domElement);

    //create a orbit controller 
    controls = new OrbitControls(camera, renderer.domElement);
    controls.update();
    
    //add a point light
    const light1 = new THREE.PointLight( 0xffffff, 2, 1000);
    light1.position.set( -15, 20, -15);
    light1.shadow.bias = 0.00001;
    light1.shadow.mapSize.width = 1024*2;
    light1.shadow.mapSize.height = 1024*2;
    light1.shadow.camera.near = 0.1;
    light1.shadow.camera.far = 500;
    light1.castShadow = true; 
    scene.add(light1);


    // create the arena 
    let texture = new THREE.TextureLoader().load(arenaImg);
    //create the geometry and the materila for the arena
    let planeMat = new THREE.MeshPhongMaterial({map:texture, lightMap:texture, specular: 100, shininess: 10 });//{map:texture, normalMap:texture});
    let PlaneGeo = new THREE.PlaneGeometry(AREANA_DIM, AREANA_DIM,10,10);
    plane = new THREE.Mesh(PlaneGeo, planeMat);
    plane.receiveShadow = true;
    plane.castShadow = true;
    plane.name = "arena";
    plane.rotateX(-Math.PI/2);
    plane.position.set(0, 0, 0);
    scene.add(plane);
    


    //the light used to highlight the bot
    botLight = new THREE.PointLight(0x05f3ff, 20, 2);
    botLight.position.set(0,1.5,0);
    botLight.shadow.bias = 0.00001;
    // scene.add(botLight);


   
    scene.add(new AxesHelper(50));
    renderer.render(scene, camera);


    //create a temp box 
    let g = new THREE.BoxGeometry(1,0.1,1);
    let m = new THREE.MeshPhongMaterial({color:0x02f7ca, opacity:0.5});
    cursor = new THREE.Mesh(g,m);
    cursor.castShadow = true;
    cursor.material.transparent =true;
    cursor.position.set(0,0.3,0);
    scene.add(cursor);

    setTimeout(updateBots, 1000);

    
    //initiate robots
    initRobots();

    //add thw event listner
    addEventListeners()

    //camera intro anomation
    animateCamera({x:40,y:40,z:40}, 1000, TWEEN.Easing.Quintic.Out );

    // start animating the GUI
    animate();


}

//class for creating a robot
class Bot{ 
    constructor(type){
        this.type = type;
        this.pos ={x:0, y:0};// denotes the position in the arena by a 0-1 value
        this.mesh = null;
        this.tween = null;
        this.light = null;
    }
    setMesh(mesh){
        this.mesh = mesh;
    }
    setPos(pos){
        if(this.mesh != null){
            this.pos = pos;
            // set the pos.x --> mesh.position.x
            //         pos.y --> mesh.position.z
            this.mesh.position.set((pos.x-0.5)*AREANA_DIM, -0.3, (pos.y-0.5)*AREANA_DIM); 
        }else{
            console.log("No mesh assigned with this instance")
        }
    }
}

function initRobots(){
    //load the STL object to the scene
    let sltloader = new STLLoader();
    sltloader.load(botSTL, robotsLoader, undefined,function(error){
        console.log("Error loading STL file");
    } );
      
}



// function for loaging the slt, adding material ,creating the mesh, scale the model to proper dimentions 
function robotsLoader(stl){
        // create the robot collection and create Bot instances
        // TODO -- convert this into a web request, rather than creating them with a random initila position
        for(let i = 0; i<botCount; i++){
            let bot = new Bot("obstacle")
            //set the model parameter with new Mesh instance
            let material = new THREE.MeshPhongMaterial({ 
                color: 0xff5533, 
                specular: 100, 
                shininess: 500,
                opacity:0 });

            bot.setMesh(new Mesh(stl, material));

            // set a random position on the arena  float:0 - 1
            bot.setPos({x:Math.random(), y:Math.random()})
            // the loaded stl file must be scaled down to fit the global scene,
            bot.mesh.geometry.computeBoundingBox(); // calculate the bounding box of the loaded bot
            let boundings = bot.mesh.geometry.boundingBox;
            // get the scaling ratio to scale the imported STL model to fit in the arena
            let ratio = Math.abs(BOT_DIM/ (boundings.max.x -  boundings.min.x)); 
            
            bot.mesh.scale.set(ratio,ratio,ratio); 
            bot.mesh.castShadow = true;           
            bot.mesh.receiveShadow = true;
            bot.mesh.name = "obstacle";

            bot.tween = new TWEEN.Tween(bot.mesh.position);
            scene.add(bot.mesh);
            // push the bot mesh to an array
            bots.push(bot);    
        }

}

//this is tempory funtion to simulate a robot movement
function updateBots(){
    console.log("dasd");
    for(let i =0; i<bots.length; i++){
        let pos = {x:Math.random(), y:Math.random()};
        bots[i].mesh.lookAt((pos.x-0.5)*AREANA_DIM, -0.3, (pos.y-0.5)*AREANA_DIM);
        bots[i].tween.to({x:(pos.x-0.5)*AREANA_DIM, y:-0.3, z:(pos.y-0.5)*AREANA_DIM},3000).start();
    }
    // setTimeout(updateBots, 1000);
}




function animate(){

    //mouse interactions
    mouseInteractions();

    renderer.render(scene,camera);
    //update tween animator    
    TWEEN.update();
    requestAnimationFrame(animate);
}


// get actions for mouse interactions
function mouseInteractions(){

    // if the orbitcontrols are not busy
    if(!controlsAtWork){
    
        //update the raycaster
        rayCaster.setFromCamera(mouse, camera);


        // set the parameters of the bots to defauls, 
        bots.forEach((bot, index)=>{
            bot.mesh.material.color.set(0xff5533);
        });


        // get the intersetions
        const intersects = rayCaster.intersectObjects(scene.children);

        for(let i = 0; i<intersects.length; i++){

            // handle the interactions with the arena plane
            if(intersects[i].object.name == "arena"){
                let x = intersects[i].uv.x*AREANA_DIM - (AREANA_DIM/2);
                let z = intersects[i].uv.y*AREANA_DIM - (AREANA_DIM/2); 
                cursor.position.set(Math.ceil(x)-0.5, 0.01, Math.ceil(-z)-0.5);

                // botLight.position.x = Math.ceil(x)+0.5;
                // botLight.position.z = Math.ceil(-z)+0.5;
            }

            //handle the interactions with bots
            if(intersects[i].object.name == "obstacle"){
                
                intersects[i].object.material.color.set(0x05ffa3);
            }
        }
    }
    
}




//add Event listners
function addEventListeners(){
    
    // these two event listner are needed to update a flag that denotes the orbitcontrols is at action
    // this flag is used to prevent unwanted mouse events while orbitcontrols are working 
    controls.addEventListener("start", ()=>{controlsAtWork = true});
    controls.addEventListener("end", ()=>{controlsAtWork = false});

    // camera reset listner
    document.getElementById("CameraReset").addEventListener("click", ()=>{
        new TWEEN.Tween(camera.position).to({x:30, y:30, z:30},1000).onUpdate(()=>{
            controls.update()
        }).easing(TWEEN.Easing.Exponential.Out).start();
    });
    
    //camera top view listner
    document.getElementById("CameraTopView").addEventListener("click", ()=>{
        //get the camera to the position of x = 0 
        new TWEEN.Tween(camera.position).to({x:0, y:camera.position.y, z:camera.position.z},100).onUpdate(()=>{
            controls.update()
        }).start().onComplete(()=>{// after the x = 0 is done set the camera to the top view 
            new TWEEN.Tween(camera.position).to({x:0, y:70, z:0},1000).onUpdate(()=>{controls.update()}).easing(TWEEN.Easing.Exponential.Out).start() });
    });

    
}



function animateCamera(pos, duration, easing){
    return new TWEEN.Tween(camera.position).to(pos,duration).onUpdate(()=>{
        controls.update()
    }).easing(easing).start();

}

init();