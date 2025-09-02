# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import formula
import gameengine
import iStaticSpaceMgr
import wonderLand_config as WL_CD
import utils
import random
import math
import gametimer
import iTimer
import iCollectionBossForMgr


class WonderLandSpaceMgr(iCollectionBossForMgr.ICollectionBossForMgr, iStaticSpaceMgr.IStaticSpaceMgr):
    def __init__(self):
        INFO_MSG("WonderLandSpaceMgr __init__")
        iStaticSpaceMgr.IStaticSpaceMgr.__init__(self)
        iCollectionBossForMgr.ICollectionBossForMgr.__init__(self)
        gameengine.getWonderLandStubBySpaceNo(self.spaceNo).onSpaceMgrReady(self.spaceNo, self)
        self._callback(1, 'summonRandomBoss', (), gametimer.TIMER_TAG_SUMMON_RANDOM_BOSS)

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        else:
            self._onTimer(tid, userArg)

    def initStaticSpace(self):
        super().initStaticSpace()

    def addEntity(self, entId, tags):
        super(WonderLandSpaceMgr, self).addEntity(entId, tags)

    def removeEntityById(self, entId):
        if entId == self.randomBossId:
            self.onRandomBossDie()

        super(WonderLandSpaceMgr, self).removeEntityById(entId)

    def onPlayerRelogin(self, box, playerGbId):
        super().onPlayerRelogin(box, playerGbId)

    def summonRandomBoss(self):
        INFO_MSG("summonRandomBoss")
        _dungeonNo = formula.getMapId(self.spaceNo)
        _dunData = utils.getDunStructureModuleData(_dungeonNo)
        if not _dunData:
            ERROR_MSG("summonRandomBoss: _dunData is None", self.spaceNo)
            return

        _initEntities = _dunData.get('InitEntities')
        if not _initEntities:
            ERROR_MSG("summonRandomBoss: _initEntities is None", self.spaceNo)
            return

        _monsters = _initEntities.get('Monster')
        if not _monsters:
            ERROR_MSG("summonRandomBoss: _monsters is None", self.spaceNo)
            return

        _bossList = []
        for _data in _monsters.values():
            if _data['CustomID'] != 'randomBoss':
                continue

            _bossList.append(_data)

        if not _bossList:
            ERROR_MSG("summonRandomBoss: _bossList is None")
            return

        _bossData = random.choice(_bossList)
        _pos = (_bossData['PosX'], _bossData['PosY'], _bossData['PosZ'])
        _dir = (0.0, 0.0, _bossData['Dir'] * math.pi / 180)
        _params = {
            'position': _pos,
            'direction': _dir,
            'spaceNo': self.spaceNo,
            'spaceno': self.spaceNo,
            'monsterId': _bossData['EntityID'],
            'level': int(_bossData['Props']['Level']),
            'spaceMgrId': self.id,
        }

        _boss = KBEngine.createEntity('Monster', self.spaceID, _pos, _dir, _params)
        self.randomBossId = _boss.id
        self.randomBossGameEntityId = _bossData['ID']

        _msgId = utils.getNeedTranslateMsgId(WL_CD.datas['wonderLand_randomBossAppear']['value'])
        _args = [utils.getNeedTranslateArg(_boss.name)]
        self.syncPlayer(lambda playerEnt: playerEnt.showMsg(_msgId, _args))

    def onRandomBossDie(self):
        self.randomBossId = 0
        _gameEntityId = self.randomBossGameEntityId
        self.randomBossGameEntityId = 0

        _dungeonNo = formula.getMapId(self.spaceNo)
        _bossData = utils.getDunStructureModuleData(_dungeonNo)
        _bossData = _bossData['InitEntities']['Monster'][str(_gameEntityId)]

        _delay = _bossData['Props']['RefreshTime']
        self._callback(_delay, 'summonRandomBoss', (), gametimer.TIMER_TAG_SUMMON_RANDOM_BOSS)

