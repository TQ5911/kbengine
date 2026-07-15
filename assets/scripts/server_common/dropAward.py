import KBEngine
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
import rank_rankDrop as R_RD


class WealthUnit(userType.UserSingleType):
    def __getstate__(self):
        return self.data

    def __str__(self):
        return str(vars(self))

    def __bool__(self):
        return bool(self.data)

    def __setstate__(self, state):
        self.data = state
        return self


class WealthNumeric(WealthUnit):
    def __init__(self, configName, itemId, data):
        self.itemId = itemId
        self.configName = configName
        self.data = data

    def __mul__(self, factor):
        self.data = int(self.data * factor)
        return self

    def __add__(self, other):
        self.data += other.data
        return self
    
    def clear(self):
        self.data = 0

    def isEqual(self, other):
        return self.data == other.data


class WealthItem(WealthUnit):
    def __init__(self, data=None, itemObjs=None):
        self.data = data or {}
        if itemObjs is None:
            itemObjs = []

        self.itemsObjs = list(filter(lambda it: it.itemNum > 0, itemObjs))

    def __mul__(self, factor):
        delItemList = []
        for itemId, awardInfo in self.data.items():
            delTypeList = []
            for bindType, num in awardInfo.items():
                val = num * factor
                base = math.floor(val)
                frac = val - base
                newNum = base
                if random.random() < frac:
                    newNum += 1
                if newNum <= 0:
                    delTypeList.append(bindType)
                else:
                    awardInfo[bindType] = newNum
            for bindType in delTypeList:
                del awardInfo[bindType]
            if not awardInfo:
                delItemList.append(itemId)
        for itemId in delItemList:
            del self.data[itemId]

        addItemsObjs = []
        delItemsList = []
        for it in self.itemsObjs:
            val = factor # 默认itemnum 是1
            base = math.floor(val)
            frac = val - base
            newNum = base
            if random.random() < frac:
                newNum += 1
            if newNum <= 0:
                delItemsList.append(it)
            elif newNum > 1:
                for num in range(0, newNum-1):
                    newItem = itemFactory.ItemFactory.forkItemObject(it)
                    newItem.uniqueId = KBEngine.genUUID64()
                    addItemsObjs.append(newItem)
        for it in delItemsList:
            self.itemsObjs.remove(it)
        self.itemsObjs.extend(addItemsObjs)

    def __add__(self, other):
        for _itemId, AwardInfo in other.data.items():
            self.data.setdefault(_itemId, {})
            for bindType, num in AwardInfo.items():
                self.data[_itemId].setdefault(bindType, 0)
                self.data[_itemId][bindType] += num

        self.itemsObjs.extend(other.itemsObjs)

        return self

    def __setstate__(self, state):
        self.data = state['data']
        self.itemsObjs = state['itemObjs']

    def __getstate__(self):
        return {'data': self.data, 'itemObjs': self.itemsObjs}

    def _lateReload(self):
        super(WealthItem, self)._lateReload()
        for _it in self.itemsObjs:
            _it.reloadScript()

    def __bool__(self):
        return bool(self.data or self.itemsObjs)

    def addAwardItem(self, itemId, itemNum, bindType):
        if bindType < 0:
            bindType = dataUtils.getItemDefaultBindType()

        if bindType not in (gameconst.ItemBindType.BIND, gameconst.ItemBindType.NORMAL):
            gameengine.panicStack('invalid bindType', itemId, itemNum, bindType)
            return

        self.data.setdefault(itemId, {}).setdefault(bindType, 0)
        self.data[itemId][bindType] += itemNum

    def toItemObjs(self, extra):
        self.itemsObjs = self.getItemObjs(extra=extra)
        self.data = {}

    def addItemObjs(self, its):
        self.itemsObjs.extend(its)

    def getItemObjs(self, remove=False, extra={}):
        _itemList = []
        for _itemId, awardInfo in self.data.items():
            for _bindType, num in awardInfo.items():
                if not num:
                    continue
                _itemList.extend(itemFactory.ItemFactory.createItemList(_itemId, num, _bindType, extra=extra))

        _itemList.extend(self.itemsObjs)
        if remove:
            self.clear()

        return _itemList

    def popDropEquipObjs(self):
        _otherObjs = []
        equipList = []
        for it in self.itemsObjs:
            if it.isEquipmentItem():
                equipList.append(it)
            else:
                _otherObjs.append(it)
        self.itemsObjs = _otherObjs
        return equipList

    def popDropPetItemObjs(self):
        _otherObjs = []
        petItemList = []
        for it in self.itemsObjs:
            if dataUtils.isLingShouItem(it.itemId):
                petItemList.append(it)
            else:
                _otherObjs.append(it)
        self.itemsObjs = _otherObjs
        return petItemList
    
    def popSoulItemObjs(self, extra):
        soulList = []
        _otherObjs = []
        soulList = []
        for it in self.itemsObjs:
            if it.isSoul():
                soulList.append(it)
            else:
                _otherObjs.append(it)
        self.itemsObjs = _otherObjs

        for itemId in list(self.data.keys()):
            if dataUtils.getItemSubType(itemId) in gameconst.ItemSubEnum.EQUIP_SOUL_TYPE:
                datas = self.data.pop(itemId)
                for bindType, itemNum in datas.items():
                    soulList.extend(itemFactory.ItemFactory.createItemList(itemId, itemNum, bindType, extra=extra))
        return soulList

    def popExtractRewardItems(self):
        _extractRewardItemsDic = {}
        for _itemId in list(self.data.keys()):
            _itemData = dataUtils.getCommItemData(_itemId)
            if not _itemData:
                LOG_WARN('popExtractRewardItems, no _itemData:', self.data)
                continue
            if _itemData['type'] == gameconst.ItemEnum.Normal and _itemData[
                'subType'] == gameconst.ItemSubEnum.ExtractReward:
                _extractRewardItemsDic[_itemId] = self.data.pop(_itemId)
        return _extractRewardItemsDic

    def popRemainBagLimitItems(self, canAddNum):
        bagLimitItemsDic = {}
        # 将物品列表中的背包限制物品数量累加到data中
        newItemsObjs = []
        for item in self.itemsObjs:
            itemId = item.itemId
            if itemId in IDIDS.categoryDatas.get(gameconst.BAG_LIMIT_ITEM_TYPE_DATA, set()):
                totalNum = item.itemNum
                bindType = item.bindType

                itemData = self.data.get(itemId, None)
                if not itemData:
                    itemData = {}
                    self.data[itemId] = itemData
                itemData[bindType] = itemData.get(bindType, 0) + totalNum
            else:
                newItemsObjs.append(item)
        self.itemsObjs = newItemsObjs
        
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
            LOG_INFO('popRemainBagLimitItems:', bagLimitItemsDic, canAddNum)
        return bagLimitItemsDic

    def clear(self):
        self.data = {}
        self.itemsObjs = []

    def updateBindType(self, awardContext, bindType):
        if bindType not in gameconst.ItemBindType.VALID_BIND_TYPE:
            LOG_ERR('updateBindType, invalid bind type:', bindType, gameconst.ItemBindType.VALID_BIND_TYPE)
            return

        for itemID, wealthData in self.data.items():
            totalNum = 0
            for _, num in wealthData.items():
                totalNum += num
            self.data[itemID] = {bindType:totalNum}

        for itemsObj in self.itemsObjs:
            itemsObj.setItemBind(bindType)

