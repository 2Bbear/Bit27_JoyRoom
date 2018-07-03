#Video.py
import cv2
import FaceRecog

class Video:
    frame = None
    camera = None
    def __init__(self,camnum):
       self.frame = []
       self.camera = cv2.VideoCapture(camnum)   
   #실제 필요한 함수이다.
    def Run(self):
                       
        useface = FaceRecog.FaceRecog()

        ret, self.frame = self.camera.read()                 
        self.frame = useface.FindFace(self.frame)  
        
    def get_jpg_bytes(self):
        self.Run()
        ret, jpg = cv2.imencode('.jpg', self.frame)
        return jpg.tobytes()

    def End(self):
        pass
