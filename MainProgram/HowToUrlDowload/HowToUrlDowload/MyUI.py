import sys
import urllib.request
import datetime
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

<<<<<<< HEAD
=======
>>>>>>> kim
=======


>>>>>>> parent of 90cae96... ui method setting
=======

>>>>>>> parent of 4a21663... DB에서 문자 받고 넣는거 넣음
=======

>>>>>>> parent of 62d1ba7... Merge branch 'kim'
form_class = uic.loadUiType("0625_DBUI.ui")[0]

class DemoForm(QMainWindow, form_class):
    #생성자
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.dblistview.setHeaderLabels(["TIME", "LOG"])
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> parent of 62d1ba7... Merge branch 'kim'
        self.dblistview = self.dblistview.invisibleRootItem()

       # self.SubmitBtn.clicked.connect(self.SubmitbtnEvent)
        self.okbtn.clicked.connect(self.OkbtnEvent)
        self.cancelbtn.clicked.connect(self.CancelBtnEvent)
        self.checkbtn.clicked.connect(self.CheckBtnEvent)
<<<<<<< HEAD
        self.getlogButton.clicked.connect(self.GetLog)
        #데이터 가져오기
        self.datalog = "nothing"
<<<<<<< HEAD
=======
        self.dblistview = self.dblistview.invisibleRootItem()       #리스트뷰 설정하는 2줄

        self.okbtn.clicked.connect(self.OkbtnEvent)                 #버튼 누르면 지정 텍스트 리스트뷰에 추가
        self.cancelbtn.clicked.connect(self.CancelBtnEvent)         #버튼 누르면 프로그램 종료
        self.Addtargetbtn.clicked.connect(self.AddTargetBtnEvent)         #버튼 누르면 새로운 Dialog창
>>>>>>> kim
=======
        self.dblistview = self.dblistview.invisibleRootItem()

       # self.SubmitBtn.clicked.connect(self.SubmitbtnEvent)
        self.okbtn.clicked.connect(self.OkbtnEvent)
        self.cancelbtn.clicked.connect(self.CancelBtnEvent)
        self.checkbtn.clicked.connect(self.CheckBtnEvent)
>>>>>>> parent of 90cae96... ui method setting
=======
>>>>>>> parent of 4a21663... DB에서 문자 받고 넣는거 넣음

    #Log url 넣으면 Log 문장을 String으로 반환하는 함수
    def downloadlocaltime(self,url):
        data = urllib.request.urlopen(url).read()
        return str(data)
=======

    def SubmitbtnEvent(self):
>>>>>>> parent of 62d1ba7... Merge branch 'kim'

    def SubmitbtnEvent(self):
        db = mysql.connector.connect(host='192.168.137.1',port='3306' ,user='bit27_1', password='123123',database='bit27_db',charset='utf8mb4')
        cursor = db.cursor()
        
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> parent of 62d1ba7... Merge branch 'kim'

            add_log = "INSERT INTO datatable (datalog) VALUES ('" +self.datalogchange+ "')"
            cursor.execute(add_log)
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
>>>>>>> parent of 4a21663... DB에서 문자 받고 넣는거 넣음
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
<<<<<<< HEAD
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
<<<<<<< HEAD
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
            return
        else:
            myTime = str(datetime.datetime.now())
            textforlist = self.textbox1.text()

            item = QTreeWidgetItem()
            item.setText(0, myTime)
            item.setText(1, textforlist)
<<<<<<< HEAD
            self.dblistview.addChild(item)                                      #집어 넣는데 setText(컬럼번호, 내용) 유의하자
>>>>>>> kim
=======
            self.dblistview.addChild(item)
>>>>>>> parent of 90cae96... ui method setting
=======
>>>>>>> parent of 4a21663... DB에서 문자 받고 넣는거 넣음

    def CancelBtnEvent(self):
        sys.exit()

=======

    def CancelBtnEvent(self):
        sys.exit()


    def CheckBtnEvent(self):
        pass
>>>>>>> parent of 62d1ba7... Merge branch 'kim'

    def CheckBtnEvent(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoWindow = DemoForm()
    demoWindow.show() 
    app.exec_()