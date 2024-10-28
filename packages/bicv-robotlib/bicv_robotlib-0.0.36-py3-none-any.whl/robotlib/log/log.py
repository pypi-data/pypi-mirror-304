"""
模式功能描述：提供日志打印系统，此系统师线程安全，但不是进程安全，只能跨线程使用，不能跨进程使用
           两种类别的日志输出系统：上位机日志和测试脚本日志
           每种日志输出系统可以有两种输出：控制台日志输出和文件日志输出
           每种日志系统可以通过配置文件配置
模块及全局变量：
           上位机日志系统全局变量  uper_log
           测试系统全局变量       testcase_log
类：Base_Log
@author:xumeng
@date:2024/5/18
"""
# encoding=utf-8
import logging
import os.path
import threading
from logging import handlers
from logging.handlers import RotatingFileHandler
import time
from robotlib.log.log_config import Log_Config
import queue


class Base_Log:
    """
    功能描述：日志基类
    接口：
    属性：
    修改记录：
    @autor:xumeng
    """

    def __init__(self, log_config):
        print("cls:Base_Log fn:__init__")
        print(log_config)
        # 日志器配置
        self.log_config = log_config

        # 日志器名

        # self.logger = logging.getLogger("deflut")
        # Base_Log.__logger = logging.getLogger("deflut")
        self.__log_show_callback = None
        self.__logger = logging.getLogger(log_config.logger_name)
        print(f"创建日志记录器：{log_config.logger_name}")

        self.console_handler = None
        self.file_handler = None
        self.xx_handle = None
        nullhandler = logging.NullHandler()
        # self.logger.addHandler(nullhandler)
        self.__logger.addHandler(nullhandler)
        self.__init_Logger()

    def __init_Logger(self):
        """
        功能描述：日志记录器初始化函数
        参数1：log_config 日志器配置信息

        """
        print("fn:__init_Logger 初始化日志处理器")
        # print(self.log_config )
        log_config = self.log_config
        # 创建日志器
        # logger = logging.getLogger(log_config.logger_name)
        # print(f"创建日志记录器：{log_config.logger_name}")

        # 设置all.log文件的日志最低级别为DEBUG
        self.__logger.setLevel(logging.DEBUG)
        print(f"控制台开关：{log_config.enable_consolelog} 文件开关：{log_config.enable_filelog}")
        # 创建一个格式化器
        formatter_filelog = logging.Formatter(log_config.filelog_format)
        formatter_consolelog = logging.Formatter(log_config.consolelog_format)
        # print(f"文件日志输出格式{log_config.filelog_format}")
        # print(f"控件台日志输出格式{log_config.consolelog_format}")

        logging.raiseExceptions = False
        self.log_queue_handler = logging.handlers.QueueHandler(queue.Queue(2000))
        self.log_queue_handler.setFormatter(formatter_filelog)
        self.log_queue_handler.setLevel(logging.DEBUG)
        self.__logger.addHandler(self.log_queue_handler)
        # logging.raiseExceptions = True :
        # 如果发生了异常（例如由于有界队列已满），则会调用 handleError() 方法来处理错误。消息被打印到 sys.stderr (如果 logging.raiseExceptions 为 True)。不影响用户的日志记录
        # logging.raiseExceptions = False:
        # 如果发生了异常（例如由于有界队列已满），则记录被静默地丢弃。
        # 补充说明:
        # 调用emit()期间遇到异常时，应从处理器中调用此方法。如果模块级属性raiseExceptions是False，则异常将被静默忽略。
        # logging.raiseExceptions =False 这是大多数情况下日志系统需要的 —— 大多数用户不会关心日志系统中的错误，他们对应用程序错误更感兴趣。
        # 但是，你可以根据需要将其替换为自定义处理器。指定的记录是发生异常时正在处理的记录。（raiseExceptions的默认值是True，因为这在开发过程中是比较有用的）。

        if log_config.enable_filelog or log_config.enable_consolelog:
            # 日志开关有一个开的
            if log_config.enable_consolelog:
                # 构建控制台相关
                # 创建控制台处理器  stderr in put
                print("构建控制台处理器")
                consoleHandler = logging.StreamHandler()
                consoleHandler.setLevel(log_config.consolelog_level)
                consoleHandler.setFormatter(formatter_consolelog)
                # 添加处理器
                print("添加控制台日志处理器")
                self.__logger.addHandler(consoleHandler)
                self.console_handler = consoleHandler
            if log_config.enable_filelog:
                # 构建文件相关
                # 创建处理器
                print("构建文件日志处理器")
                fileHandler = None
                if log_config.filelog_savetype == 2:
                    # 创建文件大小分割处理器
                    fileHandler = RotatingFileHandler(filename=log_config.filelog_filepath,
                                                      maxBytes=log_config.filelog_max_szie,
                                                      backupCount=log_config.filelog_backcount)
                    # 设置处理器输出格式
                    fileHandler.setFormatter(formatter_filelog)

                    # 设置处理器日志输出等级
                    fileHandler.setLevel(log_config.filelog_level)
                    print("添加文件日志处理器-文件分割类型")
                    self.__logger.addHandler(fileHandler)
                else:
                    # 创建以日期分割处理器
                    fileHandler = logging.handlers.TimedRotatingFileHandler(filename=log_config.filelog_filepath,
                                                                            when=log_config.filelog_when,
                                                                            interval=log_config.filelog_when_interval,
                                                                            backupCount=log_config.filelog_when_backcount,
                                                                            utc=log_config.filelog_when_utc,
                                                                            )
                    # 设置处理器输出格式
                    fileHandler.setFormatter(formatter_filelog)
                    # 设置处理器日志输出等级
                    fileHandler.setLevel(log_config.filelog_level)
                    print("添加文件日志处理器-日期分割类型")
                    self.__logger.addHandler(fileHandler)
                self.file_handler = fileHandler
        else:
            # 日志开关都没有开
            print("创建空处理器")
            nullhandler = logging.NullHandler()
            print("添加空日志处理器")
            self.__logger.addHandler(nullhandler)
        # self.logger = logger
        print("构建日记器完成")

    def change_save_dir_filelog(self, ffilelog_dir):
        """
            函数功能描述：日志保存目录，切换处理器
            Param:
                ffilelog_dir:日志文件保存目录
            Retrun: True 处理器切换成功 False 处理器切换识别
        """
        print(f"改变日志处理器文件存储目录：{ffilelog_dir}")
        print(f"原先日志处理器文件存储目录：{self.log_config.filelog_dir}")
        b_reslut = False
        # 判断目录是否是目录

        if ffilelog_dir.lower() == self.log_config.filelog_dir.lower():
            print("路径相同无需切换")
            b_reslut = False
            return b_reslut
        if not os.path.exists(ffilelog_dir):
            print("目录不存在创建目录,创建目录")
            os.makedirs(ffilelog_dir, exist_ok=True, mode=0o755)
        if not os.path.isdir(ffilelog_dir):
            print("路径不是目录")
            b_reslut = False
            return b_reslut
        self.log_config.filelog_dir = ffilelog_dir
        print(self.log_config)
        log_config = self.log_config
        logger = self.__logger
        print(f"控制台开关：{log_config.enable_consolelog} 文件开关：{log_config.enable_filelog}")
        if log_config.enable_filelog:
            # 创建一个格式化器
            formatter_filelog = logging.Formatter(log_config.filelog_format)
            # 构建文件相关
            # 创建处理器
            print("构建文件日志处理器")
            fileHandler = None
            if self.file_handler:
                print("文件处理器存在，移除此文件处理器")
                logger.removeHandler(self.file_handler)
            if log_config.filelog_savetype == 2:
                # 创建文件大小分割处理器
                fileHandler = RotatingFileHandler(filename=log_config.filelog_filepath,
                                                  maxBytes=log_config.filelog_max_szie,
                                                  backupCount=log_config.filelog_backcount)
                # 设置处理器输出格式
                fileHandler.setFormatter(formatter_filelog)
                # 设置处理器日志输出等级
                fileHandler.setLevel(log_config.filelog_level)
                print("添加文件日志处理器-文件分割类型")
                logger.addHandler(fileHandler)
            else:
                # 创建以日期分割处理器
                fileHandler = logging.handlers.TimedRotatingFileHandler(filename=log_config.filelog_filepath,
                                                                        when=log_config.filelog_when,
                                                                        interval=log_config.filelog_when_interval,
                                                                        backupCount=log_config.filelog_when_backcount,
                                                                        utc=log_config.filelog_when_utc,
                                                                        )
                # 设置处理器输出格式
                fileHandler.setFormatter(formatter_filelog)
                # 设置处理器日志输出等级
                fileHandler.setLevel(log_config.filelog_level)
                print("添加文件日志处理器-日期分割类型")
                logger.addHandler(fileHandler)
            self.file_handler = fileHandler
            print("构建日记器完成")
            b_reslut = True
        else:
            b_reslut = False
            print("文件日志开关没有打开")
        return True

    def _get_logstr_from_squenue_handler(self):
        '''
        返回日志对象内部队列处理器一条记录
        :return:
        '''

        return self.log_queue_handler.queue.get()

    def _squenue_handler_logstr_count(self):
        """
        返回日志器对象内部队列处理器中记录个数
        :return:
        """
        return self.log_queue_handler.queue._qsize()

    def get_child(self, module_name: str = None):
        """
        返回对象日志器的次一级日志记录器。模块调用
        :param module_name:
        :return:
        """
        return self.__logger.getChild(module_name)

    def get_logger(self):
        """
        返回本对象的日志处理器对象
        :return:
        """
        return self.__logger

    def _log_show_backthread_func(self):
        while True:
            time.sleep(0.01)
            if self.__log_show_callback != None:
                if self._squenue_handler_logstr_count() > 0:
                    log_str_for_show = self._get_logstr_from_squenue_handler()
                    self.__log_show_callback(log_str_for_show.msg)

    def set_log_show_callback_func(self, func=None):
        '''
        设置日志内容回调函数
        :param func: func 回调函数。形如  show_log(log_mes:str=None) 参数log_mes是字符串类型
        :return:None
        '''
        if func == None:
            raise Exception("func ==None")
        self.__log_show_callback = func
        self.__log_show_backthread_handle = threading.Thread(target=self._log_show_backthread_func)
        self.__log_show_backthread_handle.daemon = True
        self.__log_show_backthread_handle.start()

    def log(self, level, msg, *args, **kwargs):
        """
        函数功能描述：输出warning日志
        Args：
        msg:日志信息
        *args：
        **kwargs： 参数说明详见debug函数
        Retruns：
        Raises：
        修改记录：
        """
        self.__logger.log(level, msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs):
        """
        函数功能描述：输出Debug级日志
        Args：
            msg:日志信息
            *args：msg 是消息格式字符串，而 args 是用于字符串格式化操作合并到 msg 的参数。当未提供 args 时，不会对 msg 执行 ％ 格式化操作。
            **kwargs： exc_info，默认false,如果未true，则会将异常信息添加到日志信息中，如果没有异常信息则将None添加到日志信息中
                      stack_info，默认false,如果未true,则将堆栈信息添加到日志消息中，包括实际的日志调用
                      stacklevel,默认为 1 。如果大于 1 ，则在为日志记录事件创建的 LogRecord 中计算行号和函数名时，将跳过相应数量的堆栈帧
                      extra,传递一个字典，该字典用于填充为日志记录事件创建的、带有用户自定义属性的 LogRecord 中的 __dict__
        Retruns：
        Raises：
        Example: debug("日志")  debug("日志%d %d",i1,i2)  debug("日志%d %d",i1,i2,exc_info = true)
        修改记录：
        """
        self.__logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        函数功能描述：输出warning日志
        Args：
        msg:日志信息
        *args：
        **kwargs： 参数说明详见debug函数
        Retruns：
        Raises：
        修改记录：
        """
        # print("msg:"+msg)
        # print("args:"+str(args))
        # print("kwargs:"+str(kwargs))
        self.__logger.warning(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        函数功能描述：输出info基本日志
        Args：
        msg:日志信息
        *args：
        **kwargs： 参数说明详见debug函数
        Retruns：
        Raises：
        修改记录：
        """
        # self.logger.info(msg, *args, **kwargs)
        # if Base_Log.__logger != None:
        self.__logger.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        函数功能描述：输出error基本日志
        Args：
        msg:日志信息
        *args：
        **kwargs： 参数说明详见debug函数
        Retruns：
        Raises：
        修改记录：
        """
        self.__logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        函数功能描述：输出critical基本日志
        Args：
        msg:日志信息
        *args：
        **kwargs： 参数说明详见debug函数
        Retruns：
        Raises：
        修改记录：
        """
        self.__logger.critical(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """
        函数功能描述：输出exception基本日志
        Args：
        msg:日志信息
        *args：
        **kwargs： 参数说明详见debug函数
        Retruns：
        Raises：
        修改记录：
        """
        self.__logger.exception(msg, *args, **kwargs)


def show(logg=None):
    print('pp==='+logg)
    pass

if __name__ == '__main__':
    # setting id
    time.sleep(3)
    from robotlib.init.init import g_testcase_log
    from robotlib.init.init import g_uper_log

    uper_log = g_uper_log
    testcase_log = g_testcase_log

    uper_log.set_log_show_callback_func(show)
    # 验证日志输出是否正常
    # 不带格式化参数

    uper_log.get_logger().warning("heellow")

    uper_log.get_logger().warning("test_no_param1")
    uper_log.get_logger().warning("test_no_param2")
    uper_log.get_logger().warning("test_no_param3")
    uper_log.get_logger().warning("test_no_param4")
    # 带1个格式化参数 和 2个格式化参数
    i1 = 1
    i2 = 2
    uper_log.get_logger().warning("test_one_param:%d", i1)
    uper_log.get_logger().warning("test_one_param:%d %d", i1, i2)
    # 不带格式化参数及有额外参数exc_info
    uper_log.get_logger().warning("test_no_param", exc_info=True)
    time.sleep(60*100)
    # 一个格式化参数及有额外参数exc_info
    uper_log.get_logger().warning("test_extra_param:%d", i1, exc_info=True)
    # 一个格式化参数及有额外参数exc_info,stack_info
    uper_log.get_logger().warning("test_extra_param:%d", i1, exc_info=True, stack_info=True)
    # 一个格式化参数及有额外参数exc_info,stack_info
    uper_log.get_logger().warning("test_extra_param:%d", i1, exc_info=True, stack_info=True, stacklevel=2)
    # uppercomperlog = Base_Log(settings.uppercompter_log_config)
    # uper_log.warning("ddd")
    for i in range(10):
        # uper_log.info("Hello%d" % i)
        uper_log.get_logger().warning("Hello%d" % i)
        testcase_log.get_logger().warning("Hello%d" % i)
        time.sleep(3)
    # 切换文件输出目录测试
    testcase_log.get_logger().change_save_dir_filelog(
        "D:\\test\\05_Project\\project1\\03_TestCaseResult\\测试_v1.0_1\\02_TestCase_Logs")
    for i in range(10):
        uper_log.warning("Hello%d" % i)
        testcase_log.get_logger().warning("Hello%d" % i)
        time.sleep(3)
