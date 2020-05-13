#!/usr/bin/env python3

import pickle
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

class cache_interface:
    @staticmethod
    def save(interface):
        sh.command(['mkdir', '-p', dir.config])
        pickle.dump(interface, open(dir.interface, 'wb'))
    @staticmethod
    def get():
        try: return pickle.load(open(dir.interface, 'rb'))
        except: sh.log.error('need to set an interface with "wifi on <interface>"')

def get_networks():
    interfaces = sh.respond(['find', dir.netctl, '-maxdepth', '1', '-type', 'f']).split('\n')
    return [sh.basename(f.strip()) for f in interfaces[:-1]]

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
                            if arg in get_networks(): sh.log.error('interface "' + arg + '" already exists')
                            else:
                                ret = sh.command(['sudo', 'cp', '/etc/netctl/examples/wireless-wpa', '/etc/netctl/' + arg])
                                sys.exit(ret)
                    class edit_e:
                        description = 'edit a network interface'
                        @staticmethod
                        def instructions(arg):
                            if arg in get_networks():
                                ret = sh.command('sudo vim /etc/netctl/' + arg)
                                sys.exit(ret)
                            else: sh.log.error(arg + ' not in networks')
                    class delete_d:
                        description = 'remove a network interface'
                        @staticmethod
                        def instructions(arg):
                            if arg in get_networks():
                                ret = sh.command('sudo rm -f /etc/netctl/' + arg)
                                sys.exit(ret)
                            else: sh.log.error('"' + arg + '" not in networks')
                    class start_s:
                        description = 'connetc to the specified network'
                        @staticmethod
                        def instructions(arg):
                            if arg in get_networks():
                                interface = cache_interface.get()
                                sh.command(['sudo ip link set', interface, 'down'], passFail=True)
                                ret = sh.command(['sudo netctl start', arg], passFail=True)
                                if ret != 0: sh.command('systemctl status netctl@{}.service'.format(arg))
                                sh.finish()
                            else: sh.log.error('"' + arg + '" not in networks')
                class Commands(DeclarativeCommands):
                    class ls:
                        description = 'list current networks'
                        @staticmethod
                        def instructions(remainder):
                            ret = sh.command(['netctl list'])
                            sys.exit(ret)

        class test:
            description = 'tests the internet connection by pinging google'
            @staticmethod
            def instructions(remainder):
                sh.command(['ping -c 3 google.com'], passFail=True)
                sh.command('echo ""')
                sh.finish()
        class on:
            description = '<interface> turn interface on'
            @staticmethod
            def instructions(remainder):
                if remainder:
                    interface = remainder[0]
                    ret = sh.command(['sudo ip link set', interface, 'up'], passFail=True)
                    if ret == 0: cache_interface.save(interface)
                    sh.finish()
                else: sh.log.error('command, on, requires input <interface>')
        class off:
            description = 'turn wifi interface off'
            @staticmethod
            def instructions(remainder):
                interface = cache_interface.get()
                sh.command(['sudo netctl stop-all'], passFail=True)
                sh.command(['sudo ip link set', interface, 'down'], passFail=True)
                sh.command(['rm -rf', dir.interface], passFail=True)
                sh.finish()
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
                    class networks_n:
                        description = 'scan for networks to connect to'
                        @staticmethod
                        def instructions():
                            interface = cache_interface.get()
                            ret = sh.command(['sudo iw dev', interface, 'scan | grep "SSID: ."'])
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
