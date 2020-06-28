
import socket


def host():
    addr = '0.0.0.0'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80)); addr, _ = s.getsockname()
    finally:
        s.close()
    return addr


def localhost():
    return 'localhost'
