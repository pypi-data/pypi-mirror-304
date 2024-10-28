"""
    模块描述：CAN基础配置，单个设备配置
"""

import configparser
import os
from robotlib.devices.device_manager.device_type_define import *
from robotlib.init.init import g_uper_log, g_commonpath


class CAN_Device_Config:
    """
        类功能描述：CAN配置类，从配置文件中获取
    """

    def __init__(self, section: str, fconfig_path: str):
        """
            函数功能描述：初始化
            Param:
                section：
                fconfig_path:
        """
        # 设备通用类配置
        self.device_type_enum = DeviceTypeEnum.CAN
        self.device_sub_type_enum = None
        self.device_state_enum = DeviceStateEnum.NONE
        self.program_control_type_enum = ProgramControlTypeEnum.PROGRAM_CONTROL
        # 设备专业性配置
        self.__device_name = "GCAN"
        self.__re_device_init = True
        self.__load_config(section, fconfig_path)

    def __str__(self):
        return f"设备类型str：{self.device_type_enum.name} " \
               f"设备子类型: {self.device_sub_type_enum} " \
               f"设备状态: {self.device_state_enum} " \
               f"设备编程能力: {self.program_control_type_enum} " \
               f"设备名称: {self.device_name} " \
               f"操作方式重新初始化：{self.re_device_init}"

    def __load_config(self, section, fconfig_path):
        """
            函数功能描述：加载日志配置信息
            参数：
                section ：配置文件section
                fconfig_path:配置文件路径
            修改记录：
            @author:
            @date:
        """
        g_uper_log.debug(f"读取配置:{section}")
        if not os.path.isfile(fconfig_path):
            g_uper_log.debug("配置文件路径不是文件路径")
            return
        # 判断路径文件是否存在
        if not os.path.exists(fconfig_path):
            g_uper_log.debug("配置文件路径不存在")
            return
        # 读取配置文件
        config = configparser.ConfigParser()
        readret = config.read(fconfig_path, encoding="utf-8")
        if (len(readret)) == 0:
            g_uper_log.debug("配置文件为空")
            return
        try:
            # 默认配置
            # 设备子类型
            # 读取设备子类型
            device_sub_type = config.getint(section, "device_sub_type", fallback=1)
            g_uper_log.debug(f"设备子类型 = {device_sub_type} type:{type(device_sub_type)}")
            self.device_sub_type_enum = self.__device_subtype_conversion_to_enum(device_sub_type)

            # 读取设备编程能力
            device_program_control = config.getboolean(section, "device_program_control", fallback=False)
            g_uper_log.debug(f"设备编程能力 = {device_program_control} ype:{type(device_program_control)}")
            self.program_control_type_enum = self.__device_program_control_to_enum(device_program_control)

            # 读取设备状态
            device_status = config.getint(section, "device_state_enum", fallback=0)
            g_uper_log.debug(f"设备状态 = {device_status}")
            self.device_state_enum = self.__device_statue_to_enum(device_status)
            g_uper_log.debug(f"设备状态 = {self.device_state_enum}")
            # 读取设备名称
            self.__device_name = config.get(section, "device_name", fallback="relay_three_side_xxx")
            g_uper_log.debug(f"设备名称 = {self.device_name} {type(self.device_name)}")
            # 读取设备操作方式
            self.__re_device_init = config.getboolean(section, "re_device_init", fallback=True)
            g_uper_log.debug(f"设备操作方式重新初始化 = {self.re_device_init}")

            self.__re_device_init = config.getboolean(section, "re_device_init", fallback=True)
            g_uper_log.debug(f"设备操作方式重新初始化 = {self.re_device_init}")

            self.__can_standard = config.get(section, "can_standard", fallback='can')
            g_uper_log.debug(f"CAN 标准 = {self.re_device_init}")

            self.__can_aisle = config.getint(section, "aisle", fallback=1)
            g_uper_log.debug(f"CAN 通道 = {self.re_device_init}")

        except Exception as e:
            g_uper_log.exception(str(e))

    def __device_subtype_conversion_to_enum(self, device_subtype: int):
        """
            函数功能说明：设备子类型int转enum,从配置文件读取出来的值转CODE中的ENUM
            Param:
                device_subtype(int):设备类型
            Retrun:DeviceMultimeterSubTypeEnum
        """
        if device_subtype == 1:
            return DeviceCANEnum.GCAN
        elif device_subtype == 2:
            return DeviceCANEnum.TOMOS
        else:
            return DeviceCANEnum.NONE

    def __device_program_control_to_enum(self, device_program_control: bool):
        """
            函数功能说明：设备子类型int转enum,从配置文件读取出来的值转CODE中的ENUM
            Param:
                    device_program_control(bool):设备编程能力
                    Retrun:ProgramControlTypeEnum
            """
        if device_program_control:
            return ProgramControlTypeEnum.PROGRAM_CONTROL
        else:
            return ProgramControlTypeEnum.NOT_PROGRAM_CONTROL

    def __device_statue_to_enum(self, device_status: int):
        """
            函数功能说明：设备状态int转enum,从配置文件读取出来的值转CODE中的ENUM
            Param:
                    device_status(int):设备状态
                    Retrun:DeviceStateEnum
            """
        if device_status == 1:
            return DeviceStateEnum.ON
        elif device_status == 2:
            return DeviceStateEnum.OFF
        elif device_status == 3:
            return DeviceStateEnum.TROUBLE
        else:
            return DeviceStateEnum.NONE

    @property
    def device_name(self):
        return self.__device_name

    @property
    def re_device_init(self):
        return self.__re_device_init

    @property
    def device_can_aisle(self):
        return self.__can_aisle

    @property
    def device_can_standard(self):
        return self.__can_standard


