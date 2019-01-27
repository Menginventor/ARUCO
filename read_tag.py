import numpy as np
import cv2
from cv2 import aruco
import yaml

with open("calib/src/calib_data.yml", 'r') as stream:
    try:
        calib_data = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

mtx=calib_data['cameraMatrix']
dist = calib_data['distCoeffs']
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
#cap.set(cv2.CAP_PROP_EXPOSURE, 40)
ret, frame = cap.read()
h,  w = frame.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
markerLength = 0.03
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()
print(w,h)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.undistort(frame, mtx, dist, None, mtx)
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame



    # lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    aruco.drawDetectedMarkers(frame, corners,ids)

    for i in range(len(corners)):
        if ids[i][0] == 0:
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners[i], markerLength, newcameramtx, dist)

            aruco.drawAxis(frame, newcameramtx, dist, rvec, tvec, 0.05)
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()