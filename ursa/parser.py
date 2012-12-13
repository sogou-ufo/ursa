#!/usr/bin/env python
#-*- coding:utf-8 -*-

import codecs
import os
import json
from bs4 import BeautifulSoup
import hashlib
import re

from jinja2 import Template,Environment,FileSystemLoader,TemplateNotFound

import conf
import utils
import log


import mgr



jinjaenv = Environment( loader=FileSystemLoader( os.path.join( conf.getConfig()['path'], conf.getConfig()['template_dir']) ,  conf.getConfig()['encoding']) )


def parseTpl(token , data={} , noGetTpl = False):
    """
    """
    if not noGetTpl:
        tpl = token + '.tpl'
        dataFile = conf.getPath() + '/.data/' + token + '.json'
    else:
        tpl = token


    if not noGetTpl:
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


def compileCommon(content):
    """通用编译方法
    编译 @tm:file_path@为6位时间戳
    
    Arguments:
    - `content`:
    """
    TM_TOKEN = '@tm:(.*)@'

    iters = re.finditer( TM_TOKEN , content )
    for i in reversed(list(iters)):
        content = content[0:i.start(0)] + getFileTimeStamp(i.group(1)) + content[i.end(0):]
    return content

def compileHTML(filepath):
    """编译html文件
    
    Arguments:
    - `filepath`:
    """
    if not os.path.exists(filepath):
        return False
    tpl = utils.readfile( filepath )

    log.log( 'Compile for '+ filepath + '.' )
    tpl = BeautifulSoup(tpl)

    links = tpl.find_all('link')
    scripts = tpl.find_all('script')

    static_prefix = conf.getConfig()['static_prefix']
    for link in links:
        if link['rel'] and 'stylesheet' in link['rel']:
            link['href'] = static_prefix + link['href'] + '?t=' + getFileTimeStamp(link['href'])
    for script in scripts:
        if 'src' in script and not script['src'].startswith('http'):
            script['src'] = static_prefix + script['src'] + '?t=' + getFileTimeStamp(script['src'])

            
    tpl = tpl.prettify(formatter=None) # can set str(tpl) if need html minify
    tpl = compileCommon(tpl)
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
            print css

    css = compileCommon(css)
    return css
    
    

