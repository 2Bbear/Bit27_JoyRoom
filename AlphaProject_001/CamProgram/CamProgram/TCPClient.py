#
import socket
import time
from os.path import exists

#Team Libliry


#Custom Libliry

#
# -*- coding: utf-8 -*-


class TcpClient:
    tcpserverip=''
    tcpserverport=9009
    filename=''
    def __init__(self,_tcpserverip='192.168.137.240',_port=9009):
        self.tcpserverip=_tcpserverip
        self.tcpserverport=_port

        pass
    def __del__(self):
        pass

#Override
#Team
    def SetTCPServerip(self,_ip):
        self.tcpserverip=_ip
    def SendFileToServer(self,path):
        #보낼 파일이 존재하냐
        self.filename=path

        if not exists(self.filename): # 파일이 해당 디렉터리에 존재하지 않으면
            self.filename=None
            print('파일이 없음')
            return False # handle()함수를 빠져 나온다.
        print('파일이 있음')
        self.__getFileFromServer()

        pass
#Custom
    def __getFileFromServer(self):
        time.sleep(1)
        data_transferred = 0
        filename=self.filename
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.tcpserverip,self.tcpserverport))
            
            print('파일[%s] 전송 시작...' %filename)
            fin=self.filename.split('/')[-1]
            ef = fin.encode()
            sock.send(ef)
            print("파일 이름 "+fin)
            with open(filename, 'rb') as f:
                try:
                    data = f.read(1024) # 파일을 1024바이트 읽음
                    while data: # 파일이 빈 문자열일때까지 반복
                        data_transferred += sock.send(data)
                        data = f.read(1024)
                except Exception as e:
                    print(e)
            
            print('전송완료[%s], 전송량[%d]' %(filename,data_transferred))
            