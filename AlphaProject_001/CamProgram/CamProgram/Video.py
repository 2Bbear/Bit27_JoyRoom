#Video.py
import cv2
import threading

#Team 
import FaceRecog

#Custom
import Log as l

class Video:
    video_length=10 #second
    istimer=True
    thread_frame=None

    frame = None
    camera = None
    ismakecomplete=False
    save_videofile_name=''
    save_videofile_path='D:/GitHub/Bit27_JoyRoom/AlphaProject_001/CamProgram/CamProgram/saveavi'
    useface=None

    

    def __init__(self,camnum=0):
       self.useface = FaceRecog.FaceRecog()
       self.frame = []
       #self.camera = cv2.VideoCapture(camnum)   
   #실제 필요한 함수이다.
    #캠을 여는 함수
    def OpenCam(self):
        self.camera = cv2.VideoCapture(0)   
        pass
    #캠을 닫는 함수
    def CloseCam(self):
        pass

    def Run(self):
        ret, self.frame = self.camera.read()
        

        #self.frame = self.useface.FindFace(self.frame)  

    #frame을 jpg로 만드는 함수    
    def get_jpg_bytes(self):
        self.Run()
        ret, jpg = cv2.imencode('.jpg', self.frame)
        return jpg.tobytes()

    def End(self):
        pass

    #타이머를 위한 함수
    def __ChangeIsTimer(self):
        self.thread_frame=threading.Timer(self.video_length,self.__ChangeIsTimer)#프레임 타이머
        l.L_Flow()
        self.istimer=False
        self.thread_frame.daemon=True
        self.thread_frame.start()
