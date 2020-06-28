
from util import carry
from concurrent.futures import ThreadPoolExecutor
import evt


class Executor(carry.Worker, object):
    """
    task exec container
    """

    def __init__(self):
        carry.Worker.__init__(self)
        self.__executor = ThreadPoolExecutor()

    def handle(self, obj):
        carry.Worker.handle(self, obj)
        self.__executor.submit(evt.task.Unit.fire, (obj))
