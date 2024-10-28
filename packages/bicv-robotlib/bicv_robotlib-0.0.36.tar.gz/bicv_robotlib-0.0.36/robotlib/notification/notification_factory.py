from threading import RLock
from robotlib.devices.device_manager.device_type_define import NotificationSubTypeEnum
from robotlib.init.init import g_uper_log
from robotlib.notification.notification import E_Mail, Ding_Talk
from robotlib.notification.notification_config import Notification_Config

class NotificationFactory:
    '''
    发送消息管理
    '''

    __single_client_lock = RLock()
    __single_configs_lock = RLock()
    __support_client_name_list = ["dingding", "email"]

    @classmethod
    def get_client(cls, client_name: str):
        """
            函数功能描述：获取电源对象
            Return:
                PowerDevice 电源抽象基类
        """
        with cls.__single_client_lock:
            if "_" + cls.__name__ + "__client_instance_dict" not in dir(NotificationFactory):
                g_uper_log.info("配置和创建通知模块-开始####")
                notification_config = cls.get_notification_configs()
                g_uper_log.debug(f"当前配置支持的通知客户端数量：{notification_config.client_config_support_count}")
                g_uper_log.debug(f"设备名称：{notification_config.client_configs_dict.keys()}")
                cls.__client_instance_dict = dict()
                # 此处没有考虑数目为0的情况
                for key, value in notification_config.client_configs_dict.items():
                    g_uper_log.debug(f"创建通知对象 key -> {key}：value -> {value}")
                    print(f'value.client_sub_type_enum -> {value.client_sub_type_enum} NotificationSubTypeEnum.DING_TALK -> {type(NotificationSubTypeEnum.DING_TALK)} {NotificationSubTypeEnum.E_MAIL}')
                    # 判断单口继电器类型
                    if value.client_sub_type_enum == NotificationSubTypeEnum.DING_TALK:
                        client1 = Ding_Talk(value)
                        g_uper_log.debug(f"创建完成--")
                        g_uper_log.debug(client1)
                        cls.__client_instance_dict[key] = client1
                    elif value.client_sub_type_enum == NotificationSubTypeEnum.E_MAIL:
                        client2 = E_Mail(value)
                        g_uper_log.debug(client2)
                        cls.__client_instance_dict[key] = client2
                    else:
                        g_uper_log.error("通知未知类型")
                g_uper_log.info(cls.__client_instance_dict)
                g_uper_log.info("配置和创建通知模块-结束 ####")

        return cls.__client_instance_dict.get(client_name)


    @classmethod
    def get_notification_configs(cls):
        """
            函数功能描述：获取所有电源设备配置
            Retrun:Power_Config
        """
        with cls.__single_configs_lock:
            # 判断__device_configs属性是否存在，不存在说明电源配置还没有创建，需要创建此配置
            if "_" + cls.__name__ + "__device_configs" not in dir(NotificationFactory):
                g_uper_log.info("创建通知配置对象####")
                cls.__device_configs = Notification_Config()
                g_uper_log.info("创建通知配置对象-结束 ####")
        return cls.__device_configs


if __name__ == '__main__':
    manage = NotificationFactory.get_client('email')
    print(f'manage -> {manage}')
    result = manage.send_message_with_text('调试ssss', '810420211@qq.com')
    print(f'result -> {result}')
