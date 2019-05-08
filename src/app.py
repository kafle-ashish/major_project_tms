

import cv2
import numpy as np
import os
from background_sub import Extratcors

def getCapture(device=0):
    cap = cv2.VideoCapture(device)
    if cap.isOpened():
        return cap

if __name__ == '__main__':

    cap = getCapture('testTwo.mp4')
    _, frame = cap.read()
    ex = Extratcors(frame)

    while True:
        _, frame = cap.read()
        
        subtracted = ex.extractBackground(frame)
        cv2.imshow('image', subtracted)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()