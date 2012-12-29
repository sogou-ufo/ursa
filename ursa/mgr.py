#!/usr/bin/env python
#-*- coding:utf-8 -*-

import codecs
import os
import json

import utils
import conf
import uparser as parser


BASE = conf.getPath() + os.sep + '.data' + os.sep
SUFFIX = '.json'
COMMON_TOKEN = '.ursa'

def getRawData(token):
    """获取原始文件
    
    Arguments:
    - `token`:
    """
    fpath = BASE + token + SUFFIX
    if os.path.exists(fpath):
        return utils.readfile( fpath )
    else:
        return ''
    

def getData(token):
    """
    
    Arguments:
    - `token`:
    """
    data = getRawData(token)
    if len(data):
        data = json.loads(data)
    else:
        data = {}
    
    commonpath = BASE + COMMON_TOKEN + SUFFIX
    if os.path.exists(commonpath):
        commondata = json.loads( utils.readfile( commonpath ) )
    else:
        commondata = {}
    
    data.update(commondata)
    data.update({'_token':token})
    return data



def setData(token , data):
    """
    
    Arguments:
    - `token`:
    - `data`:
    """
    fpath = BASE + token + SUFFIX
    f = codecs.open(fpath , 'w' , conf.getConfig()['encoding'])
    f.write( json.dumps(data , sort_keys = True , indent = 4, separators = ( ',' , ': ')) )
    f.close()


def getPage(token):
    """获取mgr的页面
    
    Arguments:
    - `token`:
    """
    base = conf.getConfig()['base']
    mgrTpl = os.path.join( base , 'assets' , 'mgr' , 'index.html')

    body = parser.parseTpl(mgrTpl , {
            'name':token,
            'data': getRawData(token)
            } , True)

    return body
    
    
