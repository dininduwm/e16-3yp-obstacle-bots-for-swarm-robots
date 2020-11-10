import cv2
import numpy as np

cam = cv2.VideoCapture(0)

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
    print(markerIds)

    for i in range(len(markerCorners)):
        # ploting rectangles around the markers
        pts = np.array([markerCorners[i][0][0],markerCorners[i][0][1],markerCorners[i][0][2],markerCorners[i][0][3]], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(frame,[pts],True,(0,255,255))


    cv2.imshow('Cam', frame)

    #saving to the file
    #outVid.write(frame)

    if (cv2.waitKey(1) == ord('q')):
        break

cam.release()
#outVid.release()
cv2.destroyAllWindows()