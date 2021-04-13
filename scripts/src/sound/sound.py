#!/usr/bin/env python3

import sys, os
from declarecli import DeclarativeCLI, DeclarativeOptions, DeclarativeCommands
from syspy import Shell
sh = Shell()

version = 'Version: 0.0.1'

# switching https://unix.stackexchange.com/questions/62818/how-can-i-switch-between-different-audio-output-hardware-using-the-shell

synopsis = '''\
Usage: sound <--option|-o> <command>
tools to manage sound cards'''

class dir:
    home = os.path.expanduser('~')
    config = os.path.join(home, '.config', 'wifi')
    interface = os.path.join(config, 'interface')
    netctl = os.path.join('/etc', 'netctl')

class CLI(DeclarativeCLI):
    __level__ = 0
    class Synopsis:
        @staticmethod
        def body(): print(synopsis)

    class Options(DeclarativeOptions):
        class help_h:
            description = 'extended help message of this package'
            @staticmethod
            def instructions():
                cli.extended_help()
                sh.log.success()
        class verbose_v:
            description = 'get more descriptive command output'
            @staticmethod
            def instructions():
                sh.verbose = True
        class version:
            description = 'output the current tool version'
            @staticmethod
            def instructions():
                print(version)
                sh.log.success()

    class Commands(DeclarativeCommands):
        class gui:
            description = 'launch pavucontrol (pulseaudio gui)'
            @staticmethod
            def instructions(remainder):
                sh.command(['pavucontrol &'])
        class outputs:
            description = 'list current sound sinks in use'
            @staticmethod
            def instructions(remainder):
                sh.command(['pacmd list-sinks | grep -e "name:" -e "index:"'])
        class nvidia:
            description = 'list the nvidia card'
            @staticmethod
            def instructions(remainder):
                sh.command(['lspci -H1 | grep -i nvidia'])
        class check:
            description = 'did the nvidia sound card register'
            @staticmethod
            def instructions(remainder):
                sh.command(['lspci | grep -i "nvidia"'])
                sh.command(['aplay -l | grep -i nvidia'])
        class cards:
            description = 'list all available cards (available yes or unknown)'
            @staticmethod
            def instructions(remainder):
                # sh.command(["pacmd list-cards | grep -i 'output:' | grep -i 'available: unknown\|available: yes' | grep -i -e 'available:' -e 'output:'"])
                response = sh.respond("pacmd list-cards | grep -i 'output:' | grep -i 'available: unknown\|available: yes' | grep -i -e 'available:' -e 'output:'", shell=True)
                lines = response.split('\n')
                lines.pop()
                for line in lines:
                    first_part, second_part = line.split('(priority ')
                    name_ext = None
                    try:
                        _, name, description = first_part.split(':')
                    except: 
                        _, name, name_ext, description = first_part.split(':')
                    priority, availability = second_part.split(', ')
                    if name_ext: name = ':'.join([name, name_ext])
                    print(name)
                    print(f"\t{description}")
                    print(f"\t priority: {priority}")
                    print(f"\t{availability}")
                    print("________________________________________________________________________________")


        def __default_no_args__(self):
            cli.help()

cli = CLI()
cli.run(sys.argv[1:])
sh.finish()
