# -*- coding: utf-8 -*-

from KBEDebug import *
import KBEngine

import utils
import formula
import gametimer
import gameconfig
import gameconst

import worldBoss_base as WB_BASE
import mutex_mutex as MUTEX_MD
import mutex_set as MUTEX_SET_MD
import formula_generalFormula as F_GFD


class IBossMutexCell(object):
    """BOSS 互斥组 Cell 侧 Mixin"""

    def __init__(self):
        if not hasattr(self, 'bossMutexCoolDownDict'):
            self.bossMutexCoolDownDict = {}
        self.onBossMutexLoginInit()

    # ---------------------------------------------------------------
    # 公共工具
    # ---------------------------------------------------------------
    @staticmethod
    def _toMutexMapId(mapId):
        """互斥表按本服地图配置，跨服世界boss地图统一还原为本服地图id"""
        return WB_BASE.cross2LocalMap.get(mapId, mapId)

    def _getBossMutexCoolDownSec(self, srcMapId, toMapId):
        """按"源地图+目标地图"用公式表公式动态计算冷却时长（秒）"""
        formulaId = MUTEX_SET_MD.datas['mutexFormula']['value']
        formulaData = F_GFD.datas.get(formulaId)
        if not formulaData:
            LOG_ERR('_getBossMutexCoolDownSec: formula not found', formulaId)
            return 0
        return formulaData['serverFormula'](srcMapId, toMapId)

    def _getBossMutexMaxCoolDownSec(self, groupId, srcMapId):
        """取组内所有目标地图中的最大冷却时长，用于过期清理"""
        groupData = MUTEX_MD.datas.get(groupId)
        if not groupData:
            return 0
        maxCdSec = 0
        for toMapId in groupData['scene']:
            cdSec = self._getBossMutexCoolDownSec(srcMapId, toMapId)
            if cdSec > maxCdSec:
                maxCdSec = cdSec
        return maxCdSec

    # ---------------------------------------------------------------
    # 冷却状态管理
    # ---------------------------------------------------------------
    def addBossMutexCoolDown(self, groupId, srcMapId, srcLineNo):
        """添加互斥冷却，起始时间为当前时间，时长在判定时按目标地图动态计算"""
        srcMapId = self._toMutexMapId(srcMapId)
        LOG_INFO(f'addBossMutexCoolDown: {groupId}:{srcMapId}-{srcLineNo}')
        self.bossMutexCoolDownDict[groupId] = {
            'startTs': utils.curTS(),
            'srcMapId': srcMapId,
            'srcLineNo': srcLineNo,
        }
        self.syncBossMutexCoolDownToClient()

        # 跨服上触发的冷却同步回本服 avatar，否则跨服副本销毁后冷却丢失
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerCell(
                'addBossMutexCoolDown',
                (groupId, srcMapId, srcLineNo)
            )

    def isBossMutexCoolDown(self, groupId, toMapId):
        """检查是否处于冷却中，返回 (isInCoolDown, leftSec)，时长按目标地图动态计算"""
        data = self.bossMutexCoolDownDict.get(groupId)
        if not data:
            return False, 0

        startTs = data['startTs']
        endTs = startTs + self._getBossMutexCoolDownSec(data['srcMapId'], toMapId)
        now = utils.curTS()
        if endTs > now:
            return True, endTs - now

        # 单条记录是否彻底过期与目标地图相关，按组内最大冷却时长判定后再惰性清理
        if now > startTs + self._getBossMutexMaxCoolDownSec(groupId, data['srcMapId']):
            self.bossMutexCoolDownDict.pop(groupId, None)
        return False, 0

    def onBossMutexLoginInit(self):
        """登录/创建 Cell 时清理过期冷却，过期与否按组内最大冷却时长判定"""
        now = utils.curTS()
        for groupId, data in list(self.bossMutexCoolDownDict.items()):
            maxCdSec = self._getBossMutexMaxCoolDownSec(groupId, data['srcMapId'])
            if now > data['startTs'] + maxCdSec:
                self.bossMutexCoolDownDict.pop(groupId, None)

    def syncBossMutexCoolDownToClient(self):
        """同步冷却列表到客户端"""
        if not self.client:
            return
        dataList = []
        for groupId, data in self.bossMutexCoolDownDict.items():
            dataList.append({
                'groupId': groupId,
                'startTs': data['startTs'],
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
        toMapId = self._toMutexMapId(toMapId)
        for groupId in list(self.bossMutexCoolDownDict.keys()):
            groupData = MUTEX_MD.datas.get(groupId)
            if not groupData or toMapId not in groupData['scene']:
                continue

            inCd, leftSec = self.isBossMutexCoolDown(groupId, toMapId)
            if not inCd:
                continue

            # 同地图同分线（同一 spaceNo）放行
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
        toMapId = self._toMutexMapId(toMapId)
        for groupId in list(self.bossMutexCoolDownDict.keys()):
            groupData = MUTEX_MD.datas.get(groupId)
            if not groupData or toMapId not in groupData['scene']:
                continue

            inCd, leftSec = self.isBossMutexCoolDown(groupId, toMapId)
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
