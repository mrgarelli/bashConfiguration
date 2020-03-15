#!/usr/bin/env python3

from syspy import Shell
from syspy.implementations import source_executables

sh = Shell()
sh.verbose = False
extensions = ['.sh', '.py', '.js', '.xsh']
ignore_sources = ['__init__.py', '__pycache__', '.pytest_cache']

source_executables(sh, extensions, ignore_sources)
