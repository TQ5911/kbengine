import time

from filecmp import clear_cache
import KBEngine
from KBEDebug import *
import iTimer
import awardContext
import dataUtils
import dropAward
import utils
import json
import gamePlay_gamePlay as GMP
import creep_base as CBD
import creep_coefficient as C_CD
import character_roleData_r_school as SD
import itemData_itemData as ID
import NPC_Pick as NPD
# dropParamDic = {
#     'lv': playerlevel,
#     'srcLevel': context.level or 0,
#     'monsterId': context.monsterId or 0,
#     'school': context.school or 0,
#     'quality': quality or 0,
# }

#KBEngine.addTimer(1, 0, lambda tid: checkGameConfigReady())

QA_DROP_GLOBAL_CACHE = {}

BATCH_SEND_SIZE = 4096  # 4K

# 动态批次大小配置
BATCH_TIME_COUNT_INIT = 1000       # 初始批次大小
BATCH_TIME_COUNT_MIN = 100          # 最小批次大小
BATCH_TIME_COUNT_MAX = 50000        # 最大批次大小
TARGET_TICK_S = 0.2                # 目标每tick耗时（秒），超过则暂停等待下个tick

BATCH_TIME_DUN_COUNT_INIT = 5       # 副本掉落初始批次大小
BATCH_TIME_DUN_COUNT_MIN = 1
BATCH_TIME_DUN_COUNT_MAX = 50

CALCTYPE_DROP_ID = 1  # 掉落id
CALCTYPE_MONSTER_ID = 2 # 怪物id
CALCTYPE_MONSTER_ID = 3 # 宝箱id
CALCTYPE_DUN_NO = 9 # 场景id

CACHE_STATUS_NOT_FOUND = 'not_found'
CACHE_STATUS_RUNNING = 'running'
CACHE_STATUS_FINISHED = 'finished'

class DropUnit():
    def __init__(self, su, totalTimes, *args, **kargs):
        self.su = su
        self.totalTimes = totalTimes
        self.startTime = {}

    def _update_process_info(self, cacheKey, cur, total=None):
        QA_DROP_GLOBAL_CACHE[cacheKey]['process_info']['cur'] = cur
        if total:
            QA_DROP_GLOBAL_CACHE[cacheKey]['process_info']['total'] = total
    
    def _get_process_info(self, cacheKey):
        return QA_DROP_GLOBAL_CACHE[cacheKey]['process_info']


    # 如果后面出现数据量过大被限长的话，还得做分批返回的逻辑
    def _getCacheResult(self, cacheKey, clearCahce=True, callback=None):
        cacheStatus = QA_DROP_GLOBAL_CACHE.get(cacheKey, {}).get('status', CACHE_STATUS_NOT_FOUND)
        
        if cacheStatus == CACHE_STATUS_FINISHED:
            ret = QA_DROP_GLOBAL_CACHE[cacheKey]['data']
            if callback:
                QA_DROP_GLOBAL_CACHE[cacheKey]['callbacks'].append(callback)
                self._doCacheCallback(cacheKey)
            if clearCahce:
                del QA_DROP_GLOBAL_CACHE[cacheKey]
            return True, cacheStatus, ret, {}
        elif cacheStatus == CACHE_STATUS_RUNNING:
            if callback:
                QA_DROP_GLOBAL_CACHE[cacheKey]['callbacks'].append(callback)
            process_info = self._get_process_info(cacheKey)
            return False, cacheStatus, '正在执行中，请等待', process_info   
        self.startTime[cacheKey] = time.perf_counter()
        QA_DROP_GLOBAL_CACHE[cacheKey] = {'data': None, 'status': CACHE_STATUS_RUNNING, 'callbacks': [], 'process_info': {}}
        if callback:
            QA_DROP_GLOBAL_CACHE[cacheKey]['callbacks'].append(callback)
        self._update_process_info(cacheKey, 0, self.totalTimes)
        return False, cacheStatus, '开始执行，请等待', {}
    
    def _setCacheResult(self, cacheKey, data):
        endTime = time.perf_counter()
        LOG_DBG("DropUnit: _setCacheResult cacheKey:%s dataLen:%s costTime:%s" % (cacheKey, len(data), endTime - self.startTime[cacheKey])) 
        QA_DROP_GLOBAL_CACHE[cacheKey]['data'] = data
        QA_DROP_GLOBAL_CACHE[cacheKey]['status'] = CACHE_STATUS_FINISHED
        self._doCacheCallback(cacheKey)

    def _doCacheCallback(self, cacheKey):
        callbacks = QA_DROP_GLOBAL_CACHE[cacheKey]['callbacks']
        data = QA_DROP_GLOBAL_CACHE[cacheKey]['data']
        for cb in callbacks:
            cb(data)
        QA_DROP_GLOBAL_CACHE[cacheKey]['callbacks'] = []
    
    def _genCacheKey(self, awardId, contextVar, totalTimes):
        context_str = "_".join([str(v) for v in sorted(contextVar.values())])
        cacheKey = "%s_%s_%s" % (awardId, context_str, totalTimes)
        return cacheKey

    # 相同的请求进来会被cache机制拦掉，先做一个callback列表，不过还是会导致时间变长，尽量外部维护
    def batchGenAward(self, awardId, contextVar, totalTimes=None, clearCache=True, callback=None):
        totalTimes = totalTimes or self.totalTimes
        cacheKey = self._genCacheKey(awardId, contextVar, totalTimes)
        ret, cacheStatus, content, process_info = self._getCacheResult(cacheKey, clearCache, callback)
        if cacheStatus != CACHE_STATUS_NOT_FOUND:
            return ret, content, process_info
        # 初始化合并结果列表
        allAward = dropAward.AwardVal()
        awardCtx = self._genAwardContext(contextVar)
        processed = 0
        current_batch_size = BATCH_TIME_COUNT_INIT

        def process_batch():
            nonlocal allAward, processed, current_batch_size
            tick_start = time.perf_counter()

            while processed < totalTimes:
                remaining = totalTimes - processed
                batch_size = min(current_batch_size, remaining)

                batch_start = time.perf_counter()
                allAward += dropAward.getAward(awardId, batch_size, awardCtx, False)
                batch_elapsed = time.perf_counter() - batch_start

                processed += batch_size
                self._update_process_info(cacheKey, processed)

                # 根据上次批次耗时动态调整批次大小
                if batch_elapsed > TARGET_TICK_S * 2:
                    current_batch_size = max(BATCH_TIME_COUNT_MIN, current_batch_size // 2)
                elif batch_elapsed < TARGET_TICK_S * 0.5:
                    current_batch_size = min(BATCH_TIME_COUNT_MAX, current_batch_size * 2)

                LOG_DBG("DropUnit: batchGenAward rewardId:%s totalTimes:%s processed:%s batchSize:%s batchElapsed:%.4f" %
                        (awardId, totalTimes, processed, batch_size, batch_elapsed))

                # 如果当前tick已消耗超过目标时间，暂停等待下个tick
                if time.perf_counter() - tick_start >= TARGET_TICK_S:
                    break

            if processed >= totalTimes:
                dropData = self.updateItemInfoByDropList(allAward.toBriefList(), totalTimes)
                if not self.su:
                    self.writeToJsonFile(dropData)
                else:
                    # 可能执行时间过长断掉连接，放缓存里
                    self._setCacheResult(cacheKey, dropData)
            else:
                KBEngine.addTimer(1, 0, lambda tid: process_batch())

        # 启动处理
        process_batch()
        return ret, content, process_info


    def _genAwardContext(self, contextVar):
        awardCtx = awardContext.CommonContext(0, {'lv': contextVar.get('playerLevel', 0)})
        awardCtx.addContextVar('awardId', contextVar.get('awardId', 0))
        awardCtx.addContextVar('school', contextVar.get('school', 0))
        awardCtx.args.addArg('avatarLv', contextVar.get('playerLevel', 0))
        awardCtx.args.addArg('avatarSex', contextVar.get('sex', 0))
        awardCtx.addContextVar('isMonthCardExpired', contextVar.get('isMonthCardExpired', False))
        awardCtx.addContextVar('isBigMonthCardExpired', contextVar.get('isBigMonthCardExpired', False))
        awardCtx.addContextVar('avatarScoreRank', contextVar.get('avatarScoreRank', 0))
        awardCtx.addContextVar('isCrossServer', contextVar.get('isCrossServer', False))

        return awardCtx

    # toBriefList 里每个实例会占用一行，还是得统计一下
    def updateItemInfoByDropList(self, dropList, totalTimes):
        itemCount = {}
        itemInfoList = []
        for itemInfo in dropList:
            itemId = itemInfo.get('itemId')
            bindType = itemInfo.get('bindType', 0)
            itemCount[(itemId, bindType)] = itemCount.get((itemId, bindType), 0) + itemInfo.get('itemNum', 0)
        for (itemId, bindType), itemNum in itemCount.items():
            itemInfo = {}
            itemData = dataUtils.getEquipItemData(itemId)
            if not itemData:
                itemData = dataUtils.getCommItemData(itemId)
            if not itemData:
                itemData = {}
            itemInfo['quality'] = itemData.get('quality', 0)
            itemInfo['name'] = itemData.get('name', '')
            itemInfo['itemId'] = itemId
            itemInfo['bindType'] = bindType
            itemInfo['itemNum'] = itemNum
            itemInfo['onceDrop'] = itemNum * 1.0 / totalTimes  # 这里其实是单次掉落数量，和概率不一样
            itemInfoList.append(itemInfo)
        return itemInfoList


    def getDunDrop(self, dunNo, num=1000):
        cacheKey = "%s_%s" % (dunNo, num)
        ret, cacheStatus, content, process_info = self._getCacheResult(cacheKey)
        if cacheStatus != CACHE_STATUS_NOT_FOUND:
            return ret, content, process_info
        
        output = {}
        mapData = GMP.datas.get(dunNo)
        dunData = utils.getDunModuleData(dunNo)
        dunName = mapData.get('name', '')
        dunStr = f"{dunName}({dunNo})"
        outputByDun = {dunStr: []}
        # 预先收集所有掉落相关参数
        count_data_list = []
        count_data_filter = []
        for spawnId, spawnData in dunData.items():
            ClassName = spawnData.get('ClassName', '')
            EntityID = spawnData.get('EntityID', 0)
            Name = spawnData.get('DisplayName', '')
            props = spawnData.get('Props', {})
            
            goCount = False
            rewardIDs = []
            Level = 0
            if ClassName == 'Monster':
                Level = props.get('Level', 0)
                rewardIDs = dataUtils.getMonsterRewardIds(EntityID, Level)
                Name = Name or CBD.datas.get(EntityID, {}).get('name', '')
                goCount = True
            elif ClassName == 'Collection':
                rewardID = NPD.datas.get(EntityID, {}).get('rewardID', 0)
                Name = Name or NPD.datas.get(EntityID, {}).get('name', '')
                rewardIDs = [rewardID]
                goCount = True
            entityName = f"{Name}({EntityID})"
            if goCount:
                outputByDun[dunStr].append({
                    'className': ClassName,
                    'spawnId': spawnId,
                    'entityName': entityName,
                    'entityID': EntityID,
                    'level': Level
                })
                if (ClassName, EntityID, Level) not in count_data_filter:
                    count_data_filter.append((ClassName, EntityID, Level))
                    for school in SD.datas:
                        for rewardId in rewardIDs:
                            count_data_list.append({
                                'rewardId': rewardId,
                                'school': school,
                                'Level': Level,
                                'EntityID': EntityID,
                                'ClassName': ClassName
                            })
            
        def callback(output, _outputByDun=outputByDun, _cacheKey=cacheKey):
            LOG_DBG(f"DropUnit: getDunDrop done dunNo:{dunNo} num:{num} outputByDunLen:{len(outputByDun)} count_data_list:{len(count_data_list)}")
            # 为了避免回传超长，这里分开传，在前端拼
            all_data = {
                'dropData': output,
                'dunData': outputByDun,
            }
            
            if self.su:
                self._setCacheResult(_cacheKey, all_data)
                self.writeToJsonFile(all_data)
            else:
                self.writeToJsonFile(all_data)

        # 存储分批处理所需数据
        self._batch_dun_data = {
            'count_data_list': count_data_list,
            'current_index': 0,
            'output': output,
            'num': num,
            'callback': callback,
            'batch_size': BATCH_TIME_DUN_COUNT_INIT,
        }
        self._update_process_info(cacheKey, 0, len(count_data_list))
        # 启动第一批处理
        self._batch_getDunDrop(0, _cacheKey=cacheKey)
        return ret, content, process_info

    def _batch_getDunDrop(self, tid, _cacheKey=None):
        """
        分批处理 getDunDrop 的逻辑，直接调用 batchGenAward
        动态调整每批次调度数量，根据 tick 耗时自适应
        """
        process_data = self._batch_dun_data
        count_data_list = process_data['count_data_list']
        total_count = len(count_data_list)
        current_index = process_data['current_index']
        batch_size = process_data['batch_size']
        end_index = min(current_index + batch_size, total_count)
        # 提前推进索引，避免同步回调触发时索引未更新导致重复处理
        process_data['current_index'] = end_index

        self._update_process_info(_cacheKey, current_index)

        # 本批次待回调数量
        pending_count = end_index - current_index
        tick_start = time.perf_counter()

        def on_one_done():
            nonlocal pending_count
            pending_count -= 1
            if pending_count <= 0:
                _finish_batch()

        def _finish_batch():
            nonlocal batch_size
            tick_elapsed = time.perf_counter() - tick_start
            # 根据本批次总耗时动态调整下一批的批次大小
            if tick_elapsed > TARGET_TICK_S * 2:
                process_data['batch_size'] = max(BATCH_TIME_DUN_COUNT_MIN, batch_size // 2)
            elif tick_elapsed < TARGET_TICK_S * 0.5:
                process_data['batch_size'] = min(BATCH_TIME_DUN_COUNT_MAX, batch_size * 2)

            if process_data['current_index'] >= total_count:
                if process_data['callback']:
                    process_data['callback'](process_data['output'])
            else:
                KBEngine.addTimer(1, 0, lambda t, k=_cacheKey: self._batch_getDunDrop(t, k))

        def make_inner_callback(_rewardId, _ClassName, _EntityID, _Level, _school, _output):
            def inner_callback(dropData):
                cls_dict = _output.setdefault(_ClassName, {})
                ent_dict = cls_dict.setdefault(_EntityID, {})
                lvl_dict = ent_dict.setdefault(_Level, {})
                sch_dict = lvl_dict.setdefault(_school, {'drop': {}})
                sch_dict['drop'][_rewardId] = dropData
                on_one_done()
            return inner_callback

        for i in range(current_index, end_index):
            count_data = count_data_list[i]
            cb = make_inner_callback(
                count_data['rewardId'], count_data['ClassName'],
                count_data['EntityID'], count_data['Level'],
                count_data['school'], process_data['output']
            )
            self.batchGenAward(count_data['rewardId'],
                               {"awardId": count_data['rewardId'], "level": count_data['Level'],
                                "school": count_data['school'], "sex": 0},
                               process_data['num'], clearCache=False, callback=cb)
        
        

    def writeToJsonFile(self, data):
        file_path = '/mnt/hgfs/game/Server/kbeLinux/kbengine/assets/output.json'
        LOG_INFO(f"DropUnit: writeToJsonFile {file_path}")
        # 先判断一下目录是否存在，不存在就不写入了
        import os
        if not os.path.exists(os.path.dirname(file_path)):
            return
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data))


def doTest():
    dropUnit = DropUnit(None, 10000)
    dropUnit.batchGenAward(40020261, {'awardId': 40020261, 'playerLevel': 1, 'school': 1003, 'sex': 0})
    LOG_INFO("DropUnit: doTest")


'''
import sys
del sys.modules['test']
from test import dropTest
a = dropTest.DropUnit(None, 10000)
a.batchGenAward(40020261, 1, 1003, 0)
'''
