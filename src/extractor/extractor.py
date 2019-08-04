import cv2
import numpy as np
from globals import BG_IMG_DATA


class Extractors:
    '''
            Implements foreground, background extraction and image subtraction.
            Parameters
            ----------
                    @params : Frame
                            A numpy array of input image.
    '''

    def __init__(self):
        self.bg_sub = cv2.bgsegm.createBackgroundSubtractorMOG()
        self.kernel = np.ones((7, 7), np.uint8)
        self.frame = np.zeros((720, 1280, 3), dtype=np.uint8)
        self.bg_avg = np.float32(self.frame)

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
        res = cv2.convertScaleAbs(self.bg_avg)
        return res

    def subtractor(self):
        return cv2.subtract(cv2.imread(BG_IMG_DATA), self.frame)
