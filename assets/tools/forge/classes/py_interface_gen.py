import os


class PyInterfaceGen(object):
    def __init__(self, mod_name):
        self.mod_name = mod_name

    def get_file_path(self):
        _mod_name = self.mod_name + 'Interface.py'
        return os.path.join(os.environ['KBE_ASSETS'], 'scripts', 'interface', _mod_name)

    def gen(self):
        pass


