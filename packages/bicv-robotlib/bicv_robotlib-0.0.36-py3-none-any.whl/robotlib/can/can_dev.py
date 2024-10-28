"""
    模块功能说明：CAN 模块
    基类：CAN_Device
    派生类：
         GCAN
    派生类:
        TomosCAN

"""

import time
from abc import abstractmethod
import serial
import serial.tools.list_ports
from pymodbus.pdu import ModbusResponse
from robotlib.devices.base.modbus.modbus import Modbus_Device
from robotlib.devices.base.serial_base import Serail_Base
from robotlib.devices.device_manager.base_device import Device
from robotlib.devices.device_manager.device_type_define import DeviceStateEnum
from robotlib.can.can_dev_config import *
from robotlib.can.can_dev_config import *
from robotlib.init.init import g_uper_log
from canlib.test_terms.CarConfig import *
from canlib.can_server import *
import robotlib.init.init
import canlib


class CAN_Device(Device):
    """
        类功能描述：设备基类
        抽象函数：
    """

    def __init__(self, can_dev_config: CAN_Device_Config):
        """
            函数功能描述：初始化设备
            Param:
        """
        g_uper_log.debug("父类初始化")

        # 万用表设备配置
        self.__can_device_config = can_dev_config
        self._can_server_oem: CanServer = None

    def __str__(self):
        return Device.__str__(self) + "\n" + str(self.device_config)

    @property
    def device_config(self):
        return self.__can_device_config

    @property
    def device_name(self):
        return self.device_config.device_name

    @property
    def device_type_enum(self):
        return self.device_config.device_type_enum

    @property
    def device_sub_type_enum(self):
        return self.device_config.device_sub_type_enum

    @property
    def device_state_enum(self):
        return self.device_config.device_state_enum

    @property
    def program_control_type_enum(self):
        return self.device_config.program_control_type_enum

    @property
    def program_can_server_obj(self):
        return self._can_server_oem

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def change_signal_from_vehicle_2_mmi(self, message: str):
        """
             改变某一个信号值
             canlib 传参是信号枚举，用户很难通过UI直接下发枚举，所以用字符串
             # self.can_sever_demo.run_test_term(test_term=PEPSPowerMode.ON)  直接传信号枚举
             # self.can_sever_demo.run_test_term(test_term=eval('PEPSPowerMode.ON'))  # 直接传信号枚举
             message: 信号枚举 字符串形式
             return:None
             """
        pass
        # self._can_server_oem.change_signal_from_car(test_term=eval(message))

    @abstractmethod
    def change_signal_from_vehicle_2_mmi_by_id(self, id, sig_list):
        """
        根据id，信号信息修改信号值
        id: 帧id
        sig_list:信号列表
        return:None
        """
        pass
        # self._can_server_oem.change_sig_from_car_by_id(id, sig_list)

    @abstractmethod
    def send_frame_data_from_vehicle_2_mmi(self, id: str, data: str):
        """
             发送一帧用户输入的数据
             id: 帧id
             data:报文
             return:None
             """
        pass
        # _cmd_byte = bytes.fromhex(data)
        # self._can_server_oem.change_sig_from_car_by_id_data(id=int(id), data=_cmd_byte)

    @abstractmethod
    def check_test_signal_status(self, message: str):
        """
        读取测试目标信号结果是否和要求一致
        message: 信号枚举 字符串形式
        return :Bool
        """
        pass
        # return self._can_server_oem.read_test_sig_status(test_term=eval(message))

    @abstractmethod
    def check_can_bus_exist_signal(self, id: str, sig: str, value: str):
        """
        读取总线上是否存在某个信号和值
        id: 帧id
        sog:信号
        value:信号值
        return : Bool
        """
        pass
        # return self._can_server_oem.read_has_receive_can_sig(id=int(id), sig_name=sig, val=value)

    @abstractmethod
    def check_can_bus_exist_id(self, id: str):
        """
        读取总线上是否存在某个帧ID
        id: 帧ID
        return : Bool
        """
        pass
        # return self._can_server_oem.read_has_receive_can_id(id=int(id))


