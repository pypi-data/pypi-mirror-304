#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/20 14:15
# @Author  : 作者名:张铁君
# @Site    : 
# @File    : aes.py
# @Project : android_auto_test
# @Software: PyCharm
import base64
from Crypto.Cipher import AES

pad = lambda s: s + chr(16 - len(s) % 16) * (16 - len(s) % 16)
unpad = lambda s: s[:-s[-1]]

config_key = 'smkldospdosldaaa'
config_iv = '0392039203920300'


# ECB模式加密
def aes_ECB_Encrypt(data):  # ECB模式的加密函数，data为明文，key为16字节密钥
    key = config_key.encode('utf-8')
    data = pad(data)  # 补位
    data = data.encode('utf-8')
    aes = AES.new(key=key, mode=AES.MODE_ECB)  # 创建加密对象

    # encrypt AES加密  B64encode为base64转二进制编码
    result = base64.b64encode(aes.encrypt(data))
    return str(result, 'utf-8')  # 以字符串的形式返回


# CBC模式加密
def aes_CBC_Encrypt(data):  # CBC模式的加密函数，data为明文，key为16字节密钥,iv为偏移量
    key = config_key.encode('utf-8')
    iv = config_iv.encode('utf-8')  # CBC 模式下的偏移量
    data = pad(data)  # 补位
    data = data.encode('utf-8')
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)  # 创建加密对象

    # encrypt AES加密  B64encode为base64转二进制编码
    result = base64.b64encode(aes.encrypt(data))
    return str(result, 'utf-8')  # 以字符串的形式返回


# ECB模式解密
def aes_ECB_Decrypt(data):  # ECB模式的解密函数，data为密文，key为16字节密钥
    key = config_key.encode('utf-8')
    aes = AES.new(key=key, mode=AES.MODE_ECB)  # 创建解密对象

    # decrypt AES解密  B64decode为base64 转码
    result = aes.decrypt(base64.b64decode(data))
    result = unpad(result)  # 除去补16字节的多余字符
    return str(result, 'utf-8')  # 以字符串的形式返回


# CBC模式解密
def aes_CBC_Decrypt(data):  # CBC模式的解密函数，data为密文，key为16字节密钥
    key = config_key.encode('utf-8')
    iv = config_iv.encode('utf-8')
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)  # 创建解密对象

    # decrypt AES解密  B64decode为base64 转码
    result = aes.decrypt(base64.b64decode(data))
    result = unpad(result)  # 除去补16字节的多余字符
    return str(result, 'utf-8')  # 以字符串的形式返回
