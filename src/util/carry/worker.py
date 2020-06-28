
import threading
import util


class Worker(object):

    flag = True

    def __init__(self):
        self._flag = False
        self._sched = None

    def role(self):
        return ".".join((self.__module__, self.__class__.__name__))

    def attach(self, sched):
        util.i("%s <r: %s" % (str(sched).lower(), self.__class__.__name__.lower()))
        self._sched = sched._enroll(self)
        self._flag = not self._sched is None
        if not isinstance(self, threading.Thread):
            return
        self.setDaemon(True)
        self.start()

    @property
    def inhealth(self):
        return self._flag

    def handle(self, obj):
        util.i("%s <h: %s@%s" % (self.__class__.__name__.lower(), id(obj), str(obj.type)))
        util.v(str(obj))

    def announce(self, obj):
        util.i("%s >t: %s@%s" % (self.__class__.__name__.lower(), id(obj), str(obj.type)))
        util.v(str(obj))
        if not self._sched:
            return
        self._sched._drop(obj)
