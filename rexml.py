import os
import xml.etree.ElementTree as ET
import glob


# 重命名xml与图片文件函数
def rename(xmldir, imgdir, outdir):
    # 获取图片文件列表
    os.chdir(imgdir)
    imgs = os.listdir('.')
    imgs = glob.glob(str(imgs) + '*.jpg')

    # 获取xml文件列表
    os.chdir(xmldir)
    annotations = os.listdir('.')
    annotations = glob.glob(str(annotations) + '*.xml')

    labels = ['mask', 'face', 'mask_chin', 'mask_mouth_chin']  # 标签名
    nums = [1, 1, 1, 1, 1]  # 每一类标签对应的图片数量，最后一个代表混合标签mix，即一张图片中有多种标签对应的目标

    for i, file in enumerate(annotations):  # 遍历xml文件列表
        # actual parsing
        in_file = open(file, encoding='utf-8')  # 打开xml文件
        tree = ET.parse(in_file)
        root = tree.getroot()

        lastCla = -1  # 遍历标签时的前一个标签
        isSingle = 1  # 文件所含标签是否单一，初始化为1（代表标签单一）

        for obj in root.iter('object'):  # 遍历当前xml文件中的所有标签
            name = obj.find('name').text  # 获得标签名称
            if name == "mask":
                cla = 0
            elif name == "face":
                cla = 1
            elif name == "mask_chin":
                cla = 2
            elif name == 'mask_mouth_chin':
                cla = 3

            if lastCla == -1:
                lastCla = cla  # 如果是第一次遍历，则将cla赋值给lastCla
            elif lastCla != cla:  # 如果上一次遍历的标签与这次遍历的标签不同
                isSingle = 0  # 说明该文件包含的标签种类不是单一的
                break

        in_file.close()  # 关闭xml文件

        name = ""
        if isSingle == 1:  # 如果文件标签单一
            name = str(lastCla) + "_" + labels[lastCla] + "_" + str(nums[lastCla])
            nums[lastCla] = nums[lastCla] + 1  # 标签对应的文件数量+1
        else:  # 如果文件标签不单一
            name = "4_mix_" + str(nums[4])
            nums[4] = nums[4] + 1  # mix标签的文件数量+1

        # 重命名xml文件
        old_xml = os.path.join(os.path.abspath(xmldir), file)  # 原xml路径 + 文件名
        new_xml = os.path.join(os.path.abspath(outdir), name + ".xml")  # 新xml路径 + 文件名
        os.rename(old_xml, new_xml)

        # 重命名jpg文件
        old_img = os.path.join(os.path.abspath(imgdir), file.split('.')[0] + '.jpg')  # 原jpg路径 + 文件名
        new_img = os.path.join(os.path.abspath(outdir), name + ".jpg")  # 新jpg路径 + 文件名
        os.rename(old_img, new_img)


xmldir = 'G:/1/xml/'  # xml文件所在目录
imgdir = 'G:/1/img/'  # 图片文件所在目录
outdir = 'G:/1/rename/'  # 保存目录（本代码将重命名后的xml文件与图片文件保存在同一文件夹下，亦可修改代码保存在不同的文件夹下）

rename(xmldir, imgdir, outdir)  # 调用函数进行重命名