class WealthTitleOne(userType.UserSingleType):
    def __init__(self, titleId, startTime=-1):
        self.titleId = titleId
        self.startTime = startTime
        if startTime == -1:
            self.startTime = utils.curTS()

    def toStreamSavedDic(self):
        return {'titleId': self.titleId, 'startTime': self.startTime}


class WealthTitle(WealthUnit):
    def __init__(self, data=None):
        # data: list of title id
        self.data = data or []

    def __add__(self, other):
        self.data.extend(other.data)
        return self
    
    def createFromTitleList(self, titleList):
        if not titleList:
            return
        for titleId in titleList:
            self.data.append(WealthTitleOne(titleId))

    def clear(self):
        self.data = []

    def __mul__(self, factor):
        # 没有策划特殊需求，暂时不处理
        return self


class WealthFightProp(WealthUnit):
    def __init__(self, data=None):
        self.data = data or []

    def __mul__(self, factor):
        # 没有策划特殊需求，暂时不处理
        return self

    def clear(self):
        self.data = []

    def __add__(self, other):
        self.data.extend(other.data)
        return self

    
class WealthResDic(WealthUnit):
    def __init__(self, data=None):
        self.data = data or {}

    def __bool__(self):
        return sum(self.data.values()) > 0

    def __add__(self, other):
        for _itemId, num in other.data.items():
            self.data[_itemId] = self.data.get(_itemId, 0)+num

        return self

    def clear(self):
        self.data = {}

class WealthVal(userType.UserSingleType):
    def __getstate__(self):
        st = {}
        for _k, _v in vars(self).items():
            if _v:
                st[_k] = _v.__getstate__()
        return st

    def __str__(self):
        return str(vars(self))

    def __setstate__(self, state):
        self.__init__()
        for k, _v in state.items():
            self.__dict__[k].__setstate__(_v)

    def __str__(self):
        s = {}
        for k, _v in vars(self).items():
            if not isinstance(_v, WealthUnit):
                if _v:
                    s[k] = str(_v)
            elif _v.data:
                s[k] = str(_v.__getstate__())
        return str(s)

    def getAllWealth(self):
        pass

    def getNumericWealth(self):
        pass

    def isEmpty(self):
        return not any(self.getAllWealth())

    def addWealthByItemId(self, itemId, num, bindType):
        pass

    def scrubWealthItemObjs(self, *args, **kwargs):
        """API: 清洗itemObj中数据"""


class AwardMixin(object):
    def getItemsDic(self):
        # 获得所有有效item的数量信息, 记录日志, 爬塔奖励展示 使用
        _itemsDic = {}
        for numericWealth in self.getNumericWealth():
            if numericWealth:
                _itemsDic[numericWealth.itemId] = numericWealth.data
        for _itemId, itemInfo in self.itemWealth.data.items():
            for _, num in itemInfo.items():
                _itemsDic[_itemId] = _itemsDic.get(_itemId, 0) + num
        for it in self.itemWealth.itemsObjs:
            _itemsDic[it.itemId] = _itemsDic.get(it.itemId, 0) + it.itemNum

        for itemId, itemInfo in self.petItemWealth.data.items():
            for _, num in itemInfo.items():
                _itemsDic[itemId] = _itemsDic.get(itemId, 0) + num
        for it in self.petItemWealth.itemsObjs:
            _itemsDic[it.itemId] = _itemsDic.get(it.itemId, 0) + it.itemNum
        return _itemsDic

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
    
    def scaleUpByMult(self, multVal):
        if multVal <= 0:
            gameengine.panicStack(f"Unsupported mult val: 'scaleUpByMult' and '{multVal}'")
            return self
        
        for numericWealth in self.getNumericWealth():
            numericWealth.data *= multVal

        for itemId, itemInfo in self.itemWealth.data.items():
            for k, _ in itemInfo.items():
                itemInfo[k] *= multVal

        for itemId, itemInfo in self.petItemWealth.data.items():
            for k, _ in itemInfo.items():
                itemInfo[k] *= multVal

        for it in self.itemWealth.itemsObjs:
            it.itemNum *= multVal

        for it in self.petItemWealth.itemsObjs:
            it.itemNum *= multVal
        return self

    def itemDataIter(self):
        for itemId, itemInfo in self.itemWealth.data.items():
            for _, num in itemInfo.items():
                yield itemId, num

        for itemId, itemInfo in self.petItemWealth.data.items():
            for _, num in itemInfo.items():
                yield itemId, num

    def itemObjIter(self):
        for it in self.itemWealth.itemsObjs:
            yield it

        for it in self.petItemWealth.itemsObjs:
            yield it



