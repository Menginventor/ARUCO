import cv2, PIL, os
from cv2 import aruco
import numpy as np
import yaml
workdir = 'calib_pic/'
images_dirs = [workdir + f for f in os.listdir(workdir) ]
images = [cv2.imread(images_dir) for images_dir in images_dirs]

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
###
minimum_detection = 4
###

def read_charuco(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = aruco.detectMarkers(
                image=gray,
    dictionary=aruco_dict)


    response, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
                markerCorners=corners,
                markerIds=ids,
                image=gray,board=board)
    img = aruco.drawDetectedMarkers(image=img, corners=corners)
    img = aruco.drawDetectedCornersCharuco(image=img, charucoCorners=charuco_corners,charucoIds=charuco_ids,cornerColor =(255,0,0))
    print('found ',response,'edge')

    return response,charuco_corners,charuco_ids,img
def read_all_charuco(imgs):
    allCorners = []
    allIds = []
    for i in range(len(imgs)):
        img = imgs[i]
        response, charuco_corners, charuco_ids,img_marker = read_charuco(img)


        cv2.imwrite('calib_detect/img_detect'+str(i)+'.png',img_marker)
        if response>= minimum_detection:
            allCorners.append(charuco_corners)
            allIds.append(charuco_ids)
    gray = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    imsize = gray.shape
    return allCorners, allIds, imsize

def calibrate_camera(allCorners,allIds,imsize):
    """
    Calibrates the camera using the dected corners.
    """
    print("CAMERA CALIBRATION")

    cameraMatrixInit = np.array([[ 2000.,    0., imsize[0]/2.],
                                 [    0., 2000., imsize[1]/2.],
                                 [    0.,    0.,           1.]])

    distCoeffsInit = np.zeros((5,1))
    flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL)
    retval, cameraMatrix, distCoeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(
        charucoCorners=allCorners,
        charucoIds=allIds,
        board=board,
        imageSize=imsize,
        cameraMatrix=None,
        distCoeffs=None)

    return retval, cameraMatrix, distCoeffs, rvecs, tvecs

allCorners,allIds,imsize = read_all_charuco(images)
retval, cameraMatrix, distCoeffs, rvecs, tvecs = calibrate_camera(allCorners,allIds,imsize)

calib_data = dict(cameraMatrix=cameraMatrix,distCoeffs=distCoeffs)
with open('calib_data.yml', 'w') as outfile:
    yaml.dump(calib_data, outfile, default_flow_style=False)
print(cameraMatrix)
print(distCoeffs)