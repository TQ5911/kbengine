# -*- coding: utf-8 -*-

from KBEDebug import *
import KBEngine

import utils
import formula
import gametimer
import gameconfig
import gameconst

import mutex_mutex as MUTEX_MD


class IBossMutexCell(object):
    """BOSS 互斥组 Cell 侧 Mixin"""

    def __init__(self):
        if not hasattr(self, 'bossMutexCoolDownDict'):
            self.bossMutexCoolDownDict = {}
        self.onBossMutexLoginInit()

    # ---------------------------------------------------------------
    # 公共工具
    # ---------------------------------------------------------------
    def _getBossMutexCoolDownSec(self, groupId):
        groupData = MUTEX_MD.datas.get(groupId)
        if groupData:
            return groupData['time']
        return 0

    # ---------------------------------------------------------------
    # 冷却状态管理
    # ---------------------------------------------------------------
    def addBossMutexCoolDown(self, groupId, srcMapId, srcLineNo, cdSec=None):
        LOG_INFO(f'addBossMutexCoolDown: {groupId}:{srcMapId}-{srcLineNo} {cdSec}')
        """添加互斥冷却"""
        if cdSec is None:
            cdSec = self._getBossMutexCoolDownSec(groupId)
        if cdSec <= 0:
            return

        endTs = utils.curTS() + cdSec
        self.bossMutexCoolDownDict[groupId] = {
            'endTs': endTs,
            'srcMapId': srcMapId,
            'srcLineNo': srcLineNo,
        }
        self.syncBossMutexCoolDownToClient()

        # 跨服上触发的冷却同步回本服 avatar，否则跨服副本销毁后冷却丢失
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerCell(
                'addBossMutexCoolDown',
                (groupId, srcMapId, srcLineNo, cdSec)
            )

    def isBossMutexCoolDown(self, groupId):
        """检查是否处于冷却中，返回 (isInCoolDown, leftSec)"""
        data = self.bossMutexCoolDownDict.get(groupId)
        if not data:
            return False, 0

        endTs = data['endTs']
        now = utils.curTS()
        if endTs > now:
            return True, endTs - now

        self.bossMutexCoolDownDict.pop(groupId, None)
        return False, 0

    def onBossMutexLoginInit(self):
        """登录/创建 Cell 时清理过期冷却"""
        now = utils.curTS()
        for groupId, data in list(self.bossMutexCoolDownDict.items()):
            if data['endTs'] <= now:
                self.bossMutexCoolDownDict.pop(groupId, None)

    def syncBossMutexCoolDownToClient(self):
        """同步冷却列表到客户端"""
        if not self.client:
            return
        dataList = []
        for groupId, data in self.bossMutexCoolDownDict.items():
            dataList.append({
                'groupId': groupId,
                'endTs': data['endTs'],
                'srcMapId': data['srcMapId'],
                'srcLineNo': data.get('srcLineNo', 0xFFFF),
            })
        self.client.onBossMutexCoolDownUpdate(dataList)

    # ---------------------------------------------------------------
    # 进入/切线拦截检查
    # ---------------------------------------------------------------
    def checkBossMutexBlock(self, toMapId, toLineNo=None):
        """检查进入/切线到目标地图是否被限制
        toLineNo 为目标分线号，None/-1 表示目标分线未知（自动选线），按不同线处理
        返回 (isBlocked, leftSec)
        """
        for groupId in list(self.bossMutexCoolDownDict.keys()):
            groupData = MUTEX_MD.datas.get(groupId)
            if not groupData or toMapId not in groupData['scene']:
                continue

            inCd, leftSec = self.isBossMutexCoolDown(groupId)
            if not inCd:
                continue

            # 同地图同分线（同一 spaceNo）放行；旧数据无 srcLineNo 时不放行
            data = self.bossMutexCoolDownDict.get(groupId)
            srcLineNo = data.get('srcLineNo')
            if srcLineNo is not None and srcLineNo >= 0 and toMapId == data['srcMapId'] and toLineNo == srcLineNo:
                continue

            LOG_DBG('checkBossMutexBlock:', True, leftSec)
            return True, leftSec

        LOG_DBG('checkBossMutexBlock:', False, 0)
        return False, 0

    def checkBossMutexBlockAutoEnter(self, toMapId):
        """自动选线进入目标地图的互斥检查
        返回 (isBlocked, leftSec, bossMutexLine)
        - 目标地图是触发冷却的源地图：放行，并返回应优先选择的源分线号
        - 目标地图是同组其他地图：拦截
        - 不在任何冷却组内：放行
        """
        for groupId in list(self.bossMutexCoolDownDict.keys()):
            groupData = MUTEX_MD.datas.get(groupId)
            if not groupData or toMapId not in groupData['scene']:
                continue

            inCd, leftSec = self.isBossMutexCoolDown(groupId)
            if not inCd:
                continue

            data = self.bossMutexCoolDownDict.get(groupId)
            srcLineNo = data.get('srcLineNo')
            if srcLineNo is not None and srcLineNo >= 0 and toMapId == data['srcMapId']:
                LOG_DBG('checkBossMutexBlockAutoEnter:', False, 0, srcLineNo)
                return False, 0, srcLineNo

            LOG_DBG('checkBossMutexBlockAutoEnter:', True, leftSec, None)
            return True, leftSec, None

        LOG_DBG('checkBossMutexBlockAutoEnter:', False, 0, None)
        return False, 0, None
