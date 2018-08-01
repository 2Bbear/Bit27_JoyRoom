#사진이나 영상을 받기 위해서 TCP/IP 통신을 이용한다.
import socket
import socketserver
import numpy
import threading
from os.path import exists
# -*- coding: utf-8 -*-
#현재는 직접 써주었지만 DB에 Server의 Ip와 port를 넣어줘서 사용해야 한다
#DB에 서버의 IP를 포트를 남겨야 한다
#=========================================================================
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9009
#=========================================================================

class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global RESULT
        data_transferred = 0
        print('[%s] 연결됨' %self.client_address[0])

        sock = self.request
        namedata = sock.recv(1024)

        originalname = namedata.decode()
        filename = originalname.split('/')[-1]
        print(filename)

        imagedata = sock.recv(1024)

        if not imagedata:
            print('서버에 존재하지 않거나 전송중 오류발생')
            return

        #원하는 폴더에 저장
        with open('Test/' + filename, 'wb') as f:
            try:
                while  imagedata:
                    f.write(imagedata)
                    data_transferred += len(imagedata)
                    imagedata = sock.recv(1024)
                print('전송완료. 전송량 [%d]' %(data_transferred))
            except Exception as e:
                print(e)


class TcpIp:
    def __init__(self):
        print('안녕하세요 TCP/IP입니다')
        pass

    def __del__(self):
        pass

    #ServerManager꺼임
    def GetData(self):
        print('++++++파일 서버를 시작++++++')
        print("+++파일 서버를 끝내려면 'Ctrl + C'를 누르세요.")
        try:
            server = socketserver.TCPServer((HOST,PORT),MyTcpHandler)   
            server.serve_forever(1)
        except KeyboardInterrupt:
            print('++++++파일 서버를 종료합니다.++++++')

 
