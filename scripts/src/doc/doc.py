#!/usr/bin/env xonsh

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
    'ls': [
        'docker ps --format "table {{.Names}}\t{{.ID}}\t{{.Image}}\t{{.Ports}}"',
        ''.join(getInputs()[1:])
    ],
    'clean': [
        'docker system prune',
        ''.join(getInputs()[1:])
    ],
    'rmi': [
        'docker rmi',
        ''.join(getInputs()[1:])
    ],
    'img': [
        'docker images',
        ''.join(getInputs()[1:])
    ],
    'st': [
        'docker start',
        ''.join(getInputs()[1:])
    ],
    'sp': [
        'docker stop',
        ''.join(getInputs()[1:])
    ],
}

help_msg = '''options
        -h, --help :\thelp menu
        --synopsis :\tpackage description
        -v, --verbose :\ttalk to me
        --version :\tversion

custom commands
        launch: build a docker container and run from scratch
        rm: removes a docker image

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

CONTAINER_NAME='docCont'
def build_and_return_number():
    build_number = $(docker build .).split('\n')[-2].split(' ')[-1]
    return build_number
def docker_run(build_number, name):
    docker run --name @(name) @(build_number)
def container_is_running():
    cont_running = (CONTAINER_NAME in $(doc ls -a))
    return cont_running
def remove_docker_container(cont_name):
    result = $(docker rm @(cont_name))
    if (result != ''): print('removed ', result.strip())

# deals with options accordingly
for opt, arg in options:
    if opt in ('-h', '--help'): help(); sh.log.succeed()
    elif opt in ('--synopsis'): synopsis(); sh.log.succeed()
    elif opt in ('-v', '--verbose'):
        verbose = True
        sh.verbose = True
    elif opt == '--version': print(version); sh.log.succeed()

if (command):
    if command == 'launch':
        build_number = build_and_return_number()
        remove_docker_container(CONTAINER_NAME)
        print()
        print('~~~~~~~~~~OUTPUT~~~~~~~~~~')
        docker run --name @(CONTAINER_NAME) @(build_number)
    elif command == 'rm': remove_docker_container(remainder[0])
    else:
        sh.command(shortcuts.get(command, [command]) + remainder)
else:
    synopsis()
    help()
