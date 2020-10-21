import cv2
import numpy as np
import random
import math
import imgFunctions as img



bots = list()
BOT_COUNT = 5
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


    
#class to make a bot
class Bot:
    def __init__(self, ID):
        
        # state = -1, 0, 1 (-1:stoped, 0:success, 1:moving)
        self.state = -1 
        self.ID = ID
        # current position
        self.x = 0         
        self.y = 0
        self.angle = 0

        # destination position
        self.dest_x = 0          
        self.dest_y = 0
        self.dest_angle = 0


    def setImgs(self, imgs):
        self.bot_imgs = imgs

    def setDest(self, x, y, angle):
        self.dest_x = x 
        self.dest_y = y
        self.dest_angle = angle  

    def setPos(self, x, y, angle):
        
        # check for the overflow of the x , y values over the backgrounf image
        self.x = bot_W/2 if (x<bot_W/2) else ((backg_W - bot_W/2) if x>(backg_W - bot_W/2) else x)
        self.y = bot_H/2 if (y<bot_H/2) else ((backg_H - bot_H/2) if y>(backg_H - bot_H/2) else y)
        self.angle = angle

    
    def getState(self, bots):
        min = WINDOW_SIZE
        for i,bot in enumerate(bots):
            if self.ID != i:
                dist = math.sqrt((self.x - bot.x)*(self.x - bot.x) + (self.y - bot.y)*(self.y - bot.y))
                angle = math.atan((self.y - bot.y)/(self.x - bot.x))
                if min > dist:
                    min = dist
                
        
        if min < 100:
            self.state = -1
        else:
            self.state = 0
        

def update(bots):
    if len(bots) == 0:
       for i in range(BOT_COUNT):
           imgs = bot_pngs.copy()
           bot = Bot(i)
           bot.setPos(random.randint(0, backg_H), random.randint(0, backg_H), random.randint(0, 360))
           bot.setDest(0,0,0)
           bot.setImgs(imgs)
           bots.append(bot)
           
    else:
        for bot in bots:
            x = bot.x + (bot.state+1)*dS*np.cos(bot.angle*math.pi/180)
            y = bot.y + (bot.state+1)*dS*np.sin(-bot.angle*math.pi/180)
            angle = bot.angle + 0.8
            bot.setPos(x,y,angle)

""" draw bot images in the overlay canvas
        return : overlay(4 dims with the alpha layer)"""
def draw_bots(bots):
    overlay = np.zeros((backg_H, backg_W,4), dtype="uint8") # create a overlay layer to draw all the robots with the alpha
    for bot in bots:
        x = bot.x
        y = bot.y
        angle = bot.angle
        x_start = int(x - bot_W/2)
        y_start = int(y - bot_H/2)

        bot.getState(bots)
        # add the additional status color bar to the basic bot png
        if bot.state == 0:
            addon = bot.bot_imgs['blue']
        else:
            addon = bot.bot_imgs['red']

        bot_img = cv2.add(bot.bot_imgs['bot'], addon)        
        bot_img = img.rotate_image(bot_img, angle)
        roi = overlay[ y_start:y_start+bot_W, x_start:x_start+bot_W] # region of interest
        overlay[ y_start:y_start+bot_W, x_start:x_start+bot_W] = roi + bot_img

    return overlay
        
def mosueEvent(event, x, y, flags, param):
    global mouse_pos, mouse_state
     
    mouse_pos = [x, y]
    mouse_state = event

if __name__ == "__main__":

    backg_H, backg_W, background = img.loadBackground(GRID_SIZE, WINDOW_SIZE) #load backgroug image according to the grid size
    bot_H, bot_W, bot_pngs = img.loadBotImgs(GRID_SIZE, WINDOW_SIZE)# load all pngs of the bot to a dict
    bot_png = bot_pngs['bot'] # get the bot image 
    
    
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