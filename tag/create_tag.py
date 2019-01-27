import numpy as np
import cv2
from cv2 import aruco
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
marker_id = 0
marker_width_meter = 0.15#meter

printer_DPI = 72
meter_to_inch = 39.3700787
marker_width_pixel = int(marker_width_meter*meter_to_inch*printer_DPI)

img = aruco.drawMarker(	aruco_dict, marker_id, marker_width_pixel,None,1)

cv2.imwrite('marker_id%d.bmp'%marker_id,img)