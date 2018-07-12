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

#Custom Libliry
import Log as l

app = Flask(__name__)
cm=None
#======================================
def WebServerStart(_cm,_host='220.90.196.192'):
    l.L_Flow()
    global cm
    cm=_cm
    app.run(host=_host, debug=False)
    
    

#Route 메인 루트
@app.route('/')
def RouteMethod():
    l.L_Flow()
    return 'Web Server is Start'

#영상 전송===========================
def gen():
    l.L_Flow()
    global cm
    
    while True:
        jpg_bytes=cm.get_jpg_bytes()
        yield (b'--frame\r\n' 
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    l.L_Flow()
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')