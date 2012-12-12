#!/usr/bin/env python
#-*- coding:utf-8 -*-

import codecs
import os

from jinja2 import Template,Environment,FileSystemLoader,TemplateNotFound

import conf
import utils
import json



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
