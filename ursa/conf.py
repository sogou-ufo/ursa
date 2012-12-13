#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

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
    return globals()




if __name__ == '__main__':
    print getConfig()
