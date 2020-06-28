import sys
sys.dont_write_bytecode = True

from __init__ import *
from util import carry
from util import net

import signal
def __shdl(snum, sfrm):
    carry.Tunnel.flag = False
    pass

signal.signal(signal.SIGINT, __shdl)
carry.Tunnel().start()
execs.Executor().attach(carry.Tunnel())
sniffer.Scanner().attach(carry.Tunnel())
timing.Impulse().attach(carry.Tunnel())
soc.Listener(3, net.localhost(), 6371).attach(carry.Tunnel())
carry.Tunnel().join(0)
signal.pause()
