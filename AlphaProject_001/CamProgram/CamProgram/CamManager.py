import threading
import cv2
import numpy as np  
import time
#Team Libliry
import WebServer
import TCPClient
import Video

#Custom Li
import Log as l

class CamManger:
    video=None #Cam 객체
    thread_video=None
    thread_makeavi=None
    thread_webserver=None
    def __init__(self):
        l.L_Flow()
        self.video=Video.Video()
        pass
    def __del(self):
        l.L_Flow()
        pass

#Override
    
#Custom
    #흐름을 담당하는 함수
    def Run(self):
        l.L_Flow()

        #캠 열기
        self.video.OpenCam(0)
        #캠 작동 시키기
        self.thread_video=threading.Thread(target=self.video.RunFrame)
        self.thread_video.start()
        time.sleep(1) # 캠이 작동 하는데 까지 약간 시간이 필요함
        
        #영상 저장하기
        self.thread_makeavi=threading.Thread(target=self.MakeAviFile)
        self.thread_makeavi.start()

        time.sleep(1)
        #타이머
        self.SetTimer_A()

        #Webserver 실행
        thread_webserver=threading.Thread(target=WebServer.WebServerStart,args=(self,))
        thread_webserver.start()
        pass
    
    #frame 에서 jpg로 변환된 파일을 가져오는 함수
    def get_jpg_bytes(self):
        return self.video.get_jpg_bytes()
    #Cam 영상을 저장하는 함수=================================================
    def MakeAviFile(self):
        l.L_Flow()
        while True:
            self.video.MakeAviFile()
        print('waat?')    
        pass

    #타이머
    def SetTimer_A(self):
        l.L_Flow()
        tt=threading.Timer(10,self.SetTimer_A)
        tt.daemon=True
        tt.start()
        self.video.ismakeavi=False
    #===========================================================================
    #Cam 영상을 화면에 출력하는 함수
    def ShowCamWindow(self):
        l.L_Flow()
        #화면에 출력 시키기
        print(self.video.frame)
        while 1:
            cv2.imshow('dd',self.video.frame)
            if cv2.waitKey(1)&0xFF == ord('q'):  
                    return 


    