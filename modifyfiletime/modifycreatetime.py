#!/usr/bin/env python
# _*_coding:utf-8 _*_
# 本脚本用于windows下的文件的创建时间修改时间和接入时间的修改
# depend on  win32file install with "pip install pywin32"

import os
from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time
import time
 
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files  # 当前路径下所有非目录子文件
        
def timeOffsetAndStruct(times,format,offset):
    return time.localtime(time.mktime(time.strptime(times, format)) + offset)

def modifyFileTime(filePath,createTime,modifyTime,accessTime,offset):
    """
    用来修改任意文件的相关时间属性，时间格式：YYYY-MM-DD HH:MM:SS 例如：2019-02-02 00:01:02
    :param filePath: 文件路径名
    :param createTime: 创建时间
    :param modifyTime: 修改时间
    :param accessTime: 访问时间
    :param offset: 时间偏移的秒数,tuple格式，顺序和参数时间对应
    """
    try:
        format = "%Y-%m-%d %H:%M:%S" #时间格式
        cTime_t = timeOffsetAndStruct(createTime,format,offset[0])
        mTime_t = timeOffsetAndStruct(modifyTime,format,offset[1])
        aTime_t = timeOffsetAndStruct(accessTime,format,offset[2])
 
        fh = CreateFile(filePath, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        createTimes, accessTimes, modifyTimes = GetFileTime(fh)
 
        createTimes = Time(time.mktime(cTime_t))
        accessTimes = Time(time.mktime(aTime_t))
        modifyTimes = Time(time.mktime(mTime_t))
        SetFileTime(fh, createTimes, accessTimes, modifyTimes)
        CloseHandle(fh)
        return 0
    except:
        return 1

if __name__ == "__main__":
    l = file_name("./")
    cTime = "2020-12-29 00:01:02" # 创建时间
    mTime = "2019-02-02 00:01:03" # 修改时间
    aTime = "2019-02-02 00:01:04" # 访问时间
    offset = (0,1,2) 
    for i in l:
        modifyFileTime(i,cTime,mTime,aTime,offset)