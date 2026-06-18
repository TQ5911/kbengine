# coding: utf-8

import KBEngine
from KBEDebug import *

import math
import random

import Math
import gameconfig
import gameconst
import gametimer
import LogTrackingMgr

import const_const as CONST
import jumpData_set as JDS
import conflict_status_def as CCDD

class ISpeedCheck(object):
    def __init__(self):
        LOG_DBG("ISpeedCheck::__init__")

    def resetOverSpeedCheckTimer(self, lastSpeed = 0, isInit = False):
        if not gameconfig.overSpeedCheckSwitch():
            return
        if self.overSpeedCheckTimer > 0:
            self.pyDelTimer(self.overSpeedCheckTimer, gametimer.SPEED_STAT_CHECK)
            self.overSpeedCheckTimer = 0
        speedCheckTimeUnit = CONST.datas['speedCheckTimeUnit']['value']
        self.overSpeedCheckTimer = self.pyAddTimer(0, speedCheckTimeUnit, gametimer.SPEED_STAT_CHECK)
        if lastSpeed > 0:
            self.lastSpeed = lastSpeed
        else:
            if self.hasState(gameconst.StateEnum.Flying):
                self.lastSpeed = int(JDS.datas['thirdFlyHorizontalSpeed']['value'])
            elif self.hasState(CCDD.datas.blazing):
                self.lastSpeed = CONST.datas['blazeMaxSpeed']['value']
            else:
                self.lastSpeed = self.speed
        self.lastPosition = Math.Vector3(self.position.x, self.position.y, self.position.z)
        # 非初始化情况下，连续窗口单元内违规还是保留了
        if isInit:
            self.refreshSpeedCheckLimit()
            self.speedCheckCountPerWindow = 0
            self.speedCheckWindowSize = 0
            self.speedCheckContinuousUnit = 0
        LOG_DBG('ISpeedCheck::resetOverSpeedCheckTimer, speed: ', self.lastSpeed, self.speed, self.position)

    def refreshSpeedCheckLimit(self):
        datas = CONST.datas['speedCheckWindowSize']['value']
        minSize, maxSize = datas
        if minSize > maxSize or minSize <=0:
            LOG_ERR('ISpeedCheck::refreshSpeedCheckLimit, wrong speedCheckWindowSize cfg in const_const: ', datas)
            return
        self.speedCheckWindowSizeLimit = random.randint(minSize, maxSize)
        # 单个窗口单元内检测的大小，必须大于等于窗口大小的1/2
        goodPerWindowLimit = math.ceil(self.speedCheckWindowSizeLimit / 2)
        self.speedCheckCountPerWindowLimit = random.randint(goodPerWindowLimit, maxSize)

    def calculateOverSpeed(self):
        if not gameconfig.overSpeedCheckSwitch():
            # 关了开关，关闭引擎层统计，tick还是先1开着吧
            self.moveFlag = False 
            return
         
        if self.speedCheckCountPerWindowLimit <= 0 \
            or self.speedCheckCountPerWindowLimit <= 0:
            return 
        self.speedCheckWindowSize += 1
        # 读取引擎层移动距离统计
        moveDistance = self.moveDistance
        # 读取引擎层移动帧数统计
        moveCount = self.moveCount
        # 第一帧移动的距离
        firstMoveDistance = round(self.firstMoveDistance, 2)
        # 如果上次是变速度，第一帧单独计算
        if moveCount > 0 and firstMoveDistance > 0:
            # 流逝总的时间, 帧率*帧数
            elapsedTime = 0.1 * (moveCount - 1)
        else:
            # 流逝总的时间, 帧率*帧数
            elapsedTime = 0.1 * moveCount
        self.firstMoveDistance = 0.0
        # if round(firstMoveDistance, 1) > round(0.1 * self.lastSpeed, 1):
        #     # 超速了，拽回到上次的位置
        #     self.position = Math.Vector3(self.lastPosition.x, self.lastPosition.y, self.lastPosition.z)
        #     self.speedCheckContinuousUnit += 1
        #     LOG_DBG('ISpeedCheck::calculateOverSpeed first frame drag back, ', moveDistance, self.lastSpeed, self.lastPosition, firstMoveDistance)
        #     LogTrackingMgr.LogTrackingMgr.Illegal_Speed_Stat(self.gbId, self.clientDistinctIdCell, self.gbId, self.id, self.name, self.spaceNo, self.position, self.lastSpeed, -1, self.speedCheckWindowSize, self.speedCheckCountPerWindow, self.speedCheckContinuousUnit)
            
        #     return
        # 重置引擎层移动距离统计
        self.moveFlag = True
        # 如果大于N帧
        speedCheckTimeUnit = CONST.datas['speedCheckTimeUnit']['value']
        speedCheckFrameillegallyOverCount = CONST.datas['speedCheckFrameillegallyOverCount']['value']
        normalFrameCount = int(speedCheckTimeUnit / 0.1)
        overFrameCount = moveCount - normalFrameCount
        isOverSpeed = False
        if overFrameCount > 0:
            if overFrameCount > speedCheckFrameillegallyOverCount:
                LOG_DBG('ISpeedCheck::calculateOverSpeed, over frame:', speedCheckTimeUnit, moveCount, elapsedTime, \
                        moveDistance, self.lastSpeed, self.lastPosition, self.position, speedCheckFrameillegallyOverCount, overFrameCount)
                isOverSpeed = True
                overRate = 999999999
        
        if not isOverSpeed:
            speedCheckSpeedillegallyOverRate = CONST.datas['speedCheckSpeedillegallyOverRate']['value']
            # 客户端实际的移动距离
            realClientDistance = round(moveDistance, 1)
            # 服务端计算的真实的移动距离
            realServerDistance = round(self.lastSpeed * elapsedTime, 1)
            isOverSpeed = False
            overRate = 0.0

            if realClientDistance > realServerDistance:
                # 服务端移动距离为0
                if realServerDistance == 0:
                    # 客户端有传帧上来属于异常行为
                    if moveCount > 0:
                        overRate = 88888888
                        LOG_DBG('ISpeedCheck::calculateOverSpeed, over speed 1:', realClientDistance, realServerDistance, elapsedTime, \
                                moveCount, self.lastSpeed, self.lastPosition, self.position, overRate, speedCheckSpeedillegallyOverRate)

                        isOverSpeed = True
                else:
                    overRate = round(abs((realClientDistance - realServerDistance) / realServerDistance), 2)
                    if overRate >= speedCheckSpeedillegallyOverRate / 100.0:
                        LOG_DBG('ISpeedCheck::calculateOverSpeed, over speed 2:', realClientDistance, realServerDistance, elapsedTime, \
                                moveCount, self.lastSpeed, self.lastPosition, self.position, overRate, speedCheckSpeedillegallyOverRate)
                        isOverSpeed = True
        # 连续超速累计
        if isOverSpeed:
            self.speedCheckCountPerWindow += 1
        
        # 是否进入了窗口大小的计算
        isInWindow = False
        # 滑动窗口数到了，开始检测
        if self.speedCheckWindowSize >= self.speedCheckWindowSizeLimit:
            # 一个窗口内超过置顶次数，执行拉回操作
            if self.speedCheckCountPerWindow >= self.speedCheckCountPerWindowLimit:
                # 连续超速了，拽回到上次的位置
                self.position = Math.Vector3(self.lastPosition.x, self.lastPosition.y, self.lastPosition.z)
                LOG_DBG('ISpeedCheck::calculateOverSpeed drag back, ', moveDistance, self.lastSpeed, self.lastPosition, self.speedCheckWindowSize, self.speedCheckCountPerWindow)
                # 一个窗口内违规了一次
                self.speedCheckContinuousUnit += 1
            else:
                # 清理连续窗口违规行为
                self.speedCheckContinuousUnit = 0
            isInWindow = True
        
        # 记录每个窗口子单位的状态数据
        self.speedCheckRecord.append([isOverSpeed, Math.Vector3(self.lastPosition.x, self.lastPosition.y, self.lastPosition.z)])

        # 超速记录日志
        if overRate > 0:
            LogTrackingMgr.LogTrackingMgr.Illegal_Speed_Stat(self.gbId, self.clientDistinctIdCell, self.gbId, self.id, self.name, self.spaceNo, self.position, self.lastSpeed, overRate, self.speedCheckWindowSize, self.speedCheckCountPerWindow, self.speedCheckContinuousUnit)
        
        # 连续N个窗口单元了，清理
        if self.speedCheckContinuousUnit >= CONST.datas['speedCheckContinuousUnit']['value']:
            self.speedCheckContinuousUnit = 0

        if isInWindow:           
            lastSpeedCheckWindowSizeLimit = self.speedCheckWindowSizeLimit
            # 一轮检测结束刷新窗口和检测限制
            self.refreshSpeedCheckLimit()
            # 新窗口大于等于老窗口大小，卸载最早的一个窗口单元
            if self.speedCheckWindowSizeLimit >= lastSpeedCheckWindowSizeLimit:
                removeCount = 1
            # 新窗口小于老窗口大小，卸载前面的窗口单元
            else:
                removeCount = lastSpeedCheckWindowSizeLimit - self.speedCheckWindowSizeLimit + 1
            # 移除需要废弃的窗口单元
            for _ in range(0, removeCount):
                if len(self.speedCheckRecord) > 0:
                    self.speedCheckRecord.pop(0)
            # 调整滑动窗口大小
            self.speedCheckWindowSize -= removeCount
            # 重新计算新窗口已超速次数
            self.speedCheckCountPerWindow = 0
            lastPosition = None
            for data in self.speedCheckRecord:
                if lastPosition is None:
                    pos = data[1]
                    lastPosition = Math.Vector3(pos.x, pos.y, pos.z)
                if data[0]:
                    self.speedCheckCountPerWindow += 1
            # 重新计算上次的位置
            if not (lastPosition is None):
                self.lastPosition = lastPosition
            
    def speedChanged(self, newSpeed, oldSpeed):
        if not gameconfig.overSpeedCheckSwitch():
            return
        LOG_DBG('ISpeedCheck::speedChanged, 1 ', newSpeed, oldSpeed, self.position)
        realSpeed = newSpeed
        if oldSpeed >= newSpeed:
            realSpeed = oldSpeed
        if self.hasState(gameconst.StateEnum.Flying):
            realSpeed = int(JDS.datas['thirdFlyHorizontalSpeed']['value'])
        elif self.hasState(CCDD.datas.blazing):
            realSpeed = CONST.datas['blazeMaxSpeed']['value']
        self.lastSpeed = realSpeed
        self.calculateOverSpeed()
        # 只监听客户端的idle状态变更
        if self.hasTempMiscProp(gameconst.EntityPropsEnum.clientIdleChangeSpeed):
            LOG_DBG('ISpeedCheck::speedChanged, 2 client speed change ', newSpeed, oldSpeed, self.position)
            self.speedChange = True
        self.resetOverSpeedCheckTimer(realSpeed)
    
    def enterFlySpeed(self):
        LOG_DBG('ISpeedCheck::enterFlySpeed, 1')
        self.calculateOverSpeed()
        # 这里是在设置状态之前进入的飞行
        realSpeed = int(JDS.datas['thirdFlyHorizontalSpeed']['value'])
        self.resetOverSpeedCheckTimer(realSpeed)

    def leaveFlySpeed(self):
        LOG_DBG('ISpeedCheck::leaveFlySpeed, 1')
        self.calculateOverSpeed()
        self.resetOverSpeedCheckTimer()

    def enterBlazeState(self):
        LOG_DBG('ISpeedCheck::enterBlazeState, 1')
        self.calculateOverSpeed()
        realSpeed = CONST.datas['blazeMaxSpeed']['value']
        self.resetOverSpeedCheckTimer(realSpeed)

    def leaveBlazeState(self):
        LOG_DBG('ISpeedCheck::leaveBlazeState, 1')
        self.calculateOverSpeed()
        self.resetOverSpeedCheckTimer()