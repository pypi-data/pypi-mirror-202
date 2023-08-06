#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023--2028, Wang Weihua.
# All rights reserved.
"""utils

常用工具函数
"""
import datetime
import six
import sys


class classproperty(object):
    """将方法转换为类属性 @classmethod + @property"""

    def __init__(self, func):
        self.func = classmethod(func)

    def __get__(self, instance, owner):
        return self.func.__get__(instance, owner)()


def today():
    return datetime.date.today()


def is_str(s):
    return isinstance(s, six.string_types)


def to_date_str(dt):
    if dt is None:
        return None

    if isinstance(dt, six.string_types):
        return dt
    if isinstance(dt, datetime.datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(dt, datetime.date):
        return dt.strftime("%Y-%m-%d")
    raise Exception("错误的时间格式 {}".format(dt))


def is_list(l):
    return isinstance(l, (list, tuple))


def isatty(stream=None):
    stream = stream or sys.stdout
    _isatty = getattr(stream, 'isatty', None)
    return _isatty and _isatty()


def get_mac_address():
    import uuid
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
    return '%s:%s:%s:%s:%s:%s' % (mac[0:2], mac[2:4], mac[4:6], mac[6:8],mac[8:10], mac[10:])
