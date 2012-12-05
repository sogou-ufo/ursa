#!/usr/bin/env python
#-*- coding:utf-8 -*-

def makeOptionMap(opt):
    """
    
    Arguments:
    - `opt`:
    """
    optMap = {}
    if opt:
        for info in opt:
            if 'shortName' in info:
                optMap['-' + info['shortName']] = info
            if 'longName' in info:
                optMap['--' + info['longName']] = info

    return optMap


def parseArgv(args , optionInfo):
    """
    
    Arguments:
    - `args`:
    - `optionInfo`:
    """
    optMap = makeOptionMap(optionInfo)
    errors = []

    options = {}
    params = []

    while len(args) >0:
        arg = args.pop(0)

        if arg[0] == '-':
            try:
                option = optMap[arg]

                if 'hasValue' in option and option['hasValue']:
                    if len(args) == 0:# TODO , some problem
                        errors.append( 'Missing value for option: ' + arg )
                    else:
                        options[option.longName] = args.pop(0)
                else:
                    options[option['longName']] = True
                
            except:
               errors.append( 'Invalid options:' + arg ) 

        else:
            params.append(arg)


    return {'params':params , 'options':options , 'errors':errors}
