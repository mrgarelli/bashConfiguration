#!/usr/bin/env python3

import sys, os
from declarecli import DeclarativeCLI, DeclarativeOptions, DeclarativeCommands
from syspy import Shell
sh = Shell()

version = 'Version: 0.0.1'

synopsis = '''\
Usage: wifi <--option|-o> <command>
tools to manage network configuration'''

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
        class echo_e:
            description = 'print the argument passed in'
            @staticmethod
            def instructions(arg):
                print(arg)
                sh.log.success()

    class Commands(DeclarativeCommands):
        class test:
            description = 'tests the internet connection by pinging google'
            @staticmethod
            def instructions(remainder):
                sh.command(['ping -c 3 google.com'], passFail=True)
                sh.command('echo ""')
                sh.finish()
        class status:
            description = 'get current connection status'
            @staticmethod
            def instructions(remainder):
                sh.command(['nmcli'])
        class scan:
            description = 'scans for nearby networks'
            @staticmethod
            def instructions(remainder):
                if remainder:
                    sh.log.error('scan takes no arguments')
                sh.command(['nmcli device wifi rescan'])
                sh.command(['nmcli device wifi list'])
        class connect:
            # TODO: add method https://unix.stackexchange.com/questions/145366/how-to-connect-to-an-802-1x-wireless-network-via-nmcli
            description = '<network-name> <password> connect to specified network'
            @staticmethod
            def instructions(remainder):
                numArgs = len(remainder)
                if numArgs < 1:
                    sh.log.error('connect command requires <network-name> and optional <password> inputs')
                elif numArgs == 1:
                    netname = remainder[0]
                    sh.command(['nmcli device wifi connect', netname])
                elif numArgs == 2:
                    netname = remainder[0]
                    password = remainder[1]
                    sh.command(['nmcli device wifi connect', netname, 'password', password])
                elif numArgs > 2:
                    sh.log.error('too many input arguments, only expect <network-name> <password>')
        class disconnect:
            description = '<network-name> disconnect from specified network'
            @staticmethod
            def instructions(remainder):
                numArgs = len(remainder)
                if numArgs < 1:
                    sh.log.error('disconnect command requires <network-name> input')
                elif numArgs > 1:
                    sh.log.error('too many input arguments, only expect <network-name>')
                netname = remainder[0]
                sh.command(['nmcli con down', netname])

        def __default_no_args__(self):
            cli.help()

cli = CLI()
cli.run(sys.argv[1:])
sh.finish()
