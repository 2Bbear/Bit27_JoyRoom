import sys
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

form_class = uic.loadUiType("0625_DBUI.ui")[0]

class DemoForm(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.submitbtn.clicked.connect(self.SubmitbtnEvent)
        self.checkbtn.clicked.connect(self.CheckbtnEvent)

    def SubmitbtnEvent(self):

        db = mysql.connector.connect(host='192,168,137,1',port='3306' ,user='bit27', password='123123',database='bit27_db',charset='utf8mb4')
        cursor = db.cursor()
        
        if(self.textbox1.text() == ""):
            submitdata = "내용이 없습니다."
        else:
            submitdata = self.textbox1.text()
            add_log = "INSERT INTO data (datalog) VALUES ('"+submitdata+"')"

        cursor.execute(add_log)
        db.commit()

        cursor.close()
        db.close()

    def CheckbtnEvent(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoWindow = DemoForm()
    demoWindow.show() 
    app.exec_()