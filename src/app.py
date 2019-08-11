import multiprocessing as mp
from time import time, sleep
import cv2 as cv
import pickle

from multiprocessing import Process, Pool, Queue
from globals import VID_DATA_DIR
from main import main
from sock import Sock

names = ['1a', '2a', '1b', '2b']
servers = ['{}/one.mp4'.format(VID_DATA_DIR) for _ in range(4)]
print('using OpenCV {}'.format(cv.__version__))


def monitor(queue):
    FUTURE = 0
    AWARD = []
    TIME = 45
    buffer = {'1a': [0, 0], '2a': [0, 0], '1b': [0, 0], '2b': [0, 0]}
    GO = ['2a', '2b']
    STOP = ['1a', '1b']
    while True:
        end = time() + TIME + FUTURE
        while time() <= end:
            traffic = queue.get()
            buffer[traffic['name']][0] = traffic['count']
            buffer[traffic['name']][1] = traffic['density']
        count_GO = buffer[GO[0]][0] + buffer[GO[1]][0]
        count_STOP = buffer[STOP[0]][0] + buffer[STOP[1]][0]
        if count_GO > count_STOP:
            AWARD = GO
            FUTURE = 15
        else:
            FUTURE = 0
            AWARD = []
        GO, STOP = STOP, GO


if __name__ == '__main__':
    queue = Queue()
    m = Process(target=monitor, args=(queue))
    processes = [Process(name=name, target=main, args=(queue, video))
                 for i, name, video in zip(range(4), names, servers)]
    m.start()
    p.start() for p in processes
    p.join() for p in processes
    m.join()

    queue.close()
    queue.join_thread()


'''
servers = ['rtsp://192.168.1.8:8080/h264_pcm.sdp',
           'rtsp://192.168.1.8:8080/h264_pcm.sdp',
           'rtsp://192.168.1.8:8080/h264_pcm.sdp',
           'rtsp://192.168.1.8:8080/h264_pcm.sdp']
'''
'''
payload = dict(pos="chyasal", status="medium", density=12, count=123)
r = requests.post('http://localhost:3000/traffic/',
                  data=payload)
# r = requests.get('https://tmsbackend.herokuapp.com/traffic/')
print(r.content)
'''
