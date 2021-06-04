# Swarm Robotics Platform

### Team
* Members
   * Thushara K A R         :: E/16/369 :: [e16369@eng.pdn.ac.lk](e16369@eng.pdn.ac.lk)
   * Thilakarathna D M D U  :: E/16/366 :: [e16366@eng.pdn.ac.lk](e16366@eng.pdn.ac.lk)
   * Dissanayake D M T H    :: E/16/088 :: [e16088@eng.pdn.ac.lk](e16088@eng.pdn.ac.lk)
* Supervisor
   * Dr. Isuru Navinna
   * Mr. Ziyan Marikkar
   * Prof. Roshan Ragel
   * Dr. Upul Jayasinghe
* Related links
   * [Faculty website](http://eng.pdn.ac.lk/)
   * [Department website](http://www.ce.pdn.ac.lk/)
   * [Web Application Home Page](http://3.93.215.173/)
   * [Swarm Dash Board](http://3.93.215.173/swarm/)
   * [Git Hub Repository](https://github.com/cepdnaclk/e16-3yp-obstacle-bots-for-swarm-robots)
   * [Design Manual](https://github.com/cepdnaclk/e16-3yp-obstacle-bots-for-swarm-robots/blob/master/Documentation/DesignManual.pdf)
   * [User Manual](https://github.com/cepdnaclk/e16-3yp-obstacle-bots-for-swarm-robots/blob/master/Documentation/UserManual.pdf)

### TABLE OF CONTENT

1. >[OVERVIEW](https://github.com/cepdnaclk/e16-3yp-obstacle-bots-for-swarm-robots#overview)
2. >[GOALS](https://github.com/cepdnaclk/e16-3yp-obstacle-bots-for-swarm-robots#goals)
3. >[SPECIFICATIONS](https://github.com/cepdnaclk/e16-3yp-obstacle-bots-for-swarm-robots#specifications)
4. >[SOLUTION ARCHITECTURE](https://github.com/cepdnaclk/e16-3yp-obstacle-bots-for-swarm-robots#solution-architecture)
5. >[HARDWARE](https://github.com/cepdnaclk/e16-3yp-obstacle-bots-for-swarm-robots#hardware)
6. >[WEB INTERFACE](https://github.com/cepdnaclk/e16-3yp-obstacle-bots-for-swarm-robots#software)
7. >[ALGORITHM](https://github.com/cepdnaclk/e16-3yp-obstacle-bots-for-swarm-robots#algorithm)
8. >[TESTING](https://github.com/cepdnaclk/e16-3yp-obstacle-bots-for-swarm-robots#testing)
9. >[BUDGET](https://github.com/cepdnaclk/e16-3yp-obstacle-bots-for-swarm-robots#budget)



### OVERVIEW

In swarm robotics the major barrier is that the researchers have to do a lot of hardware implementation prior to their projects. In this particular project we are going to come up with obstacle bots for a swarm robotic arena which is a part of a swarm robots platform project which eventually solves the above mentioned problem. 

### GOALS

* Automated obstacle bots monitored by an overhead camera setup.

* Bots can move to the desired positions with a user friendly interface.

### SPECIFICATIONS

* Obstacle robot swarm is capable of moving every individual obstacle robot to their own destination with the consideration of  collision  avoidance. 

* With the help of collision avoidance algorithms, obstacle robots can be placed in certain positions which allows the researcher to make  various obstacle shapes on the arena made out of obstacle robot combinations .

* Obstacles can be programmed to be static or dynamic. Dynamic obstacles can model scenarios that have a motion in the obstacle.

* Each robot has its own radio module  which uses a 433Mhz radio band. These modules can be used to communicate with the base station. 

* Each robot has two independent wheels that can perform forward, backward and turning operations. With the help of inbuilt gyroscope robots can perform accurate turning operations.

### SOLUTION ARCHITECTURE
    
   ![robot_base_design](https://github.com/dtdinidu7/e16-3yp-obstacle-bots-for-swarm-robots/blob/master/docs/img/highlvl.jpg?raw=true)

### HARDWARE

 * #### REAL HARDWARE
    ![robot_base_design](https://github.com/dtdinidu7/e16-3yp-obstacle-bots-for-swarm-robots/blob/master/docs/img/New_Bot.jpg?raw=true)

   ![STATUS _LED](https://github.com/dtdinidu7/e16-3yp-obstacle-bots-for-swarm-robots/blob/master/docs/img/status_led.gif?raw=true)
 * #### 3D MODEL
 
   ![MODEL](https://github.com/dtdinidu7/e16-3yp-obstacle-bots-for-swarm-robots/blob/master/docs/img/solid_full.jpg?raw=true)
   
   [3D MODEL DEMO VIDEO](https://drive.google.com/file/d/1BgqnTfJoUTvxhPZTlfKIsdu9cmKUDJUL/view?usp=sharing)

 * #### SAFTY MEASURES

    ![IMERGENCY STATUS](https://github.com/dtdinidu7/e16-3yp-obstacle-bots-for-swarm-robots/blob/master/docs/img/imergency_status.gif?raw=true)

    
* #### PCB DESIGN

  ![PCB](https://github.com/dtdinidu7/e16-3yp-obstacle-bots-for-swarm-robots/blob/master/docs/img/schemetic.png?raw=true)

  ![PCB](https://github.com/dtdinidu7/e16-3yp-obstacle-bots-for-swarm-robots/blob/master/docs/img/pcb1.jpg?raw=true)
  
  [PCB DEMO VIDEO](https://drive.google.com/file/d/1F948O53cgekAJtsLhbUBktsmgBemvtih/view?usp=sharing)
  
### WEB INTERFACE

   #### Web Interface

   [WEB INTERFACE DEMO VIDEO](https://drive.google.com/file/d/1p-WY_BGf4mX0sW0hUGA0x1Oh4LhzKp-s/view?usp=sharing)

   #### 3D Interface

   [3D INTERFACE DEMO VIDEO](https://drive.google.com/file/d/1X0jq2r_McNR5bppIPc1HjJY1mYPvrYJg/view?usp=sharing)
  
   #### Platform PC Operator GUI

   [3D INTERFACE DEMO VIDEO](https://drive.google.com/file/d/1NqZ_JTVdCaxA32IgvhgPbMnpfuTEIJsR/view?usp=sharing)
  
### ALGORITHM

  ![ALGORITHM](https://github.com/dtdinidu7/e16-3yp-obstacle-bots-for-swarm-robots/blob/master/docs/img/rusiru.gif?raw=true)
  
  ![THEORY](https://github.com/dtdinidu7/e16-3yp-obstacle-bots-for-swarm-robots/blob/master/docs/img/algo.jpg?raw=true)
  
### TESTING
  
   #### Algorithm Deployment

   [Algorithm Deployment Video](https://drive.google.com/file/d/18J7mnoRWbKy1-WM-fGOGq0C8-KU52HCJ/view?usp=sharing)
  
   #### Web Interface Authentication And Authorization Testing

   [Web Interface Testing Video](https://drive.google.com/file/d/12DfR7rRFpMq2U1c6BGW0rHfQw0c6rsvO/view?usp=sharing)
  
   #### Hardware Testing

   [Hardware Testing Video](https://drive.google.com/file/d/1UNAkzgOKk-umYvnypkwuJJWv3zXbf69Z/view?usp=sharing)
  
### BUDGET
  ![BUDGET](https://github.com/dtdinidu7/e16-3yp-obstacle-bots-for-swarm-robots/blob/master/docs/img/budget.png?raw=true)

### FINAL DEMO VIDEO
  [Final Demo Video](https://drive.google.com/file/d/1B5mBls3YdkssftkCu0zrgztlk1W86l-X/view?usp=sharing)
  
### FUTURE IMPROVEMENT
  We plan to run all the algorithms first and then send the data to the robots.
  
  We have to further tune the parameters  to get a smooth process.
  
