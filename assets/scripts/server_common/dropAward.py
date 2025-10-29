import random
import const_const as C_CD
import rewardData_rewardData as RDDT
import itemData_itemData as IDIDD
import gearBase_gearConst as GBGCD
import gearBase_gearBase as GB_GBD
import gearBase_typeExplanation as GB_TED
import mail_config as MACF
from KBEDebug import *
import gameconst
import utils
import math
import gameengine
import itemFactory
import dataUtils
import userType
import EquipmentItem
import drop_drop_id as DDI
import drop_drop_package as DDP
import drop_drop_sub_package as DDS
import awardContext
import gameglobal
import itemData_itemData_set as IDIDS
import copy


class WealthUnit(userType.UserSoleType):
    def __str__(self):
        return str(vars(self))

    def __getstate__(self):
        return self.data

    def __setstate__(self, state):
        self.data = state
        return self

    def __bool__(self):
        return bool(self.data)


class WealthNumeric(WealthUnit):
    def __init__(self, configName, itemId, data):
        self.configName = configName
        self.itemId = itemId
        self.data = data

    def __add__(self, other):
        self.data += other.data
        return self

    def clear(self):
        self.data = 0

    def isEqual(self, other):
        return self.data == other.data


class WealthItem(WealthUnit):
    def __init__(self, data=None, itemObjs=None):
        # data: {itemId:{bindType:num}}
        self.data = data or {}
        itemObjs = itemObjs or []
        self.itemsObjs = list(filter(lambda it: it.itemNum > 0, itemObjs))

    def __add__(self, other):
        for itemId, AwardInfo in other.data.items():
            self.data.setdefault(itemId, {})
            for bindType, num in AwardInfo.items():
                self.data[itemId].setdefault(bindType, 0)
                self.data[itemId][bindType] += num

        self.itemsObjs.extend(other.itemsObjs)

        return self

    def __getstate__(self):
        return {'data': self.data, 'itemObjs': self.itemsObjs}

    def __setstate__(self, state):
        self.data = state['data']
        self.itemsObjs = state['itemObjs']

    def __bool__(self):
        return bool(self.data or self.itemsObjs)

    def _lateReload(self):
        super(WealthItem, self)._lateReload()
        for it in self.itemsObjs:
            it.reloadScript()

    def addAwardItem(self, itemId, num, bindType):
        if bindType < 0:
            bindType = dataUtils.getItemDefaultBindType()

        if bindType not in (gameconst.ItemBindType.BIND, gameconst.ItemBindType.NORMAL):
            gameengine.reportCritical('invalid bindType', itemId, num, bindType)
            return
        self.data.setdefault(itemId, {})
        self.data[itemId].setdefault(bindType, 0)
        self.data[itemId][bindType] += num

    def addItemObjs(self, its):
        self.itemsObjs.extend(its)

    def toItemObjs(self):
        self.itemsObjs = self.getItemObjs()
        self.data = {}

    def getItemObjs(self, remove=False):
        itemList = []
        for itemId, awardInfo in self.data.items():
            for bindType, num in awardInfo.items():
                if not num:
                    continue
                itemList.extend(itemFactory.ItemFactory.createItemList(itemId, num, bindType))

        itemList.extend(self.itemsObjs)
        if remove:
            self.clear()

        return itemList

    def popDropEquipObjs(self):
        otherObjs = []
        equipList = []
        for it in self.itemsObjs:
            if it.isEquipmentItem():
                equipList.append(it)
            else:
                otherObjs.append(it)
        self.itemsObjs = otherObjs
        return equipList

    def popDropPetItemObjs(self):
        otherObjs = []
        petItemList = []
        for it in self.itemsObjs:
            if dataUtils.isLingShouItem(it.itemId):
                petItemList.append(it)
            else:
                otherObjs.append(it)
        self.itemsObjs = otherObjs
        return petItemList

    def popExtractRewardItems(self):
        extractRewardItemsDic = {}
        for itemId in list(self.data.keys()):
            itemData = dataUtils.getCommItemData(itemId)
            if not itemData:
                WARNING_MSG('popExtractRewardItems, no itemData:', self.data)
                continue
            if itemData['type'] == gameconst.ItemType.Normal and itemData[
                'subType'] == gameconst.ItemSubType.ExtractReward:
                extractRewardItemsDic[itemId] = self.data.pop(itemId)
        return extractRewardItemsDic

    def popRemainBagLimitItems(self, canAddNum):
        bagLimitItemsDic = {}
        for itemId in list(self.data.keys()):
            if itemId in IDIDS.categoryDatas.get(gameconst.BAG_LIMIT_ITEM_TYPE_DATA, set()):
                totalNum = sum(self.data[itemId].values())
                if canAddNum >= totalNum:
                    canAddNum -= totalNum
                elif canAddNum > 0:
                    popLeft = copy.deepcopy(self.data[itemId])
                    for bindType in popLeft.keys():
                        popLeft[bindType] = 0
                    for bindType, num in self.data[itemId].items():
                        if canAddNum >= num:
                            canAddNum -= num
                        else:
                            self.data[itemId][bindType] = canAddNum
                            popLeft[bindType] = num - canAddNum
                            canAddNum = 0
                    bagLimitItemsDic[itemId] = popLeft
                else:
                    bagLimitItemsDic[itemId] = self.data.pop(itemId)
        if bagLimitItemsDic:
            DEBUG_MSG('popRemainBagLimitItems:', bagLimitItemsDic, canAddNum)
        return bagLimitItemsDic

    def clear(self):
        self.data = {}
        self.itemsObjs = []

    def updateBindType(self, awardContext, bindType):
        if bindType not in gameconst.ItemBindType.VALID_BIND_TYPE:
            ERROR_MSG('updateBindType, invalid bind type:', bindType, gameconst.ItemBindType.VALID_BIND_TYPE)
            return
        
        for itemID, wealthData in self.data.items():
            newBindType = _calculateBindType(itemID, awardContext.school)
            if newBindType is None:
                newBindType = bindType
            totalNum = 0
            for _, num in wealthData.items():
                totalNum += num
            self.data[itemID] = {newBindType:totalNum}
        
        for itemsObj in self.itemsObjs:
            newBindType = _calculateBindType(itemsObj.itemId, awardContext.school)
            if newBindType is None:
                newBindType = bindType
            itemsObj.setItemBind(bindType)

