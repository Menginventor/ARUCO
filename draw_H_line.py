import cv2
from cv2 import aruco
import yaml
import csv
import numpy as np

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
markerLength = 0.15
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()
print(w,h)
with open('test.csv', 'w', newline='') as csvfile:
    fieldnames = ['x1','y1','z1','x2','y2','z2']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        aruco.drawDetectedMarkers(frame, corners,ids)

        index_id_0 = None
        index_id_1 = None
        for i in range(len(corners)):
            if ids[i][0] == 0 :
                index_id_0 = i
            elif ids[i][0] == 1 :
                index_id_1 = i

        for i in range(len(corners)):
            if ids[i][0] == 0 or ids[i][0] == 1:
                # aruco.drawAxis(frame, newcameramtx, dist, rvec, tvec, 0.05)
                rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners[i], markerLength, newcameramtx, dist)



                #rmat = np.zeros((3, 3))
                #cv2.Rodrigues(rvec,rmat)
                #print(rmat)
                #[[[-0.0472865  -0.04246176  1.37027699]]]


        if index_id_0 != None and index_id_1 != None:

            rvec1, tvec1, obj1 = aruco.estimatePoseSingleMarkers(corners[index_id_0], markerLength, newcameramtx, dist)
            rvec2, tvec2, obj2 = aruco.estimatePoseSingleMarkers(corners[index_id_1], markerLength, newcameramtx, dist)
            Horizontal = np.float32([[-1, 0, 0], [1, 0, 0]])
            rmat1 = np.zeros((3, 3))
            cv2.Rodrigues(rvec1, rmat1)
            rmat1 = np.transpose(rmat1)
            Horizontal_offset = np.float32([[-1, 0.075, 0], [1, 0.075, 0]])

            imgpts1, jac1 = cv2.projectPoints(Horizontal_offset, rvec1, tvec1, mtx, (0, 0, 0, 0))
            imgpts1 = np.int32(imgpts1).reshape(-1, 2)
            cv2.line(frame, tuple(imgpts1[0]), tuple(imgpts1[1]), (255, 0, 0), 1)
            ####
            imgpts2, jac2 = cv2.projectPoints(Horizontal, rvec1, tvec2, mtx, (0, 0, 0, 0))
            imgpts2 = np.int32(imgpts2).reshape(-1, 2)
            cv2.line(frame, tuple(imgpts2[0]), tuple(imgpts2[1]), (255, 0, 0), 1)
            ####
            relate_tvec = np.matmul(rmat1, np.subtract(tvec2[0][0], tvec1[0][0]))
            ####
            Vertical = np.float32([[0, 0, 0], relate_tvec])
            #Vertical = np.float32([[0, 0, 0], [0, relate_tvec[1], 0]])
            imgpts2, jac2 = cv2.projectPoints(Vertical, rvec1, tvec1, mtx, (0, 0, 0, 0))
            imgpts2 = np.int32(imgpts2).reshape(-1, 2)
            cv2.line(frame, tuple(imgpts2[0]), tuple(imgpts2[1]), (255, 0, 0), 1)

            ####
            #writer.writerow({'x1': relate_tvec[0],'y1': relate_tvec[1],'z1': relate_tvec[2]})
            writer.writerow({'x1': tvec2[0][0][0], 'y1': tvec2[0][0][1], 'z1': tvec2[0][0][2]})

            ##

        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()