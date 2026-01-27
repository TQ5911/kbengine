# -*- coding: utf-8 -*-
import hashlib
import time
import KBEngine
from KBEDebug import *

import gameengine
import gameconst
import gmAdmin
import gmCommand
import formula
import gameglobal
import gamesql
import gametimer
import functools

import creep_base as MD
import buff_buff as BBD
import itemData_itemData as ITEM_DATA
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import gearBase_gearBase as GBG
import gearEnhance_gearconst as GEGCD
import gearBase_typeTab as GBTT
import gearEnhance_gearStrengthen as GEGS

import json
import redisUtils
import random
import utils
import dataUtils
import dropAward
import awardContext
import gameconfig
import mailAssistor

import Mail
import base64
import gameclass
import mail_config as MCD
import _pickle as cPickle
import itemFactory
import math, Math, sMath
import actionContext
import iRouter
import gearBase_gearConst as GBGCD

BASE = gameconst.BASE
CELL = gameconst.CELL
ALL = gameconst.ALL
INSIDE = gmAdmin.INSIDE
ALLSIDE = gmAdmin.ALLSIDE

Int = gmCommand.Int
Str = gmCommand.Str
Float = gmCommand.Float
Player = gmCommand.Player
Entity = gmCommand.Entity
PlayerAccount = gmCommand.PlayerAccount

gm_cmd = gmCommand.gm_cmd
forwardCommand = gmCommand.forwardCommand
callApps = gmCommand._callApps

RARG = gmCommand.RARG
RSU = gmCommand.RSU
RSTUB = gmCommand.RSTUB
RONE = gmCommand.RONE
RALL = gmCommand.RALL
SELF = gmCommand.SELF

GOD_GROUPS = gmCommand.GOD_GROUPS
DEV_GROUPS = gmCommand.DEV_GROUPS

IS_CELL = (KBEngine.component == 'cellapp')
IS_BASE = (KBEngine.component == 'baseapp')

import importlib

def dynamic_import(module_name: str, class_name: str = None):
    """
    根据传入的模块名动态导入模块，可选导入指定类

    Args:
        module_name: 要导入的模块名称（例如："math" 或 "my_package.my_module"）
        class_name: 可选，要导入的类名

    Returns:
        导入的模块或类对象
    """
    try:
        # 导入模块
        module = importlib.import_module(module_name)

        if class_name:
            # 如果指定了类名，则从模块中获取该类
            return getattr(module, class_name)
        else:
            # 否则返回整个模块
            return module

    except ImportError as e:
        print(f"导入模块失败: {e}")
        return None
    except AttributeError as e:
        print(f"模块中不存在该类: {e}")
        return None

@gm_cmd('$gmsetstate', (Player("gbId/Id"), Int("state"),Int("Pylance"),), RARG(0), gameconst.CELL, '设置状态', ALLSIDE, GOD_GROUPS, minArgs=2)
def gmsetstate(su, player, state, Pylance = 1):
    if Pylance == 1:
        player.setState(state)
    elif Pylance == 0:
        player.removeState(state)
    else:
        return False,"执行失败"
    return True, '执行成功'

@gm_cmd('$gotomapdataid', (Player("gbId/Id"), Int("mapdataid")), RARG(0), CELL,
        '传送到地图实体位置', ALLSIDE, GOD_GROUPS, minArgs=2)
def gotomapdataid(su, player, mapdataid):
    if mapdataid and mapdataid > 10000000:
        mapid = str(mapdataid)[:4]
        modleName = "dun_" + mapid
        mapdata = dynamic_import(modleName)
        if str(mapdataid) in mapdata.datas:
            x = mapdata.datas[str(mapdataid)]["PosX"]
            y = mapdata.datas[str(mapdataid)]["PosY"]
            z = mapdata.datas[str(mapdataid)]["PosZ"]
            pos = (x,y,z)
            mapidNO = int(mapid) * gameconst.SPACE_NO_INTERVAL
            if mapidNO and mapidNO != player.spaceNo:
                player.base.teleportByNo(mapidNO, pos, player.direction, '', ())
            else:
                player.telToPos(pos)
        else:
            return False, '执行失败,id不存在'
    else:
        return False, '执行失败,id小于10000000，不是地图编辑器里的ID'

@gm_cmd('$sethp', (Player("gbId/Id"), Int("hp"),), RARG(0), gameconst.CELL, '设置血量', ALLSIDE, GOD_GROUPS)
def setPlayerHp(su, player, hp):
    if hp < 0:
        return False, '血量不能小于0'

    player.hp = hp
    return True, '执行成功'


@gm_cmd('$adjfullHp', (Player("gbId/Id"), Int("fullhp"),), RARG(0), gameconst.CELL, '添加总血量', ALLSIDE, GOD_GROUPS)
def setPlayerFullHp(su, player, addfullhp):
    if addfullhp < 0:
        return False, '血量不能小于0'
    player.setProp('adjFullHp', addfullhp, gameconst.SourceType.Default)
    player.setProp('adjFullMp', addfullhp, gameconst.SourceType.Default)
    player.addBuff(64000069,1,player.id)
    return True, '执行成功'




@gm_cmd('$setultraSkillPower', (Player("gbId/Id"), Int("ultraSkillPower"),), RARG(0), gameconst.CELL, '设置大招充能值', ALLSIDE, GOD_GROUPS)
def setPlayerultraSkillPower(su, player, ultraSkillPower):
    player.ultraSkillPower = ultraSkillPower
    return True, '执行成功'

@gm_cmd('$reliveToPos', (Player("gbId/Id"), Str("position"), Int("hp")), RARG(0), CELL, '复活', ALLSIDE, GOD_GROUPS)
def reliveToPos(su, player, position_str, hp):
    if position_str == 'None' or not position_str:
        position = None
    else:
        coords = position_str.strip('()').split(',')
        position = Math.Vector3(float(coords[0]), float(coords[1]), float(coords[2]))
    
    direction = player.direction
    player.reliveToPos(position, direction, hp, None)
    return True, '执行成功'



@gm_cmd('$showprop', (Int("entityId"),), RSU, CELL, '显示实体属性', INSIDE, GOD_GROUPS)
def showEntityProp(su, entityId):
    if entityId <= 0:
        return False, '非法的实体ID'

    target = KBEngine.entities.get(entityId, None)
    if not target:
        return False, '没有找到ID为%s实体' % entityId

    print('-------------------- prop start --------------------')
    import fightProp_define as FDD
    for propName in FDD.datas.keys():
        if hasattr(target, propName):
            print('{0}: {1}'.format(propName, getattr(target, propName)))
    print('-------------------- prop end   --------------------')

    return True, '执行成功'

@gm_cmd('$deducthp', (Player("gbId/Id"), Int('damage'), Int('entity id'),), RARG(0), CELL, '扣除目标血量', ALLSIDE, GOD_GROUPS, minArgs=1)
def deductHp(su, player, damage, eid=0):
    # 如果没有指定目标实体ID，则使用玩家当前选中的目标
    eid = eid or player.selectedTargetId
    # 获取目标实体
    e = KBEngine.entities.get(eid)
    # 检查目标是否存在且是战斗单位
    if not e or not e.IsCombatUnit:
        return False, '%s不存在或者不是战斗单位' % eid

    # 确保扣除的血量不会超过目标当前血量
    actual_damage = min(damage, e.hp)
    # 修改目标血量，从当前血量中扣除指定数值
    e.modifyHP(-actual_damage, player.id, gameconst.SourceType.Skill, 0)
    # 返回执行成功的消息，包含实际扣除的血量
    return True, '成功扣除%d点血量，目标剩余血量: %d' % (actual_damage, e.hp)

@gm_cmd('$createmonster', (Player("gbId/Id"), Int('monster id'), Int('level'), Int('monsterNum'), Float('radius'), Int('force')), RARG(0), CELL,
        '创建怪物，可指定数量和半径', ALLSIDE, GOD_GROUPS, minArgs=3)
def createMonster(su, player, monsterId, level, monsterNum=1, radius=0, force=0):
    # 检查怪物ID和等级是否有效
    if monsterId not in MD.datas or level < 1 or monsterNum < 1:
        return False, '执行失败'
    # 计算每个怪物之间的角度间隔（弧度）
    angle_step = 2 * math.pi / monsterNum

    # 玩家当前朝向（假设player.direction是欧拉角或四元数）
    # 将玩家朝向转换为弧度角，这里假设direction.z是偏航角（yaw）
    player_yaw = player.direction.z

    # 创建怪物的信息列表
    monster_positions = []

    # 计算圆周上各点的位置
    for i in range(monsterNum):
        # 计算当前怪物的角度
        angle = i * angle_step

        # 计算最终角度（玩家朝向 + 相对角度）
        final_angle = player_yaw + angle

        # 计算怪物在圆上的坐标
        x_offset = radius * math.sin(final_angle)
        z_offset = radius * math.cos(final_angle)

        # 玩家位置加上偏移量
        monster_x = player.position.x + x_offset
        monster_y = player.position.y  # 保持与玩家相同的高度
        monster_z = player.position.z + z_offset

        monster_position = (monster_x, monster_y, monster_z)

    # 创建怪物参数
        props = {
            'monsterId': monsterId,
            'spaceMgrId': player.spaceMgrId,
            'spaceNo': player.spaceNo,
            'position': monster_position,
            'direction': player.direction,  # 可以让怪物面向与玩家相同的方向
            'level': level,
            'force': force,
        }
        # 创建一个怪物
        KBEngine.createEntity(
            'Monster',
            player.spaceID,
            monster_position,
            player.direction,
            props,
        )

    return True, f'成功在玩家周围{radius}米的圆上创建了{monsterNum}个怪物'


@gm_cmd('$addcoin', (Player("gbId/Id", raw=True), Float("num"),), RARG(0), BASE, '增加货币', ALLSIDE, GOD_GROUPS)
def addCoin(su, player, num):
    opUUID = KBEngine.genUUID64()
    src = AAC_AACDD.datas.BONUS_SRC_GM
    detail = gameclass.AwardDetail(gm_cmd='$addcoin', num=num)

    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        if num > 0:
            gamesql.recordAvatarOfflineCallback(gbId, 'addCoin', (num, opUUID, src, detail))
        elif num < 0:
            gamesql.recordAvatarOfflineCallback(gbId, 'gmDeleteItems', (gameconst.ItemId.COIN, abs(num), detail))
    else:
        if num > 0:
            player.addCoin(num, opUUID, src, detail)
        elif num < 0:
            player.deductCoinNoLimit(abs(num), opUUID, src, detail)

    su.onCommandResult(0, '', {})

    return True, '执行成功'


@gm_cmd('$deductcoin', (Player("gbId/Id", raw=True), Float("num"),), RARG(0), BASE, '扣除货币，不够时失败', ALLSIDE,
        GOD_GROUPS)
def deductcoinCompletely(su, player, num):
    opUUID = KBEngine.genUUID64()
    src = AAC_AACDD.datas.BONUS_SRC_GM
    num = abs(num)
    detail = gameclass.AwardDetail(gm_cmd='$addcoin', num=num)

    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player

        def _onCheckDeduct(ret, hasCoin, alreadyDeductNum, needDeduct):
            if ret:
                su.onCommandResult(ret, '', {'coin': hasCoin})
                return
            gamesql.recordAvatarOfflineCallback(gbId, 'gmDeleteItems', (gameconst.ItemId.COIN, num, detail))
            su.onCommandResult(0, '', {})

        gamesql.checkOfflineDeductWealth(gbId, gameconst.ItemId.COIN, num, _onCheckDeduct)
    else:
        if player.deductCoin(num, opUUID, src, detail, bMsg=False):
            su.onCommandResult(0, '', {})
        else:
            su.onCommandResult(gameconst.GMCommandErr.INSUFFICIENT, 'insufficient', {'coin': player.coin})

    return True, '执行成功'


@gm_cmd('$setvar', (Player("gbId/Id"), Int("varId"), Int("value"),), RARG(0), BASE, '设置变量值', ALLSIDE, GOD_GROUPS)
def setVar(su, player, varId, value):
    opUUID = KBEngine.genUUID64()
    varSrc = gameconst.VarChangeSrc.VAR_SRC_GM
    desc = 'gm_cmd:$setvar {} {}'.format(varId, value)
    player.gmSetVar(varId, value, opUUID, varSrc, desc)
    return True, '执行成功'


@gm_cmd('$getvar', (Player("gbId/Id"), Int("varId"),), RARG(0), BASE, '读取变量值', ALLSIDE, GOD_GROUPS)
def getVar(su, player, varId):
    result, desc = player.gmGetVar(varId)
    return result, desc


@gm_cmd('$clearspace', (Str('clearType'),), RSU, CELL, '清除当前场景实体', INSIDE, GOD_GROUPS, minArgs=0)
def clearspace(su, clearType):
    if clearType == "":
        lineType = formula.getLineType(su.spaceNo)
        typeList = utils.getDunStructureModuleData(lineType)['InitEntities'].keys()
        for e in KBEngine.entities.values():
            if e.__class__.__name__ in typeList:
                e.safeDestroy()
    else:
        for e in KBEngine.entities.values():
            if e.__class__.__name__ == clearType:
                e.safeDestroy()
    return True, '执行成功'


@gm_cmd('$crtbyid', (Str('game entity id'),), RSU, CELL, '根据唯一标识创建实体', INSIDE,
        GOD_GROUPS)
def createEntityById(su, gameEntityId):
    spaceBase = gameengine.getSpaceBase(su.spaceNo)

    if not spaceBase:
        return False, '未知空间'

    spaceCellCall = spaceBase.cell

    spaceCellCall.createEntityById(gameEntityId, None)

    return True, '执行成功'


@gm_cmd('$crtherebyid', (Str('game entity id'),), RSU, CELL,
        '根据唯一标识在当前位置创建实体', INSIDE, GOD_GROUPS)
def createEntityHereById(su, gameEntityId):
    spaceBase = gameengine.getSpaceBase(su.spaceNo)

    if not spaceBase:
        return False, '未知空间'

    spaceCellCall = spaceBase.cell

    spaceCellCall.createEntityById(gameEntityId, {'Pos': su.position})

    return True, '执行成功'


@gm_cmd('$rmbyid', (Str('game entity id'),), RSU, CELL,
        '根据唯一标识删除创建的实体', INSIDE, GOD_GROUPS)
def removeEntityById(su, gameEntityId):
    spaceBase = gameengine.getSpaceBase(su.spaceNo)

    if not spaceBase:
        return False, '未知空间'

    spaceBase.cell.removeEntityById(gameEntityId)

    return True


@gm_cmd('$createRobot', (Player("gbId/Id"), Int('robotDataId'), Int('level')), RARG(0), CELL, '创建机器人', ALLSIDE,
        GOD_GROUPS)
def createRobot(su, player, robotDataId, level):
    import utils
    import skillInfo
    import gameconst
    import robotData_robotData

    def _createEntity():
        entType = 'AvatarMirror'
        extraProps = {'spaceNo': player.spaceNo,
                      'monsterId': 0,
                      'gbId': KBEngine.genUUID64()}

        if player.spaceMgr:
            extraProps.update({'spaceMgrId': player.spaceMgr.id,
                               'spaceMgrBox': player.spaceMgr.base})

        randomTempBotId = robotDataId or random.choice(list(robotData_robotData.datas))

        # init school
        school = robotData_robotData.datas[randomTempBotId]['schoolID']

        # init name
        name = utils.getRandomName()

        props = utils.getRobotPropDict(randomTempBotId, name, school, level)

        props['force'] = gameconst.ForceType.Monster
        props['sex'] = utils.getRandomSex()

        props.update(extraProps)

        ent = KBEngine.createEntity(entType, player.spaceID, tuple(player.position), tuple(player.direction), props)
        return ent

    try:
        e = _createEntity()
    except:
        gameengine.reportCritical('gm create Robot error')
        return False, '执行失败, 创建中出错, 请联系管理员排查'
    if not e:
        return False, '执行失败'
    return True, '执行成功'


