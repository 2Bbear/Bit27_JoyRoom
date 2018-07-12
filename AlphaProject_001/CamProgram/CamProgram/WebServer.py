#Libliry
from flask import Flask
from flask import request
from flask import jsonify
from werkzeug import secure_filename
from flask import render_template,Response
from operator import eq
import threading

import time
import cv2
import os
import mysql

#Team Libliry
import Video
import threading
import WebServer
#Custom Libliry
import Log as l

app = Flask(__name__)
fr=None



#======================================
def WebServerStart(hostip='220.90.196.192',_fr=None):
    l.L_Flow()
    global fr
    fr=_fr
    app.run(host=hostip, debug=False)

def SettingForCamProgrma(_instance=None):
    global targetinstance
    global ishavetargetinstance

    #받은 _instnace가 아무것도 없다면
    if _instance==None:
        return

    targetinstance=_instance
    ishavetargetinstance=True
    pass

#Route 메인 루트
@app.route('/')
def RouteMethod():
    l.L_Flow()
    return 'Web Server is Start'

#영상 전송===========================
def gen():
    l.L_Flow()
    global fr
    global istimer
    global isonece
    #frame avi로 변환
    num=0
    fps=20
    width=int(fr.camera.get(3))
    height=int(fr.camera.get(4))
    _saveavifilepath=str(num)+'.avi'#fr.save_videofile_path+fr.save_videofile_name+'.avi'
    out = cv2.VideoWriter(_saveavifilepath,cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width,height))

    while True:
        if isonece:
            fps=20
            width=int(fr.camera.get(3))
            height=int(fr.camera.get(4))
            _saveavifilepath=str(num)+'.avi'#fr.save_videofile_path+fr.save_videofile_name+'.avi'
            out = cv2.VideoWriter(_saveavifilepath,cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width,height))
            isonece=False
            

        jpg_bytes=fr.get_jpg_bytes()
        frame=fr.frame
        out.write(frame) # avi파일 만들기
        if istimer:
            out.release()
            istimer=False
        num=num+1
        if istimer:
            pass
        yield (b'--frame\r\n' 
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    l.L_Flow()
    #1분 타이머
    TimerSaveAvifile()
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


#==============================================================
INTERVER=10
istimer=False
isonece=False
#timer
def TimerSaveAvifile():
    l.L_Flow()
    global INTERVER
    global istimer
    global isonece
    t1=threading.Timer(INTERVER,TimerSaveAvifile)

    istimer=not istimer
    isonece=not isonece

    t1.start()
    