class CAN_Config:
    """
        类功能描述：CAN模块所有配置相关
    """

    def __init__(self):
        g_uper_log.info("can设备基础配置")
        self.__device_config_support_count = 1
        self.__config_device_name = "GCAN"
        self.__dict = dict()
        # 读取配置文件
        self.__load_config("can_dev", g_commonpath.uppercompter_config_path)

        if self.device_config_support_count > 0:
            for i in range(self.device_config_support_count):
                # 拼接配置文件SECTION
                section_name = f"can_dev_{1 + i}"
                can_device_config = CAN_Device_Config(section_name,
                                                      g_commonpath.uppercompter_config_path)
                g_uper_log.debug(can_device_config)
                self.__dict[can_device_config.device_name] = can_device_config

    def __str__(self):
        return f"can配置： 支持设备数量：{self.device_config_support_count} 设备列表：{self.device_configs_dict}"

    def __load_config(self, section, fconfig_path):
        """
                    函数功能描述：加载日志配置信息
                    参数：
                        section ：配置文件section
                        fconfig_path:配置文件路径
                    修改记录：
                    @author:
                    @date:
                """
        g_uper_log.debug(f"读取配置:{section}")
        if not os.path.isfile(fconfig_path):
            g_uper_log.debug("配置文件路径不是文件路径")
            return
        # 判断路径文件是否存在
        if not os.path.exists(fconfig_path):
            g_uper_log.debug("配置文件路径不存在")
            return
        # 读取配置文件
        config = configparser.ConfigParser()
        readret = config.read(fconfig_path, encoding="utf-8")
        if (len(readret)) == 0:
            g_uper_log.debug("配置文件为空")
            return
        try:
            # 默认配置
            self.__device_config_support_count = config.getint(section, "device_config_support_count", fallback=0)
            g_uper_log.debug(f"配置支持的设备数量 = {self.device_config_support_count}")

            self.__config_device_name = config.get(section, "config_device_name", fallback='GCAN')
            g_uper_log.debug(f"配置支持的设备名称 = {self.__device_config_device_name}")

        except Exception as e:
            g_uper_log.exception(str(e))

    @property
    def device_config_support_count(self):
        return self.__device_config_support_count

    @property
    def device_configs_dict(self):
        return self.__dict

    @property
    def config_device_name(self):
        return self.__config_device_name


if __name__ == '__main__':
    # 测试所有的配置读取是否正取
    m_config = CAN_Config()
    g_uper_log.debug(m_config)
