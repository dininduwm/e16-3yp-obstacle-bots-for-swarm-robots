import cv2
import numpy as np
from math import atan
from kalman import kalman
from positioning_algo import positions  

cam = cv2.VideoCapture(0) # video source to capture images

# robot datas
robotData = {} 
robotDataSet = set()

# position dictonary to bradcast
broadcastPos = {}

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

    # current marker id set
    markerSet = set()
    
    for i in range(len(markerCorners)):
        # ploting rectangles around the markers
        pts = np.array([markerCorners[i][0][0],markerCorners[i][0][1],markerCorners[i][0][2],markerCorners[i][0][3]], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(frame,[pts],True,(0,255,255))

        # converting to center point
        conData = convert(markerCorners[i][0])
        frame = cv2.circle(frame, tuple(conData[0]), 1, (255,0,0), 2)

        # add to the marker id set
        markerSet.add(markerIds[i][0])

        # adding data to the dictionary
        if (markerIds[i][0] in robotData):
            robotData[markerIds[i][0]][0] = conData[0]
            robotData[markerIds[i][0]][1] = conData[1]

            # adding data to the kalman obj
            k_obj = robotData[markerIds[i][0]][2]       # grabbing the kalman object
            kalVal = k_obj(conData[0][0], conData[0][1] , conData[1], True)    # calculating the kalman value

        else:
            # add new key to the set
            robotDataSet.add(markerIds[i][0])

            k_obj = kalman(0, 0, 0)            # creating the kalman object
            kalVal = k_obj(conData[0][0], conData[0][1], conData[1], True) # adding data to the kalman object
            robotData[markerIds[i][0]] = [0,0,0,0]
            robotData[markerIds[i][0]][0] = conData[0]
            robotData[markerIds[i][0]][1] = conData[1]
            robotData[markerIds[i][0]][2] = k_obj   # adding kalman object to the array

        # adding data to be broadcasted
        # TODO: destination have to be changed
        broadcastPos[markerIds[i][0]] = positions(conData[0], conData[1], [0,0], 0)

    # updating the not detected objects through kalman algo
    differentSet = robotDataSet - markerSet
            
    for id in differentSet:
        k_obj = robotData[id][2]       # grabbing the kalman object
        kalVal = k_obj(0,0,0,False)    # calculating the kalman value

        # setting data to the dataset
        robotData[id][0][0] = kalVal[0]
        robotData[id][0][1] = kalVal[1]
        robotData[id][1] = kalVal[2]

        # adding data to be broadcasted
        # TODO: destination have to be changed
        broadcastPos[id] = positions([kalVal[0], kalVal[1]], kalVal[2], [0,0], 0)

    # print(robotData)
    print(broadcastPos)
    cv2.imshow('Cam', frame)

    #saving to the file
    #outVid.write(frame)

    if (cv2.waitKey(1) == ord('q')):
        break

cam.release()
#outVid.release()
cv2.destroyAllWindows()