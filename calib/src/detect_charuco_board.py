import cv2, PIL, os
from cv2 import aruco

import matplotlib.pyplot as plt
import matplotlib as mpl
workdir = 'calib_pic/'
images = [workdir + f for f in os.listdir(workdir) ]
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

####
squaresX = 7#number of chessboard squares in X direction
squaresY = 5#number of chessboard squares in Y direction
squareLength = 0.04 #chessboard square side length (normally in meters)
markerLength = 0.03 #marker square side length (normally in meters)
printer_DPI = 72
meter_to_inch = 39.3700787
board = aruco.CharucoBoard_create(squaresX, squaresY,squareLength,  markerLength, aruco_dict)
###
img = cv2.imread(images[0])
print(images[0])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
corners, ids, _ = aruco.detectMarkers(
            image=gray,
dictionary=aruco_dict)
img = aruco.drawDetectedMarkers(image=img, corners=corners)
response, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
            markerCorners=corners,
            markerIds=ids,
            image=gray,board=board)
img = aruco.drawDetectedCornersCharuco(
                image=img,
                charucoCorners=charuco_corners,
                charucoIds=charuco_ids)
print('found ',response,'edge')

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
