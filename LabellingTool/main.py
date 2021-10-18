import numpy as np
import cv2
import os

IMG_PATH = 'input'
LABEL_PATH = 'label'

file_list = os.listdir(IMG_PATH)
img_files = [file for file in file_list if file.endswith('.png')]
img_files.sort()
print(img_files)


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
            cv2.line(label, (oldx, oldy), (x, y), (0, 0, 255), brush_size, cv2.LINE_AA)
            dst = cv2.addWeighted(img, 0.7, label, 0.3, 0)
            cv2.imshow('image', dst)
            oldx, oldy = x, y

        if flags & cv2.EVENT_FLAG_RBUTTON:  # ==를 쓰면 다른 키도 입력되었을 때 작동안하므로 &(and) 사용
            cv2.line(label, (oldx, oldy), (x, y), (0, 0, 0), brush_size, cv2.LINE_AA)
            dst = cv2.addWeighted(img, 0.7, label, 0.3, 0)
            cv2.imshow('image', dst)
            oldx, oldy = x, y


oldx = oldy = -1

brush_size = 10

img_index = 0

dst = None


def crab_img(img):
    y, x, c = img.shape

    left_x = int((x - 200) / 2)
    up_y = int((y - 150) / 2)

    img = img[up_y:up_y + 150, left_x:left_x + 200]

    y, x, c = img.shape

    print(x, y)
    assert x == 200 and y == 150

    return img


img = cv2.imread(os.path.join(IMG_PATH, img_files[img_index]))
img = crab_img(img)

y, x, c = img.shape

label = np.zeros((y, x, c), dtype=np.uint8)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)  # 창 크기 수동 조절
cv2.moveWindow(winname='image', x=50, y=50)

cv2.setMouseCallback('image', on_mouse, img)
cv2.imshow('image', img)

cv2.resizeWindow(winname='image', width=1000, height=1000)

show_label = False


def next_img(n):
    global label
    global img
    global img_index

    print(img_files[img_index])
    cv2.imwrite(os.path.join(LABEL_PATH, img_files[img_index]), label)

    img_index += n

    img = cv2.imread(os.path.join(IMG_PATH, img_files[img_index]))
    img = crab_img(img)

    cv2.imshow('image', img)
    y, x, c = img.shape

    if os.path.isfile(os.path.join(LABEL_PATH, img_files[img_index])):  # label file 존재시 label 불옴옴
        label = cv2.imread(os.path.join(LABEL_PATH, img_files[img_index]))
        dst = cv2.addWeighted(img, 0.7, label, 0.3, 0)
        cv2.imshow('image', dst)
    else:
        label = np.zeros((y, x, c), dtype=np.uint8)


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
