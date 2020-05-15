# -*- coding: utf-8 -*-
"""Utility functions for tests"""

import sys

import numpy as np


def os_compatible_toolchains():
    """Get list of C compiler supported in OSes"""
    if sys.platform == 'darwin':
        toolchains = ['gcc']
    elif sys.platform == 'win32':
        toolchains = ['msvc']
    else:
        toolchains = ['gcc', 'clang']
    return toolchains


def load_txt(filename):
    """Get 1D array from text file"""
    if filename is None:
        return None
    content = []
    with open(filename, 'r') as f:
        for line in f:
            content.append(float(line))
    return np.array(content, dtype=np.float32)
