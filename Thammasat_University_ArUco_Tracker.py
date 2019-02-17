'''
Thank for gretest code
https://github.com/TutorProgramacion/pyqt-tutorial/blob/master/10-opencv/main.py
'''
import sys
import cv2
from cv2 import aruco
import yaml
import csv
import numpy as np

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSettings

class CV_Thread(QtCore.QThread):
    cv_update_signal = pyqtSignal()
    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.parent = parent
    def __del__(self):
        self.wait()
    def run(self):
        while True:
            self.ret, self.frame = cap.read()
            self.rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

            self.frame = cv2.undistort(self.frame, mtx, dist, None, newcameramtx)

            # Our operations on the frame come here
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            h, w =   self.frame.shape[:2]
            print(h,w)
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
            aruco.drawDetectedMarkers(self.frame, corners, ids)

            index_id_0 = None
            index_id_1 = None
            for i in range(len(corners)):
                if ids[i][0] == 0:
                    index_id_0 = i

                elif ids[i][0] == 1:
                    index_id_1 = i

            self.cv_update_signal.emit()


class main_widget(QWidget):
    def cv_update(self):
        self.image = self.CV_Thread.frame
        self.displayImage()

    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.image = None
        self.label = QLabel()
        self.initUI()
        self.CV_Thread = CV_Thread(self)
        self.CV_Thread.start()
        self.CV_Thread.cv_update_signal.connect(self.cv_update)

    def initUI(self):
        self.label.setText('OpenCV Image')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.resize(1280,720)
        root = QHBoxLayout(self)
        root.addWidget(self.label)
        root.addLayout(self.create_panel())
        #self.resize(1028, 720)
    def create_panel(self):
        self.setup_btn = QPushButton('Setup', self)
        self.start_btn = QPushButton('Start', self)
        self.pause_btn = QPushButton('Pause', self)
        self.stop_btn = QPushButton('Stop', self)
        font = QtGui.QFont()
        font.setPointSize(24)

        self.setup_btn.setFont(font)
        self.start_btn.setFont(font)
        self.start_btn.setFont(font)
        self.pause_btn.setFont(font)
        self.stop_btn.setFont(font)

        ####
        self.setup_btn.clicked.connect(self.set_orientation)
        ###
        panel = QVBoxLayout(self)
        panel.addWidget(self.setup_btn)
        panel.addWidget(self.start_btn)
        panel.addWidget(self.pause_btn)
        panel.addWidget(self.stop_btn)

        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        panel.addItem(verticalSpacer)
        return panel
    def set_orientation(self):

def displayImage(self):
        size = self.image.shape
        step = self.image.size / size[0]
        qformat = QImage.Format_Indexed8
        if len(size) == 3:
            if size[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(self.image, size[1], size[0], step, qformat)
        img = img.rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(img))
        self.resize(self.label.pixmap().size())
def load_camera_calib():
    global calib_data
    with open("calib/src/calib_data.yml", 'r') as stream:
        try:
            calib_data = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    ret, frame = cap.read()
    h, w = frame.shape[:2]
    global mtx
    global dist
    mtx = calib_data['cameraMatrix']
    dist = calib_data['distCoeffs']
    global newcameramtx
    global markerLength
    global aruco_dict
    global parameters
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    markerLength = 0.15
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()
class main_window(QMainWindow):
    def __init__(self ):
        super(QMainWindow, self).__init__()
        #QMainWindow.__init__(self)
        self.initUI()
    def initUI(self):
        self.setGeometry(100, 100, 1500, 720)
        self.setWindowTitle("Thammasat University ArUco Tracker")
        self.setWindowIcon(QtGui.QIcon('py_logo.png'))
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        impMenu = QMenu('Import', self)
        imp_txt_Act = QAction('Import text file', self)
        imp_csv_Act = QAction('Import CSV file', self)
        imp_byte_Act = QAction('Import Protocol file', self)
        impMenu.addAction(imp_txt_Act)
        impMenu.addAction(imp_csv_Act)
        impMenu.addAction(imp_byte_Act)

        expMenu = QMenu('Export', self)
        exp_txt_Act = QAction('Export text file', self)
        exp_csv_Act = QAction('Export CSV file', self)
        exp_byte_Act = QAction('Export Protocol file', self)
        expMenu.addAction(exp_txt_Act)
        expMenu.addAction(exp_csv_Act)
        expMenu.addAction(exp_byte_Act)

        fileMenu.addMenu(impMenu)
        fileMenu.addMenu(expMenu)

        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
        self.main_widget = main_widget(self)
        self.setCentralWidget(self.main_widget)

    def closeEvent(self, event):
        print('clossing')
        pass


def main():
    global cap
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    load_camera_calib()

    app = QApplication(sys.argv)

    w = main_window()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

