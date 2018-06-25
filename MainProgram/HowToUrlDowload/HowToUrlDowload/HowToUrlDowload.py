# load library
import urllib.request
import os
import cv2
import threading
# image url to download
url = "http://100.100.80.43:5000/video_feed"
path="D:/GitHub/bit27class/Bit27/Python/HowToUrlDowload/Videotest.png"
# file path and file name to download
outpath = "D:/GitHub/bit27class/Bit27/Python/HowToUrlDowload/Video/"
outfile = "test.png"

# Create when directory does not exist
if not os.path.isdir(outpath):
    os.makedirs(outpath)

while True:
    # download
    urllib.request.urlretrieve(url, outpath+outfile)

    #play
    #cv2.VideoWriter
    cam=cv2.VideoCapture(path)
    while True:
        try:
            ret_val, img = cam.read() # 캠 이미지 불러오기
            #cam.release()
            cv2.imshow("Cam Viewer",img) # 불러온 이미지 출력하기
            if cv2.waitKey(1) == 27:
                break  # esc to quit
            
        except :
            break

print("complete!")