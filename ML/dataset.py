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


class ToTensor(object):
    def __call__(self, data):
        label, input = data['label'], data['input']

        label = label.transpose((2, 0, 1)).astype(np.float32)
        input = input.transpose((2, 0, 1)).astype(np.float32)

        data = {'label': torch.from_numpy(label), 'input': torch.from_numpy(input)}

        return data


class Normalization(object):
    def __init__(self, mean=0.5, std=0.5):
        self.mean = mean
        self.std = std

    def __call__(self, data):
        label, input = data['label'], data['input']

        label = (label - self.mean) / self.std
        input = (input - self.mean) / self.std

        data = {'label': label, 'input': input}

        return data


class Padding(object):
    def __init__(self):
        pass
    def __call__(self, data):
        label, input = data['label'], data['input']

        m = nn.ZeroPad2d((0, 0, 10, 0))
        label = m(label)
        input = m(input)

        data = {'label': label, 'input': input}

        return data
