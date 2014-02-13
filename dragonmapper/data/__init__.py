# -*- coding: utf-8 -*-
"""Provides access to data files for dragonmapper."""

from __future__ import unicode_literals
import os.path
import pkgutil


PACKAGE_NAME = 'dragonmapper'
DATA_DIR = 'data'


def load_data_file(filename, encoding='utf-8'):
    """Load a data file and return it as a list of lines.

    Parameters:
        filename: The name of the file (no directories included).
        encoding: The file encoding. Defaults to utf-8.

    """
    data = pkgutil.get_data(PACKAGE_NAME, os.path.join(DATA_DIR, filename))
    return data.decode(encoding).splitlines()
