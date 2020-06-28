
from worker import Worker
import threading
import Queue
import time
import util


class Tunnel(Worker, threading.Thread, object):
    __metaclass__ = util.Singleton

    def __init__(self):
        Worker.__init__(self)
        threading.Thread.__init__(self)
        self.__workers = []
        self.__queue = Queue.Queue()

    def handle(self, obj):
        for worker in self.__workers:
            if not worker.inhealth:
                self.__workers.remove(worker)
                continue
            if not worker.role() in obj.dest:
                continue
            worker.handle(obj)

    def _enroll(self, worker):
        self.__workers.append(worker)
        return self

    def _drop(self, obj):
        if not obj:
            return
        self.__queue.put(obj)

    def run(self):
        while self.flag:
            self.handle(self.__queue.get())
