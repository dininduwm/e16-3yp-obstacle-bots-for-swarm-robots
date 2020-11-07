

let scene, sceneLight, renderer, camera, mesh, controls,pointLight1,pointLight2, particals = [], clock

function init() {
    scene = new THREE.Scene();
    
    sceneLight = new THREE.DirectionalLight(0xffffff, 0.5);
    sceneLight.position.set(0, 0, 1);
    scene.add(sceneLight);


    pointLight1 = new THREE.PointLight(0x4c0001, 300, 950, 2);
    pointLight1.position.set(0,0,1000);
    scene.add(pointLight1);

    
    pointLight2 = new THREE.PointLight(0x4c0198, 30, 500, 2);
    pointLight2.position.set(0,0,900);
    scene.add(pointLight2);


    mesh = new THREE.Mesh(
		new THREE.BoxGeometry(10,10,10),
		new THREE.MeshPhongMaterial({color:0xff4444})
	);
	mesh.position.z = 0;
	scene.add(mesh);
    
    camera = new THREE.PerspectiveCamera(75, window.innerWidth/ window.innerHeight, 1, 2000);
    camera.position.z = 1100;
    scene.add(camera);

    renderer = new THREE.WebGLRenderer();
    renderer.setClearColor(0x000000, 1);
    renderer.setSize(window.innerWidth, innerHeight);
    document.body.appendChild(renderer.domElement);

    controls = new THREE.OrbitControls(camera, renderer.domElement);

    renderer.render(scene, camera);
    particleSetup();
}
function particleSetup() {
    let loader = new THREE.TextureLoader();
    loader.load("/static/threejs/images/smoke.png", function (texture) {
        portalGeo = new THREE.PlaneBufferGeometry(350, 350);
        portalMat = new THREE.MeshStandardMaterial({
            map: texture,
            transparent: true
        });
        
        for (let i = 1000; i>0; i -= 13) {
            let particle = new THREE.Mesh(portalGeo, portalMat);
            particle.scale = new THREE.Vector3( 1, 1, 0 );
            
            particle.position.set(
                0.5*i*Math.cos(5*i*Math.PI/180),
                0.5*i*Math.sin(5*i*Math.PI/180), 
                1*i);
                particle.rotation.z = Math.random()*300
                particals.push(particle)
                scene.add(particle);
            }
            
            clock = new THREE.Clock();
            animate();
        });
    }
    
    
    function animate(){
        
        let dt =  clock.getDelta();
        particals.forEach(p => {
            p.rotation.z -= dt*0.01;
        });

        
        pointLight2.power =30+Math.random()*50
        
        camera.position.z += 0.3;
        controls.update();
        
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }
    
    
    init();