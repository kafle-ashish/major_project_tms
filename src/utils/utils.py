
import numpy as np
import cv2


def getCapture(device=0):
    cap = cv2.VideoCapture(device)
    if cap.isOpened():
        return cap


def getBoundingBoxes(contour, frame, color=(0, 255, 0)):
    '''
        Draws rectangles around contours.
        Parameters
        ----------
            arg1: contour:List
            arg2: frame  :Numpy Array
            arg3: color  :RGB tuple
    '''
    err = 0
    for i, c in enumerate(contour):
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        if cv2.contourArea(c) < 30:
            print("error")
            err += 1
    return frame


def smoothContours(contours, thresh=3):
    '''
        Combines multiple bounding boxes into a single one.
        Parameters
        ----------
            arg1: contour: List
            arg2: thresh: Int
    '''
    if contours is None:
        return
    weights = []
    try:
        contours, weights = cv2.groupRectangles(contours, thresh)
    except Exception as e:
        pass
    contours = list(x for x in contours if cv2.contourArea(x) > 30)
    return contours


def findHull(contour):
    '''
        A function to calculate convex hull of contours.
        Parameters
        ----------
            @param: contour: List
    '''
    return list(cv2.convexHull(x) for x in contour)


def approximateContours(contours):
    return findHull(smoothContours(contours))


def getBoxes(contour):
    if contour is None:
        return []
    return list(cv2.boundingRect(c) for c in contour)


def laneFinder(frame):
    grey_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(grey_image, (kernel_size, kernel_size), 0)
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
    return edges
