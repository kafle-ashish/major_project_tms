import cv2
import numpy as np

from extractor import Extractors
from globals import FILE_DIR, IMG_DATA_DIR, VID_DATA_DIR
from utils import getCapture, getBoundingBoxes, smoothContours, findHull

print('using OpenCV {}'.format(cv2.__version__))
if __name__ == '__main__':
    cap = getCapture('{}/one.mp4'.format(VID_DATA_DIR))
    _, frame = cap.read()
    ex = Extractors(frame)

    while True:
        print('FPS: {}'.format(int(cap.get(cv2.CAP_PROP_FPS))))
        _, frame = cap.read()

        subtracted = ex.extractForeground(frame)

        contours, _ = cv2.findContours(
            subtracted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = smoothContours(contours)
        hulls = findHull(contours)
        bounded_frame = getBoundingBoxes(hulls, frame)
        cv2.imshow('image', bounded_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()
