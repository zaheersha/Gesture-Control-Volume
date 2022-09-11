import imp
from tkinter.messagebox import NO
from handdetector import HandDetector
import cv2
import math
import time
import numpy as np
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume


devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))

handDetector=HandDetector(min_detection_confidence=0.7)
cam=cv2.VideoCapture(0)
oldDistance=0
while True:
    status,image=cam.read()
    if status:
        result=handDetector.findHandLandMarks(image=image,draw=True)
        print(result)
        if result is not None:
            x1,y1=result[4][1],result[4][2]
            x2,y2=result[8][1],result[8][2]
            distance=math.hypot(x2-x1,y2-y1)
            print(distance)
            if distance!=oldDistance:
                oldDistance=distance
                time.sleep(0.005)
            else:
                pass
            volumeValue=np.interp(oldDistance,[50,250],[-65.25,0.0])
            volume.SetMasterVolumeLevel(volumeValue,None)
            cv2.circle(image,(x1,y1),15,(255,0,255),cv2.FILLED)
            cv2.circle(image,(x2,y2),15,(255,0,255),cv2.FILLED)
            cv2.line(image,(x1,y1),(x2,y2),(255,0,255),3)
            cv2.imshow('result',image)
        #cv2.imshow('hands',image)
        cv2.waitKey(1)