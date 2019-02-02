import cv2, PIL, os
from cv2 import aruco
import yaml
import numpy as np

workdir = 'calib_pic/'
images_dirs = [workdir + f for f in os.listdir(workdir) ]
images = [cv2.imread(images_dir) for images_dir in images_dirs]

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

img = images[3]




with open("calib_data.yml", 'r') as stream:
    try:
        calib_data = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
mtx=calib_data['cameraMatrix']
dist = calib_data['distCoeffs']

h,  w = img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
for i in range(len(images)):
# undistort
    img = images[i]
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image
    x,y,w,h = roi
    print(roi)
    #dst = dst[y:y+h, x:x+w]
    cv2.imwrite('calib_result/calib_result%d.png'%i,dst)