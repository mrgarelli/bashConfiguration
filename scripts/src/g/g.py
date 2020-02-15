#!/usr/bin/env python3

from syspy import Shell
from syspy.tools import getInputs, parseOptions
sh = Shell()

version = 'Version: 1.0'

synopsis_msg = '''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
g
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A python git wrapper
On one hand this is a collection of easily accessible git shortcuts
In addition it is a clever way to track files around your system
'''
def synopsis():
	print(synopsis_msg)

shortcuts = {
	'a': ['add'],
	'b': ['branch'],
	'c': ['commit'],
	'ca': ['commit', '--amend'],
	'ch': ['checkout'],
	'cht': ['checkout', '--track'],
	'i': ['init'],
	'l': ['log'],
	'm': ['merge'],
	'ph': ['push'], 
	'pho': ['push', 'origin'],
	'pl': ['pull'],
	'plr': ['pull', '--rebase'],
	'plo': ['pull', 'origin'],
	'rma': ['rm', '-r', '--cached', '.'],
	'rst': ['reset'],
	's': ['status'],
	'sh': ['stash'],
	'shc': ['stash', 'clear'],
	't': ['ls-tree', '-r', '--name-only'],
	}

help_msg = '''options
	-h, --help :\thelp menu
	-p :\t\tplatform specific tracker (linux, osx)
	--synopsis :\tpackage description
	-u :\t\tunix configuration tracker
	-v, --verbose :\ttalk to me
	--version :\tversion

custom commands
	aa: adds all files, same as "add ." in normal repos, custom for -u and -p
  rsth <n>: resets back to HEAD, if given n then it removes that number of commits as well

command shortcuts'''

def help():
	print(help_msg)
	for sh in shortcuts:
		print('\t', sh, ':\t', ' '.join(shortcuts[sh]))

unix = False
platform = False
verbose = False

git_command = '/usr/bin/git'
command_with_tree = [
	git_command,
	' --work-tree=',
	sh.home
	]
unix_git_command = ''.join(
	command_with_tree + [' --git-dir=', sh.home, '/.unx']
	)
platform_git_command = ''.join(
	command_with_tree + [' --git-dir=', sh.home, '/.pltfrm']
	)

shortOpts = 'hpuv'
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
	elif opt in ('-p'):
		platform = True
		git_command = platform_git_command
	elif opt in ('--synopsis'): synopsis(); sh.log.succeed()
	elif opt in ('-u'):
		unix = True
		git_command = unix_git_command
	elif opt in ('-v', '--verbose'):
		verbose = True
		sh.verbose = True
	elif opt == '--version': print(version); sh.log.succeed()

def git(command): sh.command([git_command] + command)

def add_all(files):
	files = [sh.home + f for f in files]
	for file in files:
		git(['add', file])

def add_all_unix_files():
	files = [
		'/.xonshrc',
		'/.ideavimrc',
		'/.gitignore',
		'/readme.md',
		'/.rsrc',
		'/scripts/src/*',
		'/scripts/__init__.py',
		'/scripts/scripts.py',
		'/Local/scripts.py',
		]
	add_all(files)

def add_all_platform_files():
	platform = sh.os
	if platform == 'linux':
		files = [
			'/.vimrc',
			'/.platform.xsh',
			'/.xinitrc',
			'/.inputrc',
			'/.local/share/konsole/*',
			'/.config/konsolerc',
			'/.config/Code\ -\ OSS/User/keybindings.json',
			'/.config/Code\ -\ OSS/User/settings.json',
			'/.config/openbox/lxde-rc.xml',
			'/.AndroidStudio3.5/config/keymaps',
			]
	elif platform =='mac':
		files = [
			'/.vimrc',
			'/.platform.xsh',
			'/Library/Preferences/AndroidStudio3.4/keymaps/deku.xml',
			'/Library/Application\ Support/Code/User/keybindings.json',
			'/Library/Application\ Support/Code/User/settings.json',
		]
	else:
		sh.log.error('unrecognized platform')
	add_all(files)

def hardReset(remainder):
	try: number_commits = remainder[0]
	except: number_commits = None
	if number_commits:
		git(['reset --hard HEAD~' + str(number_commits)])
	else:
		git(['reset --hard HEAD'])

if (command):
	if command == 'aa':
		if unix: add_all_unix_files()
		elif platform: add_all_platform_files()
		else: git(['add .'])
	elif command == 'rsth':
		hardReset(remainder)
	else:
		git(shortcuts.get(command, [command]) + remainder)
else:
	# default behavior of the package
	synopsis()
	help()
	# git(['']) # calls the default git help
