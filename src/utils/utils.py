
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
    # print(len(contour))
    for c in contour:
        # epsilon = cv2.arcLength(c, True)/1000000
        # approx = cv2.approxPolyDP(c, epsilon, True)
        # cv2.drawContours(frame, [approx], -1, color, 3)
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
    return frame


def smoothContours(contours, thresh=1):
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
    return contours, weights
