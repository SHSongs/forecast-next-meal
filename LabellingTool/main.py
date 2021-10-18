import numpy as np
import cv2
import os

from util import crop_img, load_img_files
from cv_util import setup_cv, load_label

from config import *


def on_mouse(event, x, y, flags, param):
    global oldx, oldy
    global brush_size
    global dst

    if event == cv2.EVENT_LBUTTONDOWN:
        oldx, oldy = x, y

    elif event == cv2.EVENT_RBUTTONDOWN:
        oldx, oldy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:  # ==를 쓰면 다른 키도 입력되었을 때 작동안하므로 &(and) 사용

            cv2.line(label, (oldx, oldy), (x, y), COLOR_LIST[color_idx], brush_size, cv2.LINE_AA)
            dst = cv2.addWeighted(img, 0.7, label, 0.3, 0)
            cv2.imshow('image', dst)
            oldx, oldy = x, y

        if flags & cv2.EVENT_FLAG_RBUTTON:  # ==를 쓰면 다른 키도 입력되었을 때 작동안하므로 &(and) 사용
            cv2.line(label, (oldx, oldy), (x, y), (0, 0, 0), brush_size, cv2.LINE_AA)
            dst = cv2.addWeighted(img, 0.7, label, 0.3, 0)
            cv2.imshow('image', dst)
            oldx, oldy = x, y


color_idx = 0
img_files = load_img_files()

oldx = oldy = -1

brush_size = 10

img_index = 0


img = cv2.imread(os.path.join(IMG_PATH, img_files[img_index]))
img = crop_img(img)

y, x, c = img.shape


label, dst = load_label(img, img_files[img_index])
cv2.imshow('image', dst)

setup_cv(img, on_mouse=on_mouse)

show_label = False


def next_img(n):
    global label
    global img
    global img_index

    print(img_files[img_index])
    cv2.imwrite(os.path.join(LABEL_PATH, img_files[img_index]), label)

    img_index += n

    img = cv2.imread(os.path.join(IMG_PATH, img_files[img_index]))
    img = crop_img(img)


    label, dst = load_label(img, img_files[img_index])
    cv2.imshow('image', dst)


while True:
    key = cv2.waitKey()

    if key == ord('1'):
        brush_size -= 1
    elif key == ord('2'):
        brush_size += 1
    elif key == ord('l'):
        if show_label:
            cv2.imshow('image', label)
        else:
            cv2.imshow('image', dst)
        show_label = not show_label
    elif key == ord('z'):  # 밥
        color_idx = 0
        pass
    elif key == ord('x'):  # 국
        color_idx = 1
        pass
    elif key == ord('a'):  # 왼쪽 반찬
        color_idx = 2
        pass
    elif key == ord('r'):  # 중앙 반찬
        color_idx = 3
        pass
    elif key == ord('s'):  # 오른쪽 반찬
        color_idx = 4
        pass
    elif key == ord('t'):  # 특수반찬
        color_idx = 5
    elif key == 27:  # esc
        break

    print(key)
    if key == 3:  # right arrow
        print('right')
        next_img(1)

    elif key == 2:  # left arrow
        print('left')
        next_img(-1)

cv2.destroyAllWindows()
