import cv2
import numpy as np

faceDectect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam = cv2.VideoCapture(0);
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("./recognizer/trainningData.yml")
id = 0
font = cv2.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,1,1,0,1)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
cv2.putText()
while(True):
    ret,img = cam.read();
    gray = cv2.cvtcolor(img,cv2.COLOR_BGR2GRAY)
    faces = facesDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        id,conf = rec.predect(gray[y:y+h,x:x+w])
        cv2.cv.PutText(cv2.cv.fromarray(img),str(id),(x,y+h),font,255);
    cv2.imshow("Faces",img);
    if(cv2.waitKey(1) == ord('q')):
        break;
cam.release()
cv2.destroyAllWindows()
