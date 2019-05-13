import cv2
import numpy as np


class Extractors:
    '''
            Implements foreground, background extraction and image subtraction.
            Parameters
            ----------
                    @params : Frame
                            A numpy array of input image.
    '''

    def __init__(self, frame):
        self.bg_sub = cv2.bgsegm.createBackgroundSubtractorMOG()
        self.kernel = np.ones((3, 3), np.uint8)
        self.bg_avg = np.float32(frame)

    def extractForeground(self, frame):
        '''
                Extracts foreground from a supplied frame.
                Parameters
                ----------
                @params : Frame
                        A numpy array of input image.
                @return : Frame
                        Foreground extracted frame.
        '''
        # blur = cv2.GaussianBlur(frame, (3, 3), 0)
        # dilation = cv2.dilate(blur, self.kernel, iterations=1)
        # erosion = cv2.erode(dilation, self.kernel, iterations=2)
        return self.bg_sub.apply(frame)

    def subtractor(self, frame):
        background = cv2.imread('background.jpg')
        subtracted = cv2.subtract(background, frame)
        return subtracted

    def extractBackground(self, frame):
        '''
                Extracts background from a supplied frame.
                Parameters
                ----------
                @params: Frame
                        A numpy array of imput image.
                @return : Frame
                        Background extracted frame.
        '''
        cv2.accumulateWeighted(frame, self.bg_avg, 0.01)
        res = cv2.convertScaleAbs(self.bg_avg)
        return res
