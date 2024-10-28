from multiprocessing import RLock
from robotlib.devices.device_manager.device_type_define import TtsSubTypeEnum
from robotlib.init.init import g_uper_log
from robotlib.tts.tts import Tts_Scheme_Windows
from robotlib.tts.tts_config import Tts_Config


class TtsFactory:
    '''
    发送消息管理
    '''

    __single_client_lock = RLock()
    __single_configs_lock = RLock()
    __support_scheme_name_list = ["WINDOWS"]

    @classmethod
    def get_scheme(cls, client_name: str):
        """
            函数功能描述：获取电源对象
            Return:
                PowerDevice 电源抽象基类
        """
        with cls.__single_client_lock:
            if "_" + cls.__name__ + "__scheme_instance_dict" not in dir(TtsFactory):
                g_uper_log.info("配置和创建TTS模块-开始####")
                tts_config = cls.get_notification_configs()
                g_uper_log.debug(f"当前配置支持的TTS方案数量：{tts_config.scheme_config_support_count}")
                g_uper_log.debug(f"TTS方案名称：{tts_config.scheme_configs_dict.keys()}")
                cls.__scheme_instance_dict = dict()
                # 此处没有考虑数目为0的情况
                for key, value in tts_config.scheme_configs_dict.items():
                    g_uper_log.debug(f"创建TTS对象 key -> {key}：value -> {value}")
                    # 判断单口继电器类型
                    if value.scheme_sub_type_enum == TtsSubTypeEnum.WINDOWS:
                        scheme1 = Tts_Scheme_Windows(value)
                        g_uper_log.debug(f"创建完成--")
                        g_uper_log.debug(scheme1)
                        cls.__scheme_instance_dict[key] = scheme1
                    else:
                        g_uper_log.error("TTS未知类型")
                g_uper_log.info(cls.__scheme_instance_dict)
                g_uper_log.info("配置和创建TTS模块-结束 ####")

        return cls.__scheme_instance_dict.get(client_name)


    @classmethod
    def get_notification_configs(cls):
        """
            函数功能描述：获取所有通知设备配置
            Retrun:Power_Config
        """
        with cls.__single_configs_lock:
            # 判断__scheme_configs属性是否存在，不存在说明电源配置还没有创建，需要创建此配置
            if "_" + cls.__name__ + "__scheme_configs" not in dir(TtsFactory):
                g_uper_log.info("创建通知配置对象####")
                cls.__scheme_configs = Tts_Config()
                g_uper_log.info("创建通知配置对象-结束 ####")
        return cls.__scheme_configs


if __name__ == '__main__':
    manage = TtsFactory.get_scheme('WINDOWS')
    print(f'manage -> {manage}')
    list = manage.get_voice_package_list()
    print(f'list -> {list}')
    manage.speak_with_voice_package('按时间拉萨的干活了凯撒帝国海军考试大纲', 'Microsoft Huihui Desktop - Chinese (Simplified)')
