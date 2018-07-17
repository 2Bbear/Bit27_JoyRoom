import threading
import cv2
import numpy as np  
import time
import glob
#Team Libliry
import WebServer
import TCPClient
import Video

#Custom Li
import Log as l

#
#CAMIP='192.168.137.1' #무선인터넷
CAMIP='220.90.196.192' # 유선 인터넷


class CamManger:
    video=None #Cam 객체
    tcpclient=None # TcpClient 객체
    thread_video=None
    thread_makeavi=None
    thread_webserver=None
    thread_sendfile=None
    def __init__(self):
        l.L_Flow()
        self.video=Video.Video(_camnum=1)
        self.tcpclient=TCPClient.TcpClient('220.90.196.192',9009)
        pass
    def __del(self):
        l.L_Flow()
        pass

#Override
    
#Custom
    #파일을 보내는 함수
    def SendData(self):
        l.L_Flow()
        #기존 파일수
        filenum=1;
        #전송 시작
        issendfile=False
        #디렉토리 감시
        while True:
            #'D:/GitHub/Bit27_JoyRoom/AlphaProject_001/CamProgram/CamProgram/saveavi/*'
            list = glob.glob('saveavi/*')
            #파일수가 증가했다면
            if(list.__len__()>filenum):
                
                issendfile=True
                filenum=list.__len__()
                #파일보내기
                if(issendfile):
             
                    st2=str(list[list.__len__()-2]).replace('\\','/')
                    if(self.tcpclient.SendFileToServer(st2)==False):
                        filenum-=1
                        continue

                    issendfile=False
                pass
            
            pass
            time.sleep(1)#=============이거 이거 고쳐야 함
        pass
    

    #흐름을 담당하는 함수
    def Run(self):
        l.L_Flow()
        global CAMIP
        #캠 열기
        self.video.OpenCam()
        #캠 작동 시키기
        self.thread_video=threading.Thread(target=self.video.RunFrame)
        self.thread_video.start()
        time.sleep(1) # 캠이 작동 하는데 까지 약간 시간이 필요함

        #Tcp로 파일 전송하기
        self.thread_sendfile=threading.Thread(target=self.SendData)
        self.thread_sendfile.start()

        #Webserver 실행
        thread_webserver=threading.Thread(target=WebServer.WebServerStart,args=(self,CAMIP))
        thread_webserver.start()
        pass
    
    #frame 에서 jpg로 변환된 파일을 가져오는 함수
    def get_jpg_bytes(self):
        return self.video.get_jpg_bytes()
    #Cam 영상을 저장하는 함수=================================================
    
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


    