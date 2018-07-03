#FaceRecog.py
import cv2


class FaceRecog:
    def __init__(self):
        self.facecascade = cv2.CascadeClassifier()
        self.facecascade.load('haarcascade_frontface.xml')
    
    def FindFace(self, nowframe):
        grayframe = cv2.cvtColor(nowframe, cv2.COLOR_BGR2GRAY)
        grayframe = cv2.equalizeHist(grayframe)
        faces = self.facecascade.detectMultiScale(grayframe, 1.1, 3, 0, (30, 30))
        for (x,y,w,h) in faces:
            cv2.rectangle(nowframe,(x,y),(x+w,y+h),(0,255,0),3, 4, 0)

        return nowframe

