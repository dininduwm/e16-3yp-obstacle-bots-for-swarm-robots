import math
from robot import robot

def getDistance(robot1, robot2):

    # get the distance between the robot1 and robot2
    x1 = robot1.init_pos[0]
    y1 = robot1.init_pos[1]

    x2 = robot2.init_pos[0]
    y2 = robot2.init_pos[1]

    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    

def getForce(robot1, robot2, dest_flag = False, k = 15):
    
    # return the resultant force and the angle
    # of the force from robot2 on robot1

    # The const. k needs to be difined by the user

    x1 = robot1.init_pos[0]
    y1 = robot1.init_pos[1]

    x2 = robot2.init_pos[0]
    y2 = robot2.init_pos[1]

    x_diff = (x2 - x1)
    y_diff = (y2 - y1)

    # calculate the magnitude
    dist = getDistance(robot1, robot2)

    
    if dest_flag:
        force = (dist) / k if (dist) else 0
    else:
        force = 1 / (k * ((dist) ** 5)) if (dist) else 0
    
    # calculate the angle
    if (x1 == x2): return [force, 90.00]
    
    angle = math.degrees(math.atan(abs(y1 - y2) / abs(x1 - x2)))

    if (x_diff > 0 and y_diff > 0):
        # 0 to 90 degrees
        pass
    elif (x_diff < 0 and y_diff > 0):
        # 90 to 180 degrees
        angle = 180 - angle
    elif (x_diff > 0 and y_diff < 0):
        # 270 to 360 degrees
        angle = - angle
    elif (x_diff < 0 and y_diff < 0):
        # 180 to 270 degrees
        angle = -(180 - angle)
    
    return [force, angle] 

def calculateResultant(Forces):
    ''' 
        function takes the Forces list one the point
        and calculate the resultant force and direction
    '''
    import resaltant
    # print("Forces: ", Forces)
    return resaltant.getResultant(Forces)


def getResultant(robots_data, idx):
    ''' 
        function takes the index of the robot and 
        return the resultant force on that robot
    '''
    Forces = []

    for i in range(len(robots_data)):

        """ calculate the forces from other robots """

        if i != idx:
            Forces.append(getForce(robots_data[i], robots_data[idx]))

        """ calculate the Forces from boundaries"""

        # 1 / 4. pi . epsilon replacement factor
        k = 15

        #cordinate of the current robot
        x_coord = robots_data[idx].init_pos[0]
        y_coord = robots_data[idx].init_pos[1]
        
        # initialize the board dimensions
        board_width = 30
        board_hight = 30

        # distances, angles to each board sides
        distances = [board_width - x_coord, y_coord, x_coord, board_hight - y_coord]
        angles = [180.0, 90.0, 0.0, -90.0]

        for j in range(4):
            force = 1 / (k * ((distances[j]) ** 25)) if (distances[j]) else 0
            Forces.append([force, angles[j]])

    # calculate the Force for destination
    destination_robot = robot(robots_data[idx].des_pos, robots_data[idx].des_angle, -1, -1)
    Forces.append(getForce(robots_data[idx], destination_robot, True, 1000))
    # give a magnitude factor to to destination force
    # Forces[-1][0] *= len(robots_data)

    return calculateResultant(Forces)

    


