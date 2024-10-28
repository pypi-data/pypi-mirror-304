#!/usr/bin/env python
# -*- coding: utf-8 -*-

""""Airtest图像识别专用."""

import os
import sys
import time
import types
from six import PY3
from copy import deepcopy

from robotlib.graphic.recognize.robotcv import robotcv
from robotlib.graphic.recognize.robotcv import cv2
from robotlib.graphic.recognize.robotcv import error as robotcverr
from robotlib.graphic.recognize.core.helper import G, logwrap
from robotlib.graphic.recognize.core.settings import Settings as ST  # noqa
from robotlib.graphic.recognize.core.error import TargetNotFoundError, InvalidMatchingMethodError
from robotlib.graphic.recognize.utils.transform import TargetPos

from robotlib.graphic.recognize.robotcv.template_matching import TemplateMatching
from robotlib.graphic.recognize.robotcv.multiscale_template_matching import MultiScaleTemplateMatching,MultiScaleTemplateMatchingPre
from robotlib.graphic.recognize.robotcv.keypoint_matching import KAZEMatching, BRISKMatching, AKAZEMatching, ORBMatching
from robotlib.graphic.recognize.robotcv.keypoint_matching_contrib import SIFTMatching, SURFMatching, BRIEFMatching

MATCHING_METHODS = {
    "tpl": TemplateMatching,
    "mstpl": MultiScaleTemplateMatchingPre,
    "gmstpl": MultiScaleTemplateMatching,
    "kaze": KAZEMatching,
    "brisk": BRISKMatching,
    "akaze": AKAZEMatching,
    "orb": ORBMatching,
    "sift": SIFTMatching,
    "surf": SURFMatching,
    "brief": BRIEFMatching,
}


@logwrap
def loop_find(query, screen=None, timeout=ST.FIND_TIMEOUT, threshold=None, interval=0.5, intervalfunc=None):
    """
    Search for image template in the screen until timeout

    Args:
        query: image template to be found in screenshot
        screen: 当前设备的屏幕中显示的图像
        timeout: time interval how long to look for the image template
        threshold: default is None
        interval: sleep interval before next attempt to find the image template
        intervalfunc: function that is executed after unsuccessful attempt to find the image template

    Raises:
        TargetNotFoundError: when image template is not found in screenshot

    Returns:
        TargetNotFoundError if image template not found, otherwise returns the position where the image template has
        been found in screenshot
        找到结果：result:模板图标某个区域的坐标;
        rectangle:四个点的坐标(左上角,右上角,左下角,右下角);
        confidence:可信度（0-1）值越大表示越相似或越可信; time:耗时;
        focus_pos: 以模板图片的九宫格区域位置在，屏幕图片的中的坐标
        例:
        {'result': (37, 41),
        'rectangle': ((0, 7), (0, 76), (74, 76), (74, 7)),
        'confidence': 0.9020239114761353,
        'time': 0.018950223922729492,
        'focus_pos': (37, 41)}
    """
    G.LOGGING.info("Try finding: %s", query)
    start_time = time.time()
    while True:
        import subprocess
        # cmd = "adb shell screencap"  # 替换为你想执行的命令
        # #subprocess.run(cmd, shell=True)
        # screen = os.popen(cmd)
        # screen = screen.buffer.read().decode(encoding='utf-8')
        #screen = G.DEVICE.snapshot(filename=None, quality=ST.SNAPSHOT_QUALITY)

        if screen is None:
            G.LOGGING.warning("Screen is None, may be locked")
        else:
            if threshold:
                query.threshold = threshold
            match_pos = query.match_in(screen)
            if match_pos:
                try_log_screen(screen)
                return match_pos

        if intervalfunc is not None:
            intervalfunc(query.filepath)
        # 到这里就是没有找到了,直接抛出没找到的异常就行了,外界调用的地方一定要捕获下
        raise TargetNotFoundError('Picture %s not found in screen' % query)
        # 下面这个地方去掉
        # 超时则raise，未超时则进行下次循环:
        # if (time.time() - start_time) > timeout:
        #     try_log_screen(screen)
        #     raise TargetNotFoundError('Picture %s not found in screen' % query)
        # else:
        #     time.sleep(interval)


