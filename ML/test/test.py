import os
import sys
import unittest

import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np

from util import show_tensor_img
from model import UNet

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class TestModel(unittest.TestCase):

    def test_model(self):
        model = UNet(nch=3, nker=64, norm="bnorm", learning_type="plain")

        img = plt.imread('test_img2.png')
        img = torch.Tensor(img)
        img = img.permute(2, 0, 1)
        img = img.unsqueeze(0)

        m = nn.ZeroPad2d((0, 0, 10, 0))
        img = m(img)

        print(img.shape)

        out = model(img)

        show_tensor_img(img)
        show_tensor_img(out)
        

if __name__ == "__main__":
    unittest.main()
