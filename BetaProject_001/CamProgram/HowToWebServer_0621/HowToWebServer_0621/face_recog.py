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
#--------------------------------------------------------------Tensorflow
import ColorAnal 

#--------------------------------------------------------------
showframe = [0] #전체
faceframe = [0] #얼굴
area = ()       #인식여부
clothflag=True
class FaceRecog():
    def __init__(self):
        #=====================================================================================================
        self.timer = 0
        self.timer2 = 0   
        self.camera = camera.VideoCamera()
     
        self.process_this_frame = True #???
        self.isfindperson=False#얼굴을 잡았을 경우 True
        self.face_locations = [] #얼굴 위치 담는 배열
        self.face_encodings = [] #????
        self.face_names = [] #이름들
        self.known_face_encodings = []# 인코딩할 사진들 넣어둘 리스트
        self.known_face_names = [] #사진들 이름 넣어둘 리스트   
        self.timer2 = 0

        self.dirname = 'face'
        self.name = "Unknown"

        self.videoLocalTime=time.localtime()
        self.newpicturename=''#새로 추가된 얼굴 사진 파일 이름
        self.reencodingflag=False # 다시 인코딩 하게 하는 플레그
        #=====================================================================================================
          
         
        self.files = os.listdir(self.dirname) #face라는 폴더의 파일이름 리스트  
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
        global clothflag
        self.frame = self.camera.get_frame()
        
        now = datetime.datetime.now()

        self.small_frame = cv2.resize(self.frame, (0, 0), fx = 1, fy = 1 )
        self.rgb_small_frame = self.small_frame[:, :, ::-1]

        if self.process_this_frame:
            self.face_locations = face_recognition.face_locations(self.rgb_small_frame)  
            self.face_encodings = face_recognition.face_encodings(self.rgb_small_frame, self.face_locations)   
            self.face_names = []

             #강제 타이머
            if self.timer > 10:
                
                for self.face_encoding in self.face_encodings:
                    self.matches = face_recognition.compare_faces(self.known_face_encodings, self.face_encoding)
                    if True in self.matches:
                        self.first_match_index = self.matches.index(True)
                        self.name = self.known_face_names[self.first_match_index]
                    self.face_names.append(self.name)
                    print("%s님이 %d년 %d월 %d일 %d시 %d분 %d 초에 1번 카메라에서 발견되었습니다."%(self.name,now.year, now.month, now.day, now.hour, now.minute, now.second))
          

                # Display the results
                for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):

                    cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 0, 255), 2)#얼굴 그리기
                    cv2.rectangle(self.frame, (left-150, top+380), (right+150, bottom), (0, 0, 255), 2)#몸 그리기


                    cv2.imwrite("original/%s_original.jpg" %self.name,self.frame)#전체크기의 사진 저장
                    origin_image = cv2.imread("original/%s_original.jpg" %self.name)#원본 사진 
                    trim_image_face = origin_image[top:bottom, left:right]
                    cv2.imwrite("face_capture/%s_face.jpg" %self.name,trim_image_face)


                    #cv2.imwrite("original/%s_bodyoriginal.jpg" %self.name,self.frame)#전체크기의 사진 저장
                    origin_image = cv2.imread("original/%s_original.jpg" %self.name)#원본 사진 
                    trim_image_body = origin_image[bottom:(5*bottom)-(4*top), (2*left)-(right):(2*right)-left]
                    cv2.imwrite("body_capture/%s_body.jpg" %self.name,trim_image_body)

                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(self.frame, name, (left, bottom-130), font, 1.0, (255, 255, 255), 1)
                    
                    if self.reencodingflag:
                        self.picturepath()

                    print(self.timer)
                    
                    self.timer = 0#함수 끝날 떄 초기화
                    
                    #옷 색 찾는 코드
                    if clothflag:
                        #answer=ColorAnal.ColorAnalysis(imagePath='D:/GitHub/Bit27_JoyRoom/BetaProject_001/CamProgram/HowToWebServer_0621/HowToWebServer_0621/body_capture/Kimmyeunghwan_body.jpg',
                        #                        modelFullPath='D:/GitHub/Bit27_JoyRoom/BetaProject_001/CamProgram/HowToWebServer_0621/HowToWebServer_0621/output_graph.pb',
                        #                       labelsFullPath='D:/GitHub/Bit27_JoyRoom/BetaProject_001/CamProgram/HowToWebServer_0621/HowToWebServer_0621/output_labels.txt')
                        ColorAnal.ColorAnalysis()
                        
                        clothflag=False

        self.timer +=1#타이머 돌기
        

        self.process_this_frame = not self.process_this_frame

        if(self.face_locations):
            self.isfindperson= True
            self.videoLocalTime=time.localtime()
        else:
            self.isfindperson=False
            self.videoLocalTime=time.localtime()

        return self.frame


    def picturepath(self):
            print("picturepath")
            #새로 생성된 이미지 파일을 분간하는 코드
            #
            #분간된 이미지 파일 이름으로 인코딩
            #인코딩 된 파일은 기존의 인코딩 배열에 추가

            
            self.name = "Unknown"
            

            self.filename=self.newpicturename# 새로 추가된 얼굴 사진 이름
            name=self.filename
            self.pathname = os.path.join(self.dirname, self.filename)
            self.img = face_recognition.load_image_file(self.pathname)
            self.face_encoding = face_recognition.face_encodings(self.img)[0] 
            self.known_face_encodings.append(self.face_encoding)
            self.known_face_names.append(name)
            self.reencodingflag=False
   

    def get_jpg_bytes(self):
        frame = self.get_frame()
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()


