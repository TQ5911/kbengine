# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import gametimer
import gameconst

import iBaseWithCell
import iFubenSpace
import iTimer
import utils

import creep_group as CRG


class MonsterGrp(iBaseWithCell.IBaseWithCell, iFubenSpace.IFubenSpace,
                 iTimer.ITimer):

    def __init__(self):
        super(MonsterGrp, self).__init__()

    def onLoseCell(self, reason=gameconst.OnLoseCellReason.DEFAULT):
        if self.isDestroyed:
            return

        self.destroy(writeToDB=False)
        return

    def onTimer(self, tid, userArg):
        self._onTimer(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)

    def createMonstersFromGrp(self, p):
        LOG_DBG('MonsterGrp::createMonstersFromGrp')
        self._monsterIDs = []

        _gP = CRG.datas.get(p['groupId'])

        if 'name' in _gP:
            self.groupName = _gP['name']

        _gPgms = _gP['group']

        _gPgmsItems = _gPgms.items()

        _totalCount = sum((i[1] for i in _gPgmsItems))

        for _idx, (_mid, _mcount) in enumerate(_gPgmsItems):
            params = {
                'monsterId': _mid,
                'spaceNo': p['spaceNo'],
                'gameEntityId': p['gameEntityId'],
                'position': p['position'],
                'monsterGroupId': self.id,
                'direction': p['direction'],
                'bornRadius': p['bornRadius'],
                'level': p.get('level', gameconst.MIN_LEVEL)
            }

            if _idx > 0:
                self.addTimerCB(
                    _idx, '_createMonstersFromGrp',
                    (params, 0, gameconst.INIT_EACH_EN_LOOP_COUNT, _mcount), gametimer.TIMER_TAG_CREATE_MONSTERS_FROM_GRP)
            else:
                self._createMonstersFromGrp(
                    params, 0, gameconst.INIT_EACH_EN_LOOP_COUNT, _mcount)

        self.syncCreatedMonstersToCell(self._monsterIDs, _totalCount)

    def _createMonstersFromGrp(self, params, idx, loopCount, totalCount):
        for i in range(idx, idx + loopCount):
            if i >= totalCount:
                return

            params.update({'tmpProps': {'createCount': totalCount,
                                        'createRadius': params['bornRadius'],
                                        'createIndex': i}})

            en = KBEngine.createEntityLocally('Monster', params)

            self._monsterIDs.append(en.id)

        self.addTimerCB(0.2, '_createMonstersFromGrp',
                       (params, idx + loopCount, loopCount, totalCount), gametimer.TIMER_TAG_CREATE_MONSTERS_FROM_GRP)

    def syncCreatedMonstersToCell(self, ids, totalCount):
        if not self.cell or len(ids) < totalCount:
            LOG_IFO('Still waiting for creating monsters.')
            self.addTimerCB(0.5, 'syncCreatedMonstersToCell', (ids, totalCount), gametimer.TIMER_TAG_SYNC_CREATED_MONSTERS_TO_CELL)
            return

        self.cell.initFromBase(ids)

        del self._monsterIDs
