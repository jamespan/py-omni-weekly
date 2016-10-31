# coding=utf-8

from jinja2 import Undefined
import datetime


def date(obj, fmt='%Y.%m.%d'):
    if obj is None or isinstance(obj, Undefined):
        return obj
    return datetime.datetime.strftime(obj, fmt)
