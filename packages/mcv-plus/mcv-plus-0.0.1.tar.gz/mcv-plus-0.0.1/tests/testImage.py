import unittest
from unittest.mock import patch, MagicMock
import cv2
import numpy as np

from mcv.image import Image


class TestImage(unittest.TestCase):

    def setUp(self):
        # 创建一个测试用的cv2.Mat对象
        self.mock_image = cv2.imread(r"C:\Users\KateT\Desktop\QQ20241024-181405.png")
        self.image = Image(self.mock_image)

    def test_init(self):
        # 测试初始化是否正确
        self.assertIsInstance(self.image.data, np.ndarray)
        self.assertEqual(self.image.height, self.mock_image.shape[0])
        self.assertEqual(self.image.width, self.mock_image.shape[1])
        self.assertEqual(self.image.channels, self.mock_image.shape[2] if len(self.mock_image.shape) == 3 else 1)

    def test_read(self):
        # 测试读取文件功能
        with patch('mcv.image.Image') as MockImage:
            mock_file_path = r"C:\Users\KateT\Desktop\QQ20241024-181405.png"
            MockImage.return_value = self.image
            read_image = Image.read(mock_file_path)
            self.assertIsInstance(read_image, Image)
            # MockImage.assert_called_once_with(self.mock_image)

    def test_save(self):
        # 测试保存文件功能
        with patch('cv2.imencode') as mock_imencode:
            mock_imencode.return_value = (True, MagicMock())
            test_file_path = 'path/to/test_output.png'
            self.image.save(test_file_path)
            mock_imencode.assert_called_once_with('.png', self.mock_image)

    def test_show(self):
        # 测试显示图像功能
        with patch('cv2.imshow') as mock_imshow, \
                patch('cv2.waitKey') as mock_waitKey, \
                patch('cv2.destroyAllWindows') as mock_destroyAllWindows:
            self.image.show()
            mock_imshow.assert_called_once_with('Image', self.mock_image)
            mock_waitKey.assert_called_once_with(0)
            mock_destroyAllWindows.assert_called_once()

    def test_resize(self):
        # 测试调整图像大小
        resized_image = self.image.resize(100, 100)
        self.assertEqual(resized_image.width, 100)
        self.assertEqual(resized_image.height, 100)

    def test_scale(self):
        # 测试调整图像比例
        scaled_image = self.image.scale(0.5, 0.5)
        self.assertEqual(scaled_image.width - 1, self.image.width // 2)
        self.assertEqual(scaled_image.height, self.image.height // 2)

    def test_grayscale(self):
        # 测试灰度化图像
        gray_image = self.image.grayscale()
        self.assertEqual(gray_image.channels, 1)

    def test_clip(self):
        # 测试裁切图像
        clipped_image = self.image.clip(10, 10, 100, 100)
        self.assertEqual(clipped_image.width, 100)
        self.assertEqual(clipped_image.height, 100)

    def test_pyr_down(self):
        # 测试图像金字塔下采样
        downsampled_image = self.image.pyr_down()
        self.assertEqual(downsampled_image.width - 1, self.image.width // 2)
        self.assertEqual(downsampled_image.height, self.image.height // 2)

    def test_get_pixel(self):
        # 测试获取像素点值
        pixel_value = self.image.get_pixel(10, 10)
        self.assertIsInstance(pixel_value, np.ndarray)

    def test_draw_line(self):
        # 测试画线功能
        line_image = self.image.draw_line((10, 10), (100, 100))
        # 这里可以添加更详细的断言，检查线是否被正确绘制
        line_image.show()

    def test_draw_rectangle(self):
        # 测试画矩形功能
        rect_image = self.image.draw_rectangle((10, 10), (100, 100), (0, 0, 255), 10)
        # 这里可以添加更详细的断言，检查矩形是否被正确绘制
        rect_image.show()

    def test_draw_circle(self):
        # 测试画圆功能
        circle_image = self.image.draw_circle((50, 50), 30)
        # 这里可以添加更详细的断言，检查圆是否被正确绘制
        circle_image.show()

    def test_draw_text(self):
        # 测试画文字功能
        text_image = self.image.draw_text('Test', (10, 10), font_size=100)
        # 这里可以添加更详细的断言，检查文字是否被正确绘制
        text_image.show()

    def test_draw_point(self):
        # 测试画点功能
        point_image = self.image.draw_point((100, 100), radius=10)
        # 这里可以添加更详细的断言，检查点是否被正确绘制
        point_image.show()


if __name__ == '__main__':
    unittest.main()
