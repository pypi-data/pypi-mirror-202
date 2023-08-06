#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023--2028, Wang Weihua.
# All rights reserved.
"""Top-level package for legacyplate query."""
import io
import requests
import pandas as pd
from . import utils
from .client import LegacyplateClient


def get_total_of_plates(start_date=None, end_date=None):
    """
    获取天文底片的数目
    :param start_date 与 count 二选一，不可同时使用. 字符串或者 datetime.datetime/datetime.date 对象, 开始时间
    :param end_date 格式同上, 结束时间, 默认是'2015-12-31', 包含此日期.
    :return 返回.
    """
    start_date = utils.to_date_str(start_date)
    end_date = utils.to_date_str(end_date)
    if not start_date:
        start_date = "2015-01-01"
        
    client = LegacyplateClient.instance()
    return client.get_total_of_plates(**locals())


__all__ = [name for name in globals().keys() if name.startswith("get")]
