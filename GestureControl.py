import cv2
import time
import handtrackingmodule as htm
import math
import numpy as np

cap= cv2.VideoCapture(0)
pTime=0
detector=htm.handDetector(detection_confidence=0.95)

while True:
    success, vid= cap.read()
    vid= detector.detectHands(vid)
    lms= detector.findPosition(vid)
    if len(lms)!=0:
        thumb_x, thumb_y= lms[4][1], lms[4][2]
        index_x, index_y= lms[8][1], lms[8][2]

        cv2.line(vid, (thumb_x, thumb_y), (index_x, index_y), (255,0,255), 2)
        length= math.hypot(thumb_x-index_x, thumb_y-index_y)
        print(length)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(vid, f'FPS:{(int(fps))}', (20,50), cv2.FONT_HERSHEY_COMPLEX_SMALL,1.5, (255,0,255), 1)

    cv2.imshow('Video',vid)
    cv2.waitKey(1)