class BaseAwardVal(WealthVal, AwardMixin):

    def __init__(self, exp=0, coin=0, money=0, guildContrib=0, itemObjs=None, titleList=None, guildFund=0, guildExp=0, darkIron=0, guildMoney=0, bindMoney=0, appearanceCoin=0, guildCommission=0):
        self.exp = WealthNumeric('exp', gameconst.ItemIdEnum.EXP, exp)
        self.coin = WealthNumeric('coin', gameconst.ItemIdEnum.COIN, coin)
        self.money = WealthNumeric('money', gameconst.ItemIdEnum.MONEY, money)
        self.darkIron = WealthNumeric('darkIron', gameconst.ItemIdEnum.DARK_IRON, darkIron)
        self.guildContrib = WealthNumeric('guildContrib', gameconst.ItemIdEnum.GUILD_CONTRIB, guildContrib)
        self.guildMoney = WealthNumeric('guildMoney', gameconst.ItemIdEnum.GUILD_MONEY, guildMoney)
        self.guildFund = WealthNumeric('guildFund', gameconst.ItemIdEnum.GUILD_FUND, guildFund)
        self.guildExp = WealthNumeric('guildExp', gameconst.ItemIdEnum.GUILD_EXP, guildExp)
        self.bindMoney = WealthNumeric('boundMoney', gameconst.ItemIdEnum.BIND_MONEY, bindMoney)
        self.appearanceCoin = WealthNumeric('appearanceCoin', gameconst.ItemIdEnum.APPEARANCE_COIN, appearanceCoin)
        self.guildCommission = WealthNumeric('guildCommission', gameconst.ItemIdEnum.GUILD_COMMISSION, guildCommission)

        self.petItemWealth = WealthItem()
        self.itemWealth = WealthItem()
        self.addWealthByObjList(itemObjs)

        self.titleWealth = WealthTitle()
        self.titleWealth.createFromTitleList(titleList)

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
        self.guildContrib += other.guildContrib
        self.itemWealth += other.itemWealth
        self.petItemWealth += other.petItemWealth
        self.guildMoney += other.guildMoney
        self.guildFund += other.guildFund
        self.guildExp += other.guildExp
        self.bindMoney += other.bindMoney
        self.appearanceCoin += other.appearanceCoin

        self.titleWealth += other.titleWealth
        self.guildCommission += other.guildCommission

        return self
    
    def __mul__(self, factor):
        """重写乘法操作"""
        if not isinstance(factor, (int, float)):
            gameengine.panicStack(f"Unsupported operand type(s) for *: 'BaseAwardVal' and '{type(factor).__name__}'")
            return self
        
        for attr in self.getAllWealth():
            attr *= factor
        
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
        for _k, v in state.items():
            self.__dict__[_k].__setstate__(v)

    def getNumericWealth(self):
        return (self.exp, self.coin, self.money, self.guildContrib, self.guildFund, self.guildExp, self.darkIron, self.guildMoney, self.bindMoney, self.appearanceCoin, self.guildCommission)

    def getBaseNumeric(self):
        return (self.coin, self.money, self.guildContrib, self.darkIron, self.bindMoney, self.appearanceCoin)

    def getAllWealth(self):
        return self.getNumericWealth() + (self.itemWealth, self.petItemWealth, self.titleWealth,)

    def clear(self):
        for wealth in self.getAllWealth():
            wealth.clear()
        return

    def getNoObjItemDic(self):
        _itemsDic = {}
        for numericWealth in self.getNumericWealth():
            if numericWealth:
                _itemsDic[numericWealth.itemId] = numericWealth.data
        return _itemsDic

    def getItemsTLogStr(self):
        # 记录日志使用
        _itemsStr = ''
        for itemId, itemNum in self.getItemsDic().items():
            _itemsStr += str(itemId) + ',' + str(itemNum) + ';'
        return _itemsStr.strip(';')

    def addWealthByItemId(self, itemId, num, bindType=dataUtils.getItemDefaultBindType(), **kwargs):
        if not num:
            return self

        for _awardItem in self.getNumericWealth():
            if itemId == _awardItem.itemId:
                _awardItem.data += num
                return self

        _itemData = dataUtils.getCommItemData(itemId) or {}
        if not _itemData:
            gameengine.panicStack('BaseAwardVal::addWealthByItemId, not support itemId:', itemId)
            return self

        _type = _itemData.get('type')
        if _type == gameconst.ItemEnum.Normal:
            if _itemData['subType'] in itemFactory.ItemFactory.NormalItemClassMap:
                itemObjs = itemFactory.ItemFactory.createItemList(itemId, num, bindType, **kwargs)
                self.itemWealth.addItemObjs(itemObjs)
            else:
                self.itemWealth.addAwardItem(itemId, num, bindType)
        elif _type == gameconst.ItemEnum.LingShou:
            if _itemData['subType'] in itemFactory.ItemFactory.LingShouItemClassMap:
                itemObjs = itemFactory.ItemFactory.createItemList(itemId, num, bindType, **kwargs)
                self.petItemWealth.addItemObjs(itemObjs)
            else:
                self.petItemWealth.addAwardItem(itemId, num, bindType)
        elif _type == gameconst.ItemEnum.Title:
            self.titleWealth.data.append(WealthTitleOne(itemId))

        return self

    def addWealthByObjList(self, itemObjs):
        if not itemObjs:
            return
        # LOG_INFO('in addWealthByObjList:', [it.itemId for it in itemObjs])
        itemObjs = list(filter(lambda it: it.itemNum > 0, itemObjs))
        normalItemList = []
        petItemList = []
        for it in itemObjs:
            if it.itemNum == 0:
                continue
            itemData = dataUtils.getCommItemData(it.itemId)
            itemType = itemData.get('type')
            if itemType == gameconst.ItemEnum.LingShou:
                petItemList.append(it)
            else:
                normalItemList.append(it)
        normalItemList and self.itemWealth.addItemObjs(normalItemList)
        petItemList and self.petItemWealth.addItemObjs(petItemList)
        return self

    def getPetItemObjs(self):
        return self.petItemWealth.itemsObjs

    def scrubWealthItemObjs(self, createTime=-1):
        for _object in self.itemWealth.itemsObjs:
            if createTime > 0:
                _object.createTime = createTime
        for _object in self.petItemWealth.itemsObjs:
            if createTime > 0:
                _object.createTime = createTime

    def setAwardItemBindType(self, awardContext, bindType):
        self.itemWealth.updateBindType(awardContext, bindType)
        self.petItemWealth.updateBindType(awardContext, bindType)