@gm_cmd('$createnpc', (Player("gbId/Id"), Int('npc_id'), Int('level')), RARG(0), CELL, '创建NPC', ALLSIDE, GOD_GROUPS)
def createNPC(su, player, npcId, level):
    import NPC_NPC as NPC_D
    import creep_base as CB
    if npcId not in NPC_D.datas or level < 1:
        return False, '执行失败, 请检查参数'

    params = {
        'npcId': npcId,
        'name': NPC_D.datas[npcId]['name'],
        'spaceNo': player.spaceNo,
        'spaceID': player.spaceID,
        'position': player.position,
        'direction': player.direction,
    }

    _npcCreepId = NPC_D.datas[int(npcId)].get('creepID')
    className = 'Npc'
    if _npcCreepId and _npcCreepId in CB.datas and CB.datas[_npcCreepId]['AI']:
        className = 'CNpc'
        _npcAI = NPC_D.datas[int(npcId)].get('AI')
        if _npcAI:
            params.update({'aiName': _npcAI})

    player.base.callMethod('gmCreateEntityHasBase', (className, params))
    return True, '执行成功'


@gm_cmd('$createTeleporter', (Player("gbId/Id"), Int('teleportId'), Int('type'), Str('mapIds')), RARG(0), CELL, '创建传送门', ALLSIDE,
        GOD_GROUPS)
def createTeleporter(su, player, teleportId, teleportType, mapsIds):
    _mapIds = mapsIds.split(',')
    _mapIds = [int(i) for i in _mapIds]
    props = {
        'teleportType': teleportType,
        'mapIds': _mapIds,
        'name': 'hahaha',
        'teleporterId': teleportId,
        'spaceNo': player.spaceNo,
        'spaceno': player.spaceNo,
        'direction': player.direction,
        'position': player.position,
    }
    KBEngine.createEntity(
        'Teleporter',
        player.spaceID,
        player.position,
        player.direction,
        props,
    )
    # player.base.callMethod('gmCreateEntityHasBase', ('Collection', props))
    return True, '执行成功'


@gm_cmd('$createcollection', (Player("gbId/Id"), Int('collection id'),), RARG(0), CELL, '创建采集物', ALLSIDE,
        GOD_GROUPS)
def createCollection(su, player, collectionId):
    import NPC_Pick
    if collectionId not in NPC_Pick.datas:
        return False, '执行失败'

    props = {
        'name': NPC_Pick.datas[collectionId]['name'],
        'type': NPC_Pick.datas[collectionId]['type'],
        'collectionId': collectionId,
        'spaceNo': player.spaceNo,
        'position': player.position,
        'direction': player.direction,
        'spaceMgrId': player.spaceMgrId,
    }
    KBEngine.createEntity(
        'Collection',
        player.spaceID,
        player.position,
        player.direction,
        props,
    )
    # player.base.callMethod('gmCreateEntityHasBase', ('Collection', props))
    return True, '执行成功'


@gm_cmd('$goto', (Player("gbId/Id"), Float('x'), Float('y'), Float('z'), Int('spaceNo')), RARG(0), CELL,
        '传送到目标位置', ALLSIDE, GOD_GROUPS, minArgs=4)
def gotoPosition(su, player, x, y, z, spaceNo=0):
    if spaceNo and spaceNo != player.spaceNo:
        if not formula.isStaticSpace(player.spaceNo) or not formula.isStaticSpace(spaceNo):
            return False, '只能在大世界使用'
        player.base.teleportByNo(spaceNo, (x, y, z), player.direction, '', ())
    else:
        player.telToPos((x, y, z))
    return True, '执行成功'


@gm_cmd('$gotoid', (Entity('entity id'),), RARG(0), CELL, '传送到目标实体位置', INSIDE, GOD_GROUPS)
def gotoById(su, e):
    if su.spaceNo == e.spaceNo:
        su.telToPos(e.position)
        return True, '执行成功'

    su.cell.callMethod('gmGotoByid', (e, e.spaceNo, e.position, e.direction, getattr(e, 'tilemapsInfo', '')))
    return True, '执行成功'


@gm_cmd('$getpos', (Entity('entity id'),), RARG(0), CELL, '获得目标实体位置', INSIDE, GOD_GROUPS)
def getPosition(su, e):
    return True, '执行成功：%s %s' % (e.spaceNo, str(e.position))


@gm_cmd('$recordpos', (Entity('entity id'), Int('invaild'),), RARG(0), CELL, '记录目标实体位置和面向', INSIDE,
        GOD_GROUPS, minArgs=1)
def recordPos(su, e, invaild=1):
    writeStr = "recordpos %s %s %s,%s,%s\n" % (
        e.position[0], e.position[1], e.position[2], str(e.direction[2]), invaild)
    print("%s " % writeStr)
    detailFile = open("recordpos.txt", "a", encoding='UTF-8')
    detailFile.write(writeStr)
    detailFile.close()
    return True, '执行成功：%s %s %s' % (e.spaceNo, str(e.position), str(e.direction[2]))


@gm_cmd('$debugai', (Entity('entity id'), Int('log ai'), Int('log hate')), RARG(0), CELL, '打开对应实体的ai日志',
        ALLSIDE, GOD_GROUPS)
def toggleAIDebug(su, e, enableLogAITrace, enableLogHate):
    if not hasattr(e, 'aiController'):
        return False, '执行失败，实体没有aiController'

    if not hasattr(e.aiController, 'tree'):
        return False, '执行失败，实体没有aiController.tree'

    e.aiController.logAITrace = enableLogAITrace

    e.aiController.logHate = enableLogHate

    return True, '执行成功'


@gm_cmd('$speed', (Player('entity id'), Float('speed')), RARG(0), CELL, '设置玩家速度', ALLSIDE, GOD_GROUPS)
def setSpeed(su, player, speed):
    if gmCommand.isRawPlayer(player):
        return False, '执行失败'

    player.topSpeed = speed * 15
    player.setSpeed(speed)
    return True, '执行成功'


@gm_cmd('$moralValue', (Player('entity id'), Int('moralValue')), RARG(0), CELL, '设置玩家善恶值', ALLSIDE, GOD_GROUPS)
def setmoralValue(su, player, moralValue):
    if gmCommand.isRawPlayer(player):
        return False, '执行失败'

    player.moralValue = moralValue
    player.moralLevel = utils.getMoralLevel(player.moralValue)
    return True, '执行成功'

@gm_cmd('$setRewardNumber', (Player('gbId/Id'), Int('RewardNumber')), RARG(0), BASE, '设置讨伐次数', ALLSIDE, GOD_GROUPS)
def setRewardNumber(su, player, RewardNumber):
    if gmCommand.isRawPlayer(player):
        return False, '执行失败'
    player.crusadeInfo.rewardNumber = RewardNumber
    return True, '执行成功'

@gm_cmd('$topspeed', (Player('entity id'), Float('speed')), RARG(0), CELL, '设置玩家最大速度', ALLSIDE, GOD_GROUPS)
def setTopSpeed(su, player, speed):
    if gmCommand.isRawPlayer(player):
        return False, '执行失败'

    player.topSpeed = speed
    return True, '执行成功'


@gm_cmd('$getSpeed', (Player('entity id'),), RARG(0), CELL, 'get玩家速度', ALLSIDE, GOD_GROUPS)
def getSpeed(su, player):
    if gmCommand.isRawPlayer(player):
        return False, '执行失败'

    print("getSpeed------", player.getSpeed())
    return True, '' + str(player.getSpeed())


@gm_cmd('$setpos', (Player('palyer id'), Float('x'), Float('y'), Float('z'), Float('dir'), Int('spaceNo')), RARG(0),
        CELL, '设置玩家位置', ALLSIDE, GOD_GROUPS, True, minArgs=4)
def setPosition(su, player, x, y, z, direction=0, spaceNo=0):
    spaceNo = spaceNo or player.spaceNo
    tgtDirection = player.direction
    if direction:
        tgtDirection[2] = direction
    player.teleportToCell(player, spaceNo, (x, y, z), tgtDirection, '', ())
    return True, '执行成功'


@gm_cmd('$getrandomitems', (Player("gbId/Id"), Int('bagType'), Int('itemNum'), Int('bindType')), RARG(0), BASE,
        '获取随机物品', ALLSIDE, GOD_GROUPS)
def getRandomItems(su, player, bagType, itemNum, bindType):
    if itemNum < 1 or itemNum > 99:
        return False, '执行失败'
    itemsFilter = filter(lambda data: bagType == data['type'], ITEM_DATA.datas.values())
    items = list(itemsFilter)
    if 0 == len(items):
        return False, '执行失败'

    itemDict = {}
    sumNum = 0
    loopCnt = 0
    while sumNum < itemNum and loopCnt < 99:
        loopCnt += 1
        oneItem = random.choice(items)
        maxSize = oneItem['maxStackSize']
        if maxSize == 0:
            continue
        addNum = random.randint(1, maxSize)
        if addNum + sumNum > itemNum:
            addNum = itemNum - sumNum
        sumNum += addNum
        itemId = oneItem['ID']
        if itemId in itemDict:
            itemDict[itemId] += addNum
        else:
            itemDict[itemId] = addNum

    for itemId, itemAddNum in itemDict.items():
        itemData = ITEM_DATA.datas.get(itemId, None)
        maxSize = itemData['maxStackSize']
        if 0 == maxSize:
            continue
        leftNum = itemAddNum
        while leftNum > 0:
            if leftNum > maxSize:
                addNum = maxSize
            else:
                addNum = leftNum
            leftNum -= addNum
            ret = player.gmAddItems(bagType, itemId, addNum, 'gm_cmd:$getrandomitems %s' % itemNum, bindType=bindType)
            if ret:
                return False, '执行失败'
    return True, '执行成功'


@gm_cmd('$getfixedbox',
        (Player("gbId/Id", raw=True), Int('bagType'), Int('itemId'), Int('bindType'), Str('boxItemsJson')), RARG(0),
        BASE, '获取固定内容宝箱', ALLSIDE, GOD_GROUPS)
def getFixedItemsBox(su, player, bagType, itemId, bindType, boxItemsJson):
    if bagType not in (0, 1, 2, 3):
        return False, '执行失败, 无法添加此物品ID, 背包类型错误, {}-{}--{}'.format(itemId, bagType, bindType)
    try:
        boxItems = json.loads(boxItemsJson)
    except Exception as e:
        su.onCommandResult(gameconst.GMCommandErr.ARGS_ERR, '', {})
        return False, '执行失败'

    boxWealth = dropAward.AwardVal()
    for itemIdStr, itData in boxItems.items():
        boxItemId = int(itemIdStr)
        itemNum, boxItemBindType = itData
        boxWealth.addWealthByItemId(boxItemId, itemNum, boxItemBindType)

    fixedBox = itemFactory.ItemFactory.createItem(itemId, 1, bindType, boxWealth=boxWealth)
    wval = dropAward.AwardVal().addWealthByObjList([fixedBox])

    detail = 'gm_cmd:$getitems %s %s %s' % (itemId, itemNum, bindType)
    opUUID = KBEngine.genUUID64()
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        gamesql.recordAvatarOfflineCallback(gbId, 'gmAddWealth', (bagType, wval, opUUID, detail))
    else:
        player.gmAddWealth(bagType, wval, opUUID, detail)

    su.onCommandResult(0, '', {})
    return True, '执行成功'

@gm_cmd('$getitems', (Player("gbId/Id", raw=True), Int('bagType'), Int('itemNum'), Float('_bindType'), Int('itemId_Start'), Int('itemId_End')),
        RARG(0), BASE, '获取指定物品', ALLSIDE, GOD_GROUPS, minArgs=4)
def getItems(su, player, bagType, itemNum, _bindType, itemId_Start, itemId_End = 0):
    if itemId_End == 0 and itemId_Start != 0:
        itemId_End = itemId_Start
    if bagType not in (0, 1, 2, 3):
        return False, '执行失败, 背包类型错误'
    if 0 < _bindType < 1:
        bindTypes = [gameconst.ItemBindType.BIND, gameconst.ItemBindType.NORMAL]
    elif _bindType == 0:
        bindTypes = [gameconst.ItemBindType.BIND]
    elif _bindType == 1:
        bindTypes = [gameconst.ItemBindType.NORMAL]
    else:
        return False, '执行失败, 绑定概率错误'
    for bindType in bindTypes:
        for itemId in range(min(itemId_Start, itemId_End), max(itemId_Start, itemId_End) + 1):
            # 检查是否在装备表中存在
            if itemId in GBG.datas:
                # 检查是否为离线玩家，如果是离线玩家则执行失败
                if gmCommand.isRawPlayer(player):
                    continue
                else:
                    # 调用玩家的gmAddGearbaseEquipItem方法添加装备
                    ret = player.gmAddGearbaseEquipItem(itemId,bindType)
            # 如果不存在，检查是否在普通物品表中存在
            elif itemId in ITEM_DATA.datas:
                detail = 'gm_cmd:$getitems %s %s %s' % (itemId, itemNum, bindType)
                # 判断是否为原始玩家对象（可能是离线玩家）
                if gmCommand.isRawPlayer(player):
                    # 如果是原始玩家，解包玩家信息
                    gbId, name, accountName, dbId = player
                    # 记录离线玩家的回调，当玩家上线时执行gmAddItems操作
                    gamesql.recordAvatarOfflineCallback(gbId, 'gmAddItems', (bagType, itemId, itemNum, detail, bindType))
                else:
                    DEBUG_MSG('gmAddItems:', bagType, itemId, itemNum, detail,bindType)
                    # 如果是在线玩家，直接调用gmAddItems方法添加物品
                    player.gmAddItems(bagType, itemId, itemNum, detail,bindType)
            else:
                continue
    su.onCommandResult(0, '', {})
    return True, '执行成功'


@gm_cmd('$delitems', (
        Player("gbId/Id", raw=True), Int('itemId'), Int('itemNum'),
        Int('bindType', default=gameconst.ItemBindType.BIND)),
        RARG(0), BASE, '删除指定物品', ALLSIDE, GOD_GROUPS, minArgs=3)
def deleteItems(su, player, itemId, itemNum, bindType=gameconst.ItemBindType.BIND):
    detail = ''
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        gamesql.recordAvatarOfflineCallback(gbId, 'gmDeleteItems', (itemId, itemNum, detail, bindType))
    else:
        player.gmDeleteItems(itemId, itemNum, detail, bindType)

    su.onCommandResult(0, '', {})
    return True, '执行成功'


@gm_cmd('$cleanbag', (Player("gbId/Id"), Int('bagType'),), RARG(0), BASE, '清空背包', ALLSIDE, GOD_GROUPS)
def clenBag(su, player, bagType):
    ret = player.gmCleanBag(bagType)
    if ret:
        return True, '执行成功'
    else:
        return False, '执行失败'

@gm_cmd('$getGearbaseEquipItem', (Player("gbId/Id"), Int('templateId'), Int('bindType'), Int('grade')), RARG(0), BASE, '获取装备', ALLSIDE, GOD_GROUPS)
def getGear(su, player, templateId, bindType, grade):
    if gmCommand.isRawPlayer(player):
        return False, '执行失败'
    ret = player.gmAddGearbaseEquipItem(templateId, bindType, grade)
    if ret == gameconst.BagOPStat.BAG_OP_STAT_OK:
        return True, '执行成功'
    else:
        return False, '执行失败'


@gm_cmd('$getReward', (Player("gbId/Id"), Int('dropId'), Int('num'),), RARG(0), BASE, '获取奖励', ALLSIDE, GOD_GROUPS)
def getReward(su, player, dropId, num):
    awardCtx = awardContext.CommonContext(0, {'lv': player.getRoleCacheAttr('level', 0)})
    opUUID = KBEngine.genUUID64()
    ret = player.addAwards(AAC_AACDD.datas.BONUS_SRC_GM, dropId, num, opUUID, '', awardCtx)
    if ret:
        return True, '执行成功'
    else:
        return False, '执行失败'

