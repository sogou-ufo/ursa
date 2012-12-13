#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

import utils
import conf
import log
import parser

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


def compileHTML():
    """为所有tpl文件加上时间戳
    """
    base = os.path.join(PATH , 'build' , 'template')
    tplfiles = []
    for dirpath , dirnames , filenames  in os.walk(base):

        tplfiles.extend([ os.path.join( dirpath , f ) for f in filenames if f.endswith('.tpl')  ])
    for tpl in tplfiles:
        f = parser.compileHTML(tpl)
        utils.writefile(tpl , f)

def compileCss():
    """为所有css文件加上时间戳
    """
    base = os.path.join(PATH , 'build' , 'static' , 'css')
    cssfiles = []
    for dirpath , dirnames, filenames in os.walk(base):
        cssfiles.extend( [ os.path.join(dirpath , f) for f in filenames if f.endswith('.css') ] )
    for css in cssfiles:
        f = parser.compileCss(css)


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
        os.system( 'node ' + RJSPATH +' -o name=main out='+ mainjs + ' optimize=none baseUrl=' + os.path.join(PATH , BUILD_DIR , 'static' , 'js') )
        os.system( 'node ' + RJSPATH + ' -o cssIn=' + maincss + ' out=' + maincss )
        log.success( 'Combine css&js with r.js success.' )
    except:
        log.error('Please insure you have install r.js on your computer')
        raise
    
    compileHTML()
    compileCss();

    if options.get('compile'):
        print 'c'
    else:
        print 'n'



