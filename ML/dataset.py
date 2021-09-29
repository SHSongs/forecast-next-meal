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

        input_dir_lst = os.listdir(self.input_dir)

        input_dir_lst = [f for f in input_dir_lst if f.endswith('jpg') | f.endswith('png')]
        input_dir_lst.sort()

        self.input_lst = []

        for i in range(len(input_dir_lst)):
            self.input_lst.append(plt.imread(os.path.join(self.input_dir, input_dir_lst[i])))

        label_dir_lst = os.listdir(self.label_dir)

        label_dir_lst = [f for f in label_dir_lst if f.endswith('jpg') | f.endswith('png')]
        label_dir_lst.sort()

        self.label_lst = []

        for i in range(len(label_dir_lst)):
            self.label_lst.append(plt.imread(os.path.join(self.label_dir, label_dir_lst[i])))

    def __len__(self):
        return len(self.input_lst)

    def __getitem__(self, index):
        data = {'input': self.input_lst[index], 'label': self.label_dir[index]}

        if self.transform:
            data = self.transform(data)

        return data

