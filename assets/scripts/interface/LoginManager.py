import KBEngine
import iCentralLogin
import gameconst


class LoginManager(iCentralLogin.ICentralLogin):
    def onCentralServerConnected(self, centralServerId):
        KBEngine.addTimer(gameconst.CENTRAL_SERVICE_HEARTBEAT_INTERVAL, gameconst.CENTRAL_SERVICE_HEARTBEAT_INTERVAL,
                          lambda timerId: self.checkCentralServerActive(centralServerId))