@gm_cmd('$getDropid', (Player("gbId/Id"), Int('dropId'), Int('num'),), RARG(0), BASE, '执行掉落', ALLSIDE, GOD_GROUPS)
def getDropid(su, player, dropId, num):
    for i in range(num):
        awardCtx = awardContext.CommonContext(0, {'lv': player.getRoleCacheAttr('level', 0)})
        awardCtx.addContextVar('avatarId', player.id)
        awardCtx.addContextVar('school', player.getRoleCacheAttr('school', 0))
        opUUID = KBEngine.genUUID64()
        awardVal = dropAward._getDropAward([dropId], awardCtx)
        autoDisassemble = player.cliConfigDic.get(gameconst.CliConfigDef.EQUIP_AUTO_DISA_KEY,
                                                gameconst.CliConfigDef.EQUIP_AUTO_DISA_DEFAULT_VAL)
        if autoDisassemble:
            equipList = awardVal.itemWealth.popDropEquipObjs()
            disassembleEquips = []
            for it in equipList:
                if player.canEquipAutoDisassemble(player, it) and it.canBeDisassembled():
                    awardVal += it.returnWealthyByDisassemble(player)
                    disassembleEquips.append(it)
            for it in disassembleEquips:
                equipList.remove(it)
            awardVal.itemWealth.addItemObjs(equipList)
            disassembleEquips and player.onMessagePre(GBGCD.datas['disassembleChatMsg']['value'], [])
        ret = player.addWealth(AAC_AACDD.datas.BONUS_SRC_GM, awardVal, opUUID, None, awardCtx, notify=True, popWindow=False)
    if ret:
        return True, '执行成功'
    else:
        return False, '执行失败'

@gm_cmd('$gmenterDungeon', (Player("gbId/Id"),Int('dungeonNo'), ), RARG(0), CELL, '管理员进入副本', ALLSIDE, GOD_GROUPS)
def gmEnterDungeon(su,player, dungeonNo):
    import gamePlay_gamePlay
    import dungeonSrc
    if dungeonNo not in gamePlay_gamePlay.datas:
        return False, '执行失败, 没有找到相应副本ID'

    src = dungeonSrc.DungeonFromClientGMSrc(player.base, player.gbId)

    dungeonSpaceType = gamePlay_gamePlay.datas[dungeonNo]['type']
    dungeonEnterType = gamePlay_gamePlay.datas[dungeonNo]['enterType']
    if gameconst.DungeonType.isBothDungeon(dungeonSpaceType, dungeonEnterType):
        if player.isInTeam(player.gbId):
            player.gmEnterTeamDungeon(dungeonNo, src)
            return True, '执行成功, gm正在尝试进入全类型副本(组队)'
        else:
            player.gmEnterSingleDungeon(dungeonNo, src)
            return True, '执行成功, gm正在尝试进入全类型副本(单人)'
    elif gameconst.DungeonType.isTeamDungeon(dungeonSpaceType, dungeonEnterType):
        if not player.isInTeam(player.gbId):
            return False, '執行失敗, gm-组队副本必须组队进入'
        player.gmEnterTeamDungeon(dungeonNo, src)
        return True, '执行成功, gm正在尝试进入组队副本'
    elif gameconst.DungeonType.isSingleDungeon(dungeonSpaceType, dungeonEnterType):
        player.gmEnterSingleDungeon(dungeonNo, src)
        return True, '执行成功, gm正在尝试进入单人副本'
    elif gameconst.DungeonType.isRaidDungeon(dungeonSpaceType, dungeonEnterType):
        player.gmEnterRaidDungeon(dungeonNo, src)
        return True, '执行成功, gm正在尝试进入团队副本'
    else:
        return False, '执行失败, gm-不支持的副本类型'

@gm_cmd('$enterDungeon', (Player("gbId/Id"),Int('dungeonNo'), ), RARG(0), CELL, '进入副本', ALLSIDE, GOD_GROUPS)
def enterDungeon(su,player, dungeonNo):
    import gamePlay_gamePlay
    import dungeonSrc
    if dungeonNo not in gamePlay_gamePlay.datas:
        return False, '执行失败, 没有找到相应副本ID'

    src = dungeonSrc.DungeonFromClientSrc(player.base, player.gbId)

    dungeonSpaceType = gamePlay_gamePlay.datas[dungeonNo]['type']
    dungeonEnterType = gamePlay_gamePlay.datas[dungeonNo]['enterType']
    if gameconst.DungeonType.isBothDungeon(dungeonSpaceType, dungeonEnterType):
        if player.isInTeam(player.gbId):
            player.selfEnterTeamDungeon(dungeonNo, src)
            return True, '执行成功, 正在尝试进入全类型副本(组队)'
        else:
            player.selfEnterSingleDungeon(dungeonNo, src)
            return True, '执行成功, 正在尝试进入全类型副本(单人)'
    elif gameconst.DungeonType.isTeamDungeon(dungeonSpaceType, dungeonEnterType):
        if not player.isInTeam(player.gbId):
            return False, '執行失敗, 组队副本必须组队进入'
        player.selfEnterTeamDungeon(dungeonNo, src)
        return True, '执行成功, 正在尝试进入组队副本'
    elif gameconst.DungeonType.isSingleDungeon(dungeonSpaceType, dungeonEnterType):
        player.selfEnterSingleDungeon(dungeonNo, src)
        return True, '执行成功, 正在尝试进入单人副本'
    elif gameconst.DungeonType.isRaidDungeon(dungeonSpaceType, dungeonEnterType):
        player.selfEnterRaidDungeon(dungeonNo, src)
    else:
        return False, '执行失败, 不支持的副本类型'

@gm_cmd('$setgmmode', (Player("gbId/Id"), Int("mode"),), RARG(0), gameconst.BASE, '设置gm模式', ALLSIDE, GOD_GROUPS)
def setGmMode(su, player, gmMode):
    if gmMode not in gameconst.GmMode.ALL_MODES:
        return False, '无效的mode：%s' % (gmMode,)

    player.gmMode = gmMode
    player.cell.callMethod('_onSetGmMode', (gmMode,))
    return True, '执行成功'


@gm_cmd('$sendmail', (Str("toGBID"), Int('mailId'), Str('attachStr'), Str('despArgsStr'), Str('title'), Str('cont')),
        RSU, gameconst.BASE, '向指定玩家发送一封邮件', INSIDE, GOD_GROUPS)
def sendMail(su, toGBID, mailId, attachStr, despArgsStr, title, cont):
    toGBID = int(toGBID)
    attach = mailAssistor.parseAttachStr(attachStr)
    despArgs = mailAssistor.parseDespStr(despArgsStr)
    title = title.strip("[] ")
    cont = cont.strip("[] ")
    mailAssistor.sendMailToPlayers([toGBID], mailId, extraAttach=attach, despArgs=despArgs, title=title, cont=cont, srcType=AAC_AACDD.datas.BONUS_SRC_GM)
    return True, '执行成功'

@gm_cmd('$sendMailByGBIDNoMailId', (Player("gbId/Id", raw=True), Str('attachStr'), Str('title'), Str('cont')), RARG(0), BASE,
        '向指定玩家发送一封自定义邮件', ALLSIDE, GOD_GROUPS)
def sendMailByGBIDNoMailId(su, player, attachStr, title, cont):
    DEBUG_MSG('sendMailByGBIDNoMailId:', attachStr, title, cont)
    if gmCommand.isRawPlayer(player):
        toGBID = gmCommand.getGbIdFromRawPlayer(player)
    else:
        toGBID = player.gbID

    toGBID = int(toGBID)
    attach = mailAssistor.parseAttachStr(attachStr)
    title = title.strip("[] ")
    cont = cont.strip("[] ")
    mailAssistor.sendIDIPMailByGBID(su, toGBID, attach, title, cont, AAC_AACDD.datas.BONUS_SRC_GM, 0, ())
    return True, '执行成功'

@gm_cmd('$sendB64MailByGBIDNoMailId', (Player("gbId/Id", raw=True), Str('attachStr'), Str('title'), Str('cont')), RARG(0), BASE,
        '向指定玩家发送一封自定义邮件, base64编码', ALLSIDE, GOD_GROUPS)
def sendB64MailByGBIDNoMailId(su, player, attachStr, b64title, b64cont):
    title = base64.b64decode(b64title.encode('ascii'), b'_-').decode('utf-8')
    cont = base64.b64decode(b64cont.encode('ascii'), b'_-').decode('utf-8')
    DEBUG_MSG('sendMailByGBIDNoMailId:', attachStr, title, cont)
    if gmCommand.isRawPlayer(player):
        toGBID = gmCommand.getGbIdFromRawPlayer(player)
    else:
        toGBID = player.gbID

    toGBID = int(toGBID)
    attach = mailAssistor.parseAttachStr(attachStr)
    title = title.strip("[] ")
    cont = cont.strip("[] ")
    mailAssistor.sendIDIPMailByGBID(su, toGBID, attach, title, cont, AAC_AACDD.datas.BONUS_SRC_GM, 0, ())
    return True, '执行成功'

@gm_cmd('$sendmailByAvatarId', (Str("toId"), Int('mailId'), Str('attachStr'), Str('despArgsStr'), Str('title'), Str('cont')),
        RSU, gameconst.BASE, '向指定玩家发送一封邮件', INSIDE, GOD_GROUPS)
def sendMailByAvatarId(su, toId, mailId, attachStr, despArgsStr, title, cont):
    toId = int(toId)
    attach = mailAssistor.parseAttachStr(attachStr)
    despArgs = mailAssistor.parseDespStr(despArgsStr)
    if toId == 0:
        toId = su.id
    title = title.strip("[] ")
    cont = cont.strip("[] ")
    gameengine.broadcastBaseapp('gmSendMailByEntityId', (toId, mailId, attach, despArgs, title, cont, AAC_AACDD.datas.BONUS_SRC_GM))
    return True, '执行成功'

@gm_cmd('$sendglobalmail', (Int('mailId'), Str('attachStr'), Str('despArgsStr'), Str('title'), Str('cont'),
                            Int('minRoleTime'), Int('maxRoleTime'),Int('minRoleLevel'), Int('maxRoleLevel'), Int('channel')),
        RONE, gameconst.BASE, '发送一封全服邮件', ALLSIDE, GOD_GROUPS)
def gmSendGlobalMail(su, mailId, attachStr, despArgsStr, title, cont, minRoleTime, maxRoleTime, minRoleLevel, maxRoleLevel, channel):
    # attachStr: 多个物品用分号';'分隔; 每个物品有itemId, itemNum，若有绑定属性配置在第三个位置，例如：[30000001,100; 30001031,1,1]
    attach = mailAssistor.parseAttachStr(attachStr)
    despArgs = mailAssistor.parseDespStr(despArgsStr)
    title = base64.b64decode(title.encode('ascii'), b'_-').decode('utf-8')
    cont = base64.b64decode(cont.encode('ascii'), b'_-').decode('utf-8')
    gameengine.getGlobalBase('GlobalMailStub').sendGlobalMail(mailId, attach, despArgs, title, cont, minRoleTime, maxRoleTime, 
                                                              minRoleLevel, maxRoleLevel, channel, AAC_AACDD.datas.BONUS_SRC_GM)
    return True, '执行成功'

@gm_cmd('$getGlobalMailList', (Player("gbId/Id"), Int("mailNum")), RSU, gameconst.BASE, '查看最近mailNum封全服邮件列表', INSIDE, GOD_GROUPS)
def getGlobalMailList(su, player, mailNum):
    gameengine.getGlobalBase('GlobalMailStub').gmGetGlobalMailList(player, player._getChatChannelAvatarInfo(), mailNum)
    return True, '执行成功'

@gm_cmd('$deleteGlobalMail', (Int("mailGBID"), ), RSU, gameconst.BASE, '删除一封全服邮件', INSIDE, GOD_GROUPS)
def delectGlobalMail(su, mailGBID):
    gameengine.getGlobalBase('GlobalMailStub').gmDeleteOneGlobalMail(mailGBID)
    return True, '执行成功'

@gm_cmd('$sendBroadcast', (Int("messageId"), Str("args")), RONE, gameconst.BASE, '发放公告', ALLSIDE, GOD_GROUPS,
        minArgs=1)
def sendBroadcast(su, messageId, args):
    if args:
        gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onMessage', (messageId, args.split(','))))
    else:
        gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onMessage', (messageId, [])))
    return True, '执行成功'


@gm_cmd('$officialMessage', (Int("type"), Str("content"), Int("repeatCount")), RONE, gameconst.BASE, '普通公告',
        ALLSIDE, GOD_GROUPS, minArgs=2)
def officialMessage(su, type, content, repeatCount):
    if not repeatCount:
        repeatCount = 1

    gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onOfficialMessage', (type, content, repeatCount)))
    return True, '执行成功'


@gm_cmd('$officialMessageRegularTime', (
        Int("type"), Str("content"), Int("singleRepeatCount"), Str("startTime"), Int("interval"),
        Int("totalExecuteCount")),
        RONE, gameconst.BASE, '定时公告', ALLSIDE, GOD_GROUPS)
def officialMessageRegularTime(su, type, content, singleRepeatCount, startTime, interval, totalExecuteCount):
    startTimeArgs = startTime.split(':')
    startTimeHour = int(startTimeArgs[0])
    startTimeMinute = int(startTimeArgs[1])
    startTimeTuple = [[[startTimeMinute], [startTimeHour], [], [], [], []]]
    nextStart, _ = utils.nextByTimeTupleList(startTimeTuple)

    gameglobal.localBaseApp.sendOfficialMessage(nextStart, type, content, singleRepeatCount, interval * 60,
                                                totalExecuteCount)
    return True, '执行成功'


@gm_cmd('$onEventTips', (Player("gbId/Id"),), RARG(0), BASE, 'eventTips', ALLSIDE, GOD_GROUPS)
def gmOnEventTips(su, player):
    itemId = 30040001
    wealthVal = dropAward.AwardVal()
    wealthVal.addWealthByItemId(itemId, 1)
    awardCtx = awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID, eventTipId=10000002)
    opUUID = KBEngine.genUUID64()
    srcType = 302
    detail = gameclass.AwardDetail(rankPos=1)
    player.addWealth(srcType, wealthVal, opUUID, detail, awardCtx)


@gm_cmd('$onBroadAllEventTips',
        (Int("itemId"), Int("itemNum"), Int("templateId"), Int("srcType"), Str("avatarName"), Str("serverId")), RALL,
        BASE, '全服eventTips', ALLSIDE, GOD_GROUPS)
def onBroadAllEventTips(su, itemId, itemNum, templateId, srcType, avatarName, serverId):
    if serverId == gameconfig.serverId():
        return

    sendList = list(gameglobal.roleCache.keys())
    for i in sendList:
        entId = sendList.pop()
        ent = KBEngine.entities.get(entId)
        if not ent or not ent.client or ent.isDestroyed:
            continue
        ent.broadCastEventTips(itemId, itemNum, templateId, srcType, avatarName)


@gm_cmd('$stopOfficialMessage', (), RALL, gameconst.BASE, '停止公告', ALLSIDE, GOD_GROUPS)
def stopOfficialMessage(su):
    gameglobal.localBaseApp.stopOfficialMessage()
    return True, '执行成功'


@gm_cmd('$enterline', (Player("gbId/Id"), Int("lineType"),), RARG(0), gameconst.CELL, '进入分线', ALLSIDE, GOD_GROUPS)
def enterLine(su, player, lineType):
    lineNo = formula.getLineNo(player.spaceNo)
    pos, _ = utils.getPlayerBornInfo()
    if formula.getMapId(player.spaceNo) == lineType:
        return False, '执行失败'

    player.applyEnterLineInternal(lineType, lineNo, pos, player.direction, False)
    return True, '执行成功'


@gm_cmd('$leaveline', (Player("gbId/Id"),), RARG(0), gameconst.CELL, '离开分线', ALLSIDE, GOD_GROUPS)
def leaveLine(su, player):
    if formula.spaceInWorldLine(player.spaceNo):
        return False, '不能离开大世界分线'

    lineType = formula.getLineType(player.spaceNo)
    lineNo = random.randint(0, utils.getLineMaxNumber(lineType) - 1)
    pos = formula.whatSpaceBornPoint(formula.getLineSpaceNo(lineType, lineNo))
    if formula.getMapId(player.spaceNo) == lineType:
        return False, '执行失败'

    player.applyEnterLineInternal(lineType, lineNo, pos, player.direction, False)
    return True, '执行成功'


@gm_cmd('$claimtask', (Player("gbId/Id"), Int('taskId'), Int('check')), RARG(0), BASE, '领取任务', ALLSIDE, GOD_GROUPS)
def gmClaimTask(su, player, taskId, check):
    if taskId <= 0:
        return False, '执行失败， 任务id错误'
    import actionContext
    if check:
        player.cell.startClaimTask(taskId, '', (), actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrc.GM))
    else:
        player.baseTaskClaim(taskId, actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrc.GM), needCheck=False)
    return True, '执行成功'