class GCAN(CAN_Device):
    """
    gcan 初始化的设备
    """

    def __init__(self, can_device_config: CAN_Device_Config):
        """
            函数功能描述：初始化设备
            Param:
        """

        if can_device_config.device_can_aisle == 1:

            can_aisle = gcan_enum.Cannel.通道1
        elif can_device_config.device_can_aisle == 2:
            can_aisle = gcan_enum.Cannel.通道2
        else:
            can_aisle = gcan_enum.Cannel.通道1
        # 父类初始化
        can_device_config_data = {
            "device": CanDeviceType.广成can盒,
            "cancel": can_aisle,
            "baudrate": toomos_enum.BouBaudrate.kbs_500,
            "frame_type": toomos_enum.FrameType.can,
        }
        try:
            path = g_commonpath.upercompter_run_dir
            self._can_server_oem = canlib.get_can_server(path, can_device_config_data)
            self._can_server_oem.start_can()
        except Exception as e:
            self._can_server_oem = None

    @property
    def device_state_enum(self):
        """
                CAN 盒缺少在线离线状态返回，默认为未知
        """
        bexist = self.__device_exist()
        # temp_device_state_eunm = self.device_config.device_state_enum
        # if bexist:
        #     temp_device_state_eunm = DeviceStateEnum.ON
        # else:
        #     temp_device_state_eunm = DeviceStateEnum.OFF
        return DeviceStateEnum.NONE

    def __device_exist(self):
        """
            函数功能描述：判断设备是否存在，此设备为modbus中的一个从设备，需要和从设备通讯还能知道设备是否存在
        """
        if self._can_server_oem:

            return True
        else:
            return False

    def start(self):
        self._can_server_oem.start_can()

    def stop(self):
        self._can_server_oem.stop_can()

    def change_signal_from_vehicle_2_mmi(self, message: str):
        """
             改变某一个信号值
             canlib 传参是信号枚举，用户很难通过UI直接下发枚举，所以用字符串
             # self.can_sever_demo.run_test_term(test_term=PEPSPowerMode.ON)  直接传信号枚举
             # self.can_sever_demo.run_test_term(test_term=eval('PEPSPowerMode.ON'))  # 直接传信号枚举
             message: 信号枚举 字符串形式
             return:None
             """
        self._can_server_oem.change_signal_from_car(test_term=eval(message))

    def change_signal_from_vehicle_2_mmi_by_id(self, id, sig_list):
        """
        根据id，信号信息修改信号值
        id: 帧id
        sig_list:信号列表 信号列表[{“name”:"信号名"，"val“:"信号值"}]
        return:None
        """
        self._can_server_oem.change_sig_from_car_by_id(id, sig_list)

    def send_frame_data_from_vehicle_2_mmi(self, id: str, data: str):
        """
         发送一帧用户输入的数据
         id: 帧id
         data:报文
         return:None
        """
        hex_list = data.split()
        _cmd_byte = [int(h, 16) for h in hex_list]
        self._can_server_oem.change_sig_from_car_by_id_data(id=int(id, 16), data=_cmd_byte)

    def check_test_signal_status(self, message: str):
        """
        读取测试目标信号结果是否和要求一致
        message: 信号枚举 字符串形式
        return :Bool
        """
        return self._can_server_oem.read_test_sig_status(test_term=eval(message))

    def check_can_bus_exist_signal(self, id: str, sig: str, value: str):
        """
        读取总线上是否存在某个信号和值
        id: 帧id
        sog:信号
        value:信号值
        return : Bool
        """
        return self._can_server_oem.read_has_receive_can_sig(id=int(id, 16), sig_name=sig, val=int(id, 16))

    def check_can_bus_exist_id(self, id: str):
        """
        读取总线上是否存在某个帧ID
        id: 帧ID
        return : Bool
        """
        return self._can_server_oem.read_has_receive_can_id(id=int(id, 16))