@logwrap
def try_log_screen(screen=None, quality=None, max_size=None):
    """
    Save screenshot to file

    Args:
        screen: screenshot to be saved
        quality: The image quality, default is ST.SNAPSHOT_QUALITY
        max_size: the maximum size of the picture, e.g 1200

    Returns:
        {"screen": filename, "resolution": robotcv.get_resolution(screen)}

    """
    if not ST.LOG_DIR or not ST.SAVE_IMAGE:
        return
    if not quality:
        quality = ST.SNAPSHOT_QUALITY
    if not max_size:
        max_size = ST.IMAGE_MAXSIZE
    if screen is None:
        #screen = G.DEVICE.snapshot(quality=quality)
        # TODO 这里预留 这里如果没有传入当前图片则从当前设备获取图片,可以通过adb 从机器读取，也可以通过摄像机拍照抓取，这里主要看采集图片的方式
        return None

    filename = "%(time)d.jpg" % {'time': time.time() * 1000}
    filepath = os.path.join(ST.LOG_DIR, filename)
    if screen is not None:
        robotcv.imwrite(filepath, screen, quality, max_size=max_size)
        return {"screen": filename, "resolution": robotcv.get_resolution(screen)}
    return None


class Template(object):
    """
    picture as touch/swipe/wait/exists target and extra info for cv match
    filename: pic filename
    target_pos: （九宫格位置） ret which pos in the pic
    record_pos: pos in screen when recording
    resolution: (宽，高) screen resolution when recording
    rgb: 识别结果是否使用rgb三通道进行校验.
    scale_max: 多尺度模板匹配最大范围.
    scale_step: 多尺度模板匹配搜索步长.
    """

    def __init__(self, filename, threshold=None, target_pos=TargetPos.MID, record_pos=None, resolution=(), rgb=False, scale_max=800, scale_step=0.005):
        self.filename = filename
        self._filepath = None
        self.threshold = threshold or ST.THRESHOLD
        self.target_pos = target_pos
        self.record_pos = record_pos
        self.resolution = resolution
        self.rgb = rgb
        self.scale_max = scale_max
        self.scale_step = scale_step

    @property
    def filepath(self):
        if self._filepath:
            return self._filepath
        for dirname in G.BASEDIR:
            filepath = os.path.join(dirname, self.filename)
            if os.path.isfile(filepath):
                self._filepath = filepath
                return self._filepath
        return self.filename

    def __repr__(self):
        filepath = self.filepath if PY3 else self.filepath.encode(sys.getfilesystemencoding())
        return "Template(%s)" % filepath

    def match_in(self, screen):
        '''
        根据当前设备屏幕图片，进行匹配模板，并把匹配结果返回
        :param screen:
        :return: match_result
        这样格式的信息
        {'result': (37, 41),
        'rectangle': ((0, 7), (0, 76), (74, 76), (74, 7)),
        'confidence': 0.9020239114761353,
        'time': 0.01994609832763672,
        'focus_pos': (37, 41)}
        其中 result 是根据 target_pos 来的
        rectangle 是模板图片在查找图片中的位置坐标点 （左上角，左下角，右下角，右上角）
        '''
        match_result = self._cv_match(screen)
        G.LOGGING.debug("match result: %s", match_result)
        if not match_result:
            return None
        focus_pos = TargetPos().getXY(match_result, self.target_pos)
        #把这个 focus_pos 也加进去
        match_result['focus_pos'] = focus_pos
        return match_result

    def match_all_in(self, screen):
        image = self._imread()
        image = self._resize_image(image, screen, ST.RESIZE_METHOD)
        return self._find_all_template(image, screen)

    @logwrap
    def _cv_match(self, screen):
        # in case image file not exist in current directory:
        ori_image = self._imread()
        image = self._resize_image(ori_image, screen, ST.RESIZE_METHOD)
        ret = None
        for method in ST.CVSTRATEGY:
            # get function definition and execute:
            func = MATCHING_METHODS.get(method, None)
            if func is None:
                raise InvalidMatchingMethodError("Undefined method in CVSTRATEGY: '%s', try 'kaze'/'brisk'/'akaze'/'orb'/'surf'/'sift'/'brief' instead." % method)
            else:
                if method in ["mstpl", "gmstpl"]:
                    ret = self._try_match(func, ori_image, screen, threshold=self.threshold, rgb=self.rgb, record_pos=self.record_pos,
                                            resolution=self.resolution, scale_max=self.scale_max, scale_step=self.scale_step)
                else:
                    ret = self._try_match(func, image, screen, threshold=self.threshold, rgb=self.rgb)
            if ret:
                break
        return ret

    @staticmethod
    def _try_match(func, *args, **kwargs):
        '''

        :param func: 类或这函数
        :param args: 位置参数
        :param kwargs: 关键字参数
        :return:
        '''
        G.LOGGING.debug("try match with %s" % func.__name__)
        try:
            # 根据参数构造一个图像识别类并调用这个类中的方法
            ret = func(*args, **kwargs).find_best_result()
        except robotcverr.NoModuleError as err:
            G.LOGGING.warning("'surf'/'sift'/'brief' is in opencv-contrib module. You can use 'tpl'/'kaze'/'brisk'/'akaze'/'orb' in CVSTRATEGY, or reinstall opencv with the contrib module.")
            return None
        except robotcverr.BaseError as err:
            G.LOGGING.debug(repr(err))
            return None
        else:
            return ret

    def _imread(self):
        return robotcv.imread(self.filepath)

    def _find_all_template(self, image, screen):
        return TemplateMatching(image, screen, threshold=self.threshold, rgb=self.rgb).find_all_results()

    def _find_keypoint_result_in_predict_area(self, func, image, screen):
        if not self.record_pos:
            return None
        # calc predict area in screen
        image_wh, screen_resolution = robotcv.get_resolution(image), robotcv.get_resolution(screen)
        xmin, ymin, xmax, ymax = Predictor.get_predict_area(self.record_pos, image_wh, self.resolution, screen_resolution)
        # crop predict image from screen
        predict_area = robotcv.crop_image(screen, (xmin, ymin, xmax, ymax))
        if not predict_area.any():
            return None
        # keypoint matching in predicted area:
        ret_in_area = func(image, predict_area, threshold=self.threshold, rgb=self.rgb)
        # calc cv ret if found
        if not ret_in_area:
            return None
        ret = deepcopy(ret_in_area)
        if "rectangle" in ret:
            for idx, item in enumerate(ret["rectangle"]):
                ret["rectangle"][idx] = (item[0] + xmin, item[1] + ymin)
        ret["result"] = (ret_in_area["result"][0] + xmin, ret_in_area["result"][1] + ymin)
        return ret

    def _resize_image(self, image, screen, resize_method):
        """模板匹配中，将输入的截图适配成 等待模板匹配的截图."""
        # 未记录录制分辨率，跳过
        if not self.resolution:
            return image
        screen_resolution = robotcv.get_resolution(screen)
        #print("screen_resolution",screen_resolution,";self.resolution",self.resolution)
        # 如果分辨率一致，则不需要进行im_search的适配:
        if tuple(self.resolution) == tuple(screen_resolution) or resize_method is None:
            return image
        if isinstance(resize_method, types.MethodType):
            resize_method = resize_method.__func__
        # 分辨率不一致则进行适配，默认使用cocos_min_strategy:
        h, w = image.shape[:2]
        w_re, h_re = resize_method(w, h, self.resolution, screen_resolution)
        # 确保w_re和h_re > 0, 至少有1个像素:
        w_re, h_re = max(1, w_re), max(1, h_re)
        # 调试代码: 输出调试信息.
        G.LOGGING.debug("resize: (%s, %s)->(%s, %s), resolution: %s=>%s" % (
                        w, h, w_re, h_re, self.resolution, screen_resolution))
        # 进行图片缩放:
        image = cv2.resize(image, (w_re, h_re))
        return image


