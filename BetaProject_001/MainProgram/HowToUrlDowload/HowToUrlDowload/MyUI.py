import sys
import datetime
import mysql.connector
import cv2
import socketserver

import HistoryLogUI as hisui
import AddTarget as at
import CamDetailShow as cds

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
form_class = uic.loadUiType("0625_DBUI.ui")[0]

class DemoForm(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)                                          #UI는 이걸로 한다라는 2줄
        
        self.dblistview.setHeaderLabels(["TIME", "LOG"])
        self.dblistview = self.dblistview.invisibleRootItem()       #리스트뷰 설정하는 2줄

        self.okbtn.clicked.connect(self.OkbtnEvent)                 #버튼 누르면 지정 텍스트 리스트뷰에 추가
        self.cancelbtn.clicked.connect(self.CancelBtnEvent)         #버튼 누르면 프로그램 종료
        self.Addtargetbtn.clicked.connect(self.AddTargetBtnEvent)         #버튼 누르면 새로운 Dialog창

        self.cam1.mousePressEvent = self.click                      #cam1이라는 이름을 가진 라벨을 누르면 이벤트 발생
        self.cam2.mousePressEvent = self.click 
        self.cam3.mousePressEvent = self.click 
        self.cam4.mousePressEvent = self.click 

        self.actionLog_check.triggered.connect(self.ShowHistoryLog)        #메뉴에서 Log_Check 눌렀을때 이벤트 발생

    
    #이 함수는 QTDESIGER안에서 함수를 호출하므로 init에 없다
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
            return                                                              #텍스트 없으면 안넣음
        else:
            myTime = str(datetime.datetime.now())                               #현재시간인데 소수점이 어마어마 함
            textforlist = self.textbox1.text()

            item = QTreeWidgetItem()                                            #리스트에 넣을 타입하나 만들어주고
            item.setText(0, myTime)
            item.setText(1, textforlist)
            self.dblistview.addChild(item)                                      #집어 넣는데 setText(컬럼번호, 내용) 유의하자

    def CancelBtnEvent(self):
        item = QTreeWidgetItem()
        self.dblistview.removeChild(item)                                                           #프로그램 종료

    
    #현재는 imshow로 이미지만 보여주지만 Dialog만들어서 라벨에 크게띄우고 버튼도 만들어야 겠다
    def click(self , no_use_value):
        print(str(no_use_value))
        dlg = cds.Detail_Show()       #다른 파일에 있는 class이므로 잘 써주자
        dlg.exec_()

    def ShowHistoryLog(self):
        dlg = hisui.HisTory_Log_Show()       #다른 파일에 있는 class이므로 잘 써주자
        dlg.exec_()

    def AddTargetBtnEvent(self):
        dlg = at.Add_Target_Image()       #다른 파일에 있는 class이므로 잘 써주자
        dlg.exec_()

class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data_transferred = 0
        print('[%s] 연결됨' %self.client_address[0])
        filename = self.request.recv(1024) # 클라이언트로 부터 파일이름을 전달받음
        filename = filename.decode() # 파일이름 이진 바이트 스트림 데이터를 일반 문자열로 변환
        filename="upload/"+filename
        if not exists(filename): # 파일이 해당 디렉터리에 존재하지 않으면
            return # handle()함수를 빠져 나온다.
 
        print('파일[%s] 전송 시작...' %filename)
        with open(filename, 'rb') as f:
            try:
                data = f.read(1024) # 파일을 1024바이트 읽음
                while data: # 파일이 빈 문자열일때까지 반복
                    data_transferred += self.request.send(data)
                    data = f.read(1024)
            except Exception as e:
                print(e)
 
        print('전송완료[%s], 전송량[%d]' %(filename,data_transferred))

def ddd():
    try:
        HOST = ''
        PORT = 9009
        server = socketserver.TCPServer((HOST,PORT),MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('++++++파일 서버를 종료합니다.++++++')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoWindow = DemoForm()
    demoWindow.show() 
    app.exec_()


