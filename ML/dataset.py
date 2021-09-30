import os
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt


class Dataset(torch.utils.data.Dataset):
    def __init__(self, label_dir, input_dir, transform=None):
        self.input_dir = input_dir
        self.label_dir = label_dir

        self.transform = transform

        def load_img(path):
            dir_lst = os.listdir(path)

            dir_lst = [f for f in dir_lst if f.endswith('jpg') | f.endswith('png')]
            dir_lst.sort()

            img_lst = []

            for i in range(len(dir_lst)):
                img_lst.append(plt.imread(os.path.join(path, dir_lst[i])))

            return img_lst

        self.input_lst = load_img(input_dir)
        self.label_lst = load_img(label_dir)

    def __len__(self):
        return len(self.input_lst)

    def __getitem__(self, index):
        data = {'input': self.input_lst[index], 'label': self.label_lst[index]}

        if self.transform:
            data = self.transform(data)

        return data

