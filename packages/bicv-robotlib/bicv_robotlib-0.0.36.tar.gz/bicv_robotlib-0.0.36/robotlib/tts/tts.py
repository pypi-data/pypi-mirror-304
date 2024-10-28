from abc import abstractmethod
import time
from os import remove, listdir
from tempfile import gettempdir

import pygame
import pyttsx3

from robotlib.devices.device_manager.base_device import Device
from robotlib.init.init import g_uper_log
from robotlib.tts.tts_config import Tts_Scheme_Config


class Tts_Scheme(Device):
    """
        类功能描述：提供一个抽象的TTS类，子类继承此类，实现抽象方法
        函数：
    """

    def __init__(self, scheme_config: Tts_Scheme_Config):
        """
            函数功能描述：初始化TTS
            Param:
                scheme_config:软件配置
        """
        g_uper_log.debug("TTS父类初始化")
        # 电源配置
        self.__scheme_config = scheme_config

    def __str__(self):
        return str(self.scheme_config)

    @property
    def scheme_config(self):
        """
            函数功能描述：获取TTS方案的软件具体设置
            Return: scheme_config
        """
        return self.__scheme_config

    @property
    def scheme_name(self):
        """
            函数功能描述：获取TTS方案的名称
            Return: str
        """
        return self.scheme_config.scheme_name

    @property
    def cache_path(self):
        """
            函数功能描述：获取TTS方案的缓存路径，用来存放mp3文件
            Return: str
        """
        return self.scheme_config.cache_path

    @property
    def scheme_sub_type_enum(self):
        """
            函数功能描述：获取TTS方案的类型
            Return:
        """
        return self.scheme_config.scheme_sub_type_enum

    @property
    def device_name(self):
        """
            函数功能描述：获取方案名称
            Retrun:str
        """
        return self.scheme_config.scheme_name

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
        return self.scheme_config.scheme_sub_type_enum

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
            函数功能描述：获取方案的具体设置
        """
        return self.__scheme_config

    """获取支持的语言表"""

    @abstractmethod
    def get_voice_package_list(self):
        pass

    """播放"""

    @abstractmethod
    def speak_with_voice_package(self, text, voice_name):
        pass

    """生成MP3文件"""

    @abstractmethod
    def make_file(self, text, voice_name, is_temp=False):
        pass


class Tts_Scheme_Windows(Tts_Scheme):
    """
        类功能描述：TTS——Windows方案
    """

    def __init__(self, relay_single_device_config: Tts_Scheme_Config):
        """
            函数功能描述：初始化单口继电器设备
            Param:
                Relay_Single_Device_Config:设备配置信息
        """
        g_uper_log.debug("初始化单口继电器设备")
        # 父类初始化
        Tts_Scheme.__init__(self, relay_single_device_config)
        self.voices_data = dict()  # {voice.name: voice.id}
        self.engine = pyttsx3.init()  # 初始化模块
        self.temp_file_list = []
        try:
            voices = self.engine.getProperty('voices')
            for voice in voices:
                key = voice.name
                self.voices_data[key] = voice.id
        except Exception as e:
            g_uper_log.error(f"Tts_Scheme_Windows 初始化错误 获取语音包失败 e -> {e}")

        try:
            pygame.init()
            pygame.mixer.init()
        except Exception as e:
            g_uper_log.error(
                f"*************************这里报错的原因是因为电脑没有扬声器或者没有耳机************************* \n e -> {e}")
        g_uper_log.info(f"Tts_Scheme_Windows __init__ self.voices_data -> {self.voices_data}")

    def get_voice_package_list(self):
        return self.voices_data.keys()


    """播放"""
    def speak_with_voice_package(self, text, voice_name):
        is_voice_can_use = self.is_voice_can_use(voice_name)
        g_uper_log.info(f"Tts_Scheme_Windows speak_with_voice_package is_voice_can_use -> {is_voice_can_use}")
        """使用windows的语音包发音"""
        if not is_voice_can_use:
            return False

        """试听"""
        # 设置语音，语速，声音大小
        self.engine.setProperty("voice", self.voices_data.get(voice_name))
        # self.engine.setProperty("rate", new_rate)
        # self.engine.setProperty("volume", new_volume / 100)

        # 保存文件
        file_name = self.make_file(text=text, voice_name=voice_name, is_temp=True)
        print(f'file_name -> {file_name}')
        result = False
        # 开始播放
        try:
            pygame.mixer.music.load(file_name)
            pygame.mixer.music.play(loops=1)
            print('播放成功')
            return True
        except pygame.error:
            g_uper_log.error("播放错误 该语音包无法播放此内容 请更换语音包后重试！")
            return False
        finally:
            # 阻塞程序
            # 监听事件
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.mixer.music.stop()  # 停止音乐播放

        self.__remove_temp()
        # self.clean_last_file()


    """生成MP3文件"""
    def make_file(self, text, voice_name, is_temp=False):
        is_voice_can_use = self.is_voice_can_use(voice_name)
        g_uper_log.info(f"Tts_Scheme_Windows make_file is_voice_can_use -> {is_voice_can_use}")
        if not is_voice_can_use:
            return
        """生成音频文件"""
        # 获取本地时间作为文件名
        file = time.strftime("%Y%m%d%H%M%S", time.localtime())
        g_uper_log.info(f"Tts_Scheme_Windows make_file file -> {file}")

        # 如果是临时缓存的文件，则创建wma文件
        if is_temp:
            file_name = "{0}\\T{1}.wma".format(self.scheme_config.cache_path if not self.scheme_config.cache_path and self.scheme_config.cache_path.__len__() > 0 else gettempdir(), file)
            self.engine.save_to_file(text, file_name)
            self.engine.runAndWait()

            return file_name

        # 非临时文件
        self.engine.setProperty("voice", self.voices_data.get(voice_name))
        # self.engine.setProperty("rate", rate)
        # self.engine.setProperty("volume", volume/100)
        file_name = (self.scheme_config.cache_path if self.scheme_config.cache_path else gettempdir()) + file + ".mp3"
        g_uper_log.info(f"Tts_Scheme_Windows make_file file_name -> {file_name} cache_path -> {self.scheme_config.cache_path}")
        self.engine.save_to_file(text, file_name)
        self.engine.runAndWait()

    def __remove_temp(self):
        """删除临时文件"""
        for fl in self.temp_file_list:
            try:
                remove(fl)
            except PermissionError:
                continue

    def clean_last_file(self):
        """清理上一次缓存的文件"""
        for fn in listdir(gettempdir()):
            if len(fn.split(".")) == 2 and fn.split(".")[1] == "wma":
                remove(gettempdir() + "\\" + fn)

    def is_voice_can_use(self, voice_name):
        is_voice_contains = self.voices_data.__contains__(voice_name)
        g_uper_log.info(f"is_voice_can_use -> {is_voice_contains}")
        return is_voice_contains