@gm_cmd('$submittask', (Player("gbId/Id"), Int('taskId'),), RARG(0), BASE, '提交任务', ALLSIDE, GOD_GROUPS)
def gmSubmitTask(su, player, taskId):
    if taskId <= 0:
        return False, '执行失败, 任务ID错误'
    player.gmForceSubmitTask(taskId)
    return True, '执行成功'


@gm_cmd('$resetTask', (Player("gbId/Id"), Int('taskId'),), RARG(0), BASE, '重置任务', ALLSIDE, GOD_GROUPS)
def gmResetTask(su, player, taskId):
    if taskId <= 0:
        return False, '执行失败, 任务ID错误'
    player.gmResetTask(taskId)
    return True, '执行成功'


@gm_cmd('$settaskstate', (Player("gbId/Id"), Int('taskId'), Int('state'), Int('childState')), RARG(0), BASE,
        '设置taskId及其子任务的状态', ALLSIDE, GOD_GROUPS, minArgs=3)
def gmSetTaskState(su, player, taskId, state, childState=0):
    if taskId <= 0:
        return False, '执行失败, 任务ID错误'

    if state > gameconst.TaskStat.TASK_STAT_QUIT:
        ERROR_MSG('invalid task state', state)
        return False, '执行失败, 任务state错误'

    player.gmSetTaskState(taskId, state, childState)
    return True, '执行成功'


@gm_cmd('$playcinema', (Player("gbId/Id"), Int('cinemaId'),), RARG(0), CELL, '播放剧情动画', ALLSIDE, GOD_GROUPS)
def gmPlaycinema(su, player, cinemaId):
    player.prepareStartPlayCinema(cinemaId)
    return True, '执行成功'


@gm_cmd('$addAllTitle', (Player("gbId/Id"),), RARG(0), BASE, '激活所有的称号', ALLSIDE, GOD_GROUPS)
def addAllTitle(su, player):
    player.gmAddAllTitle()
    return True, '执行成功'


@gm_cmd('$killent', (Player("gbId/Id"), Int('entity id'),), RARG(0), CELL, 'kill目标', ALLSIDE, GOD_GROUPS, minArgs=1)
def killEnt(su, player, eid=0):
    eid = eid or player.selectedTargetId
    e = KBEngine.entities.get(eid)
    if not e or not e.IsCombatUnit:
        return False, '%s不存在或者不是战斗单位' % eid

    e.modifyHP(-e.hp, player.id, gameconst.SourceType.Skill, 0)
    return True, '执行成功'


@gm_cmd('$destroyent', (Player("gbId/Id"), Int('entity id'),), RARG(0), CELL, '销毁目标', ALLSIDE, GOD_GROUPS,
        minArgs=1)
def destroyEnt(su, player, eid=0):
    eid = eid or player.selectedTargetId
    e = KBEngine.entities.get(eid)
    if not e:
        return False, '%s不存在' % eid

    if e.__class__.__name__ not in ('Space', 'Avatar', 'Account'):
        e.safeDestroy()

    return True, '执行成功'


@gm_cmd('$setcfg', (Str('name'), Str('value')), RONE, BASE, '修改数据库中的游戏开关配置', ALLSIDE, DEV_GROUPS)
def setGameConfig(su, name, value):
    # 这里输入的string 是经过xml转义的 &apos;是' &quot;是"
    if value == '&apos;&apos;' or value == '&quot;&quot;':
        newValue = ''
    else:
        newValue = value

    err, succ = gameconfig.gmSetCutomConfig(name, newValue)
    if succ:
        return True, '执行成功'
    return False, '执行失败：%s' % err


@gm_cmd('$getcfg', (Str('cfgName'),), RONE, BASE, '获取数据库中的游戏开关配置', ALLSIDE, DEV_GROUPS)
def getGameConfig(su, cfgName):
    value = gameconfig.gmGetCutomConfig(cfgName)

    return True, '执行成功：%s' % str(value)


@gm_cmd('$setcachecfg', (Str('name'), Str('value')), RONE, BASE, '修改xml中配置的游戏开关配置', ALLSIDE, DEV_GROUPS)
def setGameCacheConfig(su, name, value):
    # 这里输入的string 是经过xml转义的 &apos;是' &quot;是"
    if value == '&apos;&apos;' or value == '&quot;&quot;':
        newValue = ''
    else:
        newValue = value

    callApps(gameconst.BASE, 'gameconfig.setCacheConfig', (name, newValue))
    callApps(gameconst.CELL, 'gameconfig.setCacheConfig', (name, newValue))
    gameglobal.localBaseApp.notifyInterfaceCacheConfigChanged(name, value)

    return True, '执行成功'


@gm_cmd('$getcachecfg', (Str('cfgName'),), RONE, BASE, '读取xml中配置的游戏开关配置', ALLSIDE, DEV_GROUPS)
def getGameCacheConfig(su, cfgName):
    value = gameconfig.getCacheConfig(cfgName)
    return True, '执行成功：%s' % str(value)


@gm_cmd('$gmCleanAllTasks', (Player("gbId/Id"),), RARG(0), BASE, '清除身上所有任务', ALLSIDE, GOD_GROUPS)
def gmCleanAllTasks(su, player):
    import tutorConst_guideConfig as TCGCD
    player.taskInfo.tasks.clear()
    player.taskInfo.taskRecordDic.clear()
    player.newbieStep = TCGCD.datas['firstStep']['value']
    player.gmFinishedNewbie(0)
    return True, '执行成功'


@gm_cmd('$botFinishNewbie', (Player("gbId/Id"),), RARG(0), BASE, '机器人完成新手', ALLSIDE, GOD_GROUPS)
def botFinishNewbie(su, player):
    player.gmBotFinishedNewbie()
    return True, '执行成功'


@gm_cmd('$findEntity', (Int('entity id'),), RONE, CELL, '实体所在进程', ALLSIDE, GOD_GROUPS)
def findEntity(su, eid):
    forwardCommand(su, '$_findEntity-cell', eid)
    forwardCommand(su, '$_findEntity-base', eid)


@gm_cmd('$_findEntity-cell', (Int('entity id'),), RALL, CELL, '实体所在进程', ALLSIDE, GOD_GROUPS)
def findEntityCell(su, eid):
    import utils
    e = KBEngine.entities.get(eid)
    if not e:
        return

    processIp = utils.getPythonServer()
    return True, 'findEntity-cell执行成功,进程IP：cellapp{:0>2}-{}'.format(KBEngine.getComponentGroupOrder(), processIp)


@gm_cmd('$_findEntity-base', (Int('entity id'),), RALL, BASE, '实体所在进程', ALLSIDE, GOD_GROUPS)
def findEntityBase(su, eid):
    import utils
    e = KBEngine.entities.get(eid)
    if not e:
        return

    processIp = utils.getPythonServer()
    return True, 'findEntity-base执行成功,进程IP：baseapp{:0>2}-{}'.format(KBEngine.getComponentGroupOrder(), processIp)


@gm_cmd('$findStub', (Str('stub name'),), RONE, BASE, 'stub所在进程', ALLSIDE, GOD_GROUPS)
def findStub(su, stubName):
    forwardCommand(su, '$_findStub-base', stubName)


@gm_cmd('$_findStub-base', (Str('stub name'),), RALL, BASE, 'stub所在进程', ALLSIDE, GOD_GROUPS)
def findStubBase(su, stubName):
    import utils

    baseStub = gameengine.getGlobalBase(stubName)

    if isinstance(baseStub, (utils.Swallower,)):
        return
    else:
        e = KBEngine.entities.get(baseStub.id)
        if not e:
            return

        processIp = utils.getPythonServer()
        return True, '执行成功,进程IP：baseapp{:0>2}-{}，stub id ：{}'.format(KBEngine.getComponentGroupOrder(), processIp,
                                                                           baseStub.id)


@gm_cmd('$getlinest', (Int('lineType'),), RONE, BASE, '获取分线状态', ALLSIDE, GOD_GROUPS)
def getlinest(su, lineType):
    forwardCommand(su, '$_getlinest-base', lineType)


@gm_cmd('$_getlinest-base', (Int('lineType'),), RALL, BASE, '获取分线状态', INSIDE, GOD_GROUPS)
def getlinestBase(su, lineType):
    import utils

    line = gameengine.getLineStub(lineType)
    if isinstance(line, (utils.Swallower,)):
        return
    else:
        e = KBEngine.entities.get(line.id)
        if not e:
            return
        else:
            sum = 0
            result = ''
            for key, value in e.allPlayers.items():
                sum += len(value)
                result += ('%s线有%d人，' % (key, len(value)))

            return True, '执行成功,%s共有%d人' % (result, sum)


@gm_cmd('$me', (Player('player id'),), RARG(0), CELL, '获取玩家自己信息', ALLSIDE, GOD_GROUPS)
def me(su, e):
    import utils

    processIp = utils.getPythonServer()
    playerName = e.name
    playerId = e.id
    playerGbId = e.gbId
    playerSchool = e.school
    playerSelectedTargetId = e.selectedTargetId

    return True, '执行成功,name:{},gbId:{},id:{},school:{},selectedTargetId:{},进程IP:cellapp{:0>2}-{} base:{}'.format(
        playerName, playerGbId, playerId, playerSchool, playerSelectedTargetId, KBEngine.getComponentGroupOrder(),
        processIp, e.base)


@gm_cmd('$findavatar', (Player("gbId/Id"),), RARG(0), CELL, '通过玩家名字找到avatar', ALLSIDE, GOD_GROUPS)
def findavatar(su, player):
    import utils

    processIp = utils.getPythonServer()
    playerName = player.name
    playerId = player.id
    playerGbId = player.gbId
    playerSchool = player.school
    playerSpaceNo = player.spaceNo
    playerSelectedTargetId = player.selectedTargetId

    return True, '{}:{}:{},school:{},selectId:{},spaceNo:{},cellapp:{:0>2}-{} base:{}'.format(
        playerName, playerGbId, playerId, playerSchool, playerSelectedTargetId, playerSpaceNo,
        KBEngine.getComponentGroupOrder(), processIp, player.base)


@gm_cmd('$findclient', (Player("gbId/Id"),), RARG(0), BASE, '查看client', ALLSIDE, GOD_GROUPS)
def findClient(su, player):
    return True, 'client:{}'.format(player.client)


@gm_cmd('$getpropCell', (Entity('entity'), Str("propName")), RARG(0), CELL, '输出CELL实体属性值', ALLSIDE, GOD_GROUPS)
def getpropCell(su, ent, propName):
    if not hasattr(ent, propName):
        return

    su.feedbackCommandSucc('执行成功,{}:{}'.format(propName, str(getattr(ent, propName, ''))))


@gm_cmd('$getpropBase', (Entity('entity'), Str("propName")), RARG(0), BASE, '输出BASE实体属性值', ALLSIDE, GOD_GROUPS)
def getpropBase(su, ent, propName):
    if not hasattr(ent, propName):
        return

    su.feedbackCommandSucc('执行成功,{}:{}'.format(propName, str(getattr(ent, propName, ''))))

@gm_cmd('$statAvatarNum', (), RALL, ALL, '统计Avatar数量', ALLSIDE, GOD_GROUPS)
def statAvatarNum(su):
    componentNo = KBEngine.getComponentGroupOrder()
    avatarNumber = len(utils.getEntityList('Avatar'))
    if IS_BASE:
        su.feedbackCommandSucc('执行成功,baseapp{:0>2}:{}'.format(componentNo, avatarNumber))
    else:
        su.feedbackCommandSucc('执行成功,cellapp{:0>2}:{}'.format(componentNo, avatarNumber))
    return


@gm_cmd('$_statAvatarNum-cell', (), RALL, CELL, '统计Avatar数量', ALLSIDE, GOD_GROUPS)
def statAvatarNumCell(su):
    componentNo = KBEngine.getComponentGroupOrder()
    baseAppNum = gameconfig.baseAppCount()
    delayTime = baseAppNum * 5 + componentNo * 2

    def _delayStatAvarNumCell(su):
        avatarNumber = len(utils.getEntityList('Avatar'))
        su.feedbackCommandSucc('执行成功,cellapp{:0>2}:{}'.format(componentNo, avatarNumber))

    KBEngine.addTimer(delayTime, 0, lambda timeId: _delayStatAvarNumCell(su))


@gm_cmd('$_statAvatarNum-base', (), RALL, BASE, '统计Avatar数量', ALLSIDE, GOD_GROUPS)
def statAvatarNumBase(su):
    componentNo = KBEngine.getComponentGroupOrder()
    delayTime = componentNo

    def _delayStatAvarNumBase(su):
        avatarNumber = len(utils.getEntityList('Avatar'))
        su.feedbackCommandSucc('执行成功,baseapp{:0>2}:{}'.format(componentNo, avatarNumber))

    KBEngine.addTimer(delayTime, 0, lambda timerId: _delayStatAvarNumBase(su))


@gm_cmd('$spaceWeightStat', (), RALL, CELL, 'spaceWeight统计', ALLSIDE, GOD_GROUPS)
def spaceWeightStat(su):
    spaceList = utils.getEntityList('Space')
    totalWeight = 0
    spaceDic = {}
    for spaceEntity in spaceList:
        spaceWeight = spaceEntity.getSpaceWeight(spaceEntity.spaceID)
        totalWeight += spaceWeight
        mapId = formula.getMapId(spaceEntity.spaceNo)
        spaceDic.setdefault(mapId, 0)
        spaceDic[mapId] += spaceWeight

    su.feedbackCommandSucc(
        '执行成功,cellapp{:0>2}:{},total:{}'.format(KBEngine.getComponentGroupOrder(), str(spaceDic), totalWeight))


@gm_cmd('$doEval', (Str("componentGroupOrder"), Str("evalStr"),), RONE, BASE, 'eval', ALLSIDE, GOD_GROUPS)
def doEval(su, componentGroupOrder, evalStr):
    forwardCommand(su, '$_doEval-cell', componentGroupOrder, evalStr)
    forwardCommand(su, '$_doEval-base', componentGroupOrder, evalStr)
    return


@gm_cmd('$_doEval-cell', (Str("componentGroupOrder"), Str("evalStr"),), RALL, CELL, 'eval', ALLSIDE, GOD_GROUPS)
def doEvalCell(su, componentGroupOrder, evalStr):
    DEBUG_MSG('cellapp{:0>2}'.format(KBEngine.getComponentGroupOrder()))
    if 'cellapp{:0>2}'.format(KBEngine.getComponentGroupOrder()) == componentGroupOrder:
        result = str(eval(evalStr))
        su.feedbackCommandSucc('执行成功,{}'.format(result))


@gm_cmd('$_doEval-base', (Str("componentGroupOrder"), Str("evalStr"),), RALL, BASE, 'eval', ALLSIDE, GOD_GROUPS)
def doEvalBase(su, componentGroupOrder, evalStr):
    DEBUG_MSG('BASEAPP{:0>2}'.format(KBEngine.getComponentGroupOrder()))
    if 'baseapp{:0>2}'.format(KBEngine.getComponentGroupOrder()) == componentGroupOrder:
        result = str(eval(evalStr))
        su.feedbackCommandSucc('执行成功,{}'.format(result))


@gm_cmd('$switchline', (Player("gbId/Id"), Int('lineNo')), RARG(0), CELL, '切换分线', ALLSIDE, GOD_GROUPS)
def switchline(su, player, lineNo):
    player.applySwitchLine(player.id, lineNo)
    return True, '执行成功'


@gm_cmd('$setgmgroup', (Player("gbId/Id", raw=True), Int('group')), RARG(0), BASE, '设置gm组', ALLSIDE, GOD_GROUPS)
def setgmgroup(su, player, group):
    if gmCommand.isRawPlayer(player):
        sql = "update tbl_Avatar set sm_gmGroup = %d where sm_gbID =%s" % (
            group, gmCommand.getGbIdFromRawPlayer(player))
        KBEngine.executeRawDatabaseCommand(sql)
    else:
        player.gmGroup = group
    return True, '执行成功'


@gm_cmd('$loadentity', (Player('player id'), Str('class name'), Int('object id'), Int('entity id'), Int('num')),
        RARG(0), CELL, '创建entity实体', ALLSIDE, GOD_GROUPS)
