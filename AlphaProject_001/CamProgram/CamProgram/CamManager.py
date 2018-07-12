import threading
import time
import cv2
import numpy

from datetime import datetime


#Team Libliry
import DB
import Video
import WebServer
import TCPIP
#Custom Libliry
import Log as l



class CamManager:
    instance_db=None #DB 객체
    instance_video=None #Video 객체
    instance_tcpip=None #TCP 객체
    frame=None#프레임이 저장될 변수
    
    thread_video=None
    thread_webserver=None
    thread_sendavifile=None

    isprogrmaend=False
    
    
    def __init__(self):
        l.L_Flow()
        #instance 생성
        #self.instance_db=DB.DB()
        self.instance_video=Video.Video()
        self.instance_tcpip=TCPIP.TcpIp()
        self.Run()
        pass
    def __del__(self):
        l.L_Flow()
        
        pass

#Override
    
#Team Method
    def Run(self):
        l.L_Flow()
        #db에 camip 전송하기
        #self.instance_db.CamIPInsert(self.instance_db.truehost)

        #Cam 시작하기
        self.instance_video.OpenCam()

        #Web Server 시작
        self.thread_webserver=threading.Thread(target=WebServer.WebServerStart,args=('220.90.196.192',self.instance_video,))
        self.thread_webserver.daemon=True
        self.thread_webserver.start()
       

        #대기 시키기
        filename=self.instance_video.save_videofile_name
        filepath=self.instance_video.save_videofile_path #나중에 폴더명 정해지면 그곳으로 넣어야 함
        hostip='220.90.196.192'
        port=9009

        while True:
            if self.instance_video.ismakecomplete==True:
                self.thread_sendavifile=threading.Thread(target=self.instance_tcpip.GiveData,args=(filepath,filename,hostip,port))
                self.thread_sendavifile.start
                self.instance_video.ismakecomplete=False
                pass

            #CamProgram이 종료되었는가
            if self.isprogrmaend==True:
                break
            pass

        
#Custom Method

    