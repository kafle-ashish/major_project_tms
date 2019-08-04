import multiprocessing as mp
import cv2 as cv

from multiprocessing import Process, Pool, Queue
from main import main
from priority import DataQueue
print('using OpenCV {}'.format(cv.__version__))


def monitor(queue):
    # operator = DataQueue()
    while True:
        data = queue.get()


if __name__ == '__main__':
    queue = Queue()
    p = Process(name="east", target=main, args=(queue,))
    q = Process(name="west", target=main, args=(queue,))
    m = Process(name="monitor", target=monitor, args=(queue,))
    q.start()
    p.start()
    m.start()
    p.join()
    q.join()
    m.join()
    queue.close()
    queue.join_thread()
    # payload = dict(pos="chyasal", status="medium", density=12, count=123)
    # r = requests.post('http://localhost:3000/traffic/',
    #                   data=payload)
    # # r = requests.get('https://tmsbackend.herokuapp.com/traffic/')
    # print(r.content)
