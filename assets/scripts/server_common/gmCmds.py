# -*- coding: utf-8 -*-
import gameglobal

for mod in ('SYSTEM', 'MISC', 'BOT', 'TEST_CMD', 'OPERATION', 'GAME_API'):
    exec("import commands.%s" % (mod,))


def preReloadScript():
    gameglobal.clearCommandsCache()
