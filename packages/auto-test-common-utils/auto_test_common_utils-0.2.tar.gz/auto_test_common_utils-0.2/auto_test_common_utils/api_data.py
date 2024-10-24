#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/20 13:37
# @Author  : 作者名:张铁君
# @Site    : 
# @File    : api_data.py
# @Project : android_auto_test
# @Software: PyCharm
import requests

from yaml_config import GetConf
from api_request_base import api_request_base


class api_data:
    def start_task(self, request_data):
        """
        开始执行任务 进行远程调用
        :param request_data:
        :return:
        """
        return api_request_base().send_post_request_normal("/start_task", request_data)

    def api_login(self, username, password):
        """
        用户登录
        :param username:
        :param password:
        :return:
        """
        request_data = {
            "loginName": username,
            "pwd": password,
            "customerUuid": ""
        }
        res = api_request_base().send_post_request("/api/user/account/v0/login/submit/web", request_data)
        print(res)
        return res["data"]["customerUuid"]

    def api_login_token(self, username, password):
        """
        用户登录
        :param username:
        :param password:
        :return:
        """
        request_data = {
            "loginName": username,
            "pwd": password,
            "customerUuid": ""
        }
        res = api_request_base().send_post_request("/api/user/account/v0/login/submit/web", request_data)
        print(res)
        return res["data"]["sessionId"]

    def work_account_list(self, customerUuid):
        """
        获取工作账号列表
        :param customerUuid:
        :return:
        """
        request_data = {
            "customerUuid": customerUuid
        }
        res = api_request_base().send_post_request("/api/user/account/v0/getWorkRoleList/web", request_data)
        return res["data"]["workList"]

    def channel_data(self, customer_uuid):
        request_data = {
            "tpye": "",
            "customerUuid": customer_uuid
        }
        res = api_request_base().send_post_request("/api/homePage/v0/channelSubscription/web", request_data)
        return res["data"]

    def news_list(self, channel_id, customer_uuid):
        request_data = {
            "channelId": channel_id,
            "customerUuid": customer_uuid,
            "pageNum": 0,
            "pageSize": 20,
            "keyWord": "",
            "publishChannels": "JG",
            "prevUuid": "",
            "prevPublishDate": ""
        }
        res = api_request_base().send_post_request("/api/homePage/v2/newsList/web", request_data)
        return res["data"]

    def video_channel_data_list(self, channel_id, customer_uuid):
        request_data = {
            "productUuid": "",
            "targetType": "",
            "queryType": channel_id,
            "pageNum": 0,
            "pageSize": 20,
            "customerUuid": customer_uuid

        }
        res = api_request_base().send_post_request("/api/CTerminalStudio/v0/videos/web", request_data)
        return res["data"]

    def live_channel_data_list(self, channel_id, customer_uuid):
        request_data = {
            "queryType": channel_id,
            "pageNum": 0,
            "pageSize": 20,
            "longitude": -1,
            "latitude": -1,
            "customerUuid": customer_uuid

        }
        res = api_request_base().send_post_request("/api/CTerminalStudio/v0/liveRelatedEntrance/web", request_data)
        return res["data"]

    def product_data_list(self, key, customer_uuid):
        request_data = {
            "key": key,
            "customerUuid": customer_uuid

        }
        res = api_request_base().send_post_request("/api/index/v2/guessYouLike/web", request_data)
        return res["data"]

    def mall_order_title(self, category, customer_uuid):
        request_data = {
            "moduleCode": category,
            "customerUuid": customer_uuid

        }
        res = api_request_base().send_post_request("/api/user/center/v0/moduleOrderTitle/web", request_data)
        return res["data"]

    def mall_category(self, category, customer_uuid):
        request_data = {
            "key": category,
            "customerUuid": customer_uuid

        }
        res = api_request_base().send_post_request("/api/index/v0/getIndexCategorys/web", request_data)
        return res["data"]["items"]

    def category_left(self, category_uuid, parent_uuid, customer_uuid):
        request_data = {
            "categoryUuid": category_uuid,
            "parentUuid": parent_uuid,
            "customerUuid": customer_uuid

        }
        res = api_request_base().send_post_request("/api/products/categorys/v0/getLevelOneCategorys/web", request_data)
        return res["data"]

    def sub_category(self, parent_category_uuid, show_type, customer_uuid):
        request_data = {
            "parentCategoryUuid": parent_category_uuid,
            "showType": show_type,
            "customerUuid": customer_uuid
        }
        res = api_request_base().send_post_request("/api/products/categorys/v0/getSubCategorys/web", request_data)
        return res["data"][0]["subCategoryList"]

    def category_product_list(self, category_uuids, customer_uuid):
        request_data = {
            "categoryUuids": category_uuids,
            "customerUuid": customer_uuid
        }
        res = api_request_base().send_post_request("/api/products/categorys/v0/getProducts/web", request_data)
        return res["data"]["list"]

    def category_recommend_product_list(self, level_one_category_uuid, customer_uuid):
        request_data = {
            "pageSize": 10,
            "pageNum": 1,
            "levelOneCategoryUuid": level_one_category_uuid,
            "prevUuid": "",
            "prevShelveTime": "",
            "customerUuid": customer_uuid

        }
        res = api_request_base().send_post_request("/api/products/categorys/v0/getRecommendProducts/web", request_data)
        return res["data"]["list"]

    def other_order_title(self, category, module, real_path):
        request_data = {
            "moduleCode": category
        }
        res = api_request_base().send_get_request(request_data, module, real_path)
        return res["data"]

    # 关联企业
    def related_enterprise(self, customerUuid, module, real_path):
        request_data = {
            "pageNum": 0,
            "pageSize": 30,
            "type": "0"
        }
        res = api_request_base().send_get_request(customerUuid, request_data, module, real_path)
        print(res)
        return res["data"]

    # 结算企业
    def settlement_company(self, customerUuid, module, real_path):
        request_data = {
            "pageNum": 0,
            "pageSize": 30
        }
        res = api_request_base().send_post_request_with_real_path(customerUuid, request_data, module, real_path)
        return res["data"]

    # 关联合同
    def related_contracts(self, customerUuid, module, real_path):
        request_data = {
            "pageNo": 0,
            "pageSize": 30
        }
        res = api_request_base().send_post_request_with_real_path(customerUuid, request_data, module, real_path)
        return res["data"]

    # 签约主体
    def contracting_party(self, customerUuid, module, real_path):
        request_data = {
            "pageNum": 0,
            "pageSize": 30
        }
        res = api_request_base().send_post_request_with_real_path(customerUuid, request_data, module, real_path)
        return res["data"]

    # 发布渠道
    def publish_channel_list(self, customerUuid, category, module, real_path):
        request_data = {
            "showPosition": category

        }
        res = api_request_base().send_get_request(customerUuid, request_data, module, real_path)
        return res["data"]

    # 发布渠道
    def ad_publish_channel_list(self, customerUuid, category, module, real_path):
        request_data = {
            "platform": "1",
            "tagType": "3"

        }
        res = api_request_base().send_get_request(customerUuid, request_data, module, real_path)
        return res["data"]

    # 线上媒体广告
    def online_media_ad_publish_channel_list(self, customerUuid, module, real_path):
        request_data = {
            "isDefault": 0,
            "pageNum": 0,
            "tagType": "3"
        }
        res = api_request_base().send_get_request(customerUuid, request_data, module, real_path)
        return res["data"]

    # 主站群发布位置
    def main_site_publish_channel_list(self, customerUuid, category, module, real_path):
        request_data = {
            "platform": "1",
            "tagType": "3"
        }
        res = api_request_base().send_get_request(customerUuid, request_data, module, real_path)
        return res["data"]

    # 主站频道
    def main_site_channel_list(self, customerUuid, module, real_path):
        request_data = {
            "firstTag": "article_site_category",
            "platform": "1",
            "tagType": "3"
        }
        res = api_request_base().send_get_request(customerUuid, request_data, module, real_path)
        return res["data"]

    def location_list(self, customerUuid, location_id, category, module, real_path):
        request_data = {
            "type": category,
            "id": location_id
        }
        res = api_request_base().send_get_request(customerUuid, request_data, module, real_path)
        return res["data"]


