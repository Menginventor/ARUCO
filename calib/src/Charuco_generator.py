
import cv2, PIL, os
from cv2 import aruco

import matplotlib.pyplot as plt
import matplotlib as mpl

workdir = "board/"
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)



squaresX = 7#number of chessboard squares in X direction
squaresY = 5#number of chessboard squares in Y direction
squareLength = 0.04 #chessboard square side length (normally in meters)
markerLength = 0.03 #marker square side length (normally in meters)
printer_DPI = 72
meter_to_inch = 39.3700787
board = aruco.CharucoBoard_create(squaresX, squaresY,squareLength,  markerLength, aruco_dict)


board_width_meter = (board.getChessboardSize()[0])*board.getSquareLength()
board_height_meter = (board.getChessboardSize()[1])*board.getSquareLength()
board_width_pixel= int(board_width_meter*meter_to_inch*printer_DPI)
board_height_pixel = int(board_height_meter*meter_to_inch*printer_DPI)
print('board size = ',board_width_meter,board_height_meter,'meters')
print('board size = ',board_width_pixel,board_height_pixel,'pixels')
imboard = board.draw( (board_width_pixel,board_height_pixel) )
cv2.imwrite(workdir + "chessboard.tiff", imboard)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.imshow(imboard, cmap = mpl.cm.gray, interpolation = "nearest")
ax.axis("off")
plt.show()