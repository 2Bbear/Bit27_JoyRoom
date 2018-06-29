import sys
import cv2
import socketserver
import urllib.request
import threading

from os.path import exists
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

myflag=True
subform_class = uic.loadUiType("Add_Target.ui")[0]

fileimage = ''
filepath = ''

class Add_Target_Image(QDialog, subform_class):
    
    def __init__(self):
        #===========================================
        self.cmaip="http://192.168.137.1:5000"
        
        #===========================================

        QDialog.__init__(self)
        self.setupUi(self)

        self.findimgfile.clicked.connect(self.FindImage)
        self.pictureokbtn.clicked.connect(self.SendImage)
       

    def FindImage(self):
        self.fname = QFileDialog.getOpenFileName(self,'Open file','c://',"Image files (*.jpg *.gif *.png)")
        print(self.fname)
        filepath = self.fname[0]
        print(filepath)
        if(self.fname[0] != ''):
            img = cv2.imread(str(self.fname[0]))
            qformat = QImage.Format_Indexed8
            outimage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        
            #outimage = outimage.rgbSwapped()
            self.alreadyimage.setPixmap(QPixmap.fromImage(outimage))
            self.alreadyimage.setScaledContents(True)
            filepath = self.fname[0]
            fileimage = cv2.imread(self.fname[0])
            cv2.imshow("ALREADY_SHOW", fileimage)

    def startServer(self):
        
        HOST = ''
        PORT = 9009
        server = socketserver.TCPServer((HOST,PORT),MyTcpHandler)
        server.serve_forever()

        pass

    def SendImage(self):
        try:
            
            #데이터 전송용 서버 생성
            tt=threading.Thread(target=self.startServer)
            
            tt.start()
            #========================================
            
            #Cam에 이미지 줄거라고 호출
            temp=''
            temp=self.fname[0]
            temp=temp.replace("/","_")
            print(temp)
            url=self.cmaip+"/sendImageFile"+'/'+temp
            
            urllib.request.urlretrieve(url)#"http://192.168.137.1:5000/sendImageFile/tt.jpg"
            
            
            
        except KeyboardInterrupt:
            print('++++++파일 서버를 종료합니다.++++++')

class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        
        data_transferred = 0
        print('[%s] 연결됨' %self.client_address[0])
        filename = self.request.recv(1024) # 클라이언트로 부터 파일이름을 전달받음
        filename = filename.decode() # 파일이름 이진 바이트 스트림 데이터를 일반 문자열로 변환
        print(filename)
        
        #if not exists(filename): # 파일이 해당 디렉터리에 존재하지 않으면
            
            #return # handle()함수를 빠져 나온다.
         
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
        global myflag
       