class AwardVal(BaseAwardVal):
    def __init__(self, exp=0, coin=0, money=0, fightPropList=None, itemObjs=None, titleList=None, **kwargs):
        super().__init__(exp=exp, coin=coin, money=money, itemObjs=itemObjs, titleList=titleList, **kwargs)
        self.fightProps = WealthFightProp(fightPropList)
        return

    def __add__(self, other):
        super().__add__(other)
        self.fightProps += other.fightProps
        return self
    
    def __mul__(self, factor):
        """重写乘法操作"""
        if not isinstance(factor, (int, float)):
            gameengine.panicStack(f"Unsupported operand type(s) for *: 'AwardVal' and '{type(factor).__name__}'")
            return self
        super().__mul__(factor)
        return self

    def getAllWealth(self):
        return super(AwardVal, self).getAllWealth() +(self.fightProps,)

    def processAntiAddict(self, owner, isNotify, srcType, detail):
        return self

    def toClientDisplayVal(self):
        _retList = []
        _retList.append([{'itemId': itemId, 'itemNum': num} for itemId, num in self.getNoObjItemDic().items()])
        _retList.append([{'itemId': i.itemId, 'itemNum': i.itemNum, 'bindType': i.bindType} for i in self.itemWealth.getItemObjs()])
        _retList.append([{'itemId': i.itemId, 'itemNum': i.itemNum, 'bindType': i.bindType} for i in self.petItemWealth.getItemObjs()])
        return _retList


class DeductWealthVal(WealthVal, AwardMixin):
    def __init__(self, coin=0, money=0, itemsDic=None, petItemsDic=None, guildContrib=0, guildFund=0, guildExp=0, darkIron=0, guildMoney=0, bindMoney=0, appearanceCoin=0, guildCommission=0):
        self.coin = WealthNumeric('coin', gameconst.ItemIdEnum.COIN, coin)
        self.money = WealthNumeric('', gameconst.ItemIdEnum.MONEY, money)
        self.darkIron = WealthNumeric('darkIron', gameconst.ItemIdEnum.DARK_IRON, darkIron)
        self.guildContrib = WealthNumeric('guildContrib', gameconst.ItemIdEnum.GUILD_CONTRIB, guildContrib)
        self.itemWealth = WealthItem(itemsDic)
        self.petItemWealth = WealthItem(petItemsDic)
        self.guildMoney = WealthNumeric('guildMoney', gameconst.ItemIdEnum.GUILD_MONEY, guildMoney)
        self.guildFund = WealthNumeric('guildFund', gameconst.ItemIdEnum.GUILD_FUND, guildFund)
        self.guildExp = WealthNumeric('guildExp', gameconst.ItemIdEnum.GUILD_EXP, guildExp)
        self.bindMoney = WealthNumeric('bindMoney', gameconst.ItemIdEnum.BIND_MONEY, bindMoney)
        self.appearanceCoin = WealthNumeric('appearanceCoin', gameconst.ItemIdEnum.APPEARANCE_COIN, appearanceCoin)
        self.guildCommission = WealthNumeric('guildCommission', gameconst.ItemIdEnum.GUILD_COMMISSION, guildCommission)

    def __getstate__(self):
        st = {}
        for k, v in vars(self).items():
            if not v:
                continue
            st[k] = v.__getstate__()
        return st

    def __setstate__(self, state):
        self.__init__()
        for _k, _v in state.items():
            self.__dict__[_k].__setstate__(_v)

    def getNumericWealth(self):
        return (self.coin, self.money, self.guildContrib, self.darkIron, self.bindMoney, self.appearanceCoin)

    def getAllWealth(self):
        return self.getNumericWealth() + (self.itemWealth, self.petItemWealth)

    def addWealthByItemDict(self, itemDict):
        """通过老的itemDict形式加入物品

            type itemDict: {itemID_1: [itemNum_1, bindType_1], ...}
        """
        for _itemId, (itemNum, bindType) in itemDict.items():
            self.addWealthByItemId(_itemId, itemNum, bindType)

    def addWealthByItemId(self, itemId, num, bindType=dataUtils.getItemDefaultBindType()):
        for awardItem in self.getNumericWealth():
            if itemId == awardItem.itemId:
                awardItem.data += num
                return self

        itemType = dataUtils.getCommItemData(itemId).get('type')
        if itemType == gameconst.ItemEnum.Normal:
            self.itemWealth.addAwardItem(itemId, num, bindType)
        elif itemType == gameconst.ItemEnum.LingShou:
            self.petItemWealth.addAwardItem(itemId, num, bindType)
        else:
            LOG_ERR('DeductWealthVal error:', itemId, bindType, num)
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
                LOG_ERR('DeductWealthVal::addWealthByObjList, not support itemId:', it.itemId)
                continue
            itemData = dataUtils.getCommItemData(it.itemId)
            itemType = itemData.get('type')
            if itemType == gameconst.ItemEnum.LingShou:
                petItemList.append(it)
            else:
                normalItemList.append(it)
        normalItemList and self.itemWealth.addItemObjs(normalItemList)
        petItemList and self.petItemWealth.addItemObjs(petItemList)
        return self

    def scrubWealthItemObjs(self, createTime=-1):
        for _object in self.itemWealth.itemsObjs:
            if createTime > 0:
                _object.createTime = createTime
        for _object in self.petItemWealth.itemsObjs:
            if createTime > 0:
                _object.createTime = createTime


