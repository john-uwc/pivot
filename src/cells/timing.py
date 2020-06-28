from util import carry
import threading
import time
import m
import evt


class Impulse(carry.Worker, threading.Thread, object):
    """
    timing source to sensitize the cells
    """

    def __init__(self):
        carry.Worker.__init__(self)
        threading.Thread.__init__(self)
        self.__catalogue = m.node.Catalogue()

    def handle(self, obj):
        carry.Worker.handle(self, obj)
        pass

    def run(self):
        while self.flag and self._flag:
            self.announce(evt.probe.Catalogue(self.__catalogue.fresh(120)))
            time.sleep(6)
