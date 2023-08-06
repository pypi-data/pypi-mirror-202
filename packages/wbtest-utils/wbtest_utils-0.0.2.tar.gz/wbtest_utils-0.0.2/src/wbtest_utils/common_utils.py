# -*- encoding=utf8 -*-
__author__ = "zhihui18"

from airtest.core.ios import IOS
from wbtest_utils import android_utils
from wbtest_utils.android_utils import *
from wbtest_utils.ios_utils import apputils
from src.wbtest_utils.android_utils import clean_mock_dir

auto_setup(__file__)

if isinstance(G.DEVICE, IOS):
    ios_app_utils = apputils(G.DEVICE.uuid)


def push_preset_mock_data_file_to_device(src: str):
    """
    将启动就要用到的 data mock 配置文件放入app
    src: 本地配置文件绝对路径
    :return: true false
    """
    if isinstance(G.DEVICE, Android):
        print()
    elif isinstance(G.DEVICE, IOS):
        return ios_app_utils.push_preset_mock_data_file_to_device(src)
    else:
        print("please check the devices is connected")


def push_preset_mock_ab_file_to_device(src: str):
    """
    将启动就要用到的 ab mock 配置文件放入 app
    :param src: 本地配置文件绝对路径
    :return: true false
    """
    if isinstance(G.DEVICE, Android):
        print()
    elif isinstance(G.DEVICE, IOS):
        return ios_app_utils.push_preset_mock_ab_file_to_device(src)
    else:
        print("please check the devices is connected")


def pull_log_file_from_devices():
    """
    从手机中获取日志文件
    :return: true false
    """
    if isinstance(G.DEVICE, Android):
        return get_wlog_file_from_adb()
    elif isinstance(G.DEVICE, IOS):
        return ios_app_utils.pull_log_file_from_device()
    else:
        print("please check the devices is connected")


def get_last_log_file_content(act: str, act_code: str):
    """
    获取指定类型的日志中的最新一条日志
    :param act: 日志行为act
    :param act_code: 日志类型act_code
    :return: json字典
    """
    if isinstance(G.DEVICE, Android):
        return get_customer_file_last(f"{act}_{act_code}")
    elif isinstance(G.DEVICE, IOS):
        return ios_app_utils.get_last_log_file_content(act, act_code)
    else:
        print("please check the devices is connected")
        return None


def clean_log_file():
    """
    清空设备上的日志文件
    :return: true false
    """
    if isinstance(G.DEVICE, Android):
        return clean_wlog_dir()
    elif isinstance(G.DEVICE, IOS):
        return ios_app_utils.clean_log_file()
    else:
        print("please check the devices is connected")


def push_mock_file_to_devices(paths: list = [str]):
    """
    将当前 case 需要 mock 的接口文件放入 app
    path: 文件绝对路径
    :return: true false
    """
    if isinstance(G.DEVICE, Android):
        print()
    elif isinstance(G.DEVICE, IOS):
        return ios_app_utils.push_mock_file_to_device(paths)
    else:
        print("please check the devices is connected")


# iOS 平台，需要启动app后才可用
def push_mock_interface(url_path, file_path):
    if isinstance(G.DEVICE, Android):
        return android_utils.push_mock_file_to_devices(file_path)
    elif isinstance(G.DEVICE, IOS):
        return ios_app_utils.push_mock_interface(url_path, file_path)
    else:
        print("please check the devices is connected")


# iOS 平台，需要启动app后才可用
def clean_mock_interface(interface_dict):
    if isinstance(G.DEVICE, Android):
        return clean_mock_file(interface_dict)
    elif isinstance(G.DEVICE, IOS):
        return ios_app_utils.clean_mock_interface(interface_dict)
    else:
        print("please check the devices is connected")


# iOS 平台，需要启动app后才可用
def mock_ab(ab_dict):
    if isinstance(G.DEVICE, Android):
        return mock_weibo_ab(ab_dict)
    elif isinstance(G.DEVICE, IOS):
        return ios_app_utils.mock_ab(ab_dict)
    else:
        print("please check the devices is connected")


# iOS 平台，需要启动app后才可用
def unmock_ab(ab_dict):
    if isinstance(G.DEVICE, Android):
        return mock_weibo_ab(ab_dict)
    elif isinstance(G.DEVICE, IOS):
        return ios_app_utils.unmock_ab(ab_dict)
    else:
        print("please check the devices is connected")


# iOS 平台，需要启动app后才可用
def clean_all():
    """
    清除 app 里面自动化操作的所有配置
    
    """

    if isinstance(G.DEVICE, Android):
        clean_log_file()
        clean_mock_dir()
    elif isinstance(G.DEVICE, IOS):
        return ios_app_utils.clean_all()
    else:
        print("please check the devices is connected")


def wb_start_app(package_name, bundle_id, arguments=[], environment={}, wait_for_quiescence=False, force=False):
    """
    启动指定的 app
    :param package_name: android对应的包名
    :param bundle_id: ios对应的bundle_id
    :param arguments: 启动app时候的启动参数
    :param environment: 启动app时候的环境变量, 比如: mock_ab, mock_data, 传入对应的json即可
    :param wait_for_quiescence: 
    :param force: 强制重新启动, 默认不强制
    
    """
    if isinstance(G.DEVICE, Android):
        start_app(package_name)
    elif isinstance(G.DEVICE, IOS):
        ios_app_utils.wb_start_app(bundle_id, arguments, environment, wait_for_quiescence, force=force)
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
