# coding: utf-8
import KBEngine
from KBEDebug import *
import iCell
import iTimer
import gameconst
import gametimer
import sMath
import utils

import duel_config as D_CD


class DuelFlag(iCell.ICell, iTimer.ITimer):
    IsDuelFlag = True

    def __init__(self):
        self.addTimerCB(D_CD.datas['duel_prepareTime']['value'], '_onReadyFinish', (), gametimer.TIMER_TAG_DUEL_PREPARE)
        interval = 1
        self.checkTimer = self.pyAddTimer(interval, interval, gametimer.DUEL_FLAG_CHECK_TICK)
        self.isFinished = False
        self.finishReason = gameconst.DuelFinishReason.NORMAL

    def _onReadyFinish(self):
        if self.isFinished:
            return

        for _adVal in self.avatarInDuelDatas:
            ent = KBEngine.entities.get(_adVal.eid)
            if not ent:
                continue

            ent.duelStart()

    def _onCheckTick(self):
        duel_specialEffectTime = D_CD.datas['duel_specialEffectTime']['value']
        for _adVal in self.avatarInDuelDatas:
            ent = KBEngine.entities.get(_adVal.eid)
            if not ent:
                self.setFinishReason(gameconst.DuelFinishReason.EXCEED_RANGE)
                self.onAvatarDuelFailed(_adVal.eid)
                break

            if ent.spaceNo != self.spaceNo:
                self.setFinishReason(gameconst.DuelFinishReason.EXCEED_RANGE)
                self.onAvatarDuelFailed(_adVal.eid)
                break

            if ent.ifSafeArea():
                self.setFinishReason(gameconst.DuelFinishReason.SAFE_AREA)
                self.onAvatarDuelFailed(_adVal.eid)
                break

            if sMath.distance2D(self.position, ent.position) > D_CD.datas['duel_battleRange']['value']:
                if not _adVal.leaveCnt:
                    ent.client.duelFlagOut()

                _adVal.leaveCnt += 1
            else:
                if _adVal.leaveCnt:
                    ent.client.duelFlagIn()

                _adVal.leaveCnt = 0

            if _adVal.leaveCnt > duel_specialEffectTime:
                self.setFinishReason(gameconst.DuelFinishReason.EXCEED_RANGE)
                self.onAvatarDuelFailed(_adVal.eid)
                break

            elif _adVal.leaveCnt:
                _left = duel_specialEffectTime - _adVal.leaveCnt + 1
                ent.showMsg(D_CD.datas['duel_exceedRange']['value'], [str(_left)])

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)

        elif userArg == gametimer.DUEL_FLAG_CHECK_TICK:
            self._onCheckTick()

        else:
            self._onTimer(tid, userArg)

    def setFinishReason(self, reason):
        self.finishReason = reason

    def onAvatarDuelFailed(self, avatarEid):
        LOG_IFO('onAvatarDuelFailed', avatarEid)
        if self.checkTimer:
            self.pyDelTimer(self.checkTimer, gametimer.DUEL_FLAG_CHECK_TICK)
            self.checkTimer = 0

        if self.isFinished:
            return

        self.isFinished = True

        winGbId = 0
        winName = ''
        for _adVal in self.avatarInDuelDatas:
            if _adVal.eid != avatarEid:
                winGbId = _adVal.gbId
                winName = _adVal.name
                break

        for _adVal in self.avatarInDuelDatas:
            _ent = KBEngine.entities.get(_adVal.eid)
            if _ent:
                _ent.onDuelFinished(self.finishReason)
            else:
                _adVal.box.cell.onDuelFinished(self.finishReason)

            _adVal.box.client.onDuelResult(winGbId, winName, self.finishReason)

        self.safeDestroy()


