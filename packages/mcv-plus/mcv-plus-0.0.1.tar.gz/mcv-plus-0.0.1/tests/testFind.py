import unittest
from mcv.image import match_template_best, Image


class TestMatchTemplateBest(unittest.TestCase):
    def setUp(self):
        # 加载测试用的图片和模板
        self.img = Image.read(r"C:\Users\KateT\Desktop\QQ20241024-183127.png")
        self.template = Image.read(r"C:\Users\KateT\Desktop\QQ20241024-183059.png")

    def test_match_template_best_full_image(self):
        # 测试在整张图片上进行模板匹配
        position = match_template_best(self.img, self.template)
        self.assertIsNotNone(position)
        self.assertIsInstance(position, tuple)
        self.assertEqual(len(position), 2)
        self.img.draw_rectangle(position,
                                (position[0] + self.template.width, position[1] + self.template.height)).draw_text(
            "测试", (position[0], position[1]), font_size=30).show()

    def test_match_template_best_with_region(self):
        # 测试在图片的指定区域进行模板匹配
        region = (100, 100, 500, 500)  # (x, y, width, height)
        position = match_template_best(self.img, self.template, region=region)
        self.assertIsNotNone(position)
        self.assertIsInstance(position, tuple)
        self.assertEqual(len(position), 2)

    def test_match_template_best_below_threshold(self):
        # 测试当匹配值低于阈值时的情况
        threshold = 1.0  # 设置一个较高的阈值
        position = match_template_best(self.img, self.template, threshold=threshold)
        self.assertIsNone(position)

    def test_match_template_best_with_level(self):
        # 测试指定金字塔层级进行模板匹配
        level = 2
        position = match_template_best(self.img, self.template, level=level)
        self.assertIsNotNone(position)
        self.assertIsInstance(position, tuple)
        self.assertEqual(len(position), 2)

    def tearDown(self):
        # # 释放图片资源
        # self.img.close()
        # self.template.close()
        pass


if __name__ == '__main__':
    unittest.main()
