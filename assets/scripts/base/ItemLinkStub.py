# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import iLinkStub
import message_Message_def as M_M_DD

class ItemLinkStub(iLinkStub.ILinkStub):

    def __init__(self, **kwargs):
        super(ItemLinkStub, self).__init__()

    def uploadItemInfo(self, uniqueId, item):
        self.addLinkInfo(uniqueId, item)

    def downloadItemInfo(self, uniqueId, box):
        _itemVal = self.getLinkInfo(uniqueId)

        if _itemVal:
            if box.client:
                box.client.onQueryItemLink(uniqueId, _itemVal)
        else:
            box.onMessagePre(M_M_DD.datas.channel_noItem, [])

