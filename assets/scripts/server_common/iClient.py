# coding: utf-8
from KBEDebug import *
import gametimer
import KBEngine


class IClient(object):

    def _popDialog(self, dialogId):
        self.allClients.popDialog(dialogId)

    def _showPopoverMsg(self, msgId):
        LOG_DBG("_showPopoverMsg", msgId)
        self.allClients.showPopoverMsg(msgId)

    def showPopoverMsg(self, _, context, msgId, delay=0.5):
        if delay:
            self.addTimerCB(delay, '_showPopoverMsg', (msgId,), gametimer.TIMER_TAG_SHOW_POPOVER_MSG)
        else:
            self._showPopoverMsg(msgId)

    def showPopWithArgToSomebody(self, msgId, args, avatarId):
        _avatar = KBEngine.entities.get(avatarId)
        if not (_avatar and _avatar.client and _avatar.isReal()):
            return

        _entityCall = _avatar.clientEntity(self.id)
        if _entityCall:
            _entityCall.showPopoverMsgWithArg(msgId, args)

    def _showPopoverMsgWithArg(self, msgId, args):
        self.allClients.showPopoverMsgWithArg(msgId, args)

