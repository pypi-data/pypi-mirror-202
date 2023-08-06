#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023--2028, Wang Weihua.
# All rights reserved.
"""Top-level package for legacyplate query."""
from .api import *  # noqa
from .client import LegacyplateClient
from .version import __version__, version_info  # noqa


def auth(username, password, host=None, port=None):
    """账号认证"""
    LegacyplateClient.set_auth_params(
        host=host,
        port=port,
        username=username,
        password=password,
    )


def auth_by_token(token, host=None, port=None):
    """使用 token 认证账号"""
    LegacyplateClient.set_auth_params(host=host, port=port, token=token)


def logout():
    """退出账号"""
    LegacyplateClient.instance().logout()


def is_auth():
    """账号是否已经认证"""
    if not LegacyplateClient.instance():
        return False
    return not LegacyplateClient.instance().not_auth


def set_params(**params):
    """设置请求参数

    参数说明：
        request_timeout: 请求超时时间，单位为秒，默认为 300 秒，值不能超过 300 秒
                         该值建议在账户认证前设置，否则可能会不生效
        request_attempt_count: 请求的尝试的次数，用于网络异常时重试，默认为 3 次，
                         该次数不能超过 10 次
    """
    LegacyplateClient.set_request_params(**params)


__all__ = [
    "auth",
    "logout",
    "is_auth",
    "set_params",
    "__version__"
]
__all__.extend(api.__all__)  # noqa
