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
    SAVEDIRPATH='D:/GitHub/Bit27_JoyRoom/AlphaProject_001/CamProgram/CamProgram/saveavi/'
    frame = None
    camera = None
    thread_capture=None
    camnum=0
    ismakeavi=True
    out=None#ddfsf
    def __init__(self,_savedirpath='D:/GitHub/Bit27_JoyRoom/AlphaProject_001/CamProgram/CamProgram/saveavi/',_camnum=0):
        l.L_Flow()
        self.frame = []
        #self.SAVEDIRPATH=_savedirpath
        #self.camnum=_camnum
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
    def OpenCam(self):#dfs
        l.L_Flow()
        self.camera = cv2.VideoCapture(0)  
        self.camera.set(3,320)
        self.camera.set(4,240)

    #프레임을 찍는 함수
    def CaptureCam(self):
        lock.acquire()
        ret,self.frame =self.camera.read()
        lock.release()

    #타이머
    def SetTimer_A(self):
        l.L_Flow()
        tt=threading.Timer(10,self.SetTimer_A)
        tt.daemon=True
        tt.start()
        self.ismakeavi=False    
    #프레임을 계속 찍는 함수
    def RunFrame(self):
        l.L_Flow()
        #타이머
        self.SetTimer_A()

        fps=15
        width=int(self.camera.get(3))
        height=int(self.camera.get(4))
        
        while True:
            today=datetime.today().strftime("%Y%m%d%H%M%S")
            _saveavifilepath=self.SAVEDIRPATH+today+'_'+'cam'+str(self.camnum)+'.avi'
            self.out = cv2.VideoWriter(_saveavifilepath,cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width,height))
            while self.ismakeavi:
                print('1')
                self.thread_capture=threading.Thread(target=self.CaptureCam)
                self.thread_capture.start()
                self.thread_capture.join()
                print('2')
                self.out.write(self.frame)
                print('3')
            self.out.release()
            self.ismakeavi=True
        pass

    #캠을 닫는 함수
    def CloseCam(self):
        l.L_Flow()
        self.camera.release()