
import cv2
import numpy as np
from globals import MAX_LINE_GAP, MIN_LINE_LENGTH, THETA


def getCapture(device=0):
    cap = cv2.VideoCapture(device)
    if cap.isOpened():
        return cap


def getBoundingBoxes(contour, frame, color=(0, 255, 0)):
    '''
        Draws rectangles around contours.
        Parameters
        ----------
            @param: contour: List
            @param: frame  : Numpy Array
            @param: color  : RGB tuple
            @return frame: List
                Numpy array of an image.
    '''
    for c in contour:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
    return frame


def smoothContours(contours, thresh=3):
    '''
        Combines multiple bounding boxes into a single one.
        Parameters
        ----------
            @param: contour: List
            @param: thresh: Int
            @return contour: List
                Array of smoothed contours.
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
            @return hull: List
                Array of convex hulls.
    '''
    return list(cv2.convexHull(x) for x in contour)


def approximateContours(contours):
    return findHull(smoothContours(contours))


def getBoxes(contour):
    if contour is None:
        return []
    boxes = []
    for c in contour:
        x, y, w, h = cv2.boundingRect(c)
        boxes.append((x, y, x+w, y+h))
    return boxes  # list(cv2.boundingRect(c) for c in contour)


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
    '''
        Extracts a region of interest from given frame.
        Parameters
        ----------
            @param frame: List
                Numpy array of an image.
            @return frame: List
                Numpy array of an image.
    '''
    imshape = frame.shape
    vertices = np.array([[(0, imshape[0]/1.5),
                          (450, 320),
                          (800, 320),
                          (imshape[1], imshape[0]/1.1),
                          (imshape[1], imshape[0]),
                          (0, imshape[0])]
                         ], dtype=np.int32)
    mask = np.zeros(frame.shape, dtype=np.uint8)
    cv2.fillPoly(mask, vertices, (255, 255, 255))
    return cv2.bitwise_and(mask, frame)


def drawLanes(frame, rho=1, threshold=40):
    '''
        Draws possible lanes from an edged frame.
        Parameters
        ----------
            @param frame: List
                Numpy array of an image.
            @param rho: Number
                Distance resolution in pixels of the Hough grid.
            @param threshold: Number
                Minimum number of votes/intersections in Hough grid cell.
            @return points: List
                Numpy array of line points.
    '''
    # creating a blank to draw lines on
    lines = cv2.HoughLinesP(frame, rho, THETA, threshold,
                            np.array([]), MIN_LINE_LENGTH, MAX_LINE_GAP)
    points = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            points.append([(x1, y1), (x2, y2)])
    return points
