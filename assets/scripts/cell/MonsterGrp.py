# coding: utf-8
import KBEngine
from KBEDebug import *

import gametimer
import gameconst
import formula
import utils

import iCell
import iTimer
import EventMgr
import iFubenSpace

import creep_group as CRG


class MonsterGrp(iCell.ICell, iTimer.ITimer, EventMgr.EventMgr, iFubenSpace.IFubenSpace):
    """ monster group manager

    properties:
        groupID: int
        monsterIds: list<int>

    """

    def __init__(self):
        iCell.ICell.__init__(self)
        LOG_INFO('create monster group: {}'.format(self.id))
        if not formula.inDungeonScene(self.spaceNo):
            self.initAllMonsters()

        if self.spaceMgr:
            self.spaceMgr.addEntity(
                self.id,
                ('mgid_{}'.format(self.groupId), self.__class__.__name__))

    def initAllMonsters(self):
        _mapId = formula.fetchMapId(self.spaceNo)
        _dunData = utils.getDunModuleData(_mapId)
        _iterGIDs = []
        for _gid in self.getMonsterGIDs():
            if str(_gid) not in _dunData:
                LOG_ERR('快联系策划把这个修改了,怪物组有个怪物没配置：', _gid, self.spaceNo)
                continue

            _monData = _dunData[str(_gid)]
            _refreshNum = int(_monData['Props']['RefreshNum'])
            for i in utils.genGameEntityId(_gid, _refreshNum):
                _iterGIDs.append(i)

        _entityProps = []
        utils.loadLineReadyEntities(self.spaceNo, _iterGIDs, _entityProps)
        for _, _, _className, _, _pos, _dir, _params, _ in _entityProps:
            _params['spaceMgrId'] = self.spaceMgrId
            _params['monsterGroupId'] = self.id
            KBEngine.createEntity(_className, self.spaceID, _pos, _dir, _params)

    def getMonsterGIDs(self):
        _mapId = formula.fetchMapId(self.spaceNo)
        _groupData = utils.getDunGroupModuleData(_mapId)
        return _groupData.get(str(self.groupId))

    def doEntityRefreshGrp(self, boxGroupId, gameEntityId):
        if KBEngine.isShuttingDown():
            return
        
        if boxGroupId > 0 and self.spaceMgr and self.spaceMgr.boxGroupHasUnlock(boxGroupId):
            self.spaceMgr.addBoxGroupMonster(boxGroupId, gameEntityId, self.id)
            return

        _entityProps = []
        utils.loadLineReadyEntities(self.spaceNo, [gameEntityId], _entityProps, True)
        for _, _, _className, _, _pos, _dir, _params, _ in _entityProps:
            _params['spaceMgrId'] = self.spaceMgrId
            _params['monsterGroupId'] = self.id
            KBEngine.createEntity(_className, self.spaceID, _pos, _dir, _params)

    def canBeDestroy(self):
        if self.hasMonsterNeedRefresh:
            return False

        if self.monsters:
            return False

        return True

    def isAllMonstersDead(self):
        monsters = self.monsters

        if not monsters:
            return True

        for mid, m in monsters:
            if not m.isDie():
                return False

        return True

    @property
    def monsters(self):
        """:return all live monsters entities list"""
        results = []
        for mid in self.monsterIDs:
            monster = KBEngine.entities.get(mid)

            if monster and not monster.isDestroyed:
                results.append((mid, monster))

        return results

    def sync(self, monsterId, syncFuncName, args=None, kwargs=None):
        """Sync data from single monster to others

        MG.sync(monsterID_1, 'xxx') --> monster2.xxx, monster3.xxx

        :param monsterId: synced monster id
        :param syncFuncName: callback function name in other monster
        :param args: callback args
        :param kwargs: callback kwargs
        :return: results dict with {monsterId, cbResult, ...}
        """
        results = {}

        if args is None:
            args = []

        if kwargs is None:
            kwargs = {}

        for mid, m in self.monsters:
            if mid == monsterId:
                continue

            results[mid] = getattr(m, syncFuncName)(*args, **kwargs)

        return results

    def removeId(self, monsterId):
        try:
            self.monsterIDs.remove(monsterId)
        except ValueError:
            return

    def addId(self, monsterId):
        self.monsterIDs.append(monsterId)

    def onDestroy(self):
        """
        KBEngine method.
        entity销毁
        """
        LOG_DBG("monsterGrp::onDestroy: %i." % self.id)

        self._clearMonsters()

    def _clearMonsters(self):
        LOG_DBG('Reset monsters monsterGroupId.')
        for _, monster in self.monsters:
            if monster.monsterGroupId == self.id:
                monster.monsterGroupId = 0

    def onTimer(self, tid, userData):
        self._onTimerTrigger(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)

