import multiprocessing as mp
from time import time
import cv2 as cv

from multiprocessing import Process, Pool, Queue
from main import main
# from priority import DataQueue
print('using OpenCV {}'.format(cv.__version__))


def monitor(queue):
    FUTURE = 0
    TIME = 45
    buffer = {'1a': [0, 0], '2a': [0, 0], '1b': [0, 0], '2b': [0, 0]}
    prior = ['2a', '2b']
    seconded = ['1a', '1b']
    while True:
        end = time() + TIME + FUTURE
        while time() <= end:
            traffic = queue.get()
            buffer[traffic['name']][0] = traffic['count']
            buffer[traffic['name']][1] = traffic['density']
        count_prior = buffer[prior[0]][0] + buffer[prior[1]][0]
        count_seconded = buffer[seconded[0]][0] + buffer[seconded[1]][0]
        if count_prior > count_seconded:
            FUTURE = 15
        else:
            FUTURE = 0
        prior, seconded = seconded, prior


if __name__ == '__main__':
    queue = Queue()
    p = Process(name="east", target=main, args=(queue,))
    # q = Process(name="west", target=main, args=(queue,))
    # m = Process(name="monitor", target=monitor, args=(queue,))
    # q.start()
    p.start()
    # m.start()
    p.join()
    # q.join()
    # m.join()
    queue.close()
    queue.join_thread()
    # payload = dict(pos="chyasal", status="medium", density=12, count=123)
    # r = requests.post('http://localhost:3000/traffic/',
    #                   data=payload)
    # # r = requests.get('https://tmsbackend.herokuapp.com/traffic/')
    # print(r.content)
