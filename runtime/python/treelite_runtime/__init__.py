# coding: utf-8
import os
from importlib import import_module

VERSION_FILE = os.path.join(os.path.dirname(__file__), 'VERSION')
with open(VERSION_FILE) as f:
    __version__ = f.read().strip()

# package will re-export public members of the following scripts/subpackages:
CORE_PACKAGES = ['.predictor']

__all__ = []
for package in CORE_PACKAGES:
    module = import_module(package, __name__)
    for public_member in module.__all__:
        globals()[public_member] = vars(module).get(public_member)
    __all__ += module.__all__