if __name__ == '__main__':
    token = api_data().api_login_token("15004262682", "cc123456@")

    # data = article_publish_channel_list = api_data().publish_channel_list("9cf65f43ae914ea9afaa54e49f123927",
    #                                                                       "article",
    #                                                                       "article-center",
    #                                                                       "/work/v0/base/category/list")
    # 线上媒体
    # data = article_publish_channel_list = api_data().online_media_ad_publish_channel_list("9cf65f43ae914ea9afaa54e49f123927",
    #                                                                                      "ad-center",
    #                                                                                      "/work/v0/ad-platform/list")
    # 主站群发布位置
    # data = article_publish_channel_list = api_data().online_media_ad_publish_channel_list("9cf65f43ae914ea9afaa54e49f123927",
    #                                                                                      "ad-center",
    #                                                                                      "/work/v0/ad-position/findFirstLevelTag")

    # data = article_publish_channel_list = api_data().main_site_channel_list("9cf65f43ae914ea9afaa54e49f123927",
    #                                                                         "ad-center",
    #                                                                         "/work/v0/ad-position/findTreeByFirst")
    data = api_data().related_enterprise("de8f136366774a1682f3553df2f50c77",
                                         "ad-center",
                                         "/work/v0/ad-customer/list")
    # data = api_data().location_list(token, "", "PROVINCE", "logistics-center",
    #                                "/v1/logistics-center/work/freightTemplate/getAreaList")
    # print(data)
    # data = api_data().provice_list(token, "01", "CITY", "logistics-center",
    #                                "/v1/logistics-center/work/freightTemplate/getAreaList")
    # data = api_data().settlement_company("de8f136366774a1682f3553df2f50c77",
    #                                      "user-center",
    #                                      "/work/v0/company/findCompanyList")

    # data = api_data().related_contracts("de8f136366774a1682f3553df2f50c77",
    #                                     "ad-center", "/work/v0/contract-main/selectList")
    # data = api_data().contracting_party("de8f136366774a1682f3553df2f50c77",
    #                                     "user-center", "/work/v0/company/findCompanyList")

    print(data)
