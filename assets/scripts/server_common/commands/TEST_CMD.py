# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from commands.CMD_COMMON import *
import gzip
import json
import utils
import dataUtils
import gameconfig
import gameengine
import dropAward
import awardContext
import buff_buff as BBD
import base64
import importlib
import inspect
import ast
import time
import types
import fightProp_define as FDD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD

# 判断当前进程类型
IS_BASE = (KBEngine.component == 'baseapp')
import skill_skill as SSD
import visible_visible as UVVD
import actionContext
import gamerefresh

callApps = gmCommand._callApps
forwardCommand = gmCommand.forwardCommand


@gm_cmd('$getAllGMCmds', (), RONE, BASE, '获取所有指令', ALLSIDE, GOD_GROUPS)
def getAllGMCmds(su):
    if KBEngine.publish():
        su.onCommandResult(0, 'can not run in publish server', {})
        return
    data = utils.man_gm_cmds()
    su.onCommandResult(0, 'ok' , {"data": data})

@gm_cmd('$getAllPlayers', (), RONE, BASE, '获取所有在线用户', ALLSIDE, GOD_GROUPS)
def getAllPlayers(su):
    if KBEngine.publish():
        su.onCommandResult(0, 'can not run in publish server', {})
        return
    gameengine.callBaseApps("utils.getAllAvatarByGm", (su, gameglobal.localBaseApp))

@gm_cmd('$getAvatarAoiMonster', (Player("gbId/Id"), Int("range")), RARG(0), CELL, '获取玩家AOI附近怪物', ALLSIDE, GOD_GROUPS, minArgs=1)
def getAvatarAoiMonster(su, player, range=30):
    monsterdata = []
    for ent in player.entitiesInRange(range, 'Monster'):
        monsterdata.append({'entityId': ent.id, 'MonsterName': ent.name})
    for ent in player.entitiesInRange(range, 'Summon'):
        monsterdata.append({'entityId': ent.id, 'MonsterName': ent.name})
    for ent in player.entitiesInRange(range, 'Creation'):
        monsterdata.append({'entityId': ent.id, 'MonsterName': ent.name})
    return su.onCommandResult(0, 'ok' , {"data": monsterdata})

@gm_cmd('$getEntprop', (Entity('entid'),), RARG(0), CELL, '获取实体属性', ALLSIDE, GOD_GROUPS)
def getEntprop(su, ent):
    entprops = {}
    for propName, propData in FDD.datas.items():
        if not hasattr(ent, propName):
            continue
        entprops[propName] = {
            "value": getattr(ent, propName),
            "name": propData['name']  
        }

    sorted_items = sorted(
    entprops.items(),
    key=lambda kv: 1 if kv[1]["value"] == 0 else 0
)
    entprops = {k: v for k, v in sorted_items}
    
    return su.onCommandResult(0, 'ok', {"data": entprops})

@gm_cmd('$setEntProp', (Entity('entid'),Str("propName"), Float("value"),), RARG(0), gameconst.CELL, '修改属性', ALLSIDE, GOD_GROUPS)
def setEntProp(su, ent, propName, value):
    if not hasattr(ent, propName):
        return su.onCommandResult(0, f'Faild,{ent.name} 没有 {propName} 属性', {})
    else:
        curVal = ent.getProp(propName)
        if type(curVal) is int:
            newvalue = int(value)
        else:
            newvalue = float(value)
        ent.setProp(f'{propName}', newvalue, gameconst.SourceType.Default)
        return su.onCommandResult(0, f'ok,{ent.name} 的 {propName} 属性从 {curVal} 修改为 {value}',{} )

