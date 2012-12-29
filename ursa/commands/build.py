#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import time

import utils
import conf
import log
import uparser as parser

BUILD_DIR = 'build'
PATH = conf.getConfig()['path'] 
RJSPATH = os.path.join(conf.getConfig()['base'] , 'assets' , 'cli' , 'r.js')
YCPATH = os.path.join(conf.getConfig()['base'] , 'assets' , 'cli' , 'yuicompressor.jar')

options = [ 
    {
        'shortName':'c',
        'longName':'compress',
        'hasValue':False
        } ,
    {
        'shortName':'h',
        'longName':'html',
        'hasValue':False
        }
    ]


def compileHTML( needCompress = False , needHtml = False ):
    """为所有tpl文件加上时间戳
    """
    base = os.path.join(PATH , 'build' , 'template')
    tplfiles = []
    for dirpath , dirnames , filenames  in os.walk(base):
        tplfiles.extend([ os.path.join( dirpath , f ) for f in filenames if f.endswith('.tpl')  ])
    for tpl in tplfiles:
        f = parser.compileHTML(tpl , needCompress)
        utils.writefile(tpl , f)

    if needHtml:
        log.log('Render html file.\nIt will under build folder.')
        files = os.listdir( os.path.join( base ) )
        for fname in files:
            token = fname.split('.')[0]
            html = parser.parseTpl(token , isbuild=True)
            utils.writefile( os.path.join(PATH , 'build' , 'html' , token + '.html' ) , html )
        log.success('Render html success');
        

def compileCss():
    """为所有css文件加上时间戳
    """
    base = os.path.join(PATH , 'build' , 'static' , 'css')
    cssfiles = []
    for dirpath , dirnames, filenames in os.walk(base):
        cssfiles.extend( [ os.path.join(dirpath , f) for f in filenames if f.endswith('.css') ] )
    for css in cssfiles:
        f = parser.compileCss(css)
        utils.writefile(css , f)

def compileCommon(token):
    """
    """
    base = os.path.join(PATH , 'build' )
    files = []
    for dirpath , dirnames, filenames in os.walk(base):
        files.extend( [ os.path.join(dirpath , f) for f in filenames ] )
    for fi in files:
        f = parser.compileCommon(fi , token)
        if f:
            utils.writefile(fi , f)


def run(params , options):
    """
    """
    tmbegin = time.time()

    buildtype = None
    if params and len(params):
        if conf.getConfig().get(params[0]):
            buildtype = params[0]
        else:
            log.error('No such build type:' + params[0])
            sys.exit(1)

    


    utils.removefolder(BUILD_DIR);
    utils.createfolder(BUILD_DIR);
    
    utils.copyfiles( 'template' , os.path.join(BUILD_DIR , 'template') )
    utils.copyfiles( 'static' , os.path.join(BUILD_DIR , 'static') )

    mainjs  = os.path.join( PATH , BUILD_DIR , 'static' , 'js' , 'main.js' )
    maincss  = os.path.join( PATH , BUILD_DIR , 'static' , 'css' , 'main.css' )

    try:
        log.log( 'Combine css&js with r.js' )
        os.system( 'node ' + RJSPATH +' -o name=main out='+ mainjs + ' optimize=none baseUrl=' + os.path.join(PATH , BUILD_DIR , 'static' , 'js') )
        os.system( 'node ' + RJSPATH + ' -o cssIn=' + maincss + ' out=' + maincss )
        log.success( 'Combine css&js with r.js success.' )
    except:
        log.error('Please insure you have install r.js on your computer')
        raise
    

    if options.get('compress'):
        log.log('Begin to compile Js')
        os.system( 'java -jar ' + YCPATH + ' --type js --charset ' + conf.getConfig()['encoding'] + ' ' + mainjs + ' -o ' + mainjs );
        log.log('Begin to compile Css')
        os.system( 'java -jar ' + YCPATH + ' --type css --charset ' + conf.getConfig()['encoding'] + ' ' + maincss + ' -o ' + maincss );
    if options.get('html'):
        utils.createfolder( os.path.join( BUILD_DIR ,  'html'))
        

    log.log('Begin to compile tpls')
    compileHTML(options.get('compress') , options.get('html'))
    log.log('Begin to addTimestamps')
    compileCss();

    log.log('Begin to replace all token')

    compileCommon(buildtype)


    log.success('Compile success.')
    log.success('Time cost %s s.' % (time.time()-tmbegin) )