def loadentity(su, player, className, objId, entityId, num):
    '''
    className, 对应实体类型 如Npc, Collection, Carrier
    objId, 对应实体类型表中的ID，比如 objId就是对应数据表种中的ID

    '''
    import utils
    import Npc as _Npc
    import Collection as _Collection
    import NPC_teleporter as NPC_T
    import NPC_NPC as NPC_D
    import NPC_Pick as NPC_P
    import creep_base as CB
    import math

    bornPosition = tuple(player.position)
    bornDirection = tuple(player.direction)

    tmpProps = {}
    params = {
        'spaceNo': player.spaceNo,
        'direction': bornDirection,
        'position': bornPosition,
        'spaceno': player.spaceNo,
        'tmpProps': tmpProps,
    }

    flag = ''
    count_ = num if num else 1

    if className in ("Npc",):
        if objId not in NPC_D.datas:
            return False, '执行失败'
        _npcId = objId
        _npcCreepId = NPC_D.datas[int(_npcId)].get('creepID')
        params.update({
            'npcId': _npcId,
            # 'name': _mPrm['Name'],
        })

        for i in utils.generateGameEntityId(entityId, count_):
            params.update({
                'gameEntityId': i,
            })
            gid, gct = utils.splitGameEntityId(i)
            tmpProps['createIndex'] = gct
            player.base.callMethod('gmCreateEntityHasBase', (className, params))

        flag = "执行NPC"
        # ========================

    elif className == "Collection":
        if objId not in NPC_P.datas:
            return False, '执行失败'
        collectionId = objId
        params.update({
            'name': NPC_P.datas.get(objId, {}).get('name'),
            'type': gameconst.CollectionType.NORMAL,
            'collectionId': collectionId,
        })
        for i in utils.generateGameEntityId(entityId, count_):
            params.update({
                'gameEntityId': i,
            })
            gid, gct = utils.splitGameEntityId(i)
            tmpProps['createIndex'] = gct
            # KBEngine.createEntityLocally(className, params)
            player.base.callMethod('gmCreateEntityHasBase', (className, params))

        flag = '执行Collection'

    return True, '执行成功,' + flag


@gm_cmd('$delentity', (Int('entity id'),), RSU, CELL, '删除实体', INSIDE, GOD_GROUPS)
def delentity(su, entityId):
    for e in KBEngine.entities.values():
        if hasattr(e, 'gameEntityId'):
            if entityId == utils.getGidFromGameEntityId(e.gameEntityId):
                e.safeDestroy()

    return True, '执行成功'


@gm_cmd('$loadallentity', (Player('player id'),), RARG(0), CELL, '创建实体', ALLSIDE, GOD_GROUPS)
def loadallentity(su, player):
    import utils
    import Npc as _Npc
    import CNpc as _CNpc
    import Collection as _Collection
    import NPC_NPC as NPC_D
    import creep_base as CB
    import math

    entDatas = utils.getDunModuleData(formula.getMapId(player.spaceNo))

    for entityId, _mPrm in entDatas.items():
        entityId = int(entityId)
        bornPosition = (_mPrm['PosX'], _mPrm['PosY'], _mPrm['PosZ'])
        if 'Dir' in _mPrm:
            bornDirection = (0.0, 0.0, _mPrm['Dir'] * math.pi / 180)
        else:
            bornDirection = (0.0, 0.0, 0.0)

        tmpProps = {}
        params = {
            'spaceNo': player.spaceNo,
            'direction': bornDirection,
            'position': bornPosition,
            'spaceno': player.spaceNo,
            # 'gameEntityId': entityId,
            'tmpProps': tmpProps,
        }

        className = _mPrm['ClassName']
        if className == _Monster.__name__:
            # =====================
            # create Monster Entity
            params.update({
                'monsterId': int(_mPrm['EntityID']),
                # 'name': _mPrm['Name'],
            })
            # radius = 0
            # count = 1

            if 'Props' in _mPrm:
                _pP = _mPrm['Props']

                if 'disappearTimer' in _pP:
                    params['disappearTime'] = _pP['disappearTimer']

                if 'Radius' in _pP:
                    radius = params['bornRadius'] = float(_pP['Radius'])
                    tmpProps['createRadius'] = radius

            count_ = 1
            if formula.spaceInWorldLine(player.spaceNo) and entityId in WMR.datas:
                _pP = WMR.datas[entityId]

                if 'refreshNum' in _pP:
                    count = _pP['refreshNum']
                    tmpProps['createCount'] = count
                    if count > 1000:
                        raise TypeError('Monster count must lower than 1000')

                if 'refreshTime' in _pP:
                    params['refreshTime'] = _pP['refreshTime']

                if 'level' in _pP:
                    params['level'] = _pP['level']

                count_ = _pP.get('refreshNum', 1) or 1

            for i in utils.generateGameEntityId(entityId, count_):
                params.update({
                    'gameEntityId': i,
                })
                gid, gct = utils.splitGameEntityId(i)
                tmpProps['createIndex'] = gct
                # KBEngine.createEntityLocally(className, params)
                player.base.callMethod('gmCreateEntityHasBase', (className, params))

            # =======================


        elif className == _MonsterGrp.__name__:

            # ========================
            # create MonsterGrp Entity

            params.update({
                'groupId': int(_mPrm['EntityID']),
                'groupName': _mPrm.get('DisplayName', '未命名组怪'),
            })

            if 'Props' in _mPrm:
                _pP = _mPrm['Props']
                # if 'spawnSpan' in _pP:
                #     params['spawnSpan'] = _pP['spawnSpan']

                if 'Radius' in _pP:
                    params['bornRadius'] = float(_pP['Radius'])

            count_ = 1

            if formula.spaceInWorldLine(player.spaceNo) and entityId in WMR.datas:

                _pP = WMR.datas[entityId]

                if 'refreshTime' in _pP:
                    params['refreshTime'] = _pP['refreshTime']

                count_ = _pP.get('refreshNum', 1) or 1

            for i in utils.generateGameEntityId(entityId, count_):
                params.update({

                    'gameEntityId': i,

                })

                gid, gct = utils.splitGameEntityId(i)

                tmpProps['createIndex'] = gct

                # en = KBEngine.createEntityLocally(className, params)

                en = player.base.callMethod('gmCreateEntityHasBase', (className, params))

                en.createMonstersFromGrp(params)

            # ========================


        elif className == _Teleporter.__name__:

            # ========================

            # create Teleporter Entity

            teleporterId = _mPrm['EntityID']

            params.update({

                'name': _mPrm['DisplayName'],

                'teleporterId': teleporterId,

            })

            if teleporterId in NPC_T.datas:

                isOpen = NPC_T.datas[teleporterId]['isOpen']

                if isOpen:

                    count_ = 1

                    for i in utils.generateGameEntityId(entityId, count_):
                        params.update({

                            'gameEntityId': i,

                        })

                        gid, gct = utils.splitGameEntityId(i)

                        tmpProps['createIndex'] = gct

                        # KBEngine.createEntityLocally(className, params)

                        player.base.callMethod('gmCreateEntityHasBase', (className, params))

            # ========================

        elif className in (_Npc.__name__,):

            # =================

            # create NPC Entity

            _npcId = _mPrm['EntityID']
            _npcCreepId = NPC_D.datas[int(_npcId)].get('creepID')

            params.update({
                'npcId': _npcId,
                # 'name': _mPrm['Name'],
            })

            if _npcCreepId and _npcCreepId in CB.datas and CB.datas[_npcCreepId]['AI']:
                className = _CNpc.__name__
                _npcAI = NPC_D.datas[int(_npcId)].get('AI')
                if _npcAI:
                    params.update({'aiName': _npcAI})

            count_ = 1

            for i in utils.generateGameEntityId(entityId, count_):
                params.update({
                    'gameEntityId': i,
                })

                gid, gct = utils.splitGameEntityId(i)

                tmpProps['createIndex'] = gct

                # KBEngine.createEntityLocally(className, params)

                player.base.callMethod('gmCreateEntityHasBase', (className, params))

            # ========================


        elif className == _Collection.__name__:
            collectionId = _mPrm['EntityID']
            params.update({
                'name': _mPrm['DisplayName'],
                'type': gameconst.CollectionType.NORMAL,
                'collectionId': collectionId,
            })

            if 'Props' in _mPrm:
                _pP = _mPrm['Props']
                if 'Radius' in _pP:
                    tmpProps['createRadius'] = params['bornRadius'] = float(_pP['Radius'])

            count_ = 1
            if formula.spaceInWorldLine(spaceNo) and collectionId in WMSP.datas:
                _pP = WMSP.datas[collectionId]

                if 'refreshTime' in _pP:
                    params['spawnSpan'] = _pP['refreshTime']
            for i in utils.generateGameEntityId(entityId, count_):
                params.update({
                    'gameEntityId': i,
                })
                gid, gct = utils.splitGameEntityId(i)
                tmpProps['createIndex'] = gct
                # KBEngine.createEntityLocally(className, params)
                player.base.callMethod('gmCreateEntityHasBase', (className, params))

        elif className in ('Barrier', 'AirWall'):

            _barrierId = _mPrm['ID']

            params.update({

                # 'name': _mPrm['Name'],

                'barrierId': _barrierId,

            })

            count_ = 1

            for i in utils.generateGameEntityId(entityId, count_):
                params.update({

                    'gameEntityId': i,

                })

                gid, gct = utils.splitGameEntityId(i)

                tmpProps['createIndex'] = gct

                # KBEngine.createEntityLocally('Barrier', params)

                player.base.callMethod('gmCreateEntityHasBase', ('Barrier', params))

        elif className == 'RebornPos':

            _rebornPosId = _mPrm['EntityID']


            params.update({

                'name': _mPrm['DisplayName'],

                'rebornPosId': _rebornPosId,

            })

            count_ = 1

            for i in utils.generateGameEntityId(entityId, count_):
                params.update({

                    'gameEntityId': i,

                })

                gid, gct = utils.splitGameEntityId(i)

                tmpProps['createIndex'] = gct

                player.base.callMethod('gmCreateEntityHasBase', ('RebornPos', params))

    return True, '执行成功'


@gm_cmd('$modifyServertime', (Str('modifyTime'),), RONE, BASE, '修改服务器时间', ALLSIDE, GOD_GROUPS)
def modifyServertime(su, modifyTime):
    if KBEngine.publish():
        return False, 'modify on dev only'
    if '.' and '-' not in modifyTime:
        return False, '时间格式错误'
    forwardCommand(su, '$modifyServertime-cell', modifyTime)
    forwardCommand(su, '$modifyServertime-base', modifyTime)
    return True, '$modifyServertime执行成功'

@gm_cmd('$modifyAllServertimeInCrossGroup', (Str('modifyTime'),), RONE, BASE, '修改跨服组服务器时间', ALLSIDE, GOD_GROUPS)
def modifyAllServertimeInCrossGroup(su, modifyTime):
    if KBEngine.publish():
        return False, 'modify on dev only'
    DEBUG_MSG("modifyAllServertimeInCrossGroup", modifyTime)
    import iRouter
    _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossServerStub')
    _stub.onGmModifyAllServertimeInCrossGroup(su, modifyTime)
    return True, '$modifyServertime执行成功'


@gm_cmd('$modifyServertime-cell', (Str('modifyTime'),), RALL, CELL, '修改服务器时间', ALLSIDE, GOD_GROUPS)
def modifyServertimeCell(su, modifyTime):
    DEBUG_MSG('modifyServertimeCell')
    import datetime
    import time

    time.time = utils.tempTime

    format = "%Y.%m.%d-%H.%M.%S"
    mtime = datetime.datetime.strptime(modifyTime, format)
    nowDatetime = datetime.datetime.fromtimestamp(time.time())
    timeDelta = (mtime - nowDatetime).total_seconds()
    utils.tempTime = time.time
    time.time = lambda: utils.tempTime() + timeDelta

@gm_cmd('$modifyServertime-base', (Str('modifyTime'),), RALL, BASE, '修改服务器时间', ALLSIDE, GOD_GROUPS)
def modifyServertimeBase(su, modifyTime):
    DEBUG_MSG('modifyServertimeBase')
    import datetime
    import time

    time.time = utils.tempTime

    format = "%Y.%m.%d-%H.%M.%S"
    mtime = datetime.datetime.strptime(modifyTime, format)
    nowDatetime = datetime.datetime.fromtimestamp(time.time())
    timeDelta = (mtime - nowDatetime).total_seconds()
    utils.tempTime = time.time
    time.time = lambda: utils.tempTime() + timeDelta


@gm_cmd('$getServertime', (Player('gbId/Id'),), RARG(0), BASE, '获取服务器时间', ALLSIDE, GOD_GROUPS)
def getServertime(su,player):
    if gmCommand.isRawPlayer(player):
        return False, '执行失败'
    DEBUG_MSG('getServertime')
    import time
    import datetime
    timestamp = time.time()
    dateObject = datetime.datetime.fromtimestamp(timestamp)
    format = "%Y.%m.%d-%H.%M.%S"
    timeStr = dateObject.strftime(format)
    su.onCommandResult(0, timeStr, {})
    return True, '%s' % timeStr


@gm_cmd('$recoverServertime', (), RONE, BASE, '恢复服务器时间', ALLSIDE, GOD_GROUPS)
def recoverServertime(su):
    forwardCommand(su, '$recoverServertime-cell')
    forwardCommand(su, '$recoverServertime-base')
    return True, 'recoverServertime执行成功'


@gm_cmd('$recoverServertime-cell', (), RALL, CELL, '恢复服务器时间', ALLSIDE, GOD_GROUPS)
def recoverServertimeCell(su):
    DEBUG_MSG('recoverServertimeCell')
    import time
    time.time = utils.tempTime


@gm_cmd('$recoverServertime-base', (), RALL, BASE, '恢复服务器时间', ALLSIDE, GOD_GROUPS)
def recoverServertimeBase(su):
    DEBUG_MSG('recoverServertimeBase')
    import time
    time.time = utils.tempTime


@gm_cmd('$onlinenum', (), RSTUB('PlayerStub'), BASE, '获取在线人数', ALLSIDE, GOD_GROUPS)
def getOnlineNum(su, playerStub):
    return True, '%s' % playerStub.getOnlineNum()


@gm_cmd('$showmsg', (Player("gbId/Id"), Int('msgId'), Str('模板参数'), Str('分隔符', default='|')), RARG(0),
        gameconst.BASE, '发送测试消息到客户端', ALLSIDE, DEV_GROUPS, minArgs=2)
def showClientMsg(su, player, msgId, argStr: str, seperator):
    if argStr:
        args = argStr.split(seperator)
    else:
        args = list(['参数%i' % i for i in range(4)])
    print('showClientMsg', msgId, args, player, player.id)
    player.onMessagePre(msgId, args)
    return True, '执行成功'


@gm_cmd('$exportAvatarData', (Player("gbId/Id"), Int('serverId'), Str('playerName')), RARG(0), CELL, '导出数据',
        ALLSIDE, GOD_GROUPS)
def exportAvatarData(su, player, serverId, playerName):
    blacklistPro = ['brothersList', 'coinAuctionInfo', 'friendsInfo', 'marriage', 'moneyAuctionInfo']
    persistProList = KBEngine.getPersistentProperties('Avatar')
    avatarDict = player.__dict__
    postDataDict = {}
    for proKey, avatarPro in avatarDict.items():
        if proKey in persistProList and proKey not in blacklistPro:
            postDataDict[proKey] = avatarPro

    player.base.postAvatarProp(postDataDict, blacklistPro, persistProList, serverId, playerName)

    return True, '执行成功'