class Predictor(object):
    """
    this class predicts the press_point and the area to search im_search.
    """

    DEVIATION = 100

    @staticmethod
    def count_record_pos(pos, resolution):
        """计算坐标对应的中点偏移值相对于分辨率的百分比."""
        _w, _h = resolution
        # 都按宽度缩放，针对G18的实验结论
        delta_x = (pos[0] - _w * 0.5) / _w
        delta_y = (pos[1] - _h * 0.5) / _w
        delta_x = round(delta_x, 3)
        delta_y = round(delta_y, 3)
        return delta_x, delta_y

    @classmethod
    def get_predict_point(cls, record_pos, screen_resolution):
        """预测缩放后的点击位置点."""
        delta_x, delta_y = record_pos
        _w, _h = screen_resolution
        target_x = delta_x * _w + _w * 0.5
        target_y = delta_y * _w + _h * 0.5
        return target_x, target_y

    @classmethod
    def get_predict_area(cls, record_pos, image_wh, image_resolution=(), screen_resolution=()):
        """Get predicted area in screen."""
        x, y = cls.get_predict_point(record_pos, screen_resolution)
        # The prediction area should depend on the image size:
        if image_resolution:
            predict_x_radius = int(image_wh[0] * screen_resolution[0] / (2 * image_resolution[0])) + cls.DEVIATION
            predict_y_radius = int(image_wh[1] * screen_resolution[1] / (2 * image_resolution[1])) + cls.DEVIATION
        else:
            predict_x_radius, predict_y_radius = int(image_wh[0] / 2) + cls.DEVIATION, int(image_wh[1] / 2) + cls.DEVIATION
        area = (x - predict_x_radius, y - predict_y_radius, x + predict_x_radius, y + predict_y_radius)
        return area
