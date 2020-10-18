import cv2
import numpy as np

img = cv2.imread('/home/heshds/Academics/project/e16-3yp-obstacle-bots-for-swarm-robots/simulator/resources/grid2.jpg')
logo = cv2.imread('/home/heshds/Academics/project/e16-3yp-obstacle-bots-for-swarm-robots/simulator/resources/logo.png',cv2.IMREAD_UNCHANGED)
img = cv2.resize(img, (1000,1000))
logo = cv2.resize(logo, (100,100))

logo_alpha = logo[:,:,3]

img_H, img_W, _ = img.shape
png_H, png_W, _ = logo.shape
x,y = 200,200
f = 1
r = 5
t = 0
while True:
    x = int(np.sin(2*3.17*f*t)*r )+x
    y = int(np.cos(2*3.17*f*t)*r )+ y  
    t = t+1
    overlay = np.zeros((img_H, img_W,3),dtype="uint8")
    overlay[x:x+png_H ,y:y+png_W] = logo[:,:,:3]
    mask = np.zeros((img_H, img_W),dtype="uint8")
    mask[x:x+png_H ,y:y+png_W] = logo_alpha
    mask = cv2.bitwise_not(mask)

    masked = cv2.bitwise_and(img,img,mask = mask) 
    out = cv2.add(overlay,masked)
    
    cv2.imshow('test', out)
    
    key = cv2.waitKey(5)
    if key == 27:
        break