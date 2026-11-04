# -*- coding: utf-8 -*-
"""
新手历程 19 种 taskType 处理器 (v5, 2026-09-24)
==================================================================
v5 变更: 全部 19 种 taskType 统一为目标值累积型 (原属性查询型已删除).
  - 旧 v4: 区分累积型 (1-7,19) + 属性查询型 (8-18)
  - 新 v5: 全部 taskType 都通过 emit -> match_accumulate -> _accumulate 累积
  - 删除了 is_satisfied / is_attribute_task_type / 11 个属性查询分支
  - 新增 11 个 match_accumulate_* 函数 (taskType 8-18)
  - 删除了 iBeginnerJourney 中 10 个属性查询占位方法 (不再需要)

调用约定 (由 iBeginnerJourney.beginnerJourney_onTaskEvent 触发):
  dispatch_event(avatar, taskType, params)
    -> 校验 schema 字段
    -> 直接从 taskTypeWithPhaseTaskIds 拿 taskID 集合 (避免全表扫描)
    -> 遍历匹配的 taskCfg, 调 _ACCUMULATE_HANDLERS[taskType] (match_accumulate_*) 判定事件是否命中
    -> 命中后调 avatar._accumulate(taskId, delta=1) 累积 +1
    -> 已完成的任务 (tid in finishedTaskIds) 早退, 跳过累积

字段语义 (运行时从 BJ_PT.taskIdWithTaskParams[taskID] 读):
  taskType=1   道具变化       param2=道具ID, param3=途径(list,0=任意),delta
  taskType=2   完成任务数     param2=任务类型(1=悬赏/2=地区),param3=地图ID(list,0=任意)
  taskType=3   地区探索次数   param2=地图ID, 每 emit +1
  taskType=4   击杀怪物       param2=怪物类型, param3=地图ID(list,0=任意)
  taskType=5   通关讨伐副本   param2=dungeonId
  taskType=6   门票           param2=父活动ID
  taskType=7   采集           param2=npcPickId (list)
  taskType=8   激活精灵       param2=品质           (累积: 每次激活匹配品质 +1)
  taskType=9   精灵穿戴遗器   param2=每只精灵遗器数, param3=品质
  taskType=10  精灵等级       param2=等级           (累积: 每次升级到 >=level +1)
  taskType=11  经脉养成       param2=阶数           (累积: 每次升级到 >=level +1)
  taskType=12  装备强化       param2=品质, param3=强化等级, param4=部位(list,0=任意)
  taskType=13  装备等阶       param2=品质, param3=等阶, param4=部位(list)
  taskType=14  武器祝福       param2=等级           (累积: 每次升到 >=level +1)
  taskType=15  武器铭文       param2=品质           (累积: 每次铭文品质匹配 +1)
  taskType=16  附灵评分       param2=评分           (累积: 每次评分达 >=param2 +1)
  taskType=17  魂魄评分       param2=评分
  taskType=18  技能等级       param2=等级           (累积: 每次技能升到 >=level +1)
  taskType=19  矿战积分       param2=阈值 (score>=param2 算一次)
  taskType=20  收集系统统计   param2=目标品质 (每次收集到品质>=param2[0] 的项 +1)
  taskType=21  死亡掉装拾取   param2=目标品质 (每次成功拾取品质>=param2[0] 的装备 +1, 触发于 _onTakeDropEquipSuccess)
"""
from KBEDebug import *

import gameconst
import gamedecorator

import beginnerJourney_phaseTask as BJ_PT

# =============================================================
# 通用工具
# =============================================================

def _listContains(lst, val, allowZero=True):
    """list 匹配: lst 为空/None 或含 0(通配) -> True; 否则 val ∈ lst"""
    if not lst:
        return True
    if allowZero and 0 in lst:
        return True
    return val in lst

# =============================================================
# 累积型: 19 种 (taskType=1..19)
# =============================================================

# ---- 累积型 1-7, 19 (v4 已有, 行为不变) ----

def match_accumulate_item_change(avatar, taskCfg, targetNum, param2, param3, param4,
                                  delta, itemId, srcType, quality):
    """taskType=1: 道具变化"""
    if param2[0] != 0 and param2[0] != itemId:
        return False
    # param3=变化途径 (antiAddictCategory_ID), 0/空 表示任意
    if not _listContains(param3, srcType):
        return False
    if param4[0] != 0 and quality < param4[0]:
        return False
    return True


