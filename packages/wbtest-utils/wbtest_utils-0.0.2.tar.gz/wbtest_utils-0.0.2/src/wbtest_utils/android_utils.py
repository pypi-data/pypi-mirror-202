# -*- encoding=utf8 -*-
__author__ = "zhihui18"

from airtest.core.api import *
from airtest.core.helper import *
from airtest.core.android.android import *
import os
from os import path
import shutil
import json

# auto_setup(__file__, devices=["Android://127.0.0.1:5037/b6f505e5"])
auto_setup(__file__)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

adb_path = "/storage/emulated/0/Android/data/com.sina.weibo/cache/wlog_capture"

mock_path = "/storage/emulated/0/Android/data/com.sina.weibo/cache/mock_result"

fastbot_adb_path = "/storage/emulated/0/fastbot"

pc_wlog_capture_path = f"{PROJECT_DIR}/wlog_capture"


def check_android_env():
    """
    检查adb是否已连接，以及当前手机是否安装了微博
    :return: true false
    """
    if isinstance(G.DEVICE, Android):
        android = Android()
    else:
        return False
    device_list = android.get_default_device()
    if len(device_list) > 0:
        pass
    else:
        return False
    if android.check_app("com.sina.weibo"):
        return True
    else:
        return False


def get_wlog_file_from_adb():
    f"""
    通过adb获取手机存储的wlog日志文件，保存到 {pc_wlog_capture_path} 目录下
    :return: 成功 失败
    """
    if isinstance(G.DEVICE, Android):
        android = Android()
    else:
        return False
    android.adb.pull(adb_path, PROJECT_DIR)
    if os.path.exists(pc_wlog_capture_path):
        return True
    else:
        return False


def push_mock_file_to_devices(file_patch):
    f"""
    通过adb上传mock文件，保存到 {mock_path} 目录下
    :return: 成功 失败
    """
    if isinstance(G.DEVICE, Android):
        android = Android()
    else:
        return False
    try:
        android.adb.push(file_patch, mock_path)
        return True

    except Exception as e:
        print(e)
        return False


def clean_mock_file(file_dict):
    f"""
    删除手机上{mock_path}下的文件
    :return: 
    """
    if isinstance(G.DEVICE, Android):
        android = Android()
    else:
        return False
    if len(file_dict) == 0:
        return False
    if not isinstance(file_dict, dict):
        return False
    try:
        for key in file_dict:
            android.adb.shell(f"rm -rf {mock_path}/{file_dict[key]}")
        return True

    except Exception as e:
        print(e)
        return False


def clean_mock_dir():
    f"""
    删除手机上{mock_path}下的文件
    :return: 
    """
    if isinstance(G.DEVICE, Android):
        android = Android()
    else:
        return False
    try:
        android.adb.shell(f"rm -rf {mock_path}")
        return True
    except Exception as e:
        print(e)
        return False


def clean_wlog_dir():
    f"""
    清空 {pc_wlog_capture_path} 目录, 以及手机上存储的wlog日志文件
    :return: 
    """
    if isinstance(G.DEVICE, Android):
        android = Android()
    else:
        return False
    if os.path.exists(pc_wlog_capture_path):
        shutil.rmtree(pc_wlog_capture_path)
    else:
        pass
    try:
        android.adb.shell(f"rm -rf {adb_path}")
        return True

    except Exception as e:
        print(e)
        return False


def get_wlog_type_nums():
    """
    :return: 当前测试用例执行过程中, 记录的日志类型数量
    """
    if isinstance(G.DEVICE, Android):
        android = Android()
    else:
        return 0
    if os.path.exists(pc_wlog_capture_path):
        fileList = os.listdir(pc_wlog_capture_path)
        return len(fileList)
    else:
        return 0


def get_customer_file_num(act_code):
    """
    获取指定类型的日志数量
    :param act_code: 指定的类型 格式为: act_code act下划线code
    :return: 指定类型的日志数量
    """
    if isinstance(G.DEVICE, Android):
        android = Android()
    else:
        return 0
    if os.path.exists(pc_wlog_capture_path):
        fileList = os.listdir(pc_wlog_capture_path)
        if len(fileList) > 0:
            for sub_file in fileList:
                if sub_file.find(act_code) >= 0:
                    return len(os.listdir(pc_wlog_capture_path + "/" + sub_file))
                else:
                    continue
            else:
                return 0
        else:
            return 0
    else:
        return 0


def get_customer_file_first(act_code):
    """
    获取指定类型的日志中的第一条日志
    :param act_code: 指定的类型 格式为: act_code act下划线code
    :return: json字典
    """
    json_dic = {}
    try:
        if os.path.exists(pc_wlog_capture_path):
            fileList = os.listdir(pc_wlog_capture_path)
            if len(fileList) > 0:
                for sub_file in fileList:
                    sub_file_path = path.join(pc_wlog_capture_path, sub_file)
                    if sub_file.find(act_code) >= 0:
                        sub_dir = sorted(os.listdir(sub_file_path))
                        fr = open(path.join(sub_file_path, sub_dir[0]), 'r+')
                        json_dic = eval(fr.read())
                        fr.close()
                    else:
                        continue
    except Exception as e:
        log(e, timestamp=time.time(), desc="读取日志文件失败", snapshot=True)
    finally:
        return json_dic