class WealthTitleOne(userType.UserSoleType):
    def __init__(self, titleId, startTime=-1):
        self.titleId = titleId
        self.startTime = startTime


class WealthTitle(WealthUnit):
    def __init__(self, data=None):
        # data: list of title id
        self.data = data or []

    def __add__(self, other):
        self.data.extend(other.data)
        return self

    def clear(self):
        self.data = []

class WealthFightProp(WealthUnit):
    def __init__(self, data=None):
        self.data = data or []

    def __add__(self, other):
        self.data.extend(other.data)
        return self

    def clear(self):
        self.data = []

class WealthResDic(WealthUnit):
    def __init__(self, data=None):
        self.data = data or {}

    def __add__(self, other):
        for itemId, num in other.data.items():
            self.data[itemId] = self.data.get(itemId, 0)+num

        return self

    def __bool__(self):
        return sum(self.data.values()) > 0

    def clear(self):
        self.data = {}

class WealthVal(userType.UserSoleType):
    def __str__(self):
        return str(vars(self))

    def __getstate__(self):
        st = {}
        for k, v in vars(self).items():
            if v:
                st[k] = v.__getstate__()
        return st

    def __setstate__(self, state):
        self.__init__()
        for k, v in state.items():
            self.__dict__[k].__setstate__(v)

    def __str__(self):
        s = {}
        for k, v in vars(self).items():
            if not isinstance(v, WealthUnit):
                if v:
                    s[k] = str(v)
            elif v.data:
                s[k] = str(v.__getstate__())
        return str(s)

    def getNumericWealth(self):
        pass

    def getAllWealth(self):
        pass

    def addWealthByItemId(self, itemId, num, bindType):
        pass

    def isEmpty(self):
        return not any(self.getAllWealth())

    def scrubWealthItemObjs(self, *args, **kwargs):
        """API: 清洗itemObj中数据"""


class AwardMixin(object):
    def toShowList(self):
        return [{'itemId': k, 'itemNum': v} for k, v in self.getItemsDic().items()]

    def getItemsDic(self):
        # 获得所有有效item的数量信息, 记录日志, 爬塔奖励展示 使用
        itemsDic = {}
        for numericWealth in self.getNumericWealth():
            if numericWealth:
                itemsDic[numericWealth.itemId] = numericWealth.data
        for itemId, itemInfo in self.itemWealth.data.items():
            for _, num in itemInfo.items():
                itemsDic[itemId] = itemsDic.get(itemId, 0) + num
        for it in self.itemWealth.itemsObjs:
            itemsDic[it.itemId] = itemsDic.get(it.itemId, 0) + it.itemNum
        return itemsDic

    def toBriefList(self):
        _retList = []
        for numericWealth in self.getNumericWealth():
            if numericWealth:
                _retList.append({'itemId': numericWealth.itemId, 'itemNum': numericWealth.data, 'bindType': gameconst.ItemBindType.BIND})

        for itemId, itemInfo in self.itemWealth.data.items():
            for _bindType, num in itemInfo.items():
                _retList.append({'itemId': itemId, 'itemNum': num, 'bindType': _bindType})

        for itemId, itemInfo in self.petItemWealth.data.items():
            for _bindType, num in itemInfo.items():
                _retList.append({'itemId': itemId, 'itemNum': num, 'bindType': _bindType})

        for it in self.itemWealth.itemsObjs:
            _retList.append({'itemId': it.itemId, 'itemNum': it.itemNum, 'bindType': it.bindType})

        for it in self.petItemWealth.itemsObjs:
            _retList.append({'itemId': it.itemId, 'itemNum': it.itemNum, 'bindType': it.bindType})

        return _retList


