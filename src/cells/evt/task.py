from util import carry
import util


@carry.object.Meta(dest=('execs.Executor'))
class Unit(util.Flatable, object):
    """
    task unit, some duty that only exec once may inherit it
    """

    def __init__(self):
        util.Flatable.__init__(self)

    def fire(self):
        pass
