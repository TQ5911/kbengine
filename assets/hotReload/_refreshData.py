import gameglobal
import gamerefresh
gamerefresh.refreshData()
if gameglobal.isBootstrap:
    gameglobal.localBaseApp.notifyInterfaceDataReload()
