#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/23 18:12
# @Author  : 作者名:张铁君
# @Site    : 
# @File    : setup.py.py
# @Project : auto_test_common
# @Software: PyCharm
from setuptools import setup, find_packages

setup(
    name='auto_test_common_utils',
    version='0.2',
    packages=find_packages(),
    description='为了方便自动化测试而封装的常用工具包',
    author='zhangtj',
    author_email='ztj_5451@163.com',
    url='https://gitlab.eeo.com.cn/auto_test/auto_test_common_utils.git',  # GitLab 地址
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
