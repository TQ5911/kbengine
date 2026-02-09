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
    def Server_Recharge_Complete(accountId, roleId, itemType, itemId, price, orderId, **kwargs):
        args = {}
        args["trackName"] = "Server_Recharge_Complete"
        args["accountId"] = str(accountId)
        args["roleId"] = str(roleId)
        args["itemType"] = str(itemType)
        args["itemId"] = str(itemId)
        args["price"] = price
        args["orderId"] = str(orderId)
        LogTrackingMgr.LOG(args, kwargs)

    # PCU事件
    @staticmethod
    def Server_Pcu(pcu, **kwargs):
        args = {}
        args["trackName"] = "Server_Pcu"
        args["pcu"] = pcu
        LogTrackingMgr.LOG(args, kwargs)

    # 用户登出事件
    @staticmethod
    def Server_Logout(accountId, deviceModel, ipAddress, operatingSystem, channelSource, packageSource, **kwargs):
        args = {}
        args["trackName"] = "Server_Logout"
        args["accountId"] = str(accountId)
        args["deviceModel"] = str(deviceModel)
        args["ipAddress"] = str(ipAddress)
        args["operatingSystem"] = str(operatingSystem)
        args["channelSource"] = str(channelSource)
        args["packageSource"] = str(packageSource)
        LogTrackingMgr.LOG(args, kwargs)

    # 用户登录事件
    @staticmethod
    def Server_Login(accountId, deviceModel, ipAddress, operatingSystem, accountType, channelSource, packageSource, **kwargs):
        args = {}
        args["trackName"] = "Server_Login"
        args["accountId"] = str(accountId)
        args["deviceModel"] = str(deviceModel)
        args["ipAddress"] = str(ipAddress)
        args["operatingSystem"] = str(operatingSystem)
        args["accountType"] = str(accountType)
        args["channelSource"] = str(channelSource)
        args["packageSource"] = str(packageSource)
        LogTrackingMgr.LOG(args, kwargs)

    # 角色登录事件
    @staticmethod
    def Server_Role_Login(accountId, gbId, school, name, level, gameId, userInfoId, createTimestamp, accountType, channelSource, packageSource, **kwargs):
        args = {}
        args["trackName"] = "Server_Role_Login"
        args["accountId"] = str(accountId)
        args["gbId"] = gbId
        args["school"] = school
        args["name"] = str(name)
        args["level"] = level
        args["gameId"] = str(gameId)
        args["userInfoId"] = str(userInfoId)
        args["createTimestamp"] = createTimestamp
        args["accountType"] = str(accountType)
        args["channelSource"] = str(channelSource)
        args["packageSource"] = str(packageSource)
        LogTrackingMgr.LOG(args, kwargs)

    # 角色登出事件
    @staticmethod
    def Server_Role_Logout(accountId, gbId, school, name, level, packageSource, **kwargs):
        args = {}
        args["trackName"] = "Server_Role_Logout"
        args["accountId"] = str(accountId)
        args["gbId"] = gbId
        args["school"] = school
        args["name"] = str(name)
        args["level"] = level
        args["packageSource"] = str(packageSource)
        LogTrackingMgr.LOG(args, kwargs)

    # 创建角色事件
    @staticmethod
    def Server_Create_Role(accountId, gbId, school, name, gameId, userInfoId, createTimestamp, packageSource, faceId, faceColorId, hairId, hairColorId, **kwargs):
        args = {}
        args["trackName"] = "Server_Create_Role"
        args["accountId"] = str(accountId)
        args["gbId"] = gbId
        args["school"] = school
        args["name"] = str(name)
        args["gameId"] = str(gameId)
        args["userInfoId"] = str(userInfoId)
        args["createTimestamp"] = createTimestamp
        args["packageSource"] = str(packageSource)
        args["faceId"] = faceId
        args["faceColorId"] = faceColorId
        args["hairId"] = hairId
        args["hairColorId"] = hairColorId
        LogTrackingMgr.LOG(args, kwargs)

    # 善恶值变化事件
    @staticmethod
    def Moral_Change(gbId, moral, delta, srcType, **kwargs):
        args = {}
        args["trackName"] = "Moral_Change"
        args["gbId"] = gbId
        args["moral"] = moral
        args["delta"] = delta
        args["srcType"] = srcType
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会排行榜
    @staticmethod
    def LeaderBoard_Guild(type, rank, guildUUID, guildName, guildLevel, guildScore, **kwargs):
        args = {}
        args["trackName"] = "LeaderBoard_Guild"
        args["type"] = type
        args["rank"] = rank
        args["guildUUID"] = guildUUID
        args["guildName"] = str(guildName)
        args["guildLevel"] = guildLevel
        args["guildScore"] = guildScore
        LogTrackingMgr.LOG(args, kwargs)

    # 玩家等级排行榜
    @staticmethod
    def LeaderBoard_Level(type, rank, gbId, name, level, school, guildUUID, guildName, **kwargs):
        args = {}
        args["trackName"] = "LeaderBoard_Level"
        args["type"] = type
        args["rank"] = rank
        args["gbId"] = gbId
        args["name"] = str(name)
        args["level"] = level
        args["school"] = school
        args["guildUUID"] = guildUUID
        args["guildName"] = str(guildName)
        LogTrackingMgr.LOG(args, kwargs)

    # 玩家其他排行榜
    @staticmethod
    def LeaderBoard_Avatar(type, rank, gbId, name, level, score, school, guildUUID, guildName, **kwargs):
        args = {}
        args["trackName"] = "LeaderBoard_Avatar"
        args["type"] = type
        args["rank"] = rank
        args["gbId"] = gbId
        args["name"] = str(name)
        args["level"] = level
        args["score"] = score
        args["school"] = school
        args["guildUUID"] = guildUUID
        args["guildName"] = str(guildName)
        LogTrackingMgr.LOG(args, kwargs)

    # 合成道具事件
    @staticmethod
    def Synthesis_Item(gbId, costItemID, costItemNum, costCurrencyID, costCurrencyNum, getID, getNum, getQuality, desc, opUUID, **kwargs):
        args = {}
        args["trackName"] = "Synthesis_Item"
        args["gbId"] = gbId
        args["costItemID"] = str(costItemID)
        args["costItemNum"] = costItemNum
        args["costCurrencyID"] = str(costCurrencyID)
        args["costCurrencyNum"] = costCurrencyNum
        args["getID"] = str(getID)
        args["getNum"] = getNum
        args["getQuality"] = getQuality
        args["desc"] = str(desc)
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 矿战开启事件
    @staticmethod
    def MineBattle_Start(activityStartTime, coreBelongGuildID, **kwargs):
        args = {}
        args["trackName"] = "MineBattle_Start"
        args["activityStartTime"] = str(activityStartTime)
        args["coreBelongGuildID"] = str(coreBelongGuildID)
        LogTrackingMgr.LOG(args, kwargs)

    # 矿战结束事件
    @staticmethod
    def MineBattle_End(activityEndTime, mapId, coreBelongGuildID, coreBelongTime, **kwargs):
        args = {}
        args["trackName"] = "MineBattle_End"
        args["activityEndTime"] = str(activityEndTime)
        args["mapId"] = str(mapId)
        args["coreBelongGuildID"] = str(coreBelongGuildID)
        args["coreBelongTime"] = str(coreBelongTime)
        LogTrackingMgr.LOG(args, kwargs)

    # 矿战结束后奖励事件
    @staticmethod
    def MineBattle_End_Reward(activityEndTime, mapId, activityRank, **kwargs):
        args = {}
        args["trackName"] = "MineBattle_End_Reward"
        args["activityEndTime"] = str(activityEndTime)
        args["mapId"] = str(mapId)
        args["activityRank"] = str(activityRank)
        LogTrackingMgr.LOG(args, kwargs)

    # 矿战分红事件
    @staticmethod
    def MineBattle_Shared(gbId, miningAreaBelongGuildID, miningAreaOutput, dividendedPlayerID, dividendedCurrencyNum, opUUID, **kwargs):
        args = {}
        args["trackName"] = "MineBattle_Shared"
        args["gbId"] = gbId
        args["miningAreaBelongGuildID"] = str(miningAreaBelongGuildID)
        args["miningAreaOutput"] = str(miningAreaOutput)
        args["dividendedPlayerID"] = str(dividendedPlayerID)
        args["dividendedCurrencyNum"] = dividendedCurrencyNum
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 矿战击杀旗帜事件
    @staticmethod
    def MineBattle_KillFlag(mapId, killerGuildID, gbId, flagDeathTimes, **kwargs):
        args = {}
        args["trackName"] = "MineBattle_KillFlag"
        args["mapId"] = str(mapId)
        args["killerGuildID"] = str(killerGuildID)
        args["gbId"] = gbId
        args["flagDeathTimes"] = str(flagDeathTimes)
        LogTrackingMgr.LOG(args, kwargs)

    # 好友操作事件
    @staticmethod
    def Friend_Opr(gbId, otherGbId, friendNum, opr, otherSchool, otherScore, **kwargs):
        args = {}
        args["trackName"] = "Friend_Opr"
        args["gbId"] = gbId
        args["otherGbId"] = otherGbId
        args["friendNum"] = friendNum
        args["opr"] = opr
        args["otherSchool"] = otherSchool
        args["otherScore"] = otherScore
        LogTrackingMgr.LOG(args, kwargs)

    # 技能升级事件
    @staticmethod
    def Skill_Upgrade(gbId, ID, costItemID, costItemNum, costCurrencyID, costCurrencyNum, level, opUUID, **kwargs):
        args = {}
        args["trackName"] = "Skill_Upgrade"
        args["gbId"] = gbId
        args["ID"] = str(ID)
        args["costItemID"] = costItemID
        args["costItemNum"] = costItemNum
        args["costCurrencyID"] = str(costCurrencyID)
        args["costCurrencyNum"] = costCurrencyNum
        args["level"] = level
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 发红包事件
    @staticmethod
    def Release_RedBag(gbId, sendType, sendChannel, sendNumber, sendCostItemID, sendCostItemNum, opUUID, **kwargs):
        args = {}
        args["trackName"] = "Release_RedBag"
        args["gbId"] = gbId
        args["sendType"] = sendType
        args["sendChannel"] = sendChannel
        args["sendNumber"] = sendNumber
        args["sendCostItemID"] = str(sendCostItemID)
        args["sendCostItemNum"] = sendCostItemNum
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 领红包事件
    @staticmethod
    def Fetch_RedBag(gbId, getType, getChannel, getItemID, getItemNum, claimedRemainNumber, claimedRemainItemID, claimedRemainItemNum, opUUID, **kwargs):
        args = {}
        args["trackName"] = "Fetch_RedBag"
        args["gbId"] = gbId
        args["getType"] = getType
        args["getChannel"] = getChannel
        args["getItemID"] = str(getItemID)
        args["getItemNum"] = getItemNum
        args["claimedRemainNumber"] = claimedRemainNumber
        args["claimedRemainItemID"] = str(claimedRemainItemID)
        args["claimedRemainItemNum"] = claimedRemainItemNum
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 退还红包事件
    @staticmethod
    def Return_RedBag(gbId, opUUID, **kwargs):
        args = {}
        args["trackName"] = "Return_RedBag"
        args["gbId"] = gbId
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 公会信息事件
    @staticmethod
    def Guild_Info(guildUUID, level, guildExp, fundNum, goldNum, tokenNum, src, opUUID, desc, **kwargs):
        args = {}
        args["trackName"] = "Guild_Info"
        args["guildUUID"] = guildUUID
        args["level"] = level
        args["guildExp"] = guildExp
        args["fundNum"] = fundNum
        args["goldNum"] = goldNum
        args["tokenNum"] = tokenNum
        args["src"] = src
        args["opUUID"] = opUUID
        args["desc"] = str(desc)
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会操作相关
    @staticmethod
    def Guild_Opr(guildUUID, gbId, guildMemberNum, guildLevel, operation, **kwargs):
        args = {}
        args["trackName"] = "Guild_Opr"
        args["guildUUID"] = guildUUID
        args["gbId"] = gbId
        args["guildMemberNum"] = guildMemberNum
        args["guildLevel"] = guildLevel
        args["operation"] = operation
        LogTrackingMgr.LOG(args, kwargs)

    # 公会练功场重置
    @staticmethod
    def Guild_Train_Reset(gbId, **kwargs):
        args = {}
        args["trackName"] = "Guild_Train_Reset"
        args["gbId"] = gbId
        LogTrackingMgr.LOG(args, kwargs)

    # 公会练功场事件
    @staticmethod
    def Guild_Train(gbId, trainId, trainLevel, trainProp, **kwargs):
        args = {}
        args["trackName"] = "Guild_Train"
        args["gbId"] = gbId
        args["trainId"] = trainId
        args["trainLevel"] = trainLevel
        args["trainProp"] = str(trainProp)
        LogTrackingMgr.LOG(args, kwargs)

    # 公会任务事件
    @staticmethod
    def Guild_Task(gbId, taskId, taskProgress, taskState, **kwargs):
        args = {}
        args["trackName"] = "Guild_Task"
        args["gbId"] = gbId
        args["taskId"] = taskId
        args["taskProgress"] = taskProgress
        args["taskState"] = taskState
        LogTrackingMgr.LOG(args, kwargs)

    # 公会商店事件
    @staticmethod
    def Guild_Shop(shopSellItemId, shopSellTimes, **kwargs):
        args = {}
        args["trackName"] = "Guild_Shop"
        args["shopSellItemId"] = str(shopSellItemId)
        args["shopSellTimes"] = shopSellTimes
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会聚义楼协助
    @staticmethod
    def Guild_Assist(guild_buildingID, srcGbId, guildUUID, guild_buildingLevel, exp, opUUID, src, **kwargs):
        args = {}
        args["trackName"] = "Guild_Assist"
        args["guild_buildingID"] = guild_buildingID
        args["srcGbId"] = srcGbId
        args["guildUUID"] = guildUUID
        args["guild_buildingLevel"] = guild_buildingLevel
        args["exp"] = exp
        args["opUUID"] = opUUID
        args["src"] = src
        LogTrackingMgr.LOG(args, kwargs)

    # 好友聊天事件
    @staticmethod
    def Friend_Msg(gbId, friendGbId, msg, isOnline, isFriend, **kwargs):
        args = {}
        args["trackName"] = "Friend_Msg"
        args["gbId"] = gbId
        args["friendGbId"] = friendGbId
        args["msg"] = str(msg)
        args["isOnline"] = isOnline
        args["isFriend"] = isFriend
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会军需处协助
    @staticmethod
    def Guild_QiXieAssist(guild_warEquipmentID, srcGbId, guildUUID, guild_warEquipmentLevel, exp, **kwargs):
        args = {}
        args["trackName"] = "Guild_QiXieAssist"
        args["guild_warEquipmentID"] = guild_warEquipmentID
        args["srcGbId"] = srcGbId
        args["guildUUID"] = guildUUID
        args["guild_warEquipmentLevel"] = guild_warEquipmentLevel
        args["exp"] = exp
        LogTrackingMgr.LOG(args, kwargs)

    # 魔方事件
    @staticmethod
    def Cube_Info(gbId, gameId, floor, mapId, cubeEvent, leftTime, **kwargs):
        args = {}
        args["trackName"] = "Cube_Info"
        args["gbId"] = gbId
        args["gameId"] = str(gameId)
        args["floor"] = floor
        args["mapId"] = mapId
        args["cubeEvent"] = cubeEvent
        args["leftTime"] = leftTime
        LogTrackingMgr.LOG(args, kwargs)

    # 仙境事件
    @staticmethod
    def Wonderland_Info(gbId, gameId, floor, wonderLandEvent, **kwargs):
        args = {}
        args["trackName"] = "Wonderland_Info"
        args["gbId"] = gbId
        args["gameId"] = str(gameId)
        args["floor"] = floor
        args["wonderLandEvent"] = wonderLandEvent
        LogTrackingMgr.LOG(args, kwargs)

    # 成就事件
    @staticmethod
    def Achievement_Update(accountId, gbId, gameId, achieveId, version, state, progress, **kwargs):
        args = {}
        args["trackName"] = "Achievement_Update"
        args["accountId"] = str(accountId)
        args["gbId"] = gbId
        args["gameId"] = str(gameId)
        args["achieveId"] = str(achieveId)
        args["version"] = str(version)
        args["state"] = state
        args["progress"] = progress
        LogTrackingMgr.LOG(args, kwargs)

    # 道具事件
    @staticmethod
    def Get_Item(accountId, gbId, gameId, itemId, uniqueId, bagType, bindType, delta, newNum, src, opUUID, desc, **kwargs):
        args = {}
        args["trackName"] = "Get_Item"
        args["accountId"] = str(accountId)
        args["gbId"] = gbId
        args["gameId"] = str(gameId)
        args["itemId"] = itemId
        args["uniqueId"] = uniqueId
        args["bagType"] = bagType
        args["bindType"] = bindType
        args["delta"] = delta
        args["newNum"] = newNum
        args["src"] = src
        args["opUUID"] = opUUID
        args["desc"] = str(desc)
        LogTrackingMgr.LOG(args, kwargs)

    # 通用死亡事件
    @staticmethod
    def Common_Death(gbId, mapId, killerGbId, killerType, deadPosition, **kwargs):
        args = {}
        args["trackName"] = "Common_Death"
        args["gbId"] = gbId
        args["mapId"] = mapId
        args["killerGbId"] = killerGbId
        args["killerType"] = str(killerType)
        args["deadPosition"] = str(deadPosition)
        LogTrackingMgr.LOG(args, kwargs)

    # 装备制造
    @staticmethod
    def Equip_Make(opUUID, gbId, uniqueId, equipId, count, grade, quality, bindValue, makeType, baseAttrs, upgradeAttrs, enhanceAttrs, score, **kwargs):
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
        args["baseAttrs"] = str(baseAttrs)
        args["upgradeAttrs"] = str(upgradeAttrs)
        args["enhanceAttrs"] = str(enhanceAttrs)
        args["score"] = score
        LogTrackingMgr.LOG(args, kwargs)

    # 装备强化
    @staticmethod
    def Equip_Enhancement(opUUID, gbId, uniqueId, equipId, equipBelongTo, baseAttrsBefore, enhanceAttrsBefore, upgradeAttrsBefore, baseAttrsAfter, enhanceAttrsAfter, upgradeAttrsAfter, addBindValueBefore, addBindValueAfter, consumedItemBindValue, levelBefore, levelAfter, result, score, bindValueBefore, bindValueAfter, **kwargs):
        args = {}
        args["trackName"] = "Equip_Enhancement"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["uniqueId"] = uniqueId
        args["equipId"] = equipId
        args["equipBelongTo"] = equipBelongTo
        args["baseAttrsBefore"] = str(baseAttrsBefore)
        args["enhanceAttrsBefore"] = str(enhanceAttrsBefore)
        args["upgradeAttrsBefore"] = str(upgradeAttrsBefore)
        args["baseAttrsAfter"] = str(baseAttrsAfter)
        args["enhanceAttrsAfter"] = str(enhanceAttrsAfter)
        args["upgradeAttrsAfter"] = str(upgradeAttrsAfter)
        args["addBindValueBefore"] = addBindValueBefore
        args["addBindValueAfter"] = addBindValueAfter
        args["consumedItemBindValue"] = consumedItemBindValue
        args["levelBefore"] = levelBefore
        args["levelAfter"] = levelAfter
        args["result"] = result
        args["score"] = score
        args["bindValueBefore"] = bindValueBefore
        args["bindValueAfter"] = bindValueAfter
        LogTrackingMgr.LOG(args, kwargs)

    # 装备附灵
    @staticmethod
    def Equip_Spirit(opUUID, gbId, uniqueId, equipId, equipBelongTo, spiritDataBefore, spiritDataAfter, addBindValueBefore, addBindValueAfter, consumedItemBindValue, score, refId, bindValueBefore, bindValueAfter, **kwargs):
        args = {}
        args["trackName"] = "Equip_Spirit"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["uniqueId"] = uniqueId
        args["equipId"] = equipId
        args["equipBelongTo"] = equipBelongTo
        args["spiritDataBefore"] = str(spiritDataBefore)
        args["spiritDataAfter"] = str(spiritDataAfter)
        args["addBindValueBefore"] = addBindValueBefore
        args["addBindValueAfter"] = addBindValueAfter
        args["consumedItemBindValue"] = consumedItemBindValue
        args["score"] = score
        args["refId"] = refId
        args["bindValueBefore"] = bindValueBefore
        args["bindValueAfter"] = bindValueAfter
        LogTrackingMgr.LOG(args, kwargs)

    # 装备升阶
    @staticmethod
    def Equip_Upgrade(opUUID, gbId, uniqueId, equipId, equipBelongTo, baseAttrsBefore, enhanceAttrsBefore, upgradeAttrsBefore, baseAttrsAfter, enhanceAttrsAfter, upgradeAttrsAfter, gradeBefore, gradeAfter, bindValueBefore, bindValueAfter, score, **kwargs):
        args = {}
        args["trackName"] = "Equip_Upgrade"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["uniqueId"] = uniqueId
        args["equipId"] = equipId
        args["equipBelongTo"] = equipBelongTo
        args["baseAttrsBefore"] = str(baseAttrsBefore)
        args["enhanceAttrsBefore"] = str(enhanceAttrsBefore)
        args["upgradeAttrsBefore"] = str(upgradeAttrsBefore)
        args["baseAttrsAfter"] = str(baseAttrsAfter)
        args["enhanceAttrsAfter"] = str(enhanceAttrsAfter)
        args["upgradeAttrsAfter"] = str(upgradeAttrsAfter)
        args["gradeBefore"] = gradeBefore
        args["gradeAfter"] = gradeAfter
        args["bindValueBefore"] = bindValueBefore
        args["bindValueAfter"] = bindValueAfter
        args["score"] = score
        LogTrackingMgr.LOG(args, kwargs)

    # 装备铭文
    @staticmethod
    def Equip_Glyph(opUUID, gbId, uniqueId, equipId, equipBelongTo, glyphDataBefore, glyphDataAfter, addBindValueBefore, addBindValueAfter, consumedItemBindValue, score, refId, glyphPos, bindValueBefore, bindValueAfter, **kwargs):
        args = {}
        args["trackName"] = "Equip_Glyph"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["uniqueId"] = uniqueId
        args["equipId"] = equipId
        args["equipBelongTo"] = equipBelongTo
        args["glyphDataBefore"] = str(glyphDataBefore)
        args["glyphDataAfter"] = str(glyphDataAfter)
        args["addBindValueBefore"] = addBindValueBefore
        args["addBindValueAfter"] = addBindValueAfter
        args["consumedItemBindValue"] = consumedItemBindValue
        args["score"] = score
        args["refId"] = refId
        args["glyphPos"] = glyphPos
        args["bindValueBefore"] = bindValueBefore
        args["bindValueAfter"] = bindValueAfter
        LogTrackingMgr.LOG(args, kwargs)

    # 装备祝福
    @staticmethod
    def Equip_Bless(opUUID, gbId, uniqueId, equipId, equipBelongTo, blessDataBefore, blessDataAfter, addBindValueBefore, addBindValueAfter, consumedItemBindValue, blessLvRateBefore, blessLvRateAfter, maxBlessLvBefore, maxBlessLvAfter, score, bindValueBefore, bindValueAfter, **kwargs):
        args = {}
        args["trackName"] = "Equip_Bless"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["uniqueId"] = uniqueId
        args["equipId"] = equipId
        args["equipBelongTo"] = equipBelongTo
        args["blessDataBefore"] = str(blessDataBefore)
        args["blessDataAfter"] = str(blessDataAfter)
        args["addBindValueBefore"] = addBindValueBefore
        args["addBindValueAfter"] = addBindValueAfter
        args["consumedItemBindValue"] = consumedItemBindValue
        args["blessLvRateBefore"] = blessLvRateBefore
        args["blessLvRateAfter"] = blessLvRateAfter
        args["maxBlessLvBefore"] = maxBlessLvBefore
        args["maxBlessLvAfter"] = maxBlessLvAfter
        args["score"] = score
        args["bindValueBefore"] = bindValueBefore
        args["bindValueAfter"] = bindValueAfter
        LogTrackingMgr.LOG(args, kwargs)

    # 装备绑定值洗涤
    @staticmethod
    def Equip_BindValue_Washing(opUUID, gbId, uniqueId, equipId, equipBelongTo, bindValueWashingBefore, bindValueWashingAfter, addBindValueStatusBefore, addBindValueStatusAfter, washCount, **kwargs):
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
        LogTrackingMgr.LOG(args, kwargs)

    # 道具工坊
    @staticmethod
    def Work_Shop(opUUID, gbId, normalItems, luckyItems, finalItems, **kwargs):
        args = {}
        args["trackName"] = "Work_Shop"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["normalItems"] = str(normalItems)
        args["luckyItems"] = str(luckyItems)
        args["finalItems"] = str(finalItems)
        LogTrackingMgr.LOG(args, kwargs)

    # 等级有礼事件
    @staticmethod
    def Level_Reward(gbId, level, welfareId, levelLimit, school, **kwargs):
        args = {}
        args["trackName"] = "Level_Reward"
        args["gbId"] = gbId
        args["level"] = level
        args["welfareId"] = welfareId
        args["levelLimit"] = levelLimit
        args["school"] = school
        LogTrackingMgr.LOG(args, kwargs)

    # 七日签到事件
    @staticmethod
    def Welfare_SignInSevenDay(gbId, welfareId, level, loginDay, dayId, opUUID, **kwargs):
        args = {}
        args["trackName"] = "Welfare_SignInSevenDay"
        args["gbId"] = gbId
        args["welfareId"] = welfareId
        args["level"] = level
        args["loginDay"] = loginDay
        args["dayId"] = dayId
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 十日签到事件
    @staticmethod
    def Welfare_SignInTenDay(gbId, welfareId, level, loginDay, dayId, opUUID, **kwargs):
        args = {}
        args["trackName"] = "Welfare_SignInTenDay"
        args["gbId"] = gbId
        args["welfareId"] = welfareId
        args["level"] = level
        args["loginDay"] = loginDay
        args["dayId"] = dayId
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 月卡事件
    @staticmethod
    def MonthCard_Invoke(gbId, level, invokeTime, expireTime, opUUID, **kwargs):
        args = {}
        args["trackName"] = "MonthCard_Invoke"
        args["gbId"] = gbId
        args["level"] = level
        args["invokeTime"] = invokeTime
        args["expireTime"] = expireTime
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 月卡挂机事件
    @staticmethod
    def MonthCard_Afk(gbId, timeLeft, timeCity, opUUID, **kwargs):
        args = {}
        args["trackName"] = "MonthCard_Afk"
        args["gbId"] = gbId
        args["timeLeft"] = timeLeft
        args["timeCity"] = timeCity
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 月卡离线挂机事件
    @staticmethod
    def MonthCard_Offline(gbId, timeLeft, timeOffline, **kwargs):
        args = {}
        args["trackName"] = "MonthCard_Offline"
        args["gbId"] = gbId
        args["timeLeft"] = timeLeft
        args["timeOffline"] = timeOffline
        LogTrackingMgr.LOG(args, kwargs)

    # 月卡离线奖励领取
    @staticmethod
    def MonthCard_OfflineReward(gbId, AFK_rewardType, opUUID, **kwargs):
        args = {}
        args["trackName"] = "MonthCard_OfflineReward"
        args["gbId"] = gbId
        args["AFK_rewardType"] = AFK_rewardType
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 礼包购买
    @staticmethod
    def Gift_Buy(gbId, buyPackage_Id, opUUID, **kwargs):
        args = {}
        args["trackName"] = "Gift_Buy"
        args["gbId"] = gbId
        args["buyPackage_Id"] = buyPackage_Id
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 升级
    @staticmethod
    def Level_LevelUp(gbId, preLevel, currLevel, upgradeExp, totalExp, expSrc, opUUID, **kwargs):
        args = {}
        args["trackName"] = "Level_LevelUp"
        args["gbId"] = gbId
        args["preLevel"] = preLevel
        args["currLevel"] = currLevel
        args["upgradeExp"] = upgradeExp
        args["totalExp"] = totalExp
        args["expSrc"] = expSrc
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # GM指令
    @staticmethod
    def GM_GM(src, command, **kwargs):
        args = {}
        args["trackName"] = "GM_GM"
        args["src"] = str(src)
        args["command"] = str(command)
        LogTrackingMgr.LOG(args, kwargs)

    # 货币兑换
    @staticmethod
    def Currency_Exchange(gbId, exchangeID, opUUID, **kwargs):
        args = {}
        args["trackName"] = "Currency_Exchange"
        args["gbId"] = gbId
        args["exchangeID"] = exchangeID
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 商店购买
    @staticmethod
    def Store_Buy(gbId, mallID, mallType, productID, realItemID, itemNum, limitType, limitNum, buyNum, costInfo, opUUID, **kwargs):
        args = {}
        args["trackName"] = "Store_Buy"
        args["gbId"] = gbId
        args["mallID"] = mallID
        args["mallType"] = mallType
        args["productID"] = productID
        args["realItemID"] = realItemID
        args["itemNum"] = itemNum
        args["limitType"] = limitType
        args["limitNum"] = limitNum
        args["buyNum"] = buyNum
        args["costInfo"] = str(costInfo)
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 收集事件
    @staticmethod
    def Collectible_Detail(gbId, collectId, status, propChange, opUUID, **kwargs):
        args = {}
        args["trackName"] = "Collectible_Detail"
        args["gbId"] = gbId
        args["collectId"] = collectId
        args["status"] = status
        args["propChange"] = str(propChange)
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 抽卡事件
    @staticmethod
    def DrawCard_Detail(gbId, poolId, poolGroupId, rollCost, realRollNum, itemList, befPityNum, aftPityNum, pityPullNum, befGuaranteed, aftGuaranteed, guaranteedType, opUUID, **kwargs):
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
        LogTrackingMgr.LOG(args, kwargs)

    # 抽卡保底
    @staticmethod
    def DrawCard_GuaranteedReward(gbId, poolId, poolGroupId, pityReward, guaranteed, guaranteedType, opUUID, **kwargs):
        args = {}
        args["trackName"] = "DrawCard_GuaranteedReward"
        args["gbId"] = gbId
        args["poolId"] = poolId
        args["poolGroupId"] = poolGroupId
        args["pityReward"] = pityReward
        args["guaranteed"] = guaranteed
        args["guaranteedType"] = guaranteedType
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 采集事件
    @staticmethod
    def Gather_Collection(gbId, collectionId, collectionType, startTime, endTime, opUUID, **kwargs):
        args = {}
        args["trackName"] = "Gather_Collection"
        args["gbId"] = gbId
        args["collectionId"] = collectionId
        args["collectionType"] = collectionType
        args["startTime"] = startTime
        args["endTime"] = endTime
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会副本开启
    @staticmethod
    def Guild_BossChallenge_Open(opUUID, guildUUID, job, openType, consumeType, consumeCount, openDungeonId, openTime, openedMoneyCount, openedFundCount, **kwargs):
        args = {}
        args["trackName"] = "Guild_BossChallenge_Open"
        args["opUUID"] = opUUID
        args["guildUUID"] = guildUUID
        args["job"] = job
        args["openType"] = openType
        args["consumeType"] = consumeType
        args["consumeCount"] = consumeCount
        args["openDungeonId"] = openDungeonId
        args["openTime"] = openTime
        args["openedMoneyCount"] = openedMoneyCount
        args["openedFundCount"] = openedFundCount
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会副本取消开启
    @staticmethod
    def Guild_BossChallenge_Cancel(opUUID, guildUUID, cancelType, consumeType, consumeCount, openDungeonId, openTime, openedMoneyCount, openedFundCount, **kwargs):
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
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会副本恢复回退
    @staticmethod
    def Guild_BossChallenge_Recover(opUUID, guildUUID, cancelType, consumeType, consumeCount, openDungeonId, openTime, openedMoneyCount, openedFundCount, **kwargs):
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
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会副本创建
    @staticmethod
    def Guild_BossChallenge_CreateDungeon(opUUID, **kwargs):
        args = {}
        args["trackName"] = "Guild_BossChallenge_CreateDungeon"
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会副本倒计时开启
    @staticmethod
    def Guild_BossChallenge_CDOpen(opUUID, **kwargs):
        args = {}
        args["trackName"] = "Guild_BossChallenge_CDOpen"
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会副本副本结算
    @staticmethod
    def Guild_BossChallenge_Settlement(opUUID, gbId, isClear, dmgScore, dmgRank, isFirstClear, firstPassRewards, rankRewards, **kwargs):
        args = {}
        args["trackName"] = "Guild_BossChallenge_Settlement"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["isClear"] = isClear
        args["dmgScore"] = dmgScore
        args["dmgRank"] = dmgRank
        args["isFirstClear"] = isFirstClear
        args["firstPassRewards"] = str(firstPassRewards)
        args["rankRewards"] = str(rankRewards)
        LogTrackingMgr.LOG(args, kwargs)

    # 扩容（背包或者仓库）
    @staticmethod
    def Capacity_Expansion(opUUID, gbId, type, capacityBefore, expansionCount, capacityAfter, playerLevel, consumeItems, **kwargs):
        args = {}
        args["trackName"] = "Capacity_Expansion"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["type"] = type
        args["capacityBefore"] = capacityBefore
        args["expansionCount"] = expansionCount
        args["capacityAfter"] = capacityAfter
        args["playerLevel"] = playerLevel
        args["consumeItems"] = str(consumeItems)
        LogTrackingMgr.LOG(args, kwargs)

    # 道具或者装备分解
    @staticmethod
    def Item_Disassembly(opUUID, gbId, type, disassembleItems, rewardItems, disassembleSettings, **kwargs):
        args = {}
        args["trackName"] = "Item_Disassembly"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["type"] = type
        args["disassembleItems"] = str(disassembleItems)
        args["rewardItems"] = str(rewardItems)
        args["disassembleSettings"] = disassembleSettings
        LogTrackingMgr.LOG(args, kwargs)

    # 传送
    @staticmethod
    def Teleport(gbId, level, fromMapId, toMapId, ways, isSuccess, failReason, **kwargs):
        args = {}
        args["trackName"] = "Teleport"
        args["gbId"] = gbId
        args["level"] = level
        args["fromMapId"] = fromMapId
        args["toMapId"] = toMapId
        args["ways"] = str(ways)
        args["isSuccess"] = isSuccess
        args["failReason"] = str(failReason)
        LogTrackingMgr.LOG(args, kwargs)

    # 怪物死亡
    @staticmethod
    def Kill_Monster(monsterId, mapId, suffix, **kwargs):
        args = {}
        args["trackName"] = "Kill_Monster"
        args["monsterId"] = monsterId
        args["mapId"] = mapId
        args["suffix"] = suffix
        LogTrackingMgr.LOG(args, kwargs)

    # 任务状态变更
    @staticmethod
    def Task_State_Change(gbId, taskId, taskState, taskType, taskMap, playerLevel, **kwargs):
        args = {}
        args["trackName"] = "Task_State_Change"
        args["gbId"] = gbId
        args["taskId"] = taskId
        args["taskState"] = taskState
        args["taskType"] = taskType
        args["taskMap"] = taskMap
        args["playerLevel"] = playerLevel
        LogTrackingMgr.LOG(args, kwargs)

    # pc引流奖励
    @staticmethod
    def Welfare_PcDrainage(accountId, gbId, deviceModel, claimTimestamp, opUUID, **kwargs):
        args = {}
        args["trackName"] = "Welfare_PcDrainage"
        args["accountId"] = str(accountId)
        args["gbId"] = gbId
        args["deviceModel"] = str(deviceModel)
        args["claimTimestamp"] = claimTimestamp
        args["opUUID"] = opUUID
        LogTrackingMgr.LOG(args, kwargs)

    # 副本门票消耗
    @staticmethod
    def Dungeon_Ticket_Consume(uniqueId, dungeonType, dungeonId, ticketType, enterType, playerCount, gbId, score, playerLevel, **kwargs):
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
        LogTrackingMgr.LOG(args, kwargs)

    # Boss出生
    @staticmethod
    def Dungeon_Boss_Born(uniqueId, dungeonType, dungeonId, spaceUUID, spaceNo, monsterId, bornTime, dungeonStartTime, **kwargs):
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
        LogTrackingMgr.LOG(args, kwargs)

    # Boss死亡
    @staticmethod
    def Dungeon_Boss_Dead(uniqueId, dungeonType, dungeonId, spaceUUID, spaceNo, monsterId, bornTime, deadTime, dungeonStartTime, **kwargs):
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
        LogTrackingMgr.LOG(args, kwargs)

    # 副本结算
    @staticmethod
    def Dungeon_Settlement(uniqueId, dungeonType, dungeonId, spaceUUID, spaceNo, gbId, isClear, isFirstClear, finishTime, isWin, reasonType, finishedPlayerCount, deadCount, firstRewards, clearRewards, goldRewards, autoBattleTimes, playerScore, playerLevel, **kwargs):
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
        args["firstRewards"] = str(firstRewards)
        args["clearRewards"] = str(clearRewards)
        args["goldRewards"] = str(goldRewards)
        args["autoBattleTimes"] = autoBattleTimes
        args["playerScore"] = playerScore
        args["playerLevel"] = playerLevel
        LogTrackingMgr.LOG(args, kwargs)

    # 更新经验
    @staticmethod
    def Update_Exp(gbId, deltaVal, modifyVal, opUUID, src, spaceNo, **kwargs):
        args = {}
        args["trackName"] = "Update_Exp"
        args["gbId"] = gbId
        args["deltaVal"] = deltaVal
        args["modifyVal"] = modifyVal
        args["opUUID"] = opUUID
        args["src"] = src
        args["spaceNo"] = spaceNo
        LogTrackingMgr.LOG(args, kwargs)

    # 死亡掉装
    @staticmethod
    def Drop_Equip(gbId, uniqueId, itemId, quality, grade, mapId, pos, operation, **kwargs):
        args = {}
        args["trackName"] = "Drop_Equip"
        args["gbId"] = gbId
        args["uniqueId"] = uniqueId
        args["itemId"] = itemId
        args["quality"] = quality
        args["grade"] = grade
        args["mapId"] = mapId
        args["pos"] = pos
        args["operation"] = operation
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会关系
    @staticmethod
    def Guild_Relation(guildUUID1, guildUUID2, operation, endTime, **kwargs):
        args = {}
        args["trackName"] = "Guild_Relation"
        args["guildUUID1"] = guildUUID1
        args["guildUUID2"] = guildUUID2
        args["operation"] = operation
        args["endTime"] = endTime
        LogTrackingMgr.LOG(args, kwargs)

    # 物品移动
    @staticmethod
    def Item_Movement(opUUID, gbId, uniqueId, itemId, itemCount, itemBindType, moveType, **kwargs):
        args = {}
        args["trackName"] = "Item_Movement"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["uniqueId"] = uniqueId
        args["itemId"] = itemId
        args["itemCount"] = itemCount
        args["itemBindType"] = itemBindType
        args["moveType"] = moveType
        LogTrackingMgr.LOG(args, kwargs)

    # 经脉升级
    @staticmethod
    def Meridian_UpGrade(opUUID, gbId, meridianId, pointId, newLevel, **kwargs):
        args = {}
        args["trackName"] = "Meridian_UpGrade"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["meridianId"] = meridianId
        args["pointId"] = pointId
        args["newLevel"] = newLevel
        LogTrackingMgr.LOG(args, kwargs)

    # 经脉强化
    @staticmethod
    def Meridian_Enhance(opUUID, gbId, meridianId, **kwargs):
        args = {}
        args["trackName"] = "Meridian_Enhance"
        args["opUUID"] = opUUID
        args["gbId"] = gbId
        args["meridianId"] = meridianId
        LogTrackingMgr.LOG(args, kwargs)

    # 精灵获取
    @staticmethod
    def Pet_Get(gbId, petId, petQuality, petSrc, **kwargs):
        args = {}
        args["trackName"] = "Pet_Get"
        args["gbId"] = gbId
        args["petId"] = petId
        args["petQuality"] = petQuality
        args["petSrc"] = petSrc
        LogTrackingMgr.LOG(args, kwargs)

    # 精灵升级
    @staticmethod
    def Pet_LevelUp(gbId, opUUID, petId, petQuality, oldLevel, newLevel, equip, addScore, **kwargs):
        args = {}
        args["trackName"] = "Pet_LevelUp"
        args["gbId"] = gbId
        args["opUUID"] = opUUID
        args["petId"] = petId
        args["petQuality"] = petQuality
        args["oldLevel"] = oldLevel
        args["newLevel"] = newLevel
        args["equip"] = str(equip)
        args["addScore"] = addScore
        LogTrackingMgr.LOG(args, kwargs)

    # 精灵编组
    @staticmethod
    def Pet_MakeTeam(gbId, playerLevel, battleId, battleType, petId, petQuality, petLevel, opType, joinBattleCount, battleCount, **kwargs):
        args = {}
        args["trackName"] = "Pet_MakeTeam"
        args["gbId"] = gbId
        args["playerLevel"] = playerLevel
        args["battleId"] = battleId
        args["battleType"] = battleType
        args["petId"] = petId
        args["petQuality"] = petQuality
        args["petLevel"] = petLevel
        args["opType"] = opType
        args["joinBattleCount"] = joinBattleCount
        args["battleCount"] = battleCount
        LogTrackingMgr.LOG(args, kwargs)

    # 精灵切换编组
    @staticmethod
    def Pet_ChangeTeam(gbId, mapId, battleId, battleData, **kwargs):
        args = {}
        args["trackName"] = "Pet_ChangeTeam"
        args["gbId"] = gbId
        args["mapId"] = mapId
        args["battleId"] = battleId
        args["battleData"] = str(battleData)
        LogTrackingMgr.LOG(args, kwargs)

    # 精灵跟随
    @staticmethod
    def Pet_Follow(gbId, mapId, petId, petQuality, petLevel, petEquipData, petFollowType, **kwargs):
        args = {}
        args["trackName"] = "Pet_Follow"
        args["gbId"] = gbId
        args["mapId"] = mapId
        args["petId"] = petId
        args["petQuality"] = petQuality
        args["petLevel"] = petLevel
        args["petEquipData"] = str(petEquipData)
        args["petFollowType"] = petFollowType
        LogTrackingMgr.LOG(args, kwargs)

    # 邮件发送
    @staticmethod
    def Mail_Send(toGBID, mailID, mailGBID, srcType, srcSubType, opUUID, idipSource, attachStr, **kwargs):
        args = {}
        args["trackName"] = "Mail_Send"
        args["toGBID"] = toGBID
        args["mailID"] = mailID
        args["mailGBID"] = mailGBID
        args["srcType"] = srcType
        args["srcSubType"] = srcSubType
        args["opUUID"] = opUUID
        args["idipSource"] = idipSource
        args["attachStr"] = str(attachStr)
        LogTrackingMgr.LOG(args, kwargs)

    # 邮件查看
    @staticmethod
    def Mail_Read(fromGBID, mailID, mailGBID, globalMailGBID, srcType, srcSubType, opUUID, idipSource, attachStr, **kwargs):
        args = {}
        args["trackName"] = "Mail_Read"
        args["fromGBID"] = fromGBID
        args["mailID"] = mailID
        args["mailGBID"] = mailGBID
        args["globalMailGBID"] = globalMailGBID
        args["srcType"] = srcType
        args["srcSubType"] = srcSubType
        args["opUUID"] = opUUID
        args["idipSource"] = idipSource
        args["attachStr"] = str(attachStr)
        LogTrackingMgr.LOG(args, kwargs)

    # 邮件领取
    @staticmethod
    def Mail_Get(fromGBID, mailID, mailGBID, globalMailGBID, srcType, srcSubType, opUUID, idipSource, attachStr, **kwargs):
        args = {}
        args["trackName"] = "Mail_Get"
        args["fromGBID"] = fromGBID
        args["mailID"] = mailID
        args["mailGBID"] = mailGBID
        args["globalMailGBID"] = globalMailGBID
        args["srcType"] = srcType
        args["srcSubType"] = srcSubType
        args["opUUID"] = opUUID
        args["idipSource"] = idipSource
        args["attachStr"] = str(attachStr)
        LogTrackingMgr.LOG(args, kwargs)

    # 邮件删除
    @staticmethod
    def Mail_Delete(fromGBID, mailID, mailGBID, globalMailGBID, srcType, srcSubType, opUUID, idipSource, attachStr, deleteSrcType, **kwargs):
        args = {}
        args["trackName"] = "Mail_Delete"
        args["fromGBID"] = fromGBID
        args["mailID"] = mailID
        args["mailGBID"] = mailGBID
        args["globalMailGBID"] = globalMailGBID
        args["srcType"] = srcType
        args["srcSubType"] = srcSubType
        args["opUUID"] = opUUID
        args["idipSource"] = idipSource
        args["attachStr"] = str(attachStr)
        args["deleteSrcType"] = deleteSrcType
        LogTrackingMgr.LOG(args, kwargs)

    # 交易行出售
    @staticmethod
    def Auction_ItemSale(playerGBID, opUUID, auctionUUID, itemId, itemNum, eachPrice, totalPrice, isPublicity, **kwargs):
        args = {}
        args["trackName"] = "Auction_ItemSale"
        args["playerGBID"] = playerGBID
        args["opUUID"] = opUUID
        args["auctionUUID"] = auctionUUID
        args["itemId"] = itemId
        args["itemNum"] = itemNum
        args["eachPrice"] = eachPrice
        args["totalPrice"] = totalPrice
        args["isPublicity"] = isPublicity
        LogTrackingMgr.LOG(args, kwargs)

    # 交易行购买
    @staticmethod
    def Auction_ItemBuy(playerGBID, opUUID, auctionUUID, itemId, auctionBuyItemNum, price, **kwargs):
        args = {}
        args["trackName"] = "Auction_ItemBuy"
        args["playerGBID"] = playerGBID
        args["opUUID"] = opUUID
        args["auctionUUID"] = auctionUUID
        args["itemId"] = itemId
        args["auctionBuyItemNum"] = auctionBuyItemNum
        args["price"] = price
        LogTrackingMgr.LOG(args, kwargs)

    # 交易行下架
    @staticmethod
    def Auction_ItemCanel(playerGBID, auctionUUID, itemId, itemNum, eachPrice, totalPrice, **kwargs):
        args = {}
        args["trackName"] = "Auction_ItemCanel"
        args["playerGBID"] = playerGBID
        args["auctionUUID"] = auctionUUID
        args["itemId"] = itemId
        args["itemNum"] = itemNum
        args["eachPrice"] = eachPrice
        args["totalPrice"] = totalPrice
        LogTrackingMgr.LOG(args, kwargs)

    # 交易行成交
    @staticmethod
    def Auction_ItemDeal(playerGBID, fromPlayerGBID, opUUID, auctionUUID, itemId, itemNum, totalPrice, realAddPrice, totalPriceTax, **kwargs):
        args = {}
        args["trackName"] = "Auction_ItemDeal"
        args["playerGBID"] = playerGBID
        args["fromPlayerGBID"] = fromPlayerGBID
        args["opUUID"] = opUUID
        args["auctionUUID"] = auctionUUID
        args["itemId"] = itemId
        args["itemNum"] = itemNum
        args["totalPrice"] = totalPrice
        args["realAddPrice"] = realAddPrice
        args["totalPriceTax"] = totalPriceTax
        LogTrackingMgr.LOG(args, kwargs)

    # 交易行收藏
    @staticmethod
    def Auction_ItemCollect(playerGBID, collectDataType, collectOpType, collectId, **kwargs):
        args = {}
        args["trackName"] = "Auction_ItemCollect"
        args["playerGBID"] = playerGBID
        args["collectDataType"] = collectDataType
        args["collectOpType"] = collectOpType
        args["collectId"] = collectId
        LogTrackingMgr.LOG(args, kwargs)

    @staticmethod
    def LOG(args, kwargs):
        logData = {
            'server': gameconfig.serverId(),
            'log_id': "LogTracking",
            'sentTimestamp': utils.getTimestamp64(),
            'gameId': gameconfig.gameId(),
        }
        logData.update(args)
        # 固定的不能改
        fixedHeaders = list(logData.keys())
        for k, v in kwargs.items():
            if k in fixedHeaders:
                continue
            if type(v) is int:
                logData[k] = v
            else:
                logData[k] = str(v)
        gamelog.TLOG("", json.dumps(logData), True)