@gm_cmd('$importAvatarData', (Player("gbId/Id"), Str("data"),), RARG(0), BASE, '导入数据', ALLSIDE, GOD_GROUPS)
def importAvatarData(su, player, data):
    import pickle
    import functools
    import base64
    import tutorConst_guideConfig as TCGCD

    def _onAvatarSaved(accountEntId, props, homeProp, success, avatar):
        print("_onAvatarSaved", success)
        # 如果此时账号已经销毁， 角色已经无法被记录则我们清除这个角色
        accountEnt = KBEngine.entities.get(accountEntId, None)
        if not accountEnt:
            return

        if accountEnt.isDestroyed:
            if avatar:
                avatar.destroy(True)
            return

        if success:
            accountEnt.characters.addCharacter(avatar.gbID, avatar.databaseID, props["school"], props["name"],
                                               props['sex'], 1, props['birthInDB'])

            if gameconfig.enableCentralLogin():
                createInfo = (
                    accountEnt.accountType, accountEnt.accountName, avatar.gbID, props['name'], 1, props['school'],
                    props['sex'],)
                gameengine.getGlobalBase('LoginStub').notifyCentralServerCreateAvatar(createInfo,
                                                                                      accountEnt.centralServerId)
            accountEnt.client.onCreateAvatarResult(gameconst.CreateAvatarRes.OK, accountEnt.characters[avatar.gbID])

            homeProp.update({'ownerGbId': avatar.gbID})
            home = KBEngine.createEntityLocally('PlayerHome', homeProp)
            home.writeToDB(functools.partial(_onHomeSaved, home.id, homeProp))

            avatar.entireDestroy(False, False)
        else:
            avatar.destroy()

    def _onHomeSaved(homeEntId, homeProp, ok, baseRef):
        print("_onHomeSaved", ok)
        homeEnt = KBEngine.entities.get(homeEntId, None)
        if not homeEnt:
            return

        if not ok:
            print('fail to write db:', homeEnt.ownerGbId, homeEnt.homeNUID)
            return

        addPropDict = {'dbId': baseRef.databaseID,
                       'ownerGbId': homeProp['ownerGbId'],
                       'ownerRole': homeProp['ownerRole'],
                       'homeName': homeProp['homeName'],
                       'homeNUID': homeProp['homeNUID'],
                       'homeType': homeProp['homeType'],
                       'displayInfo': homeProp['displayInfo'], }

        gameengine.getGlobalBase('HomeStub').addHomeCache(addPropDict)

        homeEnt.entireDestroy(False, True)

    temp = base64.b64decode(data)
    props = pickle.loads(temp)
    avatarProp = props.get('avatarData', {})
    homeProp = props.get('homeData', {})

    gbId = utils.generateUniqGlobalId()
    # avatarProp.update({'gbID':gbId,
    #               'name': avatarProp['name']+'B',
    #               'spaceNo': formula.getLineSpaceNo(gameconst.MapIdDef.mapWorldLine,random.choice(range(gameconst.MAX_LINE_CNT))),
    #               'position' : TCGCD.datas['playerBornPosition']['value']
    #               })
    avatarProp.update({'gbID': gbId,
                       'spaceNo': formula.getLineSpaceNo(gameconst.MapIdDef.mapWorldLine, random.choice(
                           range(utils.getLineMaxNumber(gameconst.MapIdDef.mapWorldLine)))),
                       "position": TCGCD.datas['playerBornPosition']['value']})
    avatar = KBEngine.createEntityLocally('Avatar', avatarProp)
    accountEnt = player.accountEntity
    if avatar:
        if avatarProp['name']:
            avatar.writeToDB(functools.partial(_onAvatarSaved, accountEnt.id, avatarProp, homeProp))
        avatar.accountEntity = accountEnt

    return True, '执行成功'


@gm_cmd('$importAvatar', (Int("targetAvatarGbId"), Str("accountName"),), RONE, BASE, '导入角色', ALLSIDE, GOD_GROUPS)
def importAvatar(su, targetAvatarGbId, accountName):
    import const_const

    def _func(result, rows, insertid, error):
        if len(result) == 1 and not result[0][1]:
            characterNum = 0
        elif len(result) > 0:
            characterNum = len(result)
        else:
            su.feedbackCommandFail("账号不存在，执行失败")
            return

        maxChars = const_const.datas.get('createConst_CharLimit', {}).get('value', 3)
        if characterNum >= min(maxChars, 4):
            su.feedbackCommandFail("角色列表已满，执行失败")
            return

        gamesql.updateCharacterParentID(accountName, targetAvatarGbId)
        su.feedbackCommandSucc("执行成功")

    gamesql.countCharacterNum(accountName, _func)


# 测试专用GM 测试后删除
@gm_cmd('$testAccountGM', (PlayerAccount("accountName"),), RONE, BASE, '测试账号GM', ALLSIDE, GOD_GROUPS)
def testAccountGM(su, account):
    DEBUG_MSG("testAccountGM", account)
    return True, '执行成功'


@gm_cmd('$getaccountinfo', (Player("gbId/Id", raw=True),), RARG(0), BASE, '获取角色的账号信息', ALLSIDE, GOD_GROUPS)
def getAccountInfo(su, player):
    if gmCommand.isRawPlayer(player):
        gbId = gmCommand.getGbIdFromRawPlayer(player)
        accSql = 'select ta.sm_accountType from tbl_Account as ta,tbl_Account_characters_characters as tacc where ta.id=tacc.parentID and tacc.sm_gbId=%s' % gbId
        sql = "select accType.sm_accountType, ta.sm_accountName from tbl_Avatar as ta, (%s) as accType where ta.sm_gbID =%s" % (
            accSql, gbId)
        KBEngine.executeRawDatabaseCommand(sql,
                                           lambda ret, num, insertId, err: _onGetAccountInfo(ret, num, insertId, err,
                                                                                             su))
    else:
        return True, "玩家账号类型：%s, 账号名：%s" % (player.accountEntity.accountType, player.accountName)


def _onGetAccountInfo(ret, num, insertId, err, su):
    if err:
        ERROR_MSG('get account info err:', err)
        return

    accoutType, accountName = ret[0]
    accoutType = accoutType.decode('utf-8')
    accountName = accountName.decode('utf-8')
    su.feedbackCommandSucc("玩家账号类型：%s, 账号名：%s" % (accoutType, accountName))


@gm_cmd('$paotu', (Player("gbId/Id"), Int('rideFlag'), Int('pathId')), RARG(0), CELL, '跑图', ALLSIDE, GOD_GROUPS)
def paotu(su, player, rideFlag, pathId):
    import path_path

    if rideFlag:
        player.enterRiding(player.id, False)
    else:
        player.exitRiding(player.id)
    firstPosition = path_path.datas[pathId]['pointList'][0]
    player.position = firstPosition
    player._callback(5, 'setRoute', (pathId,), gametimer.TIMER_TAG_SET_ROUTE)
    return True, '执行成功'


@gm_cmd('$checkRandomName', (), RONE, BASE, '随机姓名检测敏感词', ALLSIDE, GOD_GROUPS)
def checkRandomName(su):
    import randomName_playerName as RNP

    surnameList = RNP.datas.get('surname')
    femaleNameList = RNP.datas.get('femaleName')
    maleNameList = RNP.datas.get('maleName')
    nameList = maleNameList + femaleNameList

    sensitiveWordSet = set()

    ff = open('checkResult.txt', 'a')
    ff.seek(0)
    ff.truncate()

    def func(name, resultFlag, dirtyLevel, resultMsg):
        DEBUG_MSG("####func", name)
        if resultFlag != gameconst.CheckUserInputResult.normal:
            ff.write('%s is sensitive word;result is %s\n' % (name, resultMsg))
            sensitiveWordSet.add(name[resultMsg.find('*'):resultMsg.rfind('*') + 1])

        if name == surnameList[-1] + nameList[-1]:
            ff.close()
            su.feedbackCommandSucc("随机玩家姓名敏感词：{}".format(sensitiveWordSet))

    def checkName():
        for surname in surnameList:
            for name in nameList:
                yield lambda: docheck(surname + name)

    def docheck(name):
        DEBUG_MSG("#####", name)
        utils.miscCheckUserInput(name, functools.partial(func, name))

    gameglobal.localBaseApp.batchlyCall(checkName(), 40, 1)

    return True, '执行成功'


@gm_cmd('$checkRandomBotName', (), RONE, BASE, '随机机器人姓名检测敏感词', ALLSIDE, GOD_GROUPS)
def checkRandomBotName(su):
    import randomName_robotName as RNR

    surnameList = RNR.datas.get('surname')
    femaleNameList = RNR.datas.get('femaleName')
    maleNameList = RNR.datas.get('maleName')
    nameList = maleNameList + femaleNameList

    sensitiveWordSet = set()

    ff = open('checkBotResult.txt', 'a')
    ff.seek(0)
    ff.truncate()

    def func(name, resultFlag, dirtyLevel, resultMsg):
        DEBUG_MSG("####func", name)
        if resultFlag != gameconst.CheckUserInputResult.normal:
            ff.write('%s is sensitive word;result is %s\n' % (name, resultMsg))
            sensitiveWordSet.add(name[resultMsg.find('*'):resultMsg.rfind('*') + 1])

        if name == surnameList[-1] + nameList[-1]:
            ff.close()
            su.feedbackCommandSucc("随机机器人姓名敏感词：{}".format(sensitiveWordSet))

    def checkName():
        for surname in surnameList:
            for name in nameList:
                yield lambda: docheck(surname + name)

    def docheck(name):
        DEBUG_MSG("#####", name)
        utils.miscCheckUserInput(name, functools.partial(func, name))

    gameglobal.localBaseApp.batchlyCall(checkName(), 800, 1)

    return True, '执行成功'


@gm_cmd('$checkItemName', (), RONE, BASE, '道具名称检测敏感词', ALLSIDE, GOD_GROUPS)
def checkItemName(su):
    import itemData_itemData as IDIDD

    itemKeyList = IDIDD.datas.keys()
    sensitiveWordSet = set()
    checkNum = 0

    ff = open('checkResult.txt', 'a')
    ff.seek(0)
    ff.truncate()

    def func(name, resultFlag, dirtyLevel, resultMsg):
        DEBUG_MSG("####func", name)
        nonlocal checkNum
        if resultFlag != gameconst.CheckUserInputResult.normal:
            ff.write('%s is sensitive word;result is %s\n' % (name, resultMsg))
            sensitiveWordSet.add(name[resultMsg.find('*'):resultMsg.rfind('*') + 1])

        checkNum += 1
        if checkNum == len(IDIDD.datas):
            ff.close()
            su.feedbackCommandSucc("道具名称敏感词：{}".format(sensitiveWordSet))

    def checkName():
        for itemId in itemKeyList:
            yield lambda: docheck(IDIDD.datas[itemId]['name'])

    def docheck(name):
        DEBUG_MSG("#####", name)
        utils.miscCheckUserInput(name, functools.partial(func, name))

    gameglobal.localBaseApp.batchlyCall(checkName(), 40, 1)

    return True, '执行成功'


@gm_cmd('$checkRandomNameZk', (), RONE, BASE, '随机姓名检测字库', ALLSIDE, GOD_GROUPS)
def checkRandomNameZk(su):
    import randomName_playerName as RNP
    import validate_chars

    surnameList = RNP.datas.get('surname')
    femaleNameList = RNP.datas.get('femaleName')
    maleNameList = RNP.datas.get('maleName')
    nameList = maleNameList + femaleNameList

    ilegalList = []
    charSet = set()

    for surname in surnameList:
        for name in nameList:
            nameSet = set(surname + name)
            charSet = charSet | nameSet

    for char in charSet:
        if not validate_chars.RE_VALIDATE_SPECIAL_COMPILE.fullmatch(char):
            ilegalList.append(char)

    su.feedbackCommandSucc("随机玩家非法字库列表：{}".format(ilegalList))

    return True, '执行成功'


@gm_cmd('$checkRandomBotNameZk', (), RONE, BASE, '随机机器人姓名检测字库', ALLSIDE, GOD_GROUPS)
def checkRandomBotNameZk(su):
    import randomName_robotName as RNR
    import validate_chars

    surnameList = RNR.datas.get('surname')
    femaleNameList = RNR.datas.get('femaleName')
    maleNameList = RNR.datas.get('maleName')
    nameList = maleNameList + femaleNameList

    ilegalList = []
    charSet = set()

    for surname in surnameList:
        for name in nameList:
            nameSet = set(surname + name)
            charSet = charSet | nameSet

    for char in charSet:
        if not validate_chars.RE_VALIDATE_SPECIAL_COMPILE.fullmatch(char):
            ilegalList.append(char)

    su.feedbackCommandSucc("随机机器人非法字库列表：{}".format(ilegalList))

    return True, '执行成功'


@gm_cmd('$gmBlockExposedMethod', (Int('isAdd'), Str('funcName'), Int('msgId')), RONE, BASE, '禁止对外接口', ALLSIDE,
        GOD_GROUPS)
def gmBlockExposedMethod(su, isAdd, method, msgId):
    gameengine.callAllApps('gameengine.modifyGlobalExposedFunc', (isAdd, method, msgId))
    return True, '执行成功'


@gm_cmd('$gmAutoRunTask', (Player("gbId/Id"), Int('taskId')), RARG(0), BASE, '自动进行任务', ALLSIDE, GOD_GROUPS)
def gmAutoRunTask(su, player, taskId):
    player.gmAutoRunTask(taskId)
    return True, '执行成功'

@gm_cmd('$getItemUniqueId', (Player("gbId/Id"), Int('itemId'),), RONE, BASE, 'get item uniqueId', ALLSIDE, GOD_GROUPS)
def getItemUniqueId(su, player, itemId):
    uId = player.getItemUniqueId(itemId)
    return True, '' + str(uId)


@gm_cmd('$gmSignIn', (Player("gbId/Id"), Int('activityId'),), RONE, BASE, 'sign in', ALLSIDE, GOD_GROUPS)
def gmSignIn(su, player, aId):
    player.reqSignInfo(aId)
    player.reqSignIn(aId)
    return True, '执行成功'


@gm_cmd('$offline', (Player("entity id"),), RARG(0), CELL, 'offline', ALLSIDE, GOD_GROUPS)
def gmOffline(su, player):
    player.offline(player.id, gameconst.AVATAR_OFFLINE_REASON_MANNUALLY)
    return True, '执行成功'


@gm_cmd('$modifyName', (Player("gbId/Id", raw=True), Str('newName')), RARG(0), BASE, '改名', ALLSIDE, GOD_GROUPS)
def modifyName(su, player, newName):
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        gamesql.recordAvatarOfflineCallback(gbId, 'IDIPModifyName', (newName,))
    else:
        player.IDIPModifyName(newName)
    return True, '执行成功'

@gm_cmd('$modifyscore', (Player("gbId/Id", raw=True), Int('newScore')), RARG(0), CELL, '修改战力', ALLSIDE, GOD_GROUPS)
def modifyscore(su, player, newScore):
    player._changeScore("rewardFightProp", newScore)
    return True, '执行成功'



@gm_cmd('$modifyNameByItem', (Player("entity id"), Str('newName'), Int("gridId")), RARG(0), CELL, '道具改名', ALLSIDE,
        GOD_GROUPS)
def modifyNameByItem(su, player, newName, gridId):
    itemId = 30010100
    player.reqUseItems(player.id, 0, gridId, itemId, None, 1, [newName, ])
    return True, '执行成功'


@gm_cmd('$testPickupExtractItem',
        (Player("gbId/Id", raw=True), Int('boxId'), Int('boxNum'), Int('tarNum'), Int('fillId')), RARG(0), BASE,
        '拆解奖励接口测试', ALLSIDE, GOD_GROUPS)
def testPickupExtractItem(su, player, boxId, boxNum, tarNum, fillId):
    DEBUG_MSG('GM testPickupExtractItem~')
    itemGroup = player.pickExtractItems(boxId, boxNum, tarNum, fillId, dataUtils.getItemDefaultBindType())
    return True, '执行成功_%s' % str(itemGroup)


@gm_cmd('$deleteAvatar', (Player("gbId"),), RARG(0), BASE, 'set did limit', ALLSIDE, GOD_GROUPS)
def deleteAvatar(su, player):
    player.reqDeleteAvatar()




@gm_cmd('$addPlayerCalendarPoint', (Player("gbId"), Int('point'),), RARG(0), BASE, 'add player calendar point', ALLSIDE,
        GOD_GROUPS)
def addPlayerCalendarPoint(su, player, point):
    player.calendarPoint += point
    return True, '执行成功'


@gm_cmd('$setforbiddenflag', (Player("gbId/Id", raw=True), Int('flagType'), Int('forbiddenTime'), Str('reason')),
        RARG(0), BASE, '封禁指定功能', ALLSIDE, GOD_GROUPS)
def setForbiddenFlag(su, player, forbiddenType, forbidTime, reason):
    tEnd = utils.getNow() + forbidTime
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        gamesql.recordAvatarOfflineCallback(gbId, 'setForbiddenFlag', (forbiddenType, (tEnd, reason)))
    else:
        player.setForbiddenFlag(forbiddenType, (tEnd, reason))

    su.onCommandResult(0, '', {})
    return True, '执行成功'


