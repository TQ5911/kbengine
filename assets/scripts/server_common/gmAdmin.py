# -*- coding: utf-8 -*-
from KBEDebug import *

INSIDE = 1
OUTSIDE = 2
ALLSIDE = 3


class _DUMMY_SU():
    def feedbackCommandSucc(self, *args):
        DEBUG_MSG('DUMMY.feedbackCommandSucc', *args)

    def feedbackCommandFail(self, *args):
        DEBUG_MSG('DUMMY.feedbackCommandFail', *args)

    def replyCommand(self, *args):
        DEBUG_MSG('DUMMY.replyCommand', *args)


DUMMY_SU = _DUMMY_SU()