def get_all_customer_files(act_code):
    """
    获取指定类型的日志中下的所有日志
    :param act_code: 指定的类型 格式为: act_code act下划线code
    :return: json字典List
    """
    json_dic_list = []
    try:
        if os.path.exists(pc_wlog_capture_path):
            fileList = os.listdir(pc_wlog_capture_path)
            if len(fileList) > 0:
                for sub_file in fileList:
                    sub_file_path = path.join(pc_wlog_capture_path, sub_file)
                    if sub_file.find(act_code) >= 0:
                        sub_dir = sorted(os.listdir(sub_file_path))
                        for file in sub_dir:
                            fr = open(path.join(sub_file_path, file), 'r+')
                            json_dic_list.append(eval(fr.read()))
                            fr.close()
                        print("{}下文件数是{}".format(sub_file_path, len(json_dic_list)))
                    else:
                        continue
    except Exception as e:
        log(e, timestamp=time.time(), desc="读取日志文件失败", snapshot=True)
    finally:
        return json_dic_list


def get_customer_file_last(act_code):
    """
    获取指定类型的日志中的最后一条日志
    :param act_code: 指定的类型 格式为: act_code act下划线code
    :return: json字典
    """
    json_dic = {}
    try:
        if os.path.exists(pc_wlog_capture_path):
            fileList = os.listdir(pc_wlog_capture_path)
            if len(fileList) > 0:
                for sub_file in fileList:
                    sub_file_path = path.join(pc_wlog_capture_path, sub_file)
                    if sub_file.find(act_code) >= 0:
                        sub_dir = sorted(os.listdir(sub_file_path))
                        fr = open(path.join(sub_file_path, sub_dir[-1]), 'r+')
                        json_dic = eval(fr.read())
                        fr.close()
                    else:
                        continue
    except Exception as e:
        log(e, timestamp=time.time(), desc="读取日志文件失败", snapshot=True)
    finally:
        json_dic = get_json_dic_from_string(json_dic.get("requestBody"))
        return json_dic


def get_json_dic_from_string(json_str):
    if len(json_str) == 0:
        return None
    else:
        return json.loads(json_str)


def mock_weibo_ab(mock_ab_dict):
    """
    通过scheme设置AB
    :param mock_ab_dict: 需要设置的AB内容,字典。eg: {"xxxx":"true","xxx":"false"}
    :return: 设置是否成功
    """
    if isinstance(G.DEVICE, Android):
        android = Android()
    else:
        return False
    mock_ab_list = []
    if len(mock_ab_dict) == 0:
        return False
    if not isinstance(mock_ab_dict, dict):
        return False
    for key in mock_ab_dict:
        mock_ab_list.append(f"{key}={mock_ab_dict[key]}")
    ab_command = "am start -d \'sinaweibo://greyconfig?"
    if mock_ab_list:
        for index in range(len(mock_ab_list)):
            if index < (len(mock_ab_list) - 1):
                ab_command = ab_command + mock_ab_list[index] + "&"
            else:
                ab_command = ab_command + mock_ab_list[index] + "\'"
        try:
            print(ab_command)
            android.adb.shell(ab_command)
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False


def fastbot_start_with_shell(shell_cmd):
    f"""
    -s 设备号  多个设备需要指定设备号，单独设备无需此-s参数\n
    CLASSPATH={fastbot_adb_path}/monkeyq.jar:{fastbot_adb_path}/framework.jar:{fastbot_adb_path}/fastbot-thirdpart.jar\n
    exec app_process /system/bin com.android.commands.monkey.Monkey\n
    -p 包名  遍历app的包名，-p+包名\n
    --agent reuseq  遍历模式，无需更改\n
    --running-minutes 遍历时长(分钟) # 遍历时间：--running-minutes 时间\n
    --throttle 事件频率  遍历事件频率，建议为500-800\n
    可选参数\n
    --bugreport  崩溃时保存bug report log\n
    --output-directory /sdcard/xxx log/crash 另存目录\n
    :param shell_cmd: 手动拼接的完整shell命令\n
    :return:执行结果 True False
    """
    if isinstance(G.DEVICE, Android):
        android = Android()
    else:
        return False
    try:
        android.adb.shell(f"ls {fastbot_adb_path}")
    except Exception as e:
        print(e)
        android.adb.shell(f"mkdir {fastbot_adb_path}")
        android.adb.push(f"{PROJECT_DIR}/fastbot/fastbot-thirdpart.jar", fastbot_adb_path)
        android.adb.push(f"{PROJECT_DIR}/fastbot/framework.jar", fastbot_adb_path)
        android.adb.push(f"{PROJECT_DIR}/fastbot/monkeyq.jar", fastbot_adb_path)
        android.adb.push(f"{PROJECT_DIR}/fastbot/libs/arm64-v8a", "/data/local/tmp/")
        android.adb.push(f"{PROJECT_DIR}/fastbot/libs/armeabi-v7a", "/data/local/tmp/")
    try:
        android.adb.start_cmd(shell_cmd)
        android.adb.pull("/storage/emulated/0/crash-dump.log", PROJECT_DIR)
        android.adb.pull("/storage/emulated/0/oom-traces.log", PROJECT_DIR)
        return True
    except Exception as e:
        print(e)
        return False


