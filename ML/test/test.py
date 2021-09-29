import os
import sys
import unittest

import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np

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
        self.assertTrue((1, 3, 160, 200) == img.size())

        out = model(img)
        self.assertTrue((1, 3, 160, 200) == out.size())

        fn_tonumpy = lambda x: x.to('cpu').detach().numpy().transpose(0, 2, 3, 1)
        fn_denorm = lambda x, mean, std: (x * std) + mean

        img = fn_tonumpy(img)

        out = fn_tonumpy(fn_denorm(out, mean=0.5, std=0.5))
        out = np.clip(out, a_min=0, a_max=1)

        print(out.shape)

        plt.imsave('input.png', img[0])
        plt.imsave('output.png', out[0])


if __name__ == "__main__":
    unittest.main()
