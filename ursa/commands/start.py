#!/usr/bin/env python
#-*- coding:utf-8 -*-

try:
    import ursa.server as server
except:
    import server


options = [ ]




def run(params , options):
    """
    """
    if len(params) and params[0].isdigit():
        server.run(int(params[0]))
    else:
        server.run()
