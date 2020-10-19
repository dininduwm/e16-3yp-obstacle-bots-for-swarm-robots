import cv2
import numpy as np
import random
import math
# postions and the angle data of robots
# bots = [[120, 500, 10],
#         [200, 600, 15],
#         [400, 202, 60],
#         [300, 100, 30],
#         [700, 300, 80]]


bots = list()
BOT_COUNT = 11
RADI = 50
dS = 3
background = cv2.imread('/home/heshds/Academics/project/e16-3yp-obstacle-bots-for-swarm-robots/simulator/resources/grid.png')
bot_png = cv2.imread('/home/heshds/Academics/project/e16-3yp-obstacle-bots-for-swarm-robots/simulator/resources/logo.png',cv2.IMREAD_UNCHANGED)


background = cv2.resize(background, (1000, 1000))
bot_png = cv2.resize(bot_png, (70,70))

backg_H, backg_W, _ = background.shape
bot_H, bot_W, _ = bot_png.shape

print(backg_H, backg_W)
print(bot_H, bot_W)


def update(bots):
    if len(bots) == 0:
       for i in range(BOT_COUNT):
           bots.append([random.randint(0, backg_H), random.randint(0, backg_H), random.randint(0, 360)])
    else:
        for bot in bots:
            bot[0] = bot[0] + dS*np.cos(bot[2]*math.pi/180)
            bot[1] = bot[1] + dS*np.sin(-bot[2]*math.pi/180)
            bot[2] = bot[2] + 0.8
                


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def draw_bots(bots):
    overlay = np.zeros((backg_H, backg_W,4), dtype="uint8")
    circles = np.zeros((backg_H, backg_W,3), dtype="uint8")
    for bot in bots:
        x = bot[0]
        y = bot[1]
        angle = bot[2]
        x_start = int(x - bot_W/2)
        y_start = int(y - bot_H/2)

        x_start = 0 if (x_start<0) else ((backg_W - bot_W) if x_start>(backg_W - bot_W) else x_start)
        y_start = 0 if (y_start<0) else ((backg_H - bot_H) if y_start>(backg_H - bot_H) else y_start)

        bot_img = rotate_image(bot_png.copy(), angle)
        overlay[ y_start:y_start+bot_W, x_start:x_start+bot_W] = bot_img
        cv2.circle(overlay, (int(x_start+ bot_W/2), int(y_start+ bot_H/2)), RADI, (255,255,0,255),1)

    return overlay
        
while True:
    update(bots)
    overlay = draw_bots(bots)
    masked_backg = cv2.bitwise_and(background, background, mask = cv2.bitwise_not(overlay[:,:,3])) 
    
    out = cv2.add(overlay[:,:,:3], masked_backg)
    cv2.imshow('test', out)
    
    key = cv2.waitKey(5)
    if key == 27:
        break


