#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/13 16:16
# @Author  : 作者名:张铁君
# @Site    : 
# @File    : obs_operation.py
# @Project : auto_test_manager
# @Software: PyCharm
import json
from glob import glob

from obs import ObsClient
from obs import PutObjectHeader
import os

from common_config import ResultType
from tools import get_uuid_str, get_project_path
from yaml_config import GetConf


class ObsOperation:

    def __init__(self, obs_info):
        global obs_client, bucket_name, file_dir
        # obs_info = GetConf().get_obs_config()
        ak = obs_info['ak']
        sk = obs_info['sk']
        server = obs_info['server']
        file_dir = obs_info['file_dir']
        bucket_name = obs_info['bucket_name']
        # 创建obsClient实例
        # 如果使用临时AKSK和SecurityToken访问OBS，需要在创建实例时通过security_token参数指定securityToken值
        obs_client = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)

    def put_object(self, file_type, file_path):

        try:
            # 上传对象的附加头域
            headers = PutObjectHeader()
            # 【可选】待上传对象的MIME类型
            headers.contentType = 'text/plain'
            file_extension = file_path.split(".")[-1]
            object_name = file_dir + "/" + file_type + "/" + get_uuid_str() + "." + file_extension
            resp = obs_client.putFile(bucket_name, object_name, file_path)
            # 上传成功
            if resp['status'] == 200 and resp['reason'] == 'OK':
                return ResultType.OBS_SUCCESS, resp['body']['objectUrl']
            else:
                return ResultType.OBS_FAIL
        except:
            return ResultType.OBS_ERROR


if __name__ == '__main__':
    # res = obs_client().put_object(ObsFileType.IMAGE.value, 'H:/12.png')
    # print(res)
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    print("当前文件路径:", get_project_path())
    print("当前目录路径:", current_directory)
