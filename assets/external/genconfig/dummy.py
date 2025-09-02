# coding: utf-8
class Swallower(object):
    def __getattribute__(self, name):
        return self

    def __call__(self, *args, **kw):
        pass

    def __bool__(self):
        return False

    def __index__(self):
        return self

    def __getitem__(self, item):
        return self

class Dummy(object):
    def __getattribute__(self, name):
        return self

    def __call__(self, *args, **kw):
        pass
        
    def __iter__(self):
        yield Swallower()

    def __getitem__(self, i):
        return Swallower()

dummy = Dummy()