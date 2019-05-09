

import cv2
import numpy as np
import os

from extractor import Extractors
from utils import getBoundingBoxes, nonMaxSuppression

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
VID_DATA_DIR = os.path.join(FILE_DIR, 'data', 'video')
IMG_DATA_DIR = os.path.join(FILE_DIR, 'data', 'image')


def getCapture(device=0):
    cap = cv2.VideoCapture(device)
    if cap.isOpened():
        return cap


if __name__ == '__main__':
    cap = getCapture('{}/one.mp4'.format(VID_DATA_DIR))
    _, frame = cap.read()
    ex = Extractors(frame)

    while True:
        _, frame = cap.read()

        subtracted = ex.extractForeground(frame)
        contours, _ = cv2.findContours(
            subtracted, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        bounded_frame = getBoundingBoxes(contours, frame)
        cv2.imshow('image', bounded_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()
