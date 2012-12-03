#!/usr/bin/env python
#-*- coding:utf-8 -*-

bcolors = {
    'HEADER':'\033[95m',
    'OKBLUE':'\033[94m',
    'OKGREEN':'\033[92m',
    'WARNING':'\033[93m',
    'FAIL':'\033[91m',
    'ENDC': '\033[0m'
}

def warn(str):
    """
    
    Arguments:
    - `str`:
    """
    print bcolors['WARNING'] + str + bcolors['ENDC']



def error(str):
    """
    
    Arguments:
    - `str`:
    """
    
    print bcolors['FAIL'] + str + bcolors['ENDC']

def log(str):
    """
    
    Arguments:
    - `str`:
    """
    print bcolors['OKBLUE'] + str + bcolors['ENDC']

def success(str):
    """
    """
    print bcolors['OKGREEN'] + str + bcolors['ENDC']
