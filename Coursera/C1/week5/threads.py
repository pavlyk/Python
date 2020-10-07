# Синхронизация потоков, условные переменные
import threading
from threading import Thread
from time import sleep

class Queue(object):
    def __init__(self, size=5):
        self._size = size
        self._queue = []
        self._mutex = threading.RLock()
        self._empty = threading.Condition(self._mutex)
        self._full = threading.Condition(self._mutex)
    def put(self, val):
        with self._full:
            while len(self._queue) >= self._size:
                print('_full.wait')
                self._full.wait()
            self._queue.append(val)
            self._empty.notify()
    def get(self):
        with self._empty:
            print('Блокировка self._empty')
            # while len(self._queue) == 0:
            while self.emptylen():
                print('начало ожидания wait')
                self._empty.wait()
                print('конец ожидания wait')
            ret = self._queue.pop(0)
            self._full.notify()
            return ret
    def emptylen(self):
        print('while',self._queue)
        return len(self._queue) == 0

def worker(q, n):
    while True:
        print('Процесс', n, 'запрашивает из очереди') # , datetime.datetime.now()
        item = q.get()
        print('Процесс', n, 'получил из очереди', item) # , datetime.datetime.now()
        if item is None:
            break
        # print("process data:", n, item)

q = Queue(5)
th1 = Thread(target=worker, args=(q, 1))
th2 = Thread(target=worker, args=(q, 2))

th1.start(); th2.start();
sleep(5)

for i in range(5):
    print('put', i)
    q.put(i)
    sleep(1)
q.put(None); q.put(None);
th1.join(); th2.join();