class TomosCAN(CAN_Device):
    """
    Tomos。初始化的设备
    """

    def __init__(self, can_device_config: CAN_Device_Config):
        """
            函数功能描述：初始化设备
            Param:
        """
        # 父类初始化
        if can_device_config.device_can_aisle == 1:
            can_aisle = toomos_enum.Cannel.通道1
        elif can_device_config.device_can_aisle == 2:
            can_aisle = toomos_enum.Cannel.通道2
        else:
            can_aisle = toomos_enum.Cannel.通道1

        can_device_config_data = {
            "device": CanDeviceType.图模斯can盒,
            "cancel": can_aisle,
            "baudrate": toomos_enum.BouBaudrate.kbs_500,
            "frame_type": toomos_enum.FrameType.can,
        }
        path = g_commonpath.upercompter_run_dir
        try:
            self._can_server_oem = canlib.get_can_server(path, can_device_config_data)
            self._can_server_oem.start_can()
        except Exception as e:
            self._can_server_oem = None

    @property
    def device_state_enum(self):
        """
        CAN 盒缺少在线离线状态返回，默认为未知
        """
        bexist = self.__device_exist()
        # temp_device_state_eunm = self.device_config.device_state_enum
        # if bexist:
        #     temp_device_state_eunm = DeviceStateEnum.ON
        # else:
        #     temp_device_state_eunm = DeviceStateEnum.OFF
        return DeviceStateEnum.NONE

    def __device_exist(self):
        """
            函数功能描述：判断设备是否存在，此设备为modbus中的一个从设备，需要和从设备通讯还能知道设备是否存在
        """
        if self._can_server_oem:
            return True
        else:
            return False

    def start(self):
        self._can_server_oem.start_can()

    def stop(self):
        self._can_server_oem.stop_can()

    def change_signal_from_vehicle_2_mmi(self, message: str):
        """
             改变某一个信号值
             canlib 传参是信号枚举，用户很难通过UI直接下发枚举，所以用字符串
             # self.can_sever_demo.run_test_term(test_term=PEPSPowerMode.ON)  直接传信号枚举
             # self.can_sever_demo.run_test_term(test_term=eval('PEPSPowerMode.ON'))  # 直接传信号枚举
             message: 信号枚举 字符串形式
             return:None
             """
        self._can_server_oem.change_signal_from_car(test_term=eval(message))

    def change_signal_from_vehicle_2_mmi_by_id(self, id, sig_list):
        """
        根据id，信号信息修改信号值
        id: 帧id
        sig_list:信号列表
        return:None
        """
        self._can_server_oem.change_sig_from_car_by_id(id, sig_list)

    def send_frame_data_from_vehicle_2_mmi(self, id: str, data: str):
        """
             发送一帧用户输入的数据
             id: 帧id
             data:报文
             return:None
             """
        hex_list = data.split()
        _cmd_byte = [int(h, 16) for h in hex_list]
        self._can_server_oem.change_sig_from_car_by_id_data(id=int(id, 16), data=_cmd_byte)

    def check_test_signal_status(self, message: str):
        """
        读取测试目标信号结果是否和要求一致
        message: 信号枚举 字符串形式
        return :Bool
        """
        return self._can_server_oem.read_test_sig_status(test_term=eval(message))

    def check_can_bus_exist_signal(self, id: str, sig: str, value: str):
        """
        读取总线上是否存在某个信号和值
        id: 帧id
        sog:信号
        value:信号值
        return : Bool
        """
        return self._can_server_oem.read_has_receive_can_sig(id=int(id, 16), sig_name=sig, val=value)

    def check_can_bus_exist_id(self, id: str):
        """
        读取总线上是否存在某个帧ID
        id: 帧ID
        return : Bool
        """
        return self._can_server_oem.read_has_receive_can_id(id=int(id, 16))
