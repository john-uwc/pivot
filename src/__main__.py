
import sys
sys.dont_write_bytecode = True

from multiprocessing import Process
import opls
import cells


ps = {
    cells.__name__: Process(target=cells.__main__, name=cells.__name__, args=())
    opls.__name__: Process(target=opls.__main__, name=opls.__name__, args=())
}

for p in ps.values():
    p.start()
for p in ps.values():
    p.join()
