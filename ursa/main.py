#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys


import server
import log





BASE_DIR = os.path.abspath(os.path.dirname(__file__))  + os.sep





def run():
    args = sys.argv
    
    target = None

    if len(args) <=1: # no arguments , help
        args.append('help')
    

    if len(args) >1 :
        commandName = args[1]
        
    if commandName == 'help':
        commandName = 'uhelp'


    try:
        command = __import__( 'commands.' + commandName , globals() , locals() , ['run'] )
        command.run( args[2:] )
    except:
        log.error('Invalid commandName: ' + commandName )
        return
        
        

        


if __name__ == '__main__':
    run()