@gm_cmd('$getEntSkillDic', (Entity('entid'),), RARG(0), gameconst.CELL, '获取实体技能信息', ALLSIDE, GOD_GROUPS)
def getEntSkillDic(su, ent):
    
    mod = importlib.import_module('skill_skill')
    datas = getattr(mod, 'datas', None)
    if not hasattr(ent, 'skillDic'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", ent.id)} 没有 skillDic 方法', {})
    weight_map = {}
    if hasattr(ent, 'IsMonster') and getattr(ent, 'skillPropInfo', None):
        skill_ids, weights = ent.skillPropInfo
        weight_map = {sid: w for sid, w in zip(skill_ids, weights)}
    entskilldic = {}
    for skill_id, skill_obj in ent.skillDic.items():        
        # 获取技能action
        try:
            action_func = datas.get(skill_id, {}).get('action', None)
            if action_func:
                skillaction = _getTableValue(action_func)
            else:
                skillaction = "None"
        except Exception as e:
            skillaction = f"<获取失败: {str(e)}>"
        
        entskilldic[skill_id] = {
            'skillid': skill_id,
            'name': skill_obj.getSkillName(skill_id),
            'skilllevel': skill_obj.skillLv,
            'weight': weight_map.get(skill_id),
            'action': skillaction
        }
    return su.onCommandResult(0, 'ok', entskilldic)


def update_skills_by_playerLevel(ent, playerLevel, skillLevel=0):
    import skill_skill as SSD
    import skillRelevant_skillUpgrade as SRSUD
    skill_dicts = {
    1001: {},
    1002: {},
    1003: {}  }
    level = playerLevel or getattr(ent, 'level', None) or gameglobal.roleCache.get(ent.id, {}).get('level', 0)
    #根据角色等级和技能levelLimit确定技能最多能升多少级
    def assign_skill_level(level_limit, player_level):
        if not level_limit:
            return 1

        # 找到角色等级能达到的最高技能等级
        max_skill_level = 1
        for skill_level_index, required_player_level in enumerate(level_limit):
            if player_level >= required_player_level:
                max_skill_level = skill_level_index + 1
            else:
                break

        return max_skill_level

    for skill_id, skill_info in SRSUD.datas.items():
        school_id = 1000 + int(str(skill_info.get('ID'))[3])  # 提取学校 ID
        if  school_id in skill_dicts:
            skill_dicts[school_id][skill_id] = skillLevel or assign_skill_level(skill_info.get('levelLimit', []), level)

    
    def update_skill_levels(self, skill_dict):
        skill_id_list = []
        skill_lv_list = []
        for skill_id, skill_lv in skill_dict.items():
            if skill_id not in self.buildDic.activeSkills:
                continue
            skill_id_list.append(skill_id)
            skill_lv_list.append(skill_lv)
            self.cell.onChangeSkillLv(skill_id, skill_lv)
            newLevel = skill_lv
            self.buildDic.skillLevels[skill_id] = newLevel
            self.updateSkillLevelSetSummonSlotIdx(skill_id, newLevel)

            recommendSlot = self.buildDic.getSkillRecommendSlot(self, skill_id)
            if recommendSlot is not None:
                self.buildDic.changeSkillSlot(self, skill_id, None, recommendSlot)

            # 被动技能替换的技能一并要升级
            relatedSkills = SSD.datas.get(skill_id, {}).get('conflictSkill') or ()
            skillIdList = [skill_id] + list(relatedSkills)
            for sid in relatedSkills:
                if sid in self.buildDic.skillLevels:
                    self.buildDic.skillLevels[sid] = newLevel
                    self.updateSkillLevelSetSummonSlotIdx(sid, newLevel)

                    recommendSlot = self.buildDic.getSkillRecommendSlot(self, sid)
                    if recommendSlot is not None:
                        self.buildDic.changeSkillSlot(self, sid, None, recommendSlot)

        self.client.onUpdateSkillLevel(skill_id_list, skill_lv_list)

    school = ent.getAvatarSchool()
    if school in skill_dicts:
        update_skill_levels(ent, skill_dicts[school])

def getPetItemList():
    import itemData_itemData as ID
    import petData_petData as PD
    petItemListValid = []
    for itemId, itemData in ID.datas.items():
        itemType = itemData.get('type', None)
        subType = itemData.get('subType', None)
        if itemType == gameconst.ItemType.LingShou and subType == gameconst.ItemSubType.LingShouEgg and (itemData.get('indexID', None) in PD.datas):
            petItemListValid.append(itemId)
    return petItemListValid


def _getItems(school, quality, awardCtx):
    import gearBase_typeExplanation as GBE
    import gearBase_gearBase as GBG
    _targetList = []
    for k, v in GBE.auctionDic.items():
        # k : (1, 1001), v: [(1, 11), (2, 21), (3, 31), (4, 41)]
        if k[1] != school:
            continue

        _targetList.extend(v)

    print('_targetList', _targetList)

    _itemIds = []
    for k, v in GBG.auctionDic.items():
        if (k[0], k[1]) not in _targetList:
            continue

        if k[2] != quality:
            continue
        for i in v:
            _itemIds.append(i)
            if k[0] == 6 or k[0] == 7:
                _itemIds.append(i)

    _items = []
    for _itemId in _itemIds:
        _items.extend(dropAward._genEquipItemList(_itemId, 1, 0, quality, awardCtx))

    return _items

@gm_cmd('$dropEquip', (Player("gbId/Id"), Int("slotId")), RARG(0), CELL, '丢装备', ALLSIDE, GOD_GROUPS)
def dropEquip(su, player, slotId):
    player.dropEquip(slotId, player.gbId, player.name)
    return True, '执行成功'

@gm_cmd('$dropWithoutDress', (Player("gbId/Id"), Int('count')), RARG(0), CELL, '丢装备', ALLSIDE, GOD_GROUPS)
def dropWithoutDress(su, player, count):
    _items = _getItems(player.school, 3, 3, awardContext.CommonContext(0))
    for _item in _items[:count]:
        player.dropEquipByItem(_item, player.name)

    return True, '执行成功'

def _gmGetEquipment(player, school, quality, grade, enhanceLv):
    import gearEnhance_gearconst as GEGCD
    import gearBase_typeTab as GBTT
    import gearEnhance_gearStrengthen as GEGS
    awardCtx = awardContext.CommonContext(0)
    awardVal = dropAward.AwardVal()
    if school == 0:
        school = player.getRoleCacheAttr('school', 0)
        if school == 0:
            DEBUG_MSG('gmGetEquipment: failed to fetch school from role cache, school=0')
            return False, '执行失败，玩家门派未知', []
    if quality not in gameconst.ItemQuality.COLL_QUALITY:
        return False, '执行失败，无效品质', []
    if not(0 < grade <= GEGCD.datas['equipmentClassLevel']['value']):
        return False, '执行失败，无效品阶', []
    for equipType in GBTT.datas.keys():
        key = equipType * 10000 + quality * 1000 + grade * 100 + enhanceLv
        if key not in GEGS.datas:
            return False, '执行失败，无效强化等级', []
        
    awardCtx.addContextVar('grade', grade)
    awardCtx.addContextVar('enhanceLv', enhanceLv)
    _items = _getItems(school, quality, awardCtx)

    awardVal.addWealthByObjList(_items)
    player.addWealth(
        AAC_AACDD.datas.BONUS_SRC_GM,
        awardVal,
        KBEngine.genUUID64(),
        detail="_gmGetEquipment",
        awardCtx=awardCtx,
        )
    return True, '执行成功', _items

@gm_cmd('$getEquipment', (Player("gbId/Id"), Int('school'), Int('quality'), Int('grade'), Int('enhanceLv')), RARG(0), BASE, '获得套装', ALLSIDE, GOD_GROUPS)
def gmGetEquipment(su, player, school, quality, grade, enhanceLv):
    ret, msg, _ = _gmGetEquipment(player, school, quality, grade, enhanceLv)
    return ret, msg
    

@gm_cmd('$enhanceRole', (Player("gbId/Id"),Int('enhanceLevel')), RARG(0), gameconst.BASE, '根据配置强化角色', ALLSIDE, GOD_GROUPS, minArgs=1)
def enhanceRole(su, player, enhanceLevel=0):
    # from test.roleStrengthConfig import data as roleStrengthData
    import random
    import gearEnhance_gearconst as GEGCD
    # 等级设置
    maxRoleLevel = utils.getPlayerMaxLevel()
    forwardCommand(su,"$setlv", player.id, maxRoleLevel)
    # 装备获取
    maxQuality = 4
    maxClassLevel = GEGCD.datas['equipmentClassLevel']['value']
    maxEnhanceLevel = len(GEGCD.datas['strengthenPercent']['value'])
    _, _, items = _gmGetEquipment(player, 0, maxQuality, maxClassLevel, maxEnhanceLevel)

    
    
    # 装备改造
    # 1.铭文 因为gm穿戴有延迟，所以先在包里处理铭文
    for equipItem in items:
        if equipItem.equipAttr.glyphSlotNum:
            affixList = equipItem.equipAttr._genGlyphAffix(2 * len(equipItem.equipAttr.glyphSlotNum))
            affixIds = [affix.getAffixId() for affix in affixList]
            for glyphPos in equipItem.equipAttr.glyphSlotNum:
                affixId1 = affixIds.pop(0) if affixIds else 0
                affixId2 = affixIds.pop(0) if affixIds else 0
                player.gmGlyphWashingEquips(equipItem.itemId, glyphPos, affixId1, affixId2)
            
    # forwardCommand(su, "$glyphWashingEquipmentsInEquip", player.id)
    # 2.祝福
    # 3.穿戴
    dressSlotIds = list(range(gameconst.BodyEquipSlot.EQUIP_WEAPON_SLOT, gameconst.BodyEquipSlot.EQUIP_BELT_SLOT + 1))
    player.gmBaseDressEquips(dressSlotIds, maxQuality)
    # 技能改造 
    # 1.技能升级
    update_skills_by_playerLevel(player, maxRoleLevel)
    # 精灵穿戴
    #  1.获得道具
    itemList = getPetItemList()
    bindType = 0
    for itemId in itemList:
        player.gmAddItems(0, itemId, 1, 'gm_cmd:$enhanceRole', bindType)
    #  2.使用道具
    import actionContext
    for itemId in itemList:
        gridId, it = player.petBag.getItemObjByItemID(itemId, bindType)
        abCtx = actionContext.AddLingShouCtx(gameconst.AddLingShouReason.normal, extra={'item': it, 'school':player.getAvatarSchool()})
        player.addLingShouBase(abCtx)
    #  3.设置出战
    battleIndex = player.battleIndex
    allPetIds = list(player.lingShouInfo.pets.keys())
    slotNum = len(player.lingShouInfo.getBattleListByIndex(battleIndex))
    slotNum = min(slotNum, len(allPetIds))
    petIds = random.sample(allPetIds, slotNum)
    for slotId, petId in enumerate(petIds):
        player.updateLingShouBattleList(player.id, battleIndex, petId, slotId)
    #  4.穿戴装备
    #  5.设置跟随
    player.cell.setFollowPet(True, petIds[0])

    # 收集系统
    # 经脉系统
    player.gmUnlockAllMeridian()
    return su.onCommandResult(0, 'ok', {})

@gm_cmd('$modifyAttrByLevel', (Player("gbId/Id"),Int('level')), RARG(0), gameconst.CELL, '根据等级设置角色属性', ALLSIDE, GOD_GROUPS)
def modifyAttrByLevel(su, player, level):
    from test import roleLevelAttribute
    
    roleAttrData = roleLevelAttribute.data.get(str(level), None)
    if not roleAttrData:
        return False, '执行失败，等级属性配置不存在'
    
    opUUID = KBEngine.genUUID64()
    src = AAC_AACDD.datas.BONUS_SRC_GM
    detail = gameclass.AwardDetail(gm_cmd='$setlv', level=level)
    player.levelUp(min(utils.getPlayerMaxLevel(), level), opUUID, src, detail)

    attrList = []
    for attrName, attrVal in roleAttrData.items():
        if attrName not in FDD.datas:
            continue
        if player.getProp(attrName) is None:
            continue
        delta = attrVal - player.getProp(attrName)  # 根据当前属性差值补足
        attrList.append(("adj" + attrName[0].upper() + attrName[1:], delta))
    forwardCommand(su, '$addAwardFightProps', player.id, str(attrList))

@gm_cmd('$setskillLv', (Player("gbId/Id"), Int("skillLevel"),), RARG(0), gameconst.BASE, '设置技能等级', ALLSIDE, GOD_GROUPS, minArgs=0)
def setskillLv(su, player, skillLevel=0):
    update_skills_by_playerLevel(player, 0, skillLevel)
    return True, '执行成功'

@gm_cmd('$addAwardFightProps', (Player("gbId/Id"),Str('attrList')), RARG(0), gameconst.BASE, '增加奖励战斗属性', ALLSIDE, GOD_GROUPS)
def addAwardFightProps(su, player, attrList):
    try:
        attrList = eval(attrList)
    except Exception as e:
        return False, f'执行失败，attrList格式错误: {str(e)}'
    player.addAwardFightProps(attrList, gameconst.SourceType.Item, 0, 0, "_gmAddAwardFightProps")
    return True, '执行成功'

@gm_cmd('$Alladdbuff', (Int("buffid"),), RALL, gameconst.CELL, '所有人添加buff', ALLSIDE, GOD_GROUPS)
def Alladdbuff(su, buffid):
    if buffid:
        for e in KBEngine.entities.values():
            if e.className == 'Avatar':
                e.addBuff(buffid,1,e.id)
    return True, '执行成功'

@gm_cmd('$AllsetskillLV', (Int("playerLevel"),), RALL, gameconst.BASE, '所有人技能升级', ALLSIDE, GOD_GROUPS, minArgs=0)
def AllsetskillLV(su, playerLevel=0):
    for e in KBEngine.entities.values():
        if e.className == 'Avatar':
            update_skills_by_playerLevel(e, playerLevel)
    return True, '执行成功'

@gm_cmd('$replaceMonsterSkill', (Entity('entid'),Str('skillList')), RARG(0), gameconst.CELL, '替换怪物技能', ALLSIDE, GOD_GROUPS)
def replaceMonsterSkill(su, ent, skillList):
    if not hasattr(ent, 'skillDic'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", ent.id)} 没有 skillDic 方法', {})
    if not hasattr(ent, 'IsMonster'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", ent.id)} 不是怪物', {})
    newSkillList = ast.literal_eval(skillList)
    ent.changeAllSkill(newSkillList)
    return su.onCommandResult(0, 'ok,替换成功', {})

@gm_cmd('$getEntBuffinfo', (Player("gbId/Id"),Int('entid')), RARG(0), gameconst.CELL, '获取实体buff信息', ALLSIDE, GOD_GROUPS)
def getEntBuffinfo(su, player,entid):
    import utils
    entbuffdic = {}
    ent = KBEngine.entities.get(entid)
    mod = importlib.import_module('buff_buff')
    datas = getattr(mod, 'datas', None)
    if not hasattr(ent, 'buffDic'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", entid)} 没有 buffDic 方法', {})
    for buffid,buffmap in ent.buffDic.items():
        if not buffmap:
            continue  
        buffdict = None
        for buffSrcKey, buffVal in buffmap.items():
            if buffVal:
                buffdict = buffVal
                break
                
        if buffdict is None:
            continue  
            
        entbuffdic[buffid] = {
            'buffid': int(buffid),  # 确保是普通int
            'name': str(datas[buffid].get('name', None)) if datas[buffid].get('name') else None,
            'bufflv': int(buffdict.level),  # 确保是普通int
            'time': float(buffdict.getBuffDuration()),  # 确保是普通float
            'starttime': float(buffdict.tStartTime),  # 确保是普通float
            'servertime':int(utils.getNow())
            # 'effectlist': effectlist_normal
        }

    return su.onCommandResult(0, 'ok,获取实体buff信息成功', entbuffdic)

@gm_cmd('$GMtoolsaddEntBuff', (Int('entityid'), Int('buffId'), Int('lv'), Int('time')), RONE, CELL, 'GM工具给实体加buff', ALLSIDE, GOD_GROUPS,minArgs=3)
def GMtoolsaddEntBuff(su, entityid, buffId, buffLv,time=-1):
    ent = KBEngine.entities.get(entityid)
    if buffId in BBD.datas and ent:
        ent.addBuff(buffId, buffLv, entityid,time)
        return True, '执行成功'
    else:
        return False, '执行失败'
    
@gm_cmd('$delEntBuff', (Entity('entid'),Int('buffid')), RARG(0), gameconst.CELL, '删除实体buff', ALLSIDE, GOD_GROUPS)
def delEntBuff(su, ent,buffid):
    if not hasattr(ent, 'buffDic'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", ent.id)} 没有 buffDic 方法', {})
    ent.removeBuff(buffid)
    return su.onCommandResult(0, 'ok,获取实体buff信息成功', {})
    
@gm_cmd('$getEntScoreinfo', (Str('entlist'),), RALL, gameconst.CELL, '获取实体战力信息', ALLSIDE, GOD_GROUPS)
def getEntScoreinfo(su, entlist):
    entscoredic = {}
    entlist_parsed = ast.literal_eval(entlist)
    for entid in entlist_parsed:
        entid_int = int(entid)
        ent = KBEngine.entities.get(entid_int)
        if not ent:
            continue  # 实体不存在，跳过
        if not hasattr(ent, 'scoresInfo'):
            continue  # 实体没有scoresInfo属性，跳过
        try:
            score_data = {
                'totalScore': ent.scoresInfo.totalScore,
                'rewardFightProp': ent.scoresInfo.rewardFightProp,
                'equipments': ent.scoresInfo.equipments,
                'level': ent.scoresInfo.level,
                'mount': ent.scoresInfo.mount,
                'pet': ent.scoresInfo.pet,
                'skill': ent.scoresInfo.skill,
                'meridian': ent.scoresInfo.meridian,
            }
            for key, value in score_data.items():
                if hasattr(value, '__dict__'):
                    score_data[key] = str(value)
            
            entscoredic[str(entid_int)] = score_data
        except Exception as e:
            continue
    return su.onCommandResult(0, 'ok', entscoredic)

@gm_cmd('$getEntBodyEquipmentInfo', (Entity('entid'),), RARG(0), gameconst.CELL, '获取实体装备信息', ALLSIDE, GOD_GROUPS)
def getEntBodyEquipmentInfo(su, ent):
    bodyequipinfo = {}
    if not hasattr(ent, 'bodyEquipData'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", ent.id)} 没有 bodyEquipData 方法', {})
    for equipType,equipdata in ent.bodyEquipData.equips_map.items():
        bodyrandomAffixesInfo = {}
        bodyblessInfo = {}

        for randomAffixesInfo in equipdata.equipAttr.spiritAffixes:
            affixeid = randomAffixesInfo.toAfxClientDic().get('affixId')
            affixValue = randomAffixesInfo.toAfxClientDic().get('affixVal')
            affixscore = randomAffixesInfo.getAfxScore()
            bodyrandomAffixesInfo[affixeid] = {
                '附灵ID': affixeid,
                '附灵的值': affixValue,
                '附灵的战力': affixscore,
            }
            
        for blessInfo in equipdata.equipAttr.blessAffixes:
            blessId = blessInfo.toAfxClientDic().get('affixId')
            blessValue = blessInfo.toAfxClientDic().get('affixVal')
            blessscore = blessInfo.getAfxScore()
            bodyblessInfo[blessId] = {
                '祝福ID': blessId,
                '祝福的值': blessValue,
                '祝福的战力': blessscore,
            }
        if equipdata.getItemName() in bodyequipinfo:
            bodyequipinfo[equipdata.getItemName()+'2'] = {
            '装备名字': equipdata.getItemName(),
            '装备品阶': equipdata.grade(),
            '装备品质': equipdata.quality,
            '装备战力': equipdata.getEquipScore(),
            '装备ID': equipdata.itemId,
            '装备基础词条':equipdata.getBaseAttrInfo(),
            '装备的随机基础词条':equipdata.equipAttr.baseAttrsByAfxVal,
            '装备的强化等级':equipdata.getEnhanceLevel(),
            '装备的强化属性':equipdata.equipAttr.enhancementAttrs,
            '装备的附灵属性':bodyrandomAffixesInfo,
            '装备的祝福属性':bodyblessInfo
        }
        else:
            bodyequipinfo[equipdata.getItemName()] = {
                '装备名字': equipdata.getItemName(),
                '装备品阶': equipdata.grade(),
                '装备品质': equipdata.quality,
                '装备战力': equipdata.getEquipScore(),
                '装备ID': equipdata.itemId,
                '装备基础词条':equipdata.getBaseAttrInfo(),
                '装备的随机基础词条':equipdata.equipAttr.baseAttrsByAfxVal,
                '装备的强化等级':equipdata.getEnhanceLevel(),
                '装备的强化属性':equipdata.equipAttr.enhancementAttrs,
                '装备的附灵属性':bodyrandomAffixesInfo,
                '装备的祝福属性':bodyblessInfo
            }
    return su.onCommandResult(0, 'ok', bodyequipinfo)

    

@gm_cmd('$unlockAllFunc', (Player("gbId/Id"), Int("onlyTask")), RARG(0), BASE, '解锁所有功能', ALLSIDE, GOD_GROUPS, minArgs=1)
def unlockAllFunc(su, player, onlyTask=0):
    import actionContext
    import tutorConst_newbieStep as TCNSD
    import visible_visible as V_VD
    import tutorConst_triggerGuide as TTGD
    maxLv = 0
    roleMaxLv = utils.getPlayerMaxLevel()
    needCompleteTasks = set()
    for _, data in V_VD.datas.items():
        lvLimit = data.get('level', 0)
        taskId = data.get('task', 0)
        if taskId > 0 and dataUtils.getTaskData(taskId):
            needCompleteTasks.add(taskId)
        if lvLimit > maxLv and lvLimit <= roleMaxLv:
            maxLv = lvLimit
    if maxLv > 0 and onlyTask == 0:
        forwardCommand(su,"$setlv", player.id, maxLv)
    # 整理出根任务及其子任务即可，否则会因为根任务后完成清掉子任务的状态
    finishedRootTasks = []
    for taskId in needCompleteTasks:
        rootTaskId = dataUtils.getRootTaskId(taskId)
        if rootTaskId in finishedRootTasks:
            continue
        finishedRootTasks.append(rootTaskId)
        player.baseTaskClaim(rootTaskId, actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrc.GM), needCheck=False)
        taskData = dataUtils.getTaskData(rootTaskId)
        for subTaskId in taskData.get('ChildTaskIds', []):
            player.taskInfo.tasks.pop(subTaskId, None)

            player.taskInfo.taskRecordDic[subTaskId] = gameconst.TaskStat.TASK_STAT_SUBMITTED
            if subTaskId in V_VD.taskDic:
                player.updateVisibleByList(V_VD.taskDic[subTaskId])
        player.taskInfo.tasks.pop(rootTaskId, None)
        player.taskInfo.taskRecordDic[rootTaskId] = gameconst.TaskStat.TASK_STAT_SUBMITTED
        if taskId in V_VD.taskDic:
            player.updateVisibleByList(V_VD.taskDic[taskId])
    player.unlockSkill(True, 0, 0)
    for newbieGuideId in TTGD.datas.keys():
        if newbieGuideId not in player.newbieGuideIds:
            player.newbieGuideIds.append(newbieGuideId)
    player.gmFinishedNewbie(0)

    return True, '执行成功'


# 统计掉落 路由那边需要随便选一个stub来固定所在base，不然第二次来取cache的话可能会串
@gm_cmd('$statDropByDropId', (Int("rewardId"), Int("count"), Int("Level"), Int("school"), Int("sex"), Int("isMonthCardExpired"), Int("avatarScoreRank"), Int("isCrossServer")), RSTUB('PlayerStub'), BASE, 
    '根据掉落id统计掉落', ALLSIDE, GOD_GROUPS, minArgs=2)
def statDropByDropId(su, playerStub, rewardId, count, level=0, school=0, sex=0, isMonthCardExpired=0, avatarScoreRank=0, isCrossServer=0):
    from test import dropTest
    dropUnit = dropTest.DropUnit(su, count)
    contextVar = {
        'playerLevel': level,
        'school': school,
        'sex': sex,
        'isMonthCardExpired': isMonthCardExpired,
        'avatarScoreRank': avatarScoreRank,
        'isCrossServer': isCrossServer
    }
    ret, data, process_info = dropUnit.batchGenAward(rewardId, contextVar)
    if ret:
        su.onCommandResult(0, 'ok', {'data': {f"{rewardId}_{count}_{level}_{school}_{sex}_{isMonthCardExpired}_{avatarScoreRank}_{isCrossServer}": data}})
    else:
        su.onCommandResult(0, 'wait', {'msg': data, 'process_info': process_info})


@gm_cmd('$statDropByDunNo', (Int("dunNo"), Int("count")), RSTUB('PlayerStub'), BASE, 
    '根据副本编号统计掉落', ALLSIDE, GOD_GROUPS)
def statDropByDunNo(su, playerStub, dunNo, count):
    from test import dropTest
    dropUnit = dropTest.DropUnit(su, count)
    ret, content, process_info = dropUnit.getDunDrop(dunNo, count)
    if ret:
        content = gzip.compress(json.dumps(content).encode('utf-8'))
        su.onCommandResult(0, 'ok', {'data': str(content)})
    else:
        su.onCommandResult(0, 'wait', {'msg': content, 'process_info': process_info})

@gm_cmd('$hookModuleFunc', (Str("moduleName"), Str("prefix"), Str("preCall"), Str("postCall")), RALL, ALL, 
    'hook模块方法，输出入参和回参', ALLSIDE, GOD_GROUPS, minArgs=1)
def hookModuleFunc(su, moduleName, prefix='', preCall='', postCall=''):
    from test import functionHooker
    import sys
    mod = sys.modules.get(moduleName)
    if mod is None:
        return su.onCommandResult(1, f'module {moduleName} not found', {})
    functionHooker.hook_specific_module(moduleName, prefix=prefix, verbose=True, pre_call_func_type=preCall, post_call_func_type=postCall)
    return su.onCommandResult(0, f'hook module {moduleName} success', {})

@gm_cmd('$hookClassFunc', (Str("moduleName"), Str("className"), Str("prefix")), RALL, ALL, 
    'hook类方法，输出入参和回参', ALLSIDE, GOD_GROUPS, minArgs=2)
def hookClassFunc(su, moduleName, className, prefix=''):
    from test import functionHooker
    import sys
    mod = sys.modules.get(moduleName)
    if mod is None:
        return su.onCommandResult(1, f'module {moduleName} not found', {})
    functionHooker.hook_specific_class(moduleName, className, prefix=prefix, verbose=True)
    return su.onCommandResult(0, f'hook class {className} in module {moduleName} success', {})

@gm_cmd('$hookFunc', (Str("moduleName"), Str("className"), Str("funcName"), Int("traceDepth"), Str("prefix")), RALL, ALL, 
    'hook指定函数，输出入参和回参', ALLSIDE, GOD_GROUPS, minArgs=3)
def hookFunc(su, moduleName, className, funcName, traceDepth=0, prefix=''):
    from test import functionHooker
    import sys
    mod = sys.modules.get(moduleName)
    if mod is None:
        return su.onCommandResult(1, f'module {moduleName} not found', {})
    functionHooker.hook_specific_class_method(moduleName, className, funcName, prefix=prefix, show_traceback=bool(traceDepth), traceback_depth=traceDepth, verbose=True)
    return su.onCommandResult(0, f'hook class {className} func {funcName} in module {moduleName} success', {})

@gm_cmd('$hookShowLog', (Int("is_open"),), RALL, ALL, 
    'hook打印开关', ALLSIDE, GOD_GROUPS)
def hookShowLog(su, is_open):
    from test import functionHooker
    functionHooker.hook_print_open(bool(is_open))
    return su.onCommandResult(0, f'hook print open: {is_open}', {})

@gm_cmd('$refreshData', (Str('moduleName'),), RALL, ALL, '刷新表格数据', ALLSIDE, GOD_GROUPS, minArgs=0)
def refreshData(su, moduleName=None):
    """刷新表格数据，在所有进程中执行"""
    
    # 确定当前进程类型
    process_type = 'BaseApp' if IS_BASE else 'CellApp'
    try:
        import gamerefresh
        if moduleName and moduleName.strip():
            gamerefresh.refreshData(moduleName)
            return su.onCommandResult(0, f'{process_type}进程刷新 {moduleName} 数据成功', {})
        else:
            gamerefresh.refreshData()
            return su.onCommandResult(0, f'{process_type}进程刷新所有数据成功', {})
    except Exception as e:
        return su.onCommandResult(1, f'{process_type}进程刷新数据失败: {str(e)}', {})



@gm_cmd('$setdata', (Str('moduleName'), Str('key'), Str('attrName'), Str('value'), Int('isBase64')), RALL, ALL, '修改内存数据(支持普通值和函数)', ALLSIDE, GOD_GROUPS, minArgs=4)
def setMemoryData(su, moduleName, key, attrName, value, isBase64=0):
    """修改内存数据，支持普通字段和函数表达式，在所有进程中执行"""
    # 确定当前进程类型
    process_type = 'BaseApp' if IS_BASE else 'CellApp'
    # 直接在当前进程中执行修改
    return _setMemoryDataInProcess(su, moduleName, key, attrName, value, isBase64, process_type)

def _translateValue(value, valueType, module_dict=None):
    """根据valueType转换value"""
    try:
        DEBUG_MSG(f'_translateValue:: {value} {type(value)} to {valueType}')
        import ast
        if valueType == 'int':
            if type(value) is bool:
                value = 1 if value else 0
            else:
                value = int(value)
        elif valueType == 'float':
            value = float(value)
        elif valueType == 'str':
            value = str(value)
        elif valueType == 'bool':
            value = value.lower() in ('true', '1', 'yes')
        elif valueType == 'list':
            value = ast.literal_eval(value) if isinstance(value, str) else list(value)
        elif valueType == 'dict':
            value = ast.literal_eval(value) if isinstance(value, str) else dict(value)
        elif valueType == 'tuple':
            value = ast.literal_eval(value) if isinstance(value, str) else tuple(value)
        elif valueType == 'function':
            if value == '':
                return True, "转换成功", None
            # 解析函数名
            rootNode = ast.parse(value)
            funcName = None
            for node in ast.walk(rootNode):
                if isinstance(node, ast.FunctionDef):
                    funcName = node.name
                    break
            if not funcName:
                return False, '函数定义不正确，无法找到函数名', None
            # 在原模块的全局命名空间中编译函数，保留所有导入的模块
            exec(value, module_dict)
            if funcName not in module_dict:
                return False, f'函数 {funcName} 编译失败', None
            # 获取编译好的函数对象
            new_func = module_dict[funcName]
            # 添加源码属性，用于getEntSkillDic获取源码
            new_func.__source_code__ = value
            value = new_func
        else:
            # 默认尝试eval
            value = eval(value)
        return True, "转换成功", value
    except Exception as e:
        return False, f"转换失败: {str(e)}", value

def _setMemoryDataInProcess(su, moduleName, key, attrName, value, isBase64, processType):
    """在指定进程中修改内存数据的公共逻辑"""
    try:
        # 导入模块
        import sys
        mod = sys.modules.get(moduleName)
        if mod is None:
            return su.onCommandResult(1, f'{processType}进程: 模块 {moduleName} 未加载', {})
        # 获取模块的datas属性
        datas = getattr(mod, 'datas', None)
        if datas is None:
            return su.onCommandResult(1, f'{processType}进程: 模块 {moduleName} 没有 datas 属性', {})
        # 处理key类型
        ori_keys = datas.keys()
        ori_key_type = type(next(iter(ori_keys))) if ori_keys else str
        _, _, key_cast = _translateValue(key, ori_key_type.__name__)
        if key_cast not in datas:
            return su.onCommandResult(1, f'{processType}进程: key {key} 不在 {moduleName}.datas 中', {})
        # 获取目标数据对象
        target_data = datas[key_cast]
        # 根据目标属性的当前值类型进行转换
        target_value = target_data.get(attrName, None)
        
        if target_value is not None:
            valueType = type(target_value).__name__
        else:
            for v in datas.values():
                tmp_value = v.get(attrName, None)
                if tmp_value is not None:
                    valueType = type(tmp_value).__name__
                    break
        # 判断value类型并处理
        if isBase64 :
            # 直接内存替换方案 - 不编译，直接创建函数对象
            try:
                value = base64.b64decode(value).decode('utf-8')
            except Exception as e:
                return su.onCommandResult(1, f'{processType}进程: base64解码失败: {str(e)}', {})
        try:
            ret, msg, parsed_value = _translateValue(value, valueType, mod.__dict__)
            if not ret:
                return su.onCommandResult(1, f'{processType}进程: {msg}', {})
            # 设置到数据中
            if hasattr(target_data, '_data'):
                target_data._data[attrName] = parsed_value
            else:
                target_data[attrName] = parsed_value
        except Exception as e:
            return su.onCommandResult(1, f'{processType}进程: 值设置失败: {str(e)}', {})
        import gamerefresh
        gamerefresh.refreshData(' ') # 主要为了调用clearCacheInTick
        return su.onCommandResult(0, f'{processType}进程修改 {moduleName}.datas[{key_cast}].{attrName} 成功 {target_data[attrName]}', {attrName: value})
    except Exception as e:
        return su.onCommandResult(1, f'{processType}进程修改失败: {str(e)}', {})

def _getTableValue(value):
    """递归获取表格值，处理函数和自定义类"""
    value_type = type(value).__name__
    if callable(value):
        # 尝试获取源码
        try:
            if hasattr(value, '__source_code__'):
                # 动态函数，有源码属性
                func_source = value.__source_code__
            else:
                # 普通函数，用inspect获取源码
                import inspect
                func_source = inspect.getsource(value).strip()
        except:
            # 无法获取源码，显示函数名和类型
            func_source = f"<func: {getattr(value, '__name__', 'unknown')} - {type(value).__name__}>"
        return func_source
    elif value_type == 'RODict':
        # 处理自定义类，提取_data属性
        return {k: _getTableValue(v) for k, v in value._data.items()}
    elif value_type == 'ROList':
        # 处理自定义类，提取_data属性
        return [_getTableValue(v) for v in value._data]
    elif value_type == 'ROSet':
        # 处理自定义类，提取_data属性
        return set([_getTableValue(v) for v in value._data])
    return value

@gm_cmd('$getdata', (Str('moduleName'), Str('key'), Str('attrName')), RONE, CELL, '获取内存数据', ALLSIDE, GOD_GROUPS, minArgs=2)
def getMemoryData(su, moduleName, key, attrName=None):
    # 导入模块
    import sys
    mod = sys.modules.get(moduleName)
    if mod is None:
        return su.onCommandResult(1, f' 模块 {moduleName} 未加载', {})
    # 获取模块的datas属性
    datas = getattr(mod, 'datas', None)
    if datas is None:
        return su.onCommandResult(1, f' 模块 {moduleName} 没有 datas 属性', {})
    # 处理key类型
    ori_keys = datas.keys()
    ori_key_type = type(next(iter(ori_keys))) if ori_keys else str
    _, _, key_cast = _translateValue(key, ori_key_type.__name__)
    if key_cast not in datas:
        return su.onCommandResult(1, f'key {key} 不在 {moduleName}.datas 中', {})
    # 获取目标数据对象
    target_data = datas[key_cast]
    if attrName:
        if attrName not in target_data:
            return su.onCommandResult(1, f'属性 {attrName} 不在 {moduleName}.datas[{key}]. 中', {})
        value = _getTableValue(target_data[attrName])
        return su.onCommandResult(0, 'ok', {attrName: value})
    else:
        # rodict类型，提取_data, 否则无法json序列化
        if hasattr(target_data, '_data'):
            new_data = {k: _getTableValue(v) for k, v in target_data._data.items()}
        else:
            new_data = {k: _getTableValue(v) for k, v in target_data.items()}
        DEBUG_MSG("GM: getMemoryData ~ ", new_data)
        return su.onCommandResult(0, 'ok', new_data)

@gm_cmd('$reqWorkshopSetAutoMF', (Player("gbId/Id"), Int('autoMF')), RARG(0), gameconst.BASE, '测试开启自动合成制作', ALLSIDE, GOD_GROUPS)
def reqWorkshopSetAutoMF(su, player, autoMF):
    INFO_MSG("GM: reqWorkshopSetAutoMF ~ ", autoMF)
    return player.reqWorkshopSetAutoMF(autoMF)

@gm_cmd('$reqWorkshopMF', (Player("gbId/Id"), Int('itemID'), Int('batchCount')), RARG(0), gameconst.BASE, '测试合成制作', ALLSIDE, GOD_GROUPS)
def reqWorkshopMF(su, player, itemID, batchCount):
    INFO_MSG("GM: reqWorkshopMF ~ ", itemID, batchCount)
    return player.reqWorkshopMF(itemID, batchCount)

@gm_cmd('$getServerAllEntities', (), RALL, ALL, '获取服务器所有实体', ALLSIDE, GOD_GROUPS)
def getServerAllEntities(su):
    """获取服务器所有实体，按进程类型分类返回"""
    
    # 获取当前进程信息
    componentNo = KBEngine.getComponentGroupOrder()
    process_type = 'BaseApp' if IS_BASE else 'CellApp'
    process_name = f'{process_type.lower()}{componentNo:02d}'
    
    # 收集当前进程中的所有实体
    entity_classes = {}
    total_entity_count = 0
    
    # 定义需要限制显示ID数量的实体类型
    limited_types = {''}
    
    for entity in KBEngine.entities.values():
        class_name = entity.className
        
        if class_name not in entity_classes:
            entity_classes[class_name] = {
                'count': 0,
                'entity_ids': [],
                'is_limited': class_name in limited_types
            }
        
        entity_classes[class_name]['count'] += 1
        
        # 对于Space类型实体，保存ID和spaceNo
        if class_name == 'Space':
            entity_info = {'id': entity.id}
            if hasattr(entity, 'spaceNo'):
                entity_info['spaceNo'] = entity.spaceNo
            entity_classes[class_name]['entity_ids'].append(entity_info)
        # 对于数量较多的实体类型，只保存少量ID作为示例
        elif class_name in limited_types:
            if len(entity_classes[class_name]['entity_ids']) < 3:
                entity_classes[class_name]['entity_ids'].append(entity.id)
        else:
            # 其他类型保存所有ID
            entity_classes[class_name]['entity_ids'].append(entity.id)
            
        total_entity_count += 1
    
    # 构造返回数据
    result_data = {
        'process_info': {
            'process_name': process_name,
            'process_type': process_type,
            'component_order': componentNo
        },
        'entity_summary': {
            'total_entity_count': total_entity_count,
            'unique_entity_types': len(entity_classes)
        },
        'entity_details': entity_classes,
        'limited_types': list(limited_types)
    }
    
    return su.onCommandResult(0, f'{process_name}进程实体统计完成', result_data)


@gm_cmd('$getStubAllProp', (Str("processType"), Int('entityId'), Str('attrPath')), RALL, ALL, '获取指定进程实体属性', ALLSIDE, GOD_GROUPS, minArgs=2)
def getStubAllProp(su, processType, entityId, attrPath=""):
    """获取指定实体的所有属性，按类型分类显示"""
    try:
        # 解析目标进程
        if processType.startswith('base'):
            target_type, target_component = 'baseapp', int(processType[4:]) if len(processType) > 4 else 1
        elif processType.startswith('cell'):
            target_type, target_component = 'cellapp', int(processType[4:]) if len(processType) > 4 else 1
        else:
            return su.onCommandResult(1, f'无效的进程类型: {processType}', {})

        # 检查是否为目标进程
        current_type = KBEngine.component
        current_component = KBEngine.getComponentGroupOrder()
        if current_type != target_type or current_component != target_component:
            return su.onCommandResult(0, '', {})  # 非目标进程返回空数据

        # 获取实体
        entity = KBEngine.entities.get(entityId)
        if not entity:
            return su.onCommandResult(1, f'实体{entityId}不存在', {
                "process_info": {"type": current_type, "component": current_component, "process_name": processType, "matched": True},
                "target_info": {"path": f"entity.{entityId}", "object_type": "Unknown"},
                "attributes": {"公共": {"error": "实体不存在"}, "私有": {}, "函数/方法": {}, "特殊属性": {}}
            })

        # 获取目标对象
        if attrPath:
            try:
                target_obj = eval(f"entity.{attrPath}", {"__builtins__": {}}, {'entity': entity})
                current_path = f"entity.{attrPath}"
            except Exception as e:
                return su.onCommandResult(1, f'路径访问失败: {attrPath}, 错误: {str(e)}', {})
        else:
            target_obj = entity
            current_path = "entity"

        # 获取分类属性并返回结果
        classified_attrs = _get_entity_attributes_classified(target_obj, processType)
        return su.onCommandResult(0, f'获取实体{entityId}属性完成', {
            "process_info": {"type": current_type, "component": current_component, "process_name": processType, "matched": True},
            "target_info": {"path": current_path, "object_type": type(target_obj).__name__},
            "attributes": classified_attrs
        })
        
    except Exception as e:
        import traceback
        return su.onCommandResult(1, f"获取实体属性时出错: {str(e)}\n{traceback.format_exc()}", {})


def _get_entity_attributes_classified(target_obj, process_name):
    """获取对象的分类属性"""
    classified = {"公共": {}, "私有": {}, "函数/方法": {}, "特殊属性": {}}
    
    try:
        # 处理容器类型：字典、RODict、列表
        if isinstance(target_obj, dict) or type(target_obj).__name__ == 'RODict':
            # 字典类型展开键值对
            items_iter = None
            try:
                items_iter = target_obj.items()
            except:
                try:
                    items_iter = [(k, target_obj[k]) for k in target_obj]
                except:
                    pass
            
            if items_iter:
                for key, value in items_iter:
                    try:
                        classified["公共"][str(key)] = _get_simple_value(value)
                    except:
                        classified["公共"][str(key)] = "<error>"
            return classified
        
        elif isinstance(target_obj, (list, tuple)):
            # 列表类型展开索引值对
            for i, value in enumerate(target_obj):
                try:
                    classified["公共"][str(i)] = _get_simple_value(value)
                except:
                    classified["公共"][str(i)] = "<error>"
            return classified
        
        elif isinstance(target_obj, (set, frozenset)):
            try:
                values_list = list(target_obj)
                for i, value in enumerate(values_list):
                    try:
                        classified["公共"][str(i)] = _get_simple_value(value)
                    except:
                        classified["公共"][str(i)] = "<error>"
            except:
                classified["公共"]["error"] = "无法遍历set内容"
            return classified
        # 普通对象：按属性名分类
        skip_attrs = {'canDestroy', 'destroy', 'destroyEntity', 'writeToDB', 'createCellEntity', 'destroyCellEntity', 'teleport', 'addTimer', 'delTimer', 'giveClientTo'}
        
        for attr_name in dir(target_obj):
            if attr_name in skip_attrs:
                continue
                
            try:
                attr_value = getattr(target_obj, attr_name)
                simple_value = _get_simple_value(attr_value)
                
                # 按名称分类
                if attr_name.startswith('__') and attr_name.endswith('__'):
                    classified["特殊属性"][attr_name] = simple_value
                elif attr_name.startswith('_'):
                    classified["私有"][attr_name] = simple_value
                elif callable(attr_value):
                    classified["函数/方法"][attr_name] = simple_value
                else:
                    classified["公共"][attr_name] = simple_value
            except:
                classified["公共"][attr_name] = "<无法访问>"
                
    except:
        classified["公共"]["error"] = "获取属性时出错"
    
    return classified


def _get_simple_value(value):
    """获取属性值的简化字符串表示"""
    try:
        if value is None:
            return 'None'
        elif isinstance(value, bool):
            return str(value)
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            return f'"{value[:50]}..."' if len(value) > 50 else f'"{value}"'
        elif isinstance(value, (list, tuple)):
            # 列表和元组也可以展开查看内容
            return f"{type(value).__name__}[{len(value)}] [可展开]"
        elif isinstance(value, dict):
            # 字典也可以展开查看内容
            return f"dict[{len(value)}] [可展开]"
        elif isinstance(value, set):
            # set集合类型也可以展开查看内容
            return f"set[{len(value)}] [可展开]"
        elif callable(value):
            return f"<{type(value).__name__}>"
        else:
            # 检查常见的游戏类型
            class_name = type(value).__name__
            
            # Vector3 类型特殊处理
            if class_name == 'Vector3':
                try:
                    if hasattr(value, 'x') and hasattr(value, 'y') and hasattr(value, 'z'):
                        return f"Vector3({value.x}, {value.y}, {value.z}) [可展开]"
                except:
                    pass
            
            # MAILBOX 类型特殊处理
            elif class_name == 'MAILBOX':
                try:
                    if hasattr(value, 'id'):
                        return f"MAILBOX(id={value.id}) [可展开]"
                except:
                    pass
            
            # RODict 类型特殊处理
            elif class_name == 'RODict':
                try:
                    return f"RODict[{len(value)}] [可展开]"
                except:
                    pass
            
            # 检查是否是可展开的复杂对象
            if (hasattr(value, '__dict__') and 
                not isinstance(value, (str, int, float, bool, list, tuple, dict)) and
                hasattr(value, '__class__')):
                # 这是一个自定义类实例，可以展开
                return f"<{class_name}> [可展开]"
            else:
                return f"<{class_name}>"
    except Exception:
        return "<unknown>"


@gm_cmd('$broadcastSystemMsg', (Str('message'),), RONE, BASE, '向系统频道广播消息', ALLSIDE, GOD_GROUPS)
def broadcastSystemMsg(su, message):
    #给机器人广播使用
    try:
        strmessage = base64.b64decode(message).decode('utf-8')
        system_avatar_info = {
            'gbId': 0, 
            'name': '系统',
            'level': 0,
            'vipLevel': 0,
            'school': 0,
            'sex': 0
        }
        
        # 只在一个BaseApp进程中执行，然后向所有BaseApp广播
        gameengine.broadcastBaseapp('broadcastToAllAvatar',
                                    (gameconst.BASE, 'onRecvChannelMsg',
                                     (gameconst.ChatChannel.SYSTEM, system_avatar_info, strmessage), ()))
        
        return su.onCommandResult(0, f'系统消息广播成功: {strmessage}', {})
        
    except Exception as e:
        return su.onCommandResult(1, f'系统消息广播失败: {str(e)}', {})

# --------------------------dev test only cmd segment----------------------------------------------------------------------------------------------------------------------------------------- 
@gm_cmd('$modifyEquipEnhanceLevel', (Player("gbId/Id"), Int("slotID"), Int("enhanceLevel")), RARG(0), gameconst.CELL, '修改装备强化等级', ALLSIDE, GOD_GROUPS)
def modifyEquipEnhanceLevel(su, player, slotID, enhanceLevel):
    ret = player.gmModifyEquipEnhanceLevel(slotID, enhanceLevel)
    if not ret:
        return False, '执行失败'
    return True, '执行成功'

@gm_cmd('$dressAllEquipments', (Player("gbId/Id"), Int("quality")), RARG(0), gameconst.CELL, '穿戴所有装备', ALLSIDE, GOD_GROUPS)
def dressAllEquipments(su, player, quality):
    if quality not in gameconst.ItemQuality.COLL_QUALITY:
        return False, '执行失败，无效品质'
    ret = player.gmDressEquips(quality)
    if not ret:
        return False, '执行失败'
    return True, '执行成功'

@gm_cmd('$glyphWashingEquipments', (Player("gbId/Id"), Int("equipPos"), Int("slotId"), Int("itemId"), Int("affixId1"), Int("affixId2")), RARG(0), gameconst.CELL, '给指定的装备洗铭文', ALLSIDE, GOD_GROUPS)
def glyphWashingEquipments(su, player, equipPos, slotId, itemId, affixId1, affixId2):
    ret = player.gmGlyphWashingEquips(equipPos, slotId, itemId, affixId1, affixId2)
    if not ret:
        return False, '执行失败'
    return True, '执行成功'

@gm_cmd('$glyphWashingEquipmentsInEquip', (Player("gbId/Id"), Int("equipPos"), Str("affixIds")), RARG(0), gameconst.CELL, '给穿戴的装备洗铭文', ALLSIDE, GOD_GROUPS, minArgs=1)
def glyphWashingEquipmentsInEquip(su, player, equipPos=0, affixIds=''):
    equipPos = equipPos or gameconst.BodyEquipSlot.EQUIP_WEAPON_SLOT
    equipItem = player.bodyEquipData.getEquipItem(equipPos)
    if not equipItem:
        return False, '执行失败，指定位置没有装备'
    # 直接获得的强化装备没有刷新祝福孔位,重新触发一下
    # enhanceLevel = equipItem.getEnhanceLevel()
    # player.gmModifyEquipEnhanceLevel(equipPos, enhanceLevel)
    itemId = equipItem.itemId
    affixIds = [int(item) for item in affixIds.split(',') if item.isdigit()]
    if not affixIds:
        affixList = equipItem.equipAttr._genGlyphAffix(2 * len(equipItem.equipAttr.glyphSlotNum))
        affixIds = [affix.getAffixId() for affix in affixList]
    for slotId in equipItem.equipAttr.glyphSlotNum:
        affixId1 = affixIds.pop(0) if affixIds else 0
        affixId2 = affixIds.pop(0) if affixIds else 0
        ret = player.gmGlyphWashingEquips(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId, itemId, affixId1, affixId2)
        if not ret:
            return False, '执行失败'
    return True, '执行成功'

@gm_cmd('$openGuildDungeon', (Player("gbId/Id"), Int("openTime"), Int("openType"), Int("openID")), RARG(0), gameconst.CELL, '测试公会boss开启', ALLSIDE, GOD_GROUPS)
def openGuildDungeon(su, player, openTime, openType, openID):
    ret = player.openGuildDungeon(player.id, openTime, openType, openID)
    if not ret:
        return False, '执行失败'
    return True, '执行成功'

@gm_cmd('$cancelGuildDungeonOrder', (Player("gbId/Id"), Int("openID")), RARG(0), gameconst.CELL, '测试公会boss预约取消', ALLSIDE, GOD_GROUPS)
def cancelGuildDungeonOrder(su, player, openID):
    ret = player.cancelGuildDungeonOrder(player.id, openID)
    if not ret:
        return False, '执行失败'
    return True, '执行成功'

@gm_cmd('$enterBossChallengeDungeon', (Player("gbId/Id"), Int("openID")), RARG(0), gameconst.CELL, '测试公会boss进入', ALLSIDE, GOD_GROUPS)
def enterBossChallengeDungeon(su, player, openID):
    ret = player.enterBossChallengeDungeon(player.id, openID)
    if not ret:
        return False, '执行失败'
    return True, '执行成功'

@gm_cmd('$leaveBossChallengeDungeon', (Player("gbId/Id"), Int("openID")), RARG(0), gameconst.CELL, '测试公会boss离开', ALLSIDE, GOD_GROUPS)
def leaveBossChallengeDungeon(su, player, openID):
    ret = player.leaveBossChallengeDungeon(player.id, openID)
    if not ret:
        return False, '执行失败'
    return True, '执行成功'

@gm_cmd('$modifyGuildFund', (Player("gbId/Id"), Int("addCount")), RARG(0), gameconst.BASE, '加公会资金', ALLSIDE, GOD_GROUPS)
def modifyGuildFund(su, player, addCount):
    opUUID = KBEngine.genUUID64()
    src = AAC_AACDD.datas.BONUS_SRC_GM
    detail = gameclass.AwardDetail(gm_cmd='$modifyGuildFund', addCount=addCount)
    if addCount < 1:
        return False, '执行失败，资金不能小于1'
    elif player.guildBox is None:
        return False, '当前玩家没有帮会'
    player.guildBox.modifyGuildFund(addCount, src, opUUID, detail)
    return True, '执行成功'

@gm_cmd('$modifyGuildMoney', (Player("gbId/Id"), Int("addCount")), RARG(0), gameconst.BASE, '加公会金币', ALLSIDE, GOD_GROUPS)
def modifyGuildMoney(su, player, addCount):
    opUUID = KBEngine.genUUID64()
    src = AAC_AACDD.datas.BONUS_SRC_GM
    detail = gameclass.AwardDetail(gm_cmd='$modifyGuildMoney', addCount=addCount)
    if addCount < 1:
        return False, '执行失败，金币不能小于1'
    elif player.guildBox is None:
        return False, '当前玩家没有帮会'
    player.guildBox.modifyGuildMoney(addCount, src, opUUID, detail)
    return True, '执行成功'

@gm_cmd('$modifyGuildDungeonStatus', (Player("gbId/Id"), Int("status")), RARG(0), gameconst.BASE, '修改公会副本状态', ALLSIDE, GOD_GROUPS)
def modifyGuildDungeonStatus(su, player, status):
    if player.guildBox is None:
        return False, '当前玩家没有帮会'
    player.guildBox.gmModifyGuildBossChallengeStatus(status)
    return True, '执行成功'

@gm_cmd('$resetGuildDungeonOpenCount', (Player("gbId/Id"),), RARG(0), gameconst.BASE, '重置公会副本开启次数', ALLSIDE, GOD_GROUPS)
def resetGuildDungeonOpenCount(su, player):
    if player.guildBox is None:
        return False, '当前玩家没有帮会'
    player.guildBox.gmResetGuildDungeonOpenCount()
    return True, '执行成功'

@gm_cmd('$resetGuildDungeonAllData', (Player("gbId/Id"),), RARG(0), gameconst.BASE, '重置公会副本数据', ALLSIDE, GOD_GROUPS)
def resetGuildDungeonAllData(su, player):
    if player.guildBox is None:
        return False, '当前玩家没有帮会'
    player.guildBox.gmResetGuildDungeonAllData()
    return True, '执行成功'

@gm_cmd('$resetCrusadeNum', (Player("gbId/Id"),), RARG(0), gameconst.BASE, '重置组队次数', ALLSIDE, GOD_GROUPS)
def resetCrusadeNum(su, player):
    if player is None:
        return False, '执行失败'
    player.onCrusadeDailyRewardNumUpdate()
    player.onCrusadeWeeklyAddRewardItemNumUpdate()
    return True, '执行成功'


@gm_cmd('$resetChiefNum', (Player("gbId/Id"),), RARG(0), gameconst.BASE, '重置团队次数', ALLSIDE, GOD_GROUPS)
def resetChiefNum(su, player):
    if player is None:
        return False, '执行失败'
    player.onChiefDailyRewardNumUpdate()
    player.onChiefWeeklyAddRewardItemNumUpdate()
    return True, '执行成功'


@gm_cmd('$clearCrusadeNum', (Player("gbId/Id"),), RARG(0), gameconst.BASE, '清理组队次数', ALLSIDE, GOD_GROUPS)
def clearCrusadeNum(su, player):
    if player is None:
        return False, '执行失败'
    player.crusadeInfo.clear()
    player.crusadeInfo = player.crusadeInfo
    return True, '执行成功'

@gm_cmd('$clearChiefNum', (Player("gbId/Id"),), RARG(0), gameconst.BASE, '清理团队次数', ALLSIDE, GOD_GROUPS)
def clearChiefNum(su, player):
    if player is None:
        return False, '执行失败'
    player.chiefInfo.clear()
    player.chiefInfo = player.chiefInfo
    return True, '执行成功'

@gm_cmd('$resetGuildBossChallengeWeeklyNum', (Player("gbId/Id"),), RARG(0), gameconst.BASE, '清理公会副本挑战次数', ALLSIDE, GOD_GROUPS)
def resetGuildBossChallengeWeeklyNum(su, player):
    if player is None:
        return False, '执行失败'
    player.dungeonSettlementWeeklyReset()
    return True, '执行成功'


@gm_cmd('$getSettlementRankList', (Player("gbId/Id"), Int("statisticType"), Int("dungeonNo"), Int("dungeonPlayMode"), Int("idx"), Int("offset"),), RARG(0), gameconst.CELL, '获取副本排名数据', ALLSIDE, GOD_GROUPS)
def getSettlementRankList(su, player, statisticType, dungeonNo, dungeonPlayMode, idx, offset):
    if player is None:
        return False, '执行失败'
    player.getSettlementRankList(player.id, statisticType, dungeonNo, dungeonPlayMode, idx, offset)
    return True, '执行成功'

@gm_cmd('$MoveWarehouseOrBag', (Player("gbId/Id"), Int("gridID"), Int("itemID"), Int("itemNum"), Int("moveType"),), RARG(0), gameconst.BASE, '仓库背包互相移动', ALLSIDE, GOD_GROUPS)
def MoveWarehouseOrBag(su, player, gridID, itemID, itemNum, moveType):
    if player is None:
        return False, '执行失败'
    # 仓库到背包
    if moveType == 1:
        player.reqMoveItemToBag(player.id, gridID, itemID, itemNum)
    # 背包到仓库
    elif moveType == 2:
        player.reqMoveItemToWarehouse(player.id, gridID, itemID, itemNum)
    else:
        return False, '执行失败'
    return True, '执行成功'

@gm_cmd('$showPetDraw', (Player("gbId/Id"), Str("petItemList"),), RARG(0), gameconst.CELL, '模拟精灵抽卡结果（需要打开抽卡界面）', ALLSIDE, GOD_GROUPS)
def showPetDraw(su, player, petItemList):
    if player is None:
        return False, '执行失败'
    import random
    petItemList = [int(item) for item in petItemList.split(',') if item.isdigit()]
    if len(petItemList) == 0:
        return False, '执行失败，精灵石列表不能为空'
    petItemListValid = getPetItemList()
    for itemID in petItemList:
        if itemID not in petItemListValid:
            return False, f'执行失败，物品ID {itemID} 不是精灵石'
    if len(petItemList) != 1 and len(petItemList) != 11:
        petItemList = petItemList + random.sample(petItemListValid, 11 - len(petItemList))
        petItemList = petItemList[:11]
    player.client.onRandomSummonPet(petItemList)
    return True, '执行成功'

@gm_cmd('$gmUnlockAllMeridian', (Player("gbId/Id"),), RARG(0), gameconst.BASE, '经脉升至满级', ALLSIDE, GOD_GROUPS)
def gmUnlockAllMeridian(su,player):
    if player is None:
        return False, '执行失败'
    player.gmUnlockAllMeridian()
    return True, '执行成功'

@gm_cmd('$gmLevelUpMeridianSlot', (Player("gbId/Id"),Int("slotId"),), RARG(0), gameconst.BASE, '将经脉x所有穴位升至满级并贯通', ALLSIDE, GOD_GROUPS)
def gmLevelUpMeridianSlot(su,player,slotId):
    if player is None:
        return False, '执行失败'
    player.gmLevelUpMeridianSlot(slotId)
    return True, '执行成功'

@gm_cmd('$gmLevelUpMeridianPoint', (Player("gbId/Id"),Int("slotId"), Int("pointId"), Int("level"),), RARG(0), gameconst.BASE, '升级指定经脉的指定穴位1级或至满级', ALLSIDE, GOD_GROUPS)
def gmLevelUpMeridianPoint(su,player,slotId,pointId,level):
    if player is None:
        return False, '执行失败'
    player.gmLevelUpMeridianPoint(slotId,pointId,level)
    return True, '执行成功'


# --------------------------dev test only cmd segment-----------------------------------------------------------------------------------------------------------------------------------------
