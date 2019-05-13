import sys
import cv2
import numpy as np

from extractor import Extractors
from globals import FILE_DIR, IMG_DATA_DIR, VID_DATA_DIR
from utils import getCapture, getBoundingBoxes, approximateContours, getBoxes
from utils import laneFinder, roi
print('using OpenCV {}'.format(cv2.__version__))
cap = getCapture('{}/one.mp4'.format(VID_DATA_DIR))
ex = Extractors(roi(cap.read()[1], []))


def detectVehicles(frame):
    subtracted = ex.extractForeground(frame)
    contours, _ = cv2.findContours(
        subtracted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    hulls = approximateContours(contours)
    # boxes = getBoxes(hulls)
    return getBoundingBoxes(hulls, frame)


def detectLanes(frame):
    background = ex.extractBackground(frame)
    return laneFinder(background)


if __name__ == '__main__':
    while True:
        _, frame = cap.read()
        bounded_frame = detectLanes(frame)
        mask = roi(bounded_frame, [])
        cv2.putText(mask,
                    'FPS: {}'.format(int(cap.get(cv2.CAP_PROP_FPS))),
                    (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.25,
                    (255, 255, 255),
                    lineType=cv2.LINE_AA)
        cv2.imshow('image', mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()
