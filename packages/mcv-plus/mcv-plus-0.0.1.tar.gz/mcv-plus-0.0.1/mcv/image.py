import base64
import math
import os
from typing import Sequence, Tuple, Optional, List

import cv2
import numpy as np
from PIL import ImageDraw, Image as PilImage, ImageFont


class Image:
    def __init__(self, image: cv2.Mat):
        """
        图像包装类
        :param image: cv2.Mat
        """
        self.data = image
        self.height, self.width = image.shape[:2]
        self.channels = self.data.shape[2] if len(self.data.shape) == 3 else 1

    """基础功能-读写显示"""

    @classmethod
    def read(cls, file_path: str):
        """
        从文件读取图像
        :param file_path: 文件路径
        :return: Image
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        # 读取文件内容
        data = np.fromfile(file_path, dtype=np.uint8)
        # 解码图像
        return cls(cv2.imdecode(data, cv2.IMREAD_COLOR))

    def save(self, file_path, ext=".png"):
        """
        保存图像
        :param file_path: 文件路径
        :param ext: 压缩格式
        :return:
        """
        return cv2.imencode(ext, self.data)[1].tofile(file_path)

    def show(self, window_name="Image"):
        """
        显示图像
        :param window_name: 窗口名称
        :return:
        """
        cv2.imshow(window_name, self.data)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def to_base64(self):
        """
        将图像转换为base64编码
        :return: base64编码
        """
        _, buffer = cv2.imencode(".png", self.data)
        return str(base64.b64encode(buffer.tobytes()).decode("utf-8"))

    def to_bytes(self):
        """
        将图像转换为字节数组
        :return: 字节数组
        """
        return self.data.tobytes()

    """图像处理功能"""
    def resize(self, width: int, height: int):
        """
        调整图像大小
        :param width: 宽
        :param height: 高
        :return:
        """
        return Image(cv2.resize(self.data, (width, height)))

    def scale(self, fx: float = 100.0 / 100, fy: float = 100.0 / 100):
        """
        调整图像比例
        :param fx: 宽比例
        :param fy: 高比例
        :return:
        """
        return Image(cv2.resize(self.data, None, fx=fx, fy=fy))

    def grayscale(self):
        """
        灰度化图像
        :return:
        """
        return Image(cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY))

    def clip(self, x: int, y: int, w: int, h: int):
        """
        裁切图像
        :param x: 起始点x
        :param y: 起始点y
        :param w: 宽
        :param h: 高
        :return:
        """
        return Image(self.data[y:y + h, x:x + w])

    def pyr_down(self):
        """
        图像金字塔下采样
        :return:
        """
        return Image(cv2.pyrDown(self.data))

    """其他功能"""

    def get_pixel(self, x: int, y: int):
        """
        获取图像像素点BGR值
        :param x:
        :param y:
        :return:
        """
        return self.data[y, x]

    """绘图功能"""
    """画线"""

    def draw_line(self, pt1: Sequence[int], pt2: Sequence[int], color: Sequence[float] = (0, 0, 255)
                  , thickness: int = 1):
        """
        画线
        :param pt1: (x,y)
        :param pt2: (x,y)
        :param color: (b,g,r)
        :param thickness: 线粗细
        :return:
        """
        return Image(cv2.line(self.data, pt1, pt2, color, thickness))

    def draw_rectangle(self, pt1: Sequence[int], pt2: Sequence[int], color: Sequence[float] = (0, 0, 255)
                       , thickness: int = 1):
        """
        方框绘制
        :param pt1: (start_x,start_y)
        :param pt2: (end_x,end_y)
        :param color: (b,g,r)
        :param thickness: 线粗细
        :return:
        """
        return Image(cv2.rectangle(self.data, pt1, pt2, color, thickness))

    def draw_circle(self, center: Sequence[int], radius: int, color: Sequence[float] = (0, 0, 255)
                    , thickness: int = 1):
        """
        画圆
        :param center: (x,y)
        :param radius: 直径
        :param color: (b,g,r)
        :param thickness: 线粗细
        :return:
        """
        return Image(cv2.circle(self.data, center, radius, color, thickness))


    def draw_text(self, text: str, position: Sequence[int], color: Sequence[int] = (0, 0, 255)
                  , font_size: int = 1, font_path: str = "simsun.ttc"):
        """
        画文字
        :param text: 文本内容
        :param position: 文字位置
        :param color: 文字颜色
        :param font_size: 字体大小
        :param font_path: 字体路径
        :return:
        """
        # 将OpenCV图像转换为Pillow图像
        img_pil = PilImage.fromarray(cv2.cvtColor(self.data, cv2.COLOR_BGR2RGB))

        # 创建Pillow的绘图对象
        draw = ImageDraw.Draw(img_pil)

        # 加载字体
        font = ImageFont.truetype(font_path, font_size)
        b, g, r = color
        x, y = position
        # 绘制文本
        draw.text((x, y), text, font=font, fill=(r, g, b))

        return Image(cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR))



    def draw_point(self, center: Sequence[int], radius: int = 1, color: Sequence[float] = (0, 0, 255)):
        """
        画点
        :param center: 中心点坐标
        :param radius: 半径
        :param color: 颜色
        :return:
        """
        return Image(cv2.circle(self.data, center, radius, color, -1))


"""模板匹配相关"""


def select_pyramid_level(img: Image, template: Image):
    min_dim = min(img.height, img.width,
                  template.height, template.width)
    if min_dim < 32:
        return 0
    max_level = int(math.log2(min_dim // 16))
    return min(6, max_level)


def generate_pyramid(img: Image, level: int):
    pyramid = [img]
    for _ in range(level):
        img = img.pyr_down()
        pyramid.append(img)
    return pyramid


def find_matches(res: cv2.Mat, match_threshold: float = 0.95):
    loc = np.where(res >= match_threshold)
    return [pt for pt in zip(*loc[::-1])]


def match_template(img: Image, template: Image, region: Sequence[int] = None, threshold: float = 0.95,
                   max_result: int = 5) -> Optional[List[Tuple[int, int]]]:
    """
    模板匹配(找图)
    :param img: Image 大图
    :param template: Image 小图
    :param region: 匹配范围[x,y,w,h]
    :param threshold: 匹配阈值
    :param max_result: 最大匹配数量
    :return:
    """
    # 设置查找区域
    x, y, w, h = region if region else (0, 0, img.width, img.height)
    img = img.clip(x, y, w, h)

    # # 对图像和模板进行灰度化
    img = img.grayscale()
    template = template.grayscale()

    matches = []
    res = cv2.matchTemplate(img.data, template.data, cv2.TM_CCOEFF_NORMED)

    loc = find_matches(res, threshold)

    for pt in loc[:max_result]:
        match = (pt[0] + x, pt[1] + y)
        if not any(np.allclose(match, m) for m in matches):
            matches.append(match)

    return matches if len(matches) > 0 else None


def match_template_best(img: Image, template: Image, region: Sequence[int] = None,
                        threshold: float = 0.95,
                        level: int = None) -> Optional[Tuple[int, int]]:
    """
    模板匹配(找图)
    :param img: Image 大图
    :param template: Image 小图
    :param region: 匹配范围[x,y,w,h]
    :param threshold: 匹配阈值
    :param level: level
    :return:
    """
    # 设置查找区域
    x, y, w, h = region if region else (0, 0, img.width, img.height)
    img = img.clip(x, y, w, h)

    # 设置金字塔等级
    if level is None:
        level = select_pyramid_level(img, template)
    # 灰度化
    img = img.grayscale()
    template = template.grayscale()
    # 创建图像金字塔列表
    img_array = generate_pyramid(img, level)
    template_array = generate_pyramid(template, level)

    for i in reversed(range(level + 1)):
        img_level = img_array[i]
        template_level = template_array[i]
        res = cv2.matchTemplate(img_level.data, template_level.data, cv2.TM_CCOEFF_NORMED)

        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if max_val > threshold:
            return max_loc[0] * (2 ** i) + x, max_loc[1] * (2 ** i) + y


"""找色相关"""


def find_color_inner(img: Image, color: Sequence[int], region: Sequence[int] = None, threshold: int = 4):
    """

    :param img:
    :param color:
    :param region:
    :param threshold:
    :return:
    """
    lower_bound = np.array(
        [max(color - threshold, 0) for color in color], dtype=np.uint8
    )
    upper_bound = np.array(
        [min(color + threshold, 255) for color in color], dtype=np.uint8
    )
    x, y, w, h = region if region else [0, 0, img.width, img.height]
    img = img.clip(x, y, w, h)
    mask = cv2.inRange(img, lower_bound, upper_bound)
    return cv2.findNonZero(mask)


def find_color(img: Image, color: Sequence[int], region: Sequence[int] = None, threshold: int = 4) -> Optional[
    Tuple[int, int]]:
    """

    :param img:
    :param color:
    :param region:
    :param threshold:
    :return:
    """
    x, y = region[:2] if region else [0, 0]
    result = find_color_inner(img, color, region, threshold)
    if result is None:
        return None
    point = [e for e in result[0][0]]
    return point[0] + x, point[1] + y


def find_all_points_color(img: Image, color: Sequence[int], region: Sequence[int] = None, threshold: int = 4) -> \
        Optional[List[Tuple[int, int]]]:
    """

    :param img:
    :param color:
    :param region:
    :param threshold:
    :return:
    """
    x, y = region[:2] if region else [0, 0]
    result = find_color_inner(img, color, region, threshold)
    if result is None:
        return None
    points = [(p[0][0], p[0][1]) for p in result]
    return [(point[0] + x, point[1] + y) for point in points]


def find_multi_colors(img: Image, first_color: Sequence[int], colors: List[Tuple[int, int, Sequence[int]]],
                      region: Sequence[int] = None,
                      threshold: int = 4) -> Optional[Tuple[int, int]]:
    first_color_points = find_all_points_color(img, first_color, region=region, threshold=threshold)
    if first_color_points is None:
        return None
    for result in first_color_points:
        for x, y, target_color in colors:
            dx, dy = x + result[0], y + result[1]
            if dx >= img.width or dy >= img.height or dx < 0 or dy < 0:
                result = None
                break
            offset_color = img.get_pixel(dx, dy)  # (b,g,r)
            is_similar = all(abs(a - b) <= threshold for a, b in zip(offset_color, target_color))
            if not is_similar:
                result = None
                break
        if result is not None:
            return result
    return None
