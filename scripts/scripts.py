#!/usr/bin/env python3

from syspy import Shell
from syspy.implementations import source_executables

sh = Shell()
sh.verbose = False
extensions = ['.sh', '.py', '.js', '.xsh']

source_executables(sh, extensions)
