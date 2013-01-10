#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys

bcolors = {
    'HEADER':'\033[95m',
    'OKBLUE':'\033[94m',
    'OKGREEN':'\033[92m',
    'WARNING':'\033[93m',
    'FAIL':'\033[91m',
    'ENDC': '\033[0m'
}

def warn(str , noNewLine = False):
    """
    
    Arguments:
    - `str`:
    """
    sys.stdout.write(bcolors['WARNING'] + str + bcolors['ENDC'] + ('' if noNewLine else '\n'))



def error(str , noNewLine = False):
    """
    
    Arguments:
    - `str`:
    """
    
    sys.stdout.write(bcolors['FAIL'] + str + bcolors['ENDC'] + ('' if noNewLine else '\n'))

def log(str , noNewLine = False):
    """
    
    Arguments:
    - `str`:
    """
    sys.stdout.write(bcolors['OKBLUE'] + str + bcolors['ENDC']  + ('' if noNewLine else '\n'))

def success(str , noNewLine = False):
    """
    """
    sys.stdout.write(bcolors['OKGREEN'] + str + bcolors['ENDC'] + ('' if noNewLine else '\n'))
