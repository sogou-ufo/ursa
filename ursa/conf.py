#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import json

import utils
import log

path = os.getcwd()
encoding = 'utf-8'
base = os.path.abspath(os.path.dirname(__file__)) 


template_dir = 'template'
static_prefix = ''








def getPath():
    """
    """
    return path


def getConfig():
    """
    """
    conf = globals().copy()
    conffile = os.path.join(path , 'manifest.json')
    if os.path.exists(conffile):
        try:
            f = open(conffile)
            body = f.read()
            f.close()
            conf.update( json.loads( body ) )
        except ValueError:
            log.error('Your format of manifest.json is wrong.')
        except:
            raise
    return conf




if __name__ == '__main__':
    print getConfig()
