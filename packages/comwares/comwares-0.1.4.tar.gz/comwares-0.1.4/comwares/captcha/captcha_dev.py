import cv2.cv2 as cv2
import numpy as np
from matplotlib import pyplot as plt
from comwares import change_to_root_dir, recognize_captcha_in_line
import time
import os
from PIL import Image


def plot_in_grey_scale(img):
    plt.imshow(img, cmap='gray', interpolation='none')
    plt.show()


def load_img_in_gray_scale(img_filename, plot=False):
    img = cv2.imread(img_filename, 0)
    if plot:
        plot_in_grey_scale(img)
    return img


def to_threshold(img, res=127, to=255, mode=cv2.THRESH_BINARY, plot=False):
    res, thres = cv2.threshold(img, res, to, mode)
    if plot:
        plot_in_grey_scale(thres)
    return thres


def to_laplacian(img, plot=False):
    lap = cv2.Laplacian(img, cv2.CV_64F)
    if plot:
        plot_in_grey_scale(lap)
    return lap


def get_connections(img, plot=False):
    ret, labels = cv2.connectedComponents(img, connectivity=4)
    labels = labels * 50
    if plot:
        plot_in_grey_scale(img)
    return labels


def get_diff(img1, img2, plot=False):
    diff = img1 - img2 + 255
    if plot:
        plot_in_grey_scale(diff)
    return diff


def blur_img(img, size=3, plot=False):
    blur = cv2.blur(img, (size, size))
    if plot:
        plot_in_grey_scale(blur)
    return blur


def get_hist(img, plot=False):
    hist_full = cv2.calcHist([img], [0], None, [256], [0, 256])
    if plot:
        plot_in_grey_scale(hist_full)
    return hist_full


def plot_hist(img):
    plt.hist(img.ravel(), 256, [0, 256])
    plt.show()


def plot_binary(img, count_white=False, axis=0):

    pass


def hist_to_dict(hist):
    d = {}
    for key, value in enumerate(hist):
        d[key] = value[0]
    return d


def reverse_hist_dict(hist_dict):
    rd0 = {}
    for c, freq in hist_dict.items():
        if freq not in rd0.keys():
            rd0[freq] = [c]
        else:
            rd0[freq].append(c)
    rd1 = {}
    for k in reversed(sorted(rd0.keys())):
        rd1[k] = rd0[k]
    return rd1


def get_background_greyscale_color(img):
    h, w = img.shape
    pixels = h * w
    hist = get_hist(img)
    d = hist_to_dict(hist)
    rd = reverse_hist_dict(d)
    max_freq = list(rd.keys())[0]
    max_color = rd[max_freq][0]
    return max_color, max_freq / pixels


def process_img(filename, expected_length=4, plot_origin=True, plot_binary=False, plot_curve=False, plot_modified=True):
    img = load_img_in_gray_scale(filename)
    if plot_origin:
        plot_in_grey_scale(img)
        plot_hist(img)
    max_color, _ = get_background_greyscale_color(img)
    img_clean = to_threshold(img, 180, 255, mode=cv2.THRESH_BINARY, plot=plot_binary)
    img_curve = to_threshold(img, 127, 255, mode=cv2.THRESH_BINARY)
    img_curve_blur = blur_img(img_curve, size=5, plot=False)
    img_curve_binary = to_threshold(img_curve_blur, 200, 255, mode=cv2.THRESH_BINARY, plot=plot_curve)
    img_diff = get_diff(img_clean, img_curve_binary, plot=False)
    img_diff_blur = blur_img(img_diff, size=1, plot=False)
    img_diff_binary = to_threshold(img_diff_blur, 130, 255, mode=cv2.THRESH_BINARY, plot=plot_modified)
    plot_hist(img_curve_binary)
    im = Image.fromarray(img_diff_binary, mode='L')

    text_raw = recognize_captcha_in_line(img, only_numbers=True)
    text_origin = recognize_captcha_in_line(img_clean, only_numbers=True)
    text_modified = recognize_captcha_in_line(im, only_numbers=True)

    if len(text_raw) == expected_length:
        return text_raw
    elif len(text_origin) == expected_length:
        return text_origin
    elif len(text_modified) == expected_length:
        return text_modified
    else:
        return None


if __name__ == '__main__':
    change_to_root_dir('merchant')
    folder = 'tmp/captcha_imgs/'
    files = os.listdir(folder)
    for f in files:
        if '.png' in f:
            img_filename = folder + f
            print(img_filename)
            text = process_img(img_filename)
            print(text)
            time.sleep(2)
