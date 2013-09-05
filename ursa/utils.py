#!/usr/bin/env python
#-*- coding:utf-8 -*-

import codecs
import time
import urllib
import os
import shutil

import conf

def readfile(filename  , mode='r'):
    """
    
    Arguments:
    - `filename`:
    - `encoding`:
    """
    if 'b' in mode:#Binary file
        f = open( filename , mode )
    else:
        f = codecs.open(filename , mode , conf.getConfig()['encoding'])
    body = f.read()
    f.close()
                    
    return body

def writefile(filename , content):
    try:
        f = codecs.open(filename , 'w' , conf.getConfig()['encoding'])
        f.write(content)
        f.close()
    except:
        print filename,content
        raise
    
def copyfiles(sourceDir, targetDir):
    """拷贝文件夹
    
    Arguments:
    - `filename`:
    """
    for file in os.listdir(sourceDir): 
        sourceFile = os.path.join(sourceDir,  file) 
        targetFile = os.path.join(targetDir,  file) 
        if os.path.isfile(sourceFile): 
            if not os.path.exists(targetDir):  
                os.makedirs(targetDir)  
            if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):  
                open(targetFile, "wb").write(open(sourceFile, "rb").read()) 
        if os.path.isdir(sourceFile): 
            copyfiles(sourceFile, targetFile)    
    
def removefolder(target):
    """移出文件夹
    
    Arguments:
    - `folder`:
    """
    if os.path.exists(target):
        if os.path.isfile(target):
            os.remove(target)
        elif os.path.isdir(target):
            shutil.rmtree(target)

    return True
    
def createfolder(target):
    """
    
    Arguments:
    - `target`:
    """
    os.mkdir(target)


def queryToDict(query):
    """
    
    Arguments:
    - `query`:
    """
    query = query.strip('&')
    query = query.split('&')
    data = {}
    for item in query:
        pairs = item.split('=')
        data[pairs[0]] = urllib.unquote_plus(pairs[1])

    return data

def isyes(value):
    """判断是否为yes之类的词
    
    Arguments:
    - `value`:
    """
    return value.lower() in ['y' , 'yes' ]


def md5toInt(md5):
    """将md5得到的字符串变化为6位数字传回。
    基本算法是将得到的32位字符串切分成两部分，每部分按16进制得整数后除997，求得的余数相加
    最终得到6位
    
    Arguments:
    - `md5`:
    """
    md5 = [ md5[:16] , md5[16:] ]
    result = ''
    for item in md5:
        num = str( int( item , 16 ) % 997 ).zfill(3)
        result = result+num
        
    return result

def getDate():
    return time.strftime("%Y%m%d%S", time.localtime())
