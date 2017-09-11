# !/usr/bin/python
# coding=utf-8

import os
import imghdr
import json
from PIL import Image

global path
global arrImageData

####################变量设置区#################################
path = "/Users/yzq/Desktop/test"
####################变量设置区#################################

arrImageData = [];

def saveImageData(mPath):
    global arrImageData
    img  = Image.open(mPath)
    arrImageData.append({"path":mPath,"name":os.path.basename(mPath),"size":img.size})

def findImage(mPath):
    if os.path.isfile(mPath):
        fileType = imghdr.what(mPath)
        if (fileType == "png") or (fileType == "PNG") or (fileType == "jpg") or (fileType == "jpeg"):
            saveImageData(mPath)
    elif os.path.isdir(mPath):
        dirList = os.listdir(mPath)
        for item in dirList:
            tempPath = os.path.join(mPath,item)
            findImage(tempPath)

def generateJSFile(mArrImageData):
    if os.path.exists("./imageData.js"):
        os.remove("./imageData.js")
    f = open("./imageData.js", 'w')
    strJson = json.dumps({"data":mArrImageData})
    strDes = "var imageData = " + strJson
    # print strJson
    f.write(strDes)
    f.close()

def openIndexHtml():
    command = "open index.html"
    os.system(command)

def checkDepend():
    print "检查依赖库..."
    isHavePillow = False
    r = os.popen("pip freeze")
    x = r.readlines()
    for line in x:
        if line.startswith("Pillow="):
            isHavePillow = True
    if isHavePillow:
        print "依赖库存在"
    else:
        print "依赖库不存在，安装依赖库..."
        os.system("sudo pip install Pillow")
        print "依赖库安装完成"

def main():
    global path
    global arrImageData

    checkDepend()
    print "图片检索开始..."
    findImage(path)
    print "图片检索完毕，开始输出js文件..."
    generateJSFile(arrImageData)
    print "js文件输出完毕，打开页面"
    openIndexHtml()

main()