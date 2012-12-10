#!/usr/bin/env python
#-*- coding:utf-8 -*-

import codecs
import os

from jinja2 import Template

import conf
import utils
import json










def parse(token):
    """
    """
    tpl = conf.getPath() + '/template/' + token + '.tpl'
    dataFile = conf.getPath() + '/.data/' + token + '.json'

    if os.path.exists(tpl):
        
        body = Template(utils.readFile(tpl))
        if os.path.exists(dataFile):
            print 111
            data = json.loads(utils.readFile(dataFile))
        else:
            data = {}

        body = body.render(data)

        return body
    else:
        return ''
