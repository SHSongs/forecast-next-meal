

def crop_img(img):
    y, x, c = img.shape

    left_x = int((x - 200) / 2)
    up_y = int((y - 150) / 2)

    img = img[up_y:up_y + 150, left_x:left_x + 200]

    y, x, c = img.shape

    print(x, y)
    assert x == 200 and y == 150

    return img