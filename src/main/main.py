import cv2 as cv
import requests
import os
import multiprocessing as mp

from tasks import LaneDetector
from extractor import Extractors
from tracker import CentroidTracker

from utils import roi, getBoxes, getCap, approxCnt, getBBoxes
from globals import VID_DATA_DIR, TEXT_COLOR, CV_FONT, CV_AA, ROI_AREA


def detectVehicles(frame, ex, tracker):
    try:
        sub = ex.update(frame, "fg")
        contours, _ = cv.findContours(
            sub, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )
        hulls = approxCnt(contours)
        boxes, area = getBoxes(hulls)
        objects = tracker.update(boxes)
        if len(boxes) > 0:
            tracker.density(int(area))
        else:
            tracker.density(area)
        frame = getBBoxes(hulls, objects, frame)
        return frame, contours
    except Exception as e:
        pass


def detectLanes(frame, lanes, ex):
    try:
        background = ex.update(frame)
        return lanes.update(background)
    except Exception as e:
        pass


def main(queue, device=False):
    SKIP = True
    STATUS = False
    averagedLines = False
    tracker = CentroidTracker()
    if device:
        cap = getCap(device)
    else:
        cap = getCap('{}/one.mp4'.format(VID_DATA_DIR))
    WIDTH = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))   # float
    HEIGHT = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))  # float
    ex = Extractors(HEIGHT, WIDTH)
    lanes = LaneDetector(HEIGHT, WIDTH)
    while cap.isOpened():
        try:
            start = cv.getTickCount()
            _, frame = cap.read()
            detection, ret = detectVehicles(roi(frame), ex, tracker)
            if SKIP:
                averagedLines, STATUS = detectLanes(frame, lanes, ex)
            if STATUS:
                tracker.setBoundary(averagedLines)
                SKIP = False
                STATUS = False
            end = cv.getTickCount()
            fps = 'FPS: '+str(int(1/((end - start)/cv.getTickFrequency())))

            # cv.imshow('frame', detection)
            queue.put({"name": mp.current_process().name, "count":
                       tracker.count(), "density": tracker.density() *
                       100/ROI_AREA, "fps": fps})
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
    cv.destroyAllWindows()
    cap.release()

# cv.putText(detection, fps, (20, 50), CV_FONT,
#            0.8, TEXT_COLOR, 1, CV_AA)
# cv.putText(detection, "Count: {}".format(tracker.count()), (20, 80),
#            CV_FONT, 0.8, TEXT_COLOR, 1, CV_AA)
# cv.putText(detection, "Density:{:.3f}%".format(tracker.density()*100 /
#                                                ROI_AREA), (20, 115),
#            CV_FONT, 0.8, TEXT_COLOR, 1, CV_AA)
# if STATUS == SKIP:
#     for points in averagedLines:
#         try:
#             cv.line(detection, (int(points[0][0]),
#                                 int(points[0][1])),
#                     (int(points[1][0]),
#                      int(points[1][1])), (255, 0, 0), 5)
#         except Exception as e:
#             print(e)