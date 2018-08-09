#FaceRecog.py
import cv2
import face_recognition
import os
class FaceRecog:

    #얼굴 객체 
    detectedface=list()
    known_face_encodings=[]
    known_face_names=[]
    foundfacecount=1
    def __init__(self):
        #얼굴 인코딩
        self.MakeFaceEncode()
        #

        self.facecascade = cv2.CascadeClassifier()
        self.facecascade.load('haarcascade_frontface.xml')

        
    def MakeFaceEncode(self):
        # Load sample pictures and learn how to recognize it.
        dirname = 'knownsface'
        files = os.listdir(dirname)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.png':
                self.known_face_names.append(name)
                pathname = os.path.join(dirname, filename)
                img = face_recognition.load_image_file(pathname)
                face_encoding = face_recognition.face_encodings(img)[0]
                self.known_face_encodings.append(face_encoding)

    def RecognitionFace(self,small_frame,facelocation):
        rgb_small_frame = small_frame[:, :, ::-1]
        # Find all the faces and face encodings in the current frame of video
        
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, facelocation)
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

                return name
        pass

    def FindFace(self, nowframe):
        smalframe=cv2.resize(nowframe, (0, 0), fx=0.25, fy=0.25)
        grayframe = cv2.cvtColor(smalframe, cv2.COLOR_BGR2GRAY)
        grayframe = cv2.equalizeHist(grayframe)
        faces = self.facecascade.detectMultiScale(grayframe, 1.1, 3, 0, (30, 30))
        errorbound=20
        tempfacelocation=None
        failcount=1
        tempx=0
        tempy=0

        #
        
        #
        for (x,y,w,h) in faces:#한프레임에 찾은 총 얼굴
            tempname=''
            
            #객체 위치 파악
            if len(self.detectedface)>0:
                for target in self.detectedface:
                    #영역에 들어오는지 확인
                   
                    if (target['x']-errorbound<=x and target['x']+errorbound>=x) and (target['y']-errorbound<=y and target['y']+errorbound>=y):
                        print('근접함')
                        target['x']=x
                        target['y']=y
                        tempname=str(target['index'])
                        target['isthere']=True

                        cv2.rectangle(nowframe,(x*4,y*4),((x+w)*4,(y+h)*4),(0,255,0),3, 4, 0)
                        #객체 이름 출력하기

                        font = cv2.FONT_HERSHEY_DUPLEX
                        
                        name=tempname
                        cv2.putText(nowframe, name, (x*4 + 6, y*4 - 6), font, 1.0, (255, 255, 255), 1)
                        break;
                    else:
                        print('다름')
                        failcount+=1
                        tempx=x
                        tempy=y

                if len(self.detectedface)<failcount:
                    tempfacelocation={'x':tempx,'y':tempy,'index':self.foundfacecount,'name':'','ishavename':False}
                    print('추추추가')
                print(str(self.foundfacecount))
            #배열속 찾은 얼굴이 아무것도 없을 때
            else:
                self.detectedface.append({'x':x,'y':y,'index':self.foundfacecount,'name':'','ishavename':False})
                self.foundfacecount+=1
                print('얼굴추가')

        if tempfacelocation!=None:
            self.detectedface.append(tempfacelocation)
            self.foundfacecount+=1

        
                
        
        return nowframe

    def isInthere(self,area,x,y,w,h):
        result=False

        return result

