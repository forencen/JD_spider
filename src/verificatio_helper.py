import cv2
import numpy as np
import math


def swipe():
    pass


def template_match(original_image, template_ori):
    # Convert to grayscale
    image_gray = cv2.cvtColor(cv2.GaussianBlur(original_image, (3, 3), 0), cv2.COLOR_BGR2GRAY)
    gaussian_template = cv2.cvtColor(cv2.GaussianBlur(template_ori, (3, 3), 0), cv2.COLOR_BGR2GRAY)
    # template_gray = handle_template(template_ori)
    # ret, image_gray = cv2.threshold(image_gray, 127, 255, cv2.THRESH_BINARY)
    # 阈值二值化
    adaptive_image_gray = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25,
                                                5)
    adaptive_template_gray = handle_template(gaussian_template)

    # assign width and height of template in w and h
    h, w = gaussian_template.shape
    # Perform match operations.
    res = cv2.matchTemplate(adaptive_image_gray, adaptive_template_gray, cv2.TM_SQDIFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(original_image, top_left, bottom_right, (222, 100, 35), 4)

    cv2.imshow('adaptive_image_gray', adaptive_image_gray)
    cv2.imshow('adaptive_template_gray', adaptive_template_gray)
    cv2.imshow('original', original_image)
    cv2.waitKey(0)


def cut_template(img):
    _, thresh = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)

    crop = img[y:y + h, x:x + w]
    return crop
    # cv2.imwrite('../resources/template.png', crop)


def handle_template(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    width, heigth = image.shape
    for h in range(heigth):
        for w in range(width):
            if image[w, h] == 0:
                image[w, h] = 96
    # cv.imshow('gray', gray)
    binary = cv2.inRange(gray, 96, 96)
    res = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)  # 开运算去除白色噪点
    # cv.imshow('res', res)
    return res


def match(target, template):
    img_rgb = cv2.imread(target)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template, 0)
    run = 1
    w, h = template.shape[::-1]
    print(w, h)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # 使用二分法查找阈值的精确值
    L = 0
    R = 1
    while run < 20:
        run += 1
        threshold = (R + L) / 2
        print(threshold)
        if threshold < 0:
            print('Error')
            return None
        loc = np.where(res >= threshold)
        print(len(loc[1]))
        if len(loc[1]) > 1:
            L += (R - L) / 2
        elif len(loc[1]) == 1:
            print('目标区域起点x坐标为：%d' % loc[1][0])
            break
        elif len(loc[1]) < 1:
            R -= (R - L) / 2

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7, 279, 151), 2)
    cv2.imshow('Dectected', img_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return loc[1][0]


if __name__ == '__main__':
    image_full = cv2.imread('../resources/WechatIMG27.png')
    image_item = cv2.imread('../resources/WechatIMG26.png')
    template_match(image_full, image_item)
    # match('../resources/WechatIMG26.png', '../resources/WechatIMG27.png')
    # image_gray = cv2.cvtColor(cv2.GaussianBlur(image_full, (3, 3), 0), cv2.COLOR_BGR2GRAY)
    # ret, image_gray = cv2.threshold(image_gray, 127, 255, cv2.THRESH_BINARY)
    # cv2.imshow('original', image_gray)
    # cv2.waitKey(0)


