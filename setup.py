#!/usr/bin/env python
import os
from distutils.core import setup

setup(
	name             = 'hondler',
	version          = '0.0.1',
	description      = 'Django cart and checkout + frontend js',
	long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read(),
	author           = 'Artem Rudenko',
	author_email     = 'nenegoro@gmail.com',
	url              = 'https://github.com/gvidon/hondler/',
	package_dir      = {'hondler': '.'},
	package_data     = {'hondler': ['static/js/*', 'templates/hondler/*']},
	packages         = ['hondler'],
)