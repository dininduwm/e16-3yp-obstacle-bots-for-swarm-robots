class robot():
    # robot class - basic information of the robot.
    def __init__(self, s_pos, s_angle, e_pos, e_angle):
        # initial position
        self.init_pos = s_pos
        self.init_angle = s_angle
        # end_position
        self.des_pos = e_pos
        self.des_angle = e_angle
        self.idle = True

