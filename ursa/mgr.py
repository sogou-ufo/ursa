#!/usr/bin/env python
#-*- coding:utf-8 -*-

import codecs
import os
import json

import utils
import conf
import uparser as parser

import re

BASE = conf.getPath() + os.sep + '_data' + os.sep
SUFFIX = '.json'
COMMON_TOKEN = '_ursa'

def dorepeat(data):
    if type(data)==type({}):
        for item in data.keys():
            dorepeat(data[item])
            if re.search( '@\d+$' , item ):
                name = item.split('@')[0]
                times = item.split('@')[1]
                
                if int(times):
                    for time in range(int(times)):
                        if not data.get(name):
                            data[name] = []
                        data[name].append(data[item])

        

def getRawData(token):
    """获取原始文件
    
    Arguments:
    - `token`:
    """
    fpath = BASE + token + SUFFIX
    if os.path.exists(fpath):
        data = utils.readfile( fpath )
    else:
        data = ''


    data = re.sub( '\/\*[\s\S]*?\*\/' , '' , data )
    return data

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

    dorepeat(data);
    
    commonpath = BASE + COMMON_TOKEN + SUFFIX
    if os.path.exists(commonpath):
        commondata = json.loads( utils.readfile( commonpath ) )
    else:
        commondata = {}
    
    data.update(commondata)
    
    multoken = token.split('/')

    data.update({'_token':token.replace('/','_')})
    data.update({'_folder':multoken[0]})
    data.update({'_subtoken':multoken[1] if len(multoken)>1 else ""})
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
    mgrTpl = os.path.join( base , 'assets' , 'mgr' , 'mgr.html')

    body = parser.parseTpl(mgrTpl , {
            'name':token,
            'data': getRawData(token)
            } , True)

    return body
    
def getIndex():
    base = conf.getConfig()['base']
    indexTpl = os.path.join( base , 'assets' , 'mgr' , 'index.html' )

    path = conf.getConfig()['path']
    
    tpls = []
    for dirpath , dirnames , filenames  in os.walk( os.path.join( path , 'template' ) ):
        for f in filenames:
            if f.endswith('.tpl'):
                tpldir = dirpath.replace( os.path.join( path , 'template' ) , '' )
                url = '/'.join( [ tpldir , f.replace('.tpl' , '') ] )
            tpls.extend([ url[1:] ])

    body = parser.parseTpl( indexTpl , {
            'tpls':tpls
            } , True )
    return body
