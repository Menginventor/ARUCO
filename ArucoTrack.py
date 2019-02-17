from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal

import sys

import  time
import numpy as np
import cv2
from cv2 import aruco
import yaml
import csv

def load_cam_calib():
    with open("calib/src/calib_data.yml", 'r') as stream:
        try:
            global calib_data
            calib_data = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    print('load_cam_calib,successful')


class CV_Thread(QtCore.QThread):
    cv_update_signal = pyqtSignal()
    def __init__(self,parent):
        QtCore.QThread.__init__(self)
        self.parent = parent
    def __del__(self):
        self.wait()
    def run(self):
        while True:
            ret, frame = cap.read()
            self.rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, byteValue = self.rgbImage.shape
            byteValue = byteValue * width
            #print('Runing')
            self.mQImage = QImage(self.rgbImage, width, height, byteValue, QImage.Format_RGB888)
            #self.cv_update_signal.emit(self.mQImage)

class main_widget(QWidget):

    def __init__(self, parent):

        super().__init__(parent)
        self.setupUI()


    def setupUI(self):
        main_Vlayout = QVBoxLayout(self)
        self.l1 = QLabel()
        self.l1.setPixmap(QPixmap("py_logo.png"))
        main_Vlayout.addWidget(self.l1)
        self.setLayout(main_Vlayout)
        ################################


        self.CV_Thread = CV_Thread(self)
        self.CV_Thread.start()
        self.CV_Thread.cv_update_signal.connect(self.cv_update)


    def cv_update(self,image):
        print('cv_update')
        #self.l1.setPixmap(QPixmap.fromImage(image))


class main_window(QMainWindow):
    def __init__(self ):

        super(QMainWindow, self).__init__()
        #QMainWindow.__init__(self)
        self.initUI()
    def initUI(self):
        self.setGeometry(300, 300, 1280, 720)
        self.setWindowTitle("Thammasat University:ArUco Tracker")
        self.setWindowIcon(QtGui.QIcon('py_logo.png'))
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')





        editMenu = mainMenu.addMenu('Setup')
        helpMenu = mainMenu.addMenu('Help')
        self.main_widget = main_widget(self)
        self.setCentralWidget( self.main_widget)




    def closeEvent(self, event):
        print('Exit Program')
        app = QtGui.QApplication.instance()
        app.closeAllWindows()


def main():
    load_cam_calib()
    global cap
    cap = cv2.VideoCapture(0)

    app = QApplication(sys.argv)

    w = main_window()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()