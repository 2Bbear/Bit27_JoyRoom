import sys
import datetime
import mysql.connector
<<<<<<< HEAD

from scipy.ndimage import imread
from PyQt5 import QtWidgets, QtGui, QtCore
=======
>>>>>>> parent of 62d1ba7... Merge branch 'kim'
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

form_class = uic.loadUiType("0625_DBUI.ui")[0]

class DemoForm(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.dblistview.setHeaderLabels(["TIME", "LOG"])
        self.dblistview = self.dblistview.invisibleRootItem()
        
        self.SubmitBtn.clicked.connect(self.SubmitbtnEvent)
        self.okbtn.clicked.connect(self.OkbtnEvent)
        self.cancelbtn.clicked.connect(self.CancelBtnEvent)
        self.checkbtn.clicked.connect(self.CheckBtnEvent)
<<<<<<< HEAD
        self.cam1.mousePressEvent = self.click
=======
>>>>>>> parent of 62d1ba7... Merge branch 'kim'

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


    def CheckBtnEvent(self):
        pass
<<<<<<< HEAD

    def click(self , no_use_value):
        cam = cv2.VideoCapture(0)

        ret, frame = cam.read()

        qformat = QImage.Format_Indexed8
        if(len(frame.shape)==3):
            if(frame.shape[2] == 4):
                qformat = Qimage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        outimage = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], qformat)
        outimage = outimage.rgbSwapped()

        self.cam1.setPixmap(QPixmap.fromImage(outimage))
        self.cam1.setScaledContents(True)
=======
>>>>>>> parent of 62d1ba7... Merge branch 'kim'

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoWindow = DemoForm()
    demoWindow.show() 
    app.exec_()