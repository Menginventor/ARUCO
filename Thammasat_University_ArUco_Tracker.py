'''
Thank for gretest code
https://github.com/TutorProgramacion/pyqt-tutorial/blob/master/10-opencv/main.py
'''
import sys
import time
import cv2
from cv2 import aruco
import yaml
import csv
import numpy as np
import csv
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

            self.frame = cv2.undistort(self.frame, mtx, dist,None, newcameramtx)

            # Our operations on the frame come here
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
            aruco.drawDetectedMarkers(self.frame, corners, ids)

            self.index_id_0 = None
            self.index_id_1 = None
            self.ref_rvec = None
            self.ref_tvec = None
            for i in range(len(corners)):
                if ids[i][0] == 0:
                    self.index_id_0 = i

                elif ids[i][0] == 1:
                    self.index_id_1 = i

            if self.index_id_0 != None:


                rvec1, tvec1, obj1 = aruco.estimatePoseSingleMarkers(corners[self.index_id_0], markerLength, newcameramtx,(0,0,0,0))
                aruco.drawAxis(self.frame, newcameramtx, dist, rvec1, tvec1, 0.075)
                H_Line = np.float32([[-1, 0, 0], [1, 0, 0]])

                imgpts, jac = cv2.projectPoints(H_Line, rvec1, tvec1, newcameramtx, dist)
                imgpts = np.int32(imgpts).reshape(-1, 2)

                cv2.line(self.frame, tuple(imgpts[0]), tuple(imgpts[1]), (255, 0, 0), 1)
                self.ref_rvec = rvec1
            if self.index_id_1 != None:
                rvec2, tvec2, obj2 = aruco.estimatePoseSingleMarkers(corners[self.index_id_1], markerLength,
                                                                     newcameramtx, dist)
                aruco.drawAxis(self.frame, newcameramtx, dist, rvec2, tvec2, 0.075)
                if not REF_RVEC is None:
                    self.ref_tvec = np.copy(tvec2)
                    if not (REF_TVEC is None):
                        self.ref_tvec[0][0][0] = REF_TVEC[0][0][0]
                        self.ref_tvec[0][0][1] = REF_TVEC[0][0][1]
                    #print(REF_TVEC)
                    rmat1 = np.identity(3)
                    cv2.Rodrigues(REF_RVEC, rmat1)
                    rmat1 = np.transpose(rmat1)


                    upper_H_offest = np.float32([[-1, 0.05, 0], [1, 0.05, 0]])
                    lower_H_offest = np.float32([[-1, -0.05, 0], [1, -0.05, 0]])
                    imgpts_up, jac_up = cv2.projectPoints(upper_H_offest, REF_RVEC, self.ref_tvec, newcameramtx, (0,0,0,0))
                    imgpts_lw, jac_lw = cv2.projectPoints(lower_H_offest, REF_RVEC, self.ref_tvec, newcameramtx, (0,0,0,0))
                    imgpts_up = np.int32(imgpts_up).reshape(-1, 2)
                    imgpts_lw = np.int32(imgpts_lw).reshape(-1, 2)

                    cv2.line(self.frame, tuple(imgpts_up[0]), tuple(imgpts_up[1]), (0, 0, 255), 2)
                    cv2.line(self.frame, tuple(imgpts_lw[0]), tuple(imgpts_lw[1]), (0, 0, 255), 2)
                    if self.parent.running_state == 'Recording':
                        #print('recording')
                        with open('log/' + str(temp_log_filename) + '.csv', 'a', newline='') as csvfile:
                            #['time stamp', 'pos x', 'pos y', 'pos z']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            global start_time
                            crr_time = time.clock() - start_time
                            relate_tvec = np.matmul(rmat1, np.subtract(tvec2[0][0], REF_TVEC[0][0]))
                            writer.writerow({'time stamp':crr_time,'pos x': relate_tvec[0], 'pos y': relate_tvec[1], 'pos z': relate_tvec[2]})
                            print(relate_tvec)
            self.cv_update_signal.emit()

class main_widget(QWidget):
    running_state = 'Idle'
    def cv_update(self):
        self.image = self.CV_Thread.frame
        self.displayImage()
        if self.CV_Thread.index_id_0 != None:
            self.setup_btn.setEnabled(True)
        else:
            self.setup_btn.setEnabled(False)
        if self.CV_Thread.index_id_1 != None and (not REF_RVEC is None) and  self.running_state == 'Idle':
            self.start_btn.setEnabled(True)
        else:
            self.start_btn.setEnabled(False)
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
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.start_btn.setFont(font)
        self.pause_btn.setFont(font)
        self.stop_btn.setFont(font)
        ####
        self.setup_btn.clicked.connect(self.setup_oreintation)
        self.start_btn.clicked.connect(self.start_record)
        ###
        panel = QVBoxLayout(self)
        panel.addWidget(self.setup_btn)
        panel.addWidget(self.start_btn)
        panel.addWidget(self.pause_btn)
        panel.addWidget(self.stop_btn)
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        panel.addItem(verticalSpacer)
        return panel
    def setup_oreintation(self):
        print('setup!')
        global REF_RVEC
        REF_RVEC = self.CV_Thread.ref_rvec
        print(REF_RVEC)

    def start_record(self):
        print('start_record')
        self.running_state = 'Recording'
        global REF_TVEC
        REF_TVEC = self.CV_Thread.ref_tvec
        global temp_log_filename

        file_name_err = True
        while file_name_err:
            temp_log_filename = time.strftime("%d-%b-%Y-%H-%M-%S", time.localtime())
            print(temp_log_filename)
            try:
                with open('log/'+str(temp_log_filename)+'.csv', 'w', newline='') as csvfile:

                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    file_name_err = False
            except Exception as e:
                print(e)
                file_name_err = True

        global start_time
        start_time = time.clock()
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
    global REF_RVEC
    global REF_TVEC
    global temp_log_filename
    global fieldnames
    fieldnames = ['time stamp', 'pos x', 'pos y', 'pos z']
    temp_log_filename = ''
    REF_RVEC = None
    REF_TVEC = None
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
    global start_time
    load_camera_calib()
    app = QApplication(sys.argv)
    w = main_window()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

