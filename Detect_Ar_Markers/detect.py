import cv2

cam = cv2.VideoCapture(0)

#Load the dictionary that was used to generate the markers.
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

# Initialize the detector parameters using default values
parameters =  cv2.aruco.DetectorParameters_create()

while True:
    ret, frame = cam.read()
    cv2.imshow('Cam', frame)

    # Detect the markers in the image8
    markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
    print(markerIds)

    if (cv2.waitKey(1) == ord('q')):
        break

cam.release()
cv2.destroyAllWindows()