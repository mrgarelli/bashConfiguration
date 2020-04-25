import sys, traceback

RED = '\033[0;31m'
GREEN = '\033[0;32m'
CYAN = '\033[0;36m'
ORANGE = '\033[33m'
NC = '\033[0m'  # No Color
# for coloring text

class Log:
    def __init__(self):
        self.color = True

    def red(self): return '\033[0;31m' if self.color else ''
    def green(self): return '\033[0;32m' if self.color else ''
    def orange(self): return '\033[33m' if self.color else ''
    def cyan(self): return '\033[0;36m' if self.color else ''
    def no_color(self): return '\033[0m' if self.color else ''

    @staticmethod
    def failure(): sys.exit(1)

    @staticmethod
    def success(): sys.exit(0)

    def header(self, msg):
        divider = '___________________________________________________________________________________'
        print('{}{}{}'.format(self.cyan(), divider, self.no_color()))
        print('{}{}{}'.format(self.cyan(), msg, self.no_color()))

    def subheader(self, msg):
        divider = ''.join(['_' for char in range(len(msg))])
        print('{}{}{}'.format(self.green(), divider, self.no_color()))
        print('{}{}{}'.format(self.green(), msg, self.no_color()))

    def warn(self, message):
        print('{}[WARNING]{} {}'.format(self.orange(), self.no_color(), message))

    def error(self, message):
        print('{}[ERROR]{} {}'.format(self.red(), self.no_color(), message))
        sys.exit(1)

    def validate(self, message):
        print('{}[LIT]{} {}'.format(self.green(), self.no_color(), message))