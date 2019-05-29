
import cv2 as cv
import asyncio

from tasks import LaneDetector
from tracker import CentroidTracker
from extractor import Extractors
from globals import VID_DATA_DIR, TEXT_COLOR, CV_FONT, CV_AA
from utils import roi, getBoxes, getCap, approxCnt, getBBoxes
print('using OpenCV {}'.format(cv.__version__))

cap = getCap('{}/one.mp4'.format(VID_DATA_DIR))
tracker = CentroidTracker()
ex = Extractors(roi(cap.read()[1]))
WIDTH = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
lanes = LaneDetector(HEIGHT, WIDTH)


async def detectVehicles(frame):
    sub = ex.update(frame, "fg")
    contours, _ = cv.findContours(
        sub, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
    )
    hulls = approxCnt(contours)
    boxes, area = getBoxes(hulls)
    objects = tracker.update(boxes)
    if len(boxes) > 0:
        tracker.density(int(area/len(boxes)))
    else:
        tracker.density(area)
    frame = getBBoxes(hulls, objects, frame)
    return frame, sub


async def detectLanes(frame):
    background = ex.update(frame)
    return lanes.update(background)


async def main():
    while cap.isOpened():
        start = cv.getTickCount()

        _, frame = cap.read()
        detection, ret = await detectVehicles(roi(frame))
        # averagedLines = await detectLanes(frame)
        # for points in lines:
        #     cv.line(detection, points[0], points[1], (255, 0, 0), 5)
        # if averagedLines is not False:
        #     for points in averagedLines:
        #         try:
        #             cv.line(detection, points[0], points[1], (255, 0, 0), 5)
        #         except Exception as e:
        #             continue
        end = cv.getTickCount()
        fps = 'FPS: '+str(int(1/((end - start)/cv.getTickFrequency())))
        cv.putText(detection, fps, (20, 50), CV_FONT,
                   0.8, TEXT_COLOR, 1, CV_AA)
        cv.putText(detection, "Count: {}".format(tracker.count()), (20, 80),
                   CV_FONT, 0.8, TEXT_COLOR, 1, CV_AA)
        cv.putText(detection, "Density: {}".format(tracker.density()),
                   (20, 115), CV_FONT, 0.8, TEXT_COLOR, 1, CV_AA)
        cv.imshow('frame', detection)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()
    cap.release()


if __name__ == '__main__':
    asyncio.run(main())
