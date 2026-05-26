# -*- encoding:utf-8 -*-
import KBEngine
from KBEDebug import *

from ai import botBtMeta
import ai.py_trees as py_trees
import gameconst
import Math
import sMath
import global_data as GD
import random


class BotAI(object):
    def __init__(self):
        self.treeDict = {}
        self._stopCnt = 0
        self._lastPatrolPos = self.position

    def buildBtTree(self):
        Root =  py_trees.composites.Parallel(name = 'Root')

        _attack =  botBtMeta.Attack('Attack', aiController=self, args=())
        _attack.addCondition(botBtMeta.ShouldAttack('ShouldAttack', aiController=self, args=()))
        Root.add_child(_attack)

        _stopPatrol = botBtMeta.StopPatrol('StopPatrol', aiController=self, args=())
        _stopPatrol.addCondition(botBtMeta.ShouldStopPatrol('ShouldStopPatrol', aiController=self, args=()))
        Root.add_child(_stopPatrol)

        _patrol =  botBtMeta.Patrol('Patrol', aiController=self, args=())
        _patrol.addCondition(botBtMeta.ShouldPatrol('ShouldPatrol', aiController=self, args=()))
        Root.add_child(_patrol)

        return Root

    # -------------------
    # PyTree use

    def createTreeDic(self, tree):
        if tree.id not in self.treeDict:
            self.treeDict[tree.id] = {
                'currentIndex': -1,
                'executeCount': 0,
                'status': py_trees.Status.FAILURE
            }
        for _c in tree.children:
            if _c.id not in self.treeDict:
                self.treeDict[_c.id] = {
                    'currentIndex': -1,
                    'executeCount': 0,
                    'status': py_trees.Status.FAILURE
                }
                self.createTreeDic(_c)

    def getCurrentIndex(self, id):
        if id not in self.treeDict:
            return -1
        _dic = self.treeDict.get(id)
        return _dic['currentIndex']

    def setCurrentIndex(self, id, currentIndex):
        if id not in self.treeDict:
            DEBUG_MSG('setCurrentIndex error', id)
            return
        dic = self.treeDict.get(id)
        dic['currentIndex'] = currentIndex

    def getStatus(self, id):
        if id not in self.treeDict:
            return -1
        dic = self.treeDict.get(id)
        return dic['status']

    def setStatus(self, id, status):
        if id not in self.treeDict:
            DEBUG_MSG('setStatus error', id)
            return
        dic = self.treeDict.get(id)
        dic['status'] = status

    def addExecuteCount(self, id, addNum=1):
        if id not in self.treeDict:
            ERROR_MSG('addExecuteCount error', id)
            return
        dic = self.treeDict.get(id)
        dic['executeCount'] += 1

    def getExecuteCount(self, id):
        if id not in self.treeDict:
            return -1
        _dic = self.treeDict.get(id)
        return _dic['executeCount']

    def hasBotState(self, stat):
        return self.state & (1 << stat) == (1 << stat)

    def _moveToNextPos(self):
        if not (self.dstPos is not None and sMath.distance2D(self.dstPos, self.dstPos) > 30):
            self.updateNextPos()

        _vecPos = Math.Vector3(self.dstPos)
        _vecPos.y = self.position.y
        self.dstPos = _vecPos
        self.cell.botMoveTo(self.dstPos)
        DEBUG_MSG('mmmmmmmmmmm _moveToNextPos, dst pos:', self.dstPos)

    def updateNextPos(self):
        _dstPos = self._getRandomMonsterKillPos() or self._getRandomPatrolPos()
        rand_x = random.uniform(-10, 10)
        rand_z = random.uniform(-10, 10)
        _dstPos.x = _dstPos.x + rand_x
        _dstPos.z = _dstPos.z + rand_z
        self.dstPos = Math.Vector3(_dstPos)

    def shouldPatrol(self):
        _entities = self.getEnemyNearBy()
        _ret = False
        _reason = 'unknown'
        if self.isDead():
            _ret = False
            _reason = 'dead'
        elif self.hasBotState(gameconst.StateEnum.Idle) and 0 == len(_entities):
            _ret = True
            _reason = 'OK'
        elif self.hasBotState(gameconst.StateEnum.Moving):
            _ret = False
            _reason = 'moving'
        DEBUG_MSG('in shouldPatrol:', _ret, _reason, self.position)
        return _ret

    def patrol(self):
        DEBUG_MSG('in patrol')
        if self.hasBotState(gameconst.StateEnum.Idle):
            self._stopCnt = 0
            self._lastPatrolPos = self.position
            self._startPatrol()
            return py_trees.Status.RUNNING

        if ((self.dstPos is not None and sMath.distance2D(self.dstPos, self.position) < 1)
                or sMath.distance2D(self.position, self._lastPatrolPos) < 1):
            DEBUG_MSG('     in patrol,  arrived dst')
            return py_trees.Status.SUCCESS

        self._lastPatrolPos = self.position

        if self.hasBotState(gameconst.StateEnum.Moving):
            DEBUG_MSG('     in patrol,  Running')
            return py_trees.Status.RUNNING
        else:
            DEBUG_MSG('     in patrol,  Failed')
            return py_trees.Status.FAILURE

    def _startPatrol(self):
        DEBUG_MSG('in _startPatrol')
        self._moveToNextPos()

    def shouldStopPatrol(self):
        _ret = False
        _reason = 'unknown'
        if self.hasBotState(gameconst.StateEnum.Idle):
            _ret = False
            _reason = 'idle'
        elif self.dstPos is not None and sMath.distance2D(self.position, self.dstPos) < 1:
            _ret = True
            _reason = 'OK'
        elif sMath.distance2D(self.position, self._lastPatrolPos) < 0.01:
            self._stopCnt += 1
            if self._stopCnt > 2:
                _ret = True
                self._stopCnt = 0
            else:
                _ret = False
            _reason = 'not move'
        else:
            _entities = self.getEnemyNearBy()
            if len(_entities) > 0:
                _ret = True
                _reason = 'enemy come'
        DEBUG_MSG('in shouldStopPatrol, _ret:', _ret, _reason)
        return _ret

    def isDead(self):
        return False

    def stopPatrol(self):
        DEBUG_MSG('in stopPatrol')
        if self.hasBotState(gameconst.StateEnum.Idle):
            return py_trees.Status.SUCCESS
        else:
            self.cell.botStopMove()
            return py_trees.Status.RUNNING

    def relive(self):
        DEBUG_MSG('in relive')
        if self.isDead():
            pass
            self.cell.relive(1)
            return py_trees.Status.RUNNING
        else:
            return py_trees.Status.SUCCESS

    def shouldBotAttack(self):
        _ret = False
        _reason = 'default'
        _entities = self.getEnemyNearBy()
        if len(_entities) > 0:
            _ret = True
            _reason = 'enemy in range'
        DEBUG_MSG('in shouldBotAttack:', _ret, _reason)
        return _ret

    def attack(self):
        _entities = self.getEnemyNearBy()
        DEBUG_MSG('in attack, _entities:', len(_entities))
        if len(_entities) > 0:
            DEBUG_MSG('  ATTACK')
            mids = list(_entities.keys())
            targetId = random.choice(mids)
            targetPos = _entities[targetId]
            self.useSkill(targetId, targetPos)
            return py_trees.Status.RUNNING
        else:
            DEBUG_MSG('  NO TARGET')
            return py_trees.Status.SUCCESS

    def hasMonstersNearby(self):
        _nearby = self.getMonstersNearBy()
        return len(_nearby) > 0

    def getEnemyNearBy(self, nearBy=20):
        _enemy = {}
        _nearbyMonsters = self.getMonstersNearBy(nearBy)
        _nearbyForce = self.getAvatarForceNearBy(nearBy)
        for key in _nearbyMonsters.keys():
            _enemy[key] = _nearbyMonsters[key]
        for key in _nearbyForce.keys():
            _enemy[key] = _nearbyForce[key]
        return _enemy

    def getMonstersNearBy(self, nearBy=10):
        _nearby = {}
        if random.randint(0, 100) > 20:
            return _nearby
        _monsters = GD.monsters_map.get(self.clientapp.id, {})
        _role_pos = self.position
        for mid, pos in _monsters.items():
            dis = sMath.distance2D(_role_pos, pos)
            if self.id == mid:
                continue
            if dis > _nearBy:
                continue
            else:
                _nearby[mid] = pos
        return _nearby

    def getAvatarForceNearBy(self, nearBy=10):
        _nearby = {}
        if random.randint(0, 100) > 10:
            return _nearby
        _role_pos = self.position
        for _e in self.clientapp.entities.values():
            if self.force == _e.force:
                continue
            if self.id == _e.id:
                continue
            dis = sMath.distance2D(_role_pos, _e.position)
            if dis > _nearBy:
                continue
            else:
                _nearby[_e.id] = _e.position
        return _nearby


    def _getRandomMonsterKillPos(self, nearBy=300):
        _dic = self.getEnemyNearBy(nearBy)
        _pos = list(_dic.values())
        return random.choice(_pos) if _pos else None

    def botUpdate(self):
        DEBUG_MSG("botUpdate")
        if not isinstance(self, BotAI):
            return
        if self.shouldBotAttack():
            _entities = self.getEnemyNearBy()
            DEBUG_MSG('in attack, _entities:', len(_entities))
            if len(_entities) > 0:
                mids = list(_entities.keys())
                targetId = random.choice(mids)
                targetPos = _entities[targetId]
                self.useSkill(targetId, targetPos)
        elif self.shouldPatrol():
            self._moveToNextPos()
        elif self.shouldStopPatrol():
            self.cell.botStopMove()



