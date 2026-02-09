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

import gameengine
import gameconst
import gametimer
import formula
import gameglobal
import const_const as CONST
import NPC_Pick as NPD
import NPC_pickConst as NPCST
import NPC_pickTimes as NPPT
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
        self.force = gameconst.ForceType.NPC
        self.type = NPD.datas.get(self.collectionId, {}).get('type', gameconst.CollectionType.NORMAL)
        DEBUG_MSG("--------create collection", self.id, self.refreshTime, self.gameEntityId, self.collectionId, self.type)

        if not self.name:
            self.name = NPD.datas.get(self.collectionId, {}).get('name', '无名采集物')

        self.initPosition()
        if NPD.datas.get(self.collectionId, {}).get('isInvalid'):
            ERROR_MSG('create invalid collection!', self.collectionId)
            self.delaySafeDestroy(5)

        self._initBornState()

        spaceMgr = self.spaceMgr
        gid = utils.getGidFromGameEntityId(self.gameEntityId)
        if spaceMgr:
            spaceMgr.addEntity(self.id, (str(self.collectionId), 'gid_{}'.format(gid), self.__class__.__name__,))
        elif formula.isDungeonSpace(self.spaceNo):
            if spaceMgr:
                spaceMgr.addEntity(self.id, (str(self.fbEntityId), str(self.collectionId),
                                             'gid_{}'.format(gid), self.__class__.__name__,))
        elif spaceMgr:
            spaceMgr.addEntity(self.id, (str(self.collectionId), 'gid_{}'.format(gid), self.__class__.__name__,))


    def _initBornState(self):
        ifBornState = NPD.datas[self.collectionId]['ifBornState']
        if ifBornState:
            self.changeBornState(gameconst.BornStateType.invisible)
            self._callback(CBSD.datas[ifBornState]['refreshTime'], 'changeBornState',
                           (gameconst.BornStateType.static, ), gametimer.TIMER_TAG_CHANGE_BORN_STATE)
        else:
            self.changeBornState(gameconst.BornStateType.move)

    def changeBornState(self, newState):
        self.bornState = newState

    @property
    def creepBaseId(self):
        return self.collectionId

    def getPickTimes(self, collectionId):
        pickData = NPPT.datas.get(collectionId, None)
        if not pickData:
            return 0
        return pickData['pickTimes']

    def getSpecialPickTimes(self, collectionId):
        collData = NPD.datas.get(collectionId, None)
        if not collData:
            return 0
        return collData['timeCheck']

    def checkEventListened(self, eventId):
        return False

    def onTimer(self, tid, userData):
        self._onTimer(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)
        else:
            super(Collection, self).onTimer(tid, userData)

    def onCollectRewards(self, avatarId, gbId, needDestroy):
        DEBUG_MSG('onCollectRewards::', needDestroy)
        if not needDestroy:
            return

        spaceMgr = self.spaceMgr
        if spaceMgr:
            spaceMgr.onCollectionBeCollect(utils.getGidFromGameEntityId(self.gameEntityId), self.creepBaseId)

        if formula.isLineSpace(self.spaceNo):
            lineType = formula.getMapId(self.spaceNo)
            gameengine.getLineStub(lineType).onCollectionBeCollectAndDestroyed(self.spaceNo, self.posIndex, self.gameEntityId)
        # TODO:: 处理非线空间的Entity

        self.delaySafeDestroy(CONST.datas.get("chestOpened", {}).get("value", 0.3))

    def onEquipDropDestroy(self, dropEquipId):
        if self.dropEquipId != dropEquipId:
            return

        INFO_MSG('Collection onEquipDropDestroy', self.id, dropEquipId)
        self.dropEquipId = 0
        self.delaySafeDestroy()

    def _preSafeDestory(self):
        super()._preSafeDestory()

        spaceMgr = self.spaceMgr
        if spaceMgr:
            spaceMgr.removeEntityById(self.id)
        if self.dropEquipId and self.gatherAvatars.get('gatherCnt', 0) == 0:
            # 过5秒后检查状态并向玩家发送提醒邮件
            KBEngine.addTimer(5, 0, lambda *args: gameengine.getGlobalBase('DropStub').sendRepairDropMail(self.dropEquipId))

    def initPosition(self):
        if self.tmpProps.get('createCount', None) is None:
            self.tmpProps['createCount'] = 1
        super().initPosition()

    def addGatherAvatar(self, avatarId, gbId, collectionId):
        avatar = KBEngine.entities.get(avatarId)
        collData = NPD.datas[collectionId]
        canPickTime = collData['timeCheck']
        if canPickTime:
            self.gatherAvatars[gbId] = self.gatherAvatars.get(gbId, 0) + 1
            avatar and avatar.checkCollectionGatherFlag(self.id)

        pickTimes = self.getPickTimes(collectionId)

        shouldHide = collData.get('isDisappear', False)
        if canPickTime:
            if shouldHide:
                avatar.addPickedCollections(self, canPickTime)
            else:
                avatar.addPickedCollections(self, 0)

        if pickTimes > 0:
            self.gatherAvatars['gatherCnt'] = self.gatherAvatars.get('gatherCnt', 0) + 1
            if self.gatherAvatars['gatherCnt'] >= pickTimes:
                self.onCollectRewards(avatarId, gbId, not shouldHide) #不隐藏的就销毁
            else:
                self.onCollectRewards(avatarId, gbId, False)
            self.gatherCnt = self.gatherAvatars['gatherCnt']
        elif pickTimes == 0:
            # 永久Collection, 不删除实体
            self.onCollectRewards(avatarId, gbId, False)


    def checkAvatarGather(self, avatarBase, gbId, ctx):
        ret = self._checkAvatarGather(avatarBase, gbId)
        if not ret:
            WARNING_MSG("checkAvatarGather::failed")
            return False

        # 矿战预检查
        avatar = KBEngine.entities.get(avatarBase.id)
        if avatar and not avatar.mineWarCellPrecheckCollection(self.collectionId):
            return False

        avatarBase.checkGatherCond(self.collectionId, self.id, self.dropEquipId, ctx)
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
        npData = NPD.datas[self.collectionId]
        if npData['timeCheck'] and self.gatherAvatars.get(gbId, 0) >= npData['timeCheck']:
            WARNING_MSG("_checkAvatarGather failed1", npData['timeCheck'], self.gatherAvatars.get(gbId, 0))
            return False

        if npData.get('isInvalid'):
            ERROR_MSG('pick invalid collection!', self.collectionId)
            return False

        if not avatarBase:
            ERROR_MSG('_checkAvatarGather, cannot find avatar111', avatarBase)
            return False

        canPickTime = npData['timeCheck']
        if canPickTime:
            avatar = KBEngine.entities.get(avatarBase.id)
            if not avatar or avatar.isDestroyed:
                ERROR_MSG('_checkAvatarGather, cannot find avatar', avatarBase)
                return False
            curTime = avatar.getCollectionAlreadyPickTime(self.collectionId)
            if curTime<0 or curTime>=canPickTime:
                WARNING_MSG("_checkAvatarGather failed2", canPickTime, curTime)
                return False

        pickTimes = self.getPickTimes(self.collectionId)

        if pickTimes and self.gatherAvatars.get('gatherCnt', 0) >= pickTimes:
            return False

        return True

    def checkAvatarGatherPickTimes(self, avatarBase, gbId):
        curPickTimes, pickTimes = self.getGatherPickTimes(gbId)

        if avatarBase.client:
            DEBUG_MSG("onUpdateCollectionGatherPickTimes", self.id, curPickTimes, pickTimes)
            avatarBase.client.onUpdateCollectionGatherPickTimes(self.id, curPickTimes, pickTimes)

    def getGatherPickTimes(self, gbId):
        if self.type not in (gameconst.CollectionType.PERSONAL_BOX, gameconst.CollectionType.VIEWPOINT):
            return self.gatherAvatars.get('gatherCnt', 0), self.getPickTimes(self.collectionId)

        return self.gatherAvatars.get(gbId, 0), self.getSpecialPickTimes(self.collectionId)

    def setSpecialGatherAvatar(self, avatarId, gbId, gatherCnt):
        if self.type not in (gameconst.CollectionType.PERSONAL_BOX, gameconst.CollectionType.VIEWPOINT):
            return

        self.gatherAvatars[gbId] = gatherCnt

    def onDestroy(self):
        super().onDestroy()
        if self.refreshTime > 0:
            self.onEntityRefresh()

        if KBEngine.isShuttingDown() and self.dropEquipId:
            ERROR_MSG('Collection onDestroy', self.id, KBEngine.isShuttingDown())
            _collEndTime = utils.getNow() + 60
            gameengine.getGlobalBase('DropStub').updateCollEndTime(self.dropEquipId, _collEndTime)

    def onEntityRefresh(self):
        # 解耦，spaceNo在iCell， posIndex 在iGameEntity
        super().onEntityRefresh(self.spaceNo, self.calculateRefreshTime())
