#!/user/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
from ssd import SSD
import os

ssd = SSD()


def predict_img():
    while True:
        img = input('Input image filename:')
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            r_image = ssd.detect_image(image)
            r_image.show()


def predict_image(img, index):
    image = Image.open(img)
    result = ssd.detect_image(image)
    result.save("img_output/" + str(index) + ".jpg")


def getFileList(dir, Filelist, ext=None):
    """
        获取文件夹及其子文件夹中文件列表
        输入 dir：文件夹根目录
        输入 ext: 扩展名
        返回： 文件路径列表
        """
    newDir = dir
    if os.path.isfile(dir):
        if ext is None:
            Filelist.append(dir)
        else:
            if ext in dir[-3:]:
                Filelist.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            getFileList(newDir, Filelist, ext)
    return Filelist


org_img_folder = "img/"

if __name__ == "__main__":
    # 检索文件
    imglist = getFileList(org_img_folder, [], 'jpg')
    print('本次执行检索到 ' + str(len(imglist)) + ' 张图像\n')

    index = 0

    for img in imglist:
        predict_image(img, index)
        index += 1


