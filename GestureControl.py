import cv2
import time
import handtrackingmodule as htm
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


cap= cv2.VideoCapture(0)
pTime=0
detector=htm.handDetector(detection_confidence=0.95)

device = AudioUtilities.GetSpeakers()
interface= device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
Range= volume.GetVolumeRange()

interpreted_vol_bar= 380
volume_percentage=0

while True:
    success, vid= cap.read()
    vid= detector.detectHands(vid, False)
    lms= detector.findPosition(vid)
    if len(lms)!=0:
        thumb_x, thumb_y= lms[4][1], lms[4][2]
        index_x, index_y= lms[8][1], lms[8][2]

        cv2.line(vid, (thumb_x, thumb_y), (index_x, index_y), (255,255, 0), 2)
        length= math.hypot(thumb_x-index_x, thumb_y-index_y)
        interpreted_vol= np.interp(length, [40,250], [Range[0],Range[1]])
        interpreted_vol_bar= np.interp(length, [40,250], [380,580])
        volume_percentage= np.interp(length, [40,250], [0,100])
        volume.SetMasterVolumeLevel(interpreted_vol, None)

    cv2.rectangle(vid,(380,430),(580,450), (128,128,128),3)
    cv2.line(vid, (380,440), (int(interpreted_vol_bar),440), (255,255,0),3)
    cv2.circle(vid, (int(interpreted_vol_bar),440), 10, (255,255,0), cv2.FILLED)
    cv2.putText(vid, f'{int(volume_percentage)}%', (590, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0),2)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(vid, f'FPS:{(int(fps))}', (20,50), cv2.FONT_HERSHEY_SIMPLEX,1, (255,255,0), 2)

    cv2.imshow('Video',vid)
    cv2.waitKey(1)
