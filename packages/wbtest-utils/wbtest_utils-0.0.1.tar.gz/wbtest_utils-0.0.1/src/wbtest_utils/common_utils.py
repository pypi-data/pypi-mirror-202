# -*- encoding=utf8 -*-
__author__ = "zhihui18"

from airtest.core.ios import IOS
from wbtest_utils import android_utils
from wbtest_utils.android_utils import *
from wbtest_utils.ios_utils import apputils

auto_setup(__file__)

if isinstance(G.DEVICE, IOS):
    ios_app_utils = apputils(G.DEVICE.uuid)


def pull_log_file_from_devices():
    """
    从手机中获取日志文件
    :return: true false
    """
    if isinstance(G.DEVICE, Android):
        return get_wlog_file_from_adb()
    elif isinstance(G.DEVICE, IOS):
        return True
    else:
        print("please check the devices is connected")


def get_last_log_file_content(act, act_code):
    """
    获取指定类型的日志中的最新一条日志
    :param act: 日志行为act
    :param act_code: 日志类型act_code
    :return: json字典
    """
    if isinstance(G.DEVICE, Android):
        return get_customer_file_last(f"{act}_{act_code}")
    elif isinstance(G.DEVICE, IOS):
        return ios_app_utils.get_last_log_file_content(act_code)
    else:
        return None
        print("please check the devices is connected")


def clean_log_file():
    """
    清空设备上的日志文件
    :return: true false
    """
    if isinstance(G.DEVICE, Android):
        return clean_wlog_dir()
    elif isinstance(G.DEVICE, IOS):
        print()
    else:
        print("please check the devices is connected")


def push_mock_file_to_devices(path):
    if isinstance(G.DEVICE, Android):
        print()
    elif isinstance(G.DEVICE, IOS):
        print()
    else:
        print("please check the devices is connected")


def push_mock_interface(url_path, file_path):
    if isinstance(G.DEVICE, Android):
        return android_utils.push_mock_file_to_devices(file_path)
    elif isinstance(G.DEVICE, IOS):
        print()
    else:
        print("please check the devices is connected")


def clean_mock_interface(interface_dict):
    if isinstance(G.DEVICE, Android):
        return clean_mock_file(interface_dict)
    elif isinstance(G.DEVICE, IOS):
        print()
    else:
        print("please check the devices is connected")


def mock_ab(ab_dict):
    if isinstance(G.DEVICE, Android):
        return mock_weibo_ab(ab_dict)
    elif isinstance(G.DEVICE, IOS):
        print()
    else:
        print("please check the devices is connected")


def unmock_ab(ab_dict):
    if isinstance(G.DEVICE, Android):
        return mock_weibo_ab(ab_dict)
    elif isinstance(G.DEVICE, IOS):
        print()
    else:
        print("please check the devices is connected")


def start_fastbot_with_params(appid, activity_list, minutes, throttle):
    """
    执行fastbot
    :param appid: 微博小程序appid,不能为空
    :param activity_list: 当前小程序需要跳转的activity字符串数组,换行加\n ["包名.类名\n","包名.类名"]
    :param minutes: 遍历时长(分钟)
    :param throttle: 遍历事件频率，建议为500-800
    :return:
    """
    if isinstance(G.DEVICE, Android):
        fastbot_start_with_params(appid, activity_list, minutes, throttle)
