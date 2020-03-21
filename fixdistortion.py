import cv2
import numpy


cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    np_img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    cv2.imshow('',np_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('distortion1.jpg',np_img)
cap.release()