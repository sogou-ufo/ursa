#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

import log
import conf
import utils
import sys

options = [ ]



def copyfiles(ptype):
    """拷贝库文件到目标文件
    """
    pfolder = 'project' if ptype == 'pc' else 'mproject'

    base  = os.path.join(conf.getConfig()['base'] , 'assets' , pfolder  )

    utils.copyfiles(base , conf.getConfig()['path'])
        
    



def run(params , options):
    ptype = 'mobile' if ( len(params) and params[0]=='mobile') else 'pc'
    if os.listdir( conf.getConfig()['path'] ):
        log.warn('Not an empty folder.\nContinue may change your exists files.\nStill Continue?')
        iscontinue = utils.isyes(raw_input('(y/n):'))
        if not iscontinue:
            log.log('User cancel init.')
            sys.exit(1)

    log.log('Begin to init current folder')
        
    copyfiles(ptype)

    log.success('Init success.')
