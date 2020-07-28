import numpy as np
from numpy.linalg import inv
import time


class kalman:
    def __init__(self, x, y, angle):
        self.initT = time.time()
        self.dt = 0

        self.x = np.array([x, y, angle, 0, 0, 0]).transpose()
        """x isa matrix in dimentios(8,1)-> [center x, center y, angle, dx, dy, dtheta]
        """
        self.conf = self.x
        self.y = self.x # set the initail prediction as same as the input
        self.F =  np.zeros((6, 6))
        self.H = np.eye(6, 6)

        self.R = 20*np.array([  [1,    0,     0,      0,    0,    0],        # covariece of the measurement
                                [0,    1,     0,      0,    0,    0],
                                [0,    0,     1,      0,    0,    0],
                                [0,    0,     0,    100,    0,    0],
                                [0,    0,     0,      0,  100,    0],
                                [0,    0,     0,      0,    0,  100]])

        self.P = np.zeros((6,6))     #covariace of the state prediction


        self.Q = 10*np.eye(6, 6) #process noise

        self.K = 0  #kalman gain
        self.i = 0

    def __call__(self, x, y, angle, isdata):
        """
        x      - x_cordinate
        y      - Y_cordinate
        angle  -
        isData - [True] if data is available, else [False]


        return - array of 1x6 consist of [x, y, angle, dx,dy, dtheta]
        """
        T = time.time()

        self.dt = (T-self.initT)
        self.initT = T

        """                 x   y   angle    dx         dy       dtheta   """
        self.F = np.array([[1,  0,    0, self.dt,        0,       0],
                           [0,  1,    0,       0,  self.dt,       0],
                           [0,  0,    1,       0,        0, self.dt],
                           [0,  0,    0,       1,        0,       0],
                           [0,  0,    0,       0,        1,       0],
                           [0,  0,    0,       0,        0,       1]])

        #Prediction
        self.x = (self.F).dot(self.x)
        self.P = (self.F).dot(self.P).dot(self.F.transpose()) + self.Q

        if isdata:
            dx = (x - self.x[0]) / self.dt
            dy = (y - self.x[1]) / self.dt
            dtheta = (angle - self.x[2]) / self.dt
            self.y = np.array([x, y, angle, dx, dy, dtheta]).transpose()
        else:
            self.y = self.x

        #Update
        try:
            self.i = inv(self.P + self.R)
        except:
            print("exeption")
            np.linalg.LinAlgError

        self.K = (self.P).dot(self.i)
        self.conf = (self.y -self.x)
        self.x = self.x + (self.K).dot(self.conf)
        self.P = (np.eye(6,6) - self.K).dot(self.P)

        return self.x