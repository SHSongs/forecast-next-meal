import cv2
import os

from util import crop_img, load_img_files, clamp
from cv_util import setup_cv, load_label

import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

from config import *

font = ImageFont.truetype("fonts/NanumGothic.ttf", 40)


def on_mouse(event, x, y, flags, param):
    global oldx, oldy
    global brush_size
    global dst
    global font

    if event == cv2.EVENT_LBUTTONDOWN:
        oldx, oldy = x, y

    elif event == cv2.EVENT_RBUTTONDOWN:
        oldx, oldy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:  # ==를 쓰면 다른 키도 입력되었을 때 작동안하므로 &(and) 사용
            cv2.line(label, (oldx, oldy), (x, y), COLOR_LIST[color_idx], brush_size, cv2.LINE_AA)
            dst = cv2.addWeighted(img, 0.4, label, 0.6, 0)
            cv2.line(dst, (x, y), (x, y), COLOR_LIST[color_idx], brush_size, cv2.LINE_4)

        if flags & cv2.EVENT_FLAG_RBUTTON:  # ==를 쓰면 다른 키도 입력되었을 때 작동안하므로 &(and) 사용
            cv2.line(label, (oldx, oldy), (x, y), (0, 0, 0), brush_size, cv2.LINE_AA)
            dst = cv2.addWeighted(img, 0.5, label, 0.5, 0)

        dst = Image.fromarray(dst)
        draw = ImageDraw.Draw(dst)
        text = CLASS_LIST[color_idx]
        org = (50, 50)
        draw.text(org, text, font=font, fill=(255, 255, 255))
        dst = np.array(dst)
        cv2.imshow('image', dst)
        oldx, oldy = x, y


color_idx = 0
img_files = load_img_files()

oldx = oldy = -1

brush_size = 100
brush_size_control_ratio = 10

img_index = 0

img = cv2.imread(os.path.join(IMG_PATH, img_files[img_index]))
img = crop_img(img)
img = cv2.resize(img, dsize=(200 * 5, 150 * 5), interpolation=cv2.INTER_AREA)

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

    label = cv2.resize(label, dsize=(200, 150), interpolation=cv2.INTER_AREA)
    cv2.imwrite(os.path.join(LABEL_PATH, img_files[img_index]), label)

    img_index += n
    img_index = clamp(img_index, 0, len(img_files) - 1)

    img = cv2.imread(os.path.join(IMG_PATH, img_files[img_index]))
    img = crop_img(img)
    img = cv2.resize(img, dsize=(200 * 5, 150 * 5), interpolation=cv2.INTER_AREA)

    label, dst = load_label(img, img_files[img_index])
    cv2.imshow('image', dst)


while True:
    key = cv2.waitKey()

    if key == ord('1'):
        brush_size -= brush_size_control_ratio
    elif key == ord('2'):
        brush_size += brush_size_control_ratio
    elif key == ord('l'):
        if show_label:
            cv2.imshow('image', label)
        else:
            cv2.imshow('image', dst)
        show_label = not show_label
    elif key == ord('z'):  # 밥
        color_idx = 0
        pass
    elif key == ord('x'):  # 중앙 부식 (보통 우유)
        color_idx = 1
        pass
    elif key == ord('c'):  # 국
        color_idx = 2
        pass
    elif key == ord('a'):  # 왼쪽 반찬
        color_idx = 3
        pass
    elif key == ord('s'):  # 중앙 반찬 (윈쪽)
        color_idx = 4
        pass
    elif key == ord('d'):  # 중앙 반찬 (오른쪽)
        color_idx = 5
        pass
    elif key == ord('f'):  # 오른쪽 반찬
        color_idx = 6
        pass
    elif key == ord('g'):  # 식판에 걸쳐있는 부식
        color_idx = 7
        pass
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
