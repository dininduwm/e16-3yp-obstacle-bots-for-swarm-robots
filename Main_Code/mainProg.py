import cv2
import numpy as np
from math import atan
import kalman

cam = cv2.VideoCapture(0) # video source to capture images

# robot datas
robotData = {} 

# finction to convert for points to center point + angle
def convert(points):
    # grabing the points
    p1 = points[0]
    p2 = points[1]
    p3 = points[2]
    p4 = points[3]

    # calculating the center point
    center = [int((p1[0]+p2[0]+p3[0]+p4[0])/4), int((p1[1]+p2[1]+p3[1]+p4[1])/4)]
    angle = atan((p1[1]-p2[1])/(p1[0]-p2[0]))

    return [center, angle]

# parameters for saving the video
frameRate = 21
dispWidth = 640
dispHeight = 480

#Load the dictionary that was used to generate the markers.
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

# Initialize the detector parameters using default values
parameters =  cv2.aruco.DetectorParameters_create()

# saving to a video
#outVid = cv2.VideoWriter('videos/recordings.avi', cv2.VideoWriter_fourcc(*'XVID'),  frameRate, (dispWidth, dispHeight))

while True:
    ret, frame = cam.read()    

    # Detect the markers in the image8
    markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)

    for i in range(len(markerCorners)):
        # ploting rectangles around the markers
        pts = np.array([markerCorners[i][0][0],markerCorners[i][0][1],markerCorners[i][0][2],markerCorners[i][0][3]], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(frame,[pts],True,(0,255,255))

        # converting to center point
        conData = convert(markerCorners[i][0])
        frame = cv2.circle(frame, tuple(conData[0]), 1, (255,0,0), 2)

        # adding data to the dictionary
        if (markerIds[i][0] in robotData):
            robotData[markerIds[i][0]][0] = conData[0]
            robotData[markerIds[i][0]][1] = conData[1]
        else:
            robotData[markerIds[i][0]] = [0,0,0,0]
            robotData[markerIds[i][0]][0] = conData[0]
            robotData[markerIds[i][0]][1] = conData[1]

    print(robotData)
    cv2.imshow('Cam', frame)

    #saving to the file
    #outVid.write(frame)

    if (cv2.waitKey(1) == ord('q')):
        break

cam.release()
#outVid.release()
cv2.destroyAllWindows()