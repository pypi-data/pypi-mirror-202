#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023--2028, Wang Weihua.
# All rights reserved.
"""Top-level package for legacyplate query."""
import io
import requests
from collections import OrderedDict
import pandas as pd
from . import utils
from .client import LegacyplateClient


def get_info():
    """
    获取信息
    :return 返回.
    """
    client = LegacyplateClient.instance()
    data = OrderedDict()
    # 天文底片
    try:
        result = client.get_total_of_plates()
        if result['status'] == 200:
            data['plates'] = result['data'][0]['count']            
    except Exception as err:
        print(f'{err}')

    # 星表
    try:
        result = client.get_total_of_star_catalog()
        if result['status'] == 200:
            data['stars'] = result['data'][0]['count']            
    except Exception as err:
        print(f'{err}')
    
    return pd.Series(data)


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
    result = client.get_total_of_plates(**locals())
    if result['status'] == 200:
        data = result['data']            
        return pd.DataFrame(data)
    else:
        pass


def get_plates_by_radial_query(ra, dec, radius=0.1):
    """
    使用 q3c_radial_query 搜索天文底片
    :param ra. 浮点数, 赤经，单位为度
    :param dec, 浮点数, 赤纬，单位为度
    :param radius. 浮点数, 距离，单位为度
    :return 返回.
    """
    ra = float(ra)
    dec = float(dec)
    radius = float(radius)
    client = LegacyplateClient.instance()
    result = client.legacyplate_radial_query(**locals())
    if result['status'] == 200:
        data = result['data']            
        return pd.DataFrame(data)
    else:
        pass


def get_total_of_star_catalog(start_date=None, end_date=None):
    """
    获取天文底片星表目标的数目
    :param start_date 与 count 二选一，不可同时使用. 字符串或者 datetime.datetime/datetime.date 对象, 开始时间
    :param end_date 格式同上, 结束时间, 默认是'2015-12-31', 包含此日期.
    :return 返回.
    """
    start_date = utils.to_date_str(start_date)
    end_date = utils.to_date_str(end_date)
    if not start_date:
        start_date = "2015-01-01"
        
    client = LegacyplateClient.instance()
    result = client.get_total_of_star_catalog(**locals())
    if result['status'] == 200:
        data = result['data']            
        return pd.DataFrame(data)
    else:
        pass


def get_star_catalog_by_radial_query(ra, dec, radius=0.1):
    """
    使用 q3c_radial_query 搜索星表
    :param ra. 浮点数, 赤经，单位为度
    :param dec, 浮点数, 赤纬，单位为度
    :param radius. 浮点数, 距离，单位为度
    :return 返回.
    """
    ra = float(ra)
    dec = float(dec)
    radius = float(radius)
    client = LegacyplateClient.instance()
    result = client.star_catalog_radial_query(**locals())
    if result['status'] == 200:
        data = result['data']            
        return pd.DataFrame(data)
    else:
        pass


__all__ = [name for name in globals().keys() if name.startswith("get")]
