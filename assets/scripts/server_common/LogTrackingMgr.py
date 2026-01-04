# -*- coding: utf-8 -*-
import json
from enum import Enum
from KBEDebug import *
import KBEngine
import gamelog
import gameconfig
import utils

class LogTrackingMgr:
    # 充值完成事件
    @staticmethod
    def Server_Recharge_Complete(accountId, roleId, itemType, itemId, price, orderId):
        args = {}
        args["trackName"] = "Server_Recharge_Complete"
        args["accountId"] = accountId
        args["roleId"] = roleId
        args["itemType"] = itemType
        args["itemId"] = itemId
        args["price"] = price
        args["orderId"] = orderId
        LogTrackingMgr.LOG(args)

    # PCU事件
    @staticmethod
    def Server_Pcu(pcu):
        args = {}
        args["trackName"] = "Server_Pcu"
        args["pcu"] = pcu
        LogTrackingMgr.LOG(args)

    # 用户登出事件
    @staticmethod
    def Server_Logout(accountId, deviceModel, ipAddress, operatingSystem, channelSource):
        args = {}
        args["trackName"] = "Server_Logout"
        args["accountId"] = accountId
        args["deviceModel"] = deviceModel
        args["ipAddress"] = ipAddress
        args["operatingSystem"] = operatingSystem
        args["channelSource"] = channelSource
        LogTrackingMgr.LOG(args)

    # 用户登录事件
    @staticmethod
    def Server_Login(accountId, deviceModel, ipAddress, operatingSystem, accountType, channelSource):
        args = {}
        args["trackName"] = "Server_Login"
        args["accountId"] = accountId
        args["deviceModel"] = deviceModel
        args["ipAddress"] = ipAddress
        args["operatingSystem"] = operatingSystem
        args["accountType"] = accountType
        args["channelSource"] = channelSource
        LogTrackingMgr.LOG(args)

    # 角色登录事件
    @staticmethod
    def Server_Role_Login(accountId, gbId, school, name, level, gameId, userInfoId, createTimestamp, accountType, channelSource):
        args = {}
        args["trackName"] = "Server_Role_Login"
        args["accountId"] = accountId
        args["gbId"] = gbId
        args["school"] = school
        args["name"] = name
        args["level"] = level
        args["gameId"] = gameId
        args["userInfoId"] = userInfoId
        args["createTimestamp"] = createTimestamp
        args["accountType"] = accountType
        args["channelSource"] = channelSource
        LogTrackingMgr.LOG(args)

    # 角色登出事件
    @staticmethod
    def Server_Role_Logout(accountId, gbId, school, name, level):
        args = {}
        args["trackName"] = "Server_Role_Logout"
        args["accountId"] = accountId
        args["gbId"] = gbId
        args["school"] = school
        args["name"] = name
        args["level"] = level
        LogTrackingMgr.LOG(args)

    # 创建角色事件
    @staticmethod
    def Server_Create_Role(accountId, gbId, school, name, gameId, userInfoId, createTimestamp):
        args = {}
        args["trackName"] = "Server_Create_Role"
        args["accountId"] = accountId
        args["gbId"] = gbId
        args["school"] = school
        args["name"] = name
        args["gameId"] = gameId
        args["userInfoId"] = userInfoId
        args["createTimestamp"] = createTimestamp
        LogTrackingMgr.LOG(args)

    # 合成道具事件
    @staticmethod
    def Synthesis_Item(costItemID, costItemNum, costCurrencyID, costCurrencyNum, getID, getNum, getQuality):
        args = {}
        args["trackName"] = "Synthesis_Item"
        args["costItemID"] = costItemID
        args["costItemNum"] = costItemNum
        args["costCurrencyID"] = costCurrencyID
        args["costCurrencyNum"] = costCurrencyNum
        args["getID"] = getID
        args["getNum"] = getNum
        args["getQuality"] = getQuality
        LogTrackingMgr.LOG(args)

    # 矿战开启事件
    @staticmethod
    def MineBattle_Start(activityStartTime, coreBelongGuildID):
        args = {}
        args["trackName"] = "MineBattle_Start"
        args["activityStartTime"] = activityStartTime
        args["coreBelongGuildID"] = coreBelongGuildID
        LogTrackingMgr.LOG(args)

    # 矿战结束事件
    @staticmethod
    def MineBattle_End(activityEndTime, coreBelongGuildID, coreBelongTime, activityRank):
        args = {}
        args["trackName"] = "MineBattle_End"
        args["activityEndTime"] = activityEndTime
        args["coreBelongGuildID"] = coreBelongGuildID
        args["coreBelongTime"] = coreBelongTime
        args["activityRank"] = activityRank
        LogTrackingMgr.LOG(args)

    # 矿战分红事件
    @staticmethod
    def MineBattle_Shared(miningAreaBelongGuildID, miningAreaOutput, dividendedPlayerID, dividendedCurrencyNum):
        args = {}
        args["trackName"] = "MineBattle_Shared"
        args["miningAreaBelongGuildID"] = miningAreaBelongGuildID
        args["miningAreaOutput"] = miningAreaOutput
        args["dividendedPlayerID"] = dividendedPlayerID
        args["dividendedCurrencyNum"] = dividendedCurrencyNum
        LogTrackingMgr.LOG(args)

    # 矿战击杀旗帜事件
    @staticmethod
    def MineBattle_KillFlag(mapId, killerGuildID, killerPlayerID, flagDeathTimes):
        args = {}
        args["trackName"] = "MineBattle_KillFlag"
        args["mapId"] = mapId
        args["killerGuildID"] = killerGuildID
        args["killerPlayerID"] = killerPlayerID
        args["flagDeathTimes"] = flagDeathTimes
        LogTrackingMgr.LOG(args)

    # 技能升级事件
    @staticmethod
    def Skill_Upgrade(ID, costItemID, costItemNum, costCurrencyID, costCurrencyNum, level):
        args = {}
        args["trackName"] = "Skill_Upgrade"
        args["ID"] = ID
        args["costItemID"] = costItemID
        args["costItemNum"] = costItemNum
        args["costCurrencyID"] = costCurrencyID
        args["costCurrencyNum"] = costCurrencyNum
        args["level"] = level
        LogTrackingMgr.LOG(args)

    # 发红包事件
    @staticmethod
    def Release_RedBag(sendType, sendChannel, sendNumber, sendCostItemID, sendCostItemNum):
        args = {}
        args["trackName"] = "Release_RedBag"
        args["sendType"] = sendType
        args["sendChannel"] = sendChannel
        args["sendNumber"] = sendNumber
        args["sendCostItemID"] = sendCostItemID
        args["sendCostItemNum"] = sendCostItemNum
        LogTrackingMgr.LOG(args)

    # 领红包事件
    @staticmethod
    def Fetch_RedBag(getType, getChannel, getItemID, getItemNum, claimedRemainNumber, claimedRemainItemID, claimedRemainItemNum):
        args = {}
        args["trackName"] = "Fetch_RedBag"
        args["getType"] = getType
        args["getChannel"] = getChannel
        args["getItemID"] = getItemID
        args["getItemNum"] = getItemNum
        args["claimedRemainNumber"] = claimedRemainNumber
        args["claimedRemainItemID"] = claimedRemainItemID
        args["claimedRemainItemNum"] = claimedRemainItemNum
        LogTrackingMgr.LOG(args)

    # 公会信息事件
    @staticmethod
    def Guild_Info(guildUUID, level, fundNum, goldNum, tokenNum, src, opUUID, desc):
        args = {}
        args["trackName"] = "Guild_Info"
        args["guildUUID"] = guildUUID
        args["level"] = level
        args["fundNum"] = fundNum
        args["goldNum"] = goldNum
        args["tokenNum"] = tokenNum
        args["src"] = src
        args["opUUID"] = opUUID
        args["desc"] = desc
        LogTrackingMgr.LOG(args)

    # 公会练功场重置
    @staticmethod
    def Guild_Train_Reset(gbId):
        args = {}
        args["trackName"] = "Guild_Train_Reset"
        args["gbId"] = gbId
        LogTrackingMgr.LOG(args)

    # 公会练功场事件
    @staticmethod
    def Guild_Train(gbId, trainId, trainLevel, trainProp):
        args = {}
        args["trackName"] = "Guild_Train"
        args["gbId"] = gbId
        args["trainId"] = trainId
        args["trainLevel"] = trainLevel
        args["trainProp"] = trainProp
        LogTrackingMgr.LOG(args)

    # 公会任务事件
    @staticmethod
    def Guild_Task(gbId, taskId, taskProgress, taskState):
        args = {}
        args["trackName"] = "Guild_Task"
        args["gbId"] = gbId
        args["taskId"] = taskId
        args["taskProgress"] = taskProgress
        args["taskState"] = taskState
        LogTrackingMgr.LOG(args)

    # 公会商店事件
    @staticmethod
    def Guild_Shop(shopSellItemId, shopSellTimes):
        args = {}
        args["trackName"] = "Guild_Shop"
        args["shopSellItemId"] = shopSellItemId
        args["shopSellTimes"] = shopSellTimes
        LogTrackingMgr.LOG(args)

    # 帮会聚义楼协助
    @staticmethod
    def Guild_Assist(guild_buildingID, srcGbId, guildUUID, guild_buildingLevel, exp):
        args = {}
        args["trackName"] = "Guild_Assist"
        args["guild_buildingID"] = guild_buildingID
        args["srcGbId"] = srcGbId
        args["guildUUID"] = guildUUID
        args["guild_buildingLevel"] = guild_buildingLevel
        args["exp"] = exp
        LogTrackingMgr.LOG(args)

    # 帮会军需处协助
    @staticmethod
    def Guild_QiXieAssist(guild_warEquipmentID, srcGbId, guildUUID, guild_warEquipmentLevel, exp):
        args = {}
        args["trackName"] = "Guild_QiXieAssist"
        args["guild_warEquipmentID"] = guild_warEquipmentID
        args["srcGbId"] = srcGbId
        args["guildUUID"] = guildUUID
        args["guild_warEquipmentLevel"] = guild_warEquipmentLevel
        args["exp"] = exp
        LogTrackingMgr.LOG(args)

    # 魔方事件
    @staticmethod
    def Cube_Info(gbId, gameId, floor, mapId, cubeEvent):
        args = {}
        args["trackName"] = "Cube_Info"
        args["gbId"] = gbId
        args["gameId"] = gameId
        args["floor"] = floor
        args["mapId"] = mapId
        args["cubeEvent"] = cubeEvent
        LogTrackingMgr.LOG(args)

    # 仙境事件
    @staticmethod
    def Wonderland_Info(gbId, gameId, floor, wonderLandEvent):
        args = {}
        args["trackName"] = "Wonderland_Info"
        args["gbId"] = gbId
        args["gameId"] = gameId
        args["floor"] = floor
        args["wonderLandEvent"] = wonderLandEvent
        LogTrackingMgr.LOG(args)

    # 成就事件
    @staticmethod
    def Achievement_Update(accountId, gbId, gameId, achieveId, version, state, progress):
        args = {}
        args["trackName"] = "Achievement_Update"
        args["accountId"] = accountId
        args["gbId"] = gbId
        args["gameId"] = gameId
        args["achieveId"] = achieveId
        args["version"] = version
        args["state"] = state
        args["progress"] = progress
        LogTrackingMgr.LOG(args)

    # 道具事件
    @staticmethod
    def Get_Item(accountId, gbId, gameId, itemId, uniqueId, bagType, delta, newNum, src, opUUID, desc):
        args = {}
        args["trackName"] = "Get_Item"
        args["accountId"] = accountId
        args["gbId"] = gbId
        args["gameId"] = gameId
        args["itemId"] = itemId
        args["uniqueId"] = uniqueId
        args["bagType"] = bagType
        args["delta"] = delta
        args["newNum"] = newNum
        args["src"] = src
        args["opUUID"] = opUUID
        args["desc"] = desc
        LogTrackingMgr.LOG(args)

    # 任务事件
    @staticmethod
    def Task_Event(gbId, gameId, opNUID, taskId, state, taskType, source, reason):
        args = {}
        args["trackName"] = "Task_Event"
        args["gbId"] = gbId
        args["gameId"] = gameId
        args["opNUID"] = opNUID
        args["taskId"] = taskId
        args["state"] = state
        args["taskType"] = taskType
        args["source"] = source
        args["reason"] = reason
        LogTrackingMgr.LOG(args)

    # 通用死亡事件
    @staticmethod
    def Common_Death(gbId, gameId, mapId, killerGbId, killerType):
        args = {}
        args["trackName"] = "Common_Death"
        args["gbId"] = gbId
        args["gameId"] = gameId
        args["mapId"] = mapId
        args["killerGbId"] = killerGbId
        args["killerType"] = killerType
        LogTrackingMgr.LOG(args)

    # 等级有礼事件
    @staticmethod
    def Level_Reward(gbId, level, welfareId, levelLimit, school):
        args = {}
        args["trackName"] = "Level_Reward"
        args["gbId"] = gbId
        args["level"] = level
        args["welfareId"] = welfareId
        args["levelLimit"] = levelLimit
        args["school"] = school
        LogTrackingMgr.LOG(args)

    # 七日签到事件
    @staticmethod
    def Welfare_SignInSevenDay(gbId, welfareId, level):
        args = {}
        args["trackName"] = "Welfare_SignInSevenDay"
        args["gbId"] = gbId
        args["welfareId"] = welfareId
        args["level"] = level
        LogTrackingMgr.LOG(args)

    # 十日签到事件
    @staticmethod
    def Welfare_SignInTenDay(gbId, welfareId, level):
        args = {}
        args["trackName"] = "Welfare_SignInTenDay"
        args["gbId"] = gbId
        args["welfareId"] = welfareId
        args["level"] = level
        LogTrackingMgr.LOG(args)

    # 月卡事件
    @staticmethod
    def MonthCard_Invoke(gbId, level, invokeTime, expireTime):
        args = {}
        args["trackName"] = "MonthCard_Invoke"
        args["gbId"] = gbId
        args["level"] = level
        args["invokeTime"] = invokeTime
        args["expireTime"] = expireTime
        LogTrackingMgr.LOG(args)

    # 收集事件
    @staticmethod
    def Collectible_Detail(gbId, collectId, status, propChange):
        args = {}
        args["trackName"] = "Collectible_Detail"
        args["gbId"] = gbId
        args["collectId"] = collectId
        args["status"] = status
        args["propChange"] = propChange
        LogTrackingMgr.LOG(args)

    # 抽卡事件
    @staticmethod
    def DrawCard_Detail(gbId, poolId, poolGroupId, rollCost, realRollNum, itemList, befPityNum, aftPityNum, pityPullNum, befGuaranteed, aftGuaranteed, guaranteedType):
        args = {}
        args["trackName"] = "DrawCard_Detail"
        args["gbId"] = gbId
        args["poolId"] = poolId
        args["poolGroupId"] = poolGroupId
        args["rollCost"] = rollCost
        args["realRollNum"] = realRollNum
        args["itemList"] = itemList
        args["befPityNum"] = befPityNum
        args["aftPityNum"] = aftPityNum
        args["pityPullNum"] = pityPullNum
        args["befGuaranteed"] = befGuaranteed
        args["aftGuaranteed"] = aftGuaranteed
        args["guaranteedType"] = guaranteedType
        LogTrackingMgr.LOG(args)

    # 抽卡保底
    @staticmethod
    def DrawCard_GuaranteedReward(gbId, poolId, poolGroupId, pityReward, guaranteed, guaranteedType):
        args = {}
        args["trackName"] = "DrawCard_GuaranteedReward"
        args["gbId"] = gbId
        args["poolId"] = poolId
        args["poolGroupId"] = poolGroupId
        args["pityReward"] = pityReward
        args["guaranteed"] = guaranteed
        args["guaranteedType"] = guaranteedType
        LogTrackingMgr.LOG(args)

    @staticmethod
    def LOG(args):
        logData = {
            'server': gameconfig.serverId(),
            'log_id': "LogTracking",
            'sentTimestamp': utils.getTimestamp64(),
            'gameId': gameconfig.gameId(),
        }
        logData.update(args)
        gamelog.TLOG("", json.dumps(logData), True)
