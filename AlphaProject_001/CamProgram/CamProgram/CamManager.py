import threading
import cv2
import numpy as np  
import time
import glob
import os
#Team Libliry
import WebServer
import TCPClient
import Video
import DB
#Custom Li
import Log as l

class CamManger:
    #Cam관련
    #CAMIP='192.168.137.1' #무선인터넷
    # 220.90.196.192  유선인터넷
    CAMIP='192.168.0.30' # 유선 인터넷
    #220.90.196.196 #주 서버 컴퓨터 아이피
    CAMNUM=1 # cam 번호
    CAMLENGHT=60 #avi 길이 , second 단위

    #ServerProgram 관련
    SERVERIP='192.168.0.21'#'220.90.196.196'
    SERVERPORT=9009

    #DB 관련
    SERVERDBIP='192.168.0.21'
    SERVERDBPORT='3306'
    SERVERDBUSER='bit271'
    SERVERDBPASSWORD='123123'
    SERVERDBNAME='sys'

    
    video=None #Cam 객체
    tcpclient=None # TcpClient 객체
    db=None # DB 객체
    thread_video=None
    thread_makeavi=None
    thread_webserver=None
    thread_sendfile=None

    #==========================================
   
    #==========================================

    def __init__(self):
        l.L_Flow()
        self.video=Video.Video(_savedirpath='saveavi/',_camnum=self.CAMNUM,_video_lenght=self.CAMLENGHT)
        self.tcpclient=TCPClient.TcpClient(self.SERVERIP,9009)
        self.db=DB.DB(_host=self.CAMIP)
        pass
    def __del(self):                                                                          
        l.L_Flow()
        pass

#Override
    
#Team
    #흐름을 담당하는 함수
    def Run(self):
        l.L_Flow()
       
        #DB에 캠 등록하기
        self.db.CamIPInsert(_serverip=self.SERVERDBIP,_dbport=self.SERVERDBPORT,_dbuser=self.SERVERDBUSER,_dbpassword=self.SERVERDBPASSWORD,_dbname=self.SERVERDBNAME,_camnum=self.CAMNUM)
        
        #캠 열기
        self.video.OpenCam()
        #캠 작동 시키기
        self.thread_video=threading.Thread(target=self.video.RunFrame)
        self.thread_video.start()
        time.sleep(1) # 캠이 작동 하는데 까지 약간 시간이 필요함

        #Tcp로 파일 전송하기
        self.thread_sendfile=threading.Thread(target=self.SendData2)
        self.thread_sendfile.start()

        #Webserver 실행
        thread_webserver=threading.Thread(target=WebServer.WebServerStart,args=(self,self.CAMIP))
        thread_webserver.start()
        pass
#Custom
     #파일을 보내는 함수
    def SendData2(self):
        l.L_Flow()
        #전송 시작
        issendfile=False
        #디렉토리 감시
        while True:
            #'D:/GitHub/Bit27_JoyRoom/AlphaProject_001/CamProgram/CamProgram/saveavi/*'
            list = glob.glob('saveavi/*')
            #파일수1개 이상일때
            if(list.__len__()>1):
                issendfile=True
                #파일보내기
                if(issendfile):
                    st2=str(list[list.__len__()-2]).replace('\\','/')
                    #파일 전송에 실패 했을 때
                    if(self.tcpclient.SendFileToServer(st2)==False):
                        continue
                    #파일 전송에 성공 했을 때
                    else:
                        os.remove(st2)
                    issendfile=False
                pass
            
            pass
            time.sleep(1)#=============이거 이거 고쳐야 함
        pass
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


    