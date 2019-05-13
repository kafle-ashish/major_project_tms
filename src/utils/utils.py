
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
    for i, c in enumerate(contour):
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
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
