#!/usr/bin/env python3

from syspy import Shell
from syspy.tools import getInputs, parseOptions
sh = Shell()

version = 'Version: 0.0.1'

synopsis_msg = '''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
p
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A python wrapper for useful python commands
contains some useful commands for virtual environments
'''
def synopsis():
	print(synopsis_msg)

shortcuts = {
	'a': ['source', 'env/bin/activate'],
	'c': ['python3', '-m', 'virtualenv', 'env'],
	'd': ['deactivate'],
	't': ['python3', '-m unittest discover', '-t ../..'],
	}

help_msg = '''options
	-h, --help :\thelp menu
	--synopsis :\tpackage description
	-v, --verbose :\ttalk to me
	--version :\tversion

command shortcuts'''

def help():
	print(help_msg)
	for sh in shortcuts:
		print('\t', sh, ':\t', ' '.join(shortcuts[sh]))

verbose = False

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

if command:
	if (command in shortcuts.keys()): sh.command(shortcuts[command])
	else:
		full_command = ([command] + remainder) if remainder else [command]
		sh.command(['python3'] + full_command)
else:
	# default behavior of the package
	sh.command(['python3'])
