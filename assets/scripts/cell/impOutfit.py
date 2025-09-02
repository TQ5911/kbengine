# -*- coding: utf-8 -*-


import KBEngine
from KBEDebug import *
import utils
import gameconst
import gameengine
import dataUtils

import mounts_mounts as MOUNTS


class ImpOutfit(object):
    def __init__(self):
        DEBUG_MSG("ImpOutfit __init__ ")
        self.checkOutfitConfigOpen(gameconst.OutfitType.wing, self.appearance.outfitData.wingId)
        self.checkOutfitConfigOpen(gameconst.OutfitType.hair, self.appearance.outfitData.hairId)
        self.checkOutfitConfigOpen(gameconst.OutfitType.clothes, self.appearance.outfitData.clothesId)
        self.checkOutfitConfigOpen(gameconst.OutfitType.picFrame, self.appearance.outfitData.picFrameId)
        self.checkOutfitConfigOpen(gameconst.OutfitType.mount, self.appearance.outfitData.mountId)

    def checkOutfitConfigOpen(self, outfitType, outfitId):
        if not dataUtils.checkOutfitOpen(outfitType, outfitId):
            self.appearance.removeOutfitId(self, outfitType, outfitId)

    @utils.isMyself
    def reqDisableOutfit(self, exposed, outfitType, outfitId):
        DEBUG_MSG('reqDisableOutfit:', outfitType, outfitId)
        self.appearance.removeOutfitId(self, outfitType, outfitId)
        return

    def enableOutfit(self, outfitType, outfitId):
        DEBUG_MSG('enableOutfit:', outfitType, outfitId)
        if outfitType == gameconst.OutfitType.mount:
            if outfitId != self.curMountId:
                self._exitRiding()

        self.appearance.setOutfitId(self, outfitType, outfitId)
        return

    def checkOutfitExpired(self, outfitList):
        for outfitType, outfitId in outfitList:
            if outfitType == gameconst.OutfitType.mount and outfitId == self.curMountId:
                self._exitRiding()

            self.appearance.removeOutfitId(self, outfitType, outfitId)
        return

    def updatePicFrameId(self, picFrameId):
        DEBUG_MSG('updatePicFrameId ', picFrameId)
        # self.guildBox and self.guildBox.onUpdateAttrAndDiffNotify(self.gbId, {'picFrameId': picFrameId})
        if self.teamId > 0:
            self.updateAttrToStub({'picFrameId': picFrameId})
        # gameengine.getGlobalBase('VisitStub').onUpdateVisitInfo(self.gbId, {'picFrameId': picFrameId})

    def updatePropByMount(self, mountId, bAdd):
        DEBUG_MSG('updatePropByMount:', mountId, bAdd)
        prop = MOUNTS.datas[mountId]['prop']
        if prop:
            if bAdd:
                for propName, val in prop:
                    self.addProp(propName, val, gameconst.SourceType.MountProp)
            else:
                for propName, val in prop:
                    self.addProp(propName, -val, gameconst.SourceType.MountProp)
