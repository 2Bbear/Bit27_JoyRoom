#사진이나 영상을 받기 위해서 TCP/IP 통신을 이용한다.
import socket
import socketserver
import numpy
import cv2
from os.path import exists

#현재는 직접 써주었지만 DB에 Server의 Ip와 port를 넣어줘서 사용해야 한다
#DB에 서버의 IP를 포트를 남겨야 한다
#=========================================================================

#=========================================================================

class TcpIp:
    def __init__(self):
        print('안녕하세요 TCP/IP입니다')
        pass

    def __del__(self):
        pass

   

    #Admin, CamManager꺼임(서버에 파일을 주기위한 함수)
    def GiveData(self, _filepath='',_filename='',_hostip=socket.gethostbyname(socket.gethostname()),_port=9009):
        data_transferred = 0
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((_hostip,_port))

            #이부분은 Admin이나 Cam부분에서 매개변수로 해당파일의 path를 불러와야 함
            #밑의 소스는 예제로서 실행여부를 판단하기 위해 만들어 놓은 것이다
            #밑의 소스는 그럼 사라진다
            #===============================================================================================
            filename=_filepath+_filename+'.avi'

            #===============================================================================================

            if not exists(filename): # 파일이 해당 디렉터리에 존재하지 않으면
                return # handle()함수를 빠져 나온다.


            print('파일[%s] 전송 시작...' %filename)
            ef = filename.encode()
            sock.send(ef)#이름 보내기

            #파일 보내기
            with open(filename, 'rb') as f:
                try:
                    data = f.read(1024) # 파일을 1024바이트 읽음
                    while data: # 파일이 빈 문자열일때까지 반복
                        data_transferred += sock.send(data)
                        data = f.read(1024)
                except Exception as e:
                    print(e)
 
            print('전송완료[%s], 전송량[%d]' %(filename,data_transferred))