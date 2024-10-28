"""
模式功能描述：日志配置对象，从配置文件中读取配置信息生成配置对象，需要提供配置文件路径及，配置文件中日志SECTION
模块及全局变量：
类：Log_Config
模块函数：
@author: xumeng
@date:  2024/5/18
"""
# encoding=utf-8
import configparser
import os
import threading
import time


class Log_Config(object):
    """
    类功能描述：日志器配置，从配置文件中读取相关配置生成日期器
    属性： enable_filelog    日志输出到文件开关
         enable_consolelog 日志输出到控制台
         filelog_dir       文件保存的目录
         filelog_savetype  文件保存的方式（1.文件日期分割 2文件大小分割）
         等等
    修改记录：
    @author:xumeng
    @date:2024/5/17
    """

    def __init__(self, logger_name, section, fconfig_path, log_dir):
        """
        函数功能描述 设置Log_config 对象所具备的属性
        参数：logger_name  日志器的名称
             section      配置文件的段
             fconfig_path 配置文件的路径
             log_dir      日志存放的目录-如果是测试用例日志是和项目及测试运行结果动态创建的目录-所以需要动态修改处理器
        """
        print("cls:Log_Config fn:init")
        # 日志配置 配置文件路径
        self.config_path = fconfig_path
        # 控制台相关
        # 日记器名日志输出到控制台开关、日志等级
        self.logger_name = logger_name
        self.config_section = section
        self.enable_consolelog = False
        self.consolelog_level = 10
        self.consolelog_format = ""
        # '%(asctime)s - %(name)s - %(filename)s[:%(lineno)d] - p%(process)d - t%(thread)d - %(levelname)s- %(message)s'
        # 日志输出到文件相关
        # 日志输出到文件开关、日志等级、保存目录、文件名、文件完整路径、文件分割方式
        self.enable_filelog = False
        self.filelog_level = 10
        self.filelog_dir = log_dir
        self.filelog_format = ""
        # "%(asctime)s - %(name)s - %(filename)s[:%(lineno)d] - t%(process)d - t%(thread)d - %(levelname)s- %(message)s"
        self.filelog_name = ""
        self.filelog_savetype = 1
        # 日志输出到文件 文件大小分割配置  备份梳理、文件最大字节、
        self.filelog_backcount = 10
        self.filelog_max_szie = 300 * 1024
        # 日志输出到文件 时间分割分割配置  分割单位、分割间隔、分割备份数
        # 分割单位‘S’、‘M’、‘H’、‘D’、‘W’ 和 ‘midnight’，分别表示秒、分、时、天、周和每天的午夜
        self.filelog_when = "midnight"
        self.filelog_when_interval = 1
        self.filelog_when_backcount = 10
        self.filelog_when_utc = False
        self.__load_log_config(fconfig_path)

    def __str__(self):
        # message = super.__str__(self)
        return f" 日志器名： {self.logger_name} 控制台日志开关：{self.enable_consolelog} " \
               f"控制台日志等级：{self.consolelog_level}  " \
               f"文件日志开关：{self.enable_filelog} 文件日志等级：{self.filelog_level} " \
               f"文件保存方式：{self.filelog_savetype}   " \
               f"日志文件保存目录：{self.filelog_dir}"

    @property
    def filelog_filepath(self):
        """
            函数功能描述：获取文件日志路径
            Retrun:文件日志路径
        """
        return os.path.join(self.filelog_dir, self.filelog_name)

    def __load_log_config(self, fpath):
        """
        函数功能描述：加载日志配置信息,并创建相关日志目录层级
        参数：fpath 配置文件路径
        返回值：
        异常描述：
        修改记录：
        @author:
        @date:
        """
        print("fn:load_log_config:%s" % fpath)
        print("读取日志配置文件创建日志配置对象")
        # 判断路径是否是文件
        if not os.path.isfile(fpath):
            print("config path is not file")
            return
        # 判断路径文件是否存在
        if not os.path.exists(fpath):
            print("config file is not exists")
            return
        # 读取配置文件
        config = configparser.ConfigParser()
        readret = config.read(fpath, encoding="utf-8")

        if (len(readret)) == 0:
            print("config file is empty")
            # LogRecord.error("Failed to read the configuration file.")
            return
        print(readret)
        if readret[0] != fpath:
            # LogRecord.error("Failed to load the configuration file.")
            return
        try:
            # 读取上位机日志配置-控制台配置
            self.enable_consolelog = config.getboolean(self.config_section, "enable_consolelog")
            print(f"enable_consolelog = {self.enable_consolelog}")
            self.consolelog_level = config.getint(self.config_section, "consolelog_level")
            print(f"consolelog_level = {self.consolelog_level}")
            self.consolelog_format = config.get(self.config_section, "consolelog_format", raw=True)
            print(f"consolelog_format = {self.consolelog_format}")
            # 读取上位机日志配置-文件配置
            self.enable_filelog = config.getboolean(self.config_section, "enable_filelog")
            print(f"enable_filelog = {self.enable_filelog}")
            print(f"filelog_dir = {self.filelog_dir}")
            self.filelog_name = config.get(self.config_section, "filelog_name")
            print(f"filelog_name = {self.filelog_name}")
            self.filelog_savetype = config.getint(self.config_section, "savetype")
            print(f"filelog_savetype = {self.filelog_savetype}")
            self.filelog_level = config.getint(self.config_section, "filelog_level")
            print(f"filelog_level = {self.filelog_level}")
            self.filelog_format = config.get(self.config_section, "filelog_format", raw=True)
            print(f"filelog_format = {self.filelog_format}")
            self.filelog_backcount = config.getint(self.config_section, "filelog_backcount")
            print(f"filelog_backcount = {self.filelog_backcount}")
            self.filelog_max_szie = config.getint(self.config_section, "filelog_max_szie")
            print(f"filelog_max_szie = {self.filelog_max_szie}")
            # 配置文件是M为单位，函数是以字节为单位 M转字节的
            self.filelog_max_szie *= 1024
            print(f"filepath={self.filelog_filepath}")

            # 创建目录
            if not os.path.exists(self.filelog_dir):
                print("创建上位机日志目录")
                os.makedirs(self.filelog_dir, exist_ok=True, mode=0o755)

            # 时间分割配置
            self.filelog_when = config.get(self.config_section, "filelog_when")
            print(f"filelog_when = {self.filelog_when}")
            self.filelog_when_interval = config.getint(self.config_section, "filelog_when_interval")
            print(f"filelog_when_interval = {self.filelog_when_interval}")
            self.filelog_when_backcount = config.getint(self.config_section, "filelog_when_bacckcount")
            print(f"filelog_when_backcount = {self.filelog_when_backcount}")
            self.filelog_when_utc = config.getboolean(self.config_section, "filelog_when_utc")
            print(f"filelog_when_utc = {self.filelog_when_utc}")

        except Exception as e:
            print(str(e))  # LogRecord.error(str(e))
        print(self.__str__())



if __name__ == '__main__':
    # 配置文件读取是否正取
    from robotlib.init.init import g_commonpath

    # 上位机日志配置对象
    uppercompter_log_config = Log_Config("uppercomper_logger", "log_uppercompter",
                                         g_commonpath.uppercompter_config_path,
                                         g_commonpath.uppercompter_log_dir)
    # 测试用例日志配置对象
    testcase_log_config = Log_Config("testcase_logger", "log_testcase",
                                     g_commonpath.uppercompter_config_path,
                                     g_commonpath.testcase_log_dir)
