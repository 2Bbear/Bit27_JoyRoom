#FaceRecog.py
import cv2
import face_recognition
import os
import numpy as np
import time

#얼굴의 정보를 담는 클래스
class FaceInfo():
    location={'x':0,'y':0,'w':0,'h':0}
    name=''
    isthere=False

    def __init__(self):
        pass
    



class FaceRecog:
    faceinfo_list=list()#현재 잡힌 얼굴을 저장하는 리스트
    errorbound=100#얼굴을 잡는 범위
    known_face_encodings = []#저장된 사진을 인코딩한 배열
    known_face_names = []#저장된 사진에 따른 이름을 저장하는 배열
    
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    def __init__(self):
        #사진 인코딩하기
        self.EncodingFacePicture(_dirname='targetface')
        #
        self.facecascade = cv2.CascadeClassifier()
        self.facecascade.load('haarcascade_frontface.xml')
        #

    def __del__(self):
        del self.faceinfo_list

    #얼굴을 찾는 함수
    def FindFace(self, _nowframe):
        small_frame=cv2.resize(_nowframe, (0, 0), fx=0.5, fy=0.5)
        
        grayframe = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        grayframe = cv2.equalizeHist(grayframe)
        #Conver the image from bgr color to rgb color
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Only process every other frame of video to save time
        if self.process_this_frame:
            #얼굴 메모리 초기화
            for target in self.faceinfo_list:
                target.isthere=False
            #얼굴들의 위치 찾아내기
            #self.face_locations = self.facecascade.detectMultiScale(grayframe, 1.1, 3, 0, (30, 30))
            #self.face_locations=self.ConvertDirListToTupleList(self.face_locations)
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            ##만약 얼굴 잡힌것이 아무것도 없다면 기존의 메모리를 초기화 함
            #if len(self.face_locations)<=0:
            #    self.faceinfo_list.clear()
            #    print(len(self.face_locations))
            #    print('삭제')

            #전에 있는 얼굴 위치와 겹치는 부분 제거
            for temp_faceinfo in self.faceinfo_list:#기존의 얼굴 위치
                for temp_facelocation in self.face_locations:#새로운 얼굴 위치
                    if(temp_faceinfo.location[0]-self.errorbound<=temp_facelocation[0] and temp_faceinfo.location[0]+self.errorbound>=temp_facelocation[0]) and (temp_faceinfo.location[1]-self.errorbound<=temp_facelocation[1] and temp_faceinfo.location[1]+self.errorbound>=temp_facelocation[1]):
                        
                        temp_faceinfo.location=temp_facelocation
                        
                        self.face_locations.remove(temp_facelocation)
                        temp_faceinfo.isthere=True
                        pass
            self.face_locations=self.ConvertDirListToTupleList(self.face_locations)
            #print(self.face_locations)
            #전에 있는 얼굴 제거하면 결국 location에 남는게 없으면 encodings 또한 비어 있게 된다.
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

           

            self.face_names = []

            #비어 있다면 넘어감
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
            #만약 뭔가 인코딩 할게 남아 있다. 즉 전에 있던 얼굴이 아니라 다른 얼굴이 있을 경우 새로운 얼굴을 추가함
            if len(self.face_encodings)>0:
                for i in range(len(self.face_names)):
                    t_faceinfo=FaceInfo()
                    t_faceinfo.name=self.face_names[i]
                    t_faceinfo.location=self.face_locations[i]
                    t_faceinfo.isthere=True
                    self.faceinfo_list.append(t_faceinfo)
                    print('추가함')
            
        self.process_this_frame = not self.process_this_frame

        #현재 frame에 있지 않은 얼굴은 삭제
        for target in self.faceinfo_list:
            if target.isthere==False:
                self.faceinfo_list.remove(target)
                print('삭제함')


        # Display the results
        for temp in self.faceinfo_list:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top = 2*temp.location[0]
            right = 2*temp.location[1]
            bottom = 2*temp.location[2]
            left = 2*temp.location[3]

            # Draw a box around the face
            cv2.rectangle(_nowframe, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(_nowframe, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(_nowframe, temp.name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
     
        ##Frmae에 그림을 그리는 부분
        #for (x,y,w,h) in self.face_locations:
        #    #사각형 그리기
        #    cv2.rectangle(nowframe,(x*4,y*4),((x+w)*4,(y+h)*4),(0,255,0),3, 4, 0)
        #    #이름 출력하기
        #pass
        

        return _nowframe

    #딕셔너리 리스트를 튜플 리스트로 변환하는 함수
    def ConvertDirListToTupleList(self,_dirlist):
        result=list()
        for (x,y,w,z) in _dirlist:
            result.append((x,y,w,z))
            
        

        return result
        
    #인코딩을 하는 함수
    def EncodingFacePicture(self,_dirname='knowns'):
        # Load sample pictures and learn how to recognize it.
        dirname = _dirname
        files = os.listdir(dirname)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.png':
                self.known_face_names.append(name)
                pathname = os.path.join(dirname, filename)
                img = face_recognition.load_image_file(pathname)
                face_encoding = face_recognition.face_encodings(img)[0]
                self.known_face_encodings.append(face_encoding)
       
        pass

