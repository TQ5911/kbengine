# -*- coding: utf-8 -*-


import KBEngine
from KBEDebug import *
import utils
import gameconst
import gameengine
import dataUtils

import mounts_mounts as MOUNTS
import appearance_ModelResource as APM

class ImpOutfit(object):
    def __init__(self):
        LOG_INFO("ImpOutfit __init__ ")
        self.checkOutfitConfigOpen(gameconst.OutfitEnum.wing, self.appearance.outfitData.wingId)
        self.checkOutfitConfigOpen(gameconst.OutfitEnum.hair, self.appearance.outfitData.hairId)
        self.checkOutfitConfigOpen(gameconst.OutfitEnum.clothes, self.appearance.outfitData.clothesId)
        self.checkOutfitConfigOpen(gameconst.OutfitEnum.picFrame, self.appearance.outfitData.picFrameId)
        self.checkOutfitConfigOpen(gameconst.OutfitEnum.mount, self.appearance.outfitData.mountId)
        self.base.onGetCellAppearance(self.appearance)

    def checkOutfitConfigOpen(self, outfitType, outfitId):
        if not dataUtils.checkOpenOutfit(outfitType, outfitId):
            self.appearance.removeOutfitById(self, outfitType, outfitId)

    @utils.isMyself
    def reqDisableOutfit(self, exposed, outfitType, outfitId):
        LOG_INFO('reqDisableOutfit:', outfitType, outfitId)
        self.appearance.removeOutfitById(self, outfitType, outfitId)
        return

    def enableOutfit(self, outfitType, outfitId):
        LOG_INFO('enableOutfit:', outfitType, outfitId)
        if outfitType == gameconst.OutfitEnum.mount:
            if outfitId != self.curMountId:
                self._exitRiding()

        self.appearance.setOutfitId(self, outfitType, outfitId)

    def checkOutfitExpired(self, outfitList):
        for outfitType, outfitId in outfitList:
            if outfitType == gameconst.OutfitEnum.mount and outfitId == self.curMountId:
                self._exitRiding()

            self.appearance.removeOutfitById(self, outfitType, outfitId)

    def updatePicFrameId(self, picFrameId):
        LOG_INFO('updatePicFrameId ', picFrameId)
        # self.guildBox and self.guildBox.onUpdateAttrAndDiffNotify(self.gbId, {'picFrameId': picFrameId})
        if self.teamId > 0:
            self.updateAttrToStub({'picFrameId': picFrameId})
        # gameengine.getGlobalBase('VisitStub').onUpdateVisitInfo(self.gbId, {'picFrameId': picFrameId})

    def updatePropByMount(self, mountId, bAdd):
        LOG_INFO('updatePropByMount:', mountId, bAdd)
        prop = MOUNTS.datas[mountId]['prop']
        if prop:
            if bAdd:
                for propName, val in prop:
                    self.addProp(propName, val, gameconst.SourceType.SrcTpMountProp)
            else:
                for propName, val in prop:
                    self.addProp(propName, -val, gameconst.SourceType.SrcTpMountProp)

    def addOutfitByItem(self, itemId, dayLimit, appearanceIds):
        LOG_INFO('addOutfitByItem:', itemId, dayLimit, appearanceIds)
        now = utils.curTS()
        for appearanceId in appearanceIds:
            appearanceData = APM.datas[appearanceId]
            outfitType = appearanceData['part']
            outfitId = appearanceData['appearanceId']
            expiredTime = 0 if dayLimit == 0 else now + dayLimit * 3600 * 24

            self.base.addAppearanceByReason(appearanceId, outfitType, outfitId, expiredTime, gameconst.AddOutfitReason.REWARD)
    
    def appearanceOnLogin(self, idsDict):
        for appearanceId in idsDict:
            self.updatePropByAppearance(appearanceId, True)

    def updatePropByAppearance(self, appearanceId, bAdd):
        LOG_INFO('updatePropByAppearance:', appearanceId, bAdd)
        appearanceData = APM.datas[appearanceId]
        prop = appearanceData['prop']
        if prop:
            if bAdd:
                for propName, val in prop:
                    self.addProp(propName, val, gameconst.SourceType.SrcTpAppearance)
            else:
                for propName, val in prop:
                    self.addProp(propName, -val, gameconst.SourceType.SrcTpAppearance)
