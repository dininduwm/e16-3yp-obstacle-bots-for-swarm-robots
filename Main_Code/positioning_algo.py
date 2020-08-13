from math import atan, sqrt

def positions(start_pos, start_angle, end_pos, end_angle):
    # calculate the required gradient
    if (end_pos[0] - start_pos[0] == 0):
        required_gradient = float('inf')
    else:
        required_gradient = (end_pos[1] - start_pos[1]) / (end_pos[0] - start_pos[0])

    # calculate the required angle
    required_angle = atan(required_gradient)#3.14159 - atan(required_gradient) if (pow(start_pos[0], 2) + pow(start_pos[1], 2) 
        #     < pow(end_pos[0], 2) + pow(end_pos[1], 2)) else atan(required_gradient)
    
    # calculate howmany degrees does the robot turn at the beginning
    start_turn = required_angle - start_angle
    # calculate howfar does the robot should move
    distance = sqrt(pow((end_pos[1] - start_pos[1]), 2) + pow((end_pos[0] - start_pos[0]), 2))
    # calculate howmany degrees does the robot turn at the end
    end_turn = end_angle - required_angle

    # neglect the small angles
    min_angle = 0.03491
    min_distance = 10
    
    start_turn = start_turn if abs(start_turn) > min_angle else 0
    end_turn = end_turn if abs(end_turn) > min_angle else 0
    distance = distance if abs(distance) > min_distance else 0

    return (round(start_turn, 4), round(distance, 4), round(end_turn, 4))


