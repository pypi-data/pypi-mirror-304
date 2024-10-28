import configparser
import os

from robotlib.devices.device_manager.device_type_define import NotificationSubTypeEnum
from robotlib.init.init import g_uper_log, g_commonpath

class Notification_Config:
    """
    类功能描述：通知配置类，从配置文件中获取
    """
    def __init__(self):
        """
        函数功能描述：初始化
        :param section: 配置文件中的section
        :param fconfig_path: 配置文件路径
        """
        g_uper_log.info("通知配置类")
        self.__dict = dict()
        self.__client_config_support_count = 1
        self.__config_client_name = 'dingding'
        self.__load_config("notification_client", g_commonpath.uppercompter_config_path)
        if self.client_config_support_count > 0:
            for i in range(self.client_config_support_count):
                # 拼接配置文件SECTION
                section_name = f"notification_client_{i + 1}"
                notification_client_config = Notification_Client_Config(section_name,
                                                                        g_commonpath.uppercompter_config_path)
                g_uper_log.debug(notification_client_config)
                self.__dict[notification_client_config.client_name] = notification_client_config
        g_uper_log.info(f"所有通知配置信息：{self.__dict}")

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
            self.__client_config_support_count = config.getint(section, "client_config_support_count", fallback="")
            g_uper_log.debug(f"钉钉通知URL = {self.client_config_support_count}")
        except Exception as e:
            g_uper_log.exception(str(e))


    @property
    def client_config_support_count(self):
        return self.__client_config_support_count
    @property
    def client_configs_dict(self):
        return self.__dict
    @property
    def config_client_name(self):
        return self.__config_client_name


class Notification_Client_Config:
    """
    类功能描述：通知配置类，从配置文件中获取
    """
    def __init__(self, section: str, fconfig_path: str):
        """
        函数功能描述：初始化
        :param section: 配置文件中的section
        :param fconfig_path: 配置文件路径
        """
        self.__load_config(section, fconfig_path)

    def __str__(self):
        return f"配置的客户端名称：{self.client_name}" \
               f"配置的url：{self.url}"\
               f"配置的账号：{self.account} "\
               f"配置的密码：{self.password}"\
               f"配置的类型：{self.client_sub_type_enum}"
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
            self.__client_name = config.get(section, "client_name", fallback="")
            g_uper_log.debug(f"client_name -> {self.client_name}")
            self.__url = config.get(section, "url", fallback="")
            g_uper_log.debug(f"url -> {self.url}")
            self.__account = config.get(section, "account", fallback="")
            g_uper_log.debug(f"account -> {self.account}")
            self.__password = config.get(section, "password", fallback="")
            g_uper_log.debug(f"password -> {self.password}")
            # self.__client_sub_type_enum = config.getint(section, "client_sub_type_enum", fallback="-1")
            # g_uper_log.debug(f"client_sub_type_enum -> {self.client_sub_type_enum}")
            temp_client_sub_type_enum = config.getint(section, "client_sub_type_enum", fallback="-1")
            g_uper_log.debug(f"client_sub_type_enum -> {temp_client_sub_type_enum}")
            self.__client_sub_type_enum = self.__client_subtype_conversion_to_eum(temp_client_sub_type_enum)
        except Exception as e:
            g_uper_log.exception(str(e))


    @property
    def client_name(self):
        return self.__client_name
    @property
    def url(self):
        return self.__url
    @property
    def account(self):
        return self.__account
    @property
    def password(self):
        return self.__password
    # @property
    # def client_sub_type_enum(self):
    #     return self.__client_sub_type_enum
    @property
    def client_sub_type_enum(self):
        return self.__client_sub_type_enum

    def __client_subtype_conversion_to_eum(self, client_subtype:int):
        """
            函数功能说明：设备子类型int转enum,从配置文件读取出来的值转CODE中的ENUM
            Param:
                device_subtype(int):设备类型
            Retrun:DeviceRelaySingleSubTypeEnum
        """
        if client_subtype == 0:
            return NotificationSubTypeEnum.DING_TALK
        elif client_subtype == 1:
            return NotificationSubTypeEnum.E_MAIL
        else:
            return NotificationSubTypeEnum.NONE


if __name__ == '__main__':
    # 测试所有的配置读取是否正确
    notification_config = Notification_Config("notification_client", g_commonpath.uppercompter_config_path)
    g_uper_log.debug(notification_config)