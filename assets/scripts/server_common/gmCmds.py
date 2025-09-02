# -*- coding: utf-8 -*-
import gameglobal

for mod in ('SYSTEM', 'MISC', 'BOT', 'TEST_CMD', 'OPERATION'):
    exec("import commands.%s" % (mod,))


def getFunc(name):
    return globals()[name]


def preReloadScript():
    gameglobal.clearCommandsCache()
