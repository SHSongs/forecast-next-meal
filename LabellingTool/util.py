import os
from config import IMG_PATH


def load_img_files():
    file_list = os.listdir(IMG_PATH)
    img_files = [file for file in file_list if file.endswith('.png')]
    img_files.sort()
    print(img_files)
    return img_files


def crop_img(img):
    y, x, c = img.shape

    left_x = int((x - 200) / 2)
    up_y = int((y - 150) / 2)

    img = img[up_y:up_y + 150, left_x:left_x + 200]

    y, x, c = img.shape

    print(x, y)
    assert x == 200 and y == 150

    return img


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))
