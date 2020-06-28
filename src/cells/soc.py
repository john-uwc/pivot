# -*- coding: UTF-8 -*-

from util import carry
import threading
import time
import hashlib
import base64
import struct
import socket
import util


class Listener(carry.Worker, threading.Thread, object):
    '''listen to accept socket request'''

    def __init__(self, backlog, addr, port):
        carry.Worker.__init__(self)
        threading.Thread.__init__(self)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.bind((addr, port))
        self.__socket.listen(backlog)

    def run(self):
        while self.flag and self._flag:
            conn, addr = self.__socket.accept()  # 服务器响应请求,返回连接客户的信息(连接fd,客户地址)
            WebSocket(conn).attach(self._sched)
            time.sleep(0)


class WebSocket(carry.Worker, threading.Thread, object):
    '''socket for web'''

    def __init__(self, connection):
        carry.Worker.__init__(self)
        threading.Thread.__init__(self)
        self.__connection = connection
        self.__handShaked = False
        return

    def __resolve(self, flat):
        def __parse(flat):
            if not len(flat):
                return ([], [])
            dlen = flat[1] & 127
            if dlen == 126:
                dlen = struct.unpack('>H', flat[2:4])[0]
                if len(flat) < dlen:
                    return ([], [])
                return (flat[4:8], flat[8:])
            elif dlen == 127:
                dlen = struct.unpack('>Q', flat[2:10])[0]
                if len(flat) < dlen:
                    return ([], [])
                return (flat[10:14], flat[14:])
            else:
                if len(flat) < dlen:
                    return ([], [])
                return (flat[2:6], flat[6:])

        mask, load = __parse(flat)
        if not len(mask) and not len(load):
            return None
        data = bytearray("")
        for i, d in enumerate(load):
            data += chr(d ^ mask[i % 4])
        return data.decode('utf-8')

    def __pack(self, data):
        if not data:
            return None
        dlen = len(data.encode())  # 可能有中文内容传入，因此计算长度的时候需要转为bytes信息
        if dlen > (2 ** 64 - 1):  # 当长度超过8个字节表示时，拒绝
            return None
        flat = bytearray("\x81")  # 使用bytes格式,避免后面拼接的时候出现异常
        if dlen <= (2 ** 64 - 1) and dlen > 65535:  # 当长度需要8个字节来表示时,此字节低7位取值为127,由后8个字节标示长度
            flat += struct.pack('b', 127)
            flat += struct.pack('>q', dlen)
        elif dlen <= 65535 and dlen > 125:  # 当长度需要两个字节来表示时,此字节低7位取值为126,由后两个字节标示长度
            flat += struct.pack('b', 126)
            flat += struct.pack('>h', dlen)
        else:  # 长度小于等于125时，此字节低7位直接标示长度
            flat += str.encode(chr(dlen))
        flat += data.encode('utf-8')
        return flat

    def __handShake(self, connection):
        if self.__handShaked:
            return True
        request = connection.recv(8192)
        if not len(request):
            return False
        key = None
        for line in request.split('\r\n\r\n')[0].split('\r\n')[1:]:
            k, v = line.split(': ')
            if 'Sec-WebSocket-Key' == k:
                key = base64.b64encode(
                    hashlib.sha1(v + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest())
                break
        if not key:
            return False
        response = 'HTTP/1.1 101 Switching Protocols\r\n' + \
                   'Upgrade: websocket\r\n' + \
                   'Connection: Upgrade\r\n' + \
                   'Sec-WebSocket-Accept:' + key + '\r\n\r\n'
        connection.send(response)
        self.__handShaked = True
        return self.__handShaked

    def handle(self, obj):
        carry.Worker.handle(self, obj)
        pack = self.__pack(util.pack(obj))
        if not pack:
            return
        try:
            self.__connection.send(pack)
        except:
            self._flag = False

    def run(self):
        while self.flag and self._flag and self.__handShake(self.__connection):
            data = None
            try:
                flat = bytearray("")
                while not self.__resolve(flat):
                    flat += self.__connection.recv(128)
                data = self.__resolve(flat)
            except:
                break
            self.announce(util.unpack(data))
        self.__connection.close()
