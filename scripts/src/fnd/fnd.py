#!/usr/bin/env python3

from syspy import Shell
from syspy.tools import getInputs, parseOptions
sh = Shell()

version = 'Version: 0.0.1'

synopsis_msg = '''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fnd
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A python package to explore your filesystem
'''
def synopsis():
	print(synopsis_msg)

help_msg = '''Usage: fnd (-/--)option command <pattern>

options
	-h, --help\t: help menu
	--synopsis\t: package description
	-v, --verbose\t: talk to me
	--version\t: version
commands
	|-----|---------|------|-------|----------|------------------------|
	| cmd | recurse | from | A = a | pattern  | search for             |
	|-----|---------|------|-------|----------|------------------------|
	|  d  | true    | .    | false | is       | directories containing |
	|  h  | false   | .    | false | is       | inode                  |
	|  i  | true    | .    | false | is       | text inside file       |
	|  q  | true    | .    | true  | includes | inode                  |
	|  r  | true    | .    | false | is       | inode                  |
	|-----|---------|------|-------|----------|------------------------|'''

def help():
	print(help_msg)

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

def compile():
	source_files = sh.find.recurse('*.c')
	header_dirs = sh.find.directories_with('*.h')
	header_dirs_with_options = \
		[y for x in zip(['-I'] * len(header_dirs), header_dirs) for y in x]

	cmd = ['cc'] + \
			source_files + \
			['-o ./execute'] + \
			header_dirs_with_options

	if sh.verbose:
		print()
		print('Source files:')
		print(source_files)
		print()
		print('Header file include directories:')
		print(header_dirs)
		print()

	sh.command(cmd)

# TODO: add command to search for environment variables
if (command):
	if len(remainder) > 1: raise TypeError('too many input arguments')
	def list_print(li):
		for item in li: print('./' + item)
	try: pattern = remainder[0]
	except: raise TypeError('not enough input args, expecting a pattern to search for')

	if command == 'd': list_print(sh.find.directories_with(pattern))
	elif command == 'h': list_print(sh.find.here(pattern))
	elif command == 'i': sh.command(['find . -type f -print | xargs grep'] + remainder)
	elif command == 'q': sh.command(['find . -type f -iname "*' + remainder[0] + '*"'])
	elif command == 'r': list_print(sh.find.recurse(pattern))
	else: sh.log.error('not a recognized command: ' + command)
else:
	# default behavior of the package
	synopsis()
	help()