#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import time
import subprocess

import utils
import conf
import log
import uparser as parser

BUILD_DIR = 'build'
PATH = conf.getConfig()['path'] 
RJSPATH = os.path.join(conf.getConfig()['base'] , 'assets' , 'cli' , 'r.js')
YCPATH = os.path.join(conf.getConfig()['base'] , 'assets' , 'cli' , 'yuicompressor.jar')
COMPILE_FOLDER = conf.getConfig().get('compile_folder')

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
    if COMPILE_FOLDER:
        for dirpath , dirnames , filenames  in os.walk(os.path.join(PATH , 'build' , COMPILE_FOLDER)):
            tplfiles.extend([ os.path.join( dirpath , f ) for f in filenames  ])
        
    for tpl in tplfiles:
        f = parser.compileHTML(tpl , needCompress)
        utils.writefile(tpl , f)

    if needHtml:
        log.log('Render html file.\nIt will under build folder.')
        files = os.listdir( os.path.join( base ) )
        tplfiles = []
        for dirpath , dirnames, filenames in os.walk(base):
            tplfiles.extend( [ os.path.join(dirpath , f) for f in filenames if f.endswith('.tpl') ] )
        for fname in tplfiles:
            token = fname.replace( base + '/' , '' ).replace('.tpl' , '')
            html = parser.parseTpl(token  , isbuild=True)
            
            if token.find('/') != -1:
                subfolder = os.path.join(PATH , 'build' , 'html'  , token.split('/')[0])
                if not os.path.exists(subfolder):

                    utils.createfolder(subfolder)
            
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
    
    if COMPILE_FOLDER:
        utils.copyfiles( COMPILE_FOLDER , os.path.join(BUILD_DIR , COMPILE_FOLDER) )
        
    require_modules = conf.getConfig().get('require_modules') or ['main']
    maincss  = os.path.join( PATH , BUILD_DIR , 'static' , 'css' , conf.getConfig().get('css_folder') or '' , 'main.css' )

    try:
        log.log( 'Combine css&js with r.js' )
        for module in require_modules:
            js = os.path.join(PATH, BUILD_DIR , 'static' , 'js' , conf.getConfig().get('js_folder') or '' , module + '.js' )
            subprocess.call( 'node ' + RJSPATH +' -o name=' + module + ' out='+ js + ' optimize=none baseUrl=' + os.path.join(PATH , BUILD_DIR , 'static' , 'js' , conf.getConfig().get('js_folder') or '')  , shell=True)
        subprocess.call( 'node ' + RJSPATH + ' -o cssIn=' + maincss + ' out=' + maincss  , shell=True)
        log.success( 'Combine css&js with r.js success.' )
    except:
        log.error('Please insure you have install r.js on your computer')
        raise
    
    log.log('Begin to addTimestamps...' , True)
    compileCss();

    log.success('Success!')


    if options.get('html'):
        utils.createfolder( os.path.join( BUILD_DIR ,  'html'))

    log.log('Begin to compile tpls...' )
    compileHTML(options.get('compress') , options.get('html'))
    log.success('Success!')
    

    log.log('Begin to replace all token...', True)

    compileCommon(buildtype)
    log.success('Success!')

    if options.get('compress'):
        log.log('Begin to compile Js...' , True)
        for module in require_modules:
            js = os.path.join(PATH, BUILD_DIR , 'static' , 'js', conf.getConfig().get('js_folder') or ''  , module + '.js' )
            subprocess.call( 'java -jar ' + YCPATH + ' --type js --charset ' + conf.getConfig()['encoding'] + ' ' + js + ' -o ' + js , shell=True );
        log.success('Success!')
        log.log('Begin to compile Css...' , True)
        subprocess.call( 'java -jar ' + YCPATH + ' --type css --charset ' + conf.getConfig()['encoding'] + ' ' + maincss + ' -o ' + maincss , shell=True);
        log.success('Success!')


    log.success('Compile success.')
    log.success('Time cost %s s.' % (time.time()-tmbegin) )
