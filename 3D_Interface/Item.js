import config from "./config.js";

export class Item{ 
    constructor(type){
        this.id = null;
        this.type = type;
        this.pos ={x:0, y:0};// denotes the position in the arena by a 0-1 value
        this.mesh = null;
        this.tweens = {}; // hold the dictionary of tweens for this item
        this.discarded = false;
        this.light = null;
        this.status = "Idle";
        this.screenLable = null; //the lable that shown in the screen
    }
    setMesh(mesh){
        this.mesh = mesh;
    }
    setPos(pos){
        if(this.mesh != null){
            this.pos = pos;
            // set the pos.x --> mesh.position.x
            //         pos.y --> mesh.position.z
            this.mesh.position.set((pos.x-0.5)*config.AREANA_DIM, 0.3, (pos.y-0.5)*config.AREANA_DIM); 
        }else{
            console.log("No mesh assigned with this instance")
        }
    
        
    }
}
