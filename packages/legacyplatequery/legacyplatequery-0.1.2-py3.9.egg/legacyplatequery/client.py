#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023--2028, Wang Weihua.
# All rights reserved.
"""Legacyplatequery 客户端"""
import platform
import time
import threading
import requests
import logging
import urllib

try:
    from urllib.parse import urlencode, urljoin
    from urllib.parse import quote as urlquote
except ImportError:
    from urllib import quote as urlquote

from .utils import isatty, get_mac_address
from .version import __version__ as current_version


class LegacyplateClient(object):
    """Legacyplate 客户端"""
    _threading_local = threading.local()
    _auth_params = {}

    _default_host = "api.isciencehub.cn"
    _default_port = 80

    request_timeout = 300
    request_attempt_count = 3

    @classmethod
    def instance(cls):
        _instance = getattr(cls._threading_local, '_instance', None)
        if _instance is None:
            if cls._auth_params:
                _instance = LegacyplateClient(**cls._auth_params)
            cls._threading_local._instance = _instance
        return _instance

    def __init__(self, host=None, port=None, username="", password="", token=""):
        self.host = host or self._default_host
        self.port = int(port or self._default_port)
        self.username = username
        self.password = password
        self.token = token

        assert self.host, "host is required"
        assert self.port, "port is required"
        assert self.username or self.token, "username is required"
        assert self.password or self.token, "password is required"

        self.client = None
        self.inited = False
        self.not_auth = True
        self.compress = True
        self.data_api_url = ""
        self._http_token = ""

    @property
    def base_url(self):
        return f'http://{self._default_host}:{self._default_port}'

    @classmethod
    def set_auth_params(cls, **params):
        if params != cls._auth_params and cls.instance():
            cls.instance()._reset()
            cls._threading_local._instance = None
        cls._auth_params = params
        # cls.instance().ensure_auth()

    def ensure_auth(self):
        if self.inited:
            return

        if not self.username and not self.token:
            raise RuntimeError("not inited")

        if self.username:
            error, response = None, None
            for _ in range(self.request_attempt_count):
                try:
                    self._create_client()
                    response = self.client.auth(
                        self.username,
                        self.password,
                        self.compress,
                        get_mac_address(),
                        current_version,
                    )
                    break
                except socket_error as ex:
                    error = ex
                    time.sleep(0.5)
                    if self.client:
                        self.client.close()
                        self.client = None
                    continue
            else:
                if error and not response:
                    raise error
            if response and response.error:
                self.data_api_url = response.error
            else:
                self.data_api_url = AUTH_API_URL
        else:
            response = self.client.auth_by_token(self.token)
        auth_message = response.msg
        if not isatty():
            auth_message = ""
        if not response.status:
            self._threading_local._instance = None
            raise self.get_error(response)
        else:
            if self.not_auth:
                print("auth success %s" % auth_message)
                self.not_auth = False
        self.inited = True

    def _reset(self):
        if self.client:
            self.client.close()
            self.client = None
        self.inited = False
        self.http_token = ""

    def logout(self):
        self._reset()
        self._threading_local._instance = None
        self.__class__._auth_params = {}
        print("已退出")

    def get_error(self, response):
        err = Exception(response.error)
        return err

    def _ping_server(self):
        if not self.client or not self.inited:
            return False
        for _ in range(self.request_attempt_count):
            try:
                msg = self.query("ping", {})
            except ResponseError:
                msg = None
                continue
            except Exception:
                return False
        return msg == "pong"

    def __getattr__(self, method):
        return lambda **kwargs: self(method, **kwargs)

    def get_data_api_url(self):
        return self.data_api_url

    @property
    def http_token(self):
        if not self._http_token:
            self.set_http_token()
        return self._http_token

    @http_token.setter
    def http_token(self, value):
        self._http_token = value

    @http_token.deleter
    def http_token(self):
        self._http_token = ""

    def set_http_token(self):
        username, password = self.username, self.password
        if not username or not password:
            return
        body = {
            "method": "get_current_token",
            "mob": username,
            "pwd": urlquote(password),  # 给密码编码，防止使用特殊字符登录失败
        }
        headers = {'User-Agent': 'JQDataSDK/{}'.format(current_version)}
        try:
            res = requests.post(
                AUTH_API_URL,
                data=json.dumps(body),
                headers=headers,
                timeout=self.request_timeout
            )
            self._http_token = res.text.strip()
        except Exception:
            pass
        return self._http_token

    def get_http_token(self):
        return self.http_token
    
    def get_total_of_plates(self, **kwargs):
        """获取天文底片总数"""
        url = urljoin(self.base_url, '/legacyplate/count')
        logging.info(f'url:{url}')
        resp = requests.get(url)
        return resp.json()
    
    def legacyplate_radial_query(self, **kwargs):
        """获取目标总数"""
        url = urljoin(self.base_url, '/legacyplate/radial_query')
        payload = {
            'ra': kwargs.get('ra'),
            'dec': kwargs.get('radius'),
            'radius': kwargs.get('radius'),
        }
        logging.debug(f'url:{url}')
        resp = requests.get(url, params=payload)
        return resp.json()
    
    def get_total_of_star_catalog(self, **kwargs):
        """获取星表目标总数"""
        url = urljoin(self.base_url, '/starcatalog/count')
        logging.debug(f'url:{url}')
        resp = requests.get(url)
        return resp.json()
    
    def star_catalog_radial_query(self, **kwargs):
        """获取目标总数"""
        url = urljoin(self.base_url, '/starcatalog/radial_query')
        payload = {
            'ra': kwargs.get('ra'),
            'dec': kwargs.get('radius'),
            'radius': kwargs.get('radius'),
        }
        logging.info(f'url:{url}')
        resp = requests.get(url, params=payload)
        return resp.json()
