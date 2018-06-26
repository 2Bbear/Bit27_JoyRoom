from flask import Flask
from flask import request
from werkzeug import secure_filename

from flask import Flask, render_template,url_for, Response
import face_recog
import time
import cv2

app = Flask(__name__)
#변화 가능한 변수
rectangleColor=(0,0,255) # 하이라이트 사각형 색상

foundedName='UnKnown' # 찾은 이름
findName='UnKnown' # 찾을 이름
isFindPerson=False  # 사람을 찾았는가?

foundedClothes='nonClothes' # 찾은 옷의 이름
findClothes='nonClothes' #찾을 옷의 이름
foundedClothesColor='nonColor' #찾은 옷의 색상
findClothesColor='nonColor' #찾을 옷의 색상
isFindClothes=False # 옷을 찾았는가?

videoLocalTime=time.localtime() #로그 값에 남을 시간

#영상 전송===========================
def gen(fr):
    global rectangleColor
    global isFindPerson
    global videoLocalTime
    while True:
        fr.targetcolor=rectangleColor
        isFindPerson=fr.isfindperson
        videoLocalTime=fr.videoLocalTime
        jpg_bytes = fr.get_jpg_bytes()
        yield (b'--frame\r\n' 
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(face_recog.FaceRecog()), mimetype='multipart/x-mixed-replace; boundary=frame')
#====================================
#Route
@app.route('/')
def hello_world():
    return render_template('index.html')


#main 기본 메서드
@app.route('/mainService')
def mainService():
    return "빰빠빰빠밤"
#================================================================
#찾은 옷의 색상을 반환하는 함수
@app.route('/getFindedClothesColor')
def getFindedClothesColor():
    global foundedClothesColor
    return '%s' %foundedClothesColor

#찾을 옷의 색상을 변경하는 함수
@app.route('/changeFindClothesColor/<clothescolor>')
def changeFindClothesColor(clothescolor):
    global findClothesColor
    findClothesColor=clothescolor
    return 'changed find clothes color is %s' %findClothesColor

#찾은 옷의 이름을 반환하는 함수
@app.route('/getFindedClothes')
def getFindedClothes():
    global foundedClothes
    return '%s' %foundedClothes

#찾을 옷의 이름을 변경하는 함수
@app.route('/changeFindClothes/<clothesname>')
def changeFindClothes(clothesname):
    global findClothes
    findClothes=clothesname
    return 'changed find clothes name is %s' %findClothes

#찾은 사람의 이름을 반환하는 함수
@app.route('/getFindedPersonName')
def getFindedPersonName():
    global foundedName
    return '%s' %foundedName

#찾을 사람 이름을 변경하는 메소드
@app.route('/changeFindName/<personname>')
def changeFindName(personname):
    global findName
    findName=personname
    return 'changed find person name is %s' %findName

#색상변경하는 메소드
@app.route('/changeRectangleColor/<targetcolor>')
def changeRectangleColor(targetcolor):
    global rectangleColor
    if targetcolor=='blue':
        rectangleColor=(255,0,0)
    elif targetcolor=='green':
        rectangleColor=(0,255,0)
    elif targetcolor=='red':
        rectangleColor=(0,0,255)
    
    return 'User' 

#색상변경하는 메소드2
@app.route('/changeRectangleColor2/<int:a>/<int:b>/<int:c>')
def changeRectangleColor2(a,b=None,c=None):
    global rectangleColor
    rectangleColor=(a,b,c)
    if rectangleColor:
        return 'true'
    else:
        return 'false'
    return 'false'

#숫자 매개변수 넘기기
@app.route('/printAge/<int:post_id>')
def printAge(post_id):
    return 'Post %d d' % post_id

#사람 찾은 로그 남기는 메소드
@app.route('/getCurrentLog')
def getCurrentLog():
    global videoLocalTime
    global isFindPerson
    return "%s time: %04d-%02d-%02d %02d:%02d:%02d "%(isFindPerson,videoLocalTime.tm_year, videoLocalTime.tm_mon, videoLocalTime.tm_mday, videoLocalTime.tm_hour,videoLocalTime.tm_min, videoLocalTime.tm_sec)

#test
with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'


if __name__ == '__main__':
    #app.run(host='192.168.137.1', debug=True)
    app.run(host='100.100.80.51', debug=True)
