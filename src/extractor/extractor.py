import cv2
import numpy as np
from globals import BG_IMG_DATA
from utils import roi


class Extractors:
    '''
            Implements foreground, background extraction and image subtraction.
            Parameters
            ----------
                    @params : Frame
                            A numpy array of input image.
    '''

    def __init__(self, height, width):
        self.bg_sub = cv2.bgsegm.createBackgroundSubtractorMOG()
        self.kernel = np.ones((7, 7), np.uint8)
        self.frame = np.zeros((height, width, 3), dtype=np.uint8)
        self.bg_avg = np.float32(self.frame)
        self.res = None

    def update(self, frame, jobType="bg"):
        self.frame = frame
        if jobType == "fg":
            return self.extractForeground()
        return self.extractBackground()

    def extractForeground(self):
        '''
                Extracts foreground from a supplied frame.
                Parameters
                ----------
                @params : Frame
                        A numpy array of input image.
                @return : Frame
                        Foreground extracted frame.
        '''
        sub = self.bg_sub.apply(self.frame)
        closing = cv2.morphologyEx(sub, cv2.MORPH_CLOSE, self.kernel)
        self.extractBackground()
        return closing

    def extractBackground(self):
        '''
                Extracts background from a supplied frame.
                Parameters
                ----------
                @params: Frame
                        A numpy array of imput image.
                @return : Frame
                        Background extracted frame.
        '''
        cv2.accumulateWeighted(self.frame, self.bg_avg, 0.01)
        self.res = cv2.convertScaleAbs(self.bg_avg)
        return self.res

    def subtractor(self):
        subtracted = cv2.subtract(roi(cv2.imread(BG_IMG_DATA)), self.frame)
        # cv2.imshow('sub', subtracted)
        return subtracted
