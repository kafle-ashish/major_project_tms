import cv2
import asyncio
import numpy as np

from utils import *
from tasks import *
from extractor import Extractors
from globals import FILE_DIR, IMG_DATA_DIR, VID_DATA_DIR

print('using OpenCV {}'.format(cv2.__version__))
cap = getCapture('{}/one.mp4'.format(VID_DATA_DIR))
WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
ex = Extractors(roi(cap.read()[1]))


async def detectVehicles(frame):
    subtracted = ex.extractForeground(frame)
    contours, _ = cv2.findContours(
        subtracted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    hulls = approximateContours(contours)
    frame = getBoundingBoxes(hulls, frame)
    return frame, subtracted


async def detectLanes(frame):
    background = ex.extractBackground(frame)
    return laneFinder(background)


async def main():
    while cap.isOpened():
        start = cv2.getTickCount()

        _, frame = cap.read()

        detection, ret = await detectVehicles(roi(frame))
        lanes = await detectLanes(frame)
        
        mask = roi(lanes)
        lines = drawLanes(mask)
        averageLines(lines, (WIDTH, HEIGHT))
        
        for points in lines:
            cv2.line(detection, points[0], points[1], (255, 0, 0), 5)

        end = cv2.getTickCount()
        print('{:f}s elapsed...'.format((end - start)/cv2.getTickFrequency()))
        cv2.imshow('frame', detection)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()


if __name__ == '__main__':
    asyncio.run(main())
