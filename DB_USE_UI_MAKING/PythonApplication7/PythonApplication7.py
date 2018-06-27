import sys
import cv2
import datetime
import mysql.connector
import threading

from scipy.ndimage import imread
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

mainform_class = uic.loadUiType("0625_DBUI.ui")[0]
subform_class = uic.loadUiType("0626_DATE_LOAD_UI.ui")[0]

class Dialog2(QDialog, subform_class):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.takelogbtn.clicked.connect(self.takelog)

    def takelog(self):
        sys.exit()
        

class DemoForm(QMainWindow, mainform_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.dblistview.setHeaderLabels(["TIME", "LOG"])
        self.dblistview = self.dblistview.invisibleRootItem()
        
        self.SubmitBtn.clicked.connect(self.SubmitbtnEvent)
        self.okbtn.clicked.connect(self.OkbtnEvent)
        self.cancelbtn.clicked.connect(self.CancelBtnEvent)
        
        self.cam1.mousePressEvent = self.click
        self.cam1stop.clicked.connect(self.StopCam)
        self.recstart.clicked.connect(self.REC_Start)

        self.actionLog_check.triggered.connect(self.showlog)
#==============================================================================================================================================DB에 데이터보내고 받아오기(받아오기는 아직 안가져오메)
    def SubmitbtnEvent(self):

        db = mysql.connector.connect(host='192.168.137.1',port='3306' ,user='bit27_1', password='123123',database='bit27_db',charset='utf8mb4')
        cursor = db.cursor()
        
        if(self.textbox1.text() == ""):
            return
        else:
            submitdata = self.textbox1.text()
            add_log = "INSERT INTO datatable (datalog) VALUES ('"+submitdata+"')"

        cursor.execute(add_log)
        db.commit()
        self.textbox1.text = ""
        cursor.close()
        db.close()

    def OkbtnEvent(self):
        if(self.textbox1.text() == ""):
            return
        else:
            myTime = str(datetime.datetime.now())
            textforlist = self.textbox1.text()

            item = QTreeWidgetItem()
            item.setText(0, myTime)
            item.setText(1, textforlist)
            self.dblistview.addChild(item)

    def CancelBtnEvent(self):
        sys.exit()
    #====================================================================================================영상 시작 및 일시정지/다시재생
    def click(self , no_use_value): #라벨에 있는 화면 크기 키우려면 밑에 사이즈 조절 해주면 된다.
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)
    
    def update_frame(self):
        ret, self.image = self.capture.read()
        self.image = cv2.flip(self.image, 1)
        self.displayImage(self.image, 1)

    def displayImage(self, img, window):
        qformat = QImage.Format_Indexed8
        if(len(img.shape)==3):
            if(img.shape[2] == 4):
                qformat = Qimage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        outimage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outimage = outimage.rgbSwapped()

        if(window==1):
            self.cam1.setPixmap(QPixmap.fromImage(outimage))
            self.cam1.setScaledContents(True)

    def StopCam(self):
        if(self.cam1stop.text() == 'll'):
            self.timer.stop()
            self.cam1stop.setText('▶')
        else:
            self.timer.start()
            self.cam1stop.setText('ll')
    #========================================================================영상 저장
    def REC_Start(self):#영상 저장 하려면 와일 돌려야 함? 지금 0초인데
        fourcc = cv2.VideoWriter_fourcc('D','I','V','X')
        out = cv2.VideoWriter('output.avi',fourcc, 20.0, (320,240))
        out.write(self.image)
        self.count = 0
        self.showrectimer = QTimer(self)
        self.showrectimer.timeout.connect(self.start_timer)
        self.showrectimer.start(1000)

    def start_timer(self):
        self.count += 1
        self.rectimer.setText(str(self.count))

    #========================================================================모달 띄워서 DB에 있는 정보 불러오기
    def showlog(self):
        dlg = Dialog2()
        dlg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoWindow = DemoForm()
    demoWindow.show()
    app.exec_()