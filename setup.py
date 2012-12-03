#!/usr/bin/env python
#-*- coding:utf-8 -*-


from setuptools import setup
from ursa import __version__ as version


setup(
    name="Ursa",
    version=version,
    author="zhengxin",
    author_email="zhengxin@sogou-inc.com",
    description="Ursa is a devlelop environment for front end developer.",
    zip_safe=False,

    packages=['ursa' ],
    
    entry_points = {
        'console_scripts':[
            'ursa=ursa.main:run'
            ]
        }
)
