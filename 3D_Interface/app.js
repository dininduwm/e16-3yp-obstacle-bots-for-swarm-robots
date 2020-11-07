import * as THREE from "three";
import { AxesHelper, Loader } from "three";
import {OrbitControls} from "three/examples/jsm/controls/OrbitControls.js";   
import arenaImg from "./resources/images/simbot_back.jpg";

let scene, renderer, camera, root, controls, pointLight
const AREANA_DIM = 30

function init(){
    //initalte a scene 
    scene = new THREE.Scene()
    scene.background = (new THREE.Color(0xf0f5f5));

    //initate a rendering object and set domentions
    renderer = new THREE.WebGLRenderer({antialias : true});
    renderer.setSize(window.innerWidth, window.innerHeight);
   
    //initate a camera object 
    camera = new THREE.PerspectiveCamera(30, innerWidth/innerHeight, 1, 1000);
    camera.position.set(100,100,100);

    // append the rendering element to the html by the id of "root"
    root = document.getElementById("root");
    root.appendChild(renderer.domElement);

    //create a orbit controller 
    controls = new OrbitControls(camera, renderer.domElement);
    controls.update();
    
    
    //add a light
    let ambientLight = new THREE.AmbientLight(0xffffff, 2);
	scene.add(ambientLight);


    // create the arena 
    let loader = new THREE.TextureLoader();
    let s = loader.load(arenaImg, function(texture){
        
        //create the geometry and the materila for the arena
        let PlaneGeo = new THREE.PlaneGeometry(AREANA_DIM, AREANA_DIM,10,10);
        let planeMat = new THREE.MeshPhongMaterial({map:texture, normalMap:texture});
        let plane = new THREE.Mesh(PlaneGeo, planeMat);
        plane.receiveShadow = true;

        console.log("ss");
        plane.rotateX(-Math.PI/2);
        plane.position.set(0, 0, 0);
        scene.add(plane);
    });
    
    //
    scene.add(new AxesHelper(50));
    renderer.render(scene, camera);

    // start animating the GUI
    animate();
}

function createPlane(dim_x, dim_y, pos_x, pos_y, pos_z, texture){

    const plane = new THREE.Mesh(new THREE.PlaneGeometry(dim_x, dim_y) , new THREE.MeshPhongMaterial());
    plane.rotateX(-Math.PI/2);
    plane.position.set(pos_x, pos_y, pos_z);
    return plane;


}

init();


function animate(){
    controls.update();
    requestAnimationFrame(animate);
    renderer.render(scene,camera);
}
