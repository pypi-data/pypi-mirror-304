#! /usr/bin/python3
# coding=utf-8
# @Time:2023/10/21 23:17
# @Author: zhangtiejun
import redis

"""
redis 通过配置文件进行连接
"""


class redis_operation:
    def __init__(self, redis_info):
        self.redis_client = redis.Redis(
            host=redis_info["host"],
            port=redis_info["port"],
            db=redis_info["db"],
            password=redis_info["password"],
            decode_responses=True,
            charset="UTF-8",
            encoding="UTF-8"
        )
