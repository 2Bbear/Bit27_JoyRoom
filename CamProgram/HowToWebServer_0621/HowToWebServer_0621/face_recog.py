# face_recog.py

import face_recognition
import cv2
import camera
import os
import numpy as np
import threading
import time

#--------------------------------------------------------------
import sys
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
import datetime

font = cv2.FONT_HERSHEY_SIMPLEX
#--------------------------------------------------------------

class FaceRecog():
    def __init__(self):

        self.camera = camera.VideoCamera()
         # Initialize some variables
        self.face_locations = [] #얼굴 위치 담는 배열
        self.face_encodings = [] #????
        self.face_names = [] #이름들
        self.process_this_frame = True #???

        self.known_face_encodings = []# 인코딩할 사진들 넣어둘 리스트
        self.known_face_names = [] #사진들 이름 넣어둘 리스트

        self.face = [] #상대방 이름
        self.dirname = 'face'
        self.files = os.listdir(self.dirname)       
        self.isfindperson=False#얼굴을 잡았을 경우 True
        self.videoLocalTime=time.localtime()

        #사진 담음
        for self.filename in self.files:                                      
            name, ext = os.path.splitext(self.filename)              
            if ext == '.jpg':                                       
                self.pathname = os.path.join(self.dirname, self.filename)
                self.img = face_recognition.load_image_file(self.pathname)
                self.face_encoding = face_recognition.face_encodings(self.img)[0] 
                self.known_face_encodings.append(self.face_encoding)
                self.known_face_names.append(name)
    
        
    def __del__(self):
        del self.camera

    def get_frame(self):
        #self.timer2 = threading.Timer(0.7,self.get_frame)#0.7초 간격으로 자신의 함수를 부르는 재귀함수?
        frame = self.camera.get_frame()
        
        now = datetime.datetime.now() # 시간 나타내기
        today = str("%d%d%d%d%d%d" %(now.year, now.month, now.day, now.hour, now.minute, now.second))
        self.small_frame = cv2.resize(frame, (0, 0), fx = 1, fy = 1 ) ####################################################### 원래 0.25
        self.rgb_small_frame = self.small_frame[:, :, ::-1]
         # Only process every other frame of video to save time

        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(self.rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(self.rgb_small_frame, self.face_locations)
        
            self.face_names = []
            for self.face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                self.matches = face_recognition.compare_faces(self.known_face_encodings, self.face_encoding)#얼굴 비교하는 부분
                self.name = "Unknown"
                #print(self.matches)

                # If a match was found in known_face_encodings, just use the first one.
                if True in self.matches:
                    self.first_match_index = self.matches.index(True)
                    self.name = self.known_face_names[self.first_match_index]
                self.face_names.append(self.name) #append : 리스트에 덧붙이는 형식
                print("%s님이 %d년 %d월 %d일 %d시 %d분 %d 초에 1번 카메라에서 발견되었습니다."%(self.name,now.year, now.month, now.day, now.hour, now.minute, now.second))
           
        self.process_this_frame = not self.process_this_frame

        if(self.face_locations):
            self.isfindperson= True
            self.videoLocalTime=time.localtime()
        else:
            self.isfindperson=False
            self.videoLocalTime=time.localtime()


        # Display the results
        for (self.x, self.y, self.w, self.h), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
 
            self.x *= 4 # top *= 4
            self.y *= 4 # right *= 4
            self.w *= 4 #  bottom *= 4
            self.h *= 4 # left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (self.h, self.x), (self.y, self.w), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (self.h, self.w - 35), (self.y, self.w), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (self.h + 6, self.w - 6), font, 1.0, (255, 255, 255), 1)
        return frame

        #self.timer2.start()
        
    def get_jpg_bytes(self):
        frame = self.get_frame()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()


