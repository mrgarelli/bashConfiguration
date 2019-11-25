#!/usr/bin/env python3

from syspy import Shell
from syspy.tools import getInputs

sh = Shell()

inputs = getInputs()

if len(inputs) > 1: raise TypeError('too many input arguments')

url = ''
try: url = inputs[0]
except: pass

sh.chrome(url)