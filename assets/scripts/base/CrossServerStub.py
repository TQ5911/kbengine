# coding: utf-8

import KBEngine
from KBEDebug import *

import iGlobal
import iBaseNoCell
import iTimer
import gametimer
import SwitchServer
import utils
import gameglobal


class CrossServerStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self):
        pass

    def doNext(self):
        super().doNext()

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        else:
            self._onTimer(tid, userArg)

    def test(self):
        LOG_IFO("CrossServerStub test")

    def onGetSwitchServerData(self, data):
        LOG_IFO("onGetSwitchServerData: {}".format(len(data)))
        SwitchServer.SwitchServerUtils.saveData(data)

    def onReqCrossServer(self, accountName, reasonNo, crossServerEntityCall):
        LOG_IFO("onReqCrossServer", accountName, reasonNo)
        ret = True
        if accountName in self.accountDic:
            LOG_WARN("onReqCrossServer accountName has in accountDic", accountName)

        token = utils.generateUUID()
        self.accountDic[accountName] = {
            "box": crossServerEntityCall,
            "token": token
        }
        crossServerEntityCall.onCrossServerResp(ret, token, reasonNo)

    def onEndCrossServer(self, accountName):
        LOG_IFO("onEndCrossServer", accountName)
        if accountName not in self.accountDic:
            LOG_ERR("onGobackServer accountName not in accountDic", accountName)
            return

        self.accountDic.pop(accountName)

    def onCheckCrossServerToken(self, accountName, token, crossServerEntityCall):
        LOG_IFO("onCheckCrossServerToken", accountName, token, crossServerEntityCall)
        ret, _ = self._checkCrossServerToken(accountName, token)
        crossServerEntityCall.onCheckCrossServerTokenResp(ret)

    def _checkCrossServerToken(self, accountName, token):
        ret = False
        crossServerEntityCall = None

        if accountName not in self.accountDic:
            LOG_ERR("_checkCrossServerToken accountName not in accountDic", accountName)
        else:
            crossServerToken = self.accountDic[accountName].get("token")
            if crossServerToken != token:
                LOG_ERR("_checkCrossServerToken token err", crossServerToken, token)
            else:
                ret = True
                crossServerEntityCall = self.accountDic[accountName].get("box")
        return ret, crossServerEntityCall

    def checkCrossServerToken(self, accountName, token, box, callBackFunc, callBackArgs):
        LOG_IFO("checkCrossServerToken", accountName, token, box, callBackFunc, callBackArgs)
        ret, crossServerEntityCall = self._checkCrossServerToken(accountName, token)
        args = [ret, crossServerEntityCall]
        args.extend(callBackArgs)
        getattr(box, callBackFunc)(*args)

    def onGobackServer(self, accountName):
        LOG_IFO("onGobackServer", accountName)
        if accountName not in self.accountDic:
            LOG_ERR("onGobackServer accountName not in accountDic", accountName)
            return

        self.accountDic.pop(accountName)

    def doGmModifyServertime(self, su, modifyTime):
        LOG_IFO("doGmModifyServertime", su, modifyTime)
        import gameconfig
        import iRouter
        import gmCommand
        if gameconfig.serverId() not in gameglobal.mapleServerInfo:
            LOG_ERR("onGmModifyAllServertimeInCrossGroup gameconfig.serverId() not in maple", gameconfig.serverId())
            return


        if KBEngine.publish():
            LOG_ERR("onGmModifyAllServertimeInCrossGroup KBEngine.publish()", KBEngine.publish())
            return
        if '.' and '-' not in modifyTime:
            return
        forwardGMCommand = gmCommand.forwardGMCommand
        forwardGMCommand(su, '$modifyServertime-cell', modifyTime)
        forwardGMCommand(su, '$modifyServertime-base', modifyTime)

        LOG_DBG("doGmModifyServertime success", gameconfig.serverId(), modifyTime)

    #gm改变整个跨服组上服务器的时间（包括跨服）
    def onGmModifyAllServertimeInCrossGroup(self, su, modifyTime):
        LOG_IFO("onGmModifyAllServertimeInCrossGroup", su, modifyTime)
        import gameconfig
        import iRouter

        crossServerGroupID = gameglobal.mapleServerInfo[gameconfig.serverId()]['server_group']
        groupServerList = utils.group2ServerIds(crossServerGroupID)

        for serverID in groupServerList:
            _stub = iRouter.RemoteServerStubEntityCall(int(serverID), 'CrossServerStub')
            _stub.onGmModifyAllServertimeInCrossGroupResp(su, modifyTime)

        LOG_DBG("onGmModifyAllServertimeInCrossGroup success", gameconfig.serverId(), modifyTime)

    def onGmModifyAllServertimeInCrossGroupResp(self, su, modifyTime):
        LOG_DBG("onGmModifyAllServertimeInCrossGroupResp", su, modifyTime)
        self.doGmModifyServertime(su, modifyTime)
