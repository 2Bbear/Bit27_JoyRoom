from flask import Flask
from flask import request
from werkzeug import secure_filename

from flask import Flask, render_template,url_for, Response
import face_recog
import time
import cv2
#import pymysql
import mysql.connector
from operator import eq
import threading

import DBController

app = Flask(__name__)
#변화 가능한 변수
rectangleColor=(0,0,255)
foundedName='UnKnown'
videoLocalTime=time.localtime()
isFindPerson=False
datalog = "nothing"
#영상 전송===========================
def gen(fr):
    global rectangleColor
    global isFindPerson
    global videoLocalTime
    global foundedName
    while True:
        fr.targetcolor=rectangleColor
        isFindPerson=fr.isfindperson
        foundedName = fr.name
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


#test
with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'


#db_datalog()
if __name__ == '__main__':
    app.run(host='192.168.137.1', debug=True)

