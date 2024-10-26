# constants\__init__.py

"""project constants package.

Modules exported by this package:


- `global_setup`: its main constants.
- `patterns`: some useful regex patterns.
"""
from . import global_setup as global_setup
from . import patterns as patterns

__all__ = ["global_setup", "patterns"]