class BaseAwardVal(WealthVal, AwardMixin):

    def __init__(self, exp=0, coin=0, money=0, guildContrib=0, itemObjs=None, guildFund=0, guildExp=0, darkIron=0, guildMoney=0, geniusQi=0):
        self.exp = WealthNumeric('exp', gameconst.ItemId.EXP, exp)
        self.coin = WealthNumeric('coin', gameconst.ItemId.COIN, coin)
        self.money = WealthNumeric('money', gameconst.ItemId.MONEY, money)
        self.darkIron = WealthNumeric('darkIron', gameconst.ItemId.DARK_IRON, darkIron)
        self.geniusQi = WealthNumeric('geniusQi', gameconst.ItemId.GENIUS_QI, geniusQi)
        self.guildContrib = WealthNumeric('guildContrib', gameconst.ItemId.GUILD_CONTRIB, guildContrib)
        self.guildMoney = WealthNumeric('guildMoney', gameconst.ItemId.GUILD_MONEY, guildMoney)
        self.guildFund = WealthNumeric('guildFund', gameconst.ItemId.GUILD_FUND, guildFund)
        self.guildExp = WealthNumeric('guildExp', gameconst.ItemId.GUILD_EXP, guildExp)

        self.petItemWealth = WealthItem()
        self.itemWealth = WealthItem()
        self.addWealthByObjList(itemObjs)

    def _lateReload(self):
        for wealthIt in self.getAllWealth():
            wealthIt.reloadScript()
        return

    def __str__(self):
        s = {}
        for k, v in vars(self).items():
            if not isinstance(v, WealthUnit):
                if v:
                    s[k] = str(v)
            elif v.data:
                s[k] = str(v.__getstate__())
        return str(s)

    def __add__(self, other):
        self.exp += other.exp
        self.coin += other.coin
        self.money += other.money
        self.darkIron += other.darkIron
        self.geniusQi += other.geniusQi
        self.guildContrib += other.guildContrib
        self.itemWealth += other.itemWealth
        self.petItemWealth += other.petItemWealth
        self.guildMoney += other.guildMoney
        self.guildFund += other.guildFund
        self.guildExp += other.guildExp

        return self

    def __getstate__(self):
        st = {}
        for k, v in vars(self).items():
            if not v:
                continue
            st[k] = v.__getstate__()
        return st

    def __setstate__(self, state):
        self.__init__()
        for k, v in state.items():
            self.__dict__[k].__setstate__(v)

    def getNumericWealth(self):
        return (self.exp, self.coin, self.money, self.guildContrib, self.guildFund, self.guildExp, self.darkIron, self.guildMoney, self.geniusQi)

    def getAllWealth(self):
        return self.getNumericWealth() + (self.itemWealth, self.petItemWealth)

    def clear(self):
        for wealth in self.getAllWealth():
            wealth.clear()
        return

    def getNoObjItemDic(self):
        itemsDic = {}
        for numericWealth in self.getNumericWealth():
            if numericWealth:
                itemsDic[numericWealth.itemId] = numericWealth.data
        return itemsDic

    def getItemsTLogStr(self):
        # 记录日志使用
        itemsStr = ''
        for itemId, itemNum in self.getItemsDic().items():
            itemsStr += str(itemId) + ',' + str(itemNum) + ';'
        return itemsStr.strip(';')

    def addWealthByItemId(self, itemId, num, bindType=dataUtils.getItemDefaultBindType(), **kwargs):
        if not num:
            return self

        for awardItem in self.getNumericWealth():
            if itemId == awardItem.itemId:
                awardItem.data += num
                return self

        itemData = dataUtils.getCommItemData(itemId) or {}
        if not itemData:
            gameengine.reportCritical('BaseAwardVal::addWealthByItemId, not support itemId:', itemId)
            return self

        type = itemData.get('type')
        if type == gameconst.ItemType.Normal:
            if itemData['subType'] in itemFactory.ItemFactory.NormalItemClassMap:
                itemObjs = itemFactory.ItemFactory.createItemList(itemId, num, bindType, **kwargs)
                self.itemWealth.addItemObjs(itemObjs)
            else:
                self.itemWealth.addAwardItem(itemId, num, bindType)
        elif type == gameconst.ItemType.LingShou:
            if itemData['subType'] in itemFactory.ItemFactory.LingShouItemClassMap:
                itemObjs = itemFactory.ItemFactory.createItemList(itemId, num, bindType, **kwargs)
                self.petItemWealth.addItemObjs(itemObjs)
            else:
                self.petItemWealth.addAwardItem(itemId, num, bindType)
        return self

    def addWealthByObjList(self, itemObjs):
        if not itemObjs:
            return
        # DEBUG_MSG('in addWealthByObjList:', [it.itemId for it in itemObjs])
        itemObjs = list(filter(lambda it: it.itemNum > 0, itemObjs))
        normalItemList = []
        petItemList = []
        for it in itemObjs:
            if it.itemNum == 0:
                continue
            itemData = dataUtils.getCommItemData(it.itemId)
            itemType = itemData.get('type')
            if itemType == gameconst.ItemType.LingShou:
                petItemList.append(it)
            else:
                normalItemList.append(it)
        normalItemList and self.itemWealth.addItemObjs(normalItemList)
        petItemList and self.petItemWealth.addItemObjs(petItemList)
        return self

    def getPetItemObjs(self):
        return self.petItemWealth.itemsObjs

    def scrubWealthItemObjs(self, createTime=-1):
        for _obj in self.petItemWealth.itemsObjs:
            if createTime > 0:
                _obj.createTime = createTime
        for _obj in self.itemWealth.itemsObjs:
            if createTime > 0:
                _obj.createTime = createTime

    def setAwardItemBindType(self, awardContext, bindType):
        self.itemWealth.updateBindType(awardContext, bindType)
        self.petItemWealth.updateBindType(awardContext, bindType)

class AwardVal(BaseAwardVal):
    def __init__(self, exp=0, coin=0, money=0, fightPropList=None, itemObjs=None, **kwargs):
        super().__init__(exp=exp, coin=coin, money=money, itemObjs=itemObjs, **kwargs)
        self.fightProps = WealthFightProp(fightPropList)
        return

    def __add__(self, other):
        super().__add__(other)
        self.fightProps += other.fightProps
        return self

    def getAllWealth(self):
        return super().getAllWealth() +(self.fightProps,)

    def processAntiAddict(self, owner, isNotify, srcType, detail):
        return self

    def toClientDisplayVal(self):
        retList = []
        retList.extend({'itemId': itemId, 'itemNum': num} for itemId, num in self.getNoObjItemDic().items())
        retList.extend({'itemId': i.itemId, 'itemNum': i.itemNum} for i in self.itemWealth.getItemObjs())
        retList.extend({'itemId': i.itemId, 'itemNum': i.itemNum} for i in self.petItemWealth.getItemObjs())
        return retList


