import sys
import urllib.request
import cv2
import os
import numpy as np
import datetime
import time

import threading

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from threading import Thread
"""
이거 예외처리 안함,
3,4번 카메라 연결 안함
"""


#이거 너무 짧아서 곧 따라잡혀서 터짐 그러니까 나중에 테스트해서 기기에 맞게 조정해야 함
TimeLag=31.5

# image url to download
url = "http://100.100.80.51:5000/video_feed"
path1="D:/GitHub/bit27class/Bit27/Python/HowToUrlDowload/Videotest.png"
# file path and file name to download
outpath = "D:/GitHub/bit27class/Bit27/Python/HowToUrlDowload/"
outfile = "Videotest.png"


# image url to download
url2 = "http://100.100.80.44:5000/video_feed"
path2="D:/GitHub/bit27class/Bit27/Python/HowToUrlDowload/Videotest2.png"
# file path and file name to download
outpath2 = "D:/GitHub/bit27class/Bit27/Python/HowToUrlDowload/"
outfile2 = "Videotest2.png"

#모달리스 다이얼로그
class VideoDialog(QDialog):
    def __init__(self,modalsize,videopath, parent):
        QDialog.__init__(self,parent)
        self.setModal(0)     
        self.setupUI(modalsize)
        self.playVideo(videopath)
        self.show()

    #url을 요청하면 해당 url이 반환하는 값을 출력하는 메소드
    def downloadlocaltime(self,url):
        data = urllib.request.urlopen(url_time).read()
        return data

    #UI세팅dddddddddd
    def setupUI(self,size):
        #윈도우 설정
        self.setWindowTitle("Left Dialog")#타이틀바 이름
        self.setGeometry(size['x'],size['y'],size['w'],size['h'])#윈도우 크기
        #콘텐츠 설정
        #비디오 출력부
        self.label=QLabel("",self)
        self.label.move(0,0)
        self.label.resize(500,500)

    #비디오 출력========================================================================
    def playVideo(self,_videopath):
        self.capture = cv2.VideoCapture(_videopath)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(TimeLag)

    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, 1)#화면 출력
        #사각형 출력

    def displayImage(self, img, window=1):
        qformat = QImage.Format_Indexed8
        if(len(img.shape)==3):
            if(img.shape[2] == 4):
                qformat = Qimage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        
        outimage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outimage = outimage.rgbSwapped()

        if(window==1):
            self.label.setPixmap(QPixmap.fromImage(outimage))
            self.label.setScaledContents(True)
        elif(window==2):
            self.label.setPixmap(QPixmap.fromImage(outimage))
            self.label.setScaledContents(True)
        elif(window==3):
            cv2.imshow('Body Frame', img)
    #=====================================================================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        #윈도우 설정
        self.setGeometry(0,100,800,400)#윈도우 크기
        #버튼
        self.btn0 = QPushButton("SuuuuperVideooooooooYeah", self)
        self.btn0.move(0, 120)
        self.btn0.resize(300,30)
        self.btn0.clicked.connect(self.btn0_clicked) 
        self.btn0.setDisabled(True)

        self.btn1 = QPushButton("Video 1", self)
        self.btn1.move(20, 60)
        self.btn1.clicked.connect(self.btn1_clicked) 
        self.btn1.setDisabled(True)

        self.btn2 = QPushButton("Video 2", self)
        self.btn2.move(170, 60)
        self.btn2.clicked.connect(self.btn2_clicked)
        self.btn2.setDisabled(True)

        self.btn3 = QPushButton("Video 3", self)
        self.btn3.move(170, 60)
        self.btn3.clicked.connect(self.btn3_clicked)
        self.btn3.setDisabled(True)

        self.btn4 = QPushButton("Video 4", self)
        self.btn4.move(170, 60)
        self.btn4.clicked.connect(self.btn4_clicked)
        self.btn4.setDisabled(True)

        self.btn5 =QPushButton("Video Downloading...", self)
        self.btn5.move(340, 60)
        self.btn5.resize(200,30)
        self.btn5.clicked.connect(self.btn5_clicked) 



    #버튼 이벤트메소드
    def btn0_clicked(self):
        self.btn1Widget = QWidget()
        VideoDialog({'x':0,'y':400,'w':500,'h':500},path1,self.btn1Widget)
        self.btn2Widget = QWidget()
        VideoDialog({'x':700,'y':400,'w':500,'h':500},path2,self.btn2Widget)
        pass
    def btn1_clicked(self):
        self.btn1Widget = QWidget()
        VideoDialog({'x':0,'y':400,'w':500,'h':500},path1,self.btn1Widget)
        pass

    def btn2_clicked(self):
        self.btn2Widget = QWidget()
        VideoDialog({'x':700,'y':400,'w':500,'h':500},path2,self.btn2Widget)
        pass
    def btn3_clicked(self):
        self.btn2Widget = QWidget()
        VideoDialog({'x':0,'y':1000,'w':500,'h':500},path2,self.btn2Widget)
        pass
    def btn4_clicked(self):
        self.btn2Widget = QWidget()
        VideoDialog({'x':700,'y':1000,'w':500,'h':500},path2,self.btn2Widget)
        pass

    def btn5_clicked(self):
        #Video1 다운로딩
        self.t=threading.Thread(target=self.DownloadVideo1)
        self.t.daemon=True
        self.t.start()
        self.btn1.setDisabled(False)
        #Video2 다운로딩
        self.t2=threading.Thread(target=self.DownloadVideo2)
        self.t2.daemon=True
        self.t2.start()
        self.btn2.setDisabled(False)
        
        self.btn0.setDisabled(False)
        #Video3 다운로딩
        #self.t3=threading.Thread(target=self.DownloadVideo3)
        #self.t3.daemon=True
        #self.t3.start()
        #self.btn3.setDisabled(False)
        

        #Video4 다운로딩
        #self.t4=threading.Thread(target=self.DownloadVideo4)
        #self.t4.daemon=True
        #self.t4.start()
        #self.btn4.setDisabled(False)
        
        
        pass
    #Custom Method
    #비디오 다운로드하는 메소드
    def DownloadVideo1(self):
        # download
        urllib.request.urlretrieve(url, outpath+outfile)
    def DownloadVideo2(self):
        # download
        urllib.request.urlretrieve(url2, outpath2+outfile2)
    def DownloadVideo3(self):
        # download
        urllib.request.urlretrieve(url, outpath+outfile)
    def DownloadVideo4(self):
        # download
        urllib.request.urlretrieve(url2, outpath2+outfile2)

        
       


if __name__ == '__main__':
    app = QApplication(sys.argv)
   
    mywindow = MainWindow()
    mywindow.show()




    app.exec_()