
import cv2
import numpy as np
from globals import MAX_LINE_GAP, MIN_LINE_LENGTH, THETA


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


def laneFinder(frame, sig=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(frame)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sig) * v))
    upper = int(min(255, (1.0 + sig) * v))
    edged = cv2.Canny(frame, lower, upper)
    # return the edged image
    return edged