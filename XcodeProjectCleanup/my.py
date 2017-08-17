# !/usr/bin/python
# coding=utf-8

from biplist import *
import os

global rootObjects
global rootArr
global plistPath

####################变量设置区#################################
rootPath= "/Users/yzq/Desktop/dfc_v3/dfc_v2"
projectFilePath = "/Users/yzq/Desktop/dfc_v3/dfc_v2.xcodeproj"
plistPath = "/Users/yzq/Desktop/123.plist"
##############################################################

def checkfile(filePath,filekey):
    global rootObjects

    dic = rootObjects[filekey]
    # print(filekey) 

    strPath = ""
    if "path" in dic:
        strPath = dic["path"]
    else:
        strPath = dic["name"]

    path = filePath + "/" + strPath
    if "children" in dic:
        if len(dic["children"]) < 1:
            print("空文件夹"+"------"+path)
        else:
            for item in dic["children"]:
                checkfile(path,item)
    else:
        if os.path.exists(path) == False:
            print("文件不存在"+path)
            

def startCheckFile(mRootPath):
    global rootObjects
    global plistPath

    plist = readPlist(plistPath)
    rootObjects = plist["objects"]

    for dic in rootObjects.values():
        if ("name" in dic) and dic["name"] == "dfc_v3":
            rootArr = dic["children"]
            break
        
    print(rootArr)

    for item in rootArr:
        print("开始检查item"+item+"-------------------------------")
        checkfile(mRootPath,item)


def checkFileIsInProject(mPlistObject, mFileName, mFilePath):
    for item in mPlistObject.values():
        if (("path" in item) and (item["path"] == mFileName)) or (("name" in item) and (item["name"] == mFileName)):
            # print("发现文件引用"+mFileName)
            return
    print("未发现文件应用："+mFileName)
    print(mFilePath)


def checkProject(mPlistObject, mFilePath):
    dirList = os.listdir(mFilePath)
    for item in dirList:
        itemPath = os.path.join(mFilePath,item)
        if os.path.isfile(itemPath):
            checkFileIsInProject(mPlistObject,item,itemPath)
        elif os.path.isdir(itemPath):
            checkProject(mPlistObject,itemPath)
        else:
            print("当前路径出错:"+itemPath)


def startCheckProject(mRootPath):
    global plistPath

    plist = readPlist(plistPath)
    rootObjects = plist["objects"]

    checkProject(rootObjects,mRootPath)
    

def getPlist(mProjectFilePath,mPlistPath):
    command = "rm -rf "+mPlistPath
    os.system(command)
    command = "value=`plutil -convert xml1 -o - "+mProjectFilePath+"/project.pbxproj` && echo $value >"+mPlistPath
    os.system(command)
    print("生成plist文件:"+mPlistPath)


print("这是一个帮你检查工程文件的脚本，请输入以下数字选项执行")
print("0.准备工作")
print("1.检查工程列表当中的文件是否在对应的物理位置")
print("2.检查工程当中是否有文件未加入引用")
choice = input("请输入:")
if choice == "0":
    print("请设置脚本rootPath、projectFilePath、plistPath三个变量的路径值")
    print("rootPath：工程根目录，dfc_v2的那个文件夹目录")
    print("projectFilePath：工程文件目录,dfc_v2.xcodeproj文件目录")
    print("plistPath：生成plist文件所在位置，该位置任意，具备读写权限即可")
elif choice == "1":
    getPlist(projectFilePath,plistPath)
    startCheckFile(rootPath)
elif choice == "2":
    getPlist(projectFilePath,plistPath)
    startCheckProject(rootPath)
else:
    print("未输入正确的操作")