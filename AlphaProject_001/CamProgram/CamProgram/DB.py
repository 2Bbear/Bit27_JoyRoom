#DB.py
import socket
import mysql.connector

import numpy as np

class DB:
    ip1 =''
    ip2 =''
    ip3 =''
    ip4 =''
    splitip = []

    def __init__(self,_host='220.90.196.192'):
        #host=socket.gethostbyname(socket.gethostname())
        self.truehost =_host
        #self.truename = FA.FaceRecog.get_frame   
        #self.num = input("생성할 아이디를 입력하시오 : ") # 넘버 

    def __del__(self):    
        pass

    #디비에 아이피 저장하는 메소드
    def CamIPInsert(self,_serverip='220.90.196.196',_dbport='3306',_dbuser='bit271',_dbpassword='123123',_dbname='sys',_camnum=1):
        print('1')
        self.num = _camnum # 넘버
        
        #host='220.90.196.196',port='3306' ,user='bit271', password='123123',database='sys',charset='utf8'
        #host=_serverip,port=_dbport ,user=_dbuser, password=_dbpassword,database=_dbname,charset='utf8'
        db = mysql.connector.connect(host=_serverip,port=_dbport ,user=_dbuser, password=_dbpassword,database=_dbname,charset='utf8')
        print('2')
        loginsert = "INSERT INTO ip(num,ip) VALUES ('" + str(self.num) +"','"+ _serverip + "')" 
        print('3')
        try:
            print('4')
            cursor = db.cursor()
            cursor.execute(loginsert)
            db.commit()

            if(self.num == '1'):
                ip1 =  _serverip         
                print(ip1)

            if(self.num == '2'):
               ip2 =  _serverip
               print(ip2)

            if(self.num == '3'):
               ip3 =  _serverip
               print(ip3)

            if(self.num == '4'):
               ip4 =  _serverip
               print(ip4)

        except mysql.connector.Error as error:
            print('5')
            if int(self.num) < 5 and int(self.num) > 0:
                print("이미 번호 : %s는 사용중인 번호입니다."%self.num)
                cursor.close()
                db.close()
                self.CamIPDelete()
                self.CamIPInsertAgain(self.truehost)
                print("DB에 저장 완료")
            print("다시 입력해주세요(1~4)")
        finally:
            cursor.close()
            db.close()
        return True

    #아이피 최신화해주는 메소드
    def CamIPInsertAgain(self,host):
        #self.num = input("생성할 아이디를 입력하시오 : ") # 넘버    
        db = mysql.connector.connect(host='220.90.196.196',port='3306' ,user='bit271', password='123123',database='sys',charset='utf8')
        loginsert = "INSERT INTO ip(num,ip) VALUES ('" + str(self.num) +"','"+ host + "')"  
        try:
            cursor = db.cursor()
            cursor.execute(loginsert)
            db.commit()

            if(self.num == '1'):
                ip1 =  host         
                print(ip1)

            if(self.num == '2'):
               ip2 =  host
               print(ip2)

            if(self.num == '3'):
               ip3 =  host
               print(ip3)

            if(self.num == '4'):
               ip4 =  host
               print(ip4)
        except mysql.connector.Error as error:
            print("이미 번호 : %s는 사용중인 번호입니다."%self.num)
            cursor.close()
            db.close()
            self.CamIPDelete()
            self.CamIPInsertAgain(self.truehost)
        finally:
            cursor.close()
            db.close()

    #필요 없을 듯
    def CamIPUpdate(self):
        num = input("최신화할 아이디를 입력하시오 : ") # 넘버   
        if(num == '1'):
            db = mysql.connector.connect(host='172.16.20.235',port='3306' ,user='bit27_1', password='123123',database='bit27_db',charset='utf8')
            cursor = db.cursor()
       
            add_log = "UPDATE ip set ip('" + self.truehost +"')  where ('" + self.ip1 +"')"
            
            cursor.execute(add_log)
            db.commit()
            cursor.close()
            db.close()
            
            print("DB에 수정 완료")
            return

    #아이피 가져오는 메소드
    def CamIPSelect(self):
        num = input("가져올 ip의 아이디를 입력하시오 : ") # 넘버 
        db = mysql.connector.connect(host='220.90.196.196',port='3306' ,user='bit271', password='123123',database='sys',charset='utf8')
        logchange = "SELECT ip FROM ip WHERE num =" + str(num)

        try:
            cursor = db.cursor()
            logselet = logchange         
            cursor.execute(logselet)
            db.commit()
        except mysql.connector.Error as error:
            print("IP%s의 IP 빼오기 실패"%num)

        finally:
            cursor.close()
            db.close()

        if(num == '1'):
            ipip = cursor.fetchone()          
            self.splitip = str(ipip).split("'")
            self.ip1 = self.splitip[1]
            print(ip1)

        if(num == '2'):
           ipip = cursor.fetchone()
           self.splitip = str(ipip).split("'")
           self.ip2 = self.splitip[1]
           print(ip2)

        if(num == '3'):
           ipip = cursor.fetchone()
           self.splitip = str(ipip).split("'")
           self.ip3 = self.splitip[1]
           print(ip3)

        if(num == '4'):
           ipip = cursor.fetchone()
           self.splitip = str(ipip).split("'")
           self.ip4 = self.splitip[1]
           print(ip4)
            
        print("IP%s의 IP 빼오기 완료"%num)
       
    #아이피 최신화 하기 전 지워주는 메소드
    def CamIPDelete(self):
        
        db = mysql.connector.connect(host='220.90.196.196',port='3306' ,user='bit271', password='123123',database='sys',charset='utf8')
        logdelete = "DELETE ip FROM ip WHERE num =" + str(self.num)
        try:
            cursor = db.cursor()
            cursor.execute(logdelete)
            db.commit()
        except mysql.connector.Error as error:
            print("IP%s의 IP 삭제 실패"%self.num)
        finally:
            cursor.close()
            db.close()
            
        print("IP%s의 IP 삭제 완료"%self.num)

    #로그 남길 메소드
    def CamLogTable(self,num,filename,time,name,coordinates,clothescolor):
 
        db = mysql.connector.connect(host='220.90.196.196',port='3306' ,user='bit271', password='123123',database='sys',charset='utf8')
        cam1Log = "INSERT INTO cam"+ str(num) +"logtable(filename,time,name,coordinates,clothescolor) VALUES ('" + filename +"','"+ time +"','"+ name +"','"+ coordinates +"','"+ clothescolor+"')"
        try:
            cursor = db.cursor()
            cursor.execute(cam1Log)
            db.commit()

        except mysql.connector.Error as error:
            print("%s번캠 로그 저장 실패"%num)

        finally:
            cursor.close()
            db.close()
        print("%s번캠 로그 저장 완료"%num)




    

