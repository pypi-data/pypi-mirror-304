# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time

from robotlib.asettings.settings import Settings
from robotlib.init.init import *


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    time.sleep(3)
    print_hi('测试程序')
    print("设置项目信息1###")
    g_commonpath.set_project_info("testproject1", "v1.0", "集成测试", "1", g_testcase_log)
    upper_log = g_uper_log
    testcase_log = g_testcase_log
    # upper_log = Base_Log(Log_Config("uppercomper_logger", "log_uppercompter", g_commonpath.uppercompter_config_path,
    #                                      g_commonpath.uppercompter_log_dir))
    # testcase_log = Base_Log(Log_Config("testcase_logger", "log_testcase", g_commonpath.uppercompter_config_path,
    #                                         g_commonpath.testcase_log_dir))
    # 验证日志输出是否正常
    # 不带格式化参数
    upper_log.warning("test_no_param")
    # 带1个格式化参数 和 2个格式化参数
    i1 = 1
    i2 = 2
    upper_log.warning("test_one_param:%d", i1)
    upper_log.warning("test_one_param:%d %d", i1, i2)
    # 不带格式化参数及有额外参数exc_info
    upper_log.warning("test_no_param", exc_info=True)
    # 一个格式化参数及有额外参数exc_info
    upper_log.warning("test_extra_param:%d", i1, exc_info=True)
    # 一个格式化参数及有额外参数exc_info,stack_info
    upper_log.warning("test_extra_param:%d", i1, exc_info=True, stack_info=True)
    # 一个格式化参数及有额外参数exc_info,stack_info
    upper_log.warning("test_extra_param:%d", i1, exc_info=True, stack_info=True, stacklevel=2)

    for i in range(10):
        # uper_log.info("Hello%d" % i)
        upper_log.warning("Hello%d" % i)
        testcase_log.warning("Hello%d" % i)
        time.sleep(3)
    # 切换文件输出目录测试
    print("设置项目信息2###")
    g_commonpath.set_project_info("testproject2", "v1.0", "集成测试", "1", g_testcase_log)
    for i in range(10):
        upper_log.warning("Hello%d" % i)
        testcase_log.warning("Hello%d" % i)
        time.sleep(3)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
