
"""
    模块功能描述：提供上位机相关的路径信息
    模块全局变量：g_commonpath
    模块类：CommonPath
    @Author:xumeng
    @Date:2024/5/21
    修改记录
"""
import os.path
import shutil
import threading
import time




class CommonPath:
    """
        类功能描述：提供项目的路径配置，此路径可以看群知识库中目录思维导图
                  运行目录正常不可以改变，运行目录如果改变，上位机日志器需要重新创建
                  运行项目改变时，对应的测试日志器需要重新创建
                  此类为单列模式
        函数：
        属性：
        注意：打印上位机日志，不要在函数中动态引入 上位机日志系统，否则会引起循环依赖
        @Author:xumeng
        @Date:2024/5/21
        修改记录：
    """
    # 单列对象
    __instance = None
    # 加锁，提供线程安全
    _lock = threading.RLock()

    def __new__(cls, *args, **kwargs):
        # 创建类对象时不需要args和kwargs参数
        print("CommonPath:fn:new")
        with cls._lock:
            if cls.__instance is None:
                print("instance = None")
                cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self,path:str="D:\\test"):
        print("cls:CommonPath fn:init")
        # 判断对象是否创建过
        if not hasattr(self, "__default_project_name"):
            # 配置初始化的地方

            # 默认项目信息,当没有项目配置时时有默认信息
            self.__default_project_name = "project"
            self.__default_test_type = "测试"
            self.__default_test_rounds = "1"
            self.__default_project_version = "v1.0"
            # 项目信息
            self.__project_name = None
            self.__test_type = None
            self.__test_rounds = None
            self.__project_version = None

            # 目录名称的定义
            # 1级目录
            # 上位机运行的当前目录
            self.__upercompter_run_dir = path
            # 2级目录-3级目录
            # 2级配置文件目录-3级当前配置文件目录
            # 2级配置文件目录-3级当前配置文件目录-配置文件config.ini
            self.__two_config_date_dir_name = "02_ConfigDate"
            self.__three_defult_config_dir_name = "01_DefultConfig"
            self.__three_cur_config_dir_name = "02_CurConfig"
            self.__cur_config_file_name = "config.ini"
            # 2级软件工具目录
            self.__two_sofeware_tool_dir_name = "03_SoftwareTools"
            # 2级日志目录-2级上位机日志
            self.__two_log_dir_name = "04_Log"
            self.__three_uppercompter_log_dir_name = "01_UpperCompterLogs"
            # 2级项目目录-3级动态项目目录 属性函数获取
            # 2级项目目录-3级动态项目目录-4级测试用例
            # 2级项目目录-3级动态项目目录-4级测试用例-5级脚本源码
            # 2级项目目录-3级动态项目目录-4级测试用例-5级脚本文件
            # 2级项目目录-3级动态项目目录-4级测试结果
            # 2级项目目录-3级动态项目目录-4级测试结果动态目录-5级当前运行的测试结果动态目录 属性函数获取
            # 2级项目目录-3级动态项目目录-4级测试结果动态目录-5级当前运行的测试结果动态目录-6级测试用例日志
            # 2级项目目录-3级动态项目目录-4级测试结果动态目录-5级当前运行的测试结果动态目录-6级截图

            # 2级项目目录-3级动态项目目录-4级模版图片
            # 2级项目目录-3级动态项目目录-4级模版图片-5级模版图片1
            # 2级项目目录-3级动态项目目录-4级模版图片-5级模版图片2
            # 2级项目目录-3级动态项目目录-4级上位机
            self.__two_project_dir_name = "05_Project"

            self.__four_testcase_dir_name = "02_TestCase"
            self.__five_sourcecode_dir_name = "01_SourceCode"
            self.__five_sourcefile_dir_name = "02_ScriptFile"

            self.__four_testcaseresult_dir_name = "03_TestCaseResult"
            self.__six_testcase_log_dir_name = "02_TestCase_Logs"
            self.__six_screenshot_dir_name = "03_Screenshot"

            self.__four_template_iamge_dir_name = "04_Templated_Image"
            self.__five_template_one_dir_name = "01_Template"
            self.__five_template_two_dir_name = "02_Template"

            self.__four_vehicleuppercompter_dir_name = "05_VehicleUpperCompter"
            # self.upper_log = Base_Log(Log_Config("uppercomper_logger", "log_uppercompter", self.uppercompter_config_path,
            #                                      self.uppercompter_log_dir))
            # self.testcase_log = Base_Log(Log_Config("testcase_logger", "log_testcase", self.uppercompter_config_path,
            #                                         self.testcase_log_dir))
            self.init_config_files()  # 初始化配置文件
        # 路径拼接
    def __str__(self):
        return f"运行目录：{self.upercompter_run_dir} 项目名称：{self.project_name} " \
               f"项目版本:{self.project_version} 测试类型：{self.test_type} 测试运行轮次：{self.test_rounds}"

    def init_config_files(self):
        """
            初始化配置文件 按照路径查询config.ini配置文件是否存在， 如果不存在的话， 从项目中拷贝一份作为默认配置
        """
        if not os.path.isfile(self.uppercompter_config_path) or not os.path.exists(self.uppercompter_config_path):
            # 获取当前脚本的目录 并构建到config.txt的路径
            source_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'asettings', 'config.ini')
            # 确保目标目录存在，如果不存在则创建 复制并重命名文件
            os.makedirs(os.path.dirname(self.uppercompter_config_path), exist_ok=True)
            shutil.copyfile(source_path, self.uppercompter_config_path)

    def retset_project_info(self):
        """
            函数功能描述：测试任务运行结束重置项目信息到默认项目信息
        """
        self.__project_name = None
        self.__test_type = None
        self.__project_version = None
        self.__test_rounds = None
        from robotlib.init.init import g_uper_log
        g_uper_log.debug("重置项目信息-清空")

    def set_project_info(self, project_name, project_version, test_type, test_rounds, base_log):
        """
            函数功能藐视：设置项目信息
            Param:
                project_name:项目名称
                project_version：项目版本号
                test_type：测试类型
                test_rounds:测试轮次
                base_log:测试用例文件输出日志系统
            Return: 项目信息是否有变化 True:变化  False:无变化
        """
        from robotlib.init.init import g_uper_log
        g_uper_log.debug(f"设置项目信息 项目名称：{project_name} 项目版本：{project_version} 测试类型：{test_type} 测试轮次：{test_rounds}")
        print(f"项目名称：{project_name} 项目版本：{project_version} 测试类型：{test_type} 测试轮次：{test_rounds}")
        print(f"原有项目名称：{self.project_name} 项目版本：{self.project_version} "
                       f"测试类型：{self.test_type} 测试轮次：{self.test_rounds}")
        g_uper_log.debug(f"原有项目信息 项目名称：{project_name} 项目版本：{project_version} 测试类型：{test_type} 测试轮次：{test_rounds}")
        b_change = True
        if self.__project_name == project_name and self.__test_type == test_type and self.__project_version == project_version and self.__test_rounds == test_rounds:
            print("项目信息没有变化")
            g_uper_log.debug("项目信息没有变化")
            b_change = False
        else:
            b_change = True
            self.__project_name = project_name
            self.__test_type = test_type
            self.__project_version = project_version
            self.__test_rounds = test_rounds
            b_change = base_log.change_save_dir_filelog(self.testcase_log_dir)
        return b_change

    @property
    def upercompter_run_dir(self):
        """
            函数功能描述：获取当前运行的项目名称
            Return: __upercompter_run_dir
        """
        return self.__upercompter_run_dir

    @upercompter_run_dir.setter
    def upercompter_run_dir(self, upercompter_run_dir):
        """
            函数功能描述：设置当前运行的路径
            Param:
                upercompter_run_dir:当前运行的项目名称
        """

        #self.upper_log.debug("设置当前运行项目：%s", upercompter_run_dir)
        self.__upercompter_run_dir = upercompter_run_dir


    @property
    def project_name(self):
        """
            函数功能描述：获取当前运行的项目名称
            Return: __project_name
        """

        if self.is_run_project_dir_config:
            return self.__project_name
        else:
            return self.__default_project_name

    @property
    def test_type(self):
        """
            函数功能描述：获取当前运行的测试类型
            Return: __test_type
        """
        if self.is_run_project_dir_config:
            return self.__test_type
        else:
            return  self.__default_test_type


    @property
    def project_version(self):
        """
            函数功能描述：获取当前运行的项目版本
            Return: __project_version
        """
        if self.is_run_project_dir_config:
            return self.__project_version
        else:
            return self.__default_project_version

    @property
    def test_rounds(self):
        """
            函数功能描述：获取当前运行的测试轮次
            Return: __test_rounds
        """
        if self.is_run_project_dir_config:
            return self.__test_rounds
        else:
            return self.__default_test_rounds

    @property
    def is_run_project_dir_config(self):
        """
            函数功能描述：获取当前项目配置情况
            Retrun: True  当前项目目录已配置
                    False 当前项目目录没有配置
        """
        if self.__project_name is None:
            return False
        else:
            return True


    @property
    def uppercompter_config_path(self):
        """
            函数功能描述：获取上位置配置文件路径
            Retrun:上位机配置文件路径file_path
            规则：upercompter_run_dir\\__two_config_date_dir_name\\__three_cur_config_dir_name\\__cur_config_file_name
        """

        file_path = os.path.join(self.upercompter_run_dir,
                            self.__two_config_date_dir_name,
                            self.__three_cur_config_dir_name,
                            self.__cur_config_file_name)

        print("上位机配置文件路径：%s" % file_path)
        return file_path

    @property
    def uppercompter_log_dir(self):
        """
            函数功能描述：获取上位机日志目录
            Retrun:上位机日志目录
            规则：upercompter_run_dir\\__two_log_dir_name\\__three_uppercompter_log_dir_name
        """
        dir_path = os.path.join(self.upercompter_run_dir,
                                self.__two_log_dir_name,
                                self.__three_uppercompter_log_dir_name)
        print("上位机日志目录：%s" % dir_path)
        return dir_path

    @property
    def cur_project_dynamic_dir(self):
        """
            函数功能描述：获取当前项目目录
            Retrun:获取当前项目目录
            规则：upercompter_run_dir\\__two_project_dir_name\\project_name
        """
        dir_path = None
        dir_path = os.path.join(self.upercompter_run_dir,
                                self.__two_project_dir_name,
                                self.project_name)
        #print("前项目目录：%s" % dir_path)
        return dir_path

    @property
    def templated_image_01_templated_dir(self):
        """
            函数功能描述：获取模版一目录
            Retrun:获取模版一目录
            规则：cur_project_dynamic_dir\\__four_template_iamge_dir_name\\__five_template_one_dir_name
        """
        dir_path = None
        dir_path = os.path.join(self.cur_project_dynamic_dir,
                                self.__four_template_iamge_dir_name,
                                self.__five_template_one_dir_name)
        print("模版一目录：%s" % dir_path)
        return dir_path

    @property
    def templated_image_02_templated_dir(self):
        """
            函数功能描述：获取模版二目录
            Retrun:获取模版二目录
            规则：cur_project_dynamic_dir\\__four_template_iamge_dir_name\\__five_template_two_dir_name
        """
        dir_path = None
        dir_path = os.path.join(self.cur_project_dynamic_dir,
                                self.__four_template_iamge_dir_name,
                                self.__five_template_two_dir_name)
        print("模版二目录：%s" % dir_path)
        return dir_path

    @property
    def tasecase_run_result_dynamic_dir(self):
        """
            函数功能描述：获取当前项目测试任务运行结果动态目录
            Retrun:项目测试任务运行结果动态目录
            规则：cur_project_dynamic_dir_name\\__four_testcaseresult_dir_name\\测试类型_版本_轮次
        """
        testResult = f"{self.test_type}_{self.project_version}_{self.test_rounds}"
        dir_path = None
        dir_path = os.path.join(self.cur_project_dynamic_dir,
                                self.__four_testcaseresult_dir_name,
                                testResult)
        print("测试用例结果动态目录：%s" % dir_path)
        return dir_path

    @property
    def testcase_log_dir(self):
        """
            函数功能描述：获取上位机日志目录
            Retrun:测试用例日志目录
            规则：tasecase_run_result_dynamic_dir_name\\__six_testcase_log_dir_name
        """
        dir_path = os.path.join(self.tasecase_run_result_dynamic_dir, self.__six_testcase_log_dir_name)
        print("测试用例日志目录：%s" % dir_path)
        return dir_path

    @property
    def testcase_screenshot_dir(self):
        """
            函数功能描述：获取测试用例截图目录
            Retrun:测试用例截图目录
            规则：tasecase_run_result_dynamic_dir_name\\__six_testcase_log_dir_name
        """
        dir_path = os.path.join(self.tasecase_run_result_dynamic_dir, self.__six_screenshot_dir_name)
        print("测试用例截图目录：%s" % dir_path)
        return dir_path


if __name__ == '__main__':
    time.sleep(3)
    print("test start")
    from robotlib.init.init import g_testcase_log, g_uper_log

    common_path = CommonPath()
    # 配置上位机运行目录
    common_path.upercompter_run_dir = "D:\\test"
    # 配置项目信息
    common_path.set_project_info("FS11_A3", "v1.0", "集成测试", "1", g_testcase_log)
    # 上位机配置文件路径
    print(common_path.uppercompter_config_path)
    # 上位机日志目录
    print(common_path.uppercompter_log_dir)
    # 项目动态目录
    print(common_path.cur_project_dynamic_dir)
    # 项目模版一目录
    print(common_path.templated_image_01_templated_dir)
    # 项目模版二目录
    print(common_path.templated_image_02_templated_dir)
    # 测试结果动态目录
    print(common_path.tasecase_run_result_dynamic_dir)
    # 测试用例日志目录
    print(common_path.testcase_log_dir)
    # 测试用例截图目录
    print(common_path.testcase_screenshot_dir)
    print(common_path)
