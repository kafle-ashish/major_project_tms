import multiprocessing as mp
from time import time, sleep
import cv2 as cv
import requests

from multiprocessing import Process, Pool, Queue
from globals import VID_DATA_DIR, STOP
from priority import Watcher
from main import main
from sock import Sock

print('using OpenCV {}'.format(cv.__version__))
names = ['1a', '2a']
servers = ['{}/one.mp4'.format(VID_DATA_DIR) for _ in range(2)]


def monitor(queue):
    TIME = 5
    FUTURE = 0
    URL = 'https://tmsbackend.herokuapp.com/traffic/'
    headers = {
        'Content-Type': 'application/json',
        'X-Access-Id': '5d454a854fd9612631343699'
    }
    conn = Sock()
    conn.connect()
    conn.send("ON;TWO")
    conn.disconnect()
    watch = Watcher()
    while True:
        end = time() + TIME + FUTURE
        while time() <= end:
            traffic = queue.get()
            watch.update(traffic)
        average, award, future, active = watch.getStatus()

        payload = dict(density=average['1a'][1], count=average['1a'][0])
        r = requests.put(URL, json=payload, headers=headers)

        print(average, "Changing status", r.content)
        conn = Sock()
        conn.connect()
        if active[0] == '2a':
            conn.send("ON;TWO")
        else:
            conn.send("ON;ONE")
        conn.disconnect()


if __name__ == '__main__':
    queue = Queue()
    m = Process(target=monitor, args=(queue,))
    processes = [Process(name=name, target=main, args=(queue, video))
                 for i, name, video in zip(range(1), names, servers)]
    m.start()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    m.join()
    queue.close()
    queue.join_thread()
    # status, e = video("/home/bee/images/", "processed-im1b.mkv")
    # if status:
    #     print("done")
    # else:
    #     print("failed")
    #     print(e)

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
