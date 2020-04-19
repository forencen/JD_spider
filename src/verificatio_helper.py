import random

import cv2
import numpy as np


def ease_out_quad(x):
    return 1 - (1 - x) * (1 - x)


def ease_out_quart(x):
    return 1 - pow(1 - x, 4)


def ease_out_expo(x):
    if x == 1:
        return 1
    else:
        return 1 - pow(2, -10 * x)


def get_tracks(distance, seconds, ease_func):
    tracks = [0]
    offsets = [0]
    for t in np.arange(0.0, seconds, 0.1):
        ease = globals()[ease_func]
        offset = round(ease(t / seconds) * distance)
        tracks.append(offset - offsets[-1])
        offsets.append(offset)
    return offsets, tracks


def swipe(distance):
    # 移动间隙
    tracks = []
    offset = 45
    # 减速标示
    turn_dis = distance * 2 / 3
    t = 0.1
    # 初速度 为 0
    v = 0
    while offset < distance:
        if offset < turn_dis:
            a = random.randint(100, 105)
        else:
            a = random.randint(20, 30)
        # 计算加速度和速度
        v0 = v
        # 当前时刻速度
        v = v0 + a * t
        move_dis = v0 * t + 1 / 2 * a * t
        offset += move_dis
        tracks.append(round(move_dis, 2))
    return tracks


def find_pic(target, template):
    """
    找出图像中最佳匹配位置
    :param target: 目标即背景图
    :param template: 模板即需要找到的图
    :return: 返回最佳匹配及其最差匹配和对应的坐标
    """
    target_rgb = cv2.imread(target)
    target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
    template_rgb = cv2.imread(template, 0)

    # template_rgb = cv2.adaptiveThreshold(template_rgb, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 5)
    # adaptive_template_gray = handle_template(gaussian_template)

    res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
    value = cv2.minMaxLoc(res)
    h, w = template_rgb.shape
    top_left = (value[2:][0][0], value[2:][0][1])
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(target_rgb, top_left, bottom_right, (222, 100, 35), 4)
    cv2.imshow('adaptive_image_gray', target_gray)
    cv2.imshow('adaptive_template_gray', template_rgb)
    cv2.imshow('original', target_rgb)
    print(top_left[0])
    cv2.waitKey(0)

    return top_left


if __name__ == '__main__':
    find_pic('../captcha/bg_1587310345.png', '../captcha/template_1587310345.png')
    # get_tracks(117, 12, 'ease_out_expo')
