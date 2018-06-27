import sys
import urllib.request
import datetime
import mysql.connector
import cv2
import HistoryLogUI as hisui
import AddTarget as at

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
<<<<<<< HEAD

=======
>>>>>>> kim
form_class = uic.loadUiType("0625_DBUI.ui")[0]

class DemoForm(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)                                          #UI는 이걸로 한다라는 2줄
        
        self.dblistview.setHeaderLabels(["TIME", "LOG"])
<<<<<<< HEAD
        self.dblistview = self.dblistview.invisibleRootItem()
        
        #self.SubmitBtn.clicked.connect(self.SubmitbtnEvent)

        #self.deletealloflogButton.clicked.connect(self.DeleteAllofLog)
        self.cancelbtn.clicked.connect(self.CancelBtnEvent)
        self.checkbtn.clicked.connect(self.CheckBtnEvent)
        self.getlogButton.clicked.connect(self.GetLog)
        #데이터 가져오기
        self.datalog = "nothing"
=======
        self.dblistview = self.dblistview.invisibleRootItem()       #리스트뷰 설정하는 2줄

        self.okbtn.clicked.connect(self.OkbtnEvent)                 #버튼 누르면 지정 텍스트 리스트뷰에 추가
        self.cancelbtn.clicked.connect(self.CancelBtnEvent)         #버튼 누르면 프로그램 종료
        self.Addtargetbtn.clicked.connect(self.AddTargetBtnEvent)         #버튼 누르면 새로운 Dialog창
>>>>>>> kim

        self.cam1.mousePressEvent = self.click                      #cam1이라는 이름을 가진 라벨을 누르면 이벤트 발생
        self.actionLog_check.triggered.connect(self.ShowHistoryLog)        #메뉴에서 Log_Check 눌렀을때 이벤트 발생

    
    #이 함수는 QTDESIGER안에서 함수를 호출하므로 init에 없다
    def SubmitbtnEvent(self):

        self.datalog = self.downloadlocaltime("http://100.100.80.52:5000/findPerson")
        self.dsa = self.datalog[2:6]
        self.datalogchange = self.datalog[7:29]
        print(self.dsa)
        if(self.dsa == "True"):
            db = mysql.connector.connect(host='192.168.137.1',port='3306' ,user='bit27_1', password='123123',database='bit27_db',charset='utf8mb4')
            cursor = db.cursor()
        
<<<<<<< HEAD

            add_log = "INSERT INTO datatable (datalog) VALUES ('" +self.datalogchange+ "')"
            cursor.execute(add_log)
            db.commit()
            cursor.close()
            db.close()
        else:
            return


    # 모든거 다 보여줌
    def GetLog(self):
        # 접속
        db = mysql.connector.connect(host='192.168.137.1',port='3306' ,user='bit27_1', password='123123',database='bit27_db',charset='utf8')

        # 커서 가져오기 (cursor 는 control structure of database 입니다. (연결된 객체라는데 잘모름))
        cursor1 = db.cursor()

        print("정보 출력")

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

    def DeleteAllofLog(self):
            # 접속
            db = mysql.connector.connect(host='192.168.137.1',port='3306' ,user='bit27_1', password='123123',database='bit27_db',charset='utf8mb4')
            print("시작시작")
            # 커서 가져오기 (cursor 는 control structure of database 입니다. (연결된 객체라는데 잘모름))
            cursor = db.cursor()
        
            #데이터 지우기 
            deleteall_log = "DELETE FROM datatable"

            cursor.execute(deleteall_log)

            db.commit()

            cursor.close()
            db.close()
=======
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
            return                                                              #텍스트 없으면 안넣음
        else:
            myTime = str(datetime.datetime.now())                               #현재시간인데 소수점이 어마어마 함
            textforlist = self.textbox1.text()

            item = QTreeWidgetItem()                                            #리스트에 넣을 타입하나 만들어주고
            item.setText(0, myTime)
            item.setText(1, textforlist)
            self.dblistview.addChild(item)                                      #집어 넣는데 setText(컬럼번호, 내용) 유의하자
>>>>>>> kim

    def CancelBtnEvent(self):
        sys.exit()                                                              #프로그램 종료

    
    #현재는 imshow로 이미지만 보여주지만 Dialog만들어서 라벨에 크게띄우고 버튼도 만들어야 겠다
    def click(self , no_use_value):
        img = cv2.imread("beautiful.jpg")
        img = cv2.resize(img,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
        cv2.imshow("example", img)

    def ShowHistoryLog(self):
        dlg = hisui.HisTory_Log_Show()       #다른 파일에 있는 class이므로 잘 써주자
        dlg.exec_()

    def AddTargetBtnEvent(self):
        dlg = at.Add_Target_Image()       #다른 파일에 있는 class이므로 잘 써주자
        dlg.exec_()

    #Log url 넣으면 Log 문장을 String으로 반환하는 함수
    def downloadlocaltime(self,url):
        data = urllib.request.urlopen(url).read()
        return str(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoWindow = DemoForm()
    demoWindow.show() 
    app.exec_()