import cv2
import os
import numpy as np
from config import *


def setup_cv(img, on_mouse):
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)  # 창 크기 수동 조절
    cv2.moveWindow(winname='image', x=50, y=50)

    cv2.setMouseCallback('image', on_mouse, img)


def load_label(img, img_file_name):
    y, x, c = img.shape

    if os.path.isfile(os.path.join(LABEL_PATH, img_file_name)):  # label file 존재시 label 불옴옴
        label = cv2.imread(os.path.join(LABEL_PATH, img_file_name))
    else:
        label = np.zeros((150, 200, c), dtype=np.uint8)

    label = cv2.resize(label, dsize=(200 * 5, 150 * 5), interpolation=cv2.INTER_AREA)

    dst = cv2.addWeighted(img, 0.7, label, 0.3, 0)

    return label, dst
