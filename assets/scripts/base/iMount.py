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
        LOG_INFO('doAddMount:', pid, mountId, durationDays)
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
            self.addOutfitByReason(gameconst.OutfitType.mount, mountId, 0, gameconst.AddOutfitReason.MOUNT_ITEM)
        else:
            expireTime = utils.curTS() + int(durationDays * gameconst.ONE_DAY_COST_SECONDS)
            self.addOutfitByReason(gameconst.OutfitType.mount, mountId, expireTime, gameconst.AddOutfitReason.MOUNT_ITEM)

        self.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetMountActivated'])

        self.cell.onPendingUseItem(pid, gameconst.UseItem.TRUE)
        self.onMessagePre(MMD.datas.useMountsItemSuccess, [MOUNTS.datas[mountId]['name']])

        if not hasUnlock and not durationDays:
            self.achievementInfo.triggerAchieveByType(
                self, 
                gameconst.AchieveType.UNLOCK_MOUNT, 
                actionContext.AchievementCtx())

    def setCurMount(self, exposed, mountId):
        LOG_INFO(' set cur mount:', mountId)
        outfit = self.outfitInfo.getOutfitInfo(gameconst.OutfitType.mount, mountId)
        if outfit is None:
            return

        if outfit.expireTime and outfit.expireTime <= utils.curTS():
            return

        self.cell.setCurMountCell(mountId)
        self.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetMountRide'])

    def _eventActionAddMount(self, eventActionSrc, mountId, durationDays, *args, **kwargs):
        LOG_INFO('_eventActionAddMount:', mountId, durationDays)
        durationSeconds = int(float(durationDays) * gameconst.ONE_DAY_COST_SECONDS)
        mountId = int(mountId)
        if mountId not in MOUNTS.datas:
            LOG_ERR('_eventActionAddMount but mount id invalid:', mountId)
            return

        outfit = self.outfitInfo.getOutfitInfo(gameconst.OutfitType.mount, mountId)
        if outfit and not outfit.expireTime:
            LOG_WARN('_eventActionAddMount: but has infinity')
            return

        if durationSeconds <= 0:
            self.addOutfitByReason(gameconst.OutfitType.mount, mountId, 0, gameconst.AddOutfitReason.MOUNT_EVENT)
        else:
            expireTime = utils.curTS() + durationSeconds
            self.addOutfitByReason(gameconst.OutfitType.mount, mountId, expireTime, gameconst.AddOutfitReason.MOUNT_EVENT)

    def _eventActionRemoveMount(self, eventActionSrc, mountId, *args, **kwargs):
        LOG_INFO('_eventActionRemoveMount', mountId)
        mountId = int(mountId)
        outfit = self.outfitInfo.getOutfitInfo(gameconst.OutfitType.mount, mountId)
        if not outfit:
            LOG_WARN('_eventActionRemoveMount mount id invalid:', mountId)
            return

        self.outfitInfo.removeOutfit(self, gameconst.OutfitType.mount, mountId)
        self.cell.checkOutfitExpired([(outfit.outfitType, outfit.outfitId)])