def match_accumulate_task_finish(avatar, taskCfg, targetNum, param2, param3, param4,
                                   delta, taskSubType, areaId):
    """taskType=2: 完成任务数"""
    if param2[0] != taskSubType:
        return False
    if not _listContains(param3, areaId):
        return False
    return True


def match_accumulate_map_explore(avatar, taskCfg, targetNum, param2, param3, param4,
                                  delta, mapId):
    """taskType=3: 地区探索次数 (param2=地图ID, 每 emit +1)"""
    # 任意地图
    if param2[0] == 0:
        return True
    return param2[0] == mapId


def match_accumulate_kill_monster(avatar, taskCfg, targetNum, param2, param3, param4,
                                    delta, monsterType, mapId):
    """taskType=4: 击杀怪物"""
    if not _listContains(param2, monsterType):
        return False
    if param3[0] != 0 and not _listContains(param3, mapId):
        return False
    return True


def match_accumulate_dungeon_pass(avatar, taskCfg, targetNum, param2, param3, param4,
                                    delta, dungeonId):
    """taskType=5: 通关讨伐副本"""
    return param2[0] == dungeonId


def match_accumulate_ticket_use(avatar, taskCfg, targetNum, param2, param3, param4,
                                  delta, activityId):
    """taskType=6: 门票使用"""
    return param2[0] == activityId


def match_accumulate_collect(avatar, taskCfg, targetNum, param2, param3, param4,
                              delta, npcPickId):
    """taskType=7: 采集"""
    return npcPickId in param2


def match_accumulate_mine_war_score(avatar, taskCfg, targetNum, param2, param3, param4,
                                     delta, score):
    """taskType=19: 矿战积分 (单场 score>=param2 阈值算 1 次达成)"""
    return score >= param2[0]


# ---- v5 新增累积型 8-18 (原属性查询型改为 emit 累积) ----

def match_accumulate_pet_activate(avatar, taskCfg, targetNum, param2, param3, param4,
                                   delta, quality):
    """
    taskType=8: 激活精灵 (param2=品质)
    业务模块在玩家激活精灵时 emit: quality=该精灵品质
    """
    return quality >= param2[0]


def match_accumulate_pet_equip(avatar, taskCfg, targetNum, param2, param3, param4,
                                delta, quality, countPerPet):
    """
    taskType=9: 精灵穿戴遗器 (param2=每只精灵遗器数, param3=品质)
    业务模块在某只精灵的穿戴数满足条件时 emit: quality + countPerPet
    """
    return quality >= param3[0] and countPerPet >= param2[0]


def match_accumulate_pet_level(avatar, taskCfg, targetNum, param2, param3, param4,
                                delta, level):
    """
    taskType=10: 精灵等级 (param2=等级)
    业务模块在精灵升级时 emit: level=新等级
    """
    return level >= param2[0]


def match_accumulate_meridian(avatar, taskCfg, targetNum, param2, param3, param4,
                               delta, level):
    """
    taskType=11: 经脉养成 (param2=阶数)
    业务模块在经脉升级时 emit: level=新阶数
    """
    return level >= param2[0]


def match_accumulate_equip_strengthen(avatar, taskCfg, targetNum, param2, param3, param4,
                                       delta, quality, strengthenLevel, part):
    """
    taskType=12: 装备强化 (param2=品质, param3=强化等级, param4=部位 list)
    业务模块在装备强化时 emit: quality + strengthenLevel + part
    """
    if quality < param2[0]:
        return False
    if strengthenLevel < param3[0]:
        return False
    if param4[0] != 0 and not _listContains(param4, part):
        return False
    return True


def match_accumulate_equip_grade(avatar, taskCfg, targetNum, param2, param3, param4,
                                   delta, quality, grade, part):
    """
    taskType=13: 装备等阶 (param2=品质, param3=等阶, param4=部位 list)
    业务模块在装备升阶时 emit: quality + grade + part
    """
    if quality < param2[0]:
        return False
    if grade < param3[0]:
        return False
    if param4[0] != 0 and not _listContains(param4, part):
        return False
    return True


def match_accumulate_weapon_bless(avatar, taskCfg, targetNum, param2, param3, param4,
                                   delta, level):
    """
    taskType=14: 武器祝福 (param2=等级)
    业务模块在武器祝福升级时 emit: level=新等级
    """
    return level >= param2[0]


