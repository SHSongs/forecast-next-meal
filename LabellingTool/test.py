import unittest

from util import crop_img
import numpy as np


class UtilTestCase(unittest.TestCase):
    def test_crop_img(self):
        test_img = np.zeros((199, 303, 3), dtype=np.uint8)
        cropped_img = crop_img(test_img)
        y, x, c = cropped_img.shape
        self.assertEqual((y, x, c), (150, 200, 3))


if __name__ == '__main__':
    unittest.main()
