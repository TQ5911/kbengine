import time

import KBEngine
from KBEDebug import *

import utils
import itemFactory
import gameconst
import gearEnhance_gearconst as GEGCD
import gearEnhance_gearBless as GEBLD


QA_EQUIP_BLESS_CACHE = {}

BATCH_TIME_COUNT_INIT = 20
BATCH_TIME_COUNT_MIN = 5
BATCH_TIME_COUNT_MAX = 200
TARGET_TICK_S = 0.3

CACHE_STATUS_NOT_FOUND = 'not_found'
CACHE_STATUS_RUNNING = 'running'
CACHE_STATUS_FINISHED = 'finished'


class EquipBlessUnit:
    """
    装备祝福养成概率模拟器

    用法示例:
        tester = EquipBlessUnit(1000)
        result = tester.calcBlessExpectation(50010101, callback=myCallback)
    """

    def __init__(self, su, totalTimes):
        """
        totalTimes: 模拟的装备件数，即重复创建新装备进行祝福的次数
        """
        self.su = su
        self.totalTimes = totalTimes

    def _createEquip(self, equipId):
        equipItem = itemFactory.ItemFactory.createItem(equipId)
        if not equipItem:
            LOG_ERR('EquipBlessUnit._createEquip failed, equipId:', equipId)
            return None
        return equipItem

    @staticmethod
    def _canBackBless(equipItem):
        """本地实现的回溯判断，不含LOG_ERR，避免批量模拟时刷爆日志"""
        if len(equipItem.equipAttr.blessAffixes) == 0:
            return False
        curBlessVal = equipItem.equipAttr.blessAffixes[0].affixVal
        key = equipItem.equipAttr.getBlessKey(equipItem.equipAttr.maxBlessLv)
        cfgData = GEBLD.datas.get(key)
        if not cfgData:
            return False
        backtrack = cfgData.get('backtrack')
        if not backtrack:
            return False
        if equipItem.equipAttr.maxBlessLv <= curBlessVal:
            return False
        if equipItem.equipAttr.blessLvRate < backtrack:
            return False
        return True

    def _blessOneEquip(self, equipId):
        """
        模拟一件装备从初始等级祝福到最大等级。
        返回 (bless次数, backBless次数, 每级统计)，出错返回 (0, 0, {})
        
        每级统计格式: {level: {'attempts': N, 'up': N, 'fail': N, 'down': N}}
        level: 祝福前的等级, up/fail/down: 该级上升/失败/下降次数
        """
        equipItem = self._createEquip(equipId)
        if not equipItem:
            return 0, 0, {}

        gearBlessMaxValue = GEGCD.datas['gearBlessMaxValue']['value']
        blessCount = 0
        backBlessCount = 0
        levelStats = {}

        while True:
            # 记录祝福前的等级
            if len(equipItem.equipAttr.blessAffixes) == 0:
                oldVal = 0
            else:
                oldVal = equipItem.equipAttr.blessAffixes[0].affixVal

            try:
                equipItem.doEquipBlessing()
                blessCount += 1
            except Exception as e:
                LOG_ERR('_blessOneEquip doEquipBlessing error:', equipId, e)
                break

            newVal = equipItem.equipAttr.blessAffixes[0].affixVal
            delta = newVal - oldVal

            if oldVal not in levelStats:
                levelStats[oldVal] = {'attempts': 0, 'up': 0, 'fail': 0, 'down': 0, 'firstBlessCount': blessCount}
            levelStats[oldVal]['attempts'] += 1
            if delta > 0:
                levelStats[oldVal]['up'] += 1
            elif delta < 0:
                levelStats[oldVal]['down'] += 1
            else:
                levelStats[oldVal]['fail'] += 1

            if self._canBackBless(equipItem):
                try:
                    equipItem.doEquipBackBless()
                    backBlessCount += 1
                except Exception as e:
                    LOG_ERR('_blessOneEquip doEquipBackBless error:', equipId, e)

            if newVal >= gearBlessMaxValue:
                break

        return blessCount, backBlessCount, levelStats

    def _genCacheKey(self, equipId):
        return 'equipBless_%s_%s' % (equipId, self.totalTimes)

    def _updateProcessInfo(self, cacheKey, cur, total=None):
        QA_EQUIP_BLESS_CACHE[cacheKey]['process_info']['cur'] = cur
        if total:
            QA_EQUIP_BLESS_CACHE[cacheKey]['process_info']['total'] = total

    def _getProcessInfo(self, cacheKey):
        return QA_EQUIP_BLESS_CACHE[cacheKey]['process_info']

    def _getCacheResult(self, cacheKey, callback=None):
        cacheStatus = QA_EQUIP_BLESS_CACHE.get(cacheKey, {}).get('status', CACHE_STATUS_NOT_FOUND)

        if cacheStatus == CACHE_STATUS_FINISHED:
            ret = QA_EQUIP_BLESS_CACHE[cacheKey]['data']
            if callback:
                QA_EQUIP_BLESS_CACHE[cacheKey]['callbacks'].append(callback)
                self._doCacheCallback(cacheKey)
            del QA_EQUIP_BLESS_CACHE[cacheKey]
            return True, cacheStatus, ret, {}
        elif cacheStatus == CACHE_STATUS_RUNNING:
            if callback:
                QA_EQUIP_BLESS_CACHE[cacheKey]['callbacks'].append(callback)
            process_info = self._getProcessInfo(cacheKey)
            return False, cacheStatus, '正在执行中，请等待', process_info

        QA_EQUIP_BLESS_CACHE[cacheKey] = {
            'data': None,
            'status': CACHE_STATUS_RUNNING,
            'callbacks': [],
            'process_info': {},
        }
        if callback:
            QA_EQUIP_BLESS_CACHE[cacheKey]['callbacks'].append(callback)
        self._updateProcessInfo(cacheKey, 0, self.totalTimes)
        return False, cacheStatus, '开始执行，请等待', {}

    def _setCacheResult(self, cacheKey, data):
        QA_EQUIP_BLESS_CACHE[cacheKey]['data'] = data
        QA_EQUIP_BLESS_CACHE[cacheKey]['status'] = CACHE_STATUS_FINISHED
        self._doCacheCallback(cacheKey)

    def _doCacheCallback(self, cacheKey):
        callbacks = QA_EQUIP_BLESS_CACHE[cacheKey]['callbacks']
        data = QA_EQUIP_BLESS_CACHE[cacheKey]['data']
        for cb in callbacks:
            cb(data)
        QA_EQUIP_BLESS_CACHE[cacheKey]['callbacks'] = []

    def _buildResult(self, equipId, gearBlessMaxValue, totalBlessCount, totalBackBlessCount, blessCountList, allLevelStats):
        avgBlessToMax = totalBlessCount / max(self.totalTimes, 1)
        avgBackBless = totalBackBlessCount / max(self.totalTimes, 1)
        minBless = min(blessCountList) if blessCountList else 0
        maxBless = max(blessCountList) if blessCountList else 0

        # 每级统计整理：计算期望次数和概率
        levelSummary = {}
        for lv in sorted(allLevelStats.keys()):
            s = allLevelStats[lv]
            total = s['attempts']
            avgAtt = round(total / max(self.totalTimes, 1), 2)
            levelSummary[lv] = {
                'attempts': total,
                'avgPerEquip': avgAtt,
                'firstBlessCount': round(s['firstBlessCount']/self.totalTimes, 2),
                'upProb': round(s['up'] / max(total, 1) * 100, 2),
                'failProb': round(s['fail'] / max(total, 1) * 100, 2),
                'downProb': round(s['down'] / max(total, 1) * 100, 2),
                'up': s['up'],
                'fail': s['fail'],
                'down': s['down'],
            }

        # 按区间统计分布 (区间宽度: 每200次一个桶，因为数值范围可能很大)
        dataRange = maxBless - minBless
        if dataRange <= 1000:
            bucketSize = 50
        elif dataRange <= 5000:
            bucketSize = 200
        else:
            bucketSize = 500
        distribution = {}
        for cnt in blessCountList:
            bucket = (cnt // bucketSize) * bucketSize
            label = '{}-{}'.format(bucket, bucket + bucketSize - 1)
            distribution[label] = distribution.get(label, 0) + 1

        return {
            'equipId': equipId,
            'category': 'equipBless',
            'gearBlessMaxValue': gearBlessMaxValue,
            'totalEquips': self.totalTimes,
            'totalBless': totalBlessCount,
            'avgBlessToMax': round(avgBlessToMax, 2),
            'totalBackBless': totalBackBlessCount,
            'avgBackBless': round(avgBackBless, 2),
            'minBless': minBless,
            'maxBless': maxBless,
            'levelSummary': levelSummary,
            'distribution': distribution,
        }

    def calcBlessExpectation(self, equipId, callback=None):
        """
        计算指定装备从0级祝福到最大等级的期望次数（timer分批回调）。
        未完成时相同请求返回当前进度，完成时通过callback通知或直接返回结果。

        返回 (isDone, data, process_info)
        """
        cacheKey = self._genCacheKey(equipId)
        ret, cacheStatus, content, process_info = self._getCacheResult(cacheKey, callback)
        if cacheStatus != CACHE_STATUS_NOT_FOUND:
            return ret, content, process_info

        gearBlessMaxValue = GEGCD.datas['gearBlessMaxValue']['value']
        LOG_INFO('EquipBlessUnit.calcBlessExpectation equipId:', equipId, 'totalTimes:', self.totalTimes)

        totalBlessCount = 0
        totalBackBlessCount = 0
        blessCountList = []
        allLevelStats = {}   # 汇总每级统计
        processed = 0
        current_batch_size = BATCH_TIME_COUNT_INIT

        def process_batch():
            nonlocal totalBlessCount, totalBackBlessCount, processed, current_batch_size, allLevelStats
            tick_start = time.perf_counter()

            while processed < self.totalTimes:
                remaining = self.totalTimes - processed
                batch_size = min(current_batch_size, remaining)

                batch_start = time.perf_counter()
                batch_count = 0
                for _ in range(batch_size):
                    blessCount, backBlessCount, levelStats = self._blessOneEquip(equipId)
                    totalBlessCount += blessCount
                    totalBackBlessCount += backBlessCount
                    blessCountList.append(blessCount)

                    # 汇总每级统计
                    for lv, stats in levelStats.items():
                        if lv not in allLevelStats:
                            allLevelStats[lv] = {'firstBlessCount': 0, 'attempts': 0, 'up': 0, 'fail': 0, 'down': 0}
                        for k in ('firstBlessCount', 'attempts', 'up', 'fail', 'down'):
                            allLevelStats[lv][k] += stats[k]

                    batch_count += 1

                    # 每件装备跑完都检查 tick，避免单件耗时太长导致整帧卡死
                    if time.perf_counter() - tick_start >= TARGET_TICK_S:
                        break
                batch_elapsed = time.perf_counter() - batch_start

                processed += batch_count
                self._updateProcessInfo(cacheKey, processed)

                # 动态调整批次大小
                if batch_elapsed > TARGET_TICK_S * 2:
                    current_batch_size = max(BATCH_TIME_COUNT_MIN, current_batch_size // 2)
                elif batch_elapsed < TARGET_TICK_S * 0.5:
                    current_batch_size = min(BATCH_TIME_COUNT_MAX, current_batch_size * 2)

                LOG_DBG("EquipBlessUnit: equipId:%s processed:%s/%s batchCount:%s batchElapsed:%.4f batchSize:%s" %
                        (equipId, processed, self.totalTimes, batch_count, batch_elapsed, current_batch_size))

                if time.perf_counter() - tick_start >= TARGET_TICK_S:
                    break

            if processed >= self.totalTimes:
                result = self._buildResult(equipId, gearBlessMaxValue, totalBlessCount, totalBackBlessCount, blessCountList, allLevelStats)
                LOG_INFO('EquipBlessUnit result:', result)
                self._setCacheResult(cacheKey, result)
            else:
                KBEngine.addTimer(1, 0, lambda tid: process_batch())

        process_batch()
        return ret, content, process_info

    def batchCalcBlessExpectation(self, equipIds, callback=None):
        """
        批量计算多个装备的祝福期望
        """
        results = []

        def make_callback(_equipId, _results):
            def inner_callback(data):
                _results.append(data)
                if len(_results) >= len(equipIds) and callback:
                    callback(_results)
            return inner_callback

        for equipId in equipIds:
            self.calcBlessExpectation(equipId, callback=make_callback(equipId, results))
        return results


def doBlessTest(equipId, totalTimes=1000, callback=None):
    tester = EquipBlessUnit(totalTimes)
    return tester.calcBlessExpectation(equipId, callback=callback)


def doBatchBlessTest(equipIds, totalTimes=1000, callback=None):
    tester = EquipBlessUnit(totalTimes)
    return tester.batchCalcBlessExpectation(equipIds, callback=callback)


'''
# 在KBEngine控制台中使用:
import sys
del sys.modules['server_common.test.equipTest']
from server_common.test import equipTest

# 单个装备测试（支持 callback）
tester = equipTest.EquipBlessUnit(10000)
isDone, data, process_info = tester.calcBlessExpectation(80114001)

# 带回调
def onDone(data):
    print(data)
tester.calcBlessExpectation(80114001, callback=onDone)

# 批量测试
results = tester.batchCalcBlessExpectation([50010101, 50010102])
'''