class DeductWealthVal(WealthVal, AwardMixin):
    def __init__(self, coin=0, money=0, itemsDic=None, petItemsDic=None, guildContrib=0, guildFund=0, guildExp=0, darkIron=0, guildMoney=0, geniusQi=0):
        self.coin = WealthNumeric('coin', gameconst.ItemId.COIN, coin)
        self.money = WealthNumeric('', gameconst.ItemId.MONEY, money)
        self.darkIron = WealthNumeric('darkIron', gameconst.ItemId.DARK_IRON, darkIron)
        self.geniusQi = WealthNumeric('geniusQi', gameconst.ItemId.GENIUS_QI, geniusQi)
        self.guildContrib = WealthNumeric('guildContrib', gameconst.ItemId.GUILD_CONTRIB, guildContrib)
        self.itemWealth = WealthItem(itemsDic)
        self.petItemWealth = WealthItem(petItemsDic)
        self.guildMoney = WealthNumeric('guildMoney', gameconst.ItemId.GUILD_MONEY, guildMoney)
        self.guildFund = WealthNumeric('guildFund', gameconst.ItemId.GUILD_FUND, guildFund)
        self.guildExp = WealthNumeric('guildExp', gameconst.ItemId.GUILD_EXP, guildExp)

    def __getstate__(self):
        st = {}
        for k, v in vars(self).items():
            if not v:
                continue
            st[k] = v.__getstate__()
        return st

    def __setstate__(self, state):
        self.__init__()
        for k, v in state.items():
            self.__dict__[k].__setstate__(v)

    def getNumericWealth(self):
        return (self.coin, self.money, self.guildContrib, self.darkIron, self.geniusQi)

    def getAllWealth(self):
        return self.getNumericWealth() + (self.itemWealth, self.petItemWealth)

    def addWealthByItemDict(self, itemDict):
        """通过老的itemDict形式加入物品

            type itemDict: {itemID_1: [itemNum_1, bindType_1], ...}
        """
        for itemId, (itemNum, bindType) in itemDict.items():
            self.addWealthByItemId(itemId, itemNum, bindType)

    def addWealthByItemId(self, itemId, num, bindType=dataUtils.getItemDefaultBindType()):
        for awardItem in self.getNumericWealth():
            if itemId == awardItem.itemId:
                awardItem.data += num
                return self

        itemType = dataUtils.getCommItemData(itemId).get('type')
        if itemType == gameconst.ItemType.Normal:
            self.itemWealth.addAwardItem(itemId, num, bindType)
        elif itemType == gameconst.ItemType.LingShou:
            self.petItemWealth.addAwardItem(itemId, num, bindType)
        else:
            ERROR_MSG('DeductWealthVal error:', itemId, bindType, num)
        return self

    def addWealthByObjList(self, itemObjs):
        if not itemObjs:
            return
        itemObjs = list(filter(lambda it: it.itemNum > 0, itemObjs))
        normalItemList = []
        petItemList = []
        for it in itemObjs:
            if it.itemNum == 0:
                continue
            maxStackSize = it.maxStackSize(it.itemId)
            if maxStackSize != 1:
                ERROR_MSG('DeductWealthVal::addWealthByObjList, not support itemId:', it.itemId)
                continue
            itemData = dataUtils.getCommItemData(it.itemId)
            itemType = itemData.get('type')
            if itemType == gameconst.ItemType.LingShou:
                petItemList.append(it)
            else:
                normalItemList.append(it)
        normalItemList and self.itemWealth.addItemObjs(normalItemList)
        petItemList and self.petItemWealth.addItemObjs(petItemList)
        return self

    def scrubWealthItemObjs(self, createTime=-1):
        for _obj in self.itemWealth.itemsObjs:
            if createTime > 0:
                _obj.createTime = createTime
        for _obj in self.petItemWealth.itemsObjs:
            if createTime > 0:
                _obj.createTime = createTime


class MailWealthVal(BaseAwardVal):
    def __init__(self, exp=0, coin=0, money=0, itemObjs=None, titleList=None, **kwargs):
        super().__init__(exp=exp, coin=coin,  money=money, itemObjs=itemObjs, **kwargs)

        self.titleWealth = WealthTitle(titleList)

    def getAllWealth(self):
        return super().getAllWealth() + (self.titleWealth,)

    def __add__(self, other):
        super().__add__(other)
        self.titleWealth += other.titleWealth
        return self

    def toMailWealthDict(self):
        resItemList = []
        bagItemList = []
        bagItemObjList = []
        titleList = []

        for awardItem in self.getNumericWealth():
            if awardItem.data>0:
                resItemList.append({'itemId':awardItem.itemId, 'itemNum':awardItem.data})

        for itemId, awardInfo in self.itemWealth.data.items():
            for bindType, itemNum in awardInfo.items():
                if not itemNum:
                    continue
                bagItemList.append({'itemId':itemId, 'itemNum':itemNum, 'bindType':bindType})

        for it in self.itemWealth.itemsObjs:
            bagItemObjList.append(it.toItemSavedDict())

        for it in self.petItemWealth.itemsObjs:
            bagItemObjList.append(it.toItemSavedDict())

        for titleWealthVal in self.titleWealth.data:
            titleList.append({
                'titleId': titleWealthVal.titleId,
                'startTime': titleWealthVal.startTime,
            })

        return {
            'resItemList' : resItemList,
            'bagItemList' : bagItemList,
            'bagItemObjList' : bagItemObjList,
            'titleList': titleList,
        }

    def fromMailWealthDict(self, dic):
        self.clear()
        for resItemDic in dic['resItemList']:
            self.addWealthByItemId(resItemDic['itemId'], resItemDic['itemNum'])

        for bagItemDic in dic['bagItemList']:
            self.addWealthByItemId(bagItemDic['itemId'], bagItemDic['itemNum'], bagItemDic['bindType'])
        itemObjList = []
        for itemSavedDic in dic['bagItemObjList']:
            it = itemFactory.ItemFactory.createItemWithSavedDict(itemSavedDic)
            itemObjList.append(it)
        self.addWealthByObjList(itemObjList)

        for titleDic in dic.get('titleList', []):
            self.titleWealth.data.append(WealthTitleOne(titleDic['titleId'], titleDic['startTime']))
        return

    def addTitle(self, titleId, startTime):
        self.titleWealth.data.append(WealthTitleOne(titleId, startTime))

    def addWealthByRewardId(self, rewardId):
        DEBUG_MSG('in addWealthByRewardId:', rewardId)
        wealthVal = getAward(rewardId, 1, awardContext.CommonContext(0))
        self.addWealthByAwardVal(wealthVal)
        return

    def addWealthByAwardVal(self, wealthVal:AwardVal):
        DEBUG_MSG('in addWealthByAwardVal:', wealthVal)
        if wealthVal.isEmpty():
            return
        for awardIt in wealthVal.getNumericWealth():
            if awardIt.data <= 0:
                continue
            self.addWealthByItemId(awardIt.itemId, awardIt.data)

        self.addWealthByObjList(wealthVal.itemWealth.getItemObjs(remove=True))
        self.addWealthByObjList(wealthVal.petItemWealth.getItemObjs(remove=True))
        for itemId, itemInfo in wealthVal.itemWealth.data.items():
            for bindType, num in itemInfo.items():
                if num <= 0:
                    continue
                self.addWealthByItemId(itemId, num, bindType)

        return
    #删掉超过上限的附件道具
    def reduceItemToMaxNum(self):
        maxNum = MACF.datas['mailItemsNumMax']['value']
        for awardIt in self.getNumericWealth():
            if awardIt.data > 0:
                if maxNum <= 0:
                    awardIt.data = 0
                maxNum -= 1
        newData = {}
        for itemId, itemInfo in self.itemWealth.data.items():
            if maxNum <= 0:
                break
            maxNum -= 1
            newData.setdefault(itemId, {})
            newData[itemId] = itemInfo
        self.itemWealth.data = newData
        
        newItemObjs = []
        for it in self.itemWealth.itemsObjs:
            if maxNum <= 0:
                break
            maxNum -= 1
            newItemObjs.append(it)
        self.itemWealth.itemsObjs = newItemObjs

        newpetData = {}
        for itemId, itemInfo in self.petItemWealth.data.items():
            if maxNum <= 0:
                break
            maxNum -= 1
            newpetData.setdefault(itemId, {})
            for bindType, num in itemInfo.items():
                newpetData[itemId].setdefault(bindType, 0)
                newpetData[itemId][bindType] += num
        self.petItemWealth.data = newpetData

        newPetItemObjs = []
        for it in self.petItemWealth.itemsObjs:
            if maxNum <= 0:
                break
            maxNum -= 1
            newPetItemObjs.append(it)
        self.petItemWealth.itemsObjs = newPetItemObjs
    def mailWealthExceedUplimit(self):
        totalNum = 0
        for awardIt in self.getNumericWealth():
            if awardIt.data > 0:
                totalNum += 1

        totalNum += len(self.itemWealth.data) + len(self.itemWealth.itemsObjs)
        totalNum += len(self.petItemWealth.data) + len(self.petItemWealth.itemsObjs)
        maxNum = MACF.datas['mailItemsNumMax']['value']
        if totalNum > maxNum:
            gameengine.reportCritical('mailWealthExceedUplimit:', totalNum, maxNum)
        return totalNum > maxNum

    def getAwardVal(self):
        wealthVal = AwardVal(
            exp=self.exp.data,
            coin=self.coin.data,
            money=self.money.data,
            darkIron=self.darkIron.data,
            geniusQi=self.geniusQi.data,
            itemObjs=self.itemWealth.itemsObjs,
            guildContrib=self.guildContrib.data,
            guildMoney=self.guildMoney.data,
            guildFund=self.guildFund.data,
            guildExp=self.guildExp.data,
        )

        for itemId, itemInfo in self.itemWealth.data.items():
            for bindType, num in itemInfo.items():
                if num <= 0:
                    continue
                wealthVal.addWealthByItemId(itemId, num, bindType)

        wealthVal.addWealthByObjList(self.petItemWealth.itemsObjs)
        return wealthVal