def match_accumulate_weapon_inscription(avatar, taskCfg, targetNum, param2, param3, param4,
                                          delta, quality, numSlot):
    """
    taskType=15: 武器铭文 (param2=品质)
    业务模块在武器铭文时 emit: quality=武器品质
    """
    if quality >= param2[0]:
        if param3[0] == 1:
            if numSlot > 0:
                return True
        elif param3[0] == 2:
            if numSlot == 2:
                return True
    return False


def match_accumulate_equip_affix(avatar, taskCfg, targetNum, param2, param3, param4,
                                   delta, score):
    """
    taskType=16: 附灵评分 (param2=评分阈值)
    业务模块在装备附灵评分变化时 emit: score=新评分
    """
    return score >= param2[0]


def match_accumulate_equip_soul(avatar, taskCfg, targetNum, param2, param3, param4,
                                  delta, score):
    """
    taskType=17: 魂魄评分 (param2=评分阈值)
    业务模块在装备魂魄评分变化时 emit: score=新评分
    """
    return score >= param2[0]


def match_accumulate_skill_level(avatar, taskCfg, targetNum, param2, param3, param4,
                                   delta, level):
    """
    taskType=18: 技能等级 (param2=等级)
    业务模块在技能升级时 emit: level=新等级
    """
    return level >= param2[0]


def match_accumulate_collection_stat(avatar, taskCfg, targetNum, param2, param3, param4,
                                       delta, quality):
    """
    taskType=20: 收集系统统计 (param2=目标品质)
    业务模块在玩家完成指定品质收集项时 emit: quality=该收集项品质
    返回 quality == param2[0] 即算 1 次, 由 dispatch_event 累积 +1.

    触发点候选 (待接入, 见 _ACCUMULATE_HANDLERS 注释):
      - iCollectible.reqCollect 提交装备入收集位成功时
      - 其他收集/图鉴系统提交成功时
    """
    return quality == param2[0]


def match_accumulate_death_drop_pickup(avatar, taskCfg, targetNum, param2, param3, param4,
                                        delta, quality):
    """
    taskType=21: 死亡掉装拾取 (param2=目标品质)
    业务模块在玩家成功拾取掉落的装备时 emit: quality=被拾取装备的品质
    返回 quality >= param2[0] 即算 1 次, 由 dispatch_event 累积 delta (=1).

    触发点:
      - base/impEquipment.py::_onTakeDropEquipSuccess (统一拾取入口)
      - 当前实现统计"任意掉落装备的拾取", 不区分死亡 vs 怪物掉落 vs 邮件退还;
        进一步细分来源可在 DropStub.dropEquipItem 扩 sourceType 字段后, 在 handler 内
        配合 param3 取选。
    """
    return quality >= param2[0]


# =============================================================
# 调度层: match_accumulate 主入口 (按 taskType 分发)
# =============================================================

_ACCUMULATE_HANDLERS = {
    gameconst.BjTaskType.BJ_TASK_TYPE_ITEM_GET:        match_accumulate_item_change,
    gameconst.BjTaskType.BJ_TASK_TYPE_TASK_FINISH:        match_accumulate_task_finish,
    gameconst.BjTaskType.BJ_TASK_TYPE_MAP_EXPLORE:        match_accumulate_map_explore,
    gameconst.BjTaskType.BJ_TASK_TYPE_KILL_MONSTER:       match_accumulate_kill_monster,
    gameconst.BjTaskType.BJ_TASK_TYPE_DUNGEON_PASS:       match_accumulate_dungeon_pass,
    gameconst.BjTaskType.BJ_TASK_TYPE_TICKET_USE:         match_accumulate_ticket_use,
    gameconst.BjTaskType.BJ_TASK_TYPE_COLLECT:            match_accumulate_collect,
    gameconst.BjTaskType.BJ_TASK_TYPE_PET_ACTIVATE:       match_accumulate_pet_activate,
    gameconst.BjTaskType.BJ_TASK_TYPE_PET_EQUIP:          match_accumulate_pet_equip,
    gameconst.BjTaskType.BJ_TASK_TYPE_PET_LEVEL:          match_accumulate_pet_level,
    gameconst.BjTaskType.BJ_TASK_TYPE_MERIDIAN:           match_accumulate_meridian,
    gameconst.BjTaskType.BJ_TASK_TYPE_EQUIP_STRENGTHEN:   match_accumulate_equip_strengthen,
    gameconst.BjTaskType.BJ_TASK_TYPE_EQUIP_GRADE:        match_accumulate_equip_grade,
    gameconst.BjTaskType.BJ_TASK_TYPE_WEAPON_BLESS:       match_accumulate_weapon_bless,
    gameconst.BjTaskType.BJ_TASK_TYPE_WEAPON_INSCRIPTION: match_accumulate_weapon_inscription,
    gameconst.BjTaskType.BJ_TASK_TYPE_EQUIP_AFFIX:        match_accumulate_equip_affix,
    gameconst.BjTaskType.BJ_TASK_TYPE_EQUIP_SOUL:         match_accumulate_equip_soul,
    gameconst.BjTaskType.BJ_TASK_TYPE_SKILL_LEVEL:        match_accumulate_skill_level,
    gameconst.BjTaskType.BJ_TASK_TYPE_MINE_WAR_SCORE:     match_accumulate_mine_war_score,
    gameconst.BjTaskType.BJ_TASK_TYPE_COLLECTION_STAT:   match_accumulate_collection_stat,
    gameconst.BjTaskType.BJ_TASK_TYPE_DEATH_DROP_PICKUP: match_accumulate_death_drop_pickup,
    gameconst.BjTaskType.BJ_TASK_TYPE_ITEM_COST:        match_accumulate_item_change,
}


def dispatch_accumulate(avatar, taskCfg, targetNum, param2, param3, param4, eventArgs):
    """
    累积型 handler 统一入口. eventArgs 由 iBeginnerJourney 包装为 dict,
    handler 自行从 dict 取所需字段 (itemId, delta, srcType, ...).
    返回 True 表示事件匹配该 taskCfg, 主类负责 _accumulate.
    """
    taskType = taskCfg.get('taskType', 0)
    handler = _ACCUMULATE_HANDLERS.get(taskType)
    if not handler:
        return False
    try:
        return handler(avatar, taskCfg, targetNum, param2, param3, param4, **eventArgs)
    except TypeError:
        # handler 签名与 eventArgs 不匹配 -> 忽略
        return False


def is_accumulate_task_type(taskType):
    """该 taskType 是否属于累积型 (v5: 1-19 全部)"""
    return taskType in _ACCUMULATE_HANDLERS


# =============================================================
# 统一 emit 入口 (业务模块调用 self.beginnerJourneyOnTaskEvents)
# =============================================================

