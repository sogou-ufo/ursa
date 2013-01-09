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



jinjaenv = Environment( loader=FileSystemLoader( os.path.join( conf.getConfig()['path'], conf.getConfig()['template_dir']) ,  conf.getConfig()['encoding']) )
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
    return body


def getFileTimeStamp(fpath):
    """为文件加上时间戳并返回
    
    Arguments:
    - `fpath`:
    """
    fpath = conf.getConfig()['path'] + fpath  #may cause problem in windows
    if os.path.exists( fpath ):
        f = utils.readfile(fpath , 'rb')
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
        if not ftype in ['html' , 'htm' , 'css' , 'js' , 'tpl']:
            return False
        content = utils.readfile( filepath )

    TM_TOKEN = '@tm:(.*?)@'
    COMMON_TOKEN = '@(.*?)@'

    iters = re.finditer( TM_TOKEN , content )
    for i in reversed(list(iters)):
        content = content[0:i.start(0)] + getFileTimeStamp(i.group(1)) + content[i.end(0):]

    iters = re.finditer( COMMON_TOKEN , content )
    for i in reversed(list(iters)):
        config = conf.getConfig()
        name = i.group(1)
        value = config.get(name) or config[token].get(name)
        if value:
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

    static_prefix = conf.getConfig()['static_prefix']

    iters = re.finditer( LINK_TOKEN , tpl )
    for i in reversed(list(iters)):
        path = i.group(1)
        if not path.startswith('http'):
            tpl =  tpl[0:i.start(1)] + static_prefix + i.group(1) + '?t=' + getFileTimeStamp( i.group(1) ) + tpl[i.end(1):]

    iters = re.finditer( SCRIPT_TOKEN , tpl )
    for i in reversed(list(iters)):
        path = i.group(1)
        if not path.startswith('http'):
            tpl =  tpl[0:i.start(1)] + static_prefix + '?t=' + getFileTimeStamp( i.group(1) ) + tpl[i.end(1):]



    return tpl


def compileCss(filepath):
    if not os.path.exists(filepath):
        return False
    css = utils.readfile( filepath )
    
    IMG_TOKEN = 'url\([\'"]?(.*?)[\'"]?\)'
    iters = re.finditer( IMG_TOKEN , css )
    for i in reversed(list(iters)):
        imgpath = i.group(1)
        if not imgpath.startswith('http'):
            css = css[0:i.end(0)-1] + '?t=' + getFileTimeStamp( '/static/css/' + i.group(1)) + css[i.end(0)-1:]

    return css
    
    

