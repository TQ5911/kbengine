# -*- encoding:utf-8 -*-
# defined in */scripts/entity_defs/Account.def
# It is generated automatically, please do not modify manually
import KBEngine

class AccountBase(KBEngine.Entity):
    def minorAccountConstraintTip(self, arg0): pass
    def onAvatarDetailInAccount(self, arg0, arg1, arg2, arg3, arg4): pass
    def onAvatarOfflineTime(self, arg0, arg1): pass
    def onCharInfoChange(self, arg0): pass
    def onCreateAvatarFailed(self, arg0): pass
    def onCreateAvatarResult(self, arg0, arg1): pass
    def onGameConfigChanged(self, arg0, arg1): pass
    def onGetAuthOfflineTimeClient(self, arg0, arg1): pass
    def onHotfixVersion(self, arg0): pass
    def onKickAnotherAccount(self): pass
    def onKickAnotherAvatar(self): pass
    def onLoginNeedReconnect(self): pass
    def onMessage(self, arg0, arg1): pass
    def onRemoveAvatar(self, arg0): pass
    def onReqAvatarGBID(self, arg0): pass
    def onReqAvatarList(self, arg0, arg1, arg2): pass
    def onSelectGameFailed(self, arg0, arg1): pass
