import cv2
import time
import handtrackingmodule as htm

cap= cv2.VideoCapture(0)
pTime=0
detector=htm.handDetector()

while True:
    success, vid= cap.read()
    vid= detector.detectHands(vid)
    lms= detector.findPosition(vid)
    print(lms)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(vid, str(int(fps)), (20,70), cv2.FONT_HERSHEY_TRIPLEX,2, (255,0,255), 1)

    cv2.imshow('Video',vid)
    cv2.waitKey(1)