
import cv2
from utils import roi
import numpy as np
import math
from globals import MAX_LINE_GAP, MIN_LINE_LENGTH, THETA


class LaneDetector:
    '''
        Detects lanes from given input frame.
        Parameters
            @param rho: Number
                    Distance resolution in pixels of the Hough grid.
            @param lThresh: Number
                Minimum number of votes/intersections in Hough grid cell.
    '''

    def __init__(self, height, width, rho=1, lThresh=150, sig=0.33, sThresh=7):
        self.rho = rho
        self.sig = sig
        self.lThresh = lThresh
        self.sThresh = sThresh
        self.height = height
        self.width = width
        self.frame = None
        self.points = None
        self.kernel = np.ones((15, 15), np.uint8)
        self.count = 0

    def update(self, frame):
        '''
            Called on each frame update.
            Parameters
                @param frame: List
                    Numpy array of an image.
        '''
        self.count += 1
        if self.count > 150:
            if self.canny(frame):
                if self.drawLanes():
                    self.points.sort()
                    self.averagePoints()
                    return self.points
                else:
                    print("failed ...")
        return False

    def canny(self, frame):
        v = np.median(frame)
        lower = int(max(0, (1.0 - self.sig) * v))
        upper = int(min(255, (1.0 + self.sig) * v))
        self.frame = roi(cv2.Canny(frame, lower, upper))
        return True

    def drawLanes(self):
        '''
            Draws possible lanes from an edged frame.
        '''
        closing = cv2.morphologyEx(self.frame, cv2.MORPH_CLOSE, self.kernel)
        lines = cv2.HoughLinesP(closing, self.rho, THETA, self.lThresh,
                                np.array([]), MIN_LINE_LENGTH, MAX_LINE_GAP)
        points = []
        for line in lines:
            for x1, y1, x2, y2 in line:
                points.append([(x1, y1), (x2, y2)])
        self.points = points
        return True

    def averagePoints(self):
        head = self.points[0]
        buffer = []
        temp = []
        for point in self.points[1:]:
            if point[0][0] - head[0][0] < 20:
                temp.append(point)
                head = point
            else:
                if len(temp) > 0:
                    buffer.append(temp)
                    temp = []
                else:
                    buffer.append([point])
                head = point
        self.points = list(np.average(items, axis=0) for items in buffer)
