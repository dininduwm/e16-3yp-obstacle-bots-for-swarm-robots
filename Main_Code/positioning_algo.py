from math import atan, sqrt

def positions(start_pos, start_angle, end_pos, end_angle):
    # calculate the required gradient
    required_gradient = (end_pos[1] - start_pos[1]) / (end_pos[0] - start_pos[0])
    # calculate howmany degrees does the robot turn at the beginning
    start_turn = atan(required_gradient) - start_angle
    # calculate howfar does the robot should move
    distance = sqrt(pow((end_pos[1] - start_pos[1]), 2) + pow((end_pos[0] - start_pos[0]), 2))
    # calculate howmany degrees does the robot turn at the end
    end_turn = end_angle - atan(required_gradient)

    # neglect the small angles
    min_angle = 0.03491
    min_distance = 10
    
    start_turn = start_turn if abs(start_turn) > min_angle else 0
    end_turn = end_turn if abs(end_turn) > min_angle else 0
    distance = distance if abs(distance) > min_distance else 0

    return (round(start_turn, 4), round(distance, 4), round(end_turn, 4))


