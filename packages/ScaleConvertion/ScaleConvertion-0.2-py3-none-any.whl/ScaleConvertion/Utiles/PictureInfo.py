# -*- coding: utf-8 -*-
# @Time    : 2023/4/9 14:38
# @Author  : qxcnwu
# @FileName: PictureInfo.py
# @Software: PyCharm
import math
import os
import shutil

import exifread
import numpy as np
from PIL import Image


def read_pic(pic_path):
    """
    get picture's altitude,width,heigh,channel
    :param pic_path:
    :return: altitude,w,h,c
    """
    # 图像原位信息
    high = None
    f = open(pic_path, 'rb')
    contents = exifread.process_file(f)
    for tag, value in contents.items():
        if tag == 'GPS GPSAltitude':
            high = round(float(eval(str(value))), 2)
            break
    f.close()

    if high == None:
        raise AssertionError(pic_path, " has no altitude information please check.")

    img = np.array(Image.open(pic_path)).astype(np.int)
    img_h, img_w, img_c = img.shape
    return high, img_h, img_w, img_c


def copy_image(path: str, dst: str) -> str:
    """
    copy img to tmp.jpg
    :param path:
    :return:
    """
    if not os.path.exists(dst):
        os.mkdir(dst)
    shutil.copy(path, os.path.join(dst, "tmp.jpg"))
    return os.path.join(dst, "tmp.jpg")
