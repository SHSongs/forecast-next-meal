import numpy as np
import matplotlib.pyplot as plt

fn_tonumpy = lambda x: x.to('cpu').detach().numpy().transpose(0, 2, 3, 1)
fn_denorm = lambda x, mean, std: (x * std) + mean


def show_tensor_img(img):
    img = fn_tonumpy(fn_denorm(img, mean=0.5, std=0.5))
    img = np.clip(img, a_min=0, a_max=1)
    plt.imshow(img[0])
    plt.show()

    return img
