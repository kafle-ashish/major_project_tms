
import math
from numpy import pi
from os.path import dirname, abspath, join
from cv2 import FONT_HERSHEY_SIMPLEX, LINE_AA

ROI_AREA = 534632-100000
CV_FONT = FONT_HERSHEY_SIMPLEX
TEXT_COLOR = (255, 255, 255)
CV_AA = LINE_AA
FILE_DIR = dirname(abspath(__file__))
VID_DATA_DIR = join(FILE_DIR, 'data', 'video')
IMG_DATA_DIR = join(FILE_DIR, 'data', 'image')
BG_IMG_DATA = join(FILE_DIR, 'data', 'image', 'background.jpg')
MIN_LINE_LENGTH = 200  # minimum number of pixels making up a line
MAX_LINE_GAP = 60    # maximum gap in pixels between connectable line segments
THETA = pi/180  # angular resolution in radians of the Hough grid
