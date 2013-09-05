#!/usr/bin/env python
#-*- coding:utf-8 -*-

import codecs
import os
import json
import hashlib
import re

from jinja2 import Template,Environment,FileSystemLoader,TemplateNotFound

import conf
import utils
import log


import mgr


range_item = 0

jinjaenv = Environment( loader=FileSystemLoader( os.path.join( conf.getConfig()['path'], conf.getConfig()['template_dir']) ,  conf.getConfig()['encoding']) , extensions=["jinja2.ext.do"] , autoescape=True )
build_jinjaenv = Environment( loader=FileSystemLoader( os.path.join( conf.getConfig()['path'] , 'build', conf.getConfig()['template_dir']) ,  conf.getConfig()['encoding']) )


def parseTpl(token , data={} , noGetTpl = False , isbuild = False):
    """
    """
    if not noGetTpl:
        tpl = token + '.tpl'
    else:
        tpl = token


    if not noGetTpl:
        if isbuild:
            body = build_jinjaenv.get_template(tpl)
        else:
            body = jinjaenv.get_template(tpl)
    elif os.path.exists(tpl):
        body = Template(utils.readfile(tpl))
    else:
        return ''
    
    if not len(data) :
        data = mgr.getData(token)
    try:    
        body = body.render(data)
    except TemplateNotFound as e:
        return 'Template %s not found' % (str(e) ,)
    except Exception as e:
        print e
        return ''
    return body


def getFileTimeStamp(fpath,parentpath=''):
    """为文件加上时间戳并返回
    
    Arguments:
    - `fpath`:
    """
    if fpath.find('/') == 0:
        fpath = fpath[1:]
    fpath2 = os.path.join(conf.getConfig()['path'] , 'build' , fpath)  
    if not os.path.exists( fpath2 ) and parentpath:
        parentpath = parentpath.split('/')
        parentpath.pop()
        fpath2 = '/'.join(parentpath) + '/' + fpath

    if os.path.exists( fpath2 ):
        f = utils.readfile(fpath2 , 'rb')
        m = hashlib.md5()
        m.update(f)
        md5 = utils.md5toInt(m.hexdigest())
        return md5
    return ''


def compileCommon(filepath , token , force=False):
    """通用编译方法
    编译 @tm:file_path@为6位时间戳
    
    Arguments:
    - `content`:
    """
    if force:
        content = filepath
    else:
        if not os.path.exists(filepath):
            return False
        ftype = filepath.split('.')[-1]
        if not ftype in ['html' , 'htm' , 'css' , 'js' , 'tpl' , 'jsp']:
            return False
        content = utils.readfile( filepath )
    TM_TOKEN = '@tm:(.*?)@'
    DATE_TOKEN = '@date@';
    COMMON_TOKEN = '@(.*?)@'
    

    iters = re.finditer( TM_TOKEN , content )
    for i in reversed(list(iters)):
        content = content[0:i.start(0)] + getFileTimeStamp(i.group(1) , filepath) + content[i.end(0):]

    iters = re.finditer( DATE_TOKEN , content )
    for i in reversed(list(iters)):
        content = content[0:i.start(0)] + utils.getDate()  + content[i.end(0):]

    iters = re.finditer( COMMON_TOKEN , content )

    for i in reversed(list(iters)):
        config = conf.getConfig()
        name = i.group(1)
        value = ( token and config[token].get(name)) or config.get(name) 
        if value:
            if value.find('{num}') != -1:
                num = ( token and config[token].get('num')) or config.get('num') or '10'
                num = range(num+1)
                substr100 = content[i.end(0):i.end(0)+100]
                istimestamp = substr100.find('t=')
                if istimestamp != -1:#has timestamp
                    try:
                        tm = int(substr100[istimestamp+2:istimestamp+3])
                    except ValueError:
                        continue
                    if tm >= len(num):
                        tm = tm - len(num)
                    value = value.replace( '{num}' , str(tm) )
                else:
                    global range_item
                    value = value.replace( '{num}' , str(num[range_item]) )
                    range_item = range_item + 1
                    if range_item >= len(num):
                        range_item = 0
            content = content[0:i.start(0)] + value + content[i.end(0):]
            

    return content

def compileHTML(filepath , needCompress):
    """编译html文件
    
    Arguments:
    - `filepath`:
    """
    if not os.path.exists(filepath):
        return False
    tpl = utils.readfile( filepath )

    log.log( 'Compile for '+ filepath + '.' )

    LINK_TOKEN = '<link.* href=[\'"](.*?\.css)[\'"]'
    SCRIPT_TOKEN = '<script.* src=[\'"](.*?\.js)[\'"]'

    iters = re.finditer( LINK_TOKEN , tpl )
    for i in reversed(list(iters)):
        path = i.group(1)
        path = compileCommon(path , 'local' , True) #内部可能有替换的变量
        if not path.startswith('http') and not conf.getConfig().get('disableAutoTimestamp'):
            tpl =  tpl[0:i.start(1)] +  i.group(1) + '?t=' + getFileTimeStamp( path , filepath ) + tpl[i.end(1):]

    iters = re.finditer( SCRIPT_TOKEN , tpl )
    for i in reversed(list(iters)):
        path = i.group(1)
        path = compileCommon(path , 'local' , True) #内部可能有替换的变量
        if not path.startswith('http') and not conf.getConfig().get('disableAutoTimestamp'):
            tpl =  tpl[0:i.start(1)] +  i.group(1) + '?t=' + getFileTimeStamp( path , filepath ) + tpl[i.end(1):]



    return tpl


def compileCss(filepath):
    if not os.path.exists(filepath):
        return False
    css = utils.readfile( filepath )
    
    IMG_TOKEN = 'url\([\'"]?(.*?)[\'"]?\)'
    iters = re.finditer( IMG_TOKEN , css )
    for i in reversed(list(iters)):
        imgpath = i.group(1)
        imgpath = compileCommon(imgpath , 'local' , True) #内部可能有替换的变量
        if not imgpath.startswith('http') and not conf.getConfig().get('disableAutoTimestamp'):
            css = css[0:i.end(0)-1] + '?t=' + getFileTimeStamp( imgpath , filepath ) + css[i.end(0)-1:]

    return css
    
    

def compilePlugin(name,content):
    plugins = conf.getConfig().get('serverplugins')
    if not plugins:
        return content

    for plugin in plugins:
        try:
            pkg = __import__( plugin , globals() , locals() , ['main'] , -1 )
            content= pkg.main(name,content)
        except Exception as e:
            print "Plugin " + plugin + " is invalid"
            print e
            content = content

    return content
    
    
