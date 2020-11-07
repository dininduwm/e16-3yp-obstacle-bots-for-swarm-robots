let scene, camera, renderer, box, controls,light, ambientLight;


function init(){
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xdddddd);
    camera = new THREE.PerspectiveCamera ( 75,window.innerWidth/ window.innerHeight, 0.1, 1000);
    camera.position.set(0,25,25);
    
    renderer = new THREE.WebGLRenderer({antialias:true});
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.BasicShadowMap;
    
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    scene.add(new THREE.AxesHelper(500));

    
    document.body.appendChild(renderer.domElement);

    const geometry = new THREE.BoxGeometry(2,2,1);
    const material = new THREE.MeshPhongMaterial({color:0x0000ff});
    const box = new THREE.Mesh(geometry, material);
    box.receiveShadow = true;
    
    scene.add(box);

    ambientLight = new THREE.AmbientLight(0xffffff, 0.2);
	scene.add(ambientLight);
    
    light = new THREE.PointLight(0xffffff, 0.8, 18);
	light.position.set(-3,6,-3);
	light.castShadow = true;
	// Will not light anything closer than 0.1 units or further than 25 units
	light.shadow.camera.near = 0.1;
	light.shadow.camera.far = 25;
	scene.add(light);
    
}


function animate (){
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
    box.position.x += 10
    
}

init();
animate();