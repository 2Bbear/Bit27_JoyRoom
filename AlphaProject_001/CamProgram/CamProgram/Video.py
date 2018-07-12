#Video.py
import cv2
import FaceRecog
import numpy as np  
import threading
import time

lock=threading.Lock()#frame의 안정적인 생성을 위한 락



import Log as l
class Video:
    SAVEDIRPATH='D:/GitHub/Bit27_JoyRoom/AlphaProject_001/CamProgram/CamProgram/saveavi/'
    frame = None
    camera = None
    thread_capture=None
    num=0
    ismakeavi=True
    
    def __init__(self):
        l.L_Flow()
        self.frame = []

    #Fram을 jpg 바이너리로 변환하는 함수    
    def get_jpg_bytes(self):
        ret, jpg = cv2.imencode('.jpg', self.frame)
        return jpg.tobytes()
    
#Custom 
    #avi영상을 만드는 함수
    def MakeAviFile(self):
        l.L_Flow()
        try:
            fps=960
            width=int(self.camera.get(3))
            height=int(self.camera.get(4))
            _saveavifilepath=self.SAVEDIRPATH+str(self.num)+'.avi'
            out = cv2.VideoWriter(_saveavifilepath,cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width,height))

            while(self.ismakeavi):
                out.write(self.frame)
        except :
            pass
        finally:
            out.release()
            self.ismakeavi=True
            self.num+=1
        
    #캠을 여는 함수
    def OpenCam(self,_camnum):
        l.L_Flow()
        self.camera = cv2.VideoCapture(_camnum)  
        self.camera.set(3,320)
        self.camera.set(4,240)

    #프레임을 찍는 함수
    def CaptureCam(self):
        lock.acquire()
        ret,self.frame =self.camera.read()
        lock.release()
        
    #프레임을 계속 찍는 함수
    def RunFrame(self):
        l.L_Flow()

        while True:
            self.thread_capture=threading.Thread(target=self.CaptureCam)
            self.thread_capture.start()
            self.thread_capture.join()
             
        pass

    #캠을 닫는 함수
    def CloseCam(self):
        l.L_Flow()
        self.camera.release()