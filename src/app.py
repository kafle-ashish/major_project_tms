import cv2
import numpy as np

from extractor import Extractors
from globals import FILE_DIR, IMG_DATA_DIR, VID_DATA_DIR
from utils import getCapture, getBoundingBoxes, smoothContours

if __name__ == '__main__':
    cap = getCapture('{}/one.mp4'.format(VID_DATA_DIR))
    _, frame = cap.read()
    ex = Extractors(frame)

    while True:
        _, frame = cap.read()

        subtracted = ex.extractForeground(frame)

        contours, _ = cv2.findContours(
            subtracted, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        contours, _ = smoothContours(contours)

        bounded_frame = getBoundingBoxes(contours, frame)
        cv2.imshow('image', bounded_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()