class MailAttachVal(BaseAwardVal):
    def __init__(self, exp=0, coin=0, money=0, itemObjs=None, **kwargs):
        super().__init__(exp=exp, coin=coin,  money=money, itemObjs=itemObjs, **kwargs)

    def __repr__(self):
        return "MailAttachVal(%s)" % self.toMailWealthDict()

    def getAllWealth(self):
        return super().getAllWealth()

    def __add__(self, other):
        super().__add__(other)
        return self

    def toMailWealthDict(self):
        _resItemList = []
        _bagItemList = []
        _bagItemObjList = []
        _titleList = []

        for awardItem in self.getNumericWealth():
            if awardItem.data>0:
                _resItemList.append({'itemId':awardItem.itemId, 'itemNum':awardItem.data})

        for _itemId, awardInfo in self.itemWealth.data.items():
            for bindType, itemNum in awardInfo.items():
                if not itemNum:
                    continue
                _bagItemList.append({'itemId':_itemId, 'itemNum':itemNum, 'bindType':bindType})

        for it in self.itemWealth.itemsObjs:
            _bagItemObjList.append(it.toItemSavedDict())

        for itemId, awardInfo in self.petItemWealth.data.items():
            for bindType, itemNum in awardInfo.items():
                if not itemNum:
                    continue
                _bagItemList.append({'itemId':itemId, 'itemNum':itemNum, 'bindType':bindType})

        for it in self.petItemWealth.itemsObjs:
            _bagItemObjList.append(it.toItemSavedDict())

        for titleWealthVal in self.titleWealth.data:
            _titleList.append({
                'titleId': titleWealthVal.titleId,
                'startTime': titleWealthVal.startTime,
            })

        return {
            'resItemList' : _resItemList,
            'bagItemList' : _bagItemList,
            'bagItemObjList' : _bagItemObjList,
            'titleList': _titleList,
        }

    def fromMailWealthDict(self, dic):
        self.clear()
        for _resItemDic in dic['resItemList']:
            self.addWealthByItemId(_resItemDic['itemId'], _resItemDic['itemNum'])

        for _bagItemDic in dic['bagItemList']:
            self.addWealthByItemId(_bagItemDic['itemId'], _bagItemDic['itemNum'], _bagItemDic['bindType'])
        
        _itemObjList = []
        for itemSavedDic in dic['bagItemObjList']:
            it = itemFactory.ItemFactory.createItemWithSavedDict(itemSavedDic)
            _itemObjList.append(it)
        self.addWealthByObjList(_itemObjList)

        for _titleDic in dic.get('titleList', []):
            self.titleWealth.data.append(WealthTitleOne(_titleDic['titleId'], _titleDic['startTime']))

        return self

    def addWealthByRewardId(self, rewardId):
        LOG_INFO('in addWealthByRewardId:', rewardId)
        wealthVal = getAward(rewardId, 1, awardContext.CommonContext(0))
        self.addWealthByAwardVal(wealthVal)
        return

    def addTitle(self, titleId, startTime):
        self.titleWealth.data.append(WealthTitleOne(titleId, startTime))

    def addWealthByAwardVal(self, wealthVal:AwardVal):
        LOG_INFO('in addWealthByAwardVal:', wealthVal)
        if wealthVal.isEmpty():
            return
        for _awardIt in wealthVal.getNumericWealth():
            if _awardIt.data <= 0:
                continue
            self.addWealthByItemId(_awardIt.itemId, _awardIt.data)

        self.addWealthByObjList(wealthVal.itemWealth.getItemObjs(remove=True))
        self.addWealthByObjList(wealthVal.petItemWealth.getItemObjs(remove=True))
        for _itemId, itemInfo in wealthVal.itemWealth.data.items():
            for _bindType, num in itemInfo.items():
                if num <= 0:
                    continue
                self.addWealthByItemId(_itemId, num, _bindType)

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
        _totalNum = 0
        for awardIt in self.getNumericWealth():
            if awardIt.data > 0:
                _totalNum += 1

        _totalNum += len(self.itemWealth.data) + len(self.itemWealth.itemsObjs)
        _totalNum += len(self.petItemWealth.data) + len(self.petItemWealth.itemsObjs)
        maxNum = MACF.datas['mailItemsNumMax']['value']
        ret = _totalNum > maxNum
        if ret:
            gameengine.panicStack('mailWealthExceedUplimit:', _totalNum, maxNum)
        return ret

    def getAwardVal(self):
        wealthVal = AwardVal(
            exp=self.exp.data,
            coin=self.coin.data,
            money=self.money.data,
            darkIron=self.darkIron.data,
            appearanceCoin=self.appearanceCoin.data,
            itemObjs=self.itemWealth.itemsObjs,
            guildContrib=self.guildContrib.data,
            guildMoney=self.guildMoney.data,
            guildFund=self.guildFund.data,
            guildExp=self.guildExp.data,
            bindMoney=self.bindMoney.data,
            titleList=[titleVal.titleId for titleVal in self.titleWealth.data],
            guildCommission=self.guildCommission.data,
        )

        for _itemId, itemInfo in self.itemWealth.data.items():
            for _bindType, num in itemInfo.items():
                if num <= 0:
                    continue
                wealthVal.addWealthByItemId(_itemId, num, _bindType)
            
        for _itemId, itemInfo in self.petItemWealth.data.items():
            for _bindType, num in itemInfo.items():
                if num <= 0:
                    continue
                wealthVal.addWealthByItemId(_itemId, num, _bindType)

        wealthVal.addWealthByObjList(self.petItemWealth.itemsObjs)
        return wealthVal

