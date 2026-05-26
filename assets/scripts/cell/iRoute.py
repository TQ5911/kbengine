# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import random

import gametimer
import gamemove
import path_path
import sMath
import utils
import gameconst
import gamedecorator
import conflict_conflict_def as C_C_DD

class IRoute(object):

    @property
    def escortSpeedOverwriteData(self):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.escortSpeedOverwriteData):
            self.setTempMiscProp(gameconst.EntityPropsEnum.escortSpeedOverwriteData, {})
        return self.getTempMiscProp(gameconst.EntityPropsEnum.escortSpeedOverwriteData)

    @escortSpeedOverwriteData.setter
    def escortSpeedOverwriteData(self, newVal):
        self.setTempMiscProp(gameconst.EntityPropsEnum.escortSpeedOverwriteData, newVal)

    @property
    def IsHuacheNpc(self):
        return False
        # return self.IsNpc and self.IsCombatUnit and self.CNpcType == gameconst.CNpcType.huache

    @gamedecorator.limitcall(0.5)
    def setRoute(self, pathId, routeByAI=False, escortDistance=0, escortLeaveDistance=0, speedOverwrite: dict=None):
        LOG_DBG('setRoute', pathId, routeByAI, speedOverwrite)
        speedOverwrite = speedOverwrite if speedOverwrite is not None else {}
        if pathId not in path_path.datas:
            LOG_INFO('setRoute: invalid pathId {}'.format(pathId))
            return False

        if len(path_path.datas[pathId]['pointList']) < 2:
            LOG_INFO('setRoute: invalid pointList {}'.format(path_path.datas[pathId]['pointList']))
            return False

        self.cancelRouting()

        self.pathId = pathId

        self.escortDistance = escortDistance
        self.escortLeaveDistance = escortLeaveDistance if escortLeaveDistance > 0 else self.escortDistance
        if escortDistance > 0:
            self.escortTrapId = self.addProximity(self.escortDistance, 0.0, gameconst.ESCORT_ROUTE_TRAP)

        escortSpeedOverwriteData = self.escortSpeedOverwriteData
        escortSpeedOverwriteData.clear()
        if "baseSpeed" in speedOverwrite:
            escortSpeedOverwriteData['baseSpeed'] = self.baseSpeed
            self.setProp('baseSpeed', speedOverwrite['baseSpeed'], src=gameconst.SourceType.SrcTpEscort)
        if "adjSpeed" in speedOverwrite:
            escortSpeedOverwriteData['adjSpeed'] = self.adjSpeed
            self.setProp('adjSpeed', speedOverwrite['adjSpeed'], src=gameconst.SourceType.SrcTpEscort)
        if "moveAni" in speedOverwrite:
            escortSpeedOverwriteData['moveAni'] = self.moveAni
            self.moveAni = speedOverwrite["moveAni"]

        if routeByAI:
            self.routeState = gameconst.RouteState.ROUTE_STATE_WAIT
            return True
        else:
            #选择最近路点
            self.refreshPointIndex(False)
            return self.startRouting()

    def onPlayerEnterEscortTrap(self, entity, rangeXZ, rangeY, controllerId):
        if not (entity and entity.IsAvatar):
            return
        if self.routeState == gameconst.RouteState.ROUTE_STATE_SUSPEND \
                and self.routeSuspendReason == gameconst.RouteSuspendReason.ESCORT_NO_PLAYER_IN_DISTANCE:
            self.continueRouting()

    def cancelRouting(self):
        LOG_DBG('cancelRouting')
        if self.routeState == gameconst.RouteState.ROUTE_STATE_MOVING:
            self.cancelController('Movement')
            self.removeState(gameconst.StateEnum.Moving)

        self.routeState = gameconst.RouteState.ROUTE_STATE_IDLE
        self.routeSuspendReason = gameconst.RouteSuspendReason.UNKNOWN
        self._resetRoute()

    def _resetRoute(self):
        self.pathId = 0
        self.pointIndex = 0
        self.routeForward = True
        self.escortDistance = 0
        self.escortLeaveDistance = 0
        if self.escortTrapId:
            self.cancelController(self.escortTrapId)
        self.escortTrapId = 0
        escortSpeedOverwriteData = self.escortSpeedOverwriteData
        if "baseSpeed" in escortSpeedOverwriteData:
            self.setProp('baseSpeed', escortSpeedOverwriteData['baseSpeed'], src=gameconst.SourceType.SrcTpEscort)
        if "adjSpeed" in escortSpeedOverwriteData:
            self.setProp('adjSpeed', escortSpeedOverwriteData['adjSpeed'], src=gameconst.SourceType.SrcTpEscort)
        if "moveAni" in escortSpeedOverwriteData:
            self.moveAni = escortSpeedOverwriteData["moveAni"]
        escortSpeedOverwriteData.clear()

    def interruptRouting(self, reason=gameconst.RouteSuspendReason.NORMAL):
        if self.routeState != gameconst.RouteState.ROUTE_STATE_MOVING:
            return

        self.cancelController('Movement')
        self.removeState(gameconst.StateEnum.Moving)
        self.routeState = gameconst.RouteState.ROUTE_STATE_SUSPEND
        self.routeSuspendReason = reason
        if reason == gameconst.RouteSuspendReason.ESCORT_NO_PLAYER_IN_DISTANCE:
            entityGID = utils.parseGidFromGameEntityId(self.gameEntityId)
            self.flowCtrlEntityRoutingMissingEscort(entityGID, self.pathId)

    def continueRouting(self):
        if self.routeState != gameconst.RouteState.ROUTE_STATE_SUSPEND:
            return False

        return self.startRouting()

    def onRouteFinished(self):
        LOG_DBG("onRouteFinished::")
        entityGID = utils.parseGidFromGameEntityId(self.gameEntityId)
        self.flowCtrlEntityRouteFinished(entityGID, self.pathId)

        if self.IsHuacheNpc:
            self.onPathOver()

    def getLuckMonsterNextPointIndex(self):
        last_pointIndex = getattr(self, 'last_pointIndex', None)
        weight = path_path.datas[self.pathId]['branchWeight'][self.pointIndex]
        keys = []
        values = []
        for k, v in weight.items():
            if k == last_pointIndex:
                continue
            keys.append(k)
            values.append(v)
        next_pointIndex = random.choices(keys, values)[0] if keys else last_pointIndex
        return next_pointIndex

    def startRouting(self):
        if not self.pathId or self.pointIndex >= len(path_path.datas[self.pathId]['pointList']):
            return False

        if not self.checkConflictState(C_C_DD.datas.move):
            return False

        if sMath.distance2D(self.position, self.nextPoint()) >= 0.1:
            onNode = False
        else:
            onNode = True
            if path_path.datas[self.pathId]['type'] == 4:
                next_pointIndex = self.getLuckMonsterNextPointIndex()
                self.last_pointIndex = self.pointIndex
                self.pointIndex = next_pointIndex
            else:
                if self.pointIndex >= len(path_path.datas[self.pathId]['pointList']) - 1:
                    LOG_INFO('startRouting: already in end point')
                    self.routeState = gameconst.RouteState.ROUTE_STATE_COMPLETE
                    self.onRouteFinished()
                    self._resetRoute()
                    return True
                self.pointIndex += 1

        self.routeState = gameconst.RouteState.ROUTE_STATE_MOVING
        self.moveToRouteNode(onNode, self.nextPoint(), 0)
        return True

    # def _getNearestRouteNode(self):
    #     minDis = sys.maxsize
    #     nearest = 0
    #     for index, point in enumerate(path_path.datas[self.pathId]['pointList']):
    #         distance = sMath.distance2D(self.position, point)
    #         if distance < minDis:
    #             nearest = index
    #             minDis = distance
    #
    #     return nearest

    def nextPoint(self):
        posInfo = path_path.datas[self.pathId]['pointList'][self.pointIndex]
        return (posInfo[0], posInfo[1], posInfo[2])

    def moveToRouteNode(self, onNode, dstPos, failCnt, faceMovement = True):
        # LOG_DBG('moveToRouteNode', onNode, dstPos, failCnt, faceMovement)
        if self.routeState != gameconst.RouteState.ROUTE_STATE_MOVING:
            return
        if onNode:
            moveController = self.moveToPoint(dstPos, self.speed, 0, gamemove.ROUTE_NODE_MOVE, faceMovement, 1)
            if self.IsHuacheNpc:
                self.movePlayerToNextPoint()
        else:
            moveController = self.scriptNavigate(dstPos, self.speed, faceMovement=faceMovement, userData=gamemove.ROUTE_NODE_MOVE)

        if moveController:
            if not self.hasState(gameconst.StateEnum.Moving):
                self.setState(gameconst.StateEnum.Moving)

        else:
            LOG_WARN('moveToRouteNode: move failed, failCnt:', failCnt)
            # if self.IsAvatar:
            #     self.controlledBy = self.base
            if failCnt < 10:
                self.addTimerCB((failCnt+1)*random.random(), 'moveToRouteNode', (onNode, dstPos, failCnt+1,
                                                                                faceMovement), gametimer.TIMER_TAG_MOVE_TO_ROUTE_NODE)
            else:
                self.cancelRouting()

    def luckMonsterPatrol(self, success=True):
        pointInfo = path_path.datas[self.pathId]['pointList'][self.pointIndex]
        self.nextRouteTime = utils.curTS() + round(random.uniform(pointInfo[4], pointInfo[5]), 2)
        self.interruptRouting()

    def moveToRouteNodeCB(self, isSucceed):
        # LOG_DBG('moveToRouteNodeCB', isSucceed, self.position, self.state)
        moveOver = self._moveToRouteNodeCB(isSucceed)
        if moveOver:
            self.removeState(gameconst.StateEnum.Moving)
            return

        if self.checkConflictState(C_C_DD.datas.move):
            if path_path.datas[self.pathId]['type'] == 4:
                self.luckMonsterPatrol()
            else:
                self.moveToRouteNode(True, self.nextPoint(), 0)

        else:
            LOG_WARN('moveToRouteNodeCB: conflict state, interrupt routing')
            self.interruptRouting()

    def _moveToRouteNodeCB(self, isSucceed):
        if self.routeState != gameconst.RouteState.ROUTE_STATE_MOVING:
            return True

        if not isSucceed:
            for i in range(2, 10, 2):
                posList = self.getRandomPoints(self.nextPoint(), i, 1, 0)
                if posList:
                    LOG_INFO('moveToRouteNodeCB: choice accessible point', i, posList[0])
                    self.addTimerCB(random.random(), 'moveToRouteNode', (False, posList[0], 0, False), gametimer.TIMER_TAG_MOVE_TO_ROUTE_NODE)
                    break
                # FIXME()(ROUTE): 这里似乎想延时防止调用速度过快，需要看看，先删掉，sleep太危险了
                # time.sleep(1)
            else:
                LOG_WARN('moveToRouteNodeCB: [%s] -> [%s] failed' % self.position, self.nextPoint())
                self.routeState = gameconst.RouteState.ROUTE_STATE_IDLE
                self._resetRoute()
            return True

        pathType = path_path.datas[self.pathId]['type']
        tail = len(path_path.datas[self.pathId]['pointList']) - 1
        if pathType == 1:
            self.pointIndex += 1
            if self.pointIndex > tail:
                self.routeState = gameconst.RouteState.ROUTE_STATE_COMPLETE
                self.onRouteFinished()
                self._resetRoute()
                return True

        elif pathType == 2:
            nextPointIndex = self.pointIndex+1 if self.routeForward else self.pointIndex-1
            if nextPointIndex < 0:
                self.routeForward = True
                self.pointIndex = 1
            elif nextPointIndex > tail:
                self.routeForward = False
                self.pointIndex = tail - 1
            else:
                self.pointIndex = nextPointIndex

        elif pathType == 3:
            self.pointIndex += 1
            if self.pointIndex > tail:
                self.pointIndex = 0

        if self.escortLeaveDistance > 0:
            for _ in self.entitiesInRange(self.escortLeaveDistance, 'Avatar'):
                break
            else:
                self.interruptRouting(reason=gameconst.RouteSuspendReason.ESCORT_NO_PLAYER_IN_DISTANCE)

        return False

    def refreshPointIndex(self,needcheck=True):
        #跟新目的地为 路径中最近的点 不改变方向
        if self.routeState != gameconst.RouteState.ROUTE_STATE_SUSPEND and needcheck:
             return True
        mindis = 2 ** 32 -1
        i = 0
        for pointList in path_path.datas[self.pathId]['pointList']:
            tmpdis = sMath.distance2D(self.position, (pointList[0], pointList[1], pointList[2]))
            if tmpdis < mindis:
                mindis = tmpdis
                self.pointIndex = i
            i += 1
