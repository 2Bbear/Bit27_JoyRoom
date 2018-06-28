from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector



#DB를 다룰 수 있게 해주는 클래스

class DBController:
    #생성자
    def __init__(self,_user='JJH', _password='1234',_host='192.168.137.1',_database='but277'):
        #DB와 연결
        self.cnx=mysql.connector.connect(user=_user, password=_password,host=_host,database=_database)
        print("생성됨")
        #쿼리 저장할 변수
        self.add_Log=''
    #camiptable Insert 하는 메소드
    def InsertCamIPTable(self,_camnumber,_ip):
        try:           
            #쿼리 만들기
            self.add_log = "INSERT INTO camiptable(camNumber,ip)  VALUES ("+str(_camnumber)+",'"+_ip+ "')"
            ExecuteQuery()
            print("Insert Success")
        except :
            print("Insert Error")
            pass
    
    #cmiptable 의 모든 data를 리스트로 반환
    def getAllCamIPTable(self):
        try:
            #출력용 리스트
            result=list()
            #쿼리 만들기
            self.add_log = "SELECT * FROM camiptable;"
            result=self.ExecuteSelectQuery()
            
            print("PrintAllCamIPTable 성공")
            return result
        except :
            print("PrintAllCamIPTable 실패")

    #Select 쿼리문을 실행하여 리스트를 반환하는 메소드
    def ExecuteSelectQuery(self):
        #결과 값 출력 용 list
        result=list()
        #DB핸들용 커서 객체 생성
        cursor = self.cnx.cursor()
        
        #쿼리 실행
        cursor.execute(self.add_log)
        #받은 데이터 출력
        
        for (id, camnumber, ip) in cursor:
            print("%d , %d , %s" % (id, camnumber, ip))
            result.append(str(camnumber)+"_"+str(ip))
        
        #커서 닫기
        cursor.close()
        print("ExecuteSelectQuery 성공")
        return result

    #쿼리문을 실행하는 메소드
    def ExecuteQuery(self):
        try:
            #DB핸들용 커서 객체 생성
            cursor = self.cnx.cursor()
            #쿼리 실행
            cursor.execute(self.add_log)
            #Commit 실행
            self.cnx.commit()
            #커서 닫기
            cursor.close()
            print("ExecuteQuery Secces")
        except :
            print("ExecuteQuery Error")

    def __del__(self):
        #DB 연결 해제
        self.cnx.close()
        print("DB 연결 해제")

#tt=DBController()
##tt.InsertCamIPTable(333,'404.313.233.3')
#tt.getAllCamIPTable()