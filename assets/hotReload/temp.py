# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    import gameconst
    import utils
    import conflict_status_def as CSDD
    import AuthClsWraper
    import impCombat
    @utils.isMyself
    @AuthClsWraper.onlyMainChannel
    def clientSetState(self, exposed, state):
        if state < 0:
            return
        if state not in (gameconst.State.Idle, gameconst.State.Moving, gameconst.State.Fall, gameconst.State.Sprinting):
            return
        if self.hasState(CSDD.datas.serverControl):
            if state != gameconst.State.Sprinting:
                ERROR_MSG('clientSetState but in server control')
                return
        if state == gameconst.State.Idle and not self.hasState(gameconst.State.Moving):
            return
        DEBUG_MSG('clientSetState', state)
        self.setState(state, reportErr=False)
        self.setTempMiscProp(gameconst.AvatarProps.AvatarActiveTimestamp, utils.getNow())
    impCombat.ImpCombat.clientSetState = clientSetState
    # --auto genterate mark--
    pass
def refreshBase():
    # --auto genterate mark--
    pass
def refreshInterface():
    # --auto genterate mark--
    pass
if KBEngine.component == 'cellapp':
    refreshCell()
else:
    refreshBase()
