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


from torchvision import transforms
from dataset import *


class TestData(unittest.TestCase):
    def test_dataset(self):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        model = UNet(nch=3, nker=64, norm="bnorm", learning_type="plain")

        transform_train = transforms.Compose([Normalization(), ToTensor(), Padding()])

        dataset_train = Dataset(label_dir="data/label", input_dir="data/input", transform=transform_train)

        loader_train = DataLoader(dataset_train, batch_size=1, shuffle=True, num_workers=0)

        for batch, data in enumerate(loader_train, 1):
            label = data['label'].to(device)
            input = data['input'].to(device)

            output = model(input)

            show_tensor_img(label)
            show_tensor_img(input)
            show_tensor_img(output)

            self.assertTrue((1, 3, 160, 200) == label.size())
            self.assertTrue((1, 3, 160, 200) == input.size())
            self.assertTrue((1, 3, 160, 200) == label.size())

if __name__ == "__main__":
    unittest.main()