def fastbot_start_with_params(appid, activity_list, minutes, throttle):
    """
    执行fastbot
    :param appid: 微博小程序appid,不能为空
    :param activity_list: 当前小程序需要跳转的activity字符串数组,换行加\n ["包名.类名\n","包名.类名"]
    :param minutes: 遍历时长(分钟)
    :param throttle: 遍历事件频率，建议为500-800
    :return:
    """
    if isinstance(G.DEVICE, Android):
        android = Android()
    else:
        return False
    try:
        if len(appid) > 0:
            ab_command = f"am start -d \"sinaweibo://projectmode?appid={appid}\""
            f = open(f"{PROJECT_DIR}/fastbot/max.schema", "w")
            f.write(f"sinaweibo://projectmode?appid={appid}")
            f.close()
            android.adb.shell(ab_command)
            android.adb.push(f"{PROJECT_DIR}/fastbot/max.schema", "/sdcard")
        else:
            print("appid cannot be null")
            return False
        sleep(10)
        android.adb.shell(f"ls {fastbot_adb_path}")
        # 设置fastbot白名单文件
        origin_list = ["com.sina.weibo.SplashActivity\n", "com.sina.weibo.NewProjectModeActivity\n",
                       "com.sina.weibo.wboxsdk.page.acts.WBXPageActivity\n"]
        f_w = open(f"{PROJECT_DIR}/fastbot/awl.strings", "w")
        f_w.writelines(origin_list)
        f_w.close()
        if len(activity_list) > 0:
            f = open(f"{PROJECT_DIR}/fastbot/awl.strings", "a")
            f.writelines(activity_list)
            f.close()
        android.adb.push(f"{PROJECT_DIR}/fastbot/awl.strings", "/sdcard")
    except Exception as e:
        print(e)
        android.adb.shell(f"mkdir {fastbot_adb_path}")
        android.adb.push(f"{PROJECT_DIR}/fastbot/fastbot-thirdpart.jar", fastbot_adb_path)
        android.adb.push(f"{PROJECT_DIR}/fastbot/framework.jar", fastbot_adb_path)
        android.adb.push(f"{PROJECT_DIR}/fastbot/monkeyq.jar", fastbot_adb_path)
        android.adb.push(f"{PROJECT_DIR}/fastbot/libs/arm64-v8a", "/data/local/tmp/")
        android.adb.push(f"{PROJECT_DIR}/fastbot/libs/armeabi-v7a", "/data/local/tmp/")
        android.adb.push(f"{PROJECT_DIR}/fastbot/max.config", "/sdcard")
        android.adb.push(f"{PROJECT_DIR}/fastbot/max.widget.black", "/sdcard")

    try:
        class_path = f"{fastbot_adb_path}/monkeyq.jar:{fastbot_adb_path}/framework.jar:{fastbot_adb_path}/fastbot-thirdpart.jar"
        exec_cmd = f"exec app_process /system/bin com.android.commands.monkey.Monkey"
        pkg_cmd = f"-p com.sina.weibo"
        age_cmd = "--agent reuseq"
        minutes_cmd = f"--running-minutes {minutes}"
        throttle_cmd = f"--throttle {throttle}"
        # blacklist_cmd = "--act-blacklist-file sdcard/abl.strings"
        whitelist_cmd = "--act-whitelist-file sdcard/awl.strings"
        android.adb.shell(
            f"CLASSPATH={class_path} {exec_cmd} {pkg_cmd} {age_cmd} {whitelist_cmd} {minutes_cmd} {throttle_cmd} -v -v")
        # android.adb.pull("/storage/emulated/0/crash-dump.log", PROJECT_DIR)
        # android.adb.pull("/storage/emulated/0/oom-traces.log", PROJECT_DIR)
        return True
    except Exception as e:
        print(e)
        return False

# json_test = get_customer_file_last("actlog_14980")

# print(json_test)

# request_body = get_json_dic_from_string(json_test.get("requestBody"))

# print(request_body['extJson'])

# mock_weibo_ab(["minfo_logg_CC0=false", "btest23=false"])

# print(PROJECT_DIR)
# print(isinstance(G.DEVICE, Android))
# print(fastbot_start_with_params("5d1d6bf2e13df", ["com.sina.weibo.browser.WeiboBrowser\n"], 1, 500))
# print(get_current_activity())
# json_dict = {'name': 'value', 'name1': 'value2'}
# clean_mock_file(json_dict)
