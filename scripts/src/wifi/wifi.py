#!/usr/bin/env python3

import sys
from Shell import DeclarativeCommands, DeclarativeOptions, DeclarativeCLI, DeclarativeShell
sh = DeclarativeShell()

version = 'Version: 0.0.1'

synopsis = '''\
Usage: wifi <--option|-o> <command>
"ls -d": to ensure the driver is in use
"ls -w": to find the wireless interface'''

def get_interfaces():
    interfaces = sh.respond(['netctl', 'list']).split('\n')
    return [f.strip() for f in interfaces[:-1]]

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
        class net:
            description = 'create edit and delete networks'
            class CLI(DeclarativeCLI):
                __level__ = 1
                class Options(DeclarativeOptions):
                    class create_c:
                        description = 'creates a network interface if it does not already exist'
                        @staticmethod
                        def instructions(arg):
                            interfaces = sh.respond(['netctl', 'list']).split('\n')
                            interfaces = [f.strip() for f in interfaces[:-1]]
                            if arg in interfaces: sh.log.error('interface "' + arg + '" already exists')
                            else:
                                ret = sh.command(['sudo', 'cp', '/etc/netctl/examples/wireless-wpa', '/etc/netctl/' + arg])
                                sys.exit(ret)
                    class edit_e:
                        description = 'edit a network interface'
                        @staticmethod
                        def instructions(arg):
                            interfaces = sh.respond(['netctl', 'list']).split('\n')
                            interfaces = [f.strip() for f in interfaces[:-1]]
                            if arg in interfaces:
                                ret = sh.command('sudo vim /etc/netctl/' + arg)
                                sys.exit(ret)
                            else: sh.log.error(arg + ' not in network interfaces')
                    class delete_d:
                        description = 'remove a network interface'
                        @staticmethod
                        def instructions(arg):
                            if arg in get_interfaces():
                                ret = sh.command('sudo rm -f /etc/netctl/' + arg)
                                sys.exit(ret)
                            else: sh.log.error('"' + arg + '" not in interfaces')
                class Commands(DeclarativeCommands):
                    class ls:
                        description = 'list current networks'
                        @staticmethod
                        def instructions(remainder):
                            ret = sh.command(['netctl list'] + remainder)
                            sys.exit(ret)

        class show:
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
                    class wireless_w:
                        description = 'list wireless interface'
                        @staticmethod
                        def instructions():
                            ret = sh.command('ip link | grep -A 1 -i "[0-99: ]w"')
                            sys.exit(ret)
                class Commands(DeclarativeCommands): pass

        def __default_no_args__(self):
            cli.help()

cli = CLI()
cli.run(sys.argv[1:])
sh.finish()
