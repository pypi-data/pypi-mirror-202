#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023--2028, Wang Weihua.
# All rights reserved.
"""Legacyplatequery 版本号"""
__author__ = """Wang Weihua"""
__email__ = 'wangwh@czu.cn'
__version__ = '0.1.0'


_VersionInfo = __import__("collections").namedtuple(
    "version_info", ["major", "minor", "micro"]
)
version_info = ([int(v) for v in __version__.split('.')[:3]] + [0] * 3)[:3]
version_info = _VersionInfo(*version_info)

python_version = ".".join(str(item) for item in __import__("sys").version_info)
version_str = f"Legacyplatequery version {__version__}, Python version {python_version}"



