import gameglobal
import importlib
import hotReload
importlib.reload(hotReload)
hotReload.refreshBase()
if gameglobal.isBootstrap:
    gameglobal.localBaseApp.notifyInterfaceReload()
