# -*- coding: utf-8 -*-
import KBEngine

import gameclass
from KBEDebug import *

import iCell
import iTimer
import iFubenSpace
import iGameEntity
import iEntityRefresh
import iClient
import utils
import awardContext

import gameengine
import gameconst
import gametimer
import formula
import gameglobal
import const_const as CONST
import NPC_Pick as NPD
import NPC_pickConst as NPCST
import creep_bornState as CBSD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD



class Collection(iCell.ICell, iTimer.ITimer, iFubenSpace.IFubenSpace, iGameEntity.IGameEntity, iEntityRefresh.IEntityRefresh,
                 iClient.IClient):
    IsCollection = True
    IsCombatUnit = False

    GATHER_TRAP = 1

    def __init__(self):
        # super 形式和 直接调用形式存在混用风险
        # super(Collection, self).__init__()
        # super(iFubenSpace.IFubenSpace, self).__init__()
        iGameEntity.IGameEntity.__init__(self)
        iEntityRefresh.IEntityRefresh.__init__(self)
        self.force = gameconst.ForceTypeEnum.NPC
        self.type = NPD.datas.get(self.collectionId, {}).get('type', gameconst.CollectionType.NORMAL)
        LOG_DBG("--------create collection", self.id, self.refreshTime, self.gameEntityId, self.collectionId, self.type)

        if not self.name:
            self.name = NPD.datas.get(self.collectionId, {}).get('name', '无名采集物')

        self.initPosition()
        if NPD.datas.get(self.collectionId, {}).get('isInvalid'):
            LOG_ERR('create invalid collection!', self.collectionId)
            self.delaySafeDestroy(5)

        self._doInitBornState()

        _spaceMgr = self.spaceMgr
        gid = utils.parseGidFromGameEntityId(self.gameEntityId)
        if _spaceMgr:
            _spaceMgr.addEntity(self.id, (str(self.collectionId), 'gid_{}'.format(gid), self.__class__.__name__,))
        elif formula.inDungeonScene(self.spaceNo):
            if _spaceMgr:
                _spaceMgr.addEntity(self.id, (
                    str(self.collectionId),
                    str(self.fbEntityId), 
                    'gid_{}'.format(gid), 
                    self.__class__.__name__,
                ))
        elif _spaceMgr:
            _spaceMgr.addEntity(self.id, (str(self.collectionId), 'gid_{}'.format(gid), self.__class__.__name__,))

        self.awardContext = None
        self.createTime = utils.curTS()
        if hasattr(self, 'FBTime'):
            self.fBProtectTime = self.createTime + self.FBTime
            self.awardContext = awardContext.DropAwardCtx(self.collectionId, 1)
            self.awardContext.addContextVar('customAward', [{'itemId': self.FBItemId, 'count': 1}])

    def _doInitBornState(self):
        ifBornState = NPD.datas[self.collectionId]['ifBornState']
        if ifBornState:
            self.setBornState(gameconst.BornStateEnum.invisible)
            self.addTimerCB(CBSD.datas[ifBornState]['refreshTime'], 'setBornState',
                           (gameconst.BornStateEnum.static, ), gametimer.TIMER_TAG_CHANGE_BORN_STATE)
        else:
            self.setBornState(gameconst.BornStateEnum.move)

    def setBornState(self, newState):
        self.bornState = newState

    @property
    def creepbaseId(self):
        return self.collectionId

    def getPickTimes(self, collectionId):
        pickData = NPD.datas.get(collectionId, None)
        if not pickData:
            return 0
        return pickData['forPickTimes']

    def getSpecialPickTimes(self, collectionId):
        collData = NPD.datas.get(collectionId, None)
        if not collData:
            return 0
        return collData['timeCheck']

    def checkAIEventListened(self, eventId):
        return False

    def onTimer(self, tid, userData):
        self._onTimerTrigger(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)
        else:
            super(Collection, self).onTimer(tid, userData)

    def onCollectRewards(self, avatarId, gbId, needDestroy):
        LOG_DBG('onCollectRewards::', needDestroy)
        if not needDestroy:
            return

        spaceMgr = self.spaceMgr
        if spaceMgr:
            spaceMgr.onCollectionBeCollect(utils.parseGidFromGameEntityId(self.gameEntityId), self.creepbaseId)
            if formula.isMineWarMineArea(self.spaceNo):
                spaceMgr.onAvatarGetMineEntity(self.id, avatarId)

        if formula.inLineScene(self.spaceNo):
            lineType = formula.fetchMapId(self.spaceNo)
            gameengine.getLineStub(lineType).onCollectionBeCollectAndDestroyed(self.spaceNo, self.posIndex, self.gameEntityId)
        # TODO:: 处理非线空间的Entity

        self.delaySafeDestroy(CONST.datas.get("chestOpened", {}).get("value", 0.3))

    def onEquipDropDestroy(self, dropEquipId):
        if self.dropEquipId != dropEquipId:
            return

        LOG_INFO('Collection onEquipDropDestroy', self.id, dropEquipId)
        self.dropEquipId = 0
        self.delaySafeDestroy()

    def initPosition(self):
        if self.tmpProps.get('createCount') is None:
            self.tmpProps['createCount'] = 1
        super().initPosition()

    def _preSafeDestory(self):
        super(Collection, self)._preSafeDestory()

        spaceMgr = self.spaceMgr
        if spaceMgr:
            spaceMgr.removeEntById(self.id)
        if self.dropEquipId and self.gatherAvatarDic.get('gatherCnt', 0) == 0:
            # 过5秒后检查状态并向玩家发送提醒邮件
            KBEngine.addTimer(5, 0, lambda *args: gameengine.getGlobalBase('DropStub').sendRepairDropMail(self.dropEquipId))

    def addGatherAvatar(self, avatarId, gbId, collectionId):
        _avatar = KBEngine.entities.get(avatarId)
        collData = NPD.datas[collectionId]
        canPickTime = collData['timeCheck']
        if canPickTime:
            self.gatherAvatarDic[gbId] = self.gatherAvatarDic.get(gbId, 0) + 1
            _avatar and _avatar.checkCollectionGatherFlag(self.id)

        _pickTimes = self.getPickTimes(collectionId)

        shouldHide = collData.get('isDisappear', False)
        if canPickTime:
            if shouldHide:
                _avatar.addPickedCollections(self, canPickTime)
            else:
                _avatar.addPickedCollections(self, 0)

        if _pickTimes > 0:
            self.gatherAvatarDic['gatherCnt'] = self.gatherAvatarDic.get('gatherCnt', 0) + 1
            if self.gatherAvatarDic['gatherCnt'] >= _pickTimes:
                self.onCollectRewards(avatarId, gbId, not shouldHide) #不隐藏的就销毁
            else:
                self.onCollectRewards(avatarId, gbId, False)
            self.gatherCnt = self.gatherAvatarDic['gatherCnt']
        elif _pickTimes == 0:
            # 永久Collection, 不删除实体
            self.onCollectRewards(avatarId, gbId, False)

    def checkAvatarGather(self, avatarBase, gbId, ctx, isPicking):
        ret = self._checkAvatarGather(avatarBase, gbId)
        if not ret:
            LOG_WARN("checkAvatarGather::failed")
            return False

        # 矿战预检查
        avatar = KBEngine.entities.get(avatarBase.id)
        if avatar and not avatar.mineWarCellPrecheckCollection(self.collectionId):
            return False
        
        if self.groupLock:
            return False

        avatarBase.checkGatherCond(self.collectionId, self.id, self.dropEquipId, ctx, isPicking)
        return True

    def checkAvatarGatherFlag(self, avatarBase, gbId):
        ret = self._checkAvatarGather(avatarBase, gbId, False)
        if not avatarBase:
            return

        if not ret:
            avatarBase.onUpdateCollectionGatherFlag(self.id, 0)
        else:
            avatarBase.onUpdateCollectionGatherFlag(self.id, 1)

    def _checkAvatarGather(self, avatarBase, gbId, sendMsg=True):
        _npData = NPD.datas[self.collectionId]
        if _npData['timeCheck'] and self.gatherAvatarDic.get(gbId, 0) >= _npData['timeCheck']:
            LOG_WARN("_checkAvatarGather failed1", _npData['timeCheck'], self.gatherAvatarDic.get(gbId, 0))
            return False

        if _npData.get('isInvalid'):
            LOG_ERR('pick invalid collection!', self.collectionId)
            return False

        if not avatarBase:
            LOG_ERR('_checkAvatarGather, cannot find avatar111', avatarBase)
            return False

        canPickTime = _npData['timeCheck']
        if canPickTime:
            avatar = KBEngine.entities.get(avatarBase.id)
            if not avatar or avatar.isDestroyed:
                LOG_ERR('_checkAvatarGather, cannot find avatar', avatarBase)
                return False
            curTime = avatar.getCollectionAlreadyPickTime(self.collectionId)
            if curTime<0 or curTime>=canPickTime:
                LOG_WARN("_checkAvatarGather failed2", canPickTime, curTime)
                return False

        pickTimes = self.getPickTimes(self.collectionId)

        if pickTimes and self.gatherAvatarDic.get('gatherCnt', 0) >= pickTimes:
            return False

        if hasattr(self, 'firstBloodTargetGbIds'):
            #LOG_INFO("firstBloodTargetGbIds", self.firstBloodTargetGbIds)
            if gbId not in self.firstBloodTargetGbIds:
                if utils.curTS() - self.createTime < self.FBTime:
                    return False

        return True

    def checkAvatarGatherPickTimes(self, avatarBase, gbId):
        curPickTimes, pickTimes = self.getGatherPickTimes(gbId)

        if avatarBase.client:
            LOG_DBG("onUpdateCollectionGatherPickTimes", self.id, curPickTimes, pickTimes)
            avatarBase.client.onUpdateCollectionGatherPickTimes(self.id, curPickTimes, pickTimes)

    def getGatherPickTimes(self, gbId):
        if self.type not in gameconst.CollectionType.ADD_PICK_AVATAR_CNT:
            return self.gatherAvatarDic.get('gatherCnt', 0), self.getPickTimes(self.collectionId)

        return self.gatherAvatarDic.get(gbId, 0), self.getSpecialPickTimes(self.collectionId)

    def setSpecialGatherAvatar(self, avatarId, gbId, gatherCnt):
        if self.type not in gameconst.CollectionType.ADD_PICK_AVATAR_CNT:
            return

        self.gatherAvatarDic[gbId] = gatherCnt

    def onDestroy(self):
        super().onDestroy()
        if self.refreshTime > 0:
            self.onEntityRefresh()

        if KBEngine.isShuttingDown() and self.dropEquipId:
            LOG_ERR('Collection onDestroy', self.id, KBEngine.isShuttingDown())
            _collEndTime = utils.curTS() + 60
            gameengine.getGlobalBase('DropStub').updateCollEndTime(self.dropEquipId, _collEndTime)

    def onEntityRefresh(self):
        # 解耦，spaceNo在iCell， posIndex 在iGameEntity
        super().onEntityRefresh(self.spaceNo, self.calculateRefreshTime())
