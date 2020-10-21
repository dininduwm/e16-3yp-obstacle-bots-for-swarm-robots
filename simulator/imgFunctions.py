import cv2
import numpy as np




""" loads the back ground image with the desired grid size """
def loadBackground(girdSize, WINDOW_SIZE):
    # TODO - handle errors
    Orig = cv2.imread('/home/heshds/Academics/semester5/PROJECT/e16-3yp-obstacle-bots-for-swarm-robots/simulator/resources/simbot_back.jpg')
    limit = int(girdSize*Orig.shape[0]/30)
    cropped = Orig[:limit, :limit]
    return cv2.resize(cropped, (WINDOW_SIZE, WINDOW_SIZE))


def loadBotImgs(girdSize, WINDOW_SIZE):
    imgs = {}
    items = ['bot', 'green', 'red', 'blue']
    bot_size = int(WINDOW_SIZE/girdSize)
    for item in items:
        img = cv2.imread('simulator/resources/simbot_%s.png'%item, cv2.IMREAD_UNCHANGED)   
        img = cv2.resize(img, (bot_size, bot_size))
        imgs[item] = img
    return imgs


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result
