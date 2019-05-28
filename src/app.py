import cv2
import asyncio
import numpy as np

from utils import *
from tasks import *
from tracker import *
from extractor import Extractors
from globals import *

print('using OpenCV {}'.format(cv2.__version__))

cap = getCapture('{}/one.mp4'.format(VID_DATA_DIR))
ex = Extractors(roi(cap.read()[1]))


WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
lanes = LaneDetector(HEIGHT, WIDTH)
tracker = CentroidTracker()


async def detectVehicles(frame):
    subtracted = ex.update(frame, "fg")
    contours, _ = cv2.findContours(
        subtracted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    hulls = approximateContours(contours)
    boxes = getBoxes(hulls)
    objects = tracker.update(boxes)
    tracker.count()
    frame = getBoundingBoxes(hulls, objects, frame)
    return frame, subtracted


async def detectLanes(frame):
    background = ex.update(frame)
    return lanes.update(background)


async def main():
    while cap.isOpened():
        start = cv2.getTickCount()

        _, frame = cap.read()
        detection, ret = await detectVehicles(roi(frame))
        # averagedLines = await detectLanes(frame)
        # for points in lines:
        #     cv2.line(detection, points[0], points[1], (255, 0, 0), 5)
        # if averagedLines is not False:
        #     for points in averagedLines:
        #         try:
        #             cv2.line(detection, points[0], points[1], (255, 0, 0), 5)
        #         except Exception as e:
        #             continue
        end = cv2.getTickCount()
        fps = 'FPS: '+str(int(1/((end - start)/cv2.getTickFrequency())))
        cv2.putText(detection, fps, (20, 50), CV_FONT,
                    0.8, TEXT_COLOR, 1, CV_AA)
        cv2.putText(detection, "Count: {}".format(tracker.count()), (20, 80),
                    CV_FONT, 0.8, TEXT_COLOR, 1, CV_AA)
        cv2.imshow('frame', detection)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()


if __name__ == '__main__':
    asyncio.run(main())
