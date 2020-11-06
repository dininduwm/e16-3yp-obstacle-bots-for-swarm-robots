import numpy as np
import cv2


class ex:
  
    def __init__(self,a,b):
        self.a = a
        self.b = b
l = list()
for i in range(10):
    l.append(ex(i, i+3))
print([s.a  for s in l])
