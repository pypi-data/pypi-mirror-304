"""
    模块功能描述：初始化库模块
"""
from robotlib.common.common_path import CommonPath
from robotlib.log.log import Base_Log
from robotlib.log.log_config import Log_Config

g_commonpath = CommonPath()
# 全局变量
g_uper_log = Base_Log(Log_Config("upper_logger", "log_uppercompter", g_commonpath.uppercompter_config_path,
                                      g_commonpath.uppercompter_log_dir))
g_testcase_log = Base_Log(Log_Config("test__logger", "log_testcase", g_commonpath.uppercompter_config_path,
                                   g_commonpath.testcase_log_dir))
