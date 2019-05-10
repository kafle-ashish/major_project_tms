

import cv2
import numpy as np


class Extractors:
    '''
            Implements foreground and background
            extraction with subtraction.
            Parameters
            ----------
                    arg1 : frame
                            A numpy array of input image frame.
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
                arg1 : self
                arg2 : numpy array
                        A numpy array of input image.
        '''
        # blur = cv2.GaussianBlur(frame, (3, 3), 0)
        dilation = cv2.dilate(frame, self.kernel, iterations=1)
        erosion = cv2.erode(dilation, self.kernel, iterations=1)
        mask = self.bg_sub.apply(erosion)
        return mask

    def subtractor(self, frame):
        background = cv2.imread('background.jpg')
        subtracted = cv2.subtract(background, frame)
        # dilation = cv2.dilate(subtracted, self.kernel, iterations=1)
        # blur = cv2.GaussianBlur(dilation, (9, 9), 0)
        return subtracted

    def extractBackground(self, frame):
        '''
                Extracts background from a supplied frame.
                Parameters
                ----------
                arg1 : self
                arg2 : numpy array
                        A numpy array of imput image.
        '''
        cv2.accumulateWeighted(frame, self.bg_avg, 0.01)
        res = cv2.convertScaleAbs(self.bg_avg)
        return res
    # Malisiewicz et al.


'''
    frame_count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #img = cv2.imread('./1.jpg')
'''
