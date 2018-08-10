#Video.py
import cv2
import FaceRecog
import numpy as np  
import threading
import time
from datetime import datetime

lock=threading.Lock()#frame의 안정적인 생성을 위한 락



import Log as l
class Video:
    SAVEDIRPATH=''
    frame = None
    sendframe=None
    camera = None
    thread_capture=None
    camnum=0
    ismakeavi=True
    out=None#ddfsf
    video_lenght=10 #second
    facerr=FaceRecog.FaceRecog()
    testflg=False
    
    def __init__(self,_savedirpath='D:/GitHub/Bit27_JoyRoom/AlphaProject_001/CamProgram/CamProgram/saveavi/',_camnum=0,_video_lenght=10):
        l.L_Flow()
        self.frame = []
        self.sendframe=[]
        self.SAVEDIRPATH=_savedirpath
        self.camnum=_camnum
        self.video_lenght=_video_lenght

    def __del__(self):
        l.L_Flow()
        self.out.release()
        self.camera.release()

    #Fram을 jpg 바이너리로 변환하는 함수    
    def get_jpg_bytes(self):
        ret, jpg = cv2.imencode('.jpg', self.frame)
        return jpg.tobytes()
    
#Custom 
    #캠을 여는 함수
    def OpenCam(self):
        l.L_Flow()
        self.camera = cv2.VideoCapture(1)  
        self.camera.set(3,800)#320 800 1024 1280 1680
        self.camera.set(4,600)#240 600 960  960 1050
        

    #프레임을 찍는 함수
    def CaptureCam(self):
        lock.acquire()
        ret,self.frame =self.camera.read()
        self.sendframe=self.frame.copy()
        #얼굴 사각형 그리는 함수
        self.facerr.FindFace(self.frame)
        lock.release()

    #타이머
    def SetTimer_A(self):
        l.L_Flow()
        tt=threading.Timer(self.video_lenght,self.SetTimer_A)
        tt.daemon=True
        tt.start()
        self.ismakeavi=False    
    #프레임을 계속 찍는 함수
    def RunFrame(self):
        l.L_Flow()
        #타이머
        self.SetTimer_A()
        #어 프레임수
        fps=30
        width=int(self.camera.get(3))
        height=int(self.camera.get(4))
        self.ismakeavi=True
        while True:
            
            #파일 이름 만들기
            today=datetime.today().strftime("%Y%m%d%H%M")
            
            _saveavifilepath=self.SAVEDIRPATH+today+'_'+'cam'+str(self.camnum)+'.avi'
            #avi 영상으로 만드는 부분
            self.out = cv2.VideoWriter(_saveavifilepath,cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width,height))
            #프레임찍기
            while self.ismakeavi:
               
                self.thread_capture=threading.Thread(target=self.CaptureCam)
                self.thread_capture.start()
                self.thread_capture.join()
                
                self.out.write(self.sendframe)#self.frame
            #파일 파이프 닫기    
            self.out.release()
            self.ismakeavi=True
            self.testflg=True
        pass

    #캠을 닫는 함수
    def CloseCam(self):
        l.L_Flow()
        self.camera.release()