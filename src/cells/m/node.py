import util
import copy
import time


class State(util.Flatable, object):
    """
    the node's summary in real time, such as address, location and so on
    """

    def __init__(self, addr='0.0.0.0', port=0):
        util.Flatable.__init__(self)
        self.address = {"addr": addr, "port": port}

    def __hash__(self):
        return hash(repr(self.address))


class Catalogue(object):
    """
    list of node, that is fetched by scan
    """
    __metaclass__ = util.Singleton

    def __init__(self):
        self.__states = {}
        pass

    def fresh(self, ttl):
        cts = time.time()
        for state in self.__states.items():
            if ttl < cts - state[1][1]:
                self.__states.pop(state[0], state[1])
        return map(lambda it: copy.deepcopy(it[0]), self.__states.values())

    def touch(self, state=None):
        if not state:
            return
        self.__states[hash(state)] = (state, time.time(),)
