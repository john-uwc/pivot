from util import carry
import util
import m


@carry.object.Meta(dest=('soc.WebSocket'))
class Catalogue(util.Flatable, object):
    """
    probe report, which contains node's state
    """

    def __init__(self, states=[]):
        util.Flatable.__init__(self)
        self.states = states


@carry.object.Meta(dest=('sniffer.Scanner'))
class Scan(m.node.State, util.Flatable, object):
    """
    probe command, scan local net area to discovering node, addr may be broadcast address
    """

    def __init__(self, port=6371, addr='<broadcast>'):
        m.node.State.__init__(self, addr, port)
        util.Flatable.__init__(self)
