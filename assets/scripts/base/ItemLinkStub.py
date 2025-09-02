# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import iLinkStub
import message_Message_def as MMD

class ItemLinkStub(iLinkStub.ILinkStub):

    def __init__(self):
        super(ItemLinkStub, self).__init__()

    def uploadItemInfo(self, uniqueId, itemVal):
        self.addLinkInfo(uniqueId, itemVal)

    def downloadItemInfo(self, uniqueId, box):
        itemVal = self.getLinkInfo(uniqueId)

        if itemVal:
            box.client and box.client.onQueryItemLink(uniqueId, itemVal)
        else:
            box.onMessagePre(MMD.datas.channel_noItem, [])

