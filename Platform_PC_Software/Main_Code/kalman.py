import numpy as np
from numpy.linalg import inv
import time


class kalman:
    def __init__(self, p1, p2, p3):


        self.initT = time.time()
        self.dt = 0

        self.x = np.array([p1[0], p1[1], p2[0], p2[1], p3[0], p3[1],0, 0, 0, 0, 0, 0]).transpose()
        """x isa matrix in dimentios(12,1)-> [p1x, p1y, p2x, p2y, p3x, p3y , dp1x, dp1y, dp2x, dp2y, dp3x, dp3y]
        """

        self.y = self.x
        self.F =  np.zeros((12,12))
        self.H = np.eye(12, 12)
        self.conf = self.x
        self.R = 20*np.array([  [1,    0,     0,    0,    0,    0,    0,    0,   0,   0,   0,   0],      # covariece of the measurement
                                [0,    1,     0,    0,    0,    0,    0,    0,   0,   0,   0,   0],
                                [0,    0,     1,    0,    0,    0,    0,    0,   0,   0,   0,   0],
                                [0,    0,     0,    1,    0,    0,    0,    0,   0,   0,   0,   0],
                                [0,    0,     0,    0,    1,    0,    0,    0,   0,   0,   0,   0],
                                [0,    0,     0,    0,    0,    1,    0,    0,   0,   0,   0,   0],
                                [0,    0,     0,    0,    0,    0,  100,    0,   0,   0,   0,   0],
                                [0,    0,     0,    0,    0,    0,    0,  100,   0,   0,   0,   0],
                                [0,    0,     0,    0,    0,    0,    0,    0, 100,   0,   0,   0],
                                [0,    0,     0,    0,    0,    0,    0,    0,   0, 100,   0,   0],
                                [0,    0,     0,    0,    0,    0,    0,    0,   0,   0, 100,   0],
                                [0,    0,     0,    0,    0,    0,    0,    0,   0,   0,   0, 100]])

        self.P = np.zeros((12, 12))     #covariace of the state prediction


        self.Q = np.array([[10,    0,     0,    0,    0,    0,    0,    0,    0,    0,    0,    0],      # process noise
                           [0,   10,     0,    0,    0,    0,    0,    0,    0,    0,    0,    0],
                           [0,    0,    10,    0,    0,    0,    0,    0,    0,    0,    0,    0],
                           [0,    0,     0,   10,    0,    0,    0,    0,    0,    0,    0,    0],
                           [0,    0,     0,    0,   10,    0,    0,    0,    0,    0,    0,    0],
                           [0,    0,     0,    0,    0,   10,    0,    0,    0,    0,    0,    0],
                           [0,    0,     0,    0,    0,    0,   10,    0,    0,    0,    0,    0],
                           [0,    0,     0,    0,    0,    0,    0,   10,    0,    0,    0,    0],
                           [0,    0,     0,    0,    0,    0,    0,    0,   10,    0,    0,    0],
                           [0,    0,     0,    0,    0,    0,    0,    0,    0,   10,    0,    0],
                           [0,    0,     0,    0,    0,    0,    0,    0,    0,    0,   10,    0],
                           [0,    0,     0,    0,    0,    0,    0,    0,    0,    0,    0,   10]])

        self.K = 0  #kalman gain
        self.i = 0

    def __call__(self, p1, p2, p3, isdata):

        e = self.y - self.x
        X = np.vstack([self.y, self.x])
        try:
            V = np.cov(X.T)
            p = np.linalg.inv(V)
            D = np.sqrt(np.sum(np.dot(e, p) * e, axis=1))
            #print(V)
        except:
            #print("exeption")
            np.linalg.LinAlgError




        T = time.time()
        self.dt = (T-self.initT)
        self.initT = T

        """               p1x p1y p2x p2y p3x p3y     dp1x     dp1y     dp2x     dp2y     dp3x      dp3y """
        self.F = np.array([[1,  0,  0,  0,  0,  0, self.dt,       0,       0,       0,       0,        0],
                           [0,  1,  0,  0,  0,  0,       0, self.dt,       0,       0,       0,        0],
                           [0,  0,  1,  0,  0,  0,       0,       0, self.dt,       0,       0,        0],
                           [0,  0,  0,  1,  0,  0,       0,       0,       0, self.dt,       0,        0],
                           [0,  0,  0,  0,  1,  0,       0,       0,       0,       0, self.dt,        0],
                           [0,  0,  0,  0,  0,  1,       0,       0,       0,       0,       0,  self.dt],
                           [0,  0,  0,  0,  0,  0,       1,       0,       0,       0,       0,        0],
                           [0,  0,  0,  0,  0,  0,       0,       1,       0,       0,       0,        0],
                           [0,  0,  0,  0,  0,  0,       0,       0,       1,       0,       0,        0],
                           [0,  0,  0,  0,  0,  0,       0,       0,       0,       1,       0,        0],
                           [0,  0,  0,  0,  0,  0,       0,       0,       0,       0,       1,        0],
                           [0,  0,  0,  0,  0,  0,       0,       0,       0,       0,       0,        1]])

        #Prediction
        self.x = (self.F).dot(self.x)
        self.P = (self.F).dot(self.P).dot(self.F.transpose()) + self.Q

        if isdata:
            p1x = p1[0]
            p1y = p1[1]

            p2x = p2[0]
            p2y = p2[1]

            p3x = p3[0]
            p3y = p3[1]

            dp1x = (p1x - self.x[0]) / self.dt
            dp1y = (p1y - self.x[1]) / self.dt

            dp2x = (p2x - self.x[2]) / self.dt
            dp2y = (p2y - self.x[3]) / self.dt

            dp3x = (p3x - self.x[4]) / self.dt
            dp3y = (p3y - self.x[5]) / self.dt


            self.y = np.array([p1x, p1y, p2x, p2y, p3x, p3y, dp1x, dp1y, dp2x, dp2y, dp3x, dp3y]).transpose()
        else:
            self.y = self.x

        #Update
        try:
            self.i = inv(self.P + self.R)
        except:
            #print("exeption")
            np.linalg.LinAlgError

        self.K = (self.P).dot(self.i)
        self.conf = (self.y -self.x)
        self.x = self.x + (self.K).dot(self.conf)
        self.P = (np.eye(12, 12) - self.K).dot(self.P)
