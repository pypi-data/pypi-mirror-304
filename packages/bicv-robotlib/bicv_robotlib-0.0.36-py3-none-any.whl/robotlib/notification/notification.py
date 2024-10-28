'''
钉钉群消息通知
更新日志：
============================
V1.0.1
autoTest,caolong
2024/04/26 15.36
============================
'''
import smtplib
from abc import abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
import json

from robotlib.devices.device_manager.base_device import Device
from robotlib.init.init import g_uper_log
from robotlib.notification.notification_config import Notification_Client_Config


class Message_Client(Device):
    """
        类功能描述：提供一个抽象的消息通知类，子类继承此类，实现抽象方法
        函数：
    """
    def __init__(self, client_config: Notification_Client_Config):
        """
            函数功能描述：初始化消息通知
            Param:
                client_config:软件配置
        """
        g_uper_log.debug("消息通知父类初始化")
        # 电源配置
        self.__client_config = client_config

    def __str__(self):
        return str(self.client_config)

    @property
    def client_config(self):
        """
            函数功能描述：获取设置
            Retrun:client_config
        """
        return self.__client_config
    @property
    def client_name(self):
        """
            函数功能描述：获取消息渠道名称
            Retrun:str
        """
        return self.client_config.client_name
    @property
    def url(self):
        """
            函数功能描述：获取消息渠道配置的url
            Retrun:str
        """
        return self.client_config.url
    @property
    def account(self):
        """
            函数功能描述：获取消息渠道配置的账号
            Retrun:str
        """
        return self.client_config.account
    @property
    def password(self):
        """
            函数功能描述：获取消息渠道配置的密码
            Retrun:str
        """
        return self.client_config.password
    @property
    def client_sub_type_enum(self):
        """
            函数功能描述：获取消息渠道的类型
            Retrun:None
        """
        return self.client_config.client_sub_type_enum


    @property
    def device_name(self):
        """
            函数功能描述：获取设备名称
            Retrun:str
        """
        self.client_config.client_name

    @property
    def device_type_enum(self):
        """
            函数功能描述：获取设备类型
            Retrun:DeviceTypeEnum
        """
        pass

    @property
    def device_sub_type_enum(self):
        """
            函数功能描述：获取设备子类型，每种设备的子类型不一样
            Retrun:DeviceCameraSubTypeEnum or
                   DeviceRelaySingleSubTypeEnum or
                   DeviceRelayThreeSideSubTypeEnum or
                   DeviceClickerSubTypeEnum or
                   DevicePowerSubTypeEnum
        """
        return self.client_config.client_sub_type_enum

    @property
    def device_state_enum(self):
        """
            函数功能描述：获取设备状态
            Retrun:DeviceStateEnum
        """
        pass

    @property
    def program_control_type_enum(self):
        """
            函数功能描述：获取设备编程类型
            Retrun:ProgramControlTypeEnum
        """
        pass

    @property
    def device_config(self):
        """
            函数功能描述：获取设备配置，每种设备的配置不一样返回值类型不一样
            Retrun:Power_Device_Config or
                   Relay_Single_Device_Config
        """
        return self.__client_config

    @abstractmethod
    def send_message_with_text(self, text, reminders_account, title='BICV-自动化测试消息'):
        """
            函数功能描述：发送文本消息
            Param:
                text(str):消息文本
                reminders_account:消息接收人-type：钉钉-list(str) 邮箱-str
                title：消息标题
            Retrun:None
        """
        pass
    @abstractmethod
    def send_message_with_image_text(self, image_url, text, reminders_account, title='BICV-自动化测试消息'):
        """
            函数功能描述：发送图片文本消息
            Param:
                image_url(str):图片url
                text(str):消息文本
                reminders_account:消息接收人-type：钉钉-list(str) 邮箱-str
                title：消息标题
            Retrun:None
        """
        pass

class Ding_Talk(Message_Client):

    def __init__(self, client_config: Notification_Client_Config):
        g_uper_log.debug("Ding_Talk初始化")
        # 父类初始化
        Message_Client.__init__(self, client_config)

    def send_message_with_text(self, text, reminders_account: list, title='BICV-自动化测试消息'):
        """
            函数功能描述：发送文本消息
            Param:
                text(str):消息文本
                reminders_account:消息接收人-type：钉钉-list(str) 邮箱-str
                title：消息标题
            Retrun:None
        """
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "msgtype": "text",  # 发送消息类型为文本
            "at": {
                "atMobiles": reminders_account,
                "isAtAll": False,  # 不@所有人
            },
            "text": {
                "content": "ERROR_" + text,  # 消息正文
            }
        }
        r = requests.post(self.url, data=json.dumps(data), headers=headers)
        return r.text

    def send_message_with_image_text(self, image_url, text, reminders_account, title='BICV-自动化测试消息'):
        """
            函数功能描述：发送图片文本消息
            Param:
                image_url(str):图片url
                text(str):消息文本
                reminders_account:消息接收人-type：钉钉-list(str) 邮箱-str
                title：消息标题
            Retrun:None
        """
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "msgtype": "markdown",  # 发送消息类型为文本
            "markdown": {
                "title": "测试",
                "text": "\n> ![screenshot]("+image_url+")"+text+"@"+reminders_account[0]+"  \n>\n"
            },
            "at": {
                "atMobiles":reminders_account,
                "isAtAll": False
            },
            "text": {
                "content": "ERROR_" + text,   # 消息正文
            },

            "picUrl":image_url
        }
        r = requests.post(self.url, data=json.dumps(data), headers=headers)
        return r.text


class E_Mail(Message_Client):

    def __init__(self, client_config: Notification_Client_Config):
        g_uper_log.debug("E_Mail初始化")
        # 父类初始化
        Message_Client.__init__(self, client_config)

    def send_message_with_text(self, text, reminders_account, title='BICV-自动化测试消息'):
        '''
        函数功能描述：发送文字消息
        :param From:发送者
            To:接收者
            password:发送者邮箱密码
            Subject:邮件标题
            body:邮件主体
        '''
        # 创建邮件对象
        message = MIMEMultipart()
        message["From"] = self.account
        message["To"] = reminders_account
        message["Subject"] = title

        # 邮件正文
        message.attach(MIMEText(text, "plain"))

        # 连接到SMTP服务器并发送邮件
        server = None
        try:
            server = smtplib.SMTP_SSL("smtphz.qiye.163.com", 465)  # 使用SSL加密连接
            server.set_debuglevel(1)  # 启用调试输出
            server.login(self.account, self.password)
            server.sendmail(self.account, reminders_account, message.as_string())
            print("邮件发送成功")
        except Exception as e:
            print(f"邮件发送失败: {e}")
        finally:
            if server:
                server.quit()

    def send_message_with_image_text(self, image_url, text, reminders_account, title='BICV-自动化测试消息'):
        """
            函数功能描述：发送图片文本消息，这里不支持，直接调用发送文字消息
            Param:
                image_url(str):图片url
                text(str):消息文本
                reminders_account:消息接收人-type：钉钉-list(str) 邮箱-str
                title：消息标题
            Retrun:None
        """
        self.send_message_with_text(text=text, reminders_account=reminders_account)


