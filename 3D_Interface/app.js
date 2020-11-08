import * as THREE from "three";
import { AxesHelper, Loader, Mesh, Scene, Vector3 } from "three";
import {OrbitControls} from "three/examples/jsm/controls/OrbitControls.js";
import {STLLoader} from "three/examples/jsm/loaders/STLLoader.js";

import arenaImg from "./resources/images/simbot_back.jpg";
import botSTL from "./resources/3DModels/Cover.STL"
import TWEEN, { Tween } from "tween";

let scene, renderer, camera, root, controls, pointLight, rayCaster, mouse, plane, b, mouse2;
const AREANA_DIM = 30 // width or height of the arena
const WINDOW_HEIGHT = 900//window.innerHeight; 
const WINDOW_WIDTH = 1000//window.innerWidth;
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
    
    //initalize a raycaster
    rayCaster = new THREE.Raycaster();
    mouse =  new THREE.Vector2();
    mouse2 =  new THREE.Vector2();
    //add the mouse moveEvent listner to get the ray casted cordinates
    window.addEventListener("mousemove", (event)=>{

        var rect = event.target.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left)/ WINDOW_WIDTH ) * 2 - 1;
        mouse.y = - ( (event.clientY - rect.top) / WINDOW_HEIGHT ) * 2 + 1;
    })

   
    //initate a camera object 
    camera = new THREE.PerspectiveCamera(30, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 1000);
    camera.position.set(100,100,100);

    // append the rendering element to the html by the id of "root"
    root = document.getElementById("root");
    root.appendChild(renderer.domElement);

    //create a orbit controller 
    controls = new OrbitControls(camera, renderer.domElement);
    controls.update();
    
    //add a point light
    const light = new THREE.PointLight( 0xffffff, 1, 1000);
    light.position.set( 10, 100, 0);
    scene.add(light);

    // create the arena 
    let loader = new THREE.TextureLoader();
    let s = loader.load(arenaImg, function(texture){
        
        //create the geometry and the materila for the arena
        let planeMat = new THREE.MeshPhongMaterial({map:texture, lightMap:texture, specular: 5, shininess: 100 });//{map:texture, normalMap:texture});
        let PlaneGeo = new THREE.PlaneGeometry(AREANA_DIM, AREANA_DIM,10,10);
        plane = new THREE.Mesh(PlaneGeo, planeMat);
        plane.receiveShadow = true;
        plane.name = "arena";
        plane.rotateX(-Math.PI/2);
        plane.position.set(0, 0, 0);
        scene.add(plane);
    });
    //
    scene.add(new AxesHelper(50));
    renderer.render(scene, camera);


    //create a temp box 
    let g = new THREE.BoxGeometry(2,2,2);
    let m = new THREE.MeshPhongMaterial({color:0x02f7ca});
    b = new THREE.Mesh(g,m);
    b.position.set(0,1,0);
    scene.add(b);


    //load the STL object to the scene
    let sltloader = new STLLoader();
    sltloader.load(botSTL, robotLoader, undefined,function(error){
        console.log(error);
    } );


    //add thw event listner
    addEventListeners()

    // start animating the GUI
    animate();
}


// function for loaging the slt, adding material ,creating the mesh, scale the model to proper dimentions 
function robotLoader(stl){
    let bot = new Mesh(stl, new THREE.MeshPhongMaterial({ 
        color: 0xff5533, 
        specular: 100, 
        shininess: 100 }));
    
    // the loaded stl file must be scaled down to fit the gloable scene,
    bot.geometry.computeBoundingBox(); // calculate the bounding box of the loaded bot
    let boundings = bot.geometry.boundingBox;
    let ratio = Math.abs(BOT_DIM/ (boundings.max.x -  boundings.min.x)); 
    bot.scale.set(ratio,ratio,ratio);   
    scene.add(bot);
}




function animate(){

    //update the raycaster
    rayCaster.setFromCamera(mouse, camera)

    // get the intersetions
    const intersects = rayCaster.intersectObjects(scene.children);
    for(let i = 0; i<intersects.length; i++){
        if(intersects[i].object.name == "arena"){
            let x = intersects[i].uv.x*AREANA_DIM - (AREANA_DIM/2);
            let z = intersects[i].uv.y*AREANA_DIM - (AREANA_DIM/2); 
            // console.log(mouse);
            b.position.set(x, 1, -z);
        }
    }

    renderer.render(scene,camera);
    //update tween animator    
    TWEEN.update();
    requestAnimationFrame(animate);
}


//add Event listners
function addEventListeners(){

    // TODO - handle the target resriing problem of the camera

    // camera reset listner
    document.getElementById("CameraReset").addEventListener("click", ()=>{
        new TWEEN.Tween(camera.position).to({x:50, y:50, z:50},1000).onUpdate(()=>{
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


init();