def _getResourceFixReward(awardId, context):
    _resourceFixReward = RDDT.datas[awardId]['resourceFixReward']
    ret = AwardVal()
    for _awardInfo in _resourceFixReward:
        _itemId, _itemNum = _awardInfo
        if callable(_itemId):
            _itemId = _itemId()
        _itemData = dataUtils.getCommItemData(_itemId)
        if _itemData.get('type') != gameconst.ItemEnum.Resource:
            continue
        if callable(_itemNum):
            _itemNum = int(_itemNum(context.args))  # context.args: srcLv, playerLevel
        else:
            _itemNum = int(_itemNum)
        ret.addWealthByItemId(_itemId, _itemNum)
    return ret

def _getDefaultBindType(itemId):
    gearDropBindProb = C_CD.datas['itemUnboundProb']['value']
    if random.uniform(0, 1) > gearDropBindProb:
        return gameconst.ItemBindType.BIND
    else:
        return gameconst.ItemBindType.NORMAL

def _genEquipItemList(itemId, itemNum, bindType, quality, context):
    dropParamDic = {
        'srcLevel': context.level or 0,
        'monsterId': context.monsterId or 0,
        'school': context.school or 0,
        'quality': quality or 0,
        'grade': context.grade or 1,
        'enhanceLv': context.enhanceLv or 0,
    }

    if itemId == gameconst.ItemIdEnum.COMMON_EQUIPMENT_ID:
        itemId = EquipmentItem.EquipItemIdGen.genEquipItemIdByDropData(**dropParamDic)
        LOG_INFO('_genEquipItemList, gen Equipitem ItemId:', itemId, dropParamDic)

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
        LOG_ERR('_genEquipItemList, no match equipment:', itemId, dropParamDic)
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
    _resourceExReward = RDDT.datas[awardId]['resourceExReward']
    ret = AwardVal()
    for _awardInfo in _resourceExReward:
        _itemId, _num, prob = _awardInfo
        if callable(_itemId):
            _itemId = _itemId()
        _itemData = dataUtils.getCommItemData(_itemId)
        if _itemData.get('type') != gameconst.ItemEnum.Resource:
            continue
        if callable(_num):
            _num = int(_num(context.args))  # context.args: srcLv
        else:
            _num = int(_num)
        if callable(prob):
            prob = prob(context.args)  # context.args: srcLv
        for j in range(_num):
            if random.randint(1, prob) == 1:
                ret.addWealthByItemId(_itemId, 1)
    return ret


def _getFixedAward(fixAward, context, itemType):

    _awardVal = AwardVal()
    for _awardInfo in fixAward:
        bindType = None
        quality = 0
        if len(_awardInfo) == 2:
            itemId, itemNum = _awardInfo
        elif len(_awardInfo) == 3:
            itemId, itemNum, bindType = _awardInfo
        else:
            itemId, itemNum, bindType, quality = _awardInfo
        if callable(itemId):
            itemId = itemId()
        itemData = dataUtils.getCommItemData(itemId)
        if not itemData:
            gameengine.panicStack(f"dropAward->_getFixedAward ::raise exception, missing item config in reward data, {fixAward}, {itemId}")
            continue
        if itemData.get('type') != itemType:
            continue
        if bindType is None:
            context.addContextVar('isNeedRegenBindType', True)
            bindType = _getDefaultBindType(itemId)

        if callable(itemNum):
            itemNum = int(itemNum(context.args))  # context.args: srcLv, playerLevel
        else:
            itemNum = int(itemNum)

        _addItemToAward(_awardVal, itemId, itemNum, bindType, quality, context)

    return _awardVal


def _getFixRewardBaseOnSexual(awardId, context):
    _fixRewardBaseOnSexual = RDDT.datas[awardId]['fixRewardBaseOnSexual']
    awardVal = AwardVal()
    if not _fixRewardBaseOnSexual:
        return awardVal
    for _awardInfo in _fixRewardBaseOnSexual[context.args.avatarSex]:
        bindType = None
        if len(_awardInfo) == 2:
            itemId, itemNum = _awardInfo
        elif len(_awardInfo) == 3:
            itemId, itemNum, bindType = _awardInfo

        if bindType is None:
            context.addContextVar('isNeedRegenBindType', True)
            bindType = _getDefaultBindType(itemId)

        itemData = dataUtils.getCommItemData(itemId)
        if itemData.get('type') != gameconst.ItemEnum.Normal:
            continue
        _addItemToAward(awardVal, itemId, itemNum, bindType, 0, context)

    return awardVal


def _getNestedFixAward(awardId, context, isNeedDisturb=False):
    nestedFixAward = RDDT.datas[awardId]['nestFixReward']
    ret = AwardVal()

    for _awardInfo in nestedFixAward:
        _needSchools = ()
        if len(_awardInfo) == 2:
            _innerAwardId, num = _awardInfo
        else:
            _innerAwardId, num, _needSchools = _awardInfo

        if _needSchools and context.school not in _needSchools:
            continue

        if callable(_innerAwardId):
            _innerAwardId = _innerAwardId()

        if callable(num):
            num = int(num(context.args))  # context.args: srcLv
        else:
            num = int(num)

        ret += getAward(_innerAwardId, num, context, isNeedDisturb)

    return ret


def _getExtraAward(exAward, context, itemType):
    _awardVal = AwardVal()
    for _awardInfo in exAward:
        bindType = None
        quality = None
        if len(_awardInfo) == 3:
            itemId, num, prob = _awardInfo
        elif len(_awardInfo) == 4:
            itemId, num, prob, bindType = _awardInfo
        else:
            itemId, num, prob, bindType, quality = _awardInfo

        if callable(itemId):
            itemId = itemId()
        itemData = dataUtils.getCommItemData(itemId)
        if itemData.get('type') != itemType:
            continue

        if bindType is None:
            context.addContextVar('isNeedRegenBindType', True)
            bindType = _getDefaultBindType(itemId)

        if callable(num):
            num = int(num(context.args))  # context.args: srcLv
        else:
            num = int(num)

        if callable(prob):
            prob = prob(context.args)  # context.args: srcLv

        for j in range(num):
            if random.randint(1, prob) == 1:
                _addItemToAward(_awardVal, itemId, 1, bindType, quality, context)
    return _awardVal


