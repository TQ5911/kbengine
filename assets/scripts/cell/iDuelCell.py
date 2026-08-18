# coding: utf-8
import KBEngine
from KBEDebug import *
import formula
import gameglobal
import utils
import gameconst
import sMath
import AvatarInDuelInfo
import DuelAttrInfo
import gametimer
import gamedecorator
import duel_config as D_CD
import conflict_conflict_def as C_C_DD
import conflict_status_def as C_SD
import gamePlay_gamePlay as GP_GPD
import worldConfig_Area as WC_AD
import buff_buff as B_BD


class IDuelCell(object):
    # type hint
    id: int
    duelAttr: DuelAttrInfo.DuelAttrVal
    duelBlackDict: dict

    @gamedecorator.checkGameconfigEnable('duel')
    @utils.isMyself
    def reqDuel(self, exposed, targetId):
        LOG_INFO('reqDuel: ', targetId)
        if formula.inMineWarScene(self.spaceNo):
            if gameglobal.mineGlobalData.mineWarState == gameconst.MINE_WAR_STATE.RUNNING:
                self.showMsg(D_CD.datas['duel_wrongState1']['value'], [])
                return

        _mapId = formula.fetchMapId(self.spaceNo)
        if not GP_GPD.datas[_mapId].get('ifSinglePK', 0):
            self.showMsg(D_CD.datas['duel_forbidScene']['value'], [])
            return

        if self.ifSafeArea():
            LOG_ERR('reqDuel in safe area:', targetId)
            return

        if targetId == self.id:
            LOG_ERR('reqDuel cannot duel with yourself:', targetId)
            return

        target = KBEngine.entities.get(targetId)
        if not target:
            LOG_ERR('reqDuel target not found:', targetId)
            return

        if not self.checkConflictState(C_C_DD.datas.duel, bMsg=False):
            self.showMsg(D_CD.datas['duel_wrongState1']['value'], [])
            return

        if not target.checkConflictState(C_C_DD.datas.duel, bMsg=False):
            self.showMsg(D_CD.datas['duel_wrongState2']['value'], [])
            return

        if self.duelAttr.inDuel():
            LOG_ERR('reqDuel cannot duel while already in duel:', targetId)
            return

        if target.duelAttr.inDuel():
            LOG_ERR('reqDuel target is already in duel:', targetId)
            return

        _radius = D_CD.datas['duel_battleRange']['value']
        if sMath.distance2D(self.position, target.position) > _radius * 2:
            LOG_ERR('reqDuel distance too far:', targetId)
            return

        if self._inDuelRequest():
            self.showMsg(D_CD.datas['duel_interceptApplication']['value'], [])
            return

        if target.inRecvDuelRequest():
            self.showMsg(D_CD.datas['duel_alreadyApplied']['value'], [])
            return

        if self.id in target.duelBlackDict:
            LOG_ERR('reqDuel target is in duel black list:', targetId)
            return

        self.duelRequestId = targetId
        # 多延迟两秒，防止客户端超时后拒绝过早
        self.duelReqEndTime = utils.curTS() + D_CD.datas['duel_autoRefuseTime']['value'] + 2

        target.currentRecvDuelReqId = self.id
        target.recvDuelReqEndTime = self.duelReqEndTime

        target.client.onRecvDuelReq(self.id, self.name)
        self.showMsg(D_CD.datas['duel_waitAccept']['value'], [])

    def changeToDuelReady(self, eid):
        self.duelAttr.readyDuel(eid)
        self.clearDuelRequest()

    def clearDuelRequest(self):
        self.duelRequestId = 0
        self.duelReqEndTime = 0
        self.currentRecvDuelReqId = 0
        self.recvDuelReqEndTime = 0

    # 是否在duel请求中
    def _inDuelRequest(self):
        if self.duelReqEndTime < utils.curTS():
            return False

        return self.duelRequestId != 0

    # 是否在接收duel请求中
    def inRecvDuelRequest(self):
        if self.recvDuelReqEndTime < utils.curTS():
            return False

        return self.currentRecvDuelReqId != 0

    @property
    def duelRequestId(self):
        return self.getTempMiscProp(gameconst.EntityPropsEnum.duelRequestId, 0)

    @duelRequestId.setter
    def duelRequestId(self, value):
        if value:
            self.setTempMiscProp(gameconst.EntityPropsEnum.duelRequestId, value)
        else:
            self.popTempMiscProp(gameconst.EntityPropsEnum.duelRequestId)

    @property
    def currentRecvDuelReqId(self):
        return self.getTempMiscProp(gameconst.EntityPropsEnum.currentRecvDuelReqId, 0)

    @currentRecvDuelReqId.setter
    def currentRecvDuelReqId(self, value):
        if value:
            self.setTempMiscProp(gameconst.EntityPropsEnum.currentRecvDuelReqId, value)
        else:
            self.popTempMiscProp(gameconst.EntityPropsEnum.currentRecvDuelReqId)

    @property
    def duelReqEndTime(self):
        return self.getTempMiscProp(gameconst.EntityPropsEnum.duelReqEndTime, 0)

    @duelReqEndTime.setter
    def duelReqEndTime(self, value):
        if value:
            self.setTempMiscProp(gameconst.EntityPropsEnum.duelReqEndTime, value)
        else:
            self.popTempMiscProp(gameconst.EntityPropsEnum.duelReqEndTime)

    @property
    def recvDuelReqEndTime(self):
        return self.getTempMiscProp(gameconst.EntityPropsEnum.RecvDuelReqEndTime, 0)

    @recvDuelReqEndTime.setter
    def recvDuelReqEndTime(self, value):
        if value:
            self.setTempMiscProp(gameconst.EntityPropsEnum.RecvDuelReqEndTime, value)
        else:
            self.popTempMiscProp(gameconst.EntityPropsEnum.RecvDuelReqEndTime)

    def _removeDuelBlack(self, targetId):
        self.duelBlackDict.pop(targetId, None)

    def clearAllRequest(self, target):
        self.clearDuelRequest()

        if target:
            target.clearDuelRequest()

    def _rejectDuelReq(self, isBlack):
        target = KBEngine.entities.get(self.currentRecvDuelReqId)
        self.clearAllRequest(target)

        if not target:
            return

        if isBlack:
            self.duelBlackDict[target.id] = 1
            _delay = D_CD.datas['duel_disturbRefuseTime']['value'] * 60
            self.addTimerCB(_delay, '_removeDuelBlack', (target.id,), gametimer.TIMER_TAG_DUEL_BLACK)

    @gamedecorator.checkGameconfigEnable('duel')
    @utils.isMyself
    def dealDuelReq(self, exposed, accept, isBlack):
        LOG_INFO('dealDuelReq: ', accept, isBlack)
        if formula.inMineWarScene(self.spaceNo):
            if gameglobal.mineGlobalData.mineWarState == gameconst.MINE_WAR_STATE.RUNNING:
                self.showMsg(D_CD.datas['duel_wrongState1']['value'], [])
                return

        if not accept:
            self._rejectDuelReq(isBlack)
            return

        if not self.inRecvDuelRequest():
            self.showMsg(D_CD.datas['duel_wrongState1']['value'], [])
            return

        if self.ifSafeArea():
            self.showMsg(D_CD.datas['duel_forbidScene']['value'], [])
            return

        target = KBEngine.entities.get(self.currentRecvDuelReqId)
        if not target:
            LOG_WARN('dealDuelReq target not found:', self.id, self.currentRecvDuelReqId, self.recvDuelReqEndTime)
            return

        if target.ifSafeArea():
            self.showMsg(D_CD.datas['duel_wrongState2']['value'], [])
            return

        _radius = D_CD.datas['duel_battleRange']['value']
        if sMath.distance2D(self.position, target.position) > _radius * 2:
            self.showMsg(D_CD.datas['duel_exceedRangeTips']['value'], [])
            self.clearAllRequest(target)
            return

        _mapId = formula.fetchMapId(self.spaceNo)
        if not GP_GPD.datas[_mapId].get('ifSinglePK', 0):
            self.showMsg(D_CD.datas['duel_forbidScene']['value'], [])
            self.clearAllRequest(target)
            return

        if not self.checkConflictState(C_C_DD.datas.duel, bMsg=False):
            self.showMsg(D_CD.datas['duel_wrongState1']['value'], [])
            self.clearAllRequest(target)
            return

        if not target.checkConflictState(C_C_DD.datas.duel, bMsg=False):
            self.showMsg(D_CD.datas['duel_wrongState2']['value'], [])
            self.clearAllRequest(target)
            return

        self.setState(C_SD.datas.duel)
        target.setState(C_SD.datas.duel)

        self.changeToDuelReady(self.currentRecvDuelReqId)
        target.changeToDuelReady(self.id)

        pos = (
            (self.position[0] + target.position[0]) / 2,
            (self.position[1] + target.position[1]) / 2,
            (self.position[2] + target.position[2]) / 2,
        )

        dir = (0, 0, 0)

        avatarInDuelDatas = []
        avatarInDuelDatas.append(
            AvatarInDuelInfo.AvatarInDuelVal(
                gbId=self.id,
                box=self.base,
                eid=self.id,
                name=self.name,
            )
        )

        avatarInDuelDatas.append(
            AvatarInDuelInfo.AvatarInDuelVal(
                gbId=target.id,
                box=target.base,
                eid=target.id,
                name=target.name,
            )
        )
        params = {
            'position': pos,
            'direction': dir,
            'avatarInDuelDatas': avatarInDuelDatas,
            'spaceNo': self.spaceNo,
        }

        duelFlag = KBEngine.createEntity('DuelFlag', self.spaceID, pos, dir, params)
        self.duelAttr.setDuelFlagId(duelFlag.id)
        target.duelAttr.setDuelFlagId(duelFlag.id)

        self.duelAttr = self.duelAttr
        target.duelAttr = target.duelAttr

        self.resetAllTargetTypeCache()
        target.resetAllTargetTypeCache()

    # 正式开打
    def duelStart(self):
        self.duelAttr.startFight()
        self.resetAllTargetTypeCache()
        self.client.onDuelFlagsChanged(self.duelAttr.duelFlags)

    def leaveDuelState(self):
        self.removeState(C_SD.datas.Fighting, gameconst.RemoveStateReason.EXIT_DUEL)
        self.duelAttr.reset()
        self.duelAttr = self.duelAttr
        self.resetAllTargetTypeCache()

        if formula.inDuelScene(self.spaceNo):
            if self.mp != self.fullMp:
                _delta = self.fullMp - self.mp
                self.modifyMP(_delta)

            if self.hp != self.fullHp:
                _delta = self.fullHp - self.hp
                self.modifyHP(_delta, self.id, gameconst.SourceType.SrcTpDuelEnd, self.id)

        self.removeBuffsByTag('duelClear')

        self.showPkModelMsg(self.pkModel)

    def onDuelFinished(self, finishReason):
        self.removeState(C_SD.datas.duel)
        self.base.completeGuildTask(
            gameconst.GuildTaskType.DUEL,
            0,
            1,
        )

    def getDuelDeathHp(self, oldHp):
        if formula.inDuelScene(self.spaceNo):
            return self.fullHp

        _minHp = int(self.fullHp * gameconst.DUEL_RECOVER_PERCENT)

        return max(_minHp, oldHp)

    def isLightningArea(self):
        return self.getTempMiscProp(gameconst.EntityPropsEnum.isLightningArea, 0)

    def ifSafeArea(self):
        if not (formula.inWorldLineScene(self.spaceNo) and self.areaId):
            return False

        _areaData = WC_AD.datas.get(self.areaId)
        if not _areaData:
            return False

        return _areaData.get('ifSafeArea', 0)

    def onBeDamagedInDuel(self, srcEntId):
        _ent = KBEngine.entities.get(srcEntId)
        if not _ent:
            return

        _ent = utils.getEntityRealEntity(_ent)
        if self.duelAttr.isDuelEnemy(_ent):
            return

        if _ent.id == self.id:
            return

        _duelFlag = self.duelAttr.duelFlagEnt()
        if not _duelFlag:
            return

        _duelFlag.setFinishReason(gameconst.DuelFinishReason.THIRD_DAMAGE)
        if self.pkModel == gameconst.PKModelEnum.PEACE and not self.inRedName():
            self._setPKModel(gameconst.PKModelEnum.JUSTICE, False, False)
        _duelFlag.onAvatarDuelFailed(self.id)

