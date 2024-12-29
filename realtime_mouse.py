import HandTrackingFunctionalP as htm
import cv2 as cv
import numpy as np
import time
import os
import pyautogui as py
import math

cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 832)

print(py.size())

detector=htm.HandDetector()

while True:
    isTrue, img = cap.read()
    img=cv.flip(img,1)
    fingers=[]
    tipIds = [4, 8, 12, 16, 20]

    img=detector.showPoints(img)
    lm=detector.returnPoints(img)

    if len(lm)!=0:
        x1,y1=lm[8][1:] #Index Finger
        x2,y2=lm[12][1:] #Middle Finger

        if (lm[tipIds[0]][1] < lm[tipIds[0] - 1][1]):
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
        # Fingers
            if (lm[tipIds[id]][2] < lm[tipIds[id] - 2][2]):
                fingers.append(1)
            else:
                fingers.append(0)

        if fingers[1] and fingers[2]==False:
            cv.circle(img, (x1, y1), 15, (0,255,0), -1)
            x3=np.interp(x1,(0,1280),(0,1280))
            y3=np.interp(y1,(0,832),(0,832))
            py.moveTo(x3,y3)

        if fingers[1] and fingers[2]:
            cv.circle(img, (x1, y1), 15, (0,0,255), -1)
            cv.circle(img, (x2, y2), 15,(0,0,255), -1)

            cv.line(img,(x1,y1),(x2,y2),(0,255,0),4)
            length = math.hypot(x2 - x1, y2 - y1)

            if length<95:
                py.click(x1,y1)


    cv.imshow("Virtual Mouse", img)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
