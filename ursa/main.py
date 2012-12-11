#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import conf

#add current folder to path
sys.path.append( conf.getConfig()['base'] )



import os


import server
import log
import cli

def run():
    args = sys.argv
    
    target = None

    if len(args) <=1: # no arguments , help
        args.append('help')
    

    if len(args) >1 :
        commandName = args[1]
        
    if commandName == 'help':
        commandName = 'uhelp'

    args = args[2:]


    try:
        command = __import__( 'commands.' + commandName , globals() , locals() , ['run' , 'options'] )
    except:
        raise
        log.error('Invalid commandName: ' + commandName )
        return


    argInfo = cli.parseArgv(args , command.options)

    if len(argInfo['errors']) > 0:
        for error in argInfo['errors']:
            log.log(error)
        log.error('Invalid command line. Try `ursa help <command>`');
        return;
    command.run(argInfo['params'],argInfo['options'] );
        


if __name__ == '__main__':
    run()
