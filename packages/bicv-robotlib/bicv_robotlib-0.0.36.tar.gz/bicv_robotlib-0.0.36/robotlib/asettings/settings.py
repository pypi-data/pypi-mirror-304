# -*- coding: utf-8 -*-
"""
模式功能描述：提供公共配置读取类，并提高模块及全局单列变量，导入此变量即可使用
模块及全局变量：settings
类：Settings
@author:
@date:
"""


import configparser
import os
import threading
import time



'''
主要用来全局配置
'''
class Settings(object):

    '''
    全局配置文件路径
    '''
    #GLOBAL_CONFIG_PATH = "./config.ini"
    #GLOBAL_CONFIG_PATH = ".\\ConfigDate\\02_CurConfig\\config.ini"

    GLOBAL_CONFIG_PATH = "D:\\py_work\\temp\\robotlib\\robotlib\\asettings\\config.ini"
    '''
    日志相关
    '''
    LOG_GLOBAL_VISIBLE = True  # 日志 总开关
    DEFAULT_LOG_SAVED_PATH = os.getcwd() + "\\log\\"  # 日志默认保存路径
    AUTO_TIME_NAME_SAVE_LOG_ENABLE = True  # 时间YMD 命名文件的方式自动保存

    # 用户自定义日志文件名
    USER_SET_LOG_FILE_NAME = "{year}_{mon}_{day}".format(year=time.localtime().tm_year,
                                                         mon=time.localtime().tm_mon,
                                                         day=time.localtime().tm_mday) + '.log'

    LOG_INFO_VISIBLE = True  # 信息等级开关
    LOG_WARNING_VISIBLE = True  # 警告等级开关
    LOG_ERROR_VISIBLE = True  # 错误等级开关
    '''
    # 错误等级开关
    '''
    '''
    相机相关    
    '''
    CAMERA_TYPE='XW200' # 相机种类

    DEVICEID=0 # 相机设备号

    DEFAULT_SAVE_PATH='' # 相机 读取图片保存默认地址

    EXPOSURE_TIME=0 # 相机曝光时间

    CONTRAST=50 # 拍照对比度

    BRIGHTNESS=50 # 拍照亮度

    SATURATION=50 # 拍照饱和度

    HUE=0 # 色调
    '''
    相机型号列表
    '''
    CAMERA_TYPE_LIST = {"xw200", "hik", "lvts"}

    '''
    默认使用相机的型号
    '''
    CAMERA_TYPE_DEFALUT = "A7S3"

    '''
    保存图片位置
    '''
    CAMERA_DIR_CAPTURE_IMAGE = "./camera_capture/"

    '''
    录屏保存位置
    '''
    CAMERA_DIR_RECORD_VIDEO = "./camera_capture/"

    '''
    继电器相关
    '''
    RELAY_UP_DOWN_POWER = 'com7'
    RELAY_360 = 'com10'
    USB_SWITCH_PORT = 'com15'


    '''
    程控电源相关
    '''
    POWER_TYPE_DEFAULT = "ea2000"
    POWER_TYPE_EA2000 = "ea2000"
    POWER_TYPE_EA2000_COM = "com2"

    '''
    图片对比相关
    '''

    '''
    串口相关
    '''
    # 波特率
    SERIAL_RATE_9600 = 9600
    SERIAL_RATE_19200 = 19200
    '''
    默认波特率
    '''
    SERIAL_RATE_115200 = 115200
    SERIAL_DEFAULT_RATE = SERIAL_RATE_19200
    '''
    串口连接超时时间，单位是毫秒
    '''
    SERIAL_INIT_TIMEOUT = 5*1000
    '''
    串口数据写入失败，是否重试和重试次数
    '''
    SERIAL_WRITE_FAIL_RETRY = False
    SERIAL_WRITE_FAIL_RETRY_TIMES = 4

    SERIAL_READ_FAIL_RETRY = False
    SERIAL_READ_FAIL_RETRY_TIMES = 4

    #单列对象
    __instance = None
    # 加锁，提供线程安全
    _lock = threading.RLock()

    def __new__(cls, *args, **kwargs):
        # 创建类对象时不需要args和kwargs参数
        print("fn:new")
        with cls._lock:
            if cls.__instance is None:
                print("instance = None")
                cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        print("cls:Settings fn:init")
        # 判断对象是否创建过
        if not hasattr(self, "uppercompter_log_config"):
            # 配置初始化的地方
            # 上位机日志配置对象
            pass




    def load_config(self, fpath=GLOBAL_CONFIG_PATH):
        '''
        加载全局配置文件
        :param fpath: 配置文件的路径，比如 /usr/data/custom.ini
        :return:
        '''
        if len(fpath) == 0:
            #LogRecord.error("Config file path is empty!!")
            return

        config = configparser.ConfigParser()
        readret = config.read(fpath, encoding="utf-8")
        if (len(readret)) == 0:
           # LogRecord.error("Failed to read the configuration file.")
            return

        if readret[0] != fpath:
            #LogRecord.error("Failed to load the configuration file.")
            return
        try:
            self.LOG_FILE = config.get("log","LOG_FILE")
            self.LOG_DIR = config.get("log","LOG_DIR")
            self.CAMERA_TYPE_DEFALUT = config.get("camera","CAMERA_TYPE_DEFALUT")
            self.CAMERA_DIR_CAPTURE_IMAGE = config.get("camera","CAMERA_DIR_CAPTURE_IMAGE")
            self.CAMERA_DIR_CAPTURE_IMAGE = config.get("camera", "CAMERA_DIR_RECORD_VIDEO")

            self.RELAY_UP_DOWN_POWER = config.get("relay", "RELAY_UP_DOWN_POWER")
            self.RELAY_360 = config.get("relay", "RELAY_360")
            self.POWER_TYPE_DEFAULT = config.get("power", "POWER_TYPE_DEFALUT")
            self.USB_SWITCH_PORT = config.get("power", "USB_SWITCH_PORT")

            self.SERIAL_DEFAULT_RATE = config.get("serial", "SERIAL_DEFAULT_RATE")
            self.SERIAL_INIT_TIMEOUT = config.get("serial", "SERIAL_INIT_TIMEOUT")
            self.SERIAL_WRITE_FAIL_RETRY = config.get("serial", "SERIAL_WRITE_FAIL_RETRY")
            self.SERIAL_WRITE_FAIL_RETRY_TIMES = config.get("serial", "SERIAL_WRITE_FAIL_RETRY_TIMES")
            self.SERIAL_READ_FAIL_RETRY = config.get("serial", "SERIAL_READ_FAIL_RETRY")
            self.SERIAL_READ_FAIL_RETRY_TIMES = config.get("serial", "SERIAL_READ_FAIL_RETRY_TIMES")

        except Exception as e:
            print("")
            # LogRecord.error(str(e))


# 全局变量settings
settings = Settings()

if __name__ == '__main__':
    # 测试是否是单列
    #settting1 = Settings()
    #settting2 = Settings()
    #print(id(settting1))
    #print(id(settting2))
    print(id(settings))
    #sett.load_config()



