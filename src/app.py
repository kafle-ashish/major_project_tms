import sys
import cv2
import numpy as np

from extractor import Extractors
from globals import FILE_DIR, IMG_DATA_DIR, VID_DATA_DIR
from utils import getCapture, getBoundingBoxes, approximateContours, getBoxes
from utils import laneFinder, roi, drawLanes

print('using OpenCV {}'.format(cv2.__version__))
cap = getCapture('{}/one.mp4'.format(VID_DATA_DIR))
ex = Extractors(roi(cap.read()[1]))


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
    while cap.isOpened():
        _, frame = cap.read()
        bounded_frame = detectLanes(frame)
        mask = roi(bounded_frame)
        lines = drawLanes(mask)
        for points in lines:
            cv2.line(frame, points[0], points[1], (255, 0, 0), 5)
        lines_edges = cv2.addWeighted(frame, 0.8, line_image, 1, 0)
        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()