def _getNestedExAward(awardId, context, isNeedDisturb=False):
    nextedExtAward = RDDT.datas[awardId]['nestExReward']

    ret = AwardVal()

    for _awardInfo in nextedExtAward:
        if len(_awardInfo) == 3:
            (innerAwardId, num, prob), needSchools = _awardInfo, ()
        else:
            innerAwardId, num, prob, needSchools = _awardInfo

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

    _weighList = [oneRwData[2] for oneRwData in singleAward]
    _idx = utils.randomByWeight(_weighList)
    if _idx is not None:
        bindType = None
        quality = None
        if len(singleAward[_idx]) == 5:
            itemId, num, weight, bindType, quality = singleAward[_idx]
        if len(singleAward[_idx]) == 4:
            itemId, num, weight, bindType = singleAward[_idx]
        else:
            itemId, num, weight = singleAward[_idx]
        if callable(itemId):
            itemId = itemId()
        if bindType is None:
            context.addContextVar('isNeedRegenBindType', True)
            bindType = _getDefaultBindType(itemId)

        _itemData = dataUtils.getCommItemData(itemId)
        if _itemData.get('type') == gameconst.ItemEnum.Normal or _itemData.get('type') == gameconst.ItemEnum.LingShou:
            _addItemToAward(awardVal, itemId, num, bindType, quality, context)
    return awardVal

def _getBindWeightRank(extra):
    bindWeightRank = 0
    rank = extra['avatarScoreRank']
    isMonthCardExpired = extra['isMonthCardExpired']
    isBigMonthCardExpired = extra['isBigMonthCardExpired']
    isCrossServer = extra['isCrossServer']
    #只要有大or小月卡就吃月卡加成
    for _, v in R_RD.datas.items():
        l, r = v['rankRange'][0], v['rankRange'][1]
        if rank >= l and rank <= r:
            if v["isMonthCard"] and isMonthCardExpired:
                continue
            if v["isCrossServer"] == 0 and isCrossServer:
                continue
            bindWeightRank += v['bindWeightRank']
            break
        
    #大月卡专属加成
    for _, v in R_RD.datas.items():
        l, r = v['rankRange'][0], v['rankRange'][1]
        if rank >= l and rank <= r:
            #  【任务】大月卡特权调整+动态商品购买增加月卡特权 - 服务端
            if v["isMonthCard"] and (isBigMonthCardExpired or isMonthCardExpired):
                continue
            if v["isCrossServer"] == 0 and isCrossServer:
                continue
            bindWeightRank += v['bigBindWeightRank']
            break
    return bindWeightRank

def _calFinalBindWeight(dropTargetData, monthCard, bindWeightRank):
    #非绑概率只受配表影响
    if dropTargetData.get('unactedWeight', 0) == 1:
        return 10000 - dropTargetData.get('bindWeight', 10000)
    #非绑概率还受月卡、rank影响
    return 10000 - dropTargetData.get('bindWeight', 10000) - monthCard * dropTargetData.get('bindWeightMonth', 10000) - bindWeightRank

def _calSubPackDrop(dropTarget, times, context):
    #单次子包掉落与策划约定最大掉100次，如未来有需求更大得用numpy重构
    if times > 100:
        LOG_ERR("drop times is too large:", times, "dropTarget:", dropTarget, "context:", context)
        return [], [], [], [], []

    monthCard = 0 if context.extra['isMonthCardExpired'] else 1
    bindWeightRank = _getBindWeightRank(context.extra)

    dropSubPackageData = DDS.dropPackageData.get(dropTarget)
    if dropSubPackageData:
        dropSubPackageData = _checkDropCondition(dropSubPackageData, context)
        if len(dropSubPackageData) == 0:
            LOG_WARN("dropSubPackageData is empty, dropTarget: %s" % dropTarget)
            return [], [], [], [], []
        weights = []
        for dropData in dropSubPackageData:
            weights.append(dropData['weight'])
        data = random.choices(dropSubPackageData, weights=weights, k=times)
        dropTargetList = [item['dropTarget'] for item in data]
        numMinList = [item['dropNumMin'] for item in data]
        numMaxList = [item['dropNumMax'] for item in data]
        bindWeightList = [_calFinalBindWeight(item, monthCard, bindWeightRank) for item in data]
        gradeList = [item['grade'] for item in data]
        return dropTargetList, numMinList, numMaxList, bindWeightList, gradeList
    return [], [], [], [], []


#处理掉落子包还是掉落物品
def _getRealDropTarget(dropTargetData, context):
    monthCard = 0 if context.extra['isMonthCardExpired'] else 1
    bindWeightRank = _getBindWeightRank(context.extra)

    dropTargetList = [dropTargetData['dropTarget']]
    numMinList = [dropTargetData['dropNumMin']]
    numMaxList = [dropTargetData['dropNumMax']]
    bindWeightList = [_calFinalBindWeight(dropTargetData, monthCard, bindWeightRank)]
    gradeList = [dropTargetData['grade']]
    #子包
    if dropTargetData['dropType'] == gameconst.DropWayType.DROP_WAY_TYPE_2:
        (dropTargetList, numMinList, numMaxList, bindWeightList, gradeList) = _calSubPackDrop(dropTargetList[0], random.randint(numMinList[0], numMaxList[0]), context)
    return dropTargetList, numMinList, numMaxList, bindWeightList, gradeList


