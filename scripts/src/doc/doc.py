#!/usr/bin/env python3

from syspy import Shell
from syspy.tools import getInputs, parseOptions
sh = Shell()

version = 'Version: 0.0.1'

synopsis_msg = '''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
doc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A python wrapper for making docker easy
'''
def synopsis():
    print(synopsis_msg)

shortcuts = {
    'ls': ['docker ps --format "table {{.Names}}\t{{.ID}}\t{{.Image}}\t{{.Ports}}"'],
}

help_msg = '''options
        -h, --help :\thelp menu
        --synopsis :\tpackage description
        -v, --verbose :\ttalk to me
        --version :\tversion

custom commands
        None

command shortcuts'''

def help():
    print(help_msg)
    for sh in shortcuts:
        print('\t', sh, ':\t', ' '.join(shortcuts[sh]))

shortOpts = 'hv'
longOpts = [
    'help',
    'synopsis',
    'verbose',
    'version',
]

# parsed options and gathers remainder (command)
options, command, remainder = parseOptions(getInputs(), shortOpts, longOpts)

# deals with options accordingly
for opt, arg in options:
    if opt in ('-h', '--help'): help(); sh.log.succeed()
    elif opt in ('--synopsis'): synopsis(); sh.log.succeed()
    elif opt in ('-v', '--verbose'):
        verbose = True
        sh.verbose = True
    elif opt == '--version': print(version); sh.log.succeed()

if (command):
    if command == 'command_name':
        # logic for custom commands
        pass
    else:
        sh.command(shortcuts.get(command, [command]) + remainder)
else:
    synopsis()
    help()