def _getResourceFixReward(awardId, context):
    resourceFixReward = RDDT.datas[awardId]['resourceFixReward']
    ret = AwardVal()
    for awardInfo in resourceFixReward:
        itemId, itemNum = awardInfo
        if callable(itemId):
            itemId = itemId()
        itemData = dataUtils.getCommItemData(itemId)
        if itemData.get('type') != gameconst.ItemType.Resource:
            continue
        if callable(itemNum):
            itemNum = int(itemNum(context.args))  # context.args: srcLv, playerLevel
        else:
            itemNum = int(itemNum)
        ret.addWealthByItemId(itemId, itemNum)
    return ret

def _getDefaultBandType():
    gearDropBindProb = C_CD.datas['itemUnboundProb']['value']
    if random.uniform(0, 1) > gearDropBindProb:
        return gameconst.ItemBindType.BIND
    else:
        return gameconst.ItemBindType.NORMAL

def _genEquipItemList(itemId, itemNum, bindType, quality, context):
    dropParamDic = {
        'srcLevel': context.level or 0,
        'creatorName': context.avatarName or '',
        'mstName': context.srcEntName or '',
        'monsterId': context.monsterId or 0,
        'school': context.school or 0,
        'quality': quality or 0,
        'creatorGbId': context.avatarGbId or 0,
    }

    if itemId == gameconst.ItemId.COMMON_EQUIPMENT_ID:
        itemId = EquipmentItem.EquipItemIdGen.genEquipItemIdByDropData(**dropParamDic)
        DEBUG_MSG('_genEquipItemList, gen Equipitem ItemId:', itemId, dropParamDic)

    equipList = []
    if itemId:
        if context.isNeedRegenBindType:
            _subType = GB_GBD.datas[itemId]['subType']
            _school = GB_TED.datas[_subType]['RemindClass']
            if not _school:
                gearDropBindProb = GBGCD.datas['gearDropUnboundProbForOwnClass']['value']
            elif _school == context.school:
                gearDropBindProb = GBGCD.datas['gearDropUnboundProbForOwnClass']['value']
            else:
                gearDropBindProb = GBGCD.datas['gearDropUnboundProbForOtherClass']['value']
                
            if random.uniform(0, 1) > gearDropBindProb:
                bindType = gameconst.ItemBindType.BIND
            else:
                bindType = gameconst.ItemBindType.NORMAL
        equipList.extend(itemFactory.ItemFactory.createItemList(itemId, itemNum, bindType, **dropParamDic))
    else:
        ERROR_MSG('_genEquipItemList, no match equipment:', itemId, dropParamDic)
    return equipList

def _addItemToAward(awardVal: AwardVal, itemId, itemNum, bindType, quality, context):
    itemArgs = getattr(context, 'itemArgs', {})
    if itemArgs == '':
        itemArgs = {}
    if dataUtils.isEquipItemByItemId(itemId):
        for i in range(itemNum):
            equipList = _genEquipItemList(itemId, 1, bindType, quality, context)
            equipList and awardVal.itemWealth.addItemObjs(equipList)
    else:
        awardVal.addWealthByItemId(itemId, itemNum, bindType, **itemArgs)
    return


