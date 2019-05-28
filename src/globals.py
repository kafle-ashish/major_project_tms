
import os
import numpy as np
import cv2

CV_FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_COLOR = (255, 255, 255)
CV_AA = cv2.LINE_AA
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
VID_DATA_DIR = os.path.join(FILE_DIR, 'data', 'video')
IMG_DATA_DIR = os.path.join(FILE_DIR, 'data', 'image')
BG_IMG_DATA = os.path.join(FILE_DIR, 'data', 'image', 'background.jpg')
MIN_LINE_LENGTH = 200  # minimum number of pixels making up a line
MAX_LINE_GAP = 60    # maximum gap in pixels between connectable line segments
THETA = np.pi/180  # angular resolution in radians of the Hough grid
