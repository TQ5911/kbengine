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

    def replyCommand(self, *args):
        LOG_DBG('DUMMY.replyCommand', *args)


DUMMY_SU = _DUMMY_SU()
