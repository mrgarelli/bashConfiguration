import sys, os
from syspy import Shell

def get_contents(fileName):
    name_components = fileName.split('_')
    capital_components = [wd.title() for wd in name_components]
    className = ''.join(capital_components)

    file_contents = f'''class {className}:
    def methodName(self):
        pass'''
    test_file_contents = f'''import pytest
from ..{fileName} import {className}

class mocks:
    one = []

class Test{className}:
    @classmethod
    def setup_class(cls):
        cls.subject = {className}()

    def test_example(self):
        assert 0 == 0

    @classmethod
    def teardown_class(cls): pass

# @pytest.mark.skip()'''
    return file_contents, test_file_contents


def create_test_directory_strucutre():
    sh.command(['touch', '__init__.py'], passFail=True)
    sh.command(['mkdir', '-p', 'tests'], passFail=True)
    sh.command(['touch', 'tests/__init__.py'], passFail=True)

sh = Shell()
args = sys.argv[1:]

if len(args) > 1:
    raise TypeError('too many input arguments')
if args:
    dir_name = args[0]
    sh.mkdir(dir_name)
    sh.cd(dir_name)
    create_test_directory_strucutre()
    file_name = dir_name + '.py'
    file_contents, test_file_contents = get_contents(dir_name)
    with open(file_name, 'a') as f:
        f.write(file_contents)
    test_file_name = os.path.join('tests', 'test_' + file_name)
    with open(test_file_name, 'a') as f:
        f.write(test_file_contents)
else: create_test_directory_strucutre()