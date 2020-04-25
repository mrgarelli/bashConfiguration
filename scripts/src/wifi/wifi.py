#!/usr/bin/env python3

import sys
from Shell import DeclarativeCommands, DeclarativeOptions, DeclarativeCLI, DeclarativeShell
sh = DeclarativeShell()

version = 'Version: 0.0.1'

synopsis = '''\
Usage: wifi <--option|-o> <command>
'''

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
        class network_n:
            description = 'check the network driver status'
            @staticmethod
            def instructions():
                ret = sh.command('lspci -k | grep -i -A 2 "network"')
                sys.exit(ret)
        class echo_e:
            description = 'print the argument passed in'
            @staticmethod
            def instructions(arg):
                print(arg)
                sh.log.success()

    class Commands(DeclarativeCommands):
        class echo:
            description = 'can add custom commands'
            @staticmethod
            def instructions(remainder):
                sh.command(['echo'] + remainder)
        class ls:
            description = 'network related listings'
            class CLI(DeclarativeCLI):
                __level__ = 1
                class Options(DeclarativeOptions):
                    class driver_d:
                        description = 'check the network driver status'
                        @staticmethod
                        def instructions():
                            ret = sh.command('lspci -k | grep -i -A 2 "network"')
                            sys.exit(ret)
                class Commands(DeclarativeCommands): pass

        def __default_unspecified_command__(self, command, remainder):
            sh.log.error('unrecognized command')
        def __default_no_args__(self):
            cli.help()

cli = CLI()
cli.run(sys.argv[1:])
sh.finish()