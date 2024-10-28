# -*- coding: utf-8 -*-
from robotlib.graphic.recognize.utils.resolution import cocos_min_strategy
import os
import cv2
from distutils.version import LooseVersion


class Settings(object):

    DEBUG = False
    LOG_DIR = None
    LOG_FILE = "log.txt"
    LOG_TAG = "graphic"
    RESIZE_METHOD = staticmethod(cocos_min_strategy)

    # 图像识别 ---start
    # 配置图像查找方法
    # keypoint matching: kaze/brisk/akaze/orb, contrib: sift/surf/brief
    CVSTRATEGY = ["mstpl", "tpl", "sift", "brisk"]
    # 根据不同版本号来配置使用图片查找的不同的方法
    if LooseVersion('3.4.2') < LooseVersion(cv2.__version__) < LooseVersion('4.4.0'):
        CVSTRATEGY = ["mstpl", "tpl", "brisk"]
    KEYPOINT_MATCHING_PREDICTION = True
    # 图像识别阈值,值越大表示匹配度要求越高反之越小
    THRESHOLD = 0.7  # [0, 1]
    THRESHOLD_STRICT = None  # dedicated parameter for assert_exists
    OPDELAY = 0.1
    # 图像识别中查找相似的超时时间,单位是秒
    FIND_TIMEOUT = 20
    # 这个暂时没有地方使用
    FIND_TIMEOUT_TMP = 3
    # 图像识别 ---end


    PROJECT_ROOT = os.environ.get("PROJECT_ROOT", "")  # for ``using`` other script
    # 抓图质量
    SNAPSHOT_QUALITY: int = 10  # 1-100 https://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html#jpeg
    # Image compression size, e.g. 1200, means that the size of the screenshot does not exceed 1200*1200
    IMAGE_MAXSIZE = os.environ.get("IMAGE_MAXSIZE", None)
    SAVE_IMAGE = True
