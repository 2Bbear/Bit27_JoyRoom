# face_recog.py

import face_recognition
import cv2
import camera
import os
import numpy as np
import threading
import time
def MyThread(self):
    self.face_locations = face_recognition.face_locations(self.rgb_small_frame)
    self.face_encodings = face_recognition.face_encodings(self.rgb_small_frame, self.face_locations)
    pass
class FaceRecog():
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.camera = camera.VideoCamera()

        self.known_face_encodings = []
        self.known_face_names = []
        
        

        # Load sample pictures and learn how to recognize it.
        dirname = 'knowns'
        files = os.listdir(dirname)
        #폴더 안에 있는 모든 이미지를 얼굴 특징을 분석한 데이터로 저장
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.jpg':
                self.known_face_names.append(name)
                pathname = os.path.join(dirname, filename)
                img = face_recognition.load_image_file(pathname)#이미지 파일 불러오기
                face_encoding = face_recognition.face_encodings(img)[0]#얼굴 특징 분석
                self.known_face_encodings.append(face_encoding)#각 파일별로 분석된 특징을 저장

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.currenttimer=0;
        self.process_this_frame = True
        #CustomValue
        self.isfindperson=False#얼굴을 잡았을 경우 True
        self.targetcolor=(0, 0, 255) #얼굴을 잡았을때 생성되는 사각형의 색상
        self.videoLocalTime=time.localtime()
        
        

    def __del__(self):
        del self.camera

    def get_frame(self):
        # Grab a single frame of video
        frame = self.camera.get_frame()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        self.rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        
        #if self.process_this_frame:
        if self.currenttimer>10:
            # Find all the faces and face encodings in the current frame of video
            
            #t=threading.Thread(target=MyThread,args=(self,))
            #t.start()
            self.face_locations = face_recognition.face_locations(self.rgb_small_frame)
            #self.face_encodings = face_recognition.face_encodings(self.rgb_small_frame, self.face_locations)
            
            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                min_value = min(distances)

                # tolerance: How much distance between faces to consider it a match. Lower is more strict.
                # 0.6 is typical best performance.
                name = "Unknown"
                if min_value < 0.6:
                    index = np.argmin(distances)
                    name = self.known_face_names[index]
                    
               

                self.face_names.append(name)
                self.currenttimer=0

        self.currenttimer=self.currenttimer+1
        self.process_this_frame = not self.process_this_frame

        if(self.face_locations):
            self.isfindperson= True
            self.videoLocalTime=time.localtime()
        else:
            self.isfindperson=False
            self.videoLocalTime=time.localtime()

        # 얼굴 사각형만 출력
        for (top, right, bottom, left) in self.face_locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom),  self.targetcolor, 2)

        # Display the results
        #for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
        #    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        #    top *= 4
        #    right *= 4
        #    bottom *= 4
        #    left *= 4

        #    # Draw a box around the face
        #    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        #    # Draw a label with a name below the face
        #    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        #    font = cv2.FONT_HERSHEY_DUPLEX
        #    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        #    beforName=name

        return frame

    def get_jpg_bytes(self):
        frame = self.get_frame()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()


