# load library
import urllib.request
import os
import cv2
import threading
from time import sleep

# image url to download
url = "http://100.100.80.43:5000/video_feed"
path="D:/GitHub/bit27class/Bit27/Python/HowToUrlDowload/Videotest.png"
# file path and file name to download
outpath = "D:/GitHub/bit27class/Bit27/Python/HowToUrlDowload/"
outfile = "Videotest.png"

# image url to download
url2 = "http://100.100.80.44:5000/video_feed"
path2="D:/GitHub/bit27class/Bit27/Python/HowToUrlDowload/Videotest2.png"
# file path and file name to download
outpath2 = "D:/GitHub/bit27class/Bit27/Python/HowToUrlDowload/"
outfile2 = "Videotest2.png"

# Create when directory does not exist
if not os.path.isdir(outpath):
    os.makedirs(outpath)



def DownloadVideo():
    # download
    urllib.request.urlretrieve(url, outpath+outfile)

def DownloadVideo2():
    # download
    urllib.request.urlretrieve(url2, outpath2+outfile2)

def PlayVideo():
    #play
    #cv2.VideoWriter
    cam=cv2.VideoCapture(path)
    ret_val, before = cam.read() # 캠 이미지 불러오기
    while True:
        sleep(0.03)
        try:
            ret_val, img = cam.read() # 캠 이미지 불러오기
            #cam.release()
            cv2.imshow("Cam Viewer",img) # 불러온 이미지 출력하기
            if cv2.waitKey(1) == 27:
                break  # esc to quit
            
        except :
            break


def PlayVideo2():
    #play
    #cv2.VideoWriter
    cam2=cv2.VideoCapture(path2)
   
    while True:
        sleep(0.03)
        try:
            ret_val, img2 = cam2.read() # 캠 이미지 불러오기
            #cam.release()
            cv2.imshow("Cam Viewer",img2) # 불러온 이미지 출력하기
            if cv2.waitKey(1) == 27:
                break  # esc to quit
            
        except :
            break
          

# main
t=threading.Thread(target=DownloadVideo,args=())
t.daemon=True
t.start()

t2=threading.Thread(target=DownloadVideo2,args=())
t2.daemon=True
t2.start()

sleep(2)

try:
    t3=threading.Thread(target=PlayVideo2,args=())
    t3.daemon=True
    t3.start()
except :
    pass

try:
    PlayVideo()
    print("complete!")
except :
    sleep(4)
    pass
   
