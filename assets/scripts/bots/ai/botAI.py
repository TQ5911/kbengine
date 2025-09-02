# -*- encoding:utf-8 -*-
import KBEngine
from KBEDebug import *

from ai import botBtMeta
import ai.py_trees as py_trees
import gameconst
import sMath
import Math
import global_data as GD
import random

class botAI(object):
    def __init__(self):
        self.treeDic = {}
        self._stopCount = 0
        self._lastPatrolPos = self.position
        #self.bt_tree = self.buildBtTree()

    def buildBtTree(self):
        Root =  py_trees.composites.Parallel(name = 'Root')

        Attack =  botBtMeta.Attack('Attack', aiController=self, args=())
        Attack.addCondition(botBtMeta.ShouldAttack('ShouldAttack', aiController=self, args=()))
        Root.add_child(Attack)

        StopPatrol = botBtMeta.StopPatrol('StopPatrol', aiController=self, args=())
        StopPatrol.addCondition(botBtMeta.ShouldStopPatrol('ShouldStopPatrol', aiController=self, args=()))
        Root.add_child(StopPatrol)

        Patrol =  botBtMeta.Patrol('Patrol', aiController=self, args=())
        Patrol.addCondition(botBtMeta.ShouldPatrol('ShouldPatrol', aiController=self, args=()))
        Root.add_child(Patrol)

        return Root

    # -------------------
    # PyTree use

    def createTreeDic(self, tree):
        if tree.id not in self.treeDic:
            self.treeDic[tree.id] = {
                'currentIndex': -1,
                'executeCount': 0,
                'status': py_trees.Status.FAILURE
            }
        for c in tree.children:
            if c.id not in self.treeDic:
                self.treeDic[c.id] = {
                    'currentIndex': -1,
                    'executeCount': 0,
                    'status': py_trees.Status.FAILURE
                }
                self.createTreeDic(c)

    def getCurrentIndex(self, id):
        if id not in self.treeDic:
            return -1
        dic = self.treeDic.get(id)
        return dic['currentIndex']

    def setCurrentIndex(self, id, currentIndex):
        if id not in self.treeDic:
            print('setCurrentIndex error', id)
            return
        dic = self.treeDic.get(id)
        dic['currentIndex'] = currentIndex

    def getStatus(self, id):
        if id not in self.treeDic:
            return -1
        dic = self.treeDic.get(id)
        return dic['status']

    def setStatus(self, id, status):
        if id not in self.treeDic:
            print('setStatus error', id)
            return
        dic = self.treeDic.get(id)
        dic['status'] = status

    def addExecuteCount(self, id, addNum=1):
        if id not in self.treeDic:
            ERROR_MSG('addExecuteCount error', id)
            return
        dic = self.treeDic.get(id)
        dic['executeCount'] += 1

    def getExecuteCount(self, id):
        if id not in self.treeDic:
            return -1
        dic = self.treeDic.get(id)
        return dic['executeCount']

    # -------------------

    def botHasState(self, stat):
        return self.state & (1 << stat) == (1 << stat)

    def moveToNextPos(self):
        if self.dstPos is not None and sMath.distance2D(self.dstPos, self.dstPos) > 30:
            pass
        else:
            self.updateNextPos()

        self.dstPos = Math.Vector3(self.dstPos)
        self.dstPos.y = self.position.y
        self.cell.botMoveTo(self.dstPos)
        print('mmmmmmmmmmm moveToNextPos, dst pos:', self.dstPos)
        #self.moveToPoint( self.dstPosList[self.dstPosIdx], self.speed/3, 0.0, 0, True, True )

    def updateNextPos(self):
        # dstPos = self._getRandomPatrolPos(1.5)
        dstPos = self._getRandomMonsterKillPos() or self._getRandomPatrolPos()
        rand_x = random.uniform(-10, 10)
        rand_z = random.uniform(-10, 10)
        dstPos.x = dstPos.x + rand_x
        dstPos.z = dstPos.z + rand_z
        self.dstPos = Math.Vector3(dstPos)

    def shouldPatrol(self):
        entities = self.getEnemyNearBy()
        ret = False
        reason = 'unknown'
        if self.isDead():
            ret = False
            reason = 'dead'
        elif self.botHasState(gameconst.State.Idle) and 0 == len(entities):
            ret = True
            reason = 'OK'
        elif self.botHasState(gameconst.State.Moving):
            ret = False
            reason = 'moving'
        print('in shouldPatrol:', ret, reason, self.position)
        return ret

    def patrol(self):
        print('in patrol')
        if self.botHasState(gameconst.State.Idle):
            self._stopCount = 0
            self._lastPatrolPos = self.position
            self.startPatrol()
            return py_trees.Status.RUNNING

        if ((self.dstPos is not None and sMath.distance2D(self.position, self.dstPos) < 1)
                or sMath.distance2D(self.position, self._lastPatrolPos) < 1):
            print('     in patrol,  arrived dst')
            return py_trees.Status.SUCCESS

        self._lastPatrolPos = self.position

        if self.botHasState(gameconst.State.Moving):
            print('     in patrol,  Running')
            return py_trees.Status.RUNNING
        else:
            print('     in patrol,  Failed')
            return py_trees.Status.FAILURE

    def startPatrol(self):
        print('in startPatrol')
        self.moveToNextPos()

    def shouldStopPatrol(self):
        ret = False
        reason = 'unknown'
        if self.botHasState(gameconst.State.Idle):
            ret = False
            reason = 'idle'
        elif self.dstPos is not None and sMath.distance2D(self.position, self.dstPos) < 1:
            ret = True
            reason = 'OK'
        elif sMath.distance2D(self.position, self._lastPatrolPos) < 0.01:
            self._stopCount += 1
            if self._stopCount > 2:
                ret = True
                self._stopCount = 0
            else:
                ret = False
            reason = 'not move'
        else:
            entities = self.getEnemyNearBy()
            if len(entities) > 0:
                ret = True
                reason = 'enemy come'
        print('in shouldStopPatrol, ret:', ret, reason)
        return ret

    def stopPatrol(self):
        print('in stopPatrol')
        if self.botHasState(gameconst.State.Idle):
            return py_trees.Status.SUCCESS
        else:
            self.cell.botStopMove()
            return py_trees.Status.RUNNING

    def isDead(self):
        return False

    def relive(self):
        print('in relive')
        if self.isDead():
            self.cell.relive(1)
            return py_trees.Status.RUNNING
        else:
            return py_trees.Status.SUCCESS

    def shouldAttack(self):
        ret = False
        reason = 'default'
        entities = self.getEnemyNearBy()
        if len(entities) > 0:
            ret = True
            reason = 'enemy in range'
        print('in shouldAttack:', ret, reason)
        return ret

    def attack(self):
        entities = self.getEnemyNearBy()
        print('in attack, entities:', len(entities))
        if len(entities) > 0:
            print('  ATTACK')
            mids = list(entities.keys())
            targetId = random.choice(mids)
            targetPos = entities[targetId]
            self.useSkill(targetId, targetPos)
            return py_trees.Status.RUNNING
        else:
            print('  NO TARGET')
            return py_trees.Status.SUCCESS

    def hasMonstersNearby(self):
        nearby = self.getMonstersNearBy()
        return len(nearby) > 0

    def getEnemyNearBy(self, nearBy=20):
        enemy = {}
        nearbyMonsters = self.getMonstersNearBy(nearBy)
        nearbyForce = self.getAvatarForceNearBy(nearBy)
        for key in nearbyMonsters.keys():
            enemy[key] = nearbyMonsters[key]
        for key in nearbyForce.keys():
            enemy[key] = nearbyForce[key]
        return enemy

    def getMonstersNearBy(self, nearBy=10):
        nearby = {}
        if random.randint(0, 100) > 20:
            return nearby
        monsters = GD.monsters_map.get(self.clientapp.id, {})
        role_pos = self.position
        for mid, pos in monsters.items():
            dis = sMath.distance2D(role_pos, pos)
            if self.id == mid:
                continue
            if dis > nearBy:
                continue
            else:
                nearby[mid] = pos
        return nearby

    def getAvatarForceNearBy(self, nearBy=10):
        nearby = {}
        if random.randint(0, 100) > 10:
            return nearby
        role_pos = self.position
        for e in self.clientapp.entities.values():
            if self.force == e.force:
                continue
            if self.id == e.id:
                continue
            dis = sMath.distance2D(role_pos, e.position)
            if dis > nearBy:
                continue
            else:
                nearby[e.id] = e.position
        return nearby


    def _getRandomMonsterKillPos(self, nearBy=300):
        dic = self.getEnemyNearBy(nearBy)
        pos = list(dic.values())
        return random.choice(pos) if pos else None

    def botUpdate(self):
        if self.shouldAttack():
            entities = self.getEnemyNearBy()
            print('in attack, entities:', len(entities))
            if len(entities) > 0:
                mids = list(entities.keys())
                targetId = random.choice(mids)
                targetPos = entities[targetId]
                self.useSkill(targetId, targetPos)
        elif self.shouldPatrol():
            self.moveToNextPos()
        elif self.shouldStopPatrol():
            self.cell.botStopMove()



