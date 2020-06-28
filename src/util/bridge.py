# -*- coding: UTF-8 -*-

import cs
from serializable import Flatable
import importlib
import json


def unpack(obj):
    try:
        __dict = json.loads(obj)
        sflatable, flats = (__dict['schema'], __dict['flats'])
        if flats is None or sflatable is None:
            raise Exception()
        module = ".".join(sflatable.split(".")[0:-1])  # 获取模块路径
        flatable = sflatable.split(".")[-1]  # 获取类名称
        module__ = importlib.import_module(module)  # 通过模块名加载模块
        class__ = getattr(module__, flatable, None)  # 获取模块中属性
        if not issubclass(class__, Flatable):
            raise Exception()
        return class__.hatch(flats)
    except Exception as e:
        cs.d(e)


def pack(obj):
    try:
        __dict = {
            'schema': "%s.%s" % (obj.__class__.__bases__[0].__module__, obj.__class__.__bases__[0].__name__), 'flats': obj
        }
        return json.dumps(__dict, default=lambda obj: obj.__dict__)
    except Exception as e:
        cs.d(e)
