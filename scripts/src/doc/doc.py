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
        bld <containerName>: builds docker container with dockerfile in current directory
        sh <containerName>: execute a shell in the container
        contain <imageName> <containerName>: creates a container with the image name
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
def get_image_id(image_name_repository):
    return $(docker images | grep -i @(image_name_repository)).split()[2]
def docker_run_container(image_id, container_name):
    docker run --name @(container_name) @(image_id)
def container_is_running():
    cont_running = (CONTAINER_NAME in $(doc ls -a))
    return cont_running
def remove_docker_container(cont_name):
    result = $(docker rm @(cont_name))
    if (result != ''): print('removed ', result.strip())
def execute_shell_in_container(container_name):
    docker run -it --rm @(container_name) sh

# deals with options accordingly
for opt, arg in options:
    if opt in ('-h', '--help'): help(); sh.log.succeed()
    elif opt in ('--synopsis'): synopsis(); sh.log.succeed()
    elif opt in ('-v', '--verbose'):
        verbose = True
        sh.verbose = True
    elif opt == '--version': print(version); sh.log.succeed()

if (command):
    if (command == 'bld'):
        sh.command(['docker build -t', remainder[0], '.'])
    elif command == 'contain':
        image_name = remainder[0]
        container_name = remainder[1]
        image_id = get_image_id(image_name)
        docker_run_container(image_id, container_name)
    elif command == 'sh':
        execute_shell_in_container(remainder[0])
    elif command == 'rm': remove_docker_container(remainder[0])
    else:
        sh.command(shortcuts.get(command, [command]) + remainder)
else:
    synopsis()
    help()