# 19 种累积型 taskType 对应的 params 字段 schema.
# 业务模块按此填 kwargs, 缺字段会 LOG_WARN 拒绝.
# 19 种 taskType 对应的 params 字段 schema.
# 业务模块按此填 kwargs, 缺字段会 LOG_WARN 拒绝.
# 约定: 每种 schema 的第 1 个字段固定为 'delta' (本事件累积量, 业务模块必填).
#   - 单事件计数型 (KILL/DUNGEON/TICKET 等): delta=1
#   - 数量型 (ITEM_CHANGE): delta=实际数量 (如消耗 5 个道具 -> delta=5)
#   - 阈值多次累积型 (PET_LEVEL/MERIDIAN 等): delta=1
#   - 阈值一次型 (MINE_WAR_SCORE): delta=1
EVENT_SCHEMAS = {
    gameconst.BjTaskType.BJ_TASK_TYPE_ITEM_GET:        ('delta', 'itemId', 'srcType', 'quality'),
    gameconst.BjTaskType.BJ_TASK_TYPE_TASK_FINISH:        ('delta', 'taskSubType', 'areaId'),
    gameconst.BjTaskType.BJ_TASK_TYPE_MAP_EXPLORE:        ('delta', 'mapId'),
    gameconst.BjTaskType.BJ_TASK_TYPE_KILL_MONSTER:       ('delta', 'monsterType', 'mapId'),
    gameconst.BjTaskType.BJ_TASK_TYPE_DUNGEON_PASS:       ('delta', 'dungeonId'),
    gameconst.BjTaskType.BJ_TASK_TYPE_TICKET_USE:         ('delta', 'activityId'),
    gameconst.BjTaskType.BJ_TASK_TYPE_COLLECT:            ('delta', 'npcPickId'),
    gameconst.BjTaskType.BJ_TASK_TYPE_PET_ACTIVATE:       ('delta', 'quality'),
    gameconst.BjTaskType.BJ_TASK_TYPE_PET_EQUIP:          ('delta', 'quality', 'countPerPet'),
    gameconst.BjTaskType.BJ_TASK_TYPE_PET_LEVEL:          ('delta', 'level'),
    gameconst.BjTaskType.BJ_TASK_TYPE_MERIDIAN:           ('delta', 'level'),
    gameconst.BjTaskType.BJ_TASK_TYPE_EQUIP_STRENGTHEN:   ('delta', 'quality', 'strengthenLevel', 'part'),
    gameconst.BjTaskType.BJ_TASK_TYPE_EQUIP_GRADE:        ('delta', 'quality', 'grade', 'part'),
    gameconst.BjTaskType.BJ_TASK_TYPE_WEAPON_BLESS:       ('delta', 'level'),
    gameconst.BjTaskType.BJ_TASK_TYPE_WEAPON_INSCRIPTION: ('delta', 'quality', 'numSlot'),
    gameconst.BjTaskType.BJ_TASK_TYPE_EQUIP_AFFIX:        ('delta', 'score'),
    gameconst.BjTaskType.BJ_TASK_TYPE_EQUIP_SOUL:         ('delta', 'score'),
    gameconst.BjTaskType.BJ_TASK_TYPE_SKILL_LEVEL:        ('delta', 'level'),
    gameconst.BjTaskType.BJ_TASK_TYPE_MINE_WAR_SCORE:     ('delta', 'score'),
    gameconst.BjTaskType.BJ_TASK_TYPE_COLLECTION_STAT:   ('delta', 'quality'),
    gameconst.BjTaskType.BJ_TASK_TYPE_DEATH_DROP_PICKUP: ('delta', 'quality'),
    gameconst.BjTaskType.BJ_TASK_TYPE_ITEM_COST:        ('delta', 'itemId', 'srcType', 'quality'),
}

def dispatch_event(avatar, taskType, params):
    """
    统一 emit 入口 (业务模块调用). 业务模块通过 Avatar.beginnerJourneyOnTaskEvents 进入.
    taskType: gameconst.BjTaskType 枚举值 (1-19)
    params: dict 包含 EVENT_SCHEMAS[taskType] 列出的字段
    返回: 处理的 taskID 列表 (用于单元测试 / 日志统计)
    """
    if avatar.beginnerJourneyClosed:
        return []
    
    ret = gamedecorator.doCheckGameConfig(avatar, 'beginnerJourneyTask', False)
    if not ret:
        LOG_WARN('dispatch_event: beginnerJourneyTask switch is closed', taskType, params)
        return []
    
    schema = EVENT_SCHEMAS.get(taskType)
    if not schema:
        LOG_WARN('dispatch_event: taskType unknown (not 1-19)', 'type=', taskType)
        return []
    # 字段校验
    params = params or {}
    missing = [k for k in schema if k not in params]
    if missing:
        LOG_WARN('dispatch_event: missing fields', 'type=', taskType, 'missing=', missing)
        return []

    matched_tids = []
    # 直接从 taskTypeWithPhaseTaskIds 拿 taskID 集合 (策划导出脚本生成, 避免全表扫描)
    tids = BJ_PT.taskTypeWithPhaseTaskIds.get(taskType) or []
    for tid in tids:
        # 已完成的任务跳过累积 (避免 setVal + push update + match 检查等无效开销)
        if tid in avatar.beginnerJourneyFinishedTasks:
            continue
        cfg = BJ_PT.datas.get(tid)
        if not cfg:
            continue
        if not avatar._isTaskCountable(cfg):
            continue
        cfg_params = BJ_PT.taskIdWithTaskParams.get(tid)
        if not cfg_params:
            continue
        targetNum, param2, param3, param4 = cfg_params
        if not dispatch_accumulate(avatar, cfg, targetNum, param2, param3, param4, params):
            continue
        # delta 来自 params (ITEM_CHANGE 业务传具体数量, 如消耗 5 个道具 -> delta=5;
        # 其他 taskType 没有 delta 字段, 默认 1)
        delta = params.get('delta', 0)
        avatar._accumulate(tid, delta)
        matched_tids.append(tid)
    return matched_tids
