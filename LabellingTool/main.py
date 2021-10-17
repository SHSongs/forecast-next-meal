import numpy as np
import cv2

oldx = oldy = -1

brush_size = 10

def on_mouse(event, x, y, flags, param):
    global oldx, oldy
    global brush_size

    if event == cv2.EVENT_LBUTTONDOWN:
        oldx, oldy = x, y
        print('EVENT_LBUTTONDOWN: %d, %d' % (x, y))  # 좌표 출력

    elif event == cv2.EVENT_LBUTTONUP:
        print('EVENT_LBUTTONUP: %d, %d' % (x, y))  # 좌표 출력

    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:  # ==를 쓰면 다른 키도 입력되었을 때 작동안하므로 &(and) 사용
            cv2.line(img, (oldx, oldy), (x, y), (0, 0, 255), brush_size, cv2.LINE_AA)
            cv2.imshow('image', img)
            oldx, oldy = x, y


# img = np.ones((480, 640, 3), dtype=np.uint8) * 255
img = cv2.imread("20210991.png")

cv2.namedWindow('image')

cv2.setMouseCallback('image', on_mouse, img)

cv2.imshow('image', img)

while True:

    key = cv2.waitKey()

    if key == ord('1'):
        brush_size -= 1
    elif key == ord('2'):
        brush_size += 1
    elif key == 27:  # esc
        break

cv2.destroyAllWindows()
