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
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.dblistview.setHeaderLabels(["TIME", "LOG"])
        self.dblistview = self.dblistview.invisibleRootItem()
        
        #self.SubmitBtn.clicked.connect(self.SubmitbtnEvent)

        self.deletealloflogButton.clicked.connect(self.DeleteAllofLog)
        self.cancelbtn.clicked.connect(self.CancelBtnEvent)
        self.checkbtn.clicked.connect(self.CheckBtnEvent)
        self.getlogButton.clicked.connect(self.GetLog)
        #실시간 true된 로그 가져오기위한 변수
        self.datalog = "nothing"

    #디비에 트루 로그 넣기
    def SubmitbtnEvent(self):

        self.datalog = self.downloadlocaltime("http://100.100.80.52:5000/findPerson")
        self.dsa = self.datalog[2:6]
        self.datalogchange = self.datalog[7:29]
        print(self.dsa)
        
        #true일 경우에만 저장
        if(self.dsa == "True"):
            db = mysql.connector.connect(host='192.168.137.1',port='3306' ,user='bit27_1', password='123123',database='bit27_db',charset='utf8mb4')
            cursor = db.cursor()
        

            add_log = "INSERT INTO datatable (datalog) VALUES ('" +self.datalogchange+ "')"
            cursor.execute(add_log)
            db.commit()
            cursor.close()
            db.close()
        else:
            return
        print("DB에 저장 완료")

    # 모든로그 다 보여줌
    def GetLog(self):
        # 접속
        db = mysql.connector.connect(host='192.168.137.1',port='3306' ,user='bit27_1', password='123123',database='bit27_db',charset='utf8')

        # 커서 가져오기 (cursor 는 control structure of database 입니다. (연결된 객체라는데 잘모름))
        cursor1 = db.cursor()

        #데이터 출력
        show_log = "SELECT * FROM datatable"  
            
        cursor1.execute(show_log)

        #add_log에 대한 결과값 가져오기
        self.row = cursor1.fetchone()
        logs = []

        while self.row is not None:
           #print(self.row)
            logs.append(self.row)
            self.row = cursor1.fetchone()

        for i in logs:
            #print(i)
            #i = "why"
            self.row = cursor1.fetchone()
            myTime = str(datetime.datetime.now())
           
            item = QTreeWidgetItem()
            item.setText(0, myTime)
            item.setText(1, str(i))
            self.dblistview.addChild(item)
            self.row = cursor1.fetchone()

        cursor1.close()
        db.close()
        print("전체로그 출력 완료")

    #모든 로그 삭제
    def DeleteAllofLog(self):
            # 접속
            db = mysql.connector.connect(host='192.168.137.1',port='3306' ,user='bit27_1', password='123123',database='bit27_db',charset='utf8mb4')
            
            # 커서 가져오기 (cursor 는 control structure of database 입니다. (연결된 객체라는데 잘모름))
            cursor = db.cursor()
        
            #데이터 지우기 
            deleteall_log = "DELETE FROM datatable"

            cursor.execute(deleteall_log)

            db.commit()

            cursor.close()
            db.close()
            print("전체 삭제 완료")


    def CancelBtnEvent(self):
        sys.exit()


    def CheckBtnEvent(self):
        pass

    #Log url 넣으면 Log 문장을 String으로 반환하는 함수
    def downloadlocaltime(self,url):
        data = urllib.request.urlopen(url).read()
        return str(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoWindow = DemoForm()
    demoWindow.show() 
    app.exec_()