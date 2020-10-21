import numpy as np
import cv2

class bot:
    
    def def __init__(self, start, dest):
        
        self.state = 0 # state = -1, 0, 1 (-1:stoped, 0:success, 1:moving)
        
        #start and destination is in (x, y, angle(rad))
        self.start = start
        self.dest = dest

      