def _getBindType(itemID, bindWeight, context):
    if random.randint(1, 10000) <= bindWeight:
        return gameconst.ItemBindType.BIND
    else:
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
            LOG_WARN("dropDataList is empty, dropPackage: %s" % dropPackage)
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
            dropTargetList, numMinList, numMaxList, bindWeightList, gradeList = _getRealDropTarget(dropTargetData, context)
            for dropTarget, numMin, numMax, bindWeight, grade in zip(dropTargetList, numMinList, numMaxList, bindWeightList, gradeList):
                if dropTarget:
                    num = random.randint(numMin, numMax)
                    bindType = _getBindType(dropTarget, bindWeight, context)
                    awardVal.addWealthByItemId(dropTarget, num, bindType, grade = grade)
                else:
                    LOG_WARN("subPackage dropTarget is None, dropTarget: %s" % dropTargetData['dropTarget'])
    else:
        LOG_WARN("dropPackage is None, dropPackage: %s" % dropPackage)

    return awardVal


def _getDropAwardType3(dropPackage, dropCount, context):
    awardVal = AwardVal()
    dropDataList = DDP.dropPackageData.get(dropPackage)
    if dropDataList:
        dropDataList = _checkDropCondition(dropDataList, context)
        if len(dropDataList) == 0:
            LOG_WARN("dropDataList is empty, dropPackage: %s" % dropPackage)
            return awardVal
        for idx in range(len(dropDataList)):
            dropTargetData = dropDataList[idx]
            dropTargetList, numMinList, numMaxList, bindWeightList, gradeList = _getRealDropTarget(dropTargetData, context)
            for dropTarget, numMin, numMax, bindWeight, grade in zip(dropTargetList, numMinList, numMaxList, bindWeightList, gradeList):
                if dropTarget:
                    num = 0
                    for i in range(dropCount):
                        num += random.randint(numMin, numMax)
                    bindType = _getBindType(dropTarget, bindWeight, context)
                    awardVal.addWealthByItemId(dropTarget, num, bindType, grade = grade)
                else:
                    LOG_WARN("subPackage dropTarget is None, dropTarget: %s" % dropTargetData['dropTarget'])

    return awardVal


def _getDropAwardType4or5(dropPackage, dropType, dropCount, context):
    awardVal = AwardVal()
    dropDataList = DDP.dropPackageData.get(dropPackage)
    if dropDataList:
        dropDataList = _checkDropCondition(dropDataList, context)
        if len(dropDataList) == 0:
            LOG_WARN("dropDataList is empty, dropPackage: %s" % dropPackage)
            return awardVal
        for i in range(dropCount):
            for idx in range(len(dropDataList)):
                dropTargetData = dropDataList[idx]
                weight = dropTargetData['weight']
                if random.randint(1, 1000000) <= weight:
                    dropTargetList, numMinList, numMaxList, bindWeightList, gradeList = _getRealDropTarget(dropTargetData, context)
                    for dropTarget, numMin, numMax, bindWeight, grade in zip(dropTargetList, numMinList, numMaxList, bindWeightList, gradeList):
                        if dropTarget:
                            num = random.randint(numMin, numMax)
                            bindType = _getBindType(dropTarget, bindWeight, context)
                            awardVal.addWealthByItemId(dropTarget, num, bindType, grade = grade)
                        else:
                            LOG_WARN("subPackage dropTarget is None, dropTarget: %s" % dropTargetData['dropTarget'])

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
            LOG_WARN("dropData is None, dropID: %s" % dropID)

    return awardVal


def getAwardOne(awardId, context, isNeedDisturb=False):
    awardId = dataUtils.getRealRewardId(awardId, context)
    _award = AwardVal()
    _awardData = RDDT.datas.get(awardId, {})
    resourceFixReward = _awardData.get('resourceFixReward')
    resourceExReward = _awardData.get('resourceExReward')

    fixAward = _awardData.get('fixReward')
    fixRewardBaseOnSexual = _awardData.get('fixRewardBaseOnSexual')
    nestFixAward = _awardData.get('nestFixReward')
    exAward = _awardData.get('exReward')
    nextedExtAward = _awardData.get('nestExReward')
    singleAward = _awardData.get('singleReward')

    fixPetReward = _awardData.get('fixPetReward')
    singlePetReward = _awardData.get('singlePetReward')
    exPetReward = _awardData.get('exPetReward')

    dropID = _awardData.get('dropID')

    for _awardItem in _award.getNumericWealth():
        awardNum = _awardData.get(_awardItem.configName)
        if not awardNum:
            continue

        if callable(awardNum):
            _awardItem.data += int(awardNum(context.args))
        else:
            _awardItem.data += int(awardNum)

    titleId = _awardData.get('title')
    titleId and _award.titleWealth.data.append(WealthTitleOne(titleId, -1))

    fightProps = _awardData.get('fightProp')
    fightProps and _award.fightProps.data.extend(fightProps)

    if resourceFixReward:
        _award += _getResourceFixReward(awardId, context)

    if resourceExReward:
        _award += _getResourceExReward(awardId, context)

    if fixAward:
        _award += _getFixedAward(fixAward, context, gameconst.ItemEnum.Normal)

    if fixRewardBaseOnSexual:
        _award += _getFixRewardBaseOnSexual(awardId, context)

    if nestFixAward:
        _award += _getNestedFixAward(awardId, context, isNeedDisturb)

    if exAward:
        _award += _getExtraAward(exAward, context, gameconst.ItemEnum.Normal)

    if nextedExtAward:
        _award += _getNestedExAward(awardId, context, isNeedDisturb)

    if singleAward:
        _award += _getSinAward(singleAward, context, gameconst.ItemEnum.Normal)

    if fixPetReward:
        _award += _getFixedAward(fixPetReward, context, gameconst.ItemEnum.LingShou)

    if singlePetReward:
        _award += _getSinAward(singlePetReward, context, gameconst.ItemEnum.LingShou)

    if exPetReward:
        _award += _getExtraAward(exPetReward, context, gameconst.ItemEnum.LingShou)

    if dropID:
        _award += _getDropAward(dropID, context)
        
    if context.args and hasattr(context.args, 'factor'):
        _award *= context.args.factor

    return _award


def getAward(awardId, num, context, isNeedDisturb=False):
    award = AwardVal()
    for i in range(num):
        award += getAwardOne(awardId, context, isNeedDisturb)
    return award
