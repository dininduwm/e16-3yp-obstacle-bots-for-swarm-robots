import cv2
import numpy as np
import random
import math
import imgFunctions as img


bots = list()
BOT_COUNT = 50
RADI = 50
GRID_SIZE = 10
dS = 3
WINDOW_SIZE = 1000  # square window, height = width


backg_H = 0
backg_W = 0 
bot_H = 0
bot_W = 0

mouse_pos = [0,0]
mouse_state = 0


def update(bots):
    if len(bots) == 0:
       for i in range(BOT_COUNT):
           bots.append([random.randint(0, backg_H), random.randint(0, backg_H), random.randint(0, 360)])
    else:
        for bot in bots:
            bot[0] = bot[0] + dS*np.cos(bot[2]*math.pi/180)
            bot[1] = bot[1] + dS*np.sin(-bot[2]*math.pi/180)
            bot[2] = bot[2] + 0.8
                



def draw_bots(bots):
    overlay = np.zeros((backg_H, backg_W,4), dtype="uint8")
    for bot in bots:
        x = bot[0]
        y = bot[1]
        angle = bot[2]
        x_start = int(x - bot_W/2)
        y_start = int(y - bot_H/2)

        x_start = 0 if (x_start<0) else ((backg_W - bot_W) if x_start>(backg_W - bot_W) else x_start)
        y_start = 0 if (y_start<0) else ((backg_H - bot_H) if y_start>(backg_H - bot_H) else y_start)

        bot_img = img.rotate_image(bot_png.copy(), angle)
        roi = overlay[ y_start:y_start+bot_W, x_start:x_start+bot_W] # region of interest
        overlay[ y_start:y_start+bot_W, x_start:x_start+bot_W] = roi + bot_img

    return overlay
        
def mosueEvent(event, x, y, flags, param):
    global mouse_pos, mouse_state
     
    mouse_pos = [x, y]
    mouse_state = event

if __name__ == "__main__":

    background = img.loadBackground(GRID_SIZE, WINDOW_SIZE) #load backgroug image according to the grid size
    bot_pngs = img.loadBotImgs(GRID_SIZE, WINDOW_SIZE)# load all pngs of the bot to a dict
    bot_png = bot_pngs['bot'] # get the bot image 
    
    backg_H, backg_W, _ = background.shape
    bot_H, bot_W, _ = bot_png.shape
    
    print(backg_H, backg_W)
    print(bot_H, bot_W)
    
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mosueEvent)


    while True:
        update(bots)
        overlay = draw_bots(bots)
        masked_backg = cv2.bitwise_and(background, background, mask = cv2.bitwise_not(overlay[:,:,3])) 
        
        finalImg = cv2.add(overlay[:,:,:3], masked_backg)

        cell_size = int(WINDOW_SIZE/GRID_SIZE)
        x_cell = int(mouse_pos[0]/cell_size)*cell_size
        y_cell = int(mouse_pos[1]/cell_size)*cell_size
        color = (125,0,100) if mouse_state == cv2.EVENT_LBUTTONDOWN else (125,255,0)
        cv2.rectangle(finalImg, (x_cell, y_cell),(x_cell+cell_size, y_cell+cell_size), color, 2)
        
        cv2.imshow('image', finalImg)
        
        key = cv2.waitKey(5)
        
        if key == 27:
            break
        elif key == 32:
            while(1):
                key = cv2.waitKey(5)
                if key == 32:
                    break