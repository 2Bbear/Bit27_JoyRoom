from flask import Flask
from flask import request
from werkzeug import secure_filename

from flask import Flask, render_template,url_for, Response
import face_recog
import time
import cv2
import pymysql
import mysql.connector
from operator import eq
import threading


app = Flask(__name__)
#변화 가능한 변수
rectangleColor=(0,0,255)
foundedName='UnKnown'
videoLocalTime=time.localtime()
isFindPerson=False

#DB에 쓰는 변수
datalog = "nothing"

#영상 전송===========================
def gen(fr):
    global rectangleColor
    global isFindPerson
    global videoLocalTime
    while True:
        fr.targetcolor=rectangleColor
        isFindPerson=fr.isfindperson
        videoLocalTime=fr.videoLocalTime
        jpg_bytes = fr.get_jpg_bytes()
        yield (b'--frame\r\n' 
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(face_recog.FaceRecog()), mimetype='multipart/x-mixed-replace; boundary=frame')
#====================================
#Route
@app.route('/')
def hello_world():
    return render_template('index.html')


#main 기본 메서드
@app.route('/mainService')
def mainService():
    return "빰빠빰빠밤"

#문자열 매개변수 넘기기
@app.route('/printName/<personname>')
def printName(personname):
    return 'User %s' %personname

#색상변경하는 메소드
@app.route('/changeRectangleColor/<targetcolor>')
def changeRectangleColor(targetcolor):
    global rectangleColor
    if targetcolor=='blue':
        rectangleColor=(255,0,0)
    elif targetcolor=='green':
        rectangleColor=(0,255,0)
    elif targetcolor=='red':
        rectangleColor=(0,0,255)
    
    return 'User' 

#색상변경하는 메소드2
@app.route('/changeRectangleColor2/<int:a>/<int:b>/<int:c>')
def changeRectangleColor2(a,b=None,c=None):
    global rectangleColor
    rectangleColor=(a,b,c)
    if rectangleColor:
        return 'true'
    else:
        return 'false'
    return 'false'

#숫자 매개변수 넘기기
@app.route('/printAge/<int:post_id>')
def printAge(post_id):
    return 'Post %d d' % post_id

#사람 찾은 로그 남기는 메소드
@app.route('/findPerson')
def findPerson():
    global videoLocalTime
    global isFindPerson
    global datalog

    #웹에 보낼 string 문자열
    datalog = str("%s time: %04d-%02d-%02d %02d:%02d:%02d "%(isFindPerson,videoLocalTime.tm_year, videoLocalTime.tm_mon, videoLocalTime.tm_mday, videoLocalTime.tm_hour,videoLocalTime.tm_min, videoLocalTime.tm_sec))
   
    if eq(datalog,"nothing"): # and isFindPerson,"False" 되게 만들기.. 현재는 DB에 False인 값도 들어옴
        print("감지 못함")
    else:  
        timer = threading.Timer(0.7,db_datalog)
        timer.start()
        return datalog

#디비 관련 소스함수
def db_datalog():
    #print("DB 시작")

    # 접속
    db = mysql.connector.connect(host='100.100.80.52',port='3306' ,user='bit27', password='123123',database='bit27_db',charset='utf8mb4')

    # 커서 가져오기 (cursor 는 control structure of database 입니다. (연결된 객체라는데 잘모름))
    cursor = db.cursor()

    print("DB 시작")
    print(datalog)
    #데이터 지우기 
    #add_log = "Delete FROM data"

    #데이터 삽입
    add_log = "INSERT INTO data (datalog) VALUES ('"+ datalog+"')"

   

    cursor.execute(add_log)

    db.commit()

    cursor.close()
    db.close()


    # SQL 문 만들기
    #sql = "SELECT * FROM bit27_db.data"

    #----------------------------------------------------------------------------------------------------------

    # SQL 문 만들기
    #sql = '''
    #        CREATE TABLE korea2 (
    #               id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    #               name VARCHAR(20) NOT NULL,
    #               model_num VARCHAR(10) NOT NULL,
    #               model_type VARCHAR(10) NOT NULL,
    #               PRIMARY KEY(id)
    #        );
    #    '''
    #----------------------------------------------------------------------------------------------------------


    # 실행하기
    #cursor.execute(sql)
 
    # DB에 Complete 하기
    #db.commit()
    
    #result = cursor.fetchall()

    #for row_data in result:
    #    print(row_data[0])
    #    print(row_data[1])
    #    print(row_data[2])
    #    print(row_data[3])  
    # DB 연결 닫기
    #db.close()


#test
with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'


if __name__ == '__main__':
    #app.run(host='192.168.137.1', debug=True)
    app.run(host='100.100.80.51', debug=True)
