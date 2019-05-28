
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
                    if self.averageLines():
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

    def averageLines(self):
        '''
            Averages over a list of line points.
        '''
        angles = []
        for line in self.points:
            params = np.polyfit(line[0], line[1], 1)
            # print(math.degrees(math.atan(slope)))
            print(params[1])
            angles.append((math.degrees(math.atan(params[0])), params[1]))
        # angles.sort()
        # print(angles, "\n")
        self.points = angles
        return self.mapOrdinates()

    def averageSlopes(self):
        head = self.points[0][0]
        buffer = []
        temp = []
        for angle, intercept in self.points[1:]:
            if angle >= 86 and angle < 120:
                continue
            if angle-head <= self.sThresh:
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
        self.points = list(np.average(items, axis=0) for items in buffer)
        return True

    def averageIntercepts(self):
        head = self.points[0][1]
        buffer = []
        temp = []
        for angle, intercept in self.points[1:]:
            if intercept > self.height and intercept < 0:
                continue
            if intercept-head <= self.sThresh:
                temp.append((angle, intercept))
            else:
                if len(temp) == 0:
                    buffer.append([(angle, intercept)])
                else:
                    buffer.append(temp)
                head = intercept
                temp = []
        self.points = list(np.average(items, axis=0) for items in buffer)
        return True

    def mapOrdinates(self):
        '''
            Convert angles to tan inverse.
            find new x and y based on these new points.
            first normalize them with numpy.
        '''
        ords = []
        for angle, intercept in self.points:
            slope = math.tan(angle)
            try:
                if intercept <= self.height:
                    x1 = 0
                    y1 = int(intercept)
                    x2 = (320-intercept)/slope
                else:
                    x1 = int((self.height-intercept)/slope)
                    x2 = int((320-intercept)/slope)
                    y1 = int(self.height)
                # print(x1, x2, y1)
                ords.append([(x1, int(self.height)), (x2, 320)])
            except Exception as e:
                print(e)
        self.points = ords
        return True
