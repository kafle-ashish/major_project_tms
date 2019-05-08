

import cv2
import numpy as np


class Extratcors:
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
		self.kernel = np.ones((5, 5), np.uint8)
		self.bg_avg = np.float32(frame)

	def extractForeground(self, frame):
		'''
			Extracts foreground from a supplied frame.
			Parameters
			----------
			arg1 : self
			arg2 : numpy array
				A numpy array of imput image.
		'''
		dilation = cv2.dilate(frame, self.kernel, iterations=1)
		# blur = cv2.GaussianBlur(dilation, (3, 3), 0)
		mask = self.bg_sub.apply(dilation)
		return mask

	def subtractor(self, frame):
		background = cv2.imread('background.jpg')
		subtracted = cv2.subtract(background, frame)
		dilation = cv2.dilate(subtracted, self.kernel, iterations=1)
		blur = cv2.GaussianBlur(dilation, (9, 9), 0)
		return dilation

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

	def non_max_suppression(self, boxes, overlapThresh):
		# if there are no boxes, return an empty list
		if len(boxes) == 0:
			return []

		# if the bounding boxes integers, convert them to floats --
		# this is important since we'll be doing a bunch of divisions
		if boxes.dtype.kind == "i":
			boxes = boxes.astype("float")

		# initialize the list of picked indexes
		pick = []

		# grab the coordinates of the bounding boxes
		x1 = boxes[:, 0]
		y1 = boxes[:, 1]
		x2 = boxes[:, 2]
		y2 = boxes[:, 3]

		# compute the area of the bounding boxes and sort the bounding
		# boxes by the bottom-right y-coordinate of the bounding box
		area = (x2 - x1 + 1) * (y2 - y1 + 1)
		idxs = np.argsort(y2)

		# keep looping while some indexes still remain in the indexes
		# list
		while len(idxs) > 0:
			# grab the last index in the indexes list and add the
			# index value to the list of picked indexes
			last = len(idxs) - 1
			i = idxs[last]
			pick.append(i)

			# find the largest (x, y) coordinates for the start of
			# the bounding box and the smallest (x, y) coordinates
			# for the end of the bounding box
			xx1 = np.maximum(x1[i], x1[idxs[:last]])
			yy1 = np.maximum(y1[i], y1[idxs[:last]])
			xx2 = np.minimum(x2[i], x2[idxs[:last]])
			yy2 = np.minimum(y2[i], y2[idxs[:last]])

			# compute the width and height of the bounding box
			w = np.maximum(0, xx2 - xx1 + 1)
			h = np.maximum(0, yy2 - yy1 + 1)

			# compute the ratio of overlap
			overlap = (w * h) / area[idxs[:last]]

			# delete all indexes from the index list that have
			idxs = np.delete(idxs, np.concatenate(([last],
                                          np.where(overlap > overlapThresh)[0])))

		# return only the bounding boxes that were picked using the
		# integer data type
		return boxes[pick].astype("int")


'''
    frame_count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))   
    fps = int(cap.get(cv2.CAP_PROP_FPS))  
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #img = cv2.imread('./1.jpg')
'''
