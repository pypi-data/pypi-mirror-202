# -*- coding: utf-8 -*-

from astartool.project import get_version

version = (0, 1, 0, 'final', 0)
__version__ = get_version(version)

del get_version
