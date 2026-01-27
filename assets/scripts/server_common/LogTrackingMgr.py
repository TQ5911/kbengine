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
    def Server_Logout(accountId, deviceModel, ipAddress, operatingSystem, channelSource, packageSource):
        args = {}
        args["trackName"] = "Server_Logout"
        args["accountId"] = accountId
        args["deviceModel"] = deviceModel
        args["ipAddress"] = ipAddress
        args["operatingSystem"] = operatingSystem
        args["channelSource"] = channelSource
        args["packageSource"] = packageSource
        LogTrackingMgr.LOG(args)

    # 用户登录事件
    @staticmethod
    def Server_Login(accountId, deviceModel, ipAddress, operatingSystem, accountType, channelSource, packageSource):
        args = {}
        args["trackName"] = "Server_Login"
        args["accountId"] = accountId
        args["deviceModel"] = deviceModel
        args["ipAddress"] = ipAddress
        args["operatingSystem"] = operatingSystem
        args["accountType"] = accountType
        args["channelSource"] = channelSource
        args["packageSource"] = packageSource
        LogTrackingMgr.LOG(args)

    # 角色登录事件
    @staticmethod
    def Server_Role_Login(accountId, gbId, school, name, level, gameId, userInfoId, createTimestamp, accountType, channelSource, packageSource):
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
        args["packageSource"] = packageSource
        LogTrackingMgr.LOG(args)

    # 角色登出事件
    @staticmethod
    def Server_Role_Logout(accountId, gbId, school, name, level, packageSource):
        args = {}
        args["trackName"] = "Server_Role_Logout"
        args["accountId"] = accountId
        args["gbId"] = gbId
        args["school"] = school
        args["name"] = name
        args["level"] = level
        args["packageSource"] = packageSource
        LogTrackingMgr.LOG(args)

    # 创建角色事件
    @staticmethod
    def Server_Create_Role(accountId, gbId, school, name, gameId, userInfoId, createTimestamp, packageSource):
        args = {}
        args["trackName"] = "Server_Create_Role"
        args["accountId"] = accountId
        args["gbId"] = gbId
        args["school"] = school
        args["name"] = name
        args["gameId"] = gameId
        args["userInfoId"] = userInfoId
        args["createTimestamp"] = createTimestamp
        args["packageSource"] = packageSource
        LogTrackingMgr.LOG(args)

    # 合成道具事件
    @staticmethod
    def Synthesis_Item(costItemID, costItemNum, costCurrencyID, costCurrencyNum, getID, getNum, getQuality, desc, opUUID):
        args = {}
        args["trackName"] = "Synthesis_Item"
        args["costItemID"] = costItemID
        args["costItemNum"] = costItemNum
        args["costCurrencyID"] = costCurrencyID
        args["costCurrencyNum"] = costCurrencyNum
        args["getID"] = getID
        args["getNum"] = getNum
        args["getQuality"] = getQuality
        args["desc"] = desc
        args["opUUID"] = opUUID
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
    def MineBattle_End(activityEndTime, mapId, coreBelongGuildID, coreBelongTime):
        args = {}
        args["trackName"] = "MineBattle_End"
        args["activityEndTime"] = activityEndTime
        args["mapId"] = mapId
        args["coreBelongGuildID"] = coreBelongGuildID
        args["coreBelongTime"] = coreBelongTime
        LogTrackingMgr.LOG(args)

    # 矿战结束后奖励事件
    @staticmethod
    def MineBattle_End_Reward(activityEndTime, mapId, activityRank):
        args = {}
        args["trackName"] = "MineBattle_End_Reward"
        args["activityEndTime"] = activityEndTime
        args["mapId"] = mapId
        args["activityRank"] = activityRank
        LogTrackingMgr.LOG(args)

    # 矿战分红事件
    @staticmethod
    def MineBattle_Shared(miningAreaBelongGuildID, miningAreaOutput, dividendedPlayerID, dividendedCurrencyNum, opUUID):
        args = {}
        args["trackName"] = "MineBattle_Shared"
        args["miningAreaBelongGuildID"] = miningAreaBelongGuildID
        args["miningAreaOutput"] = miningAreaOutput
        args["dividendedPlayerID"] = dividendedPlayerID
        args["dividendedCurrencyNum"] = dividendedCurrencyNum
        args["opUUID"] = opUUID
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
    def Skill_Upgrade(ID, costItemID, costItemNum, costCurrencyID, costCurrencyNum, level, opUUID):
        args = {}
        args["trackName"] = "Skill_Upgrade"
        args["ID"] = ID
        args["costItemID"] = costItemID
        args["costItemNum"] = costItemNum
        args["costCurrencyID"] = costCurrencyID
        args["costCurrencyNum"] = costCurrencyNum
        args["level"] = level
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args)

    # 发红包事件
    @staticmethod
    def Release_RedBag(sendType, sendChannel, sendNumber, sendCostItemID, sendCostItemNum, opUUID):
        args = {}
        args["trackName"] = "Release_RedBag"
        args["sendType"] = sendType
        args["sendChannel"] = sendChannel
        args["sendNumber"] = sendNumber
        args["sendCostItemID"] = sendCostItemID
        args["sendCostItemNum"] = sendCostItemNum
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args)

    # 领红包事件
    @staticmethod
    def Fetch_RedBag(getType, getChannel, getItemID, getItemNum, claimedRemainNumber, claimedRemainItemID, claimedRemainItemNum, opUUID):
        args = {}
        args["trackName"] = "Fetch_RedBag"
        args["getType"] = getType
        args["getChannel"] = getChannel
        args["getItemID"] = getItemID
        args["getItemNum"] = getItemNum
        args["claimedRemainNumber"] = claimedRemainNumber
        args["claimedRemainItemID"] = claimedRemainItemID
        args["claimedRemainItemNum"] = claimedRemainItemNum
        args["opUUID"] = opUUID
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
        args["state"] = state # 1:新增 2.完成 3.领取
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

    # 装备制造
    @staticmethod
    def Equip_Make(opUUID, gbId, uniqueId, equipId, count, grade, quality, bindValue, makeType, baseAttrs, upgradeAttrs, enhanceAttrs, score):
        args = {}
        args["trackName"] = "Equip_Make"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["uniqueId"] = uniqueId
        args["equipId"] = equipId
        args["count"] = count
        args["grade"] = grade
        args["quality"] = quality
        args["bindValue"] = bindValue
        args["makeType"] = makeType
        args["baseAttrs"] = baseAttrs
        args["upgradeAttrs"] = upgradeAttrs
        args["enhanceAttrs"] = enhanceAttrs
        args["score"] = score
        LogTrackingMgr.LOG(args)

    # 装备强化
    @staticmethod
    def Equip_Enhancement(opUUID, gbId, uniqueId, equipId, equipBelongTo, baseAttrsBefore, enhanceAttrsBefore, upgradeAttrsBefore, baseAttrsAfter, enhanceAttrsAfter, upgradeAttrsAfter, addBindValueBefore, addBindValueAfter, consumedItemBindValue, levelBefore, levelAfter, result, score):
        args = {}
        args["trackName"] = "Equip_Enhancement"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["uniqueId"] = uniqueId
        args["equipId"] = equipId
        args["equipBelongTo"] = equipBelongTo
        args["baseAttrsBefore"] = baseAttrsBefore
        args["enhanceAttrsBefore"] = enhanceAttrsBefore
        args["upgradeAttrsBefore"] = upgradeAttrsBefore
        args["baseAttrsAfter"] = baseAttrsAfter
        args["enhanceAttrsAfter"] = enhanceAttrsAfter
        args["upgradeAttrsAfter"] = upgradeAttrsAfter
        args["addBindValueBefore"] = addBindValueBefore
        args["addBindValueAfter"] = addBindValueAfter
        args["consumedItemBindValue"] = consumedItemBindValue
        args["levelBefore"] = levelBefore
        args["levelAfter"] = levelAfter
        args["result"] = result
        args["score"] = score
        LogTrackingMgr.LOG(args)

    # 装备附灵
    @staticmethod
    def Equip_Spirit(opUUID, gbId, uniqueId, equipId, equipBelongTo, spiritDataBefore, spiritDataAfter, addBindValueBefore, addBindValueAfter, consumedItemBindValue, score):
        args = {}
        args["trackName"] = "Equip_Spirit"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["uniqueId"] = uniqueId
        args["equipId"] = equipId
        args["equipBelongTo"] = equipBelongTo
        args["spiritDataBefore"] = spiritDataBefore
        args["spiritDataAfter"] = spiritDataAfter
        args["addBindValueBefore"] = addBindValueBefore
        args["addBindValueAfter"] = addBindValueAfter
        args["consumedItemBindValue"] = consumedItemBindValue
        args["score"] = score
        LogTrackingMgr.LOG(args)

    # 装备升阶
    @staticmethod
    def Equip_Upgrade(opUUID, gbId, uniqueId, equipId, equipBelongTo, baseAttrsBefore, enhanceAttrsBefore, upgradeAttrsBefore, baseAttrsAfter, enhanceAttrsAfter, upgradeAttrsAfter, gradeBefore, gradeAfter, bindValue, originalBindValue, score):
        args = {}
        args["trackName"] = "Equip_Upgrade"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["uniqueId"] = uniqueId
        args["equipId"] = equipId
        args["equipBelongTo"] = equipBelongTo
        args["baseAttrsBefore"] = baseAttrsBefore
        args["enhanceAttrsBefore"] = enhanceAttrsBefore
        args["upgradeAttrsBefore"] = upgradeAttrsBefore
        args["baseAttrsAfter"] = baseAttrsAfter
        args["enhanceAttrsAfter"] = enhanceAttrsAfter
        args["upgradeAttrsAfter"] = upgradeAttrsAfter
        args["gradeBefore"] = gradeBefore
        args["gradeAfter"] = gradeAfter
        args["bindValue"] = bindValue
        args["originalBindValue"] = originalBindValue
        args["score"] = score
        LogTrackingMgr.LOG(args)

    # 装备铭文
    @staticmethod
    def Equip_Glyph(opUUID, gbId, uniqueId, equipId, equipBelongTo, glyphDataBefore, glyphDataAfter, addBindValueBefore, addBindValueAfter, consumedItemBindValue, score):
        args = {}
        args["trackName"] = "Equip_Glyph"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["uniqueId"] = uniqueId
        args["equipId"] = equipId
        args["equipBelongTo"] = equipBelongTo
        args["glyphDataBefore"] = glyphDataBefore
        args["glyphDataAfter"] = glyphDataAfter
        args["addBindValueBefore"] = addBindValueBefore
        args["addBindValueAfter"] = addBindValueAfter
        args["consumedItemBindValue"] = consumedItemBindValue
        args["score"] = score
        LogTrackingMgr.LOG(args)

    # 装备祝福
    @staticmethod
    def Equip_Bless(opUUID, gbId, uniqueId, equipId, equipBelongTo, blessDataBefore, blessDataAfter, addBindValueBefore, addBindValueAfter, consumedItemBindValue, blessLvRateBefore, blessLvRateAfter, maxBlessLvBefore, maxBlessLvAfter, score):
        args = {}
        args["trackName"] = "Equip_Bless"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["uniqueId"] = uniqueId
        args["equipId"] = equipId
        args["equipBelongTo"] = equipBelongTo
        args["blessDataBefore"] = blessDataBefore
        args["blessDataAfter"] = blessDataAfter
        args["addBindValueBefore"] = addBindValueBefore
        args["addBindValueAfter"] = addBindValueAfter
        args["consumedItemBindValue"] = consumedItemBindValue
        args["blessLvRateBefore"] = blessLvRateBefore
        args["blessLvRateAfter"] = blessLvRateAfter
        args["maxBlessLvBefore"] = maxBlessLvBefore
        args["maxBlessLvAfter"] = maxBlessLvAfter
        args["score"] = score
        LogTrackingMgr.LOG(args)

    # 装备绑定值洗涤
    @staticmethod
    def Equip_BindValue_Washing(opUUID, gbId, uniqueId, equipId, equipBelongTo, bindValueWashingBefore, bindValueWashingAfter, addBindValueStatusBefore, addBindValueStatusAfter, washCount):
        args = {}
        args["trackName"] = "Equip_BindValue_Washing"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["uniqueId"] = uniqueId
        args["equipId"] = equipId
        args["equipBelongTo"] = equipBelongTo
        args["bindValueWashingBefore"] = bindValueWashingBefore
        args["bindValueWashingAfter"] = bindValueWashingAfter
        args["addBindValueStatusBefore"] = addBindValueStatusBefore
        args["addBindValueStatusAfter"] = addBindValueStatusAfter
        args["washCount"] = washCount
        LogTrackingMgr.LOG(args)

    # 道具工坊
    @staticmethod
    def Work_Shop(opUUID, gbId, normalItems, luckyItems):
        args = {}
        args["trackName"] = "Work_Shop"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["normalItems"] = normalItems
        args["luckyItems"] = luckyItems
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
    def Collectible_Detail(gbId, collectId, status, propChange, opUUID):
        args = {}
        args["trackName"] = "Collectible_Detail"
        args["gbId"] = gbId
        args["collectId"] = collectId
        args["status"] = status
        args["propChange"] = propChange
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args)

    # 抽卡事件
    @staticmethod
    def DrawCard_Detail(gbId, poolId, poolGroupId, rollCost, realRollNum, itemList, befPityNum, aftPityNum, pityPullNum, befGuaranteed, aftGuaranteed, guaranteedType, opUUID):
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
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args)

    # 抽卡保底
    @staticmethod
    def DrawCard_GuaranteedReward(gbId, poolId, poolGroupId, pityReward, guaranteed, guaranteedType, opUUID):
        args = {}
        args["trackName"] = "DrawCard_GuaranteedReward"
        args["gbId"] = gbId
        args["poolId"] = poolId
        args["poolGroupId"] = poolGroupId
        args["pityReward"] = pityReward
        args["guaranteed"] = guaranteed
        args["guaranteedType"] = guaranteedType
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args)

    # 采集事件
    @staticmethod
    def Gather_Collection(gbId, collectionId, collectionType, startTime, endTime, opUUID):
        args = {}
        args["trackName"] = "Gather_Collection"
        args["gbId"] = gbId
        args["collectionId"] = collectionId
        args["collectionType"] = collectionType
        args["startTime"] = startTime
        args["endTime"] = endTime
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args)

    # 帮会副本开启
    @staticmethod
    def Guild_BossChallenge_Open(opUUID, guildUUID, openType, consumeType, consumeCount, openDungeonId, openTime, openedMoneyCount, openedFundCount):
        args = {}
        args["trackName"] = "Guild_BossChallenge_Open"
        args["opUUID"] = opUUID
        args["guildUUID"] = guildUUID
        args["openType"] = openType
        args["consumeType"] = consumeType
        args["consumeCount"] = consumeCount
        args["openDungeonId"] = openDungeonId
        args["openTime"] = openTime
        args["openedMoneyCount"] = openedMoneyCount
        args["openedFundCount"] = openedFundCount
        LogTrackingMgr.LOG(args)

    # 帮会副本取消开启
    @staticmethod
    def Guild_BossChallenge_Cancel(opUUID, guildUUID, cancelType, consumeType, consumeCount, openDungeonId, openTime, openedMoneyCount, openedFundCount):
        args = {}
        args["trackName"] = "Guild_BossChallenge_Cancel"
        args["opUUID"] = opUUID
        args["guildUUID"] = guildUUID
        args["cancelType"] = cancelType
        args["consumeType"] = consumeType
        args["consumeCount"] = consumeCount
        args["openDungeonId"] = openDungeonId
        args["openTime"] = openTime
        args["openedMoneyCount"] = openedMoneyCount
        args["openedFundCount"] = openedFundCount
        LogTrackingMgr.LOG(args)

    # 帮会副本恢复回退
    @staticmethod
    def Guild_BossChallenge_Recover(opUUID, guildUUID, cancelType, consumeType, consumeCount, openDungeonId, openTime, openedMoneyCount, openedFundCount):
        args = {}
        args["trackName"] = "Guild_BossChallenge_Recover"
        args["opUUID"] = opUUID
        args["guildUUID"] = guildUUID
        args["cancelType"] = cancelType
        args["consumeType"] = consumeType
        args["consumeCount"] = consumeCount
        args["openDungeonId"] = openDungeonId
        args["openTime"] = openTime
        args["openedMoneyCount"] = openedMoneyCount
        args["openedFundCount"] = openedFundCount
        LogTrackingMgr.LOG(args)

    # 帮会副本创建
    @staticmethod
    def Guild_BossChallenge_CreateDungeon(opUUID):
        args = {}
        args["trackName"] = "Guild_BossChallenge_CreateDungeon"
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args)

    # 帮会副本倒计时开启
    @staticmethod
    def Guild_BossChallenge_CDOpen(opUUID):
        args = {}
        args["trackName"] = "Guild_BossChallenge_CDOpen"
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args)

    # 帮会副本副本结算
    @staticmethod
    def Guild_BossChallenge_Settlement(opUUID, gbId, isClear, dmgScore, dmgRank, isFirstClear, firstPassRewards, rankRewards):
        args = {}
        args["trackName"] = "Guild_BossChallenge_Settlement"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["isClear"] = isClear
        args["dmgScore"] = dmgScore
        args["dmgRank"] = dmgRank
        args["isFirstClear"] = isFirstClear
        args["firstPassRewards"] = firstPassRewards
        args["rankRewards"] = rankRewards
        LogTrackingMgr.LOG(args)

    # 扩容（背包或者仓库）
    @staticmethod
    def Capacity_Expansion(opUUID, gbId, type, capacityBefore, expansionCount, capacityAfter, playerLevel, consumeItems):
        args = {}
        args["trackName"] = "Capacity_Expansion"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["type"] = type
        args["capacityBefore"] = capacityBefore
        args["expansionCount"] = expansionCount
        args["capacityAfter"] = capacityAfter
        args["playerLevel"] = playerLevel
        args["consumeItems"] = consumeItems
        LogTrackingMgr.LOG(args)

    # 道具或者装备分解
    @staticmethod
    def Item_Disassembly(opUUID, gbId, type, disassembleItems, rewardItems, disassembleSettings):
        args = {}
        args["trackName"] = "Item_Disassembly"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["type"] = type
        args["disassembleItems"] = disassembleItems
        args["rewardItems"] = rewardItems
        args["disassembleSettings"] = disassembleSettings
        LogTrackingMgr.LOG(args)

    # 任务状态变更
    @staticmethod
    def Task_State_Change(gbId, taskId, taskState, taskType, taskMap, playerLevel):
        args = {}
        args["trackName"] = "Task_State_Change"
        args["gbId"] = gbId
        args["taskId"] = taskId
        args["taskState"] = taskState
        args["taskType"] = taskType
        args["taskMap"] = taskMap
        args["playerLevel"] = playerLevel
        LogTrackingMgr.LOG(args)

    # pc引流奖励
    @staticmethod
    def Welfare_PcDrainage(accountId, gbId, deviceModel, claimTimestamp, opUUID):
        args = {}
        args["trackName"] = "Welfare_PcDrainage"
        args["accountId"] = accountId
        args["gbId"] = gbId
        args["deviceModel"] = deviceModel
        args["claimTimestamp"] = claimTimestamp
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args)

    # 副本门票消耗
    @staticmethod
    def Dungeon_Ticket_Consume(uniqueId, dungeonType, dungeonId, ticketType, enterType, playerCount, gbId, score, playerLevel):
        args = {}
        args["trackName"] = "Dungeon_Ticket_Consume"
        args["uniqueId"] = uniqueId
        args["dungeonType"] = dungeonType
        args["dungeonId"] = dungeonId
        args["ticketType"] = ticketType
        args["enterType"] = enterType
        args["playerCount"] = playerCount
        args["gbId"] = gbId
        args["score"] = score
        args["playerLevel"] = playerLevel
        LogTrackingMgr.LOG(args)

    # Boss出生
    @staticmethod
    def Dungeon_Boss_Born(uniqueId, dungeonType, dungeonId, spaceUUID, spaceNo, monsterId, bornTime, dungeonStartTime):
        args = {}
        args["trackName"] = "Dungeon_Boss_Born"
        args["uniqueId"] = uniqueId
        args["dungeonType"] = dungeonType
        args["dungeonId"] = dungeonId
        args["spaceUUID"] = spaceUUID
        args["spaceNo"] = spaceNo
        args["monsterId"] = monsterId
        args["bornTime"] = bornTime
        args["dungeonStartTime"] = dungeonStartTime
        LogTrackingMgr.LOG(args)

    # Boss死亡
    @staticmethod
    def Dungeon_Boss_Dead(uniqueId, dungeonType, dungeonId, spaceUUID, spaceNo, monsterId, bornTime, deadTime, dungeonStartTime):
        args = {}
        args["trackName"] = "Dungeon_Boss_Dead"
        args["uniqueId"] = uniqueId
        args["dungeonType"] = dungeonType
        args["dungeonId"] = dungeonId
        args["spaceUUID"] = spaceUUID
        args["spaceNo"] = spaceNo
        args["monsterId"] = monsterId
        args["bornTime"] = bornTime
        args["deadTime"] = deadTime
        args["dungeonStartTime"] = dungeonStartTime
        LogTrackingMgr.LOG(args)

    # 副本结算
    @staticmethod
    def Dungeon_Settlement(uniqueId, dungeonType, dungeonId, spaceUUID, spaceNo, gbId, isClear, isFirstClear, finishTime, isWin, reasonType, finishedPlayerCount, deadCount, firstRewards, clearRewards, goldRewards, autoBattleTimes, playerScore, playerLevel):
        args = {}
        args["trackName"] = "Dungeon_Settlement"
        args["uniqueId"] = uniqueId
        args["dungeonType"] = dungeonType
        args["dungeonId"] = dungeonId
        args["spaceUUID"] = spaceUUID
        args["spaceNo"] = spaceNo
        args["gbId"] = gbId
        args["isClear"] = isClear
        args["isFirstClear"] = isFirstClear
        args["finishTime"] = finishTime
        args["isWin"] = isWin
        args["reasonType"] = reasonType
        args["finishedPlayerCount"] = finishedPlayerCount
        args["deadCount"] = deadCount
        args["firstRewards"] = firstRewards
        args["clearRewards"] = clearRewards
        args["goldRewards"] = goldRewards
        args["autoBattleTimes"] = autoBattleTimes
        args["playerScore"] = playerScore
        args["playerLevel"] = playerLevel
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
