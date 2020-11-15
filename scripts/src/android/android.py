#!/usr/bin/env python3

import sys, os
from declarecli import DeclarativeCLI, DeclarativeOptions, DeclarativeCommands
from syspy import Shell
sh = Shell()

version = 'Version: 0.0.1'

synopsis = '''\
Usage: android <--option|-o> <command>
tools to manage creation of android apps'''

class dir:
    home = os.path.expanduser('~')
    config = os.path.join(home, '.config')

class file: 
    settings = os.path.join(sh.main, 'settings.txt')
    gradlesettings = os.path.join(sh.working, 'settings.gradle')

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
        class init:
            description = '<name> initialize gradle springboot kotlin project for web'
            @staticmethod
            def instructions(remainder):
                # sh.command('gradle init', passFail=True)
                # sh.command(['cat', file.settings, '>>', file.gradlesettings], passFail=True)
                init_cmd = [
                    'spring init',
                    '--type=gradle-project',
                    '--language=kotlin',
                    '--dependencies=web',
                    ] + remainder
                sh.command(init_cmd, passFail=True)
                sh.finish()
        class install:
            description = 'install all dependencies for springboot and gradle'
            @staticmethod
            def instructions(remainder):
                sh.command('yay -Sy spring-boot-cli gradle', passFail=True)
                sh.finish()

        def __default_no_args__(self):
            cli.help()

cli = CLI()
cli.run(sys.argv[1:])
sh.finish()
