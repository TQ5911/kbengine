# coding: utf-8
"""新手历程系统 - 行为累积统计 (FIXED_DICT 持久化)
==================================================================
按 taskID 存储累积计数: {taskID: count}

taskType 1-7, 11, 19 (累积型) -> 业务模块 hook 时 +N
taskType 8-10, 12-18 (属性查询型) -> 持久化字段不被使用,客户端请求领取时实时查 Avatar 属性
"""
import userType


class BeginnerJourneyBehaviorStatsVal(userType.UserSingleType):
    '''BEGINNER_JOURNEY_BEHAVIOR_STATS'''

    def __init__(self, stats=None):
        # taskID -> int (累积计数)
        self.stats = dict(stats or {})

    # -------- 持久化 --------

    def toStreamSavedDic(self):
        return {'stats': dict(self.stats)}

    # -------- 业务接口 --------

    def add(self, taskID, delta=1):
        """累加 taskID 对应的计数"""
        if not taskID or delta == 0:
            return
        self.stats[taskID] = self.stats.get(taskID, 0) + delta

    def get(self, taskID):
        """读取 taskID 当前累积数 (默认 0)"""
        return self.stats.get(taskID, 0) if taskID else 0

    def setVal(self, taskID, value):
        """直接设置 taskID 数值"""
        if taskID:
            self.stats[taskID] = max(0, int(value))

    def keys(self):
        return list(self.stats.keys())


class BeginnerJourneyBehaviorStatsInfo(object):
    """注册到 types.xml 的 implementedBy 对象 (ABCInfo 子类)"""

    def createObjFromDict(self, dataDict):
        obj = BeginnerJourneyBehaviorStatsVal()
        obj.stats = dict(dataDict.get('stats', {}) or {})
        return obj

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()

    def isSameType(self, obj):
        return type(obj) is BeginnerJourneyBehaviorStatsVal


BeginnerJourneyBehaviorStatsInstance = BeginnerJourneyBehaviorStatsInfo()