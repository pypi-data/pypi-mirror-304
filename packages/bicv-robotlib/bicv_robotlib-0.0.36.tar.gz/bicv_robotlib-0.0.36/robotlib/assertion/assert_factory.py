from threading import RLock

from airtest.core.cv import Template

from robotlib.devices.device_manager.device_type_define import AssertSubTypeEnum
from robotlib.init.init import g_uper_log
from robotlib.assertion.assert_config import Assert_Config
from robotlib.assertion.assert_bicv import Assert_Bicv, Camera_Assertion, Can_Assertion, Image_Assertion, \
    Value_Assertion


class Assert_Factory:

    """
        类功能描述：断言工厂，提供camera/value/can断言对象
                  动态添加两个类属性,动态添加方式不能改变：
                    __assert_instance_dict
                    __assert_configs
        类函数:
            get_assert_instance:提供断言对象
            get_assert_configs:提供断言配置对象
    """

    __single_device_lock = RLock()
    __single_configs_lock = RLock()

    __support_device_name_list = ["CAMERA", "CAN"]

    @classmethod
    def get_assert_instance(cls, type_name: str) -> Assert_Bicv:
        """
            函数功能描述：获取断言对象
            Return:
                Assert_Bicv 断言抽象基类
        """
        with cls.__single_device_lock:
            if "_" + cls.__name__ + "__assert_instance_dict" not in dir(Assert_Factory):
                g_uper_log.info("配置和创建断言模块-开始####")
                assert_config = cls.get_assert_configs()
                g_uper_log.debug(f"当前配置支持的断言数量：{len(assert_config.scheme_configs_dict)}")
                g_uper_log.debug(f"断言名称：{assert_config.scheme_configs_dict.keys()}")
                cls.__assert_instance_dict = dict()
                # 此处没有考虑数目为0的情况
                for key, value in assert_config.scheme_configs_dict.items():
                    g_uper_log.debug(f"创建断言对象{key}：{value}")
                    # 判断断言类型
                    if value.scheme_sub_type_enum == AssertSubTypeEnum.CAMERA:
                        cls.__assert_instance_dict[key] = Camera_Assertion(value)
                    elif value.scheme_sub_type_enum == AssertSubTypeEnum.CAN:
                        cls.__assert_instance_dict[key] = Can_Assertion(value)
                    elif value.scheme_sub_type_enum == AssertSubTypeEnum.VALUE:
                        cls.__assert_instance_dict[key] = Value_Assertion(value)
                    elif value.scheme_sub_type_enum == AssertSubTypeEnum.IMAGE:
                        cls.__assert_instance_dict[key] = Image_Assertion(value)
                    else:
                        g_uper_log.error("断言未知类型")
                g_uper_log.info(cls.__assert_instance_dict)
                g_uper_log.info("配置和创建断言模块-结束####")

        return cls.__assert_instance_dict.get(type_name)

    @classmethod
    def get_assert_configs(cls):
        """
            函数功能描述：获取所有断言方案配置
            Retrun:Assert_Scheme_Config
        """
        with cls.__single_configs_lock:
            # 判断__device_configs属性是否存在，不存在说明单口继电器配置还没有创建，需要创建此配置
            if "_"+cls.__name__+"__assert_configs" not in dir(Assert_Factory):
                g_uper_log.info("创建断言配置对象")
                cls.__assert_configs = Assert_Config()
        return cls.__assert_configs

if __name__ == '__main__':
    scheme = Assert_Factory.get_assert_instance('CAMERA')
    print(f'scheme -> {scheme}')
    result = scheme.assert_exists(Template(r"tpl1729578272916.png"))
    print(f'result -> {result}')