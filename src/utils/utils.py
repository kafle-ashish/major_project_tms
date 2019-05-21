
import os
import cv2
import math
import numpy as np


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
        return cv2.imsave(os.path.join(dir, name), frame)
    return cv2.imsave(name, frame)


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
                          (450, 320),
                          (770, 320),
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
            print(array[i], array[j], '\n')


def averageLines(lines, prop):
    '''
        Averages over a list of line points.
        Parameters
        ----------
            @params: lines: List of lines
    '''
    angles = []
    for line in lines:
        params = np.polyfit(line[0], line[1], 1)
        angles.append((math.degrees((math.atan(params[0]))), params[1]))
    angles.sort()
    # print(angles)
    return averageSlopes(angles, prop)


def averageSlopes(angles, prop, threshold=7):
    head = angles[0][0]
    buffer = []
    temp = []
    for angle, intercept in angles[1:]:
        if angle >= 86 and angle < 120:
            continue
        if angle-head <= threshold:
            # print("Threshold has been met.....")
            temp.append((angle, intercept))
        else:
            if len(temp) == 0:
                # print("Threshold exceeded. Temp is empty...")
                buffer.append([(angle, intercept)])
            else:
                # print("Threshold exceeded....")
                buffer.append(temp)
            head = angle
            temp = []
    averaged = list(np.average(items, axis=0) for items in buffer)
    return mapOrdinates(averaged, prop)


def mapOrdinates(ordinates, prop):
    '''
        Convert angles to tan inverse.
        find new x and y based on these new points.
        first normalize them with numpy.
    '''
    ords = []
    for angle, intercept in ordinates:
        slope = math.tan(angle)
        try:
            if prop[0] >= intercept >= prop[0]/1.3:
                x1 = 0
                y1 = int(intercept)
            else:
                x1 = int((320-intercept)/slope)
                x2 = int((prop[0]-intercept)/slope)
                y1 = int(prop[0])
            if 450 <= x2 <= 770 and 0 <= x1 <= prop[1]:
                ords.append([(x1, y1), (x2, 320)])
            else:
                if x2 > 770:
                    x2 = 770
                if x2 < 450:
                    x2 = 450
                if x1 > prop[1]:
                    x1 = int(prop[1])
                if x1 < 0:
                    x1 = 0
                ords.append([(x1, int(prop[0])), (x2, 320)])

        except Exception as e:
            continue
    return ords
