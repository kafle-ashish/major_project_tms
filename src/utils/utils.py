
import os
import cv2
import math
import numpy as np
from globals import *


def save(frame, dir, name="untitled"):
    '''
        Saves specified frame into a directory.
        Parameters
        ----------
            @params: frame: Numpy Array
            @params: dir  : String
            @params: name : String
    '''
    if dir is not None:
        return cv2.imwrite(os.path.join(dir, name), frame)
    return cv2.imwrite(name, frame)


def video(dir, name="processed.mp4"):
    try:
        images = [img for img in os.listdir(dir) if img.endswith(".png")]
        frame = cv2.imread(os.path.join(
            FILE_DIR, "data", "processed", images[0]))
        height, width, layers = frame.shape

        video = cv2.VideoWriter(name, 0, 1, (width, height))

        for image in images:
            video.write(cv2.imread(os.path.join(
                FILE_DIR, "data", "processed", image)))
        return True
    except Exception as e:
        return False


def getCapture(device=0):
    '''
        Gets media capture from a device.
        Parameters
        ----------
            @params: device: Integer
            @returns: cap: Device capture
    '''
    cap = cv2.VideoCapture(device)
    if cap.isOpened():
        return cap


def getBoundingBoxes(contour, objects, frame):
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
    for (objectID, centroid), c in zip(objects.items(), contour):
        text = "ID {}".format(objectID)
        x, y, w, h = cv2.boundingRect(c)
        cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                    CV_FONT, 0.4, TEXT_COLOR, 1, CV_AA)
        cv2.circle(frame, (centroid[0], centroid[1]), 4, TEXT_COLOR, -1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), TEXT_COLOR, 2)
        # rect = cv2.minAreaRect(c)
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)
        # frame = cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
    return frame


def smoothContours(contours, thresh=1):
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
    try:
        contours, weights = cv2.groupRectangles(contours, thresh)
    except Exception as e:
        pass
    # if width of the contour is very high than it's
    # height then it is probably an error.
    contours = list(x for x in contours if cv2.boundingRect(x)
                    [2]/2.5 <= cv2.boundingRect(x)
                    [3] and cv2.contourArea(x) > 50)
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
    smooth = smoothContours(contours)
    return findHull(smooth)


def getBoxes(contour):
    '''
        Gets bounding boxes from contours.
        Parameters
        ----------
            @param: contour: List
            @returns: boxes: List
    '''
    if contour is None:
        return []
    boxes = []
    for c in contour:
        x, y, w, h = cv2.boundingRect(c)
        boxes.append((x, y, x+w, y+h))
    return boxes  # list(cv2.boundingRect(c) for c in contour)


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
    vertices = np.array([[(0, imshape[0]/1.3),
                          (350, 390),
                          (850, 390),
                          (imshape[1], imshape[0]),
                          (0, imshape[0])]
                         ], dtype=np.int32)
    mask = np.zeros(imshape, dtype=np.uint8)
    cv2.fillPoly(mask, vertices, (255, 255, 255))
    return cv2.bitwise_and(mask, frame)


def compare(array):
    '''
        Compares each and every element of an array with other.
        Parameters
        ----------
            @params: array: List
    '''
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            return array[i]-array[j]
