import sys
import urllib.request
import datetime
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *


form_class = uic.loadUiType("0625_DBUI.ui")[0]

class DemoForm(QMainWindow, form_class):
    #생성자
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.dblistview.setHeaderLabels(["TIME", "LOG"])
        self.dblistview = self.dblistview.invisibleRootItem()

       # self.SubmitBtn.clicked.connect(self.SubmitbtnEvent)
        self.okbtn.clicked.connect(self.OkbtnEvent)
        self.cancelbtn.clicked.connect(self.CancelBtnEvent)
        self.checkbtn.clicked.connect(self.CheckBtnEvent)

    #Log url 넣으면 Log 문장을 String으로 반환하는 함수
    def downloadlocaltime(self,url):
        data = urllib.request.urlopen(url).read()
        return str(data)

    def SubmitbtnEvent(self):
        db = mysql.connector.connect(host='192.168.137.1',port='3306' ,user='bit27_1', password='123123',database='bit27_db',charset='utf8mb4')
        cursor = db.cursor()
        
        if(self.textbox1.text() != ""):
           submitdata = self.textbox1.text()
           add_log = "INSERT INTO datatable (datalog) VALUES ('"+submitdata+"')"
           cursor.execute(add_log)
           db.commit()
           cursor.close()
           db.close()
        else:
           return

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoWindow = DemoForm()
    demoWindow.show() 
    app.exec_()