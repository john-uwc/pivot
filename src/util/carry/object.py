
def Meta(dest=()):
    def _(load):
        class Evt(load, object):
            def __init__(self, *args, **kwargs):
                load.__init__(self, *args, **kwargs)

            @property
            def dest(self):
                return dest

            @property
            def type(self):
                return load
        return Evt
    return _
