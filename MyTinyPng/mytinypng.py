#!/usr/bin/python
# coding=utf-8

import os
import imghdr
import tinify

mydir = "/Users/yzq/Desktop/image"
apiKey = "38t2hJ6I2_x9nmuWTn9N5km0oKpnTV4o"
imageCout = 0

#查找文件夹下图片的数量
def imageCount(tempdir):

    global imageCout

    dirList = os.listdir(tempdir)

    for item in dirList:
        tempItem = os.path.join(tempdir,item)
        if os.path.isfile(tempItem):
            fileType = imghdr.what(tempItem)
            if (fileType == "png") or (fileType == "PNG") or (fileType == "jpg") or (fileType == "jpeg"):
                imageCout+=1
        elif os.path.isdir(tempItem):
            imageCount(tempItem)
        else:
            print "当前路径出现异常"
    return

def imageCompress(tempdir):
    global imageCout
    global apiKey

    dirList = os.listdir(tempdir)

    for item in dirList:
        tempItem = os.path.join(tempdir, item)
        if os.path.isfile(tempItem):
            fileType = imghdr.what(tempItem)
            if (fileType == "png") or (fileType == "PNG") or (fileType == "jpg") or (fileType == "jpeg"):
                tinify.key = apiKey
                source = tinify.from_file(tempItem)
                source.to_file(tempItem)
                print "压缩%s成功" % tempItem
        elif os.path.isdir(tempItem):
            imageCompress(tempItem)
        else:
            print "当前路径出现异常"
    return

def mainClass():

    global imageCout

    print "以下是图片压缩选项，请选择"
    print "1.查看当前文件夹下图片数量"
    print "2.压缩改文件夹下的图片"
    strInput = raw_input("请输入你的选项")

    if strInput == "1":
        imageCount(mydir)
        print "共有%d张图片" % imageCout
    elif strInput == "2":
        imageCompress(mydir)
    else:
        print "退出啦"


mainClass()
