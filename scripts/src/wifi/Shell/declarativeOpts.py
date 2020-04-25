import sys, getopt, inspect

def parseOptions(arguments, shortOpts, longOpts):
    try:
        options, remainder = getopt.getopt(
            arguments,
            shortOpts,
            longOpts
        )
        command = None
        try:
            command = remainder[0]
            remainder = remainder[1:]
        except:
            remainder = None
        return options, command, remainder
    except getopt.GetoptError as err: raise(err)

class DeclarativeOptions:
    def __init__(self):
        self.__opts__ = [a for a in dir(self) if not a.startswith('__')]
        self.__instructions_map__ = {}
        self.__short_opts__ = []
        self.__long_opts__ = []
        for opt in self.__opts__:
            variations = opt.split('_')
            particular_instruction = getattr(self, opt).instructions
            has_arg = self.__has_arguments__(particular_instruction)
            long_opt = variations[0]
            self.__instructions_map__['--' + long_opt] = particular_instruction
            self.__long_opts__.append(long_opt + '=' if has_arg else long_opt)
            if len(variations) > 1:
                short_opt = variations[1]
                self.__instructions_map__['-' + short_opt] = particular_instruction
                self.__short_opts__.append(short_opt + ':' if has_arg else short_opt)
        self.__short_opts__ = ''.join(self.__short_opts__)

    @staticmethod
    def __has_arguments__(fun):
        try: # python3
            return len(inspect.getfullargspec(fun).args) > 0
        except: # python 2
            return len(inspect.getargspec(fun)[0]) > 0

    def __parse_options__(self, argv):
        return parseOptions(argv, self.__short_opts__, self.__long_opts__)

    def __handle_options__(self, options):
        for opt, arg in options:
            instructions_method = self.__instructions_map__[opt]
            if arg: instructions_method(arg)
            else: instructions_method()

    def __documentation__(self, tabs):
        if self.__opts__: subheader('Options', tabs)
        for opt in self.__opts__:
            line = [tabs]
            variations = opt.split('_')
            attr = getattr(self, opt)
            has_arg = self.__has_arguments__(attr.instructions)
            long_opt = ['--', variations[0], '=<arg>'] if has_arg else ['--', variations[0]]
            if len(variations) > 1:
                short_opt = [', -', variations[1], ' <arg>'] if has_arg else [', -', variations[1]]
            else: short_opt = []
            description = [': ', attr.description]
            line += long_opt + short_opt + description
            print(''.join(line))

class DeclarativeCommands:
    def __list__(self):
        return [a for a in dir(self) if not a.startswith('__')]

    def __documentation__(self, tabs):
        declared_commands = self.__list__()
        if declared_commands: subheader('Commands', tabs)
        for cmd in declared_commands:
            command_class = getattr(self, cmd)
            print(''.join([tabs, command_class.__name__, ': ', command_class.description]))
            if hasattr(command_class, 'CLI'):
                CLI = command_class.CLI
                cli = CLI()
                cli.help()


    def __run_command__(self, command, remainder):
        declared_commands = self.__list__()
        if (command):
            if command in declared_commands:
                command_class = getattr(self, command)
                if hasattr(command_class, 'instructions'):
                    instructions = command_class.instructions
                    instructions(remainder)
                elif hasattr(command_class, 'CLI'):
                    CLI = command_class.CLI
                    cli = CLI()
                    cli.run(remainder)
                else: pass # TODO: raise exception for incorrect class definition
            else: self.__default_unspecified_command__(command, remainder)
        else: self.__default_no_args__()

class DeclarativeCLI:
    def __init__(self):
        self.tabs = ''.join(['\t' for n in range(self.__level__)])
        self.opts = self.Options()
        self.cmds = self.Commands()

    def help(self):
        self.opts.__documentation__(self.tabs)
        self.cmds.__documentation__(self.tabs)

    def extended_help(self):
        if hasattr(self, 'Synopsis'):
            header('Synopsis')
            self.Synopsis.body()
        header('CLI')
        self.help()

    def run(self, arguments):
        options, command, remainder = self.opts.__parse_options__(arguments)
        self.opts.__handle_options__(options)
        self.cmds.__run_command__(command, remainder)

GREEN = '\033[0;32m'
CYAN = '\033[0;36m'
NC = '\033[0m'  # No Color

def subheader(msg, tabs):
    divider = ''.join(['_' for char in range(len(msg))])
    def green_print(word): print('{}{}{}{}'.format(tabs, GREEN, word, NC))
    green_print(divider)
    green_print(msg)

def header(msg):
    divider = '___________________________________________________________________________________'
    def cyan_print(word): print('{}{}{}'.format(CYAN, word, NC))
    cyan_print(divider)
    cyan_print(msg)