from flask import Flask
from flask import request
from flask import jsonify

from werkzeug import secure_filename

from flask import Flask, render_template,url_for, Response
import face_recog
import time
import cv2
import os
#import pymysql
import mysql.connector
from operator import eq
import threading

import DBController

import socket
app = Flask(__name__)
#변화 가능한 변수
rectangleColor=(0,0,255)
foundedName='UnKnown'
videoLocalTime=time.localtime()
isFindPerson=False
datalog = "nothing"
facepicturename='' #새로 추가된 얼굴 사진 이름
facereencoding=False #새로 추가된 얼굴을 재 인코딩 하는 플래그
deathflag=False

#영상 전송===========================
def gen(fr):
    global rectangleColor
    global isFindPerson
    global videoLocalTime
    global foundedName
    global deathflag
    while True:
        fr.targetcolor=rectangleColor
        isFindPerson=fr.isfindperson
        foundedName = fr.name
        videoLocalTime=fr.videoLocalTime
        
        jpg_bytes = fr.get_jpg_bytes()
        
        fr.newpicturename=facepicturename
        if deathflag:
            fr.reencodingflag=facereencoding
            deathflag=False

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

#숫자 매개변수 넘기기
@app.route('/printAge/<int:post_id>')
def printAge(post_id):
    return 'Post %d d' % post_id


#사람 찾은 로그 남기는 메소드
@app.route('/findPerson')
def findPerson():
    global videoLocalTime
    global isFindPerson
    global foundedName
    global datalog

    #웹에 보낼 string 문자열
    datalog = str("%s name: %04s - time: %04d-%02d-%02d %02d:%02d:%02d "%(isFindPerson,foundedName,videoLocalTime.tm_year, videoLocalTime.tm_mon, videoLocalTime.tm_mday, videoLocalTime.tm_hour,videoLocalTime.tm_min, videoLocalTime.tm_sec))
  
    return datalog

#================================================================================DB
#현재 켜져있는 Cam의 ip 리스트를 반환하는 메소드
@app.route('/getCurrentCamIP')
def getCurrentCamIP():

    #DB에서 현재 켜져 있는 Cam IP 받아오기
    temp=DBController.DBController()
    iplist=temp.getAllCamIPTable()
    result=''
    for ss in iplist:
        result=result+"@"+ss

    #====================================
    return result
#================================================================================FileTcpCommunication
#사진 파일 받는 메소드
@app.route('/sendImageFile/<fliename>')
def sendImageFile(fliename):
    saveData(fliename,request.remote_addr,9009)
    return str(request.remote_addr)
    


#TCP를 이용해서 파일 다운 받는 함수
def saveData(filename,HOST,PORT):
    
    #test
    #filename='tt2.jpg'
    #=========
    data_transferred = 0
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST,PORT))
        print("1")
        #_ 파싱
        temp=''
        temp=filename
        df=chr(92)
        temp=temp.replace("_",df)
        print(temp)
        filename=temp
        print("2")
        #==============
        sock.sendall(filename.encode())
        #====파일 이름 추출
        s=os.path.split(filename)
        sname=s[1]
        print(sname)
        print(filename)
        global facepicturename
        facepicturename=sname
        #=======
        print("3")

        data = sock.recv(1024)
        if not data:
            print('파일[%s]: 서버에 존재하지 않거나 전송중 오류발생' %filename)
            return
 
        with open('face/' + sname, 'wb') as f:
            try:
                while  data:
                    f.write(data)
                    data_transferred += len(data)
                    print("앙")
                    data = sock.recv(1024)
            except Exception as e:
                print(e)
 
    print('파일[%s] 전송종료. 전송량 [%d]' %(filename, data_transferred))
    global facereencoding
    global deathflag
    deathflag=True
    facereencoding=True
    
    pass

#================================================================================
#test
with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'


#db_datalog()
if __name__ == '__main__':
    app.run(host='192.168.0.33', debug=True)
    