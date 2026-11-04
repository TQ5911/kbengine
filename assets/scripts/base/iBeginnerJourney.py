# -*- coding: utf-8 -*-
"""
新手历程系统 (iBeginnerJourney) v5 (2026-09-24)
==================================================================
v5 变更: 19 种 taskType 全部统一为目标值累积型.
  - 旧 v4 区分累积型 (1-7,19) + 属性查询型 (8-18)
  - 新 v5: 全部 taskType 都通过 emit 累积, 跨过 targetNum 即视为完成
  - 删除了 11 个 _countActivatedPets 等属性查询占位方法
  - 删除了 _isAttributeTypeTaskSatisfied
  - 删除了 takeBeginnerJourneyTaskReward 中的"领取时实时查属性"分支

按配置:
- beginnerJourney_levelPhase: 阶段配置 (phaseRewardNum / rewardID / unlockID)
    phaseRewardNum: 阶段下完成 N 个任务即可领 phase 奖励 (不要求全部完成)
- beginnerJourney_phaseTask: 阶段下子任务,字段:
    taskID / type(阶段ID) / taskType(0=旧 taskID 路径, 1-19=新数据触发系统) /
    taskDescription / ifCountedBeforeUnlock / rewardID / taskParam
- visible_visible: 阶段解锁条件 (level / task / day)
- 运行时参数: BJ_PT.taskIdWithTaskParams[taskID] = [targetNum, param2, param3_list, param4_list]

19 种 taskType 的 emit 触发约定 (见 docs/beginner-journey-task-type-schema.md):
  1=道具变化  2=完成任务数  3=地区探索度  4=击杀怪物  5=通关讨伐
  6=门票  7=采集  8=激活精灵  9=精灵穿戴遗器  10=精灵等级
  11=经脉  12=装备强化  13=装备等阶  14=武器祝福  15=武器铭文
  16=附灵评分  17=魂魄评分  18=技能等级  19=矿战积分

完成判定 (统一):
  - taskType=0 (旧): impTask._afterTaskSubmitted hook -> finishedTaskIds
  - taskType 1-19 (新): 业务模块 emit -> beginnerJourneyBehaviorStats[+N]
    -> 跨过 targetNum 即视为完成 -> 推 client.onBeginnerJourneyTaskFinished
    -> 客户端调 takeBeginnerJourneyTaskReward 领取 rewardID
  - 阶段可领奖: 该 phaseId 下 finishedTaskIds 数 >= phaseRewardNum
    -> 客户端调 takeBeginnerJourneyPhaseReward 领 phase 奖励

业务模块统一 emit 接口 (在 hook 处调用, 唯一入口):
  self.beginnerJourney_onTaskEvent(
      gameconst.BjTaskType.BJ_TASK_TYPE_ITEM_COST,
      delta=5, itemId=xxx, srcType=0)   # delta 必填, 放第 1 位
  ... 各 taskType 对应字段见 beginnerJourneyTaskType.EVENT_SCHEMAS

具体判定逻辑 (19 个 match_accumulate_*) 全部委托到独立模块
  base/beginnerJourneyTaskType.py, 本文件只负责调度+持久化+领取+GM.
"""
from KBEDebug import *

import KBEngine
import gamedecorator
import gameconst
import dropAward
import gameconfig
import LogTrackingMgr

import beginnerJourney_config as BJ_C
import beginnerJourney_levelPhase as BJ_LP
import beginnerJourney_phaseTask as BJ_PT
import message_Message_def as M_M_DD
import itemData_itemData as IDID
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD

import beginnerJourneyTaskType

# taskType 常量见 server_common/gameconst.py:BjTaskType


class IBeginnerJourney(object):
    """
    新手历程基础 mixin. 由 Avatar 继承.

    持久化属性 (iBeginnerJourney.def):
    - beginnerJourneyFinishedTasks        ARRAY<UINT32> 已完成的子任务 taskID
    - beginnerJourneyClaimedTaskRewards    ARRAY<UINT32> 已领取的子任务奖励
    - beginnerJourneyClaimedPhaseRewards   ARRAY<UINT32> 已领取的阶段奖励 phaseID
    - beginnerJourneyClosed                UINT8 系统关闭标志
    - beginnerJourneyBehaviorStats         BEGINNER_JOURNEY_BEHAVIOR_STATS (FIXED_DICT) {taskID: count}
    """
    
    def clearBeginnerJourneyBehaviorStatusEx(self, taskTypes):
        taskIds = self.beginnerJourneyBehaviorStats.keys()
        for taskId in taskIds:
            if taskId in self.beginnerJourneyFinishedTasks:
                continue
            cfg = BJ_PT.datas.get(taskId)
            if not cfg:
                continue
            if cfg['taskType'] in taskTypes:
                self.beginnerJourneyBehaviorStats.setVal(taskId, 0)
                self._pushBeginnerJourneyTaskUpdate(taskId)
    # ============== 通用累积 (累积型 taskType 1-19 共用) ==============

    def _isTaskCountable(self, cfg):
        """任务是否在当前可累积状态: 系统未关闭 + (阶段已解锁 OR ifCountedBeforeUnlock=1)"""
        if self.beginnerJourneyClosed:
            return False
        # ifCountedBeforeUnlock=1: 阶段未解锁也可累积
        # ifCountedBeforeUnlock=0: 必须 checkPhaseOpenned 通过才累积
        if not cfg.get('ifCountedBeforeUnlock', 0):
            if not self.checkPhaseOpenned(cfg['taskID']):
                return False
        return True

    def _accumulate(self, taskId, delta):
        """
        累积 +delta 到 beginnerJourneyBehaviorStats.
        若之前未达到, 现在跨过 targetNum -> 加入 finishedTaskIds + 推 client.
        """
        cfg = BJ_PT.datas.get(taskId)
        if not cfg:
            return
        params = BJ_PT.taskIdWithTaskParams.get(taskId)
        if not params:
            return
        targetNum = params[0]
        if targetNum <= 0:
            return
        cur = self.beginnerJourneyBehaviorStats.get(taskId)
        if cur >= targetNum:
            return  # 已达目标, 不再累积

        newVal = cur + max(0, int(delta))
        if newVal > targetNum:
            newVal = targetNum
        self.beginnerJourneyBehaviorStats.setVal(taskId, newVal)
        LOG_DBG('_accumulate', self.gbID, 'taskId=', taskId, 'cur=', newVal, '/', targetNum)
        # 单任务进度更新推送 (每次累积都发, 含未达阈值)
        self._pushBeginnerJourneyTaskUpdate(taskId)

        if newVal >= targetNum:
            # 跨过阈值 -> 标记完成
            if taskId not in self.beginnerJourneyFinishedTasks:
                LOG_INFO('task finished (累积)', self.gbID, taskId, 'type=', cfg.get('type'), 'taskType=', cfg.get('taskType'))
                self.beginnerJourneyFinishedTasks.append(taskId)
                isPhaseFinished = False
                phaseTaskFinishedCount = 0
                phaseTaskIds = BJ_PT.phaseWithTaskIds.get(cfg.get('type'), None)
                if phaseTaskIds:
                    for phaseTaskId in phaseTaskIds:
                        if phaseTaskId in self.beginnerJourneyFinishedTasks:
                            phaseTaskFinishedCount += 1
                    if len(phaseTaskIds) == phaseTaskFinishedCount:
                        isPhaseFinished = True

                LogTrackingMgr.LogTrackingMgr.Beginner_Journey_Task_Finish(
                    self.gbID, 
                    self.accountEntity.clientDistinctId,
                    gameconfig.serverId(),
                    gameconfig.gameId(),
                    cfg.get('type'),
                    taskId,
                    gameconst.BeginnerJourneyTaskFinishType.PHASE if isPhaseFinished else gameconst.BeginnerJourneyTaskFinishType.TASK,
                    phaseTaskFinishedCount,
                    len(self.beginnerJourneyFinishedTasks),
                    self.getRoleCacheAttr('level')
                )

                self.client.onBeginnerJourneyTaskFinished(taskId)
    # ============== 任务完成 hook (旧路径, taskType=0) ==============

    def onTaskFinishedForBeginnerJourney(self, taskId):
        """
        impTask._afterTaskSubmitted 任务完成时回调.
        只处理 taskType=0 的旧路径; 新路径 (1-19) 由 emit 函数累积.
        """
        if not taskId:
            return
        cfg = BJ_PT.datas.get(taskId)
        if not cfg:
            return
        taskType = cfg.get('taskType', 0)
        if taskType != gameconst.BjTaskType.BJ_TASK_TYPE_NONE:
            # 新路径不通过这里, 由 emit 函数累积后自动标完成
            return
        LOG_INFO('onTaskFinishedForBeginnerJourney (taskType=0):', self.gbID, taskId)

        if self.beginnerJourneyClosed:
            return
        if taskId in self.beginnerJourneyFinishedTasks:
            return
        # ifCountedBeforeUnlock=1: 阶段未解锁也允许计入; 否则必须解锁
        if not cfg.get('ifCountedBeforeUnlock', 0):
            if not self.checkPhaseOpenned(taskId):
                return
        self.beginnerJourneyFinishedTasks.append(taskId)
        self.client.onBeginnerJourneyTaskFinished(taskId)
        # 同步推一次单任务更新 (taskType=0 路径无累积进度)
        self._pushBeginnerJourneyTaskUpdate(taskId)

    def onBeginnerJourneyLogin(self):
        if self.beginnerJourneyClosed:
            return
        self._pushBeginnerJourneyRecordToClient()

    # ============== 检查阶段是否已解锁 (visible 依赖) ==============

    def checkPhaseOpenned(self, taskId):
        """阶段是否解锁: visible 表中 unlockID 对应 UI 已可见"""
        phaseTaskData = BJ_PT.datas.get(taskId)
        if not phaseTaskData:
            return False
        phaseId = phaseTaskData['type']
        levelPhaseData = BJ_LP.datas.get(phaseId)
        if not levelPhaseData:
            return False
        return self._isUIVisibleStr(levelPhaseData['unlockID'])

    # ============== 客户端领取接口 ==============

    @gamedecorator.checkGameconfigEnable('beginnerJourneyTask')
    def takeBeginnerJourneyTaskReward(self, exposed, taskId):
        """
        客户端领取某个子任务的 rewardID 奖励.
        v5: 所有 taskType 都是累积型, 仅当 finishedTaskIds 已包含 taskId 时可领.
        """
        if not taskId:
            return
        if self.beginnerJourneyClosed:
            return
        if taskId in self.beginnerJourneyClaimedTaskRewards:
            return
        # 累积型: 必须已 finished (业务 emit 跨过阈值时已 push)
        if taskId not in self.beginnerJourneyFinishedTasks:
            return
        cfg = BJ_PT.datas.get(taskId)
        if not cfg:
            return
        taskType = cfg.get('taskType', 0)
        rewardId = cfg.get('rewardID', 0)
        if not rewardId:
            return
        srcType = AAC_AACDD.datas.BONUS_SRC_BEGINNER_JOURNEY_TASK_REWARD
        ctx = self.getAvatarAwardCtx(rewardId, None)
        wealthVal = dropAward.getAward(rewardId, 1, ctx)
        if not self.canAddWealthVal(srcType, wealthVal, ctx):
            self.onMessagePre(BJ_C.datas['beginnerJourney_claimFailed']['value'], [])
            return
        self.beginnerJourneyClaimedTaskRewards.append(taskId)
        opUUID = KBEngine.genUUID64()
        self.addWealth(srcType, wealthVal, opUUID, None, ctx)
        self.client.onBeginnerJourneyTaskReward(taskId)
        LOG_INFO('takeBeginnerJourneyTaskReward ok', self.gbID, taskId, 'taskType=', taskType)

    @gamedecorator.checkGameconfigEnable('beginnerJourneyTask')
    def takeBeginnerJourneyPhaseReward(self, exposed, phaseId):
        """客户端领取某个阶段完成时的 rewardID 奖励"""
        if not phaseId:
            return
        if self.beginnerJourneyClosed:
            return
        if phaseId in self.beginnerJourneyClaimedPhaseRewards:
            return
        phaseCfg = BJ_LP.datas.get(phaseId)
        if not phaseCfg:
            return
        if not self._isBeginnerJourneyPhaseCompleted(phaseId):
            return
        rewardId = phaseCfg.get('rewardID', 0)
        if not rewardId:
            return
        srcType = AAC_AACDD.datas.BONUS_SRC_BEGINNER_JOURNEY_PHASE_REWARD
        ctx = self.getAvatarAwardCtx(rewardId, None)
        wealthVal = dropAward.getAward(rewardId, 1, ctx)
        if not self.canAddWealthVal(srcType, wealthVal, ctx):
            self.onMessagePre(BJ_C.datas['beginnerJourney_claimFailed']['value'], [])
            return
        self.beginnerJourneyClaimedPhaseRewards.append(phaseId)
        opUUID = KBEngine.genUUID64()
        self.addWealth(srcType, wealthVal, opUUID, None, ctx)
        self.client.onBeginnerJourneyPhaseReward(phaseId)

    @gamedecorator.checkGameconfigEnable('beginnerJourneyTask')
    def takeBeginnerJourneySpecialReward(self, exposed):
        if self.beginnerJourneySpecialRewardFinished:
            return
        if not self._isBeginnerJourneySpecialPhaseCompleted():
            return
        rewardItemId = BJ_C.datas['specialReward_itemID']['value']
        if rewardItemId not in IDID.datas:
            return
        srcType = AAC_AACDD.datas.BONUS_SRC_BEGINNER_JOURNEY_SPECIAL_REWARD
        ctx = self.getAvatarAwardCtx(0, None)
        wealthVal = dropAward.AwardVal()
        wealthVal.addWealthByItemId(rewardItemId, 1)
        if not self.canAddWealthVal(srcType, wealthVal, ctx):
            self.onMessagePre(BJ_C.datas['beginnerJourney_claimFailed']['value'], [])
            return
        self.beginnerJourneySpecialRewardFinished = True
        opUUID = KBEngine.genUUID64()
        self.addWealth(srcType, wealthVal, opUUID, None, ctx)

    # ============== 每日重置 (关闭系统) ==============

    def _dailyCloseBeginnerJourney(self, *args):
        """每日凌晨: 全部 phase 完成+奖励领取 -> 关闭"""
        if self.beginnerJourneyClosed:
            return
        if not self._isAllBeginnerJourneyPhaseRewardClaimed():
            return
        self.beginnerJourneyClosed = 1
        LOG_INFO('_dailyCloseBeginnerJourney: closed', self.gbID)

    # ============== 内部工具 ==============

    def _isBeginnerJourneyPhaseCompleted(self, phaseId):
        """phase 可领奖判定: 该 phaseId 下已完成任务数 >= phaseRewardNum 即可.

        数据约定 (beginnerJourney_levelPhase.phaseRewardNum):
            - phaseRewardNum=0: 无条件可领 (策划配置为 0 的特例)
            - phaseRewardNum>0: 必须 finished taskID 数 >= phaseRewardNum
        """
        phaseCfg = BJ_LP.datas.get(phaseId)
        if not phaseCfg:
            return False
        rewardNum = phaseCfg.get('phaseRewardNum', 0)
        if rewardNum <= 0:
            return False
        taskIds = BJ_PT.phaseWithTaskIds.get(phaseId) or []
        finished = sum(1 for tid in taskIds if tid in self.beginnerJourneyFinishedTasks)
        return finished >= rewardNum
    
    def _isBeginnerJourneySpecialPhaseCompleted(self):
        datas = BJ_C.datas['specialReward_unlockCondition']['value']
        if len(datas) != 2:
            return False
        targetNum = datas[1]
        if targetNum <= 0:
            return False
        phaseId = datas[0]
        phaseCfg = BJ_LP.datas.get(phaseId)
        if not phaseCfg:
            return False
        taskIds = BJ_PT.phaseWithTaskIds.get(phaseId) or []
        finished = sum(1 for tid in taskIds if tid in self.beginnerJourneyFinishedTasks)
        return finished >= targetNum

    def _isAllBeginnerJourneyPhaseRewardClaimed(self):
        for phaseId in BJ_LP.datas:
            if phaseId not in self.beginnerJourneyClaimedPhaseRewards:
                return False
        return True

    def _pushBeginnerJourneyRecordToClient(self):
        """
        登录时全量推送:
          - 3 个状态数组: finishedTasks / claimedTaskRewards / claimedPhaseRewards
          - 4 个进度数组 (索引对齐): taskIds / cur / targetNum / isFinished
        """
        taskIds = []
        curVals = []
        targetVals = []
        for tid in BJ_PT.datas:
            params = BJ_PT.taskIdWithTaskParams.get(tid)
            if not params:
                continue
            taskIds.append(tid)
            curVals.append(self.beginnerJourneyBehaviorStats.get(tid))
            targetVals.append(params[0])
        self.client.onBeginnerJourneyTaskRecord(
            list(self.beginnerJourneyFinishedTasks),
            list(self.beginnerJourneyClaimedTaskRewards),
            list(self.beginnerJourneyClaimedPhaseRewards),
            taskIds, curVals, targetVals
        )

    def _pushBeginnerJourneyTaskUpdate(self, taskId):
        """
        单任务进度更新推送 (每次累积/GMTaskType=0 完成时调用).
        协议: onBeginnerJourneyTaskUpdate(taskId, cur, targetNum, isFinished)
        """
        params = BJ_PT.taskIdWithTaskParams.get(taskId)
        if not params:
            return
        cur = self.beginnerJourneyBehaviorStats.get(taskId)
        targetNum = params[0]
        if cur > targetNum:
            cur = targetNum
        self.client.onBeginnerJourneyTaskUpdate(taskId, cur, targetNum)
    
    def beginnerJourneyOnTaskEvents(self, datas):
        LOG_DBG('beginnerJourneyOnTaskEvents: ', datas)
        for data in datas:
            taskType = data[0]
            args = data[1]
            self.beginnerJourney_onTaskEvent(taskType, **args)
    # =============================================================
    # 19 种 taskType 的统一 emit 接口 (业务模块 hook 处调用)
    # -------------------------------------------------------------
    # 不再为每个 taskType 暴露一个独立方法; 全部走这一个入口.
    # 业务模块调用示例:
    #   self.beginnerJourney_onTaskEvent(
    #       gameconst.BjTaskType.BJ_TASK_TYPE_ITEM_COST,
    #       delta=5, itemId=xxx, srcType=0)   # delta 必填, 放第 1 位
    #
    # taskType 1-19 (全部): 累积型, 委托到 beginnerJourneyTaskType.dispatch_event
    # =============================================================

    def beginnerJourney_onTaskEvent(self, taskType, **params):
        LOG_DBG('beginnerJourney_onTaskEvent: ', taskType, params)
        """
        统一 emit 入口. 业务模块在 hook 处调用本方法.

        Args:
            taskType: gameconst.BjTaskType 枚举值 (1-19)
            **params: 该 taskType 对应字段 (见 beginnerJourneyTaskType.EVENT_SCHEMAS)
                BJ_TASK_TYPE_ITEM_COST        : itemId, delta, srcType=0, quality=0
                BJ_TASK_TYPE_TASK_FINISH        : taskSubType, areaId
                BJ_TASK_TYPE_MAP_EXPLORE        : mapId, acPoint
                BJ_TASK_TYPE_KILL_MONSTER       : monsterType, mapId
                BJ_TASK_TYPE_DUNGEON_PASS       : dungeonId
                BJ_TASK_TYPE_TICKET_USE         : activityId
                BJ_TASK_TYPE_COLLECT            : npcPickId
                BJ_TASK_TYPE_PET_ACTIVATE       : quality
                BJ_TASK_TYPE_PET_EQUIP          : quality, countPerPet
                BJ_TASK_TYPE_PET_LEVEL          : level
                BJ_TASK_TYPE_MERIDIAN           : level
                BJ_TASK_TYPE_EQUIP_STRENGTHEN   : quality, strengthenLevel, part
                BJ_TASK_TYPE_EQUIP_GRADE        : quality, grade, part
                BJ_TASK_TYPE_WEAPON_BLESS       : level
                BJ_TASK_TYPE_WEAPON_INSCRIPTION : quality
                BJ_TASK_TYPE_EQUIP_AFFIX        : score
                BJ_TASK_TYPE_EQUIP_SOUL         : score
                BJ_TASK_TYPE_SKILL_LEVEL        : level
                BJ_TASK_TYPE_MINE_WAR_SCORE     : score
        """
        if gameconfig.isCrossServer():
            # 击杀怪物需要在跨服上支持，因为在跨服上触发需要转发回玩家源服处理
            if taskType == gameconst.BjTaskType.BJ_TASK_TYPE_KILL_MONSTER:
                # fnargs 必须是 tuple: 唯一参数是 list 时漏尾逗号会被 *fnargs 摊平成多个位置参数
                self.syncMethodCallToLocalServerBase('beginnerJourneyOnTaskEvents', ([(taskType, params)],))
            return
            
        if self.beginnerJourneyClosed:
            return
        
        return beginnerJourneyTaskType.dispatch_event(self, taskType, params)

    # =============================================================
    # GM 调试: 手动设置累积 (策划压测/QA 用)
    # =============================================================

    def gmSetBeginnerJourneyStat(self, taskId, value):
        """GM 命令: 设置某 taskID 的累积计数 (策划压测/QA 用)"""
        if not taskId:
            return
        self.beginnerJourneyBehaviorStats.setVal(taskId, int(value))
        # 跨过则标完成; ifCountedBeforeUnlock=1 时允许阶段未解锁也完成
        cfg = BJ_PT.datas.get(taskId)
        if cfg and (cfg.get('ifCountedBeforeUnlock', 0) or self.checkPhaseOpenned(taskId)):
            params = BJ_PT.taskIdWithTaskParams.get(taskId)
            if params:
                targetNum = params[0]
                cur = self.beginnerJourneyBehaviorStats.get(taskId)
                if cur >= targetNum and taskId not in self.beginnerJourneyFinishedTasks:
                    self.beginnerJourneyFinishedTasks.append(taskId)
                    self.client.onBeginnerJourneyTaskFinished(taskId)
        # GM 改值后同步推单任务更新
        self._pushBeginnerJourneyTaskUpdate(taskId)