def _getResourceExReward(awardId, context):
    resourceExReward = RDDT.datas[awardId]['resourceExReward']
    ret = AwardVal()
    for awardInfo in resourceExReward:
        itemId, num, prob = awardInfo
        if callable(itemId):
            itemId = itemId()
        itemData = dataUtils.getCommItemData(itemId)
        if itemData.get('type') != gameconst.ItemType.Resource:
            continue
        if callable(num):
            num = int(num(context.args))  # context.args: srcLv
        else:
            num = int(num)
        if callable(prob):
            prob = prob(context.args)  # context.args: srcLv
        for j in range(num):
            if random.randint(1, prob) == 1:
                ret.addWealthByItemId(itemId, 1)
    return ret


def _getFixedAward(fixAward, context, itemType):

    awardVal = AwardVal()
    for awardInfo in fixAward:
        bindType = None
        quality = 0
        if len(awardInfo) == 2:
            itemId, itemNum = awardInfo
        elif len(awardInfo) == 3:
            itemId, itemNum, bindType = awardInfo
        else:
            itemId, itemNum, bindType, quality = awardInfo
        if callable(itemId):
            itemId = itemId()
        itemData = dataUtils.getCommItemData(itemId)
        if not itemData:
            gameengine.reportCritical(f"dropAward->_getFixedAward ::raise exception, missing item config in reward data, {fixAward}, {itemId}")
            continue
        if itemData.get('type') != itemType:
            continue
        if bindType is None:
            context.addContextVar('isNeedRegenBindType', True)
            bindType = _getDefaultBandType()

        if callable(itemNum):
            itemNum = int(itemNum(context.args))  # context.args: srcLv, playerLevel
        else:
            itemNum = int(itemNum)

        _addItemToAward(awardVal, itemId, itemNum, bindType, quality, context)

    return awardVal


def _getFixRewardBaseOnSexual(awardId, context):
    fixRewardBaseOnSexual = RDDT.datas[awardId]['fixRewardBaseOnSexual']
    awardVal = AwardVal()
    if not fixRewardBaseOnSexual:
        return awardVal
    for awardInfo in fixRewardBaseOnSexual[context.args.avatarSex]:
        bindType = None
        if len(awardInfo) == 2:
            itemId, itemNum = awardInfo
        elif len(awardInfo) == 3:
            itemId, itemNum, bindType = awardInfo

        if bindType is None:
            context.addContextVar('isNeedRegenBindType', True)
            bindType = _getDefaultBandType()

        itemData = dataUtils.getCommItemData(itemId)
        if itemData.get('type') != gameconst.ItemType.Normal:
            continue
        _addItemToAward(awardVal, itemId, itemNum, bindType, 0, context)

    return awardVal


def _getNestedFixAward(awardId, context, isNeedDisturb=False):
    nestedFixAward = RDDT.datas[awardId]['nestFixReward']
    ret = AwardVal()

    for awardInfo in nestedFixAward:
        needSchools = ()
        if len(awardInfo) == 2:
            innerAwardId, num = awardInfo
        else:
            innerAwardId, num, needSchools = awardInfo

        if needSchools and context.school not in needSchools:
            continue

        if callable(innerAwardId):
            innerAwardId = innerAwardId()

        if callable(num):
            num = int(num(context.args))  # context.args: srcLv
        else:
            num = int(num)

        ret += getAward(innerAwardId, num, context, isNeedDisturb)

    return ret


def _getExtraAward(exAward, context, itemType):
    awardVal = AwardVal()
    for awardInfo in exAward:
        bindType = None
        quality = None
        if len(awardInfo) == 3:
            itemId, num, prob = awardInfo
        elif len(awardInfo) == 4:
            itemId, num, prob, bindType = awardInfo
        else:
            itemId, num, prob, bindType, quality = awardInfo

        if callable(itemId):
            itemId = itemId()
        itemData = dataUtils.getCommItemData(itemId)
        if itemData.get('type') != itemType:
            continue

        if bindType is None:
            context.addContextVar('isNeedRegenBindType', True)
            bindType = _getDefaultBandType()

        if callable(num):
            num = int(num(context.args))  # context.args: srcLv
        else:
            num = int(num)

        if callable(prob):
            prob = prob(context.args)  # context.args: srcLv

        for j in range(num):
            if random.randint(1, prob) == 1:
                _addItemToAward(awardVal, itemId, 1, bindType, quality, context)
    return awardVal


def _getNestedExAward(awardId, context, isNeedDisturb=False):
    nextedExtAward = RDDT.datas[awardId]['nestExReward']

    ret = AwardVal()

    for awardInfo in nextedExtAward:
        if len(awardInfo) == 3:
            (innerAwardId, num, prob), needSchools = awardInfo, ()
        else:
            innerAwardId, num, prob, needSchools = awardInfo

        if needSchools and context.school not in needSchools:
            continue

        if callable(num):
            num = int(num(context.args))  # context.args: srcLv

        if callable(prob):
            prob = prob(context.args)  # context.args: srcLv

        for k in range(num):
            if random.randint(1, prob) == 1:
                ret += getAward(innerAwardId, 1, context, isNeedDisturb)

    return ret


def _getSinAward(singleAward, context, itemType):
    awardVal = AwardVal()

    weighList = [oneRwData[2] for oneRwData in singleAward]
    idx = utils.randomByWeight(weighList)
    if idx is not None:
        bindType = None
        quality = None
        if len(singleAward[idx]) == 5:
            itemId, num, weight, bindType, quality = singleAward[idx]
        if len(singleAward[idx]) == 4:
            itemId, num, weight, bindType = singleAward[idx]
        else:
            itemId, num, weight = singleAward[idx]
        if callable(itemId):
            itemId = itemId()
        if bindType is None:
            context.addContextVar('isNeedRegenBindType', True)
            bindType = _getDefaultBandType()

        itemData = dataUtils.getCommItemData(itemId)
        if itemData.get('type') == gameconst.ItemType.Normal or itemData.get('type') == gameconst.ItemType.LingShou:
            _addItemToAward(awardVal, itemId, num, bindType, quality, context)
    return awardVal


