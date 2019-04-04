import sys
from syspy import Message, BashAPI, parseOptions, fail, succeed, getInputs

version = Message('Version: 1.0')

help = Message(
''''Wrapper for partclone'

options
	-h, --help: help menu
	--version: version
commands
	c: clone <partition> <fileName>
	r: restore <file> <partition>'''
)

verbose = False

shortOpts = 'hv'
longOpts = [
	'help',
	'verbose',
	'version',
	]

# parsed options and gathers remainder (command)
options, remainder = parseOptions(getInputs(), shortOpts, longOpts)

# deals with options accordingly
for opt, arg in options:
	if opt in ('-h', '--help'):
		help.display = True
		help.smartPrint()
		succeed()
	elif opt in ('-v', '--verbose'):
		verbose = True
	elif opt == '--version':
		version.display = True
		version.smartPrint()
		succeed()

try:
	cmd = remainder[0]
	inputs = remainder[1:]
except:
	print(version.content)
	print()
	print(help.content)
	succeed()

api = BashAPI('api.sh')

if cmd == 'c':
	api.cmd('clone', args=inputs, realTime=True)
elif cmd == 'r':
	api.cmd('restore', args=inputs, realTime=True)
else:
	print('Not a recognized command')
	print()
	print(help.content)
	fail()
