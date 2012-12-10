#!/usr/bin/env python
#-*- coding:utf-8 -*-

import codecs

import conf

def readFile(filename ):
    """
    
    Arguments:
    - `filename`:
    - `encoding`:
    """
    
    f = codecs.open(filename , 'r' , conf.getConfig()['encoding'])
    body = f.read()
    f.close()
                    
    return body
    