def _calSubPackDrop(dropTarget, times, context):
    #单次子包掉落与策划约定最大掉100次，如未来有需求更大得用numpy重构
    if times > 100:
        ERROR_MSG("drop times is too large:", times, "dropTarget:", dropTarget, "context:", context)
        return [], [], [], []

    dropSubPackageData = DDS.dropPackageData.get(dropTarget)
    if dropSubPackageData:
        dropSubPackageData = _checkDropCondition(dropSubPackageData, context)
        if len(dropSubPackageData) == 0:
            WARNING_MSG("dropSubPackageData is empty, dropTarget: %s" % dropTarget)
            return [], [], [], []
        weights = []
        for dropData in dropSubPackageData:
            weights.append(dropData['weight'])
        data = random.choices(dropSubPackageData, weights=weights, k=times)
        dropTargetList = [item['dropTarget'] for item in data]
        numMinList = [item['dropNumMin'] for item in data]
        numMaxList = [item['dropNumMax'] for item in data]
        bindWeightList = [item.get('bindWeight', 10000) for item in data]
        return dropTargetList, numMinList, numMaxList, bindWeightList
    return [], [], [], []


#处理掉落子包还是掉落物品
def _getRealDropTarget(dropTargetData, context):
    dropTargetList = [dropTargetData['dropTarget']]
    numMinList = [dropTargetData['dropNumMin']]
    numMaxList = [dropTargetData['dropNumMax']]
    bindWeightList = [dropTargetData.get('bindWeight', 10000)]
    #子包
    if dropTargetData['dropType'] == gameconst.DropWayType.DROP_WAY_TYPE_2:
        (dropTargetList, numMinList, numMaxList, bindWeightList) = _calSubPackDrop(dropTargetList[0], random.randint(numMinList[0], numMaxList[0]), context)
    return dropTargetList, numMinList, numMaxList, bindWeightList


def _getBindType(itemID, bindWeight, context):
    bindType = _calculateBindType(itemID, context.school)
    if bindType:
        return bindType
    #其他情况，根据权重随机
    if random.randint(1, 10000) <= bindWeight:
        return gameconst.ItemBindType.BIND
    else:
        return gameconst.ItemBindType.NORMAL

def _calculateBindType(itemID, school):
    #如果是非本职业装备，必定非绑定
    itemData = GB_GBD.datas.get(itemID)
    if itemData:
        _subType = itemData['subType']
        itemTypeData = GB_TED.datas.get(_subType)
        if itemTypeData:
            _school = itemTypeData['RemindClass']
            if _school and _school != school:
                return gameconst.ItemBindType.NORMAL

def _checkDropCondition(dropDataList, context):
    avatarLv = context.args.avatarLv
    # 邮件掉落不进行条件判断
    if 'school' not in context.extra:
        return dropDataList
    school = context.extra['school']
    retList = []
    for dropData in dropDataList:
        checkFail = False
        if dropData['dropCondition']:
            for condition in dropData['dropCondition']:
                tp = condition[0]
                if tp == gameconst.DropConditionType.DROP_CONDITION_TYPE_1:
                    minLv, maxLv = condition[1], condition[2]
                    if avatarLv < minLv or avatarLv > maxLv:
                        checkFail = True
                        break
                elif tp == gameconst.DropConditionType.DROP_CONDITION_TYPE_2:
                    if school != condition[1]:
                        checkFail = True
                        break
                elif tp == gameconst.DropConditionType.DROP_CONDITION_TYPE_3:
                    taskId = condition[1]
                    avatarId = context.extra['avatarId']
                    avatar = KBEngine.entities.get(avatarId)
                    if not avatar:
                        checkFail = True
                        break
                    DEBUG_MSG('checkDropCondition', avatar.taskInfo.tasks)
                    if not avatar.getTask(taskId) or avatar.isTaskComplete(taskId):
                        checkFail = True
                        break
                elif tp == gameconst.DropConditionType.DROP_CONDITION_TYPE_4:
                    if not utils.isInSiegeWarBiddingTime():
                        checkFail = True
                        break
        if not checkFail:
            retList.append(dropData)
    return retList

def _getDropAwardType1or2(dropPackage, dropType, dropCount, context):
    awardVal = AwardVal()
    dropDataList = DDP.dropPackageData.get(dropPackage)
    if dropDataList:
        dropDataList = _checkDropCondition(dropDataList, context)
        if len(dropDataList) == 0:
            WARNING_MSG("dropDataList is empty, dropPackage: %s" % dropPackage)
            return awardVal
        weights = []
        for dropData in dropDataList:
            weights.append(dropData['weight'])
        indices = range(len(weights))
        for i in range(dropCount):
            if i >= len(indices) and dropType == gameconst.DropWayType.DROP_WAY_TYPE_1:
                break
            idx = random.choices(indices, weights=weights, k=1)[0]
            if dropType == gameconst.DropWayType.DROP_WAY_TYPE_1:
                weights[idx] = 0
            dropTargetData = dropDataList[idx]
            dropTargetList, numMinList, numMaxList, bindWeightList = _getRealDropTarget(dropTargetData, context)
            for dropTarget, numMin, numMax, bindWeight in zip(dropTargetList, numMinList, numMaxList, bindWeightList):
                if dropTarget:
                    num = random.randint(numMin, numMax)
                    bindType = _getBindType(dropTarget, bindWeight, context)
                    awardVal.addWealthByItemId(dropTarget, num, bindType)
                else:
                    WARNING_MSG("subPackage dropTarget is None, dropTarget: %s" % dropTargetData['dropTarget'])
    else:
        WARNING_MSG("dropPackage is None, dropPackage: %s" % dropPackage)

    return awardVal


