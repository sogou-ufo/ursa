#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os


import utils
import conf
import log

BUILD_DIR = 'build'
PATH = conf.getConfig()['path'] 
RJSPATH = os.path.join(conf.getConfig()['base'] , 'assets' , 'cli' , 'r.js')

options = [ 
    {
        'shortName':'c',
        'longName':'compile',
        'hasValue':False
        } ,
    {
        'shorName':'h',
        'longName':'html',
        'hasValue':False
        }
    ]




def run(params , options):
    """
    """
    utils.removefolder(BUILD_DIR);
    utils.createfolder(BUILD_DIR);
    
    utils.copyfiles( 'template' , os.path.join(BUILD_DIR , 'template') )
    utils.copyfiles( 'static' , os.path.join(BUILD_DIR , 'static') )

    try:
        mainjs  = os.path.join( PATH , BUILD_DIR , 'static' , 'js' , 'main.js' )
        maincss  = os.path.join( PATH , BUILD_DIR , 'static' , 'css' , 'main.css' )
        print mainjs
        log.log( 'Combine css&js with r.js' )
        os.system( 'node ' + RJSPATH +' -o name=main out=main.js baseUrl=' + os.path.join(PATH , BUILD_DIR , 'static' , 'js') )
        os.system( 'node ' + RJSPATH + ' -o cssIn=' + maincss + ' out=' + maincss )
        log.success( 'Combine css&js with r.js success.' )
    except:
        log.error('Please insure you have install r.js on your computer')
        raise
    
    if options.get('compile'):
        print 'c'
    else:
        print 'n'
