#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/20 15:42
# @Author  : 作者名:张铁君
# @Site    : 
# @File    : api_request_base.py
# @Project : android_auto_test
# @Software: PyCharm
import json

import requests
from yaml_config import GetConf
from aes import aes_CBC_Encrypt


class api_request_base:
    # 发送post请求
    def send_post_request_normal(self, url, data):
        base_url = GetConf().get_actuator_base_url()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
            "Accept-Encoding": "utf-8"}
        return requests.post(base_url + url, headers=headers, json=data).json()

    # 发送post请求
    def send_post_request(self, url, data):
        base_url = GetConf().get_api_base_url()
        request_str = aes_CBC_Encrypt(str(data))
        request_data = {
            "requestStr": request_str
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
            "Accept-Encoding": "utf-8"}
        return requests.post(base_url + url, headers=headers, params=request_data).json()

    # 发送get请求
    def send_get_request(self, customerUuid, data, module, real_path):
        base_url = GetConf().get_proxy_url()
        request_str = aes_CBC_Encrypt(str(data))
        request_data = {
            "requestStr": request_str,
            "customerUuid": customerUuid
        }
        headers = {
            "real-path": real_path,
            "module": module

        }
        return requests.get(base_url, headers=headers, params=request_data).json()

    # 发送post请求
    def send_post_request_with_real_path(self, customerUuid, data, module, real_path):
        base_url = GetConf().get_proxy_url()
        request_str = aes_CBC_Encrypt(str(data))
        request_data = {
            "requestStr": request_str,
            "customerUuid": customerUuid
        }
        headers = {
            "real-path": real_path,
            "module": module

        }
        return requests.post(base_url, headers=headers, data=request_data).json()
