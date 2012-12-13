#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

from setuptools import setup
from ursa import __version__ as version

ursa_dir = 'ursa/assets'

data_files = []

for dirpath, dirnames , filenames in os.walk(ursa_dir):
    data_files.append( [ dirpath , [ os.path.join(dirpath , f) for f in filenames ] ] )


setup(
    name="Ursa",
    version=version,
    author="zhengxin",
    author_email="zhengxin@sogou-inc.com",
    description="Ursa is a devlelop environment for front end developer.",
    zip_safe=False,

    packages=['ursa' , 'ursa.commands' , 'ursa.jinja2' ],
    
    data_files = data_files,

    install_requires=[
        "beautifulsoup4"
        ],
    
    entry_points = {
        'console_scripts':[
            'ursa=ursa.main:run'
            ]
        }
)
