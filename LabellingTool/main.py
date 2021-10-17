import numpy as np
import cv2
import os

img_path = 'input'
file_list = os.listdir(img_path)
img_files = [file for file in file_list if file.endswith('.png')]
img_files.sort()


def on_mouse(event, x, y, flags, param):
    global oldx, oldy
    global brush_size
    global dst

    if event == cv2.EVENT_LBUTTONDOWN:
        oldx, oldy = x, y
        print('EVENT_LBUTTONDOWN: %d, %d' % (x, y))  # 좌표 출력

    elif event == cv2.EVENT_LBUTTONUP:
        print('EVENT_LBUTTONUP: %d, %d' % (x, y))  # 좌표 출력

    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:  # ==를 쓰면 다른 키도 입력되었을 때 작동안하므로 &(and) 사용
            cv2.line(label, (oldx, oldy), (x, y), (0, 0, 255), brush_size, cv2.LINE_AA)
            dst = cv2.addWeighted(img, 0.7, label, 0.3, 0)
            cv2.imshow('image', dst)
            oldx, oldy = x, y


oldx = oldy = -1

brush_size = 10

img_index = 0


dst = None

img = cv2.imread(os.path.join(img_path, img_files[img_index]))

y, x, c = img.shape
label = np.zeros((y, x, c), dtype=np.uint8)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)  # 창 크기 수동 조절
cv2.moveWindow(winname='image', x=50,y=50)

cv2.setMouseCallback('image', on_mouse, img)
cv2.imshow('image', img)

cv2.resizeWindow(winname='image', width=1000, height=1000)

show_label = False

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

    keyEx = cv2.waitKeyEx()
    print(keyEx)
    if keyEx == 63235:  # left arrow
        img_index -= 1
        img = cv2.imread(os.path.join(img_path, img_files[img_index]))
        cv2.imshow('image', img)
        print('left')
        y, x, c = img.shape
        label = np.zeros((y, x, c), dtype=np.uint8)

    elif keyEx == 63234:  # right arrow
        img_index += 1
        img = cv2.imread(os.path.join(img_path, img_files[img_index]))
        cv2.imshow('image', img)
        print('right')
        y, x, c = img.shape
        label = np.zeros((y, x, c), dtype=np.uint8)


cv2.destroyAllWindows()
