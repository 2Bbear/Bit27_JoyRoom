#실시간으로 영상을 받아서
#받은 영상들을 실시간을 분석

import threading
import time

#Team Libliry
import TcpIp

#Custom Libliry
import Log as l

class ServerManager:
    instance_tcpserver=None#TcpServer 객체

    def __init__(self):
        l.L_Flow()
        self.instance_tcpserver=TcpIp.TcpIp()
        pass
    def __del__(self):
        l.L_Flow()
        pass

    #Override

    #Team
    #주 흐름이 담긴 함수
    def Run(self):
        l.L_Flow()
        #DB 접속
        #Tcp Server 생성
        thread_tcpserver=threading.Thread(target=self.instance_tcpserver.GetData)
        thread_tcpserver.daemon=True
        thread_tcpserver.start()
        
        #영상 분석

        #메인문이 끝나지 않게 하는 코드
        while 1:
            print("메인문 살아 있땅")
            time.sleep(5)
        pass

    
    #Custom
