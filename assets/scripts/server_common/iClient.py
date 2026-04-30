# coding: utf-8
from KBEDebug import *
import KBEngine
import gametimer


class IClient(object):

    def _popDialog(self, dlogId):
        self.allClients.popDialog(dlogId)

    def _showPopoverMsg(self, msgId):
        LOG_DBG("_showPopoverMsg  ", msgId)
        self.allClients.showPopoverMsg(msgId)

    def showPopoverMsg(self, target, context, msgId, delay=0.5):
        if delay:
            self.addTimerCB(delay, '_showPopoverMsg', (msgId,), gametimer.TIMER_TAG_SHOW_POPOVER_MSG)
        else:
            self._showPopoverMsg(msgId)

    def _showPopoverMsgWithArg(self, msgId, args):
        self.allClients.showPopoverMsgWithArg(msgId, args)

    def showPopWithArgToSomebody(self, msgId, args, avatarId):
        avatar = KBEngine.entities.get(avatarId)
        if not (avatar and avatar.client and avatar.isReal()):
            return

        entityCall = avatar.clientEntity(self.id)
        if entityCall:
            entityCall.showPopoverMsgWithArg(msgId, args)
