#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import log
import utils
import re
import os

import conf

TEMP_FOLDER = os.path.join(conf.getConfig()['path'] , 'temp')


options = [ 
    
    ]




def getPkgOpen(subpkgs):
    """获取open 模块
    模块地址 http://ufo.sogou-inc.com/git/open.git
    """
    targetfolder = os.path.join( conf.getConfig()['path'] ,  'static'  , 'js' )
    utils.createfolder(TEMP_FOLDER)
    
    if not os.path.exists( targetfolder ):
        utils.createfolder(targetfolder)

    subpkgs = subpkgs or conf.getConfig()['PKG_OPEN']
    
    subpkgs.insert(0 , 'common')
    
    os.system('git clone http://ufo.sogou-inc.com/git/open.git ' + os.path.join(TEMP_FOLDER , 'open'))
    successpkg = []
    for pkg in subpkgs:
        source = os.path.join( TEMP_FOLDER , 'open' , pkg )
        if not os.path.exists(source):
            log.warn('Sub package ' + pkg + ' not exist in Open.')
            continue
        utils.copyfiles( source , os.path.join( targetfolder , 'open' , pkg ) )
        successpkg.append( pkg )
    

    utils.removefolder(TEMP_FOLDER)
    log.success( 'Adding Open package include ' + ','.join(successpkg) + ' success!' )


def anapkg(param):
    """分析pkg类似 open[auth]
    返回( open , [auth] )
    Arguments:
    - `param`:
    """
    index = param.find('[')
    lastindex = param.find(']')
    if index != -1 and lastindex != -1:
        return ( param[0:index] , param[index+1:lastindex].split(':'))
    else:
        return (param , None)

def run(params , options):
    if not params:
        log.error('Must specify package name.')
        sys.exit(1)
    log.log('Adding module ' + ','.join(params))
    for pkg in params:
        pkg = anapkg(pkg)
        if not globals().get('getPkg' + pkg[0].capitalize()):
            log.warn( "Package " + pkg[0] + ' not found.')
        else:
            globals()['getPkg' + pkg[0].capitalize()](pkg[1])
