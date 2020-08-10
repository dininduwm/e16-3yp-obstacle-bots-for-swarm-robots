from math import atan, sqrt

def positions(start_x, start_y, start_gradient, end_x, end_y, end_gradient):
    # calculate the required gradient
    required_gradient = (end_y - start_y) / (end_x - start_y)
    # calculate the start angle 
    start_angle = atan(start_y / start_x)
    # calculate the end angle of the robot
    end_angle = atan(end_y / end_x)
    # calculate howmany degrees does the robot turn at the beginning
    start_turn = atan(required_gradient) - start_angle
    # calculate howfar does the robot should move
    distance = sqrt(pow((end_y - start_y), 2) + pow((end_x - start_y), 2))
    # calculate howmany degrees does the robot turn at the end
    end_turn = end_angle - start_turn

    return (start_turn, distance, end_turn)

