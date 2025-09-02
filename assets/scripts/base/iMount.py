# -*- coding: utf-8 -*-
import KBEngine

import formula
from KBEDebug import *
import gameconst
import utils
import dropAward
import mounts_set as MSD
import message_Message_def as MMD
import mounts_mounts as MOUNTS
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import taskClass_taskTarget as TCCTD
import gametimer
import gameclass
import dataUtils
import actionContext    


class IMount(object):
    def __init__(self):
        pass

    def mountOnLogin(self):
        for outfit in self.outfitInfo.outfitDict.values():
            if outfit.outfitType == gameconst.OutfitType.mount:
                configData = dataUtils.getOutfitConfigData(outfit.outfitType, outfit.outfitId)
                if configData:
                    prop = configData.get('prop', [])
                    if prop:
                        self.cell.updatePropByMount(outfit.outfitId, True)

    def doAddMount(self, pid, mountId, durationDays):
        INFO_MSG('doAddMount:', pid, mountId, durationDays)
        outfit = self.outfitInfo.getOutfitInfo(gameconst.OutfitType.mount, mountId)
        hasUnlock = False
        if outfit:
            if not outfit.expireTime:
                hasUnlock = True
                if not durationDays:
                    self.cell.onPendingUseItem(pid, gameconst.UseItem.FALSE)
                return
            else:
                if durationDays:
                    self.cell.onPendingUseItem(pid, gameconst.UseItem.FALSE)
                    return

        if durationDays <= 0:
            self.addOutfitByReason(gameconst.OutfitType.mount, mountId, 0, gameconst.AddOutfitReason.Mount_ITEM)
        else:
            expireTime = utils.getNow() + int(durationDays * gameconst.ONE_DAY_SECONDS)
            self.addOutfitByReason(gameconst.OutfitType.mount, mountId, expireTime, gameconst.AddOutfitReason.Mount_ITEM)

        self.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetMountActivated'])

        self.cell.onPendingUseItem(pid, gameconst.UseItem.TRUE)
        self.onMessagePre(MMD.datas.useMountsItemSuccess, [MOUNTS.datas[mountId]['name']])

        if not hasUnlock and not durationDays:
            self.achievementInfo.triggerAchieveByType(
                self, 
                gameconst.AchieveType.UNLOCK_MOUNT, 
                actionContext.AchievementCtx())

    def setCurMount(self, mountId):
        INFO_MSG(' set cur mount:', mountId)
        outfit = self.outfitInfo.getOutfitInfo(gameconst.OutfitType.mount, mountId)
        if outfit is None:
            return

        if outfit.expireTime and outfit.expireTime <= utils.getNow():
            return

        self.cell.setCurMountCell(mountId)
        self.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetMountRide'])

    def _eventActionAddMount(self, eventActionSrc, mountId, durationDays, *args, **kwargs):
        INFO_MSG('_eventActionAddMount:', mountId, durationDays)
        durationSeconds = int(float(durationDays) * gameconst.ONE_DAY_SECONDS)
        mountId = int(mountId)
        if mountId not in MOUNTS.datas:
            ERROR_MSG('_eventActionAddMount but mount id invalid:', mountId)
            return

        outfit = self.outfitInfo.getOutfitInfo(gameconst.OutfitType.mount, mountId)
        if outfit and not outfit.expireTime:
            WARNING_MSG('_eventActionAddMount: but has infinity')
            return

        if durationSeconds <= 0:
            self.addOutfitByReason(gameconst.OutfitType.mount, mountId, 0, gameconst.AddOutfitReason.Mount_EVENT)
        else:
            expireTime = utils.getNow() + durationSeconds
            self.addOutfitByReason(gameconst.OutfitType.mount, mountId, expireTime, gameconst.AddOutfitReason.Mount_EVENT)

    def _eventActionRemoveMount(self, eventActionSrc, mountId, *args, **kwargs):
        INFO_MSG('_eventActionRemoveMount', mountId)
        mountId = int(mountId)
        outfit = self.outfitInfo.getOutfitInfo(gameconst.OutfitType.mount, mountId)
        if not outfit:
            WARNING_MSG('_eventActionRemoveMount mount id invalid:', mountId)
            return

        self.outfitInfo.removeOutfit(self, gameconst.OutfitType.mount, mountId)
        self.client.onOutfitExpired([{'outfitId': outfit.outfitId, 'outfitType': outfit.outfitType}])
        self.cell.checkOutfitExpired([(outfit.outfitType, outfit.outfitId)])



