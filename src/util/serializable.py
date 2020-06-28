import json
import cs


class Flatable(object):

    @classmethod
    def hatch(cls, flats):
        """
        :return: flatable
        :param flats: flat formatted in str or dict
        """
        def _(obj, flats):
            """
            :param flats: flat str or dict
            :param obj: flatable object
            :return: flatable
            """
            if not isinstance(flats, dict):
                return flats
            for e in flats.items():
                if hasattr(obj, e[0]):
                    if getattr(obj, e[0]):
                        setattr(obj, e[0], _(getattr(obj, e[0]), e[1]))
                    continue
                if isinstance(obj, dict):
                    if obj.has_key(e[0]):
                        obj[e[0]] = _(obj[e[0]], e[1])
                    continue
                obj = _(obj, e[1])
            return obj
        return _(cls(), eval(repr(flats)))

    def __repr__(self):
        return json.dumps(self, default=lambda obj: obj.__dict__)

    def __str__(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, indent=4)