@gm_cmd('$addWPWhiteList', (Player("gbId/Id", raw=True),), RARG(0), BASE, '添加白名单', ALLSIDE, GOD_GROUPS)
def addWPWhiteList(su, player):
    if not gmCommand.isRawPlayer(player):
        playerGbId = player.gbID
        isOffline = False
    else:
        playerGbId, *_ = player
        isOffline = True

    def _onAdd(success, value):
        if success:
            su.onCommandResult(0, '', {})
        else:
            valueStr = ','.join(value)
            su.onCommandResult(gameconst.GMCommandErr.REDIS_OP_ERR, '', {"values": valueStr})

    def _onOfflineSetWpList(ret, num, insertId, err):
        if not err:
            gbIds = [playerGbId, ]
            redisUtils.SetUtils.sadd(gameconst.RedisKey.WP_WHITE_LSIT_KEY, gbIds, _onAdd)
        else:
            INFO_MSG("_onOfflineSetWpList failed", ret, num, err, playerGbId)
            su.onCommandResult(gameconst.GMCommandErr.DB_OP_ERR, '', {})

    if isOffline:
        sql = f'update tbl_Avatar set sm_isWpWhiteList=1 where sm_gbID={playerGbId}'
        KBEngine.executeRawDatabaseCommand(sql,
                                           lambda ret, num, insertId, err: _onOfflineSetWpList(ret, num, insertId, err))
    else:
        player.isWpWhiteList = 1
        gbIds = [playerGbId, ]
        redisUtils.SetUtils.sadd(gameconst.RedisKey.WP_WHITE_LSIT_KEY, gbIds, _onAdd)


@gm_cmd('$remWPWhiteList', (Player("gbId/Id", raw=True),), RARG(0), BASE, '删除白名单', ALLSIDE, GOD_GROUPS)
def remWPWhiteList(su, player):
    if not gmCommand.isRawPlayer(player):
        playerGbId = player.gbID
        isOffline = False
    else:
        playerGbId, *_ = player
        isOffline = True

    def _onDel(success, value):
        if success:
            su.onCommandResult(0, '', {})
        else:
            su.onCommandResult(gameconst.GMCommandErr.REDIS_OP_ERR, '', {"values": str(value)})

    def _onOfflineDelWpList(ret, num, insertId, err):
        INFO_MSG('_onOfflineDelWpList', ret, num, err)
        if not err:
            redisUtils.SetUtils.srem(gameconst.RedisKey.WP_WHITE_LSIT_KEY, playerGbId, _onDel)
        else:
            INFO_MSG("_onOfflineDelWpList failed", ret, num, err, playerGbId)
            su.onCommandResult(gameconst.GMCommandErr.DB_OP_ERR, '', {})

    if isOffline:
        sql = f'update tbl_Avatar set sm_isWpWhiteList=0 where sm_gbID={playerGbId}'
        INFO_MSG('_onOfflineDelWpList', sql)
        KBEngine.executeRawDatabaseCommand(sql,
                                           lambda ret, num, insertId, err: _onOfflineDelWpList(ret, num, insertId, err))
    else:
        player.isWpWhiteList = 0
        redisUtils.SetUtils.srem(gameconst.RedisKey.WP_WHITE_LSIT_KEY, playerGbId, _onDel)


@gm_cmd('$queryWPWhiteList', (), RONE, BASE, '查询白名单', ALLSIDE, GOD_GROUPS)
def queryWPWhiteList(su):
    def _onLoadAll(success, values):
        if success:
            valuesStr = ','.join(values)
            su.onCommandResult(0, '', {"values": valuesStr})
        else:
            su.onCommandResult(gameconst.GMCommandErr.REDIS_OP_ERR, '', {})

    redisUtils.SetUtils.loadAllFromRedis(gameconst.RedisKey.WP_WHITE_LSIT_KEY, _onLoadAll)


@gm_cmd('$setChatForbidden', (Player("gbId/Id", raw=True), Int("seconds"),), RARG(0), BASE, '设置聊天禁止', ALLSIDE,
        GOD_GROUPS)
def setChatForbidden(su, player, seconds):
    # 离线玩家处理
    _args = (gameconst.IDIPBanType.CHAT, utils.getNow() + seconds)
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        INFO_MSG(f"gm offline setChatForbidden, gbID:{gbId}")
        gamesql.recordAvatarOfflineCallback(gbId, 'IDIPBanState', _args)
        su.onCommandResult(gameconst.ChatSysGMErr.OK, '', {'gbId': gbId, 'isOffline': True})
    # 在线玩家处理
    else:
        INFO_MSG(f"gm online setChatForbidden, gbID:{player.gbID}")
        if not player.IDIPBanState(*_args):
            su.onCommandResult(gameconst.ChatSysGMErr.FAIL, '', {'gbId': player.gbID, 'isOffline': False})
            return False, '执行失败'
        su.onCommandResult(gameconst.ChatSysGMErr.OK, '', {'gbId': player.gbID, 'isOffline': False})
    return True, '执行成功'


@gm_cmd('$removeChatForbidden', (Player("gbId/Id", raw=True),), RARG(0), BASE, '移除聊天禁止', ALLSIDE, GOD_GROUPS)
def removeChatForbidden(su, player):
    # 离线玩家处理
    _args = (gameconst.IDIPBanType.CHAT,)
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        INFO_MSG(f"gm offline removeChatForbidden, gbID:{gbId}")
        gamesql.recordAvatarOfflineCallback(gbId, 'IDIPRemoveBanState', _args)
        su.onCommandResult(gameconst.ChatSysGMErr.OK, '', {'gbId': gbId, 'isOffline': True})
    # 在线玩家处理
    else:
        INFO_MSG(f"gm online removeChatForbidden, gbID:{player.gbID}")
        if not player.IDIPRemoveBanState(*_args):
            su.onCommandResult(gameconst.ChatSysGMErr.FAIL, '', {'gbId': player.gbID, 'isOffline': False})
            return False, '执行失败'
        su.onCommandResult(gameconst.ChatSysGMErr.OK, '', {'gbId': player.gbID, 'isOffline': False})
    return True, '执行成功'


@gm_cmd('$queryChatForbidden', (Player("gbId/Id", raw=True),), RARG(0), BASE, '查询聊天禁止', ALLSIDE, GOD_GROUPS)
def queryChatForbidden(su, player):
    # 离线玩家处理
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        INFO_MSG(f"gm offline queryChatForbidden, gbID:{gbId}")

        def onGetForbiddenInfo(ret, num, insertId, err, su, gbId):
            if err:
                su.onCommandResult(gameconst.ChatSysGMErr.DBERR, '',
                                   {'gbId': gbId, 'isOffline': True, 'forbiddenExpireTime': 0, 'forbiddenCount': 0})
                ERROR_MSG("gm offline queryChatForbidden fail, ", gbId, num, insertId, err)
            else:
                forbiddenExpireTime = int(ret[0][0].decode())
                forbiddenCount = int(ret[0][1].decode())
                su.onCommandResult(gameconst.ChatSysGMErr.OK, '',
                                   {'gbId': gbId, 'isOffline': True, 'forbiddenExpireTime': forbiddenExpireTime,
                                    'forbiddenCount': forbiddenCount})
                INFO_MSG("gm offline queryChatForbidden success, ", gbId, num, insertId, err)

        gamesql.queryForbiddenInfo(player[0],
                                   lambda ret, num, insert, err: onGetForbiddenInfo(ret, num, insert, err, su, gbId))

    # 在线玩家处理
    else:
        INFO_MSG(f"gm online queryChatForbidden, gbID:{player.gbID}")
        forbiddenExpireTime, forbiddenCount = player.getChatForbiddenInfo()
        su.onCommandResult(gameconst.ChatSysGMErr.OK, '',
                           {'gbId': player.gbID, 'isOffline': False, 'forbiddenExpireTime': forbiddenExpireTime,
                            'forbiddenCount': forbiddenCount})
    return True, '执行成功'

@gm_cmd('$addBuff', (Entity('entity id'), Int('buffId'), Int('lv')), RARG(0), CELL, '给实体加buff', ALLSIDE, GOD_GROUPS)
def addBuff(su, e, buffId, buffLv):
    if buffId in BBD.datas and e.IsCombatUnit:
        e.addBuff(buffId, buffLv, e.id)
        return True, '执行成功'
    else:
        return False, '执行失败'

@gm_cmd('$setlv', (Player("gbId/Id"), Int("lv"),), RARG(0), gameconst.CELL, '设置人物等级', ALLSIDE, GOD_GROUPS)
def setPlayerlv(su, player, lv):
    if lv < player.level:
        return False, '等级不能降低'
    opUUID = KBEngine.genUUID64()
    src = AAC_AACDD.datas.BONUS_SRC_GM
    detail = gameclass.AwardDetail(gm_cmd='$setlv', level=lv)
    import utils
    player.levelUp(min(utils.getPlayerMaxLevel(), lv), opUUID, src, detail)
    return True, '执行成功'

@gm_cmd('$clearCD', (Player("gbId/Id"),), RARG(0), CELL, '清除技能CD', ALLSIDE, GOD_GROUPS)
def clearCD(su, player ):
    if not player.skillDic:
        return False, '执行失败，没有装备任何技能'

    for skill in player.skillDic.values():
        skill.clearCD(player)
    return True, '执行成功'

@gm_cmd('$getAllSkills', (Player("gbId/Id"),), RARG(0), CELL, '获得所有技能', ALLSIDE, GOD_GROUPS)
def getAllSkills(su, player ):
    if not player.skillDic:
        return False, '执行失败，没有装备任何技能'

    for skillID, skillData in player.skillDic.items():
        INFO_MSG('getAllSkills:', skillID, skillData)
    INFO_MSG('getAllSkills:', player.skillDic.skillSwitches)
    return True, '执行成功'

@gm_cmd('$destroyEntity', (Entity('entity id'), ), RARG(0), CELL, '销毁实体', INSIDE, GOD_GROUPS)
def destroyEntity(su, e):
    if e:
        e.safeDestroy()
        return True, '执行成功'
    else:
        return False, '执行失败'


@gm_cmd('$switchServer', (Player("gbId"), Int('serverId')), RARG(0), BASE, '转服', ALLSIDE, GOD_GROUPS)
def switchServer(su, player, serverId):
    player.switchAvatarServer(serverId)
    return True, '执行成功'


@gm_cmd('$enterMap', (Player("gbId/Id"), Int("mapId")), RARG(0), CELL, '进入地图', ALLSIDE, GOD_GROUPS)
def enterMap(su, player, mapId):

    player.applyEnterLine(player.id, mapId)
    return True, '执行成功'

@gm_cmd('$EnterWonderLand', (Player("gbId/Id"), Int("mapId")), RARG(0), BASE, '进入秘境峰', ALLSIDE, GOD_GROUPS)
def EnterWonderLand(su, player, mapId):
    gameengine.getWonderLandStub(mapId).doEnterWonderLand(player, player.gbID)
    return True, '执行成功'

@gm_cmd('$enterCube', (Player("gbId/Id"), Int("floor")), RARG(0), CELL, '进入魔方阵', ALLSIDE, GOD_GROUPS)
def enterCube(su, player, floor):
    player.enterCubeInternal(floor)
    return True, '执行成功'

@gm_cmd('$enterYanwu', (Player("gbId/Id"), Int("mapId")), RARG(0), CELL, '进入演武场', ALLSIDE, GOD_GROUPS)
def enterYanwu(su, player, mapId):
    player.enterLineByNpc(mapId)
    return True, '执行成功'

@gm_cmd('$leaveSingleDungeon', (Player("gbId/Id"),), RARG(0), CELL, '离开当前副本', ALLSIDE, GOD_GROUPS)
def leaveSingleDungeon(su, player):
    import gamePlay_gamePlay as GGD
    import dungeonSrc
    import tutorConst_newbieStep as TCNSD
    lockdun = []
    for _,v in TCNSD.datas.items():
        lockdun.append(v.get('lockDun'))
    dungeonNo = formula.getDungeonNoBySpaceNo(player.spaceNo)

    if  GGD.datas[dungeonNo].get('sceneType') not in [1,2]:
        return False,f'{dungeonNo}不是副本'

    if dungeonNo in lockdun:     #如果是新手副本，先跳过新手任务，在离开副本。
        forwardCommand(su,"$SkipNewbieTask",player.id)

    src = dungeonSrc.DungeonFromClientSrc(player.base, player.gbId)
    player.doLeaveSingleDungeon(dungeonNo, src, 'client leave')
    return True, '执行成功'

@gm_cmd('$SkipNewbieTask', (Player("gbId/Id"),), RARG(0), BASE, '跳过新手任务', ALLSIDE, GOD_GROUPS)
def SkipNewbieTask(su, player):
    import tutorConst_newbieStep as TCNSD
    stepLimit = max(TCNSD.datas.keys())
    for step, data in TCNSD.datas.items():
        if player.newbieStep <= step < stepLimit:
            taskId = data['taskTag']
            if taskId:
                for subTaskId in player.taskInfo.getChildTaskIds(taskId):
                    player.taskInfo.tasks.pop(subTaskId, None)
                player.gmForceSubmitTask(taskId)
                player.taskInfo.tasks.pop(taskId, None)
                player.taskInfo.taskRecordDic[taskId] = gameconst.TaskStat.TASK_STAT_SUBMITTED
            player.newbieStep = max(TCNSD.datas.keys())
    return True, '执行成功'


@gm_cmd('$AllPlayerEnterMap', (Player("gbId/Id"), Int("mapId"), Int("floor")), RARG(0), gameconst.CELL, '所有人进入指定地图', ALLSIDE, GOD_GROUPS,minArgs=2)
def AllPlayerEnterMap(su,player,mapId,floor=1):
    import gamePlay_gamePlay as GGD
    mapInfo = GGD.datas[mapId]
    sceneType = mapInfo.get('sceneType')
    type = mapInfo.get('type')
    if not sceneType or not type:
        return False, f'地图 {mapId} 配置错误：缺少sceneType或type字段'

    if (sceneType == 4 or sceneType == 7) and type == 6:  #大世界场景
        for e in KBEngine.entities.values():
            if e.className == 'Avatar':
                forwardCommand(su,"$enterMap",e.id,mapId)
    elif (sceneType == 1 or sceneType == 2) and (type == 1 or type == 2): #副本场景
        for e in KBEngine.entities.values():
            if e.className == 'Avatar':
                forwardCommand(su,"$gmenterDungeon",e.id,mapId)
    elif sceneType == 3 and type == 3:
        for e in KBEngine.entities.values():
            if e.className == 'Avatar':
                forwardCommand(su,"$enterCube",e.id,floor)
    elif sceneType == 5 and type == 7:
        for e in KBEngine.entities.values():
            if e.className == 'Avatar':
                forwardCommand(su,"$EnterWonderLand",e.id,mapId)
    elif sceneType == 6 and type == 8:
        for e in KBEngine.entities.values():
            if e.className == 'Avatar':
                forwardCommand(su,"$enterCityBattle",e.id)
    elif sceneType == 7 and type == 6:
        for e in KBEngine.entities.values():
            if e.className == 'Avatar':
                e.enterLineByNpc(mapId)
    #gameengine.getWonderLandStub(mapId).doEnterWonderLand(player, player.gbID)
    return True, '执行成功'


@gm_cmd('$finishNewbie', (Player("gbId/Id"), Int('step')), RARG(0), BASE, '完成新手', ALLSIDE, GOD_GROUPS)
def finishNewbie(su,player, step):
    # if not player.newbieStep :
    #     return False, '已跳过新手'
    player.gmFinishedNewbie(step)
    return True, '执行成功'

@gm_cmd('$ALLfinishNewbie', (Player("gbId/Id"), Int('step')), RARG(0), BASE, '所有人完成新手', ALLSIDE, GOD_GROUPS)
def ALLfinishNewbie(su,player, step):
    for e in KBEngine.entities.values():
        if e.className == 'Avatar':
            e.gmFinishedNewbie(step)
    return True, '执行成功'


@gm_cmd('$createDuelFlag', (Player("gbId/Id"),), RARG(0), CELL, '创建决斗旗子', ALLSIDE, GOD_GROUPS)
def createDuelFlag(su, player):
    params = {
        'position': player.position,
        'direction': player.direction,
        'avatarInDuelDatas': [],
        'spaceNo': player.spaceNo,
    }

    KBEngine.createEntity('DuelFlag', player.spaceID, player.position, player.direction, params)
    return True, '执行成功'



