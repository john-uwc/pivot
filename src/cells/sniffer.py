
from util import carry
import util
import threading
import time
import socket
import m
import evt


class Scanner(carry.Worker, threading.Thread, object):
    """
    scan the local area network for discovering nodes
    """

    def __init__(self):
        carry.Worker.__init__(self)
        threading.Thread.__init__(self)
        self.__catalogue = m.node.Catalogue()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def handle(self, obj):
        carry.Worker.handle(self, obj)
        try:
            dest = (obj.address['addr'], obj.address['port'])
            obj.address['addr'], obj.address['port'] = (util.net.host(), self.__socket.getsockname()[1])
            self.__socket.sendto(util.pack(obj), dest)
        except:
            pass

    def run(self):
        while self.flag and self._flag:
            try:
                data, _ = self.__socket.recvfrom(65565)
            except Exception as err:
                util.d(err)
            else:
                self.__catalogue.touch(util.unpack(data))
