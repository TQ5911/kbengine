# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import random

import gametimer
import gamemove
import path_path as P_PD
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

    @gamedecorator.limitcall(0.5)
    def setRoute(self, pathId, routeByAI=False, escortDistance=0, escortLeaveDis=0, speedOverwrite: dict=None):
        LOG_DBG('setRoute', pathId, routeByAI, speedOverwrite)
        speedOverwrite = speedOverwrite if speedOverwrite is not None else {}
        if pathId not in P_PD.datas:
            LOG_INFO('setRoute: invalid pathId {}'.format(pathId))
            return False

        if len(P_PD.datas[pathId]['pointList']) < 2:
            LOG_INFO('setRoute: invalid pointList {}'.format(P_PD.datas[pathId]['pointList']))
            return False

        self.cancelRouting()

        self.pathId = pathId

        self.escortDistance = escortDistance
        self.escortLeaveDis = escortLeaveDis if escortLeaveDis > 0 else self.escortDistance
        if escortDistance > 0:
            self.escortTrapId = self.addProximity(self.escortDistance, 0.0, gameconst.ESCORT_ROUTE_TRAP)

        _escortSpeedOverwriteData = self.escortSpeedOverwriteData
        _escortSpeedOverwriteData.clear()
        if "baseSpeed" in speedOverwrite:
            _escortSpeedOverwriteData['baseSpeed'] = self.baseSpeed
            self.setProp('baseSpeed', speedOverwrite['baseSpeed'], src=gameconst.SourceType.SrcTpEscort)
        if "adjSpeed" in speedOverwrite:
            _escortSpeedOverwriteData['adjSpeed'] = self.adjSpeed
            self.setProp('adjSpeed', speedOverwrite['adjSpeed'], src=gameconst.SourceType.SrcTpEscort)
        if "moveAni" in speedOverwrite:
            _escortSpeedOverwriteData['moveAni'] = self.moveAni
            self.moveAni = speedOverwrite["moveAni"]

        if routeByAI:
            self.routeState = gameconst.RouteStateEnum.ROUTE_STATE_WAIT
            return True
        else:
            #选择最近路点
            self.refreshPointIndex(False)
            return self.startRouting()

    def onPlayerEnterEscortTrap(self, entity, rangeXZ, rangeY, _):
        if not (entity and entity.IsAvatar):
            return
        if self.routeState == gameconst.RouteStateEnum.ROUTE_STATE_SUSPEND \
                and self.routeSuspendReason == gameconst.RouteSuspendReason.ESCORT_NO_PLAYER_IN_DISTANCE:
            self.continueRouting()

    def cancelRouting(self):
        LOG_DBG('cancelRouting')
        if self.routeState == gameconst.RouteStateEnum.ROUTE_STATE_MOVING:
            self.cancelController('Movement')
            self.removeState(gameconst.StateEnum.Moving)

        self.routeState = gameconst.RouteStateEnum.ROUTE_STATE_IDLE
        self.routeSuspendReason = gameconst.RouteSuspendReason.UNKNOWN
        self._resetRoute()

    def _resetRoute(self):
        self.pointIndex = 0
        self.pathId = 0
        self.routeForward = True
        self.escortDistance = 0
        self.escortLeaveDis = 0
        if self.escortTrapId:
            self.cancelController(self.escortTrapId)
        self.escortTrapId = 0
        _escortSpeedOverwriteData = self.escortSpeedOverwriteData
        if "baseSpeed" in _escortSpeedOverwriteData:
            self.setProp('baseSpeed', _escortSpeedOverwriteData['baseSpeed'], src=gameconst.SourceType.SrcTpEscort)
        if "adjSpeed" in _escortSpeedOverwriteData:
            self.setProp('adjSpeed', _escortSpeedOverwriteData['adjSpeed'], src=gameconst.SourceType.SrcTpEscort)
        if "moveAni" in _escortSpeedOverwriteData:
            self.moveAni = _escortSpeedOverwriteData["moveAni"]
        _escortSpeedOverwriteData.clear()

    def interruptRouting(self, reason=gameconst.RouteSuspendReason.NORMAL):
        if self.routeState != gameconst.RouteStateEnum.ROUTE_STATE_MOVING:
            return

        self.cancelController('Movement')
        self.removeState(gameconst.StateEnum.Moving)
        self.routeState = gameconst.RouteStateEnum.ROUTE_STATE_SUSPEND
        self.routeSuspendReason = reason
        if reason == gameconst.RouteSuspendReason.ESCORT_NO_PLAYER_IN_DISTANCE:
            entityGID = utils.parseGidFromGameEntityId(self.gameEntityId)
            self.flowCtrlEntityRoutingMissingEscort(entityGID, self.pathId)

    def continueRouting(self):
        if self.routeState != gameconst.RouteStateEnum.ROUTE_STATE_SUSPEND:
            return False

        return self.startRouting()

    def onRouteFinished(self):
        LOG_DBG("onRouteFinished::")
        entityGID = utils.parseGidFromGameEntityId(self.gameEntityId)
        self.flowCtrlEntityRouteFinished(entityGID, self.pathId)

    def getLuckMonsterNextPointIndex(self):
        last_pointIndex = getattr(self, 'last_pointIndex', None)
        weight = P_PD.datas[self.pathId]['branchWeight'][self.pointIndex]
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
        if not self.pathId or self.pointIndex >= len(P_PD.datas[self.pathId]['pointList']):
            return False

        if not self.checkConflictState(C_C_DD.datas.move):
            return False

        if sMath.distance2D(self.position, self.nextPoint()) >= 0.1:
            _onNode = False
        else:
            _onNode = True
            if P_PD.datas[self.pathId]['type'] == 4:
                next_pointIndex = self.getLuckMonsterNextPointIndex()
                self.last_pointIndex = self.pointIndex
                self.pointIndex = next_pointIndex
            else:
                if self.pointIndex >= len(P_PD.datas[self.pathId]['pointList']) - 1:
                    LOG_INFO('startRouting: already in end point')
                    self.routeState = gameconst.RouteStateEnum.ROUTE_STATE_COMPLETE
                    self.onRouteFinished()
                    self._resetRoute()
                    return True
                self.pointIndex += 1

        self.routeState = gameconst.RouteStateEnum.ROUTE_STATE_MOVING
        self.moveToRouteNode(_onNode, self.nextPoint(), 0)
        return True

    def nextPoint(self):
        posInfo = P_PD.datas[self.pathId]['pointList'][self.pointIndex]
        return (posInfo[0], posInfo[1], posInfo[2])

    def moveToRouteNode(self, onNode, dstPos, failCount, faceMovement = True):
        if self.routeState != gameconst.RouteStateEnum.ROUTE_STATE_MOVING:
            return
        if onNode:
            _moveController = self.moveToPoint(dstPos, self.speed, 0, gamemove.ROUTE_NODE_MOVE, faceMovement, 1)
        else:
            _moveController = self.scriptNavigate(dstPos, self.speed, faceMovement=faceMovement, userData=gamemove.ROUTE_NODE_MOVE)

        if _moveController:
            if not self.hasState(gameconst.StateEnum.Moving):
                self.setState(gameconst.StateEnum.Moving)

        else:
            LOG_WARN('moveToRouteNode: move failed, failCount:', failCount)
            if failCount < 10:
                self.addTimerCB(
                    (failCount+1)*random.random(),
                    'moveToRouteNode',
                    (onNode, dstPos, failCount+1, faceMovement),
                    gametimer.TIMER_TAG_MOVE_TO_ROUTE_NODE)

            else:
                self.cancelRouting()

    def luckMonsterPatrol(self, success=True):
        pointInfo = P_PD.datas[self.pathId]['pointList'][self.pointIndex]
        self.nextRouteTime = utils.curTS() + round(random.uniform(pointInfo[4], pointInfo[5]), 2)
        self.interruptRouting()

    def moveToRouteNodeCB(self, isSucceed):
        # LOG_DBG('moveToRouteNodeCB', isSucceed, self.position, self.state)
        moveOver = self._moveToRouteNodeCB(isSucceed)
        if moveOver:
            self.removeState(gameconst.StateEnum.Moving)
            return

        if self.checkConflictState(C_C_DD.datas.move):
            if P_PD.datas[self.pathId]['type'] == 4:
                self.luckMonsterPatrol()
            else:
                self.moveToRouteNode(True, self.nextPoint(), 0)

        else:
            LOG_WARN('moveToRouteNodeCB: conflict state, interrupt routing')
            self.interruptRouting()

    def _moveToRouteNodeCB(self, isSucceed):
        if self.routeState != gameconst.RouteStateEnum.ROUTE_STATE_MOVING:
            return True

        if not isSucceed:
            for _i in range(2, 10, 2):
                posList = self.getRandomPoints(self.nextPoint(), _i, 1, 0)
                if posList:
                    LOG_INFO('moveToRouteNodeCB: choice accessible point', _i, posList[0])
                    self.addTimerCB(
                        random.random(), 
                        'moveToRouteNode', 
                        (False, posList[0], 0, False), 
                        gametimer.TIMER_TAG_MOVE_TO_ROUTE_NODE)
                    break
                # FIXME()(ROUTE): 这里似乎想延时防止调用速度过快，需要看看，先删掉，sleep太危险了
                # time.sleep(1)
            else:
                LOG_WARN('moveToRouteNodeCB: [%s] -> [%s] failed' % self.position, self.nextPoint())
                self.routeState = gameconst.RouteStateEnum.ROUTE_STATE_IDLE
                self._resetRoute()
            return True

        _pathType = P_PD.datas[self.pathId]['type']
        tail = len(P_PD.datas[self.pathId]['pointList']) - 1
        if _pathType == 1:
            self.pointIndex += 1
            if self.pointIndex > tail:
                self.routeState = gameconst.RouteStateEnum.ROUTE_STATE_COMPLETE
                self.onRouteFinished()
                self._resetRoute()
                return True

        elif _pathType == 2:
            _nextPointIndex = self.pointIndex+1 if self.routeForward else self.pointIndex-1
            if _nextPointIndex < 0:
                self.routeForward = True
                self.pointIndex = 1
            elif _nextPointIndex > tail:
                self.routeForward = False
                self.pointIndex = tail - 1
            else:
                self.pointIndex = _nextPointIndex

        elif _pathType == 3:
            self.pointIndex += 1
            if self.pointIndex > tail:
                self.pointIndex = 0

        if self.escortLeaveDis > 0:
            for _ in self.entitiesInRange(self.escortLeaveDis, 'Avatar'):
                break
            else:
                self.interruptRouting(reason=gameconst.RouteSuspendReason.ESCORT_NO_PLAYER_IN_DISTANCE)

        return False

    def refreshPointIndex(self,needcheck=True):
        #跟新目的地为 路径中最近的点 不改变方向
        if self.routeState != gameconst.RouteStateEnum.ROUTE_STATE_SUSPEND and needcheck:
             return True
        mindis = 2 ** 32 -1
        i = 0
        for pointList in P_PD.datas[self.pathId]['pointList']:
            tmpdis = sMath.distance2D(self.position, (pointList[0], pointList[1], pointList[2]))
            if tmpdis < mindis:
                mindis = tmpdis
                self.pointIndex = i
            i += 1
