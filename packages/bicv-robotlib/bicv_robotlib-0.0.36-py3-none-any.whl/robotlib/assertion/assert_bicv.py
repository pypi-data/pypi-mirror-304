from abc import abstractmethod

from airtest.core import assertions

from robotlib.assertion.assert_config import Assert_Scheme_Config
from robotlib.can.can_dev import CAN_Device
from robotlib.can.can_dev_factory import CAN_Device_Factory
from robotlib.devices.camera.camera_cv import *
from airtest.core.error import TargetNotFoundError
from airtest.core.settings import Settings as ST
from robotlib.init.init import g_uper_log
class Assert_Bicv():
    def __init__(self, scheme_config: Assert_Scheme_Config):
        """
            函数功能描述：初始化断言
            Param:
                scheme_config:软件配置
        """
        g_uper_log.debug("TTS父类初始化")
        # 电源配置
        self.__scheme_config = scheme_config
    @abstractmethod
    def assert_exists(self, v, msg=""):
        """
            函数功能描述：断言在
        """
        pass
    @abstractmethod
    def assert_not_exists(self, v, msg=""):
        """
            函数功能描述：断言不在
        """
        pass

    def assert_signal_status(self, message: str):
        """
        断言某个信号是否和预期一致
        """
        pass

    def assert_can_bus_exist_signal(self, id: str, sig: str, value: str):
        """
        断言某个帧ID中信号值
        """
        pass

    def assert_can_bus_exist_id(self, id: str):
        """
        断言总线上是否存在帧ID
        """
        pass


    def assert_greater(self, actual_value, expected_value, msg="", snapshot=True):  # noqa
        """
        值断言  大于
        actual_value：实际值
        expected_value：预期值
        """
        pass

    def assert_less(self, actual_value, expected_value, msg="", snapshot=True):  # noqa
        """
        值断言  小于
        actual_value：实际值
        expected_value：预期值
        """
        pass

    def assert_equal(self, first, second, msg="", snapshot=True):  # noqa
        """
        值断言  等于
        actual_value：实际值
        expected_value：预期值
        """
        pass

class Camera_Assertion(Assert_Bicv):
    def __init__(self, scheme_Config: Assert_Scheme_Config):
        """
            函数功能描述：初始化相机断言
            Param:
                scheme_Config:设备配置信息
        """
        g_uper_log.debug("初始化断言设备")
        # 父类初始化
        Assert_Bicv.__init__(self, scheme_Config)
    def assert_exists(self, v, msg=""):
        """
            函数功能描述：断言在
        """
        try:
            pos = loop_find_camera(v, timeout=ST.FIND_TIMEOUT, threshold=ST.THRESHOLD_STRICT or v.threshold)
            return pos
        except TargetNotFoundError:
            raise AssertionError("%s does not exist in screen, message: %s" % (v, msg))
    def assert_not_exists(self, v, msg=""):
        """
            函数功能描述：断言不在
        """
        try:
            pos = loop_find_camera(v, timeout=ST.FIND_TIMEOUT_TMP)
            raise AssertionError("%s exists unexpectedly at pos: %s, message: %s" % (v, pos, msg))
        except TargetNotFoundError:
            pass

class Image_Assertion(Assert_Bicv):
    def __init__(self, scheme_Config: Assert_Scheme_Config):
        """
            函数功能描述：初始化图片断言
            Param:
                scheme_Config:设备配置信息
        """
        g_uper_log.debug("初始化断言设备")
        # 父类初始化
        Assert_Bicv.__init__(self, scheme_Config)
    def assert_exists(self, v, msg=""):
        """
            函数功能描述：断言在
        """
        try:
            pos = loop_find_image(v, timeout=ST.FIND_TIMEOUT, threshold=ST.THRESHOLD_STRICT or v.threshold)
            return pos
        except TargetNotFoundError:
            raise AssertionError("%s does not exist in screen, message: %s" % (v, msg))
    def assert_not_exists(self, v, msg=""):
        """
            函数功能描述：断言不在
        """
        try:
            pos = loop_find_image(v, timeout=ST.FIND_TIMEOUT_TMP)
            raise AssertionError("%s exists unexpectedly at pos: %s, message: %s" % (v, pos, msg))
        except TargetNotFoundError:
            pass


class Value_Assertion(Assert_Bicv):
    def __init__(self, scheme_Config: Assert_Scheme_Config):
        """
            函数功能描述：初始化值断言
            Param:
                scheme_Config:设备配置信息
        """
        g_uper_log.debug("初始化断言设备")
        # 父类初始化
        Assert_Bicv.__init__(self, scheme_Config)

    def assert_greater(self, actual_value, expected_value, msg="", snapshot=True):  # noqa
        """
        值断言  大于
        actual_value：实际值
        expected_value：预期值
        """
        assertions.assert_greater(actual_value, expected_value)

    def assert_less(self, actual_value, expected_value, msg="", snapshot=True):  # noqa
        """
        值断言  小于
        actual_value：实际值
        expected_value：预期值
        """
        assertions.assert_less(actual_value, expected_value)

    def assert_equal(self, actual_value, expected_value, msg="", snapshot=True):  # noqa
        """
        值断言  等于
        actual_value：实际值
        expected_value：预期值
        """
        assertions.assert_equal(actual_value, expected_value)

class Can_Assertion(Assert_Bicv):
    
    def __init__(self, scheme_Config: Assert_Scheme_Config):
        """
            函数功能描述：初始化值断言
            Param:
                scheme_Config:设备配置信息
        """
        g_uper_log.debug("初始化断言设备")
        # 父类初始化
        Assert_Bicv.__init__(self, scheme_Config)

    def assert_signal_status(self, message: str):
        """
        断言某个信号是否和预期一致
        """
        can_d: CAN_Device = CAN_Device_Factory.get_device_instance()
        can_d.check_test_signal_status(test_term=message)

    def assert_can_bus_exist_signal(self, id: str, sig: str, value: str):
        """
        断言某个帧ID中信号值
        """
        can_d: CAN_Device = CAN_Device_Factory.get_device_instance()
        can_d.check_can_bus_exist_signal(id=int(id), sig_name=sig, val=value)

    def assert_can_bus_exist_id(self, id: str):
        """
        断言总线上是否存在帧ID
        """
        can_d: CAN_Device = CAN_Device_Factory.get_device_instance()
        can_d.check_can_bus_exist_id(id=int(id))