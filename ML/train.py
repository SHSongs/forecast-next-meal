import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from torchvision import transforms

from model import UNet
from dataset import *

from util import show_tensor_img

# model = UNet(nch=3, nker=64, norm="bnorm", learning_type="plain")
#
# img = plt.imread('test/test_img2.png')
# img = torch.Tensor(img)
# img = img.permute(2, 0, 1)
# img = img.unsqueeze(0)
#
# m = nn.ZeroPad2d((0, 0, 10, 0))
# img = m(img)
#
# print(img.shape)
#
# out = model(img)
#
# show_tensor_img(img)
# show_tensor_img(out)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


model = UNet(nch=3, nker=64, norm="bnorm", learning_type="plain")


transform_train = transforms.Compose([Normalization(), ToTensor(), Padding()])

dataset_train = Dataset(label_dir="test/data/label", input_dir="test/data/input", transform=transform_train)

loader_train = DataLoader(dataset_train, batch_size=1, shuffle=True, num_workers=0)

for batch, data in enumerate(loader_train, 1):
    label = data['label'].to(device)
    input = data['input'].to(device)

    output = model(input)