@gm_cmd('$finishAchievement', (Player("gbId/Id"), Int('AchievementID')), RARG(0), BASE, '完成指定成就', ALLSIDE, GOD_GROUPS)
def finishAchievement(su,player, AchievementID):
    if AchievementID in player.achievementInfo.finishedIds:
            WARNING_MSG('AchievementID already exists', AchievementID)
    else:
        player.achievementInfo.finishedIds.add(AchievementID)
    player.achievementInfo.sendInitDataToClient(player)
    return True, '执行成功'

@gm_cmd('$AddGuildExp', (Player("gbId/Id"), Int('GuildExp')), RARG(0), BASE, '增加当前帮会经验', ALLSIDE, GOD_GROUPS)
def addguildexp(su, player,exp):
    opUUID = KBEngine.genUUID64()
    src = AAC_AACDD.datas.BONUS_SRC_GM
    detail = gameclass.AwardDetail(gm_cmd='$SetGuildLevel', exp=exp)
    if exp < 1:
        return False, '执行失败，经验不能小于1'
    elif player.guildBox is None:
        return False, '当前玩家没有帮会'
    player.guildBox.addGuildExp(exp, src, opUUID, detail)
    player._sendGuildInfo()
    return True, '执行成功'

@gm_cmd('$modifyBuildingExp', (Player("gbId/Id"),Int('building'),Int('Exp')), RARG(0), BASE, '增加帮会建筑经验', ALLSIDE, GOD_GROUPS)
def modifybuildingexp(su, player,building,exp):
    if building not in (gameconst.GuildBuilding.JU_YING,gameconst.GuildBuilding.WU_HUA,gameconst.GuildBuilding.XIANG_FANG,gameconst.GuildBuilding.YAN_WU,gameconst.GuildBuilding.CANG_KU, gameconst.GuildBuilding.JUN_XU):
        return False, '执行失败，帮会建筑不存在'
    opUUID = KBEngine.genUUID64()
    src = AAC_AACDD.datas.BONUS_SRC_GM
    detail = gameclass.AwardDetail(gm_cmd='$modifyBuildingExp', building=building,exp=exp)
    if exp < 1:
        return False, '执行失败，经验不能小于1'
    elif player.guildBox is None:
        return False, '当前玩家没有帮会'
    player.guildBox.modifyBuildingExp(building,exp,src,opUUID,detail)
    player._sendGuildInfo()
    return True, '执行成功'

@gm_cmd('$welfareSignInDay', (Player("gbId/Id"), Int("flag"), Str('welfareType')), RARG(0), gameconst.BASE, '福利签到天数累计', ALLSIDE, GOD_GROUPS)
def welfareSignInDay(su, player, flag, welfareType):
    flag %= 2
    return player.gmUpdateWelfareSignIn(flag, welfareType)

@gm_cmd('$enterCityBattle', (Player("gbId/Id"),), RARG(0), gameconst.BASE, '进城战场景', ALLSIDE, GOD_GROUPS)
def enterCityBattle(su, player):
    return player.cell.gmEnterSiegeWarSpace()

@gm_cmd('$fastBidding', (Player("gbId/Id"), Int('cnt')), RARG(0), gameconst.BASE, '快速报名+竞拍', ALLSIDE, GOD_GROUPS)
def fastBidding(su, player, cnt):
    player.gmFastBidding(cnt)
    return True, '执行成功'

@gm_cmd('$clearCityRecentRecord', (Player("gbId/Id"),), RARG(0), gameconst.BASE, '清空城池操作记录', ALLSIDE, GOD_GROUPS)
def clearCityRecentRecord(su, player):
    _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
    _stub.clearCityRecentRecord()

@gm_cmd('$addCityMoney', (Player("gbId/Id"), Int('money')), RARG(0), gameconst.BASE, '城池加钱', ALLSIDE, GOD_GROUPS)
def addCityMoney(su, player, money):
    _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
    _stub.gmAddCityMoney(money)
    return True, '执行成功'

@gm_cmd('$clearCityOwner', (Player("gbId/Id"),), RARG(0), gameconst.BASE, '清空城池归属', ALLSIDE, GOD_GROUPS)
def clearCityOwner(su, player):
    _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
    _stub.gmClearCityOwner()
    return True, '执行成功'

@gm_cmd('$RemoveCityOwnerFlag', (Player("gbId/Id"),), RARG(0), gameconst.BASE, '移除帮会标记', ALLSIDE, GOD_GROUPS)
def RemoveCityOwnerFlag(su, player):
    player.guildBox.onChangeCityOwnerFlag(False)
    return True, '执行成功'

@gm_cmd('$changeSiegeWarState', (Player("gbId/Id"), Int('state'), Int('endTime')), RARG(0), gameconst.BASE, '修改城战状态', ALLSIDE, GOD_GROUPS)
def gmChangeSiegeWarState(su, player, state, endTime):
    _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
    _stub.gmChangeSiegeWarState(state, endTime, 0)
    return True, '执行成功'

@gm_cmd('$changeSiegeWarStateOfficial', (Player("gbId/Id"), Int('state'), Int('endTime')), RARG(0), gameconst.BASE, '修改城战状态(线上用)', ALLSIDE, GOD_GROUPS)
def gmChangeSiegeWarStateOfficial(su, player, state, endTime):
    _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
    _stub.gmChangeSiegeWarState(state, endTime, (0, 1))
    return True, '执行成功'

@gm_cmd('$siegeWarBattleFastForward', (Player("gbId/Id"), Int('minutes')), RARG(0), gameconst.BASE, '城战战斗快进', ALLSIDE, GOD_GROUPS)
def gmSiegeWarBattleFastForward(su, player, minutes):
    gameengine.getGlobalBase("SiegeWarSpaceStub").onGmAddTime(minutes)
    player.sendWorldChatMsg(player, "城战战斗快进"+str(minutes)+"分钟")

    _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
    _stub.gmChangeSiegeWarState(4, 0, minutes)
    return True, '执行成功'

@gm_cmd('$siegeWarTestScores', (Player("gbId/Id"),), RARG(0), gameconst.BASE, '城战测试分数', ALLSIDE, GOD_GROUPS)
def siegeWarTestScores(su, player):
    gameengine.getGlobalBase("SiegeWarSpaceStub").onGmTestScores()
    return True, '执行成功'

@gm_cmd('$resetMailStubTime', (Player("gbId/Id"),), RARG(0), gameconst.BASE, '改数据库重置邮件lasttime', ALLSIDE, GOD_GROUPS)
def resetMailStubTime(su, player):
    now = utils.getNow()
    sql = "UPDATE tbl_GlobalMailStub SET sm_lastSendTime = %s WHERE id = 1;" % (now)
    KBEngine.executeRawDatabaseCommand(sql)
    player.sendWorldChatMsg(player, "邮件数据库lasttime已重置:"+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)))+"重启服务器生效")
    return True, '执行成功'

@gm_cmd('$createCreationByFixedPosition', (Player("gbId/Id"), Int('creationId'), Int('x'),Int('y'),Int('z')), RARG(0), CELL, '创建固定位置的创建物', ALLSIDE, GOD_GROUPS)
def createCreationByFixedPosition(su, player, creationId, x,y,z):
    context = actionContext.ActionContext()
    context.actionType = actionContext.ACTION_USE_SKILL
    context.skillId = 0
    positionList = [player.position]
    positionList.append(Math.Vector3(x,y,z))
    player.createCreationByFixedPos(player,context,creationId,1,1,0,1,positionList)
    return True,'执行成功'


@gm_cmd('$sendrewardIDglobalmail', (Int('mailId'), Int('rewardID'), Str('despArgsStr'), Str('title'), Str('cont'),
                            Int('minRoleTime'), Int('maxRoleTime'),Int('minRoleLevel'), Int('maxRoleLevel'), Int('channel')),
        RSU, gameconst.BASE, '发送一封全服邮件', INSIDE, GOD_GROUPS)
def sendrewardIDglobalmail(su, mailId, rewardID, despArgsStr, title, cont, minRoleTime, maxRoleTime, minRoleLevel, maxRoleLevel, channel):
    # attachStr: 多个物品用分号';'分隔; 每个物品有itemId, itemNum，若有绑定属性配置在第三个位置，例如：[30000001,100; 30001031,1,1]
    import dropAward
    import awardContext
    import itemData_set as IDSD
    COIN_ID = IDSD.datas['itemID_coin']['value']
    MONEY_ID = IDSD.datas['itemID_money']['value']
    attach = dropAward.MailWealthVal()

    dropCtx = awardContext.DropAwardCtx(1234, 20, {'lv': 20}, eventTipId=5678,
                                    monsterId=5678,
                                    monsterSpaceNo=10020000, activityId=0)
    award = dropAward.getAwardOne(rewardID, dropCtx)


    # if award.coin:
    #     coinnum = award.coin
    #     attach.addWealthByItemId(COIN_ID,coinnum, 0)

    # if award.money:
    #     moneynum = award.money
    #     attach.addWealthByItemId(MONEY_ID,moneynum, 0)

    if award.itemWealth.itemsObjs:
        equipdata = award.itemWealth.itemsObjs
        for equip in equipdata:
            attach.addWealthByItemId(equip.itemId, equip.itemNum, 0)

    if award.itemWealth.data:
        itemWealthData = award.itemWealth.data
        for itemId, bindTypeDict in itemWealthData.items():
            for bindType, itemNum in bindTypeDict.items():
                attach.addWealthByItemId(itemId, itemNum, bindType)

    despArgs = mailAssistor.parseDespStr(despArgsStr)
    title = title.strip("[] ")
    cont = cont.strip("[] ")
    gameengine.getGlobalBase('GlobalMailStub').sendGlobalMail(mailId, attach, despArgs, title, cont, minRoleTime, maxRoleTime,
                                                              minRoleLevel, maxRoleLevel, channel, AAC_AACDD.datas.BONUS_SRC_GM)
    return True, '执行成功'


@gm_cmd('$changeAllSkill', (Player("gbId/Id"), Str('skillList')),RARG(0), gameconst.CELL, '指定怪物替换技能', ALLSIDE, GOD_GROUPS)
def changeAllSkill(su, player,skillList):
    import ast
    newSkillList = ast.literal_eval(skillList)
    eid = player.selectedTargetId
    e = KBEngine.entities.get(eid)
    if not e or not e.IsCombatUnit:
        return su.onCommandResult(0, 'False,技能替换失败', {})
    e.changeAllSkill(newSkillList)
    return su.onCommandResult(0, 'ok,怪物技能替换成功', {})

@gm_cmd('$setProp', (Player("gbId/Id"),Str("propName"), Float("value"),), RARG(0), gameconst.CELL, '设置人物属性', ALLSIDE, GOD_GROUPS)
def setProp(su, player,propName,value):
    if value or propName:
        player.setProp(f'{propName}', value, gameconst.SourceType.Default)
        return True, '执行成功'
    return False, f'检查propName:{propName}'

@gm_cmd('$enterCubeRoom', (Player("gbId/Id"), Int("mapId"),), RARG(0), gameconst.CELL, '进入魔方阵指定房间', ALLSIDE, GOD_GROUPS)
def enterCubeRoom(su, player, mapId):
    if player.gmEnterCubeRoom(mapId):
        return True, '执行成功'
    else:
        return False, '执行失败'

@gm_cmd('$createCubeCowTeleport', (Player("gbId/Id"), ), RARG(0), gameconst.CELL, '创建进入魔方阵的传送门', ALLSIDE, GOD_GROUPS)
def createCubeCowTeleport(su, player):
    if not formula.isCubeSpace(player.spaceNo):
        return False, '当前不在魔方空间'

    player.spaceMgr.createTeleporterToCow(player.position)
    return True, '执行成功'


@gm_cmd('$changeSceneStates', (Player("gbId/Id"), Str("states")), RARG(0), gameconst.CELL, '设置场景状态', ALLSIDE, GOD_GROUPS)
def changeSceneStates(su, player, states):
    if not formula.isWolrdBossSpace(player.spaceNo):
        return False, '当前不在boss场景'

    _state = []
    for i, _st in enumerate(states):
        _st = 1 if _st == '1' else 0
        if _st:
            _state.append(i)

    DEBUG_MSG('setSceneStates', _state)
    player.setSceneStates(_state)
    return True, '执行成功'


@gm_cmd('$levelUpSkill', (Player("gbId/Id"), Int("skillId"), Int("level")), RARG(0), gameconst.BASE, '升级指定技能到指定等级', ALLSIDE, GOD_GROUPS)
def levelUpSkill(su, player, skillId, level):
    if not player:
        return False, "玩家不存在"

    import skill_skill as SSD
    if skillId not in SSD.datas:
        return False, f"技能ID {skillId} 不存在"

    newLevel = level
    player.buildDic.skillLevels[skillId] = newLevel
    player.cell.onChangeSkillLv(skillId, newLevel)
    player.updateSkillLevelSetSummonSlotIdx(skillId, newLevel)

    # 处理相关联的被动技能升级（参考原有逻辑）
    relatedSkills = SSD.datas.get(skillId, {}).get('conflictSkill') or ()
    for sid in relatedSkills:
        if sid in player.buildDic.skillLevels:
            player.buildDic.skillLevels[sid] = newLevel
            player.updateSkillLevelSetSummonSlotIdx(sid, newLevel)

    player.client.onUpdateSkillLevel([skillId], [newLevel])

    return True, f"技能 {skillId} 已升级到等级 {level}"

@gm_cmd('$gotoLinePos', (Player("gbId/Id"), Int('spaceNo'),  Float('x'), Float('y'), Float('z')), RARG(0), CELL,
        '传送到大世界地图指定位置', ALLSIDE, GOD_GROUPS, minArgs=2)
def gotoLinePos(su, player, spaceNo=0, x=0, y=0, z=0):
    if spaceNo == 0:
        spaceNo = player.spaceNo

    pos = Math.Vector3(x, y, z)
    if x == 0 and y == 0 and z == 0:
        pos, _ = utils.getPlayerBornInfo()

    try:
        lineNo = formula.getLineNo(spaceNo)
        lineType = formula.getLineType(spaceNo)
        if formula.getMapId(player.spaceNo) == lineType:
            return False, '执行失败'

        player.applyEnterLineInternal(lineType, lineNo, pos, player.direction, False)
    except:
        gameengine.reportCritical('gm gotoLinePos error')
        return False, '执行失败'
    return True, '执行成功'

@gm_cmd('$applyFinishGather', (Player("gbId/Id"),), RARG(0), gameconst.CELL, '主动结束采集', ALLSIDE, GOD_GROUPS)
def applyFinishGather(su, player):
    gatherTarget = player.getTempMiscProp(gameconst.AvatarProps.gatherTarget, None)
    if not gatherTarget or 'timer' not in gatherTarget:
        return False, '当前没有采集物体'
    player.applyFinishGather(player.id, gatherTarget['targetId'])

@gm_cmd('$clearPickedCollections', (Player("gbId/Id"), Int("collection id"),), RARG(0), gameconst.CELL, '主动结束采集', ALLSIDE, GOD_GROUPS)
def clearPickedCollections(su, player, collectionId):
    curAOI = player.getViewRadius()
    for m in player.entitiesInRange(curAOI, 'Collection'):
        if m.collectionId != collectionId:
            continue

        player.pickedCollections.pop(collectionId, None)
        m.gatherAvatars.pop(player.gbId, None)
        player.checkCollectionGatherFlag(m.id)
        if m.type == gameconst.CollectionType.VIEWPOINT:
            player.checkRelationType(m)

    return True, '执行成功'

@gm_cmd('$setVIP', (Player("gbId/Id"), Str("account"),), RARG(0), gameconst.BASE, '设置特权', ALLSIDE, GOD_GROUPS)
def setVIP(su, player, account):
    redisUtils.RedisUtils.set(gameconst.PrivilegeRedisKey.VIP + account, "1")
    return True, '执行成功'

@gm_cmd('$setSVIP', (Player("gbId/Id"), Str("account"),), RARG(0), gameconst.BASE, '设置特权', ALLSIDE, GOD_GROUPS)
def setSVIP(su, player, account):
    redisUtils.RedisUtils.set(gameconst.PrivilegeRedisKey.SVIP + account, "1")
    return True, '执行成功'
