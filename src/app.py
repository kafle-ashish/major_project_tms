import multiprocessing as mp
from time import time, sleep
import cv2 as cv
import pickle

from multiprocessing import Process, Pool, Queue
from globals import VID_DATA_DIR
from main import main
from sock import Sock
from priority import Watcher

names = ['1a', '2a', '1b', '2b']
servers = ['{}/one.mp4'.format(VID_DATA_DIR) for _ in range(4)]
print('using OpenCV {}'.format(cv.__version__))


def monitor(queue):
    conn = Sock(ip="192.168.43.144")
    conn.connect()
    conn.send("ON;ONE")
    conn.disconnect()
    watch = Watcher()
    while True:
        end = time() + TIME + FUTURE
        while time() <= end:
            traffic = queue.get()
            watch.update(traffic)
        average, award, future, active = watch.getStatus()
        if active[0] == '2a':
            conn.send("ON;TWO")
        else:
            conn.send("ON;ONE")


if __name__ == '__main__':
    queue = Queue()
    # m = Process(target=monitor, args=(queue))
    # processes = [Process(name=name, target=main, args=(queue, video))
    #              for i, name, video in zip(range(4), names, servers)]
    # m.start()
    # p.start() for p in processes
    # p.join() for p in processes
    # m.join()

    main(queue, '{}/one.mp4'.format(VID_DATA_DIR))
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
