#!/usr/bin/env python
# -*- coding: utf-8 -*-

from io import open
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import dragonmapper

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def open_file(filename):
    """Open and read the file *filename*."""
    with open(filename, encoding='utf-8') as f:
        return f.read()

readme = open_file('README.rst')
history = open_file('CHANGES.rst').replace('.. :changelog:', '')

setup(
    name='dragonmapper',
    version=dragonmapper.__version__,
    author='Thomas Roten',
    author_email='thomas@roten.us',
    url='https://github.com/tsroten/dragonmapper',
    description=('Identification and conversion functions for Chinese '
                 'text processing'),
    long_description=readme + '\n\n' + history,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing :: Linguistic',
        ],
    keywords=['chinese', 'mandarin', 'transcription', 'pinyin', 'zhuyin',
              'ipa', 'convert', 'bopomofo', 'hanzi', 'characters', 'readings'],
    packages=['dragonmapper', 'dragonmapper.data'],
    package_data={'dragonmapper': ['data/*.tsv', 'data/*.csv']},
    test_suite='dragonmapper.tests',
    install_requires=['zhon>=1.1.3', 'hanzidentifier>=1.0.2'],
)
