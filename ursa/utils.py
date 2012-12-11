#!/usr/bin/env python
#-*- coding:utf-8 -*-

import codecs
import urllib

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
    


def queryToDict(query):
    """
    
    Arguments:
    - `query`:
    """
    query = query.strip('&')
    query = query.split('&')
    data = {}
    for item in query:
        pairs = item.split('=')
        data[pairs[0]] = urllib.unquote_plus(pairs[1])

    return data
