# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import gameconst
import gameglobal
import gametimer
import utils

import iCell
import iTimer
import iChat
import iEmote


class AvataringStateRef(object):
    """Avataring 状态位参考定义（0~127），实际语义由客户端控制。"""
    Idle        = 0
    Moving      = 1
    Posture     = 2
    # 3 ~ 127 由客户端扩展


class Avataring(KBEngine.Entity, iTimer.ITimer):
    def __init__(self):
        LOG_INFO("Avataring::__intit__~")
        KBEngine.Entity.__init__(self)
        iTimer.ITimer.__init__(self)

        self.isWitnessComplete = False

    # ----------------------------
    # 状态位基础操作（服务器只同步，不处理语义和冲突）
    # ----------------------------
    def hasAvataringState(self, stateIdx):
        """查询某状态位是否置位，仅服务器内部使用。"""
        if stateIdx < 0 or stateIdx >= 128:
            return False
        if stateIdx < 64:
            return (self.state >> stateIdx) & 1 > 0
        return (self.state2 >> (stateIdx - 64)) & 1 > 0

    def setAvataringState(self, stateIdx):
        """设置某状态位。"""
        if stateIdx < 0 or stateIdx >= 128:
            LOG_ERR('Avataring::setAvataringState invalid stateIdx', stateIdx)
            return
        if stateIdx < 64:
            self.state |= (1 << stateIdx)
        else:
            self.state2 |= (1 << (stateIdx - 64))

    def removeAvataringState(self, stateIdx):
        """取消某状态位。"""
        if stateIdx < 0 or stateIdx >= 128:
            LOG_ERR('Avataring::removeAvataringState invalid stateIdx', stateIdx)
            return
        if stateIdx < 64:
            self.state &= ~(1 << stateIdx)
        else:
            self.state2 &= ~(1 << (stateIdx - 64))

    # ----------------------------
    # 客户端请求入口
    # ----------------------------
    @utils.isMyself
    def clientSetState(self, exposed, stateIdx):
        LOG_DBG('Avataring::clientSetState', stateIdx)
        self.setAvataringState(stateIdx)

    @utils.isMyself
    def clientRemoveState(self, exposed, stateIdx):
        LOG_DBG('Avataring::clientRemoveState', stateIdx)
        self.removeAvataringState(stateIdx)

    def onBaseGetCell(self):
        LOG_INFO('Avataring::onBaseGetCell~')
        self.base.onGetCellSpaceNo(self.spaceNo)

    def onGetWitness(self, chn):
        LOG_INFO('Avataring::onGetWitness~', chn)
        self.isWitnessComplete = True
        self.base.onCellGetWitness(chn)

    def onDestroy(self):
        LOG_INFO('Avataring::onDestroy~')
