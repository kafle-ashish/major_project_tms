
import cv2


def getBoundingBoxes(contour, frame, color=(0, 255, 0)):
    '''
        Draws rectangles around contours.
        Parameters
        ----------
            arg1: contour:List
            arg2: frame  :Numpy Array
            arg3: color  :RGB tuple
    '''
    for c in contour:
        x, y, w, h = cv2.boundingRect(c)
        print((x, y), (x+w, y+h))
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
    # contours = list(x for x in contours if cv2.contourArea(x) > 50)
    return contours, weights
