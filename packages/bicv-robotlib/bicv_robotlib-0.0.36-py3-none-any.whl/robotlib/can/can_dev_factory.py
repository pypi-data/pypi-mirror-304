import time
from threading import RLock
from robotlib.devices.base.modbus.modbus_factory import Modbus_Factory
from robotlib.devices.device_manager.device_type_define import DeviceMultimeterSubTypeEnum
from robotlib.devices.multiple_io.multiple_io import *
from robotlib.devices.multiple_io.multiple_io_config import *
from robotlib.can.can_dev_config import *
from robotlib.can.can_dev import *
from robotlib.init.init import g_uper_log
from canlib.can_server import *
from canlib.test_terms.CarConfig import *


class CAN_Device_Factory:
    """
        类功能描述：CAN设备工厂
                  动态添加两个类属性,动态添加方式不能改变：
                    __device_instance_dict
                    __device_configs
        类函数:
            get_device_instance:
            get_device_configs:
    """
    __single_device_lock = RLock()
    __single_configs_lock = RLock()
    __support_device_name_list = ["can"]

    @classmethod
    def get_device_instance(cls):
        """
            函数功能描述：获取can盒对象
            Return:
        """
        with cls.__single_device_lock:
            if "_" + cls.__name__ + "__device_instance_dict" not in dir(CAN_Device_Factory):
                g_uper_log.info("配置和创建cand对象-开始####")
                CAN_dev_config = cls.get_device_configs()
                g_uper_log.debug(f"当前配置支持的设备数量：{len(CAN_dev_config.device_configs_dict)}")
                g_uper_log.debug(f"设备名称：{CAN_dev_config.device_configs_dict.items()}")
                cls.__device_instance_dict = dict()
                # 此处没有考虑数目为0的情况
                for key, value in CAN_dev_config.device_configs_dict.items():
                    g_uper_log.info(f"创建功放断言对象{key}：{value}")
                    # 多态创建
                    if value.device_name == CAN_dev_config.config_device_name:
                        if value.device_sub_type_enum == DeviceCANEnum.GCAN:
                            can_device_new: CAN_Device = GCAN(value)
                            cls.__device_instance_dict[key] = can_device_new

                        elif value.device_sub_type_enum == DeviceCANEnum.TOMOS:
                            can_device_new: CAN_Device = TomosCAN(value)
                            cls.__device_instance_dict[key] = can_device_new

                        else:
                            pass
                        break
                    else:
                        continue

                g_uper_log.info(cls.__device_instance_dict)

            return cls.__device_instance_dict.get(cls.get_device_configs().config_device_name)

    @classmethod
    def get_device_configs(cls):
        """
            函数功能描述：获取设备配置配置
            Retrun:配置
        """
        with cls.__single_configs_lock:
            # 判断__device_configs属性是否存在，不存在说明万用表配置还没有创建，需要创建此配置
            if "_" + cls.__name__ + "__device_configs" not in dir(CAN_Device_Factory):
                g_uper_log.info("创建配置对象####")
                cls.__device_configs = CAN_Config()
                g_uper_log.info("创建配置对象-结束####")
        return cls.__device_configs


if __name__ == '__main__':
    # 测试所有的配置读取是否正取
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    # endregion
    can_d: CAN_Device = CAN_Device_Factory.get_device_instance()

    # can_d.change_signal_from_vehicle_2_mmi(message='PEPSPowerMode.ON')
    #
    # can_d.change_signal_from_vehicle_2_mmi_by_id(0x2fc, [{'name': "PEPS_PowerMode", "val": 2}])
    # can_d.change_signal_from_vehicle_2_mmi_by_id(0x2fc, [{'name': "PEPS_PowerModeValidity", "val": 2}])

    can_d.send_frame_data_from_vehicle_2_mmi('0x2fc', '0x33 0x2 0x3 0x4 0x4 0x6 0x7 0x44')

    sys.exit(app.exec_())
