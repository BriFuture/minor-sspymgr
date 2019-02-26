# -*- coding: utf-8 -*-

# from distutils.core import setup
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt', "r", encoding="utf-8") as f:
    requires = f.read().splitlines()

setup( 
    name = "sspymgr", 
    packages = find_packages(where='.'), 
    version = "0.0.16",

    entry_points = {
        "console_scripts": [
            'sspymgr = sspymgr.webgui:run_forever'
        ]
    },

    description = "Web Manager for Shadowsocks Service, Python Version",
    author = "BriFuture",
    author_email = "jw.brifuture@gmail.com",
    license = "GPLv3",
    url = "http://github.com/brifuture/minor-sspymgr",
    
    install_requires = requires,

    include_package_data = True,
    zip_safe=False,
    # package_data = {
    #     '':['vuttemplates/*', 'plugins/*'],
    # },
    exclude_package_data = {'': ['__pycache__']},

    # download_url = "",
    keywords = [ "webserver", "shadowsocks-manager" ],
    classifiers = [ 
        "Programming Language :: Python", 
        "Programming Language :: Python :: 3" ,
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],

    long_description = long_description,
    long_description_content_type="text/markdown",
)