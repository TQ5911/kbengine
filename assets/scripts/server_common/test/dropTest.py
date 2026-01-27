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

BATCH_TIME_COUNT = 10000
BATCH_TIME_DUN_COUNT = 1

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
        self.startTime[cacheKey] = utils.getNow()
        QA_DROP_GLOBAL_CACHE[cacheKey] = {'data': None, 'status': CACHE_STATUS_RUNNING, 'callbacks': [], 'process_info': {}}
        if callback:
            QA_DROP_GLOBAL_CACHE[cacheKey]['callbacks'].append(callback)
        self._update_process_info(cacheKey, 0, self.totalTimes)
        return False, cacheStatus, '开始执行，请等待', {}
    
    def _setCacheResult(self, cacheKey, data):
        endTime = utils.getNow()
        DEBUG_MSG("DropUnit: _setCacheResult cacheKey:%s dataLen:%s costTime:%s" % (cacheKey, len(data), endTime - self.startTime[cacheKey])) 
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
        leftTimes = totalTimes
        cacheKey = self._genCacheKey(awardId, contextVar, totalTimes)
        ret, cacheStatus, content, process_info = self._getCacheResult(cacheKey, clearCache, callback)
        if cacheStatus != CACHE_STATUS_NOT_FOUND:
            return ret, content, process_info
        # 初始化合并结果列表
        allAward = dropAward.AwardVal()
        awardCtx = self._genAwardContext(contextVar)
        # 定义回调函数，用于分批调用 getAward
        def batch_callback(tid):
            nonlocal allAward, leftTimes
            genNum = 0
            if leftTimes > BATCH_TIME_COUNT:
                leftTimes -= BATCH_TIME_COUNT
                genNum = BATCH_TIME_COUNT
            else:
                genNum = leftTimes
                leftTimes = 0
            INFO_MSG("DropUnit: batchGenAward rewardId:%s totalTimes:%s leftTimes:%s genNum:%s" % (awardId, self.totalTimes, leftTimes, genNum))  
            self._update_process_info(cacheKey, genNum)
            if genNum > 0:
                # 调用 getAward 并将结果添加到合并列表中
                allAward += dropAward.getAward(awardId, genNum, awardCtx, False)
                KBEngine.addTimer(1, 0, batch_callback)
            else:
                # 所有批次执行完毕，调用 writeToJsonFile 写入结果
                dropData = self.updateItemInfoByDropList(allAward.toBriefList(), totalTimes)
                if not self.su:
                    self.writeToJsonFile(dropData)
                else:
                    # 可能执行时间过长断掉连接，放缓存里
                    self._setCacheResult(cacheKey, dropData)
        # 启动第一次回调
        batch_callback(0)
        return ret, content, process_info


    def _genAwardContext(self, contextVar):
        awardCtx = awardContext.CommonContext(0, {'lv': contextVar.get('playerLevel', 0)})
        awardCtx.addContextVar('awardId', contextVar.get('awardId', 0))
        awardCtx.addContextVar('school', contextVar.get('school', 0))
        awardCtx.args.addArg('avatarLv', contextVar.get('playerLevel', 0))
        awardCtx.args.addArg('avatarSex', contextVar.get('sex', 0))
        awardCtx.addContextVar('isMonthCardExpired', contextVar.get('isMonthCardExpired', False))
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
                rewardIDs = CBD.datas.get(EntityID, {}).get('rewardID', ())
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
            DEBUG_MSG(f"DropUnit: getDunDrop done dunNo:{dunNo} num:{num} outputByDunLen:{len(outputByDun)} count_data_list:{len(count_data_list)}")
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
            'callback': callback
        }
        self._update_process_info(cacheKey, 0, len(count_data_list))
        # 启动第一批处理
        self._batch_getDunDrop(0, _cacheKey=cacheKey)
        return ret, content, process_info

    def _batch_getDunDrop(self, tid, _cacheKey=None):
        """
        分批处理 getDunDrop 的逻辑，直接调用 batchGenAward
        """
        process_data = self._batch_dun_data
        current_index = process_data.get('current_index', 0)
        batch_size = BATCH_TIME_DUN_COUNT
        end_index = current_index + batch_size
        count_data_list = process_data['count_data_list']
        
        self._update_process_info(_cacheKey, current_index)

        # 用于记录待完成的回调数量
        self._pending_callbacks = 0

        for i in range(current_index, min(end_index, len(count_data_list))):
            count_data = count_data_list[i]
            rewardId = count_data['rewardId']
            school = count_data['school']
            Level = count_data['Level']
            EntityID = count_data['EntityID']
            ClassName = count_data['ClassName']

            self._pending_callbacks += 1
            def inner_callback(dropData, _rewardId=rewardId, _ClassName=ClassName, _EntityID=EntityID, 
                            _Level=Level, _school=school, _output=process_data['output']):
                if _output.get(_ClassName, {}).get(_EntityID, {}).get(_Level, {}).get(_school, {}):
                    _output[_ClassName][_EntityID][_Level][_school]['drop'][_rewardId] = dropData
                else:
                    if _ClassName not in _output:
                        _output[_ClassName] = {}
                    if _EntityID not in _output[_ClassName]:
                        _output[_ClassName][_EntityID] = {}
                    if _Level not in _output[_ClassName][_EntityID]:
                        _output[_ClassName][_EntityID][_Level] = {}
                    if _school not in _output[_ClassName][_EntityID][_Level]:
                        _output[_ClassName][_EntityID][_Level][_school] = {
                            'drop': {_rewardId: dropData}
                        }
                self._pending_callbacks -= 1
                # 检查是否所有回调都已完成
                if self._pending_callbacks == 0 and process_data['current_index'] >= len(count_data_list):
                    if process_data['callback']:
                        process_data['callback'](process_data['output'])

            # 直接调用 batchGenAward, 不清理缓存

            self.batchGenAward(rewardId, {"awardId": rewardId, "level": Level, "school": school, "sex": 0}, process_data['num'], clearCache=False, callback=inner_callback)

        process_data['current_index'] = end_index
        if end_index < len(count_data_list):
            KBEngine.addTimer(1, 0, lambda tid, _cacheKey=_cacheKey: self._batch_getDunDrop(tid, _cacheKey))
        elif self._pending_callbacks == 0:
            if process_data['callback']:
                process_data['callback'](process_data['output'])
        
        

    def writeToJsonFile(self, data):
        file_path = '/mnt/hgfs/game/Server/kbeLinux/kbengine/assets/output.json'
        INFO_MSG(f"DropUnit: writeToJsonFile {file_path}")
        # 先判断一下目录是否存在，不存在就不写入了
        import os
        if not os.path.exists(os.path.dirname(file_path)):
            return
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data))


def doTest():
    dropUnit = DropUnit(None, 10000)
    dropUnit.batchGenAward(40020261, {'awardId': 40020261, 'playerLevel': 1, 'school': 1003, 'sex': 0})
    INFO_MSG("DropUnit: doTest")


'''
import sys
del sys.modules['test']
from test import dropTest
a = dropTest.DropUnit(None, 10000)
a.batchGenAward(40020261, 1, 1003, 0)
'''