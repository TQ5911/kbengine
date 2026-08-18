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
import gamedecorator
import gameconfig


class IMount(object):
    def __init__(self):
        pass

    def mountOnLogin(self):
        for outfit in self.outfitInfo.outfitDic.values():
            if outfit.outfitType == gameconst.OutfitEnum.mount:
                configData = dataUtils.getOutfitConfigData(outfit.outfitType, outfit.outfitId)
                if configData:
                    prop = configData.get('prop', [])
                    if prop:
                        self.cell.updatePropByMount(outfit.outfitId, True)

    def doAddMount(self, pid, mountId, durationDays):
        LOG_INFO('doAddMount:', pid, mountId, durationDays)
        outfit = self.outfitInfo.getOutfitInfo(gameconst.OutfitEnum.mount, mountId)
        hasUnlock = False
        if outfit:
            if not outfit.expireTime:
                hasUnlock = True
                if not durationDays:
                    self.cell.onPendingUseItemFinished(pid, gameconst.UseItemEnum.FALSE)
                return
            else:
                if durationDays:
                    self.cell.onPendingUseItemFinished(pid, gameconst.UseItemEnum.FALSE)
                    return

        if durationDays <= 0:
            self.addOutfitByReason(gameconst.OutfitEnum.mount, mountId, 0, gameconst.AddOutfitReason.MOUNT_ITEM)
        else:
            expireTime = utils.curTS() + int(durationDays * gameconst.ONE_DAY_COST_SECONDS)
            self.addOutfitByReason(gameconst.OutfitEnum.mount, mountId, expireTime, gameconst.AddOutfitReason.MOUNT_ITEM)

        self.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetMountActivated'])

        if not gameconfig.isCrossServer():
            self.cell.onPendingUseItemFinished(pid, gameconst.UseItemEnum.TRUE)
        self.onMessagePre(MMD.datas.useMountsItemSuccess, [MOUNTS.datas[mountId]['name']])

        if not hasUnlock and not durationDays:
            self.achievementInfo.triggerAchieveByType(
                self, 
                gameconst.AchieveType.UNLOCK_MOUNT, 
                actionContext.AchievementCtx())
        
        #目前只有使用道具添加坐骑，所以这里直接同步
        self.syncMethodCallToCrossServerBase('onLocalServerDoAddMount', (pid, mountId, durationDays))

    def onLocalServerDoAddMount(self, pid, mountId, durationDays):
        LOG_INFO('onLocalServerDoAddMount:', pid, mountId, durationDays)
        self.doAddMount(pid, mountId, durationDays)

    @gamedecorator.crossServer
    def setCurMount(self, exposed, mountId):
        self._setCurMount(mountId)
        self.syncMethodCallToLocalServerBase('_setCurMount', (mountId,))

    def _setCurMount(self, mountId):
        LOG_INFO(' set cur mount:', mountId)
        outfit = self.outfitInfo.getOutfitInfo(gameconst.OutfitEnum.mount, mountId)
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

        outfit = self.outfitInfo.getOutfitInfo(gameconst.OutfitEnum.mount, mountId)
        if outfit and not outfit.expireTime:
            LOG_WARN('_eventActionAddMount: but has infinity')
            return

        if durationSeconds <= 0:
            self.addOutfitByReason(gameconst.OutfitEnum.mount, mountId, 0, gameconst.AddOutfitReason.MOUNT_EVENT)
        else:
            expireTime = utils.curTS() + durationSeconds
            self.addOutfitByReason(gameconst.OutfitEnum.mount, mountId, expireTime, gameconst.AddOutfitReason.MOUNT_EVENT)

    def _eventActionRemoveMount(self, eventActionSrc, mountId, *args, **kwargs):
        LOG_INFO('_eventActionRemoveMount', mountId)
        mountId = int(mountId)
        outfit = self.outfitInfo.getOutfitInfo(gameconst.OutfitEnum.mount, mountId)
        if not outfit:
            LOG_WARN('_eventActionRemoveMount mount id invalid:', mountId)
            return

        self.outfitInfo.removeOutfit(self, gameconst.OutfitEnum.mount, mountId)
        self.cell.checkOutfitExpired([(outfit.outfitType, outfit.outfitId)])



