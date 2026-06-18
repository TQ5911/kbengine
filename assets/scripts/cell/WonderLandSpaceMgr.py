# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import formula
import gameengine
import iStaticSpaceMgr
import wonderLand_config as WL_CD
import creep_base as CBD
import utils
import random
import math
import gametimer
import iTimer
import gameconst
import iCollectionBossForMgr
import branchData_set as BDS

class WonderLandSpaceMgr(iCollectionBossForMgr.ICollectionBossForMgr, iStaticSpaceMgr.IStaticSpaceMgr):
    def __init__(self):
        LOG_INFO("WonderLandSpaceMgr __init__")
        iStaticSpaceMgr.IStaticSpaceMgr.__init__(self)
        iCollectionBossForMgr.ICollectionBossForMgr.__init__(self)
        gameengine.getWonderLandStubBySpaceNo(self.spaceNo).onSpaceMgrReady(self.spaceNo, self)
        self.addTimerCB(1, 'summonRandomBoss', (), gametimer.TIMER_TAG_SUMMON_RANDOM_BOSS)

        self.pyAddTimer(1, 60, gametimer.STATISTIC_FIGHTING_COUNT)
        self.fightingPlayersCnt = 0

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.STATISTIC_FIGHTING_COUNT:
            self._statisticFightingCount()
        else:
            self._onTimerTrigger(tid, userArg)

    def initStaticSpace(self):
        super().initStaticSpace()

    def addEntity(self, entId, tags):
        entity = KBEngine.entities.get(entId, None)
        if entity and entity.IsMonster:
            eTags = CBD.datas.get(entity.creepbaseId, {}).get('tag', [])
            eTags = [] if not eTags else eTags
            for tag in eTags:
                if tag == gameconst.CREEP_TAG_WONDERLAND_FIXED_BOSS:
                    _msgId = utils.getTranslatedMsgId(WL_CD.datas['wonderLand_fixedBossAppear']['value'])
                    _args = [utils.getTranslatedArg(entity.name)]
                    self.syncPlayer(lambda playerEnt: playerEnt.showMsg(_msgId, _args))
                elif tag == gameconst.CREEP_TAG_WONDERLAND_SUMMON_BOSS:
                    _msgId = utils.getTranslatedMsgId(WL_CD.datas['wonderLand_summoningSuccess']['value'])
                    self.syncPlayer(lambda playerEnt: playerEnt.showMsg(_msgId, []))

        super(WonderLandSpaceMgr, self).addEntity(entId, tags)

    def removeEntById(self, entId):
        if entId == self.randomBossId:
            self.onRandomBossDie()

        super(WonderLandSpaceMgr, self).removeEntById(entId)

    def onPlayerRelogin(self, box, playerGbId):
        super().onPlayerRelogin(box, playerGbId)
        _bossList = list(self.collToBoss.values())
        box.client.onWonderLandBossInfo(_bossList)

    def onPlayerEnter(self, pid):
        super(WonderLandSpaceMgr, self).onPlayerEnter(pid)
        _ent = KBEngine.entities.get(pid)
        if not _ent:
            LOG_ERR("onPlayerEnter: _ent is None", pid)
            return

        _bossList = list(self.collToBoss.values())
        _ent.client.onWonderLandBossInfo(_bossList)

    def summonRandomBoss(self):
        LOG_INFO("summonRandomBoss")
        _dungeonNo = formula.fetchMapId(self.spaceNo)
        _dunData = utils.getDunStructModData(_dungeonNo)
        if not _dunData:
            LOG_ERR("summonRandomBoss: _dunData is None", self.spaceNo)
            return

        _initEntities = _dunData.get('InitEntities')
        if not _initEntities:
            LOG_ERR("summonRandomBoss: _initEntities is None", self.spaceNo)
            return

        _monsters = _initEntities.get('Monster')
        if not _monsters:
            LOG_ERR("summonRandomBoss: _monsters is None", self.spaceNo)
            return

        _bossList = []
        for _data in _monsters.values():
            if _data['CustomID'] != 'randomBoss':
                continue

            _bossList.append(_data)

        if not _bossList:
            LOG_ERR("summonRandomBoss: _bossList is None")
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
            'instanceId': _bossData['ID'],
        }

        _boss = KBEngine.createEntity('Monster', self.spaceID, _pos, _dir, _params)
        self.randomBossId = _boss.id
        self.randomBossGameEntityId = _bossData['ID']

        '''
        _msgId = utils.getTranslatedMsgId(WL_CD.datas['wonderLand_randomBossAppear']['value'])
        _args = [utils.getTranslatedArg(_boss.name)]
        self.syncPlayer(lambda playerEnt: playerEnt.showMsg(_msgId, _args))
        '''

    def onRandomBossDie(self):
        self.randomBossId = 0
        _gameEntityId = self.randomBossGameEntityId
        self.randomBossGameEntityId = 0

        _dungeonNo = formula.fetchMapId(self.spaceNo)
        _bossData = utils.getDunStructModData(_dungeonNo)
        _bossData = _bossData['InitEntities']['Monster'][str(_gameEntityId)]

        _delay = _bossData['Props']['RefreshTime']
        self.addTimerCB(_delay, 'summonRandomBoss', (), gametimer.TIMER_TAG_SUMMON_RANDOM_BOSS)

    def _statisticFightingCount(self):
        now = utils.curTS()
        lastCnt = self.fightingPlayersCnt
        self.fightingPlayersCnt = 0
        dt = BDS.datas["Branch_activePlayer"]["value"] * 60
        for pid in self.players:
            ent = KBEngine.entities.get(pid)
            if not ent:
                continue
            #5分钟内有进入过战斗视为"活跃用户"
            if now - ent.lastFightTime < dt:
                self.fightingPlayersCnt += 1

        if lastCnt != self.fightingPlayersCnt:
            gameengine.getWonderLandStubBySpaceNo(self.spaceNo).onFightingPlayersCntSync(self.spaceNo, self.fightingPlayersCnt)
