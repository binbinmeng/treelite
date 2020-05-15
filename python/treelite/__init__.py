# coding: utf-8
"""
Treelite: a model compiler for decision tree ensembles
"""
import os
from importlib import import_module

VERSION_FILE = os.path.join(os.path.dirname(__file__), 'VERSION')
with open(VERSION_FILE, 'r') as _f:
    __version__ = _f.read().strip()

# package will re-export public members of the following scripts/subpackages:
CORE_PACKAGES = ['.core', '.frontend', '.annotator', '.contrib']

__all__ = []
for package in CORE_PACKAGES:
    module = import_module(package, __name__)
    for public_member in module.__all__:
        globals()[public_member] = vars(module).get(public_member)
    __all__ += module.__all__
