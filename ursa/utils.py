#!/usr/bin/env python
#-*- coding:utf-8 -*-

import codecs
import urllib
import os
import shutil

import conf

def readfile(filename ):
    """
    
    Arguments:
    - `filename`:
    - `encoding`:
    """
    
    f = codecs.open(filename , 'r' , conf.getConfig()['encoding'])
    body = f.read()
    f.close()
                    
    return body
    
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
