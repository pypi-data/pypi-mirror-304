#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/25 10:28
# @Author  : 作者名:张铁君
# @Site    : 登录用户
# @File    : LoginUser.py
# @Project : bh5_auto_test
# @Software: PyCharm
from enum import Enum


class CaseType(Enum):
    """
    测试用例类型
    """
    ARTICLE = 'article'
    AD_ARTICLE = 'ad_article'
    VIDEO = 'video'
    AD_VIDEO = 'ad_video'
    LIVE = 'live'
    AD_LIVE = 'ad_live'
    NEWS_FLASH = 'news_flash'
    AD_NEWS_FLASH = 'ad_news_flash'


class CaseCategory(Enum):
    """
    测试用例分类
    """
    NORMAL_CATEGORY = 'normal_article'
    AD_CATEGORY = 'ad_category'


class ObsFileType(Enum):
    """
    测试用例类型
    """
    DOC = 'doc'
    IMAGE = 'image'
    VIDEO = 'video'


class ObsFileTypeName:
    def get_obs_file_type_name(self, obs_file_type):
        obs_file_type_dic = {
            ObsFileType.DOC.value: "文档",
            ObsFileType.IMAGE.value: "图片",
            ObsFileType.VIDEO.value: "视频"
        }
        """
        测试用例类型显示
        """
        return obs_file_type_dic[obs_file_type]


class CaseTypeName:
    def get_case_type_name(self, case_type):
        case_type_dic = {
            CaseType.ARTICLE.value: "文章",
            CaseType.VIDEO.value: "视频",
            CaseType.LIVE.value: "直播",
            CaseType.AD_ARTICLE.value: "广告文章",
            CaseType.AD_VIDEO.value: "广告视频",
            CaseType.AD_LIVE.value: "广告直播",
            CaseType.NEWS_FLASH.value: "快讯",
            CaseType.AD_NEWS_FLASH.value: "广告快讯"

        }
        """
        测试用例类型显示
        """
        return case_type_dic[case_type]

    def get_case_category(self, category):
        case_type_dic = {
            CaseCategory.NORMAL_CATEGORY.value: "普通",
            CaseCategory.AD_CATEGORY.value: "广告",

        }
        """
        测试用例类型显示
        """
        return case_type_dic[category]

    def get_case_status(self, status):
        case_status_dic = {"0": "未开始",
                           "1": "进行中",
                           "2": "已完成"}
        """
        测试用例类型显示
        """
        return case_status_dic[status]


# 返回数据类型
def get_result_data(data):
    return {"status": "1", "data": data}


# 状态返回类型
class ResultType(Enum):
    """
    状态返回类型
    """
    BUILD_SUCCESS = {"status": "1", "message": "构建指令已下发！"}
    BUILD_FAIL = {"status": "0", "message": "构建失败！"}
    ADD_SUCCESS = {"status": "1", "message": "添加成功！"}
    ADD_FAIL = {"status": "0", "message": "添加失败！"}
    DELETE_SUCCESS = {"status": "1", "message": "删除成功！"}
    DELETE_FAIL = {"status": "0", "message": "删除失败！"}
    UPDATE_SUCCESS = {"status": "1", "message": "更新成功！"}
    UPDATE_FAIL = {"status": "0", "message": "更新失败！"}
    ERROR = {"status": "0", "message": "请联系管理员！"}
    CHANGE_SUCCESS = {"status": "1", "message": "设置成功！"}
    CHANGE_FAIL = {"status": "", "message": "设置失败！"}
    DELETE_ERROR = {"status": "2", "message": "操作失败，请联系管理员！"}
    SYSTEM_ERROR = {"status": "3", "message": "操作失败，请联系管理员"}
    USER_LOGIN_SUCCESS = {"status": "1", "message": "登录成功！"}
    USER_ACCOUNT_LOCK = {"status": "2", "message": "账号被锁定，请联系管理员！"}
    USER_LOGIN_FAIL = {"status": "3", "message": "账号或密码错误！"}

    USER_ACCOUNT_EXIST = {"status": "0", "message": "账号已存在！"}

    OBS_SUCCESS = {"status": "1", "message": "上传成功！"}
    OBS_FAIL = {"status": "0", "message": "上传失败！"}
    OBS_ERROR = {"status": "0", "message": "上传发生错误，请联系管理员！"}

# print(CaseTypeName().get_case_type_name(CaseType.ARTICLE.value))
# print(type(ResultType.ADD_SUCCESS.value))
# print(type({"status": "1", "message": "添加成功"}))
if __name__ == '__main__':
    ObsFileTypeName().get_obs_file_type_name(ObsFileType.DOC.value)