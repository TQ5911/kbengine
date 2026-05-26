# -*- coding: utf-8 -*-
from KBEDebug import *

INSIDE = 1
OUTSIDE = 2
ALLSIDE = 3


class _DUMMY_SU():
    def feedbackCommandSucc(self, *args):
        LOG_DBG('DUMMY.feedbackCommandSucc', *args)

    def feedbackCommandFail(self, *args):
        LOG_DBG('DUMMY.feedbackCommandFail', *args)

    def doReplyCommand(self, *args):
        LOG_DBG('DUMMY.doReplyCommand', *args)


DUMMY_SU = _DUMMY_SU()
