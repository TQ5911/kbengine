import time

import KBEngine
from KBEDebug import *

import utils
import itemFactory
import gameconst
import gearEnhance_gearStrengthen as GEGS


QA_EQUIP_ENHANCE_CACHE = {}

BATCH_TIME_COUNT_INIT = 20
BATCH_TIME_COUNT_MIN = 5
BATCH_TIME_COUNT_MAX = 200
TARGET_TICK_S = 0.3

CACHE_STATUS_NOT_FOUND = 'not_found'
CACHE_STATUS_RUNNING = 'running'
CACHE_STATUS_FINISHED = 'finished'


class EquipEnhanceUnit:
    """
    装备强化养成概率模拟器

    用法示例:
        tester = EquipEnhanceUnit(0, 1000)
        result = tester.calcEnhanceExpectation(50010101, callback=myCallback)

    与 equipTest.EquipBlessUnit 的差异:
        - 祝福调用 doEquipBlessing()，强化直接调用 equipItem.doEnhanceEquip(owner, opUUID, level)，
          level 传当前 enhanceLv，与正式强化流程一致（onBody=False 时 owner/opUUID 不会被使用）。
        - 满级判定与正式 enhanceNeedItems/checkEnhancementValid 一致：下一强化等级配置
          不存在即视为已到最大等级。该守卫只是循环终止条件（辅助逻辑），核心强化仍由
          doEnhanceEquip 完成；同时它避免 doEnhanceEquip 在 effect=0 的满级条目上 _calcEnhanceVal 崩溃。
        - 强化没有祝福那样的回溯(doEquipBackBless)机制，因此不再有 backBless 相关统计。
          （注：equipTest._canBackBless 本地化是因为正式 isCanBackBless 依赖玩家上下文——
           玩家进度/历史最大值等，脚本只需"满足条件即触发"的纯判定；强化无此机制，无需对应处理。）
        - 强化存在"破碎"(-99, ENHANCEMENT_BROKEN_FLAG)这一终端失败结果，统计中额外给出
          破碎率、每级破碎概率；破碎即停止，该装备不再继续强化。
        - 每级统计增加 'broken' 字段；'up/fail/down' 以 doEnhanceEquip 内部 doEnhanceLv
          后实际等级变化为准（encVal=-1 但被 clamp 到 0 时记为 fail，与游戏真实行为一致）。
        - "强化到满级的期望次数" 只在成功达到满级的装备上统计（破碎装备不参与该分布）。
    """

    def __init__(self, su, totalTimes):
        """
        totalTimes: 模拟的装备件数，即重复创建新装备进行强化的次数
        """
        self.su = su
        self.totalTimes = totalTimes

    def _createEquip(self, equipId):
        equipItem = itemFactory.ItemFactory.createItem(equipId)
        if not equipItem:
            LOG_ERR('EquipEnhanceUnit._createEquip failed, equipId:', equipId)
            return None
        return equipItem

    def _enhanceOneEquip(self, equipId):
        """
        模拟一件装备从 0 级强化到最大等级。
        返回 (强化次数, 是否达到满级, 是否破碎, 每级统计)，出错返回 (0, False, False, {})

        每级统计格式: {level: {'attempts': N, 'up': N, 'fail': N, 'down': N, 'broken': N, 'firstEnhanceCount': N}}
        level: 强化前的等级, up/fail/down/broken: 该级上升/不变/下降/破碎次数
        """
        equipItem = self._createEquip(equipId)
        if not equipItem:
            return 0, False, False, {}

        brokenFlag = gameconst.EquipConstVale.ENHANCEMENT_BROKEN_FLAG
        enhanceCount = 0
        reachedMax = False
        isBroken = False
        levelStats = {}

        while True:
            # 记录强化前的等级
            curLv = equipItem.equipAttr.enhanceLv

            # 满级判定：与正式 enhanceNeedItems/checkEnhancementValid 一致，
            # 下一强化等级配置不存在则视为已到最大等级（同时避免 doEnhanceEquip
            # 在 effect=0 的满级条目上 _calcEnhanceVal 崩溃）
            nextKey = equipItem.equipAttr.getEnhanceLevelKey(curLv + 1)
            if not GEGS.datas.get(nextKey):
                reachedMax = True
                break

            oldLv = curLv
            # 核心强化逻辑：直接调用 doEnhanceEquip，level 传当前 enhanceLv，
            # 与正式流程一致。onBody=False 时 owner/opUUID 不会被使用，故传 None/0。
            try:
                encVal = equipItem.doEnhanceEquip(None, 0, curLv, onBody=False, isGM=False)
            except Exception as e:
                LOG_ERR('_enhanceOneEquip doEnhanceEquip error:', equipId, e)
                break

            enhanceCount += 1

            if curLv not in levelStats:
                levelStats[curLv] = {'attempts': 0, 'up': 0, 'fail': 0, 'down': 0, 'broken': 0,
                                     'firstEnhanceCount': enhanceCount}
            levelStats[curLv]['attempts'] += 1

            # doEnhanceEquip 在配置缺失时返回 None（理论上已被上面的守卫挡住，保险起见）
            if encVal is None:
                reachedMax = True
                break

            if encVal == brokenFlag:
                # 装备破碎：终端失败，装备销毁，停止强化
                levelStats[curLv]['broken'] += 1
                isBroken = True
                break

            # doEnhanceEquip 内部已调用 doEnhanceLv(encVal) 完成等级写入，这里只读结果做统计
            newLv = equipItem.equipAttr.enhanceLv
            delta = newLv - oldLv
            if delta > 0:
                levelStats[curLv]['up'] += 1
            elif delta < 0:
                levelStats[curLv]['down'] += 1
            else:
                levelStats[curLv]['fail'] += 1

        return enhanceCount, reachedMax, isBroken, levelStats

    def _genCacheKey(self, equipId):
        return 'equipEnhance_%s_%s' % (equipId, self.totalTimes)

    def _updateProcessInfo(self, cacheKey, cur, total=None):
        QA_EQUIP_ENHANCE_CACHE[cacheKey]['process_info']['cur'] = cur
        if total:
            QA_EQUIP_ENHANCE_CACHE[cacheKey]['process_info']['total'] = total

    def _getProcessInfo(self, cacheKey):
        return QA_EQUIP_ENHANCE_CACHE[cacheKey]['process_info']

    def _getCacheResult(self, cacheKey, callback=None):
        cacheStatus = QA_EQUIP_ENHANCE_CACHE.get(cacheKey, {}).get('status', CACHE_STATUS_NOT_FOUND)

        if cacheStatus == CACHE_STATUS_FINISHED:
            ret = QA_EQUIP_ENHANCE_CACHE[cacheKey]['data']
            if callback:
                QA_EQUIP_ENHANCE_CACHE[cacheKey]['callbacks'].append(callback)
                self._doCacheCallback(cacheKey)
            del QA_EQUIP_ENHANCE_CACHE[cacheKey]
            return True, cacheStatus, ret, {}
        elif cacheStatus == CACHE_STATUS_RUNNING:
            if callback:
                QA_EQUIP_ENHANCE_CACHE[cacheKey]['callbacks'].append(callback)
            process_info = self._getProcessInfo(cacheKey)
            return False, cacheStatus, '正在执行中，请等待', process_info

        QA_EQUIP_ENHANCE_CACHE[cacheKey] = {
            'data': None,
            'status': CACHE_STATUS_RUNNING,
            'callbacks': [],
            'process_info': {},
        }
        if callback:
            QA_EQUIP_ENHANCE_CACHE[cacheKey]['callbacks'].append(callback)
        self._updateProcessInfo(cacheKey, 0, self.totalTimes)
        return False, cacheStatus, '开始执行，请等待', {}

    def _setCacheResult(self, cacheKey, data):
        QA_EQUIP_ENHANCE_CACHE[cacheKey]['data'] = data
        QA_EQUIP_ENHANCE_CACHE[cacheKey]['status'] = CACHE_STATUS_FINISHED
        self._doCacheCallback(cacheKey)

    def _doCacheCallback(self, cacheKey):
        callbacks = QA_EQUIP_ENHANCE_CACHE[cacheKey]['callbacks']
        data = QA_EQUIP_ENHANCE_CACHE[cacheKey]['data']
        for cb in callbacks:
            cb(data)
        QA_EQUIP_ENHANCE_CACHE[cacheKey]['callbacks'] = []

    def _buildResult(self, equipId, totalEnhanceCount, totalBrokenCount, reachedMaxCount, enhanceCountList, allLevelStats):
        # 达到满级的期望次数（只在成功达到满级的装备上统计）
        avgEnhanceToMax = sum(enhanceCountList) / max(reachedMaxCount, 1)
        brokenRate = totalBrokenCount / max(self.totalTimes, 1)
        minEnhance = min(enhanceCountList) if enhanceCountList else 0
        maxEnhance = max(enhanceCountList) if enhanceCountList else 0

        # 每级统计整理：计算期望次数和概率
        levelSummary = {}
        for lv in sorted(allLevelStats.keys()):
            s = allLevelStats[lv]
            total = s['attempts']
            avgAtt = round(total / max(self.totalTimes, 1), 2)
            levelSummary[lv] = {
                'attempts': total,
                'avgPerEquip': avgAtt,
                'firstEnhanceCount': round(s['firstEnhanceCount'] / max(self.totalTimes, 1), 2),
                'upProb': round(s['up'] / max(total, 1) * 100, 2),
                'failProb': round(s['fail'] / max(total, 1) * 100, 2),
                'downProb': round(s['down'] / max(total, 1) * 100, 2),
                'brokenProb': round(s['broken'] / max(total, 1) * 100, 2),
                'up': s['up'],
                'fail': s['fail'],
                'down': s['down'],
                'broken': s['broken'],
            }

        # 按区间统计分布 (区间宽度自适应)
        dataRange = maxEnhance - minEnhance
        if dataRange <= 1000:
            bucketSize = 50
        elif dataRange <= 5000:
            bucketSize = 200
        else:
            bucketSize = 500
        distribution = {}
        for cnt in enhanceCountList:
            bucket = (cnt // bucketSize) * bucketSize
            label = '{}-{}'.format(bucket, bucket + bucketSize - 1)
            distribution[label] = distribution.get(label, 0) + 1

        return {
            'equipId': equipId,
            'category': 'equipEnhance',
            'totalEquips': self.totalTimes,
            'reachedMax': reachedMaxCount,
            'totalBroken': totalBrokenCount,
            'brokenRate': round(brokenRate * 100, 2),
            'totalEnhance': totalEnhanceCount,
            'avgEnhanceToMax': round(avgEnhanceToMax, 2),
            'minEnhance': minEnhance,
            'maxEnhance': maxEnhance,
            'levelSummary': levelSummary,
            'distribution': distribution,
        }

    def calcEnhanceExpectation(self, equipId, callback=None):
        """
        计算指定装备从0级强化到最大等级的期望次数（timer分批回调）。
        未完成时相同请求返回当前进度，完成时通过callback通知或直接返回结果。

        返回 (isDone, data, process_info)
        """
        cacheKey = self._genCacheKey(equipId)
        ret, cacheStatus, content, process_info = self._getCacheResult(cacheKey, callback)
        if cacheStatus != CACHE_STATUS_NOT_FOUND:
            return ret, content, process_info

        LOG_INFO('EquipEnhanceUnit.calcEnhanceExpectation equipId:', equipId, 'totalTimes:', self.totalTimes)

        totalEnhanceCount = 0
        totalBrokenCount = 0
        reachedMaxCount = 0
        enhanceCountList = []   # 只收录成功达到满级的装备的强化次数（用于分布/期望）
        allLevelStats = {}      # 汇总每级统计
        processed = 0
        current_batch_size = BATCH_TIME_COUNT_INIT

        def process_batch():
            nonlocal totalEnhanceCount, totalBrokenCount, reachedMaxCount, processed, current_batch_size, allLevelStats
            tick_start = time.perf_counter()

            while processed < self.totalTimes:
                remaining = self.totalTimes - processed
                batch_size = min(current_batch_size, remaining)

                batch_start = time.perf_counter()
                batch_count = 0
                for _ in range(batch_size):
                    enhanceCount, reachedMax, isBroken, levelStats = self._enhanceOneEquip(equipId)
                    totalEnhanceCount += enhanceCount
                    if isBroken:
                        totalBrokenCount += 1
                    elif reachedMax:
                        reachedMaxCount += 1
                        enhanceCountList.append(enhanceCount)

                    # 汇总每级统计
                    for lv, stats in levelStats.items():
                        if lv not in allLevelStats:
                            allLevelStats[lv] = {'firstEnhanceCount': 0, 'attempts': 0, 'up': 0, 'fail': 0, 'down': 0, 'broken': 0}
                        for k in ('firstEnhanceCount', 'attempts', 'up', 'fail', 'down', 'broken'):
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

                LOG_DBG("EquipEnhanceUnit: equipId:%s processed:%s/%s batchCount:%s batchElapsed:%.4f batchSize:%s" %
                        (equipId, processed, self.totalTimes, batch_count, batch_elapsed, current_batch_size))

                if time.perf_counter() - tick_start >= TARGET_TICK_S:
                    break

            if processed >= self.totalTimes:
                result = self._buildResult(equipId, totalEnhanceCount, totalBrokenCount, reachedMaxCount, enhanceCountList, allLevelStats)
                LOG_INFO('EquipEnhanceUnit result:', result)
                self._setCacheResult(cacheKey, result)
            else:
                KBEngine.addTimer(1, 0, lambda tid: process_batch())

        process_batch()
        return ret, content, process_info

    def batchCalcEnhanceExpectation(self, equipIds, callback=None):
        """
        批量计算多个装备的强化期望
        """
        results = []

        def make_callback(_equipId, _results):
            def inner_callback(data):
                _results.append(data)
                if len(_results) >= len(equipIds) and callback:
                    callback(_results)
            return inner_callback

        for equipId in equipIds:
            self.calcEnhanceExpectation(equipId, callback=make_callback(equipId, results))
        return results


def doEnhanceTest(equipId, totalTimes=1000, callback=None):
    tester = EquipEnhanceUnit(0, totalTimes)
    return tester.calcEnhanceExpectation(equipId, callback=callback)


def doBatchEnhanceTest(equipIds, totalTimes=1000, callback=None):
    tester = EquipEnhanceUnit(0, totalTimes)
    return tester.batchCalcEnhanceExpectation(equipIds, callback=callback)


'''
# 在KBEngine控制台中使用:
import sys
del sys.modules['server_common.test.enhanceTest']
from server_common.test import enhanceTest

# 单个装备测试（支持 callback）
tester = enhanceTest.EquipEnhanceUnit(0, 10000)
isDone, data, process_info = tester.calcEnhanceExpectation(80114001)

# 带回调
def onDone(data):
    print(data)
tester.calcEnhanceExpectation(80114001, callback=onDone)

# 批量测试
results = tester.batchCalcEnhanceExpectation([50010101, 50010102])
'''
