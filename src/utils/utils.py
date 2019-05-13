
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


def laneFinder(frame, sig=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(frame)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sig) * v))
    upper = int(min(255, (1.0 + sig) * v))
    edged = cv2.Canny(frame, lower, upper)
    # return the edged image
    return edged


def roi(frame):
    imshape = frame.shape
    vertices = np.array([[(0, imshape[0]/1.5),
                          (450, 320), (800, 320),
                          (imshape[1], imshape[0]/1.1),
                          (imshape[1], imshape[0]),
                          (0, imshape[0])]
                         ], dtype=np.int32)
    mask = np.zeros(frame.shape, dtype=np.uint8)
    # filling pixels inside the polygon defined by
    # "vertices" with the fill color
    cv2.fillPoly(mask, vertices, (255, 255, 255))
    cv2.imshow('mask', mask)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # returning the image only where mask pixels are nonzero
    mask = cv2.bitwise_and(mask, frame)
    return mask
