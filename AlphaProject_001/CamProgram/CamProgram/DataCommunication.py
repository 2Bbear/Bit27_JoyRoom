import socket
#Teem Libliry
import Video
import WebServer

#Custom Libliry
import Log as l

class DataCommunication:
    host=socket.gethostbyname(socket.gethostname())
    def __init__(self):
        l.L_Flow()
        d='192.34.23.0'
        print(self.host)
        self.StartWebServer()
        pass
    def __del__(self):
        l.L_Flow()
        pass

    #Override 

    #Team Method
    #영상 전송
    def SendVideo(self):
        l.L_Flow()

        pass
    #얼굴위치 값 전송
    def SendFaceLocation(self):
        l.L_Flow()
        pass
    #avi영상 전송
    def SendAviVideo(send):
        l.L_Flow()
        pass
    #사진 전송받기
    def ReceivePicture(self):
        l.L_Flow()
        pass
    #사진 전송하기
    def SendPicture(self):
        l.L_Flow()
        pass

    #Custom Method
    #웹서버 시작시키는 메소드
    def StartWebServer(self):
        WebServer.WebServerStart()
        pass

