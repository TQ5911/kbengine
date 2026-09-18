# coding: utf-8
import KBEngine
from KBEDebug import *

import itertools
import warnings
import math
import random

import gameconfig
import gameengine
import gametimer
import formula
import gameconst
import utils

import dungeon

import creep_base as CB
import gamePlay_gamePlay as DDL
import gamePlay_set as GP_SD
# import dungeon_dungeonMonster as DDMD
import NPC_NPC as NPC_DATA

import formula_generalFormula as F_GFD




class IDungeonStubMonster(object):
    DEFAULT_DIRECTION = (0, 0, 0)
    DEFAULT_MAX_ENT_LOAD_NUM = 5

    EACH_TICK_SAPCE_CREATE_ENTITY_COUNT = 5
    # 先把流速改为 400了 第一个副本总共会放141个怪，400的话一秒钟能放完三个4002
    # 这个后续必须得压测下

    def _loadDungeonSpaceEntities(self, spaceNo, playerBox, playerGbId,\
                                  teamUUID, extra):
        pass

    def cancelSpaceEntitiesLoadingProcess(self, spaceNo):
        LOG_DBG("cancelSpaceEntitiesLoadingProcess::", spaceNo)

    # =========================================
    # KILL COUNT METHODS

    def addKillCount(self, spaceNo, flagId, creepbaseId):
        if spaceNo not in self.spaces:
            LOG_ERR('wl: createCellEntity cannot find space:', spaceNo)
            return

        _sVal = self.spaces[spaceNo]

        # 【【程序自主】【副本编辑器】服务流程编辑器怪物原型ID检测支持临时Entity(没有副本ID的Entity)】
        if not (flagId or creepbaseId):
            LOG_ERR('addKillCount:: must set flagId or creepbaseId')
            return

        # 【【任务】副本编辑器新节点-指定怪物原型死亡数量】
        dungeonNo = formula.parseDungeonNoBySpaceNo(spaceNo)
        dunData = utils.getDunModuleData(dungeonNo)
        if not creepbaseId:
            creepbaseId = dunData.get(str(flagId), {}).get('EntityID', 0)

        LOG_DBG('------ addKillCount in {}/{}'.format(spaceNo, flagId))
        _needAddCreepBaseKillNumFlag = True

        if flagId:
            if not _sVal.getTimeLine(flagId):
                _sVal.addTimeLine(flagId)
            _sVal.addKill(flagId)
            _needAddCreepBaseKillNumFlag = False
            _sVal.spaceMgr.cell.flowCtrlDunMonsterKillNumInc(
                flagId, _sVal.getTimeLine(flagId).kills, _sVal.killSum)

        # 【【任务】副本编辑器新节点-指定怪物原型死亡数量】
        if creepbaseId:
            _sVal.addKillByCreepBaseId(creepbaseId, _needAddCreepBaseKillNumFlag)
            _sVal.spaceMgr.cell.flowCtrlDunMonsterKillNumIncByMonsterId(
                creepbaseId, _sVal.getCreepBaseKilledNum(creepbaseId), _sVal.killSum)

        LOG_DBG('----- NOW KILL {} MONSTERS in space {}'
                  '-----'.format(_sVal.killSum, spaceNo))

    def flowCheckDungeonKillCount(self, spaceNo, monsterGID, symbol, number, usePrototypeID, eid, ctx, checkOnce):
        LOG_DBG("flowCheckDungeonKillCount::", spaceNo, monsterGID, symbol, number, usePrototypeID, eid, ctx, checkOnce)

        if spaceNo not in self.spaces:
            LOG_ERR('flowCheckDungeonKillCount:: cannot find space', spaceNo)
            return

        if not monsterGID:
            LOG_ERR('flowCheckDungeonKillCount:: monsterGID must set number', monsterGID)
            return

        _sVal = self.spaces[spaceNo]

        if usePrototypeID:
            curKillNum = _sVal.getCreepBaseKilledNum(monsterGID)
        else:
            _val = _sVal.getTimeLine(monsterGID)
            curKillNum = _val.kills if _val else 0

        if not (_sVal.spaceMgr and _sVal.spaceMgr.cell):
            LOG_WARN("flowCheckDungeonKillCount:: spaceMgr not found", spaceNo)
            return

        _sVal.spaceMgr.cell.flowCtrlOnCheckDungeonEntityKillNumber(monsterGID, symbol, number, curKillNum, usePrototypeID, eid, ctx, checkOnce)

    def flowCheckDungeonAllKillCount(self, spaceNo, symbol, number, eid, ctx, checkOnce):
        LOG_DBG("flowCheckDungeonAllKillCount::", spaceNo, symbol, number, eid, ctx, checkOnce)
        if spaceNo not in self.spaces:
            LOG_ERR('flowCheckDungeonAllKillCount:: cannot find space', spaceNo)
            return

        _sVal = self.spaces[spaceNo]
        curKillNum = _sVal.killSum

        if not (_sVal.spaceMgr and _sVal.spaceMgr.cell):
            LOG_WARN("flowCheckDungeonAllKillCount:: spaceMgr not found", spaceNo)
            return

        _sVal.spaceMgr.cell.flowCtrlOnCheckDungeonAllEntityKillNumber(symbol, number, curKillNum, eid, ctx, checkOnce)


    # =========================================
