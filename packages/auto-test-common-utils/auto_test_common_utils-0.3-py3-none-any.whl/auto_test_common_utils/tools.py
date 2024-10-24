import hashlib
import os
import time
from datetime import datetime, timedelta
import requests
import numpy as np

import uuid



def get_uuid():
    get_timestamp_uuid = uuid.uuid1()  # 根据 时间戳生成 uuid , 保证全球唯一
    return get_timestamp_uuid


def get_date_time_str(hours=0):
    # 步骤 1：获取当前时间的时间戳
    timestamp = time.time()
    # 步骤 2：将时间戳转换为datetime对象
    datetime_obj = datetime.fromtimestamp(timestamp)
    # 步骤 3：将时间增加2小时
    if hours == 0:
        new_datetime_obj = datetime_obj + timedelta(hours=8)
    else:
        new_datetime_obj = datetime_obj + timedelta(hours=8 + hours)
    # 步骤 4：将结果时间转换为时间戳
    new_timestamp = new_datetime_obj.timestamp()
    return time.strftime("%Y-%m-%d %H:%M", time.gmtime(new_timestamp))


def get_now_time():
    return datetime.now()


def element_click(name):
    return "点击[" + name + "]元素"


def element_input(name):
    return "输入内容为:[" + name + "]"


def get_now_date_time_str():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def get_project_path():
    """
    获取项目绝对路径
    :return:
    """
    # project_name = GetConf().get_project_name()["project"]
    project_name = 'auto_test_manager'
    file_path = os.path.dirname(__file__)
    return file_path[:file_path.find(project_name) + len(project_name)]


def sep(path, add_sep_before=False, add_sep_after=False):
    all_path = os.sep.join(path)
    if add_sep_before:
        all_path = os.sep + all_path
    if add_sep_after:
        all_path = all_path + os.sep
    return all_path


def get_img_path(img_name):
    """
    获取商品图片的路径
    :param img_name:
    :return:
    """
    img_dir_path = get_project_path() + sep(["img", img_name], add_sep_before=True)
    return img_dir_path


def get_file_path(file_name):
    """
    获取文件路径
    :param file_name:
    :return:
    """
    file_dir_path = get_project_path() + sep(["file", file_name], add_sep_before=True)
    return file_dir_path


def get_video_path(video_name):
    """
    获取视频路径地址
    :param video_name:
    :return:
    """
    video_dir_path = get_project_path() + sep(["video", video_name], add_sep_before=True)
    return video_dir_path


def get_random(start, end):
    return np.random.randint(start, end)


def get_random_image(start, end):
    return str(np.random.randint(start, end)) + ".png"


def get_radio_check_item(data_list):
    size = get_random(0, len(data_list))
    return data_list[size]


def get_every_wallpaper():
    """
    从bing获取每日壁纸
    :return:
    """
    everyday_wallpaper_url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=10&mkt=zh-CN"
    try:
        res = requests.get(url=everyday_wallpaper_url)
        wallpaper_url = "https://cn.bing.com" + res.json()["images"][0]["url"][:-7]
    except Exception as e:
        print(e)
        wallpaper_url = ""
    return wallpaper_url


def get_current_day():
    time_tuple = time.localtime(time.time())
    return str(time_tuple[2])


def get_current_month():
    time_tuple = time.localtime(time.time())
    return str(time_tuple[1])


def get_current_year():
    time_tuple = time.localtime(time.time())
    return str(time_tuple[0])


def get_uuid_str():
    return str(uuid.uuid1()).replace("-", "")


def get_md5_str(orgStr):
    md5 = hashlib.md5()  # 创建md5加密对象
    md5.update(orgStr.encode('utf-8'))  # 指定需要加密的字符串
    return md5.hexdigest()




if __name__ == '__main__':
    # print(get_now_time())
    # print(get_project_path())
    # "/Users/fengzhaoxi/imooc/code/trading_system_autotest/common"
    # sep(["config", "environment.yaml"], add_sep_before=True)
    # print(get_every_wallpaper())
    # print(get_now_date_time_str())
    # current_date = datetime.date
    #
    # print(get_current_year())
    # print(get_current_month())
    # print(get_current_day())
    print(get_uuid_str())
    print(get_now_time())
