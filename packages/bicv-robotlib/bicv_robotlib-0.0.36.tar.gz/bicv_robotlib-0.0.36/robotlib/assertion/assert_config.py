import configparser
import os
import shutil
from robotlib.devices.device_manager.device_type_define import AssertSubTypeEnum
from robotlib.init.init import g_uper_log, g_commonpath


class Assert_Config:
    """
    类功能描述：断言配置类，从配置文件中获取
    """

    def __init__(self):
        """
        函数功能描述：初始化
        :param section: 配置文件中的section
        :param fconfig_path: 配置文件路径
        """
        g_uper_log.info("断言配置类")
        self.__dict = dict()
        self.__client_config_support_count = 1
        self.__load_config("assert_scheme", g_commonpath.uppercompter_config_path)
        if self.scheme_config_support_count > 0:
            for i in range(self.scheme_config_support_count):
                # 拼接配置文件SECTION
                section_name = f"assert_scheme_{i + 1}"
                assert_scheme_config = Assert_Scheme_Config(section_name, g_commonpath.uppercompter_config_path)
                g_uper_log.debug(assert_scheme_config)
                self.__dict[assert_scheme_config.scheme_name] = assert_scheme_config
        g_uper_log.info(f"所有断言配置信息：{self.__dict}")

    def __load_config(self, section, fconfig_path):
        """
        函数功能描述：加载通知配置信息
        :param section: 配置文件section
        :param fconfig_path: 配置文件路径
        """
        g_uper_log.debug(f"读取配置:{section}")
        if not os.path.isfile(fconfig_path):
            g_uper_log.debug("配置文件路径不是文件路径")
            return
        if not os.path.exists(fconfig_path):
            g_uper_log.debug("配置文件路径不存在")
            return
        config = configparser.ConfigParser()
        readret = config.read(fconfig_path, encoding="utf-8")
        if len(readret) == 0:
            g_uper_log.debug("配置文件为空")
            return
        try:
            self.__scheme_config_support_count = config.getint(section, "scheme_config_support_count", fallback=0)
            g_uper_log.debug(f"钉钉通知URL = {self.scheme_config_support_count}")
        except Exception as e:
            g_uper_log.exception(str(e))

    @property
    def scheme_config_support_count(self):
        return self.__scheme_config_support_count

    @property
    def scheme_configs_dict(self):
        return self.__dict


class Assert_Scheme_Config:
    """
    类功能描述：断言方案配置类，从配置文件中获取
    """

    def __init__(self, section: str, fconfig_path: str):
        """
        函数功能描述：初始化
        :param section: 配置文件中的section
        :param fconfig_path: 配置文件路径
        """
        self.__load_config(section, fconfig_path)

    def __str__(self):
        return f"配置的方案名称：{self.scheme_name} " \
               f"配置的方案类型：{self.scheme_sub_type_enum}"

    def __load_config(self, section, fconfig_path):
        """
        函数功能描述：加载断言方案的配置信息
        :param section: 配置文件section
        :param fconfig_path: 配置文件路径
        """
        g_uper_log.debug(f"读取配置:{section}")
        if not os.path.isfile(fconfig_path):
            g_uper_log.debug("配置文件路径不是文件路径")
            return
        if not os.path.exists(fconfig_path):
            g_uper_log.debug("配置文件路径不存在")
            return
        config = configparser.ConfigParser()
        readret = config.read(fconfig_path, encoding="utf-8")
        if len(readret) == 0:
            g_uper_log.debug("配置文件为空")
            return
        try:
            self.__scheme_name = config.get(section, "scheme_name", fallback="")
            g_uper_log.debug(f"scheme_name -> {self.scheme_name}")
            scheme_sub_type_enum = config.getint(section, "scheme_sub_type_enum", fallback="-1")
            g_uper_log.debug(f"scheme_sub_type_enum -> {scheme_sub_type_enum}")
            self.__scheme_sub_type_enum = self.__scheme_subtype_conversion_to_eum(scheme_sub_type_enum)
        except Exception as e:
            g_uper_log.exception(str(e))

    @property
    def scheme_name(self):
        return self.__scheme_name

    @property
    def cache_path(self):
        return self.__cache_path

    @property
    def scheme_sub_type_enum(self):
        return self.__scheme_sub_type_enum

    def __scheme_subtype_conversion_to_eum(self, client_subtype: int):
        """
            函数功能说明：设备子类型int转enum,从配置文件读取出来的值转CODE中的ENUM
            Param:
                device_subtype(int):设备类型
            Retrun:DeviceRelaySingleSubTypeEnum
        """
        if client_subtype == -1:
            return AssertSubTypeEnum.NONE
        elif client_subtype == 0:
            return AssertSubTypeEnum.CAMERA
        elif client_subtype == 1:
            return AssertSubTypeEnum.CAN
        else:
            return AssertSubTypeEnum.NONE



