#!/usr/bin/env python
#-*- coding:utf-8 -*-

import codecs
import os
import json

import utils
import conf
import parser


BASE = conf.getPath() + os.sep + '.data' + os.sep
SUFFIX = '.json'


def getRawData(token):
    """获取原始文件
    
    Arguments:
    - `token`:
    """
    fpath = BASE + token + SUFFIX
    if os.path.exists(fpath):
        return utils.readFile( fpath )
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
    mgrTpl = base + os.sep + os.sep.join(['assets' , 'mgr' , 'index.html'])

    body = parser.parse(mgrTpl , {
            'name':token,
            'data': getRawData(token)
            } , True)

    return body
    
    