def _getDropAwardType3(dropPackage, dropCount, context):
    awardVal = AwardVal()
    dropDataList = DDP.dropPackageData.get(dropPackage)
    if dropDataList:
        dropDataList = _checkDropCondition(dropDataList, context)
        if len(dropDataList) == 0:
            WARNING_MSG("dropDataList is empty, dropPackage: %s" % dropPackage)
            return awardVal
        for idx in range(len(dropDataList)):
            dropTargetData = dropDataList[idx]
            dropTargetList, numMinList, numMaxList, bindWeightList = _getRealDropTarget(dropTargetData, context)
            for dropTarget, numMin, numMax, bindWeight in zip(dropTargetList, numMinList, numMaxList, bindWeightList):
                if dropTarget:
                    num = 0
                    for i in range(dropCount):
                        num += random.randint(numMin, numMax)
                    bindType = _getBindType(dropTarget, bindWeight, context)
                    awardVal.addWealthByItemId(dropTarget, num, bindType)
                else:
                    WARNING_MSG("subPackage dropTarget is None, dropTarget: %s" % dropTargetData['dropTarget'])

    return awardVal


def _getDropAwardType4or5(dropPackage, dropType, dropCount, context):
    awardVal = AwardVal()
    dropDataList = DDP.dropPackageData.get(dropPackage)
    if dropDataList:
        dropDataList = _checkDropCondition(dropDataList, context)
        if len(dropDataList) == 0:
            WARNING_MSG("dropDataList is empty, dropPackage: %s" % dropPackage)
            return awardVal
        for i in range(dropCount):
            for idx in range(len(dropDataList)):
                dropTargetData = dropDataList[idx]
                weight = dropTargetData['weight']
                if random.randint(1, 10000) <= weight:
                    dropTargetList, numMinList, numMaxList, bindWeightList = _getRealDropTarget(dropTargetData, context)
                    for dropTarget, numMin, numMax, bindWeight in zip(dropTargetList, numMinList, numMaxList, bindWeightList):
                        if dropTarget:
                            num = random.randint(numMin, numMax)
                            bindType = _getBindType(dropTarget, bindWeight, context)
                            awardVal.addWealthByItemId(dropTarget, num, bindType)
                        else:
                            WARNING_MSG("subPackage dropTarget is None, dropTarget: %s" % dropTargetData['dropTarget'])
                    
                    if dropType == gameconst.DropWayType.DROP_WAY_TYPE_5:
                        break

    return awardVal


def _getDropAward(dropIDList, context):
    awardVal = AwardVal()
    for dropID in dropIDList:
        dropData = DDI.datas.get(dropID)
        if dropData:
            dropPackage = dropData['dropPackage']
            dropType = dropData['dropType']
            dropCount = dropData['dropCount']

            if dropType == gameconst.DropWayType.DROP_WAY_TYPE_1 or dropType == gameconst.DropWayType.DROP_WAY_TYPE_2:
                awardVal += _getDropAwardType1or2(dropPackage, dropType, dropCount, context)
            elif dropType == gameconst.DropWayType.DROP_WAY_TYPE_3:
                awardVal += _getDropAwardType3(dropPackage, dropCount, context)
            elif dropType == gameconst.DropWayType.DROP_WAY_TYPE_4 or dropType == gameconst.DropWayType.DROP_WAY_TYPE_5:
                awardVal += _getDropAwardType4or5(dropPackage, dropType, dropCount, context)
        else:
            WARNING_MSG("dropData is None, dropID: %s" % dropID)

    return awardVal


def getAwardOne(awardId, context, isNeedDisturb=False):
    awardId = dataUtils.getRealRewardId(awardId, context)
    award = AwardVal()
    awardData = RDDT.datas.get(awardId, {})
    resourceFixReward = awardData.get('resourceFixReward')
    resourceExReward = awardData.get('resourceExReward')

    fixAward = awardData.get('fixReward')
    fixRewardBaseOnSexual = awardData.get('fixRewardBaseOnSexual')
    nestFixAward = awardData.get('nestFixReward')
    exAward = awardData.get('exReward')
    nextedExtAward = awardData.get('nestExReward')
    singleAward = awardData.get('singleReward')

    fixPetReward = awardData.get('fixPetReward')
    singlePetReward = awardData.get('singlePetReward')
    exPetReward = awardData.get('exPetReward')

    dropID = awardData.get('dropID')

    for awardItem in award.getNumericWealth():
        awardNum = awardData.get(awardItem.configName)
        if not awardNum:
            continue

        if callable(awardNum):
            awardItem.data += int(awardNum(context.args))
        else:
            awardItem.data += int(awardNum)

    # titleId = awardData.get('title')
    # titleId and award.titleWealth.data.append(WealthTitleOne(titleId, -1))
    #
    # petData = awardData.get('pet')
    # petData and award.petWealth.data.append(petData)

    fightProps = awardData.get('fightProp')
    fightProps and award.fightProps.data.extend(fightProps)

    # outfitWealthIds = awardData.get('outfitID')
    # outfitWealthIds and award.outfitWealth.data.extend(list(outfitWealthIds))

    if resourceFixReward:
        award += _getResourceFixReward(awardId, context)

    if resourceExReward:
        award += _getResourceExReward(awardId, context)

    if fixAward:
        award += _getFixedAward(fixAward, context, gameconst.ItemType.Normal)

    if fixRewardBaseOnSexual:
        award += _getFixRewardBaseOnSexual(awardId, context)

    if nestFixAward:
        award += _getNestedFixAward(awardId, context, isNeedDisturb)

    if exAward:
        award += _getExtraAward(exAward, context, gameconst.ItemType.Normal)

    if nextedExtAward:
        award += _getNestedExAward(awardId, context, isNeedDisturb)

    if singleAward:
        award += _getSinAward(singleAward, context, gameconst.ItemType.Normal)

    if fixPetReward:
        award += _getFixedAward(fixPetReward, context, gameconst.ItemType.LingShou)

    if singlePetReward:
        award += _getSinAward(singlePetReward, context, gameconst.ItemType.LingShou)

    if exPetReward:
        award += _getExtraAward(exPetReward, context, gameconst.ItemType.LingShou)

    if dropID:
        award += _getDropAward(dropID, context)

    return award


def getAward(awardId, num, context, isNeedDisturb=False):
    award = AwardVal()
    for i in range(num):
        award += getAwardOne(awardId, context, isNeedDisturb)
    return award
