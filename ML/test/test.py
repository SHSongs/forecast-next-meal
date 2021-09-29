import os
import sys
import unittest

import torch
import torch.nn as nn
import matplotlib.pyplot as plt

from model import UNet

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class TestModel(unittest.TestCase):

    def test_model(self):
        model = UNet(nch=3, nker=64, norm="bnorm", learning_type="plain")

        img = plt.imread('test_img2.png')
        img = torch.Tensor(img)
        img = img.transpose(0, 2)
        img = img.unsqueeze(0)

        m = nn.ZeroPad2d((0, 10, 0, 0))
        img = m(img)

        self.assertTrue((1, 3, 200, 160) == img.size())

        out = model(img)
        self.assertTrue((1, 3, 200, 160) == out.size())


if __name__ == "__main__":
    unittest.main()
