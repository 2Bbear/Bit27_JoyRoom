import sys
import datetime
import mysql.connector
import cv2

import urllib.request
import threading
import time

import HistoryLogUI as hisui
import AddTarget as at
import CamDetailShow as cds

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
form_class = uic.loadUiType("0625_DBUI.ui")[0]

#D:/GitHub/Bit27_JoyRoom/BetaProject_001/MainProgram/HowToUrlDowload/Videotest.png

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
        #비디오 관련=====================
        self.VideoDownload("http://100.100.80.51:5000/video_feed","D:/GitHub/Bit27_JoyRoom/BetaProject_001/MainProgram/HowToUrlDowload/Videotest.png")
        time.sleep(7)#다운로드와 재생 사이의 잠깐의 간격. 
        self.PlayVideo("D:/GitHub/Bit27_JoyRoom/BetaProject_001/MainProgram/HowToUrlDowload/Videotest.png")
        
        #=====================
        print(str(no_use_value))
        dlg = cds.Detail_Show()       #다른 파일에 있는 class이므로 잘 써주자
        dlg.exec_()

    def ShowHistoryLog(self):
        dlg = hisui.HisTory_Log_Show()       #다른 파일에 있는 class이므로 잘 써주자
        dlg.exec_()

    def AddTargetBtnEvent(self):
        dlg = at.Add_Target_Image()       #다른 파일에 있는 class이므로 잘 써주자
        dlg.exec_()
    #비디오 출력하는 함수======================================================== JJH
    def PlayVideo(self,_videopath):
        self.capture = cv2.VideoCapture(_videopath)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)#프레임을 읽어 들이는 속도 즉 재생 속도
    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, 1)#화면 출력
    #지금 라벨을 하나만 출력하게 끔 설정 해놓았음. 라벨에 따라 displayImage 함수를 각각 만들어 주어야 함.    
    def displayImage(self, img, window=1):
        qformat = QImage.Format_Indexed8
        if(len(img.shape)==3):
            if(img.shape[2] == 4):
                qformat = Qimage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        
        outimage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outimage = outimage.rgbSwapped()
        # 이부분이 때문에 라벨에 따라 만들어 줘야 함
        if(window==1):
            self.cam1.setPixmap(QPixmap.fromImage(outimage))
            self.cam1.setScaledContents(True)
        elif(window==2):
            self.cam1.setPixmap(QPixmap.fromImage(outimage))
            self.cam1.setScaledContents(True)
        elif(window==3):
            cv2.imshow('Body Frame', img)
    #VideoDownLoad=============================================================== JJH
    #비디오를 계속 다운로드 하게 하는 메소드 쓰레드를 사용해서 계속 다운 받음
    def VideoDownload(self,url,filepath):
        #Video1 다운로딩
        self.t=threading.Thread(target=self.UrlVideoDownload,args=(url,filepath,))
        self.t.daemon=True
        self.t.start()
        
    
    #url을 이용해서 비디오를 다운로드 하는 메소드
    #url은 다운로드 받을 링크
    #filepath는 저장 될 위치 와 파일 이름. 확장자 까지
    def UrlVideoDownload(self,url,filepath):
        # download
        urllib.request.urlretrieve(url, filepath)
    #============================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoWindow = DemoForm()
    demoWindow.show() 
    app.exec_()