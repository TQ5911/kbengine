# -*- coding: utf-8 -*-

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
import buff_buff as B_BD
import itemData_itemData as ITEM_DATA
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import gearBase_gearBase as GBG
import taskdata as TDD

import json
import redisUtils
import random
import utils
import dataUtils
import dropAward
import awardContext
import gameconfig
import mailAssistor

import base64
import gameclass
import itemFactory
import math, Math
import actionContext
import iRouter
import gearBase_gearConst as GBGCD


BASE, CELL, ALL, INSIDE, ALLSIDE = gameconst.BASE, gameconst.CELL,\
    gameconst.ALL, gmAdmin.INSIDE, gmAdmin.ALLSIDE

Int, Str, Float, Player, Entity, PlayerAccount = gmCommand.Int, gmCommand.Str,\
    gmCommand.Float, gmCommand.Player, gmCommand.Entity, gmCommand.PlayerAccount

gm_cmd, forwardGMCommand, callOnApps = gmCommand.gm_cmd, gmCommand.forwardGMCommand,\
    gmCommand._callApps

RARG, RSU, RSTUB, RONE, RALL, SELF = gmCommand.RARG, gmCommand.RSU, gmCommand.RSTUB,\
    gmCommand.RONE, gmCommand.RALL, gmCommand.SELF

GOD_GROUPS, DEVE_GROUPS = gmCommand.GOD_GROUPS, gmCommand.DEVE_GROUPS

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

    except ImportError as entity:
        print(f"导入模块失败: {entity}")
        return None
    except AttributeError as entity:
        print(f"模块中不存在该类: {entity}")
        return None

@gm_cmd('$gmsetstate', (Player("gbId or Id"), Int("int state"),Int("int Pylance"),), RARG(0), gameconst.CELL, '设置状态', ALLSIDE, GOD_GROUPS, minArgs=2)
def gm_gmsetstate(superUser, playerEnt, state, Pylance = 1):
    if Pylance == 1:
        playerEnt.setState(state)
    elif Pylance == 0:
        playerEnt.removeState(state)
    else:
        return False,"执行失败"
    return True, 'command success'

@gm_cmd('$gotomapdataid', (Player("gbId or Id"), Int("int mapdataid")), RARG(0), CELL,
        '传送到地图实体位置', ALLSIDE, GOD_GROUPS, minArgs=2)
def gm_gotomapdataid(superUser, playerEnt, mapdataid):
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
            if mapidNO and mapidNO != playerEnt.spaceNo:
                playerEnt.base.teleportByNo(mapidNO, pos, playerEnt.direction, '', ())
            else:
                playerEnt.telToPos(pos)
        else:
            return False, '执行失败,id不存在'
    else:
        return False, '执行失败,id小于10000000，不是地图编辑器里的ID'

@gm_cmd('$sethp', (Player("gbId or Id"), Int("int hp"),), RARG(0), gameconst.CELL, 'set hp', ALLSIDE, GOD_GROUPS)
def gm_setPlayerHp(superUser, playerEnt, hp):
    if hp < 0:
        return False, '血量不能小于0'

    playerEnt.hp = hp
    return True, 'command success'


@gm_cmd('$adjfullHp', (Player("gbId or Id"), Int("int fullhp"),), RARG(0), gameconst.CELL, '添加总血量', ALLSIDE, GOD_GROUPS)
def gm_setPlayerFullHp(superUser, playerEnt, addfullhp):
    if addfullhp < 0:
        return False, '血量不能小于0'
    playerEnt.setProp('adjFullHp', addfullhp, gameconst.SourceType.SrcTpDefault)
    playerEnt.setProp('adjFullMp', addfullhp, gameconst.SourceType.SrcTpDefault)
    playerEnt.addBuff(64000069,1,playerEnt.id)
    return True, 'command success'

@gm_cmd('$setultraSkillPower', (Player("gbId or Id"), Int("int ultraSkillPower"),), RARG(0), gameconst.CELL, '设置大招充能值', ALLSIDE, GOD_GROUPS)
def gm_setPlayerultraSkillPower(superUser, playerEnt, ultraSkillPower):
    playerEnt.ultraSkillPower = ultraSkillPower
    return True, 'command success'

@gm_cmd('$reliveToPos', (Player("gbId or Id"), Str("str position"), Int("int hp")), RARG(0), CELL, '复活', ALLSIDE, GOD_GROUPS)
def gm_reliveToPos(superUser, playerEnt, position_str, hp):
    if position_str == 'None' or not position_str:
        position = None
    else:
        coords = position_str.strip('()').split(',')
        position = Math.Vector3(float(coords[0]), float(coords[1]), float(coords[2]))
    
    direction = playerEnt.direction
    playerEnt.reliveToPos(position, direction, hp, None)
    return True, 'command success'



@gm_cmd('$showprop', (Int("int entityId"),), RSU, CELL, '显示实体属性', INSIDE, GOD_GROUPS)
def gm_showEntityProp(superUser, entityId):
    if entityId <= 0:
        return False, '非法的实体ID'

    _target = KBEngine.entities.get(entityId, None)
    if not _target:
        return False, '没有找到ID为%s实体' % entityId

    print('-------------------- [prop start] --------------------')
    import fightProp_define as FP_DD
    for _propName in FP_DD.datas.keys():
        if hasattr(_target, _propName):
            print('{0}: {1}'.format(_propName, getattr(_target, _propName)))
    print('-------------------- [prop end]   --------------------')

    return True, 'command success'

@gm_cmd('$deducthp', (Player("gbId or Id"), Int('damage'), Int('entityId'),), RARG(0), CELL, '扣除目标血量', ALLSIDE, GOD_GROUPS, minArgs=1)
def gm_deductHp(superUser, playerEnt, damage, eid=0):
    # 如果没有指定目标实体ID，则使用玩家当前选中的目标
    eid = eid or playerEnt.selectedTargetId
    # 获取目标实体
    entity = KBEngine.entities.get(eid)
    # 检查目标是否存在且是战斗单位
    if not entity or not entity.IsCombatUnit:
        return False, '%s不存在或者不是战斗单位' % eid

    # 确保扣除的血量不会超过目标当前血量
    actual_damage = min(damage, entity.hp)
    # 修改目标血量，从当前血量中扣除指定数值
    entity.modifyHP(-actual_damage, playerEnt.id, gameconst.SourceType.SrcTpSkill, 0)
    # 返回执行成功的消息，包含实际扣除的血量
    return True, '成功扣除%d点血量，目标剩余血量: %d' % (actual_damage, entity.hp)

@gm_cmd('$createmonster', (Player("gbId or Id"), Int('monster id'), Int('level'), Int('monsterNum'), Float('radius'), Int('force')), RARG(0), CELL,
        '创建怪物，可指定数量和半径', ALLSIDE, GOD_GROUPS, minArgs=3)
def gm_createMonster(superUser, playerEnt, monsterId, level, monsterNum=1, radius=0, force=0):
    # 检查怪物ID和等级是否有效
    if monsterId not in MD.datas or level < 1 or monsterNum < 1:
        return False, '执行失败'
    # 计算每个怪物之间的角度间隔（弧度）
    angle_step = 2 * math.pi / monsterNum

    # 玩家当前朝向（假设player.direction是欧拉角或四元数）
    # 将玩家朝向转换为弧度角，这里假设direction.z是偏航角（yaw）
    player_yaw = playerEnt.direction.z

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
        monster_x = playerEnt.position.x + x_offset
        monster_y = playerEnt.position.y  # 保持与玩家相同的高度
        monster_z = playerEnt.position.z + z_offset

        monster_position = (monster_x, monster_y, monster_z)

    # 创建怪物参数
        props = {
            'monsterId': monsterId,
            'spaceMgrId': playerEnt.spaceMgrId,
            'spaceNo': playerEnt.spaceNo,
            'position': monster_position,
            'direction': playerEnt.direction,  # 可以让怪物面向与玩家相同的方向
            'level': level,
            'force': force,
        }
        # 创建一个怪物
        KBEngine.createEntity(
            'Monster',
            playerEnt.spaceID,
            monster_position,
            playerEnt.direction,
            props,
        )

    return True, f'成功在玩家周围{radius}米的圆上创建了{monsterNum}个怪物'

@gm_cmd('$createAvatarReplica', (Player("gbId or Id"), Int('arType'), ), RARG(0), CELL, '创建Avatar副本', ALLSIDE, GOD_GROUPS, minArgs=1)
def gm_createAvatarReplica(superUser, playerEnt, arType=1):
    props = playerEnt.cloneAvatarProps(arType)
    props.update({
        'spaceNo': playerEnt.spaceNo,
        "direction": playerEnt.direction,
        "position": playerEnt.position,

        'tmpProps': {'overwriteProps': {'hpMult': 3}},
        'spaceMgrId': playerEnt.spaceMgrId,
        'replicaId': 11011099,
        #'gameEntityId': next(utils.genGameEntityId(31250003, 1), 0)
    })
    KBEngine.createEntity('AvatarReplica', playerEnt.spaceID, playerEnt.position, playerEnt.direction, props)
    return True, 'command success'

@gm_cmd('$addcoin', (Player("gbId or Id", raw=True), Float("num"),), RARG(0), BASE, '增加货币', ALLSIDE, GOD_GROUPS)
def gm_addCoin(superUser, playerEnt, num):
    _opUUID = KBEngine.genUUID64()
    src = AAC_AACDD.datas.BONUS_SRC_GM
    detail = gameclass.AwardDetailCls(gm_cmd='$addcoin', num=num)

    if gmCommand.isRawPlayer(playerEnt):
        gbId, name, accountName, dbId = playerEnt
        if num > 0:
            gamesql.recordAvatarOfflineCallback(gbId, 'addCoin', (num, _opUUID, src, detail))
        elif num < 0:
            gamesql.recordAvatarOfflineCallback(gbId, 'gmDeleteItems', (gameconst.ItemIdEnum.COIN, abs(num), detail))
    else:
        if num > 0:
            playerEnt.addCoin(num, _opUUID, src, detail)
        elif num < 0:
            playerEnt.deductCoinNoLimit(abs(num), _opUUID, src, detail)

    superUser.onCommandResult(0, '', {})

    return True, 'command success'


@gm_cmd('$deductcoin', (Player("gbId or Id", raw=True), Float("num"),), RARG(0), BASE, '扣除货币，不够时失败', ALLSIDE,
        GOD_GROUPS)
def gm_deductcoinCompletely(superUser, playerEnt, num):
    _opUUID = KBEngine.genUUID64()
    src = AAC_AACDD.datas.BONUS_SRC_GM
    num = abs(num)
    detail = gameclass.AwardDetailCls(gm_cmd='$addcoin', num=num)

    if gmCommand.isRawPlayer(playerEnt):
        gbId, name, accountName, dbId = playerEnt

        def _onCheckDeduct(ret, hasCoin, alreadyDeductNum, needDeduct):
            if ret:
                superUser.onCommandResult(ret, '', {'coin': hasCoin})
                return
            gamesql.recordAvatarOfflineCallback(gbId, 'gmDeleteItems', (gameconst.ItemIdEnum.COIN, num, detail))
            superUser.onCommandResult(0, '', {})

        gamesql.checkOfflineDeductWealth(gbId, gameconst.ItemIdEnum.COIN, num, _onCheckDeduct)
    else:
        if playerEnt.deductCoin(num, _opUUID, src, detail, bMsg=False):
            superUser.onCommandResult(0, '', {})
        else:
            superUser.onCommandResult(gameconst.GMCommandErr.GM_RET_INSUFFICIENT, 'insufficient', {'coin': playerEnt.coin})

    return True, 'command success'


@gm_cmd('$setvar', (Player("gbId or Id"), Int("int varId"), Int("int value"),), RARG(0), BASE, '设置变量值', ALLSIDE, GOD_GROUPS)
def gm_setVar(superUser, playerEnt, varId, value):
    _opUUID = KBEngine.genUUID64()
    _varSrc = gameconst.VarChangeSrcEnum.VAR_SRC_GM
    _desc = 'gm_cmd:$setvar {} {}'.format(varId, value)
    playerEnt.gmSetVar(varId, value, _opUUID, _varSrc, _desc)
    return True, 'command success'


@gm_cmd('$getvar', (Player("gbId or Id"), Int("int varId"),), RARG(0), BASE, '读取变量值', ALLSIDE, GOD_GROUPS)
def gm_getVar(superUser, playerEnt, varId):
    result, desc = playerEnt.gmGetVar(varId)
    return result, desc


@gm_cmd('$clearspace', (Str('clearType'),), RSU, CELL, '清除当前场景实体', INSIDE, GOD_GROUPS, minArgs=0)
def gm_clearspace(superUser, clearType):
    if clearType == "":
        _lineType = formula.parseLineType(superUser.spaceNo)
        _typeList = utils.getDunStructModData(_lineType)['InitEntities'].keys()
        for _e in KBEngine.entities.values():
            if _e.__class__.__name__ in _typeList:
                _e.safeDestroy()
    else:
        for _e in KBEngine.entities.values():
            if _e.__class__.__name__ == clearType:
                _e.safeDestroy()
    return True, 'command success'


@gm_cmd('$crtbyid', (Str('game entityId'),), RSU, CELL, '根据唯一标识创建实体', INSIDE,
        GOD_GROUPS)
def gm_createEntityById(superUser, gameEntityId):
    _spaceBase = gameengine.getSpaceBase(superUser.spaceNo)

    if not _spaceBase:
        return False, '未知空间'

    _spaceCellCall = _spaceBase.cell

    _spaceCellCall.createEntityById(gameEntityId, None)

    return True, 'command success'


@gm_cmd('$crtherebyid', (Str('game entityId'),), RSU, CELL,
        '根据唯一标识在当前位置创建实体', INSIDE, GOD_GROUPS)
def gm_createEntityHereById(superUser, gameEntityId):
    _spaceBase = gameengine.getSpaceBase(superUser.spaceNo)

    if not _spaceBase:
        return False, '未知空间'

    _spaceCellCall = _spaceBase.cell

    _spaceCellCall.createEntityById(gameEntityId, {'Pos': superUser.position})

    return True, 'command success'


@gm_cmd('$rmbyid', (Str('game entityId'),), RSU, CELL,
        '根据唯一标识删除创建的实体', INSIDE, GOD_GROUPS)
def gm_removeEntityById(superUser, gameEntityId):
    _spaceBase = gameengine.getSpaceBase(superUser.spaceNo)

    if not _spaceBase:
        return False, '未知空间'

    _spaceBase.cell.removeEntById(gameEntityId)

    return True


@gm_cmd('$createRobot', (Player("gbId or Id"), Int('robotDataId'), Int('level')), RARG(0), CELL, '创建机器人', ALLSIDE,
        GOD_GROUPS)
def gm_createRobot(superUser, playerEnt, robotDataId, level):
    import utils
    import robotData_robotData
    import gameconst

    def _createEntity():
        _entType = 'AvatarMirror'
        _extraProps = {'spaceNo': playerEnt.spaceNo,
                      'monsterId': 0,
                      'gbId': KBEngine.genUUID64()}

        if playerEnt.spaceMgr:
            _extraProps.update({'spaceMgrId': playerEnt.spaceMgr.id,
                               'spaceMgrBox': playerEnt.spaceMgr.base})

        _randomTempBotId = robotDataId or random.choice(list(robotData_robotData.datas))

        # init school
        _school = robotData_robotData.datas[_randomTempBotId]['schoolID']

        # init name
        _name = utils.getRandomName()

        _props = utils.getRobotPropDict(_randomTempBotId, _name, _school, level)

        _props['force'] = gameconst.ForceTypeEnum.Monster
        _props['sex'] = utils.getRandomSex()

        _props.update(_extraProps)

        _ent = KBEngine.createEntity(_entType, playerEnt.spaceID, tuple(playerEnt.position), tuple(playerEnt.direction), _props)
        return _ent

    try:
        entity = _createEntity()
    except:
        gameengine.panicStack('gm create Robot error')
        return False, '执行失败, 创建中出错, 请联系管理员排查'
    if not entity:
        return False, '执行失败'
    return True, 'command success'


@gm_cmd('$createnpc', (Player("gbId or Id"), Int('npc_id'), Int('level')), RARG(0), CELL, '创建NPC', ALLSIDE, GOD_GROUPS)
def gm_createNPC(superUser, playerEnt, npcId, level):
    import NPC_NPC as NPC_D
    import creep_base as CBD
    if npcId not in NPC_D.datas or level < 1:
        return False, '执行失败, 请检查参数'

    _params = {
        'npcId': npcId,
        'name': NPC_D.datas[npcId]['name'],
        'spaceNo': playerEnt.spaceNo,
        'spaceID': playerEnt.spaceID,
        'position': playerEnt.position,
        'direction': playerEnt.direction,
    }

    _npcCreepId = NPC_D.datas[int(npcId)].get('creepID')
    _className = 'Npc'
    if _npcCreepId and _npcCreepId in CBD.datas and CBD.datas[_npcCreepId]['AI']:
        _className = 'CNpc'
        _npcAI = NPC_D.datas[int(npcId)].get('AI')
        if _npcAI:
            _params.update({'aiName': _npcAI})

    playerEnt.base.callMethod('gmCreateEntityHasBase', (_className, _params))
    return True, 'command success'


@gm_cmd('$createTeleporter', (Player("gbId or Id"), Int('teleportId'), Int('type'), Str('mapIds')), RARG(0), CELL, '创建传送门', ALLSIDE,
        GOD_GROUPS)
def gm_createTeleporter(superUser, playerEnt, teleportId, teleportType, mapsIds):
    _mapIds = mapsIds.split(',')
    _mapIds = [int(i) for i in _mapIds]
    props = {
        'teleportType': teleportType,
        'mapIds': _mapIds,
        'name': 'hahaha',
        'teleporterId': teleportId,
        'spaceNo': playerEnt.spaceNo,
        'spaceno': playerEnt.spaceNo,
        'direction': playerEnt.direction,
        'position': playerEnt.position,
    }
    KBEngine.createEntity(
        'Teleporter',
        playerEnt.spaceID,
        playerEnt.position,
        playerEnt.direction,
        props,
    )
    return True, 'command success'


@gm_cmd('$createcollection', (Player("gbId or Id"), Int('collection id'),), RARG(0), CELL, '创建采集物', ALLSIDE,
        GOD_GROUPS)
def gm_createCollection(superUser, playerEnt, collId):
    import NPC_Pick
    if collId not in NPC_Pick.datas:
        return False, '执行失败'

    _props = {
        'name': NPC_Pick.datas[collId]['name'],
        'type': NPC_Pick.datas[collId]['type'],
        'collectionId': collId,
        'spaceNo': playerEnt.spaceNo,
        'position': playerEnt.position,
        'direction': playerEnt.direction,
        'spaceMgrId': playerEnt.spaceMgrId,
    }
    KBEngine.createEntity(
        'Collection',
        playerEnt.spaceID,
        playerEnt.position,
        playerEnt.direction,
        _props,
    )
    # playerEnt.base.callMethod('gmCreateEntityHasBase', ('Collection', props))
    return True, 'command success'


@gm_cmd('$goto', (Player("gbId or Id"), Float('xx'), Float('yy'), Float('zz'), Int('spaceNo')), RARG(0), CELL,
        '传送到目标位置', ALLSIDE, GOD_GROUPS, minArgs=4)
def gm_gotoPosition(superUser, playerEnt, x, y, z, spaceNo=0):
    if spaceNo and spaceNo != playerEnt.spaceNo:
        if not formula.inStaticScene(playerEnt.spaceNo) or not formula.inStaticScene(spaceNo):
            return False, '只能在大世界使用'
        playerEnt.base.teleportByNo(spaceNo, (x, y, z), playerEnt.direction, '', ())
    else:
        playerEnt.telToPos((x, y, z))
    return True, 'command success'


@gm_cmd('$gotoid', (Entity('entityId'),), RARG(0), CELL, '传送到目标实体位置', INSIDE, GOD_GROUPS)
def gm_gotoById(superUser, playerEnt):
    if superUser.spaceNo == playerEnt.spaceNo:
        superUser.telToPos(playerEnt.position)
        return True, 'command success'

    superUser.cell.callMethod(
        'gmGotoByid', 
        (
            playerEnt, 
            playerEnt.spaceNo, 
            playerEnt.position, 
            playerEnt.direction, 
            getattr(playerEnt, 'tilemapsInfo', '')))
    return True, 'command success'


@gm_cmd('$getpos', (Entity('entityId'),), RARG(0), CELL, '获得目标实体位置', INSIDE, GOD_GROUPS)
def gm_getPosition(superUser, entity):
    return True, '执行成功：%s %s' % (entity.spaceNo, str(entity.position))


@gm_cmd('$recordpos', (Entity('entityId'), Int('invaild'),), RARG(0), CELL, '记录目标实体位置和面向', INSIDE,
        GOD_GROUPS, minArgs=1)
def gm_recordPos(superUser, entity, invaild=1):
    writeStr = "recordpos %s %s %s,%s,%s\n" % (
        entity.position[0], entity.position[1], entity.position[2], str(entity.direction[2]), invaild)
    print("%s " % writeStr)
    detailFile = open("recordpos.txt", "a", encoding='UTF-8')
    detailFile.write(writeStr)
    detailFile.close()
    return True, '执行成功：%s %s %s' % (entity.spaceNo, str(entity.position), str(entity.direction[2]))


@gm_cmd('$debugai', (Entity('entityId'), Int('log ai'), Int('LOG HATE')), RARG(0), CELL, '打开对应实体的ai日志',
        ALLSIDE, GOD_GROUPS)
def gm_toggleAIDebug(superUser, ent, enableLogAITrace, enableLogHate):
    if not hasattr(ent, 'aiController'):
        return False, '执行失败，实体没有aiController'

    if not hasattr(ent.aiController, 'tree'):
        return False, '执行失败，实体没有aiController.tree'

    ent.aiController.logAITrace = enableLogAITrace

    ent.aiController.logHate = enableLogHate

    return True, 'command success'


@gm_cmd('$speed', (Player('entityId'), Float('speed')), RARG(0), CELL, '设置玩家速度', ALLSIDE, GOD_GROUPS)
def gm_setSpeed(superUser, playerEnt, speed):
    if gmCommand.isRawPlayer(playerEnt):
        return False, '执行失败'

    playerEnt.topSpeed = speed * 15
    playerEnt.setSpeed(speed)
    return True, 'command success'


@gm_cmd('$moralValue', (Player('entityId'), Int('moralValue')), RARG(0), CELL, '设置玩家善恶值', ALLSIDE, GOD_GROUPS)
def gm_setmoralValue(superUser, playerEnt, moralValue):
    if gmCommand.isRawPlayer(playerEnt):
        return False, '执行失败'

    playerEnt.moralValue = moralValue
    playerEnt.moralLevel = utils.getMoralLevel(playerEnt.moralValue)
    return True, 'command success'

@gm_cmd('$setRewardNumber', (Player('gbId or Id'), Int('RewardNumber')), RARG(0), BASE, '设置讨伐次数', ALLSIDE, GOD_GROUPS)
def gm_setRewardNumber(superUser, playerEnt, RewardNumber):
    if gmCommand.isRawPlayer(playerEnt):
        return False, '执行失败'
    playerEnt.crusadeInfo.rewardNumber = RewardNumber
    return True, 'command success'

@gm_cmd('$topspeed', (Player('entityId'), Float('speed')), RARG(0), CELL, '设置玩家最大速度', ALLSIDE, GOD_GROUPS)
def gm_setTopSpeed(superUser, playerEnt, speed):
    if gmCommand.isRawPlayer(playerEnt):
        return False, '执行失败'

    playerEnt.topSpeed = speed
    return True, 'command success'


@gm_cmd('$getSpeed', (Player('entityId'),), RARG(0), CELL, 'get玩家速度', ALLSIDE, GOD_GROUPS)
def gm_getSpeed(superUser, playerEnt):
    if gmCommand.isRawPlayer(playerEnt):
        return False, '执行失败'

    print("getSpeed------", playerEnt.getSpeed())
    return True, '' + str(playerEnt.getSpeed())


@gm_cmd('$setpos', (Player('palyer id'), Float('x'), Float('y'), Float('z'), Float('dir'), Int('spaceNo')), RARG(0),
        CELL, '设置玩家位置', ALLSIDE, GOD_GROUPS, True, minArgs=4)
def gm_setPosition(superUser, playerEnt, x, y, z, direction=0, spaceNo=0):
    spaceNo = spaceNo or playerEnt.spaceNo
    tgtDirection = playerEnt.direction
    if direction:
        tgtDirection[2] = direction
    playerEnt.teleportToCell(playerEnt, spaceNo, (x, y, z), tgtDirection, '', ())
    return True, 'command success'


@gm_cmd('$getrandomitems', (Player("gbId or Id"), Int('bagType'), Int('item num'), Int('bindType')), RARG(0), BASE,
        '获取随机物品', ALLSIDE, GOD_GROUPS)
def gm_getRandomItems(superUser, playerEnt, bagType, itemNum, bindType):
    if itemNum < 1 or itemNum > 99:
        return False, '执行失败'
    _itemsFilter = filter(lambda data: bagType == data['type'], ITEM_DATA.datas.values())
    items = list(_itemsFilter)
    if 0 == len(items):
        return False, '执行失败'

    _itemDict = {}
    _sumNum = 0
    _loopCnt = 0
    while _sumNum < itemNum and _loopCnt < 99:
        _loopCnt += 1
        _oneItem = random.choice(items)
        _maxSize = _oneItem['maxStackSize']
        if _maxSize == 0:
            continue
        _addNum = random.randint(1, _maxSize)
        if _addNum + _sumNum > itemNum:
            _addNum = itemNum - _sumNum
        _sumNum += _addNum
        itemId = _oneItem['ID']
        if itemId in _itemDict:
            _itemDict[itemId] += _addNum
        else:
            _itemDict[itemId] = _addNum

    for _itemId, _itemAddNum in _itemDict.items():
        itemData = ITEM_DATA.datas.get(_itemId, None)
        _maxSize = itemData['maxStackSize']
        if 0 == _maxSize:
            continue
        _leftNum = _itemAddNum
        while _leftNum > 0:
            if _leftNum > _maxSize:
                _addNum = _maxSize
            else:
                _addNum = _leftNum
            _leftNum -= _addNum
            ret = playerEnt.gmAddItems(bagType, _itemId, _addNum, 'gm_cmd:$getrandomitems %s' % itemNum, bindType=bindType)
            if ret:
                return False, '执行失败'
    return True, 'command success'


@gm_cmd('$getfixedbox',
        (Player("gbId or Id", raw=True), Int('bagType'), Int('itemId'), Int('bindType'), Str('boxItemsJson')), RARG(0),
        BASE, '获取固定内容宝箱', ALLSIDE, GOD_GROUPS)
def gm_getFixedItemsBox(superUser, playerEnt, bagType, itemId, bindType, boxItemsJson):
    if bagType not in (0, 1, 2, 3):
        return False, '执行失败, 无法添加此物品ID, 背包类型错误, {}-{}--{}'.format(itemId, bagType, bindType)
    try:
        boxItems = json.loads(boxItemsJson)
    except Exception as entity:
        superUser.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '', {})
        return False, '执行失败'

    boxWealth = dropAward.AwardVal()
    for itemIdStr, itData in boxItems.items():
        boxItemId = int(itemIdStr)
        itemNum, boxItemBindType = itData
        boxWealth.addWealthByItemId(boxItemId, itemNum, boxItemBindType)

    fixedBox = itemFactory.ItemFactory.createItem(itemId, 1, bindType, boxWealth=boxWealth)
    wval = dropAward.AwardVal().addWealthByObjList([fixedBox])

    detail = 'gm_cmd:$getitems %s %s %s' % (itemId, itemNum, bindType)
    _opUUID = KBEngine.genUUID64()
    if gmCommand.isRawPlayer(playerEnt):
        gbId, name, accountName, dbId = playerEnt
        gamesql.recordAvatarOfflineCallback(gbId, 'gmAddWealth', (bagType, wval, _opUUID, detail))
    else:
        playerEnt.gmAddWealth(bagType, wval, _opUUID, detail)

    superUser.onCommandResult(0, '', {})
    return True, 'command success'

@gm_cmd('$getitems', (Player("gbId or Id", raw=True), Int('bagType'), Int('itemNum'), Float('_bindType'), Int('itemId_Start'), Int('itemId_End')),
        RARG(0), BASE, '获取指定物品', ALLSIDE, GOD_GROUPS, minArgs=4)
def gm_getItems(superUser, playerEnt, bagType, itemNum, _bindType, itemId_Start, itemId_End = 0):
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
                if gmCommand.isRawPlayer(playerEnt):
                    continue
                else:
                    # 调用玩家的gmAddGearbaseEquipItem方法添加装备
                    ret = playerEnt.gmAddGearbaseEquipItem(itemId,bindType)
            # 如果不存在，检查是否在普通物品表中存在
            elif itemId in ITEM_DATA.datas:
                detail = 'gm_cmd:$getitems %s %s %s' % (itemId, itemNum, bindType)
                # 判断是否为原始玩家对象（可能是离线玩家）
                if gmCommand.isRawPlayer(playerEnt):
                    # 如果是原始玩家，解包玩家信息
                    gbId, name, accountName, dbId = playerEnt
                    # 记录离线玩家的回调，当玩家上线时执行gmAddItems操作
                    gamesql.recordAvatarOfflineCallback(gbId, 'gmAddItems', (bagType, itemId, itemNum, detail, bindType))
                else:
                    LOG_DBG('gmAddItems:', bagType, itemId, itemNum, detail,bindType)
                    # 如果是在线玩家，直接调用gmAddItems方法添加物品
                    playerEnt.gmAddItems(bagType, itemId, itemNum, detail,bindType)
            else:
                continue
    superUser.onCommandResult(0, '', {})
    return True, 'command success'


@gm_cmd('$delitems', (
        Player("gbId or Id", raw=True), Int('itemId'), Int('itemNum'),
        Int('bindType', default=gameconst.ItemBindType.BIND)),
        RARG(0), BASE, '删除指定物品', ALLSIDE, GOD_GROUPS, minArgs=3)
def gm_deleteItems(superUser, playerEnt, itemId, itemNum, bindType=gameconst.ItemBindType.BIND):
    detail = ''
    if gmCommand.isRawPlayer(playerEnt):
        gbId, name, accountName, dbId = playerEnt
        gamesql.recordAvatarOfflineCallback(gbId, 'gmDeleteItems', (itemId, itemNum, detail, bindType))
    else:
        playerEnt.gmDeleteItems(itemId, itemNum, detail, bindType)

    superUser.onCommandResult(0, '', {})
    return True, 'command success'


@gm_cmd('$cleanbag', (Player("gbId or Id"), Int('bagType'),), RARG(0), BASE, '清空背包', ALLSIDE, GOD_GROUPS)
def gm_clenBag(superUser, playerEnt, bagType):
    ret = playerEnt.gmCleanBag(bagType)
    if ret:
        return True, 'command success'
    else:
        return False, '执行失败'

@gm_cmd('$getGearbaseEquipItem', (Player("gbId or Id"), Int('templateId'), Int('bindType'), Int('grade')), RARG(0), BASE, '获取装备', ALLSIDE, GOD_GROUPS)
def gm_getGear(superUser, playerEnt, templateId, bindType, grade):
    if gmCommand.isRawPlayer(playerEnt):
        return False, '执行失败'
    ret = playerEnt.gmAddGearbaseEquipItem(templateId, bindType, grade)
    if ret == gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
        return True, 'command success'
    else:
        return False, '执行失败'


@gm_cmd('$getReward', (Player("gbId or Id"), Int('dropId'), Int('num'),), RARG(0), BASE, '获取奖励', ALLSIDE, GOD_GROUPS)
def gm_getReward(superUser, playerEnt, dropId, num):
    awardCtx = awardContext.CommonContext(0, {'lv': playerEnt.getRoleCacheAttr('level', 0)})
    _opUUID = KBEngine.genUUID64()
    ret = playerEnt.addAwards(AAC_AACDD.datas.BONUS_SRC_GM, dropId, num, _opUUID, '', awardCtx)
    if ret:
        return True, 'command success'
    else:
        return False, '执行失败'

@gm_cmd('$getDropid', (Player("gbId or Id"), Int('dropId'), Int('num'),), RARG(0), BASE, '执行掉落', ALLSIDE, GOD_GROUPS)
def gm_getDropid(superUser, playerEnt, dropId, num):
    for i in range(num):
        awardCtx = awardContext.CommonContext(0, {'lv': playerEnt.getRoleCacheAttr('level', 0)})
        awardCtx.addContextVar('avatarId', playerEnt.id)
        awardCtx.addContextVar('school', playerEnt.getRoleCacheAttr('school', 0))
        awardCtx.addContextVar('isMonthCardExpired', playerEnt.getRoleCacheAttr('monthCardExpired', True))
        awardCtx.addContextVar('isBigMonthCardExpired', playerEnt.getRoleCacheAttr('bigMonthCardExpired', True))
        awardCtx.addContextVar('avatarScoreRank', playerEnt.avatarScoreRank)
        awardCtx.addContextVar('isCrossServer', playerEnt.isCrossServer)
        _opUUID = KBEngine.genUUID64()
        awardVal = dropAward._getDropAward([dropId], awardCtx)
        autoDisassemble = playerEnt.cliConfigDic.get(gameconst.CliConfigDef.EQUIP_AUTO_DISA_KEY,
                                                gameconst.CliConfigDef.EQUIP_AUTO_DISA_DEFAULT_VAL)
        if autoDisassemble:
            equipList = awardVal.itemWealth.popDropEquipObjs()
            disassembleEquips = []
            for it in equipList:
                if playerEnt.canEquipAutoDisassemble(playerEnt, it) and it.canBeDisassembled(playerEnt.gbId):
                    awardVal += it.returnWealthyByDisassemble(playerEnt)
                    disassembleEquips.append(it)
            for it in disassembleEquips:
                equipList.remove(it)
            awardVal.itemWealth.addItemObjs(equipList)
        ret = playerEnt.addWealth(AAC_AACDD.datas.BONUS_SRC_GM, awardVal, _opUUID, None, awardCtx, notify=True, popWindow=False)
    if ret:
        return True, 'command success'
    else:
        return False, '执行失败'

@gm_cmd('$gmenterDungeon', (Player("gbId or Id"),Int('dungeonNo'), ), RARG(0), CELL, '管理员进入副本', ALLSIDE, GOD_GROUPS)
def gm_gmEnterDungeon(superUser,playerEnt, dungeonNo):
    import gamePlay_gamePlay
    import dungeonSrc
    if dungeonNo not in gamePlay_gamePlay.datas:
        return False, '执行失败, 没有找到相应副本ID'

    src = dungeonSrc.DungeonFromClientGMSrc(playerEnt.base, playerEnt.gbId)

    dungeonSpaceType = gamePlay_gamePlay.datas[dungeonNo]['type']
    dungeonEnterType = gamePlay_gamePlay.datas[dungeonNo]['enterType']
    if gameconst.DungeonTypeJudge.isBothDungeon(dungeonSpaceType, dungeonEnterType):
        if playerEnt.isInTeam(playerEnt.gbId):
            playerEnt.gmEnterTeamDungeon(dungeonNo, src)
            return True, '执行成功, gm正在尝试进入全类型副本(组队)'
        else:
            playerEnt.gmEnterSingleDungeon(dungeonNo, src)
            return True, '执行成功, gm正在尝试进入全类型副本(单人)'
    elif gameconst.DungeonTypeJudge.isTeamDungeon(dungeonSpaceType, dungeonEnterType):
        if not playerEnt.isInTeam(playerEnt.gbId):
            return False, '執行失敗, gm-组队副本必须组队进入'
        playerEnt.gmEnterTeamDungeon(dungeonNo, src)
        return True, '执行成功, gm正在尝试进入组队副本'
    elif gameconst.DungeonTypeJudge.isSingleDungeon(dungeonSpaceType, dungeonEnterType):
        playerEnt.gmEnterSingleDungeon(dungeonNo, src)
        return True, '执行成功, gm正在尝试进入单人副本'
    elif gameconst.DungeonTypeJudge.isRaidDungeon(dungeonSpaceType, dungeonEnterType):
        playerEnt.gmEnterRaidDungeon(dungeonNo, src)
        return True, '执行成功, gm正在尝试进入团队副本'
    else:
        return False, '执行失败, gm-不支持的副本类型'

@gm_cmd('$enterDungeon', (Player("gbId or Id"),Int('dungeonNo'), ), RARG(0), CELL, '进入副本', ALLSIDE, GOD_GROUPS)
def gm_enterDungeon(superUser,playerEnt, dungeonNo):
    import gamePlay_gamePlay
    import dungeonSrc
    if dungeonNo not in gamePlay_gamePlay.datas:
        return False, '执行失败, 没有找到相应副本ID'

    src = dungeonSrc.DungeonFromClientSrc(playerEnt.base, playerEnt.gbId)

    dungeonSpaceType = gamePlay_gamePlay.datas[dungeonNo]['type']
    dungeonEnterType = gamePlay_gamePlay.datas[dungeonNo]['enterType']
    if gameconst.DungeonTypeJudge.isBothDungeon(dungeonSpaceType, dungeonEnterType):
        if playerEnt.isInTeam(playerEnt.gbId):
            playerEnt.selfEnterTeamDungeon(dungeonNo, src)
            return True, '执行成功, 正在尝试进入全类型副本(组队)'
        else:
            playerEnt.selfEnterSingleDungeon(dungeonNo, src)
            return True, '执行成功, 正在尝试进入全类型副本(单人)'
    elif gameconst.DungeonTypeJudge.isTeamDungeon(dungeonSpaceType, dungeonEnterType):
        if not playerEnt.isInTeam(playerEnt.gbId):
            return False, '執行失敗, 组队副本必须组队进入'
        playerEnt.selfEnterTeamDungeon(dungeonNo, src)
        return True, '执行成功, 正在尝试进入组队副本'
    elif gameconst.DungeonTypeJudge.isSingleDungeon(dungeonSpaceType, dungeonEnterType):
        playerEnt.selfEnterSingleDungeon(dungeonNo, src)
        return True, '执行成功, 正在尝试进入单人副本'
    elif gameconst.DungeonTypeJudge.isRaidDungeon(dungeonSpaceType, dungeonEnterType):
        playerEnt.selfEnterRaidDungeon(dungeonNo, src)
    else:
        return False, '执行失败, 不支持的副本类型'

@gm_cmd('$setgmmode', (Player("gbId or Id"), Int("int mode"),), RARG(0), gameconst.BASE, '设置gm模式', ALLSIDE, GOD_GROUPS)
def gm_setGmMode(superUser, playerEnt, gmMode):
    if gmMode not in gameconst.GmModeEnum.ALL_MODES:
        return False, '无效的mode：%s' % (gmMode,)

    playerEnt.gmMode = gmMode
    playerEnt.cell.callMethod('_onSetGmMode', (gmMode,))
    return True, 'command success'


@gm_cmd('$sendmail', (Str("str _toGBID"), Int('mail id'), Int('due time'), Str('_attach str'), Str('despArgsStr'), Str('title'), Str('cont')),
        RSU, gameconst.BASE, '向指定玩家发一封邮件', INSIDE, GOD_GROUPS)
def gm_sendMail(superUser, toGBID, mailId, dueTime, attachStr, despArgsStr, title, cont):
    _toGBID = int(toGBID)
    _attach = mailAssistor.parseAttachStr(attachStr)
    despArgs = mailAssistor.parseDespStr(despArgsStr)
    _title = title.strip("[] ")
    _cont = cont.strip("[] ")
    mailAssistor.sendMailToPlayers([_toGBID], mailId, dueTime=dueTime, extraAttach=_attach, despArgs=despArgs, title=_title, cont=_cont, srcType=AAC_AACDD.datas.BONUS_SRC_GM)
    return True, 'command success'

@gm_cmd('$sendMailByGBIDNoMailId', (Player("gbId or Id", raw=True), Int('dueTime'), Str('attachStr'), Str('title'), Str('cont')), RARG(0), BASE,
        '向指定玩家发一封自定义邮件', ALLSIDE, GOD_GROUPS)
def gm_sendMailByGBIDNoMailId(superUser, playerEnt, dueTime, attachStr, title, cont):
    LOG_DBG('sendMailByGBIDNoMailId:', dueTime, attachStr, title, cont)
    if gmCommand.isRawPlayer(playerEnt):
        _toGBID = gmCommand.fetchGbIdFromRawPlayer(playerEnt)
    else:
        _toGBID = playerEnt.gbID

    _toGBID = int(_toGBID)
    _attach = mailAssistor.parseAttachStr(attachStr)
    _title = title.strip("[] ")
    cont = cont.strip("[] ")
    mailAssistor.sendIDIPMailByGBID(superUser, _toGBID, dueTime, _attach, _title, cont, AAC_AACDD.datas.BONUS_SRC_GM, 0, ())
    return True, 'command success'

@gm_cmd('$sendB64MailByGBIDNoMailId', (Player("gbId or Id", raw=True), Int('dueTime'), Str('attachStr'), Str('title'), Str('cont')), RARG(0), BASE,
        '向指定玩家发送一封自定义邮件, base64编码', ALLSIDE, GOD_GROUPS)
def gm_sendB64MailByGBIDNoMailId(superUser, playerEnt, dueTime, attachStr, b64title, b64cont):
    LOG_DBG('sendB64MailByGBIDNoMailId:', dueTime, attachStr, b64title, b64cont)
    _title = base64.b64decode(b64title.encode('ascii'), b'_-').decode('utf-8')
    cont = base64.b64decode(b64cont.encode('ascii'), b'_-').decode('utf-8')
    LOG_DBG('sendMailByGBIDNoMailId:', attachStr, _title, cont)
    if gmCommand.isRawPlayer(playerEnt):
        _toGBID = gmCommand.fetchGbIdFromRawPlayer(playerEnt)
    else:
        _toGBID = playerEnt.gbID

    _toGBID = int(_toGBID)
    _attach = mailAssistor.parseAttachStr(attachStr)
    _title = _title.strip("[] ")
    cont = cont.strip("[] ")
    mailAssistor.sendIDIPMailByGBID(superUser, _toGBID, dueTime, _attach, _title, cont, AAC_AACDD.datas.BONUS_SRC_GM, 0, ())
    return True, 'command success'

@gm_cmd('$sendmailByAvatarId', (Str("str toId"), Int('mail id'), Int('due time'), Str('attachStr'), Str('despArgsStr'), Str('title'), Str('cont')),
        RSU, gameconst.BASE, '向指定玩家发一封邮件', INSIDE, GOD_GROUPS)
def gm_sendMailByAvatarId(superUser, toId, mailId, dueTime, attachStr, despArgsStr, title, cont):
    toId = int(toId)
    _attach = mailAssistor.parseAttachStr(attachStr)
    _despArgs = mailAssistor.parseDespStr(despArgsStr)
    if toId == 0:
        toId = superUser.id
    title = title.strip("[] ")
    cont = cont.strip("[] ")
    gameengine.broadcastBaseapp('gmSendMailByEntityId', (toId, mailId, dueTime, _attach, _despArgs, title, cont, AAC_AACDD.datas.BONUS_SRC_GM))
    return True, 'command success'

@gm_cmd('$sendglobalmail', (Int('mail id'), Str('attachStr'), Str('despArgs str'), Str('title'), Str('cont'), Int('minRoleTime'), Int('maxRoleTime'),
                            Int('dueTime'),Int('minRoleLevel'), Int('maxRoleLevel'), Int('channel'), Int("mailTag")),
        RONE, gameconst.BASE, '发一封全服邮件', ALLSIDE, GOD_GROUPS)
def gm_gmSendGlobalMail(superUser, mailId, attachStr, despArgsStr, title, cont, minRoleTime, maxRoleTime, dueTime, minRoleLevel, maxRoleLevel, channel, mailTag):
    # attachStr: 多个物品用分号';'分隔; 每个物品有itemId, itemNum，若有绑定属性配置在第三个位置，例如：[30000001,100; 30001031,1,1]
    _attach = mailAssistor.parseAttachStr(attachStr)
    despArgs = mailAssistor.parseDespStr(despArgsStr)
    title = base64.b64decode(title.encode('ascii'), b'_-').decode('utf-8')
    cont = base64.b64decode(cont.encode('ascii'), b'_-').decode('utf-8')
    gameengine.getGlobalBase('GlobalMailStub').sendGlobalMail(mailId, _attach, despArgs, title, cont, minRoleTime, maxRoleTime, 
                                                              dueTime, minRoleLevel, maxRoleLevel, channel, AAC_AACDD.datas.BONUS_SRC_GM, mailTag)
    return True, 'command success'

@gm_cmd('$getGlobalMailList', (Player("gbId or Id"), Int("int mailNum")), RSU, gameconst.BASE, '查看最近mailNum封全服邮件列表', INSIDE, GOD_GROUPS)
def gm_getGlobalMailList(superUser, playerEnt, mailNum):
    gameengine.getGlobalBase('GlobalMailStub').gmGetGlobalMailList(playerEnt, playerEnt._getChatChannelAvatarInfo(), mailNum)
    return True, 'command success'

@gm_cmd('$deleteGlobalMail', (Int("int mailGBID"), ), RSU, gameconst.BASE, '删除一封全服邮件', INSIDE, GOD_GROUPS)
def gm_delectGlobalMail(superUser, mailGBID):
    gameengine.getGlobalBase('GlobalMailStub').gmDeleteOneGlobalMail(mailGBID)
    return True, 'command success'

@gm_cmd('$sendBroadcast', (Int("int message id"), Str("str args")), RONE, gameconst.BASE, '发放公告', ALLSIDE, GOD_GROUPS,
        minArgs=1)
def gm_sendBroadcast(superUser, msgId, args):
    if args:
        gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onMessage', (msgId, args.split(','))))
    else:
        gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onMessage', (msgId, [])))
    return True, 'command success'


@gm_cmd('$officialMessage', (Int("int type"), Str("str content"), Int("int repeat count")), RONE, gameconst.BASE, '普通公告',
        ALLSIDE, GOD_GROUPS, minArgs=2)
def gm_officialMessage(superUser, type, content, repeatCnt):
    if not repeatCnt:
        repeatCnt = 1

    gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onOfficialMessage', (type, content, repeatCnt)))
    return True, 'command success'

@gm_cmd('$onEventTips', (Player("gbId or Id"),), RARG(0), BASE, 'eventTips', ALLSIDE, GOD_GROUPS)
def gm_gmOnEventTips(superUser, playerEnt):
    itemId = 30040001
    wealthVal = dropAward.AwardVal()
    wealthVal.addWealthByItemId(itemId, 1)
    awardCtx = awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID, eventTipId=10000002)
    _opUUID = KBEngine.genUUID64()
    srcType = 302
    detail = gameclass.AwardDetailCls(rankPos=1)
    playerEnt.addWealth(srcType, wealthVal, _opUUID, detail, awardCtx)


@gm_cmd('$onBroadAllEventTips',
        (Int("int itemId"), Int("int itemNum"), Int("int templateId"), Int("int srcType"), Str("str avatarName"), Str("str serverId")), RALL,
        BASE, '全服eventTips', ALLSIDE, GOD_GROUPS)
def gm_onBroadAllEventTips(superUser, itemId, itemNum, templateId, srcType, avatarName, serverId):
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
def gm_stopOfficialMessage(superUser):
    gameglobal.localBaseApp.stopOfficialMessage()
    return True, 'command success'


@gm_cmd('$enterline', (Player("gbId or Id"), Int("int lineType"),), RARG(0), gameconst.CELL, '进入分线', ALLSIDE, GOD_GROUPS)
def gm_enterLine(superUser, playerEnt, lineType):
    lineNo = formula.parseLineNo(playerEnt.spaceNo)
    pos, _ = utils.getPlayerBornInfo()
    if formula.fetchMapId(playerEnt.spaceNo) == lineType:
        return False, '执行失败'

    playerEnt.applyEnterLineInternal(lineType, lineNo, pos, playerEnt.direction, False)
    return True, 'command success'


@gm_cmd('$leaveline', (Player("gbId or Id"),), RARG(0), gameconst.CELL, '离开分线', ALLSIDE, GOD_GROUPS)
def gm_leaveLine(superUser, playerEnt):
    if formula.inWorldLineScene(playerEnt.spaceNo):
        return False, '不能离开大世界分线'

    lineType = formula.parseLineType(playerEnt.spaceNo)
    lineNo = random.randint(0, utils.fetchLineMaxNumber(lineType) - 1)
    pos = formula.getSpaceBornPoint(formula.combineLineSpaceNo(lineType, lineNo))
    if formula.fetchMapId(playerEnt.spaceNo) == lineType:
        return False, '执行失败'

    playerEnt.applyEnterLineInternal(lineType, lineNo, pos, playerEnt.direction, False)
    return True, 'command success'


@gm_cmd('$claimtask', (Player("gbId or Id"), Int('taskId'), Int('check')), RARG(0), BASE, '领取任务', ALLSIDE, GOD_GROUPS)
def gm_gmClaimTask(superUser, playerEnt, taskId, check):
    if taskId <= 0:
        return False, '执行失败， 任务id错误'
    import actionContext
    if check:
        playerEnt.cell.doStartClaimTask(taskId, '', (), actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrcEnum.TASK_SRC_GM))
    else:
        playerEnt.baseTaskClaim(taskId, actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrcEnum.TASK_SRC_GM), needCheck=False)
    return True, 'command success'


@gm_cmd('$submittask', (Player("gbId or Id"), Int('taskId'),), RARG(0), BASE, '提交任务', ALLSIDE, GOD_GROUPS)
def gm_gmSubmitTask(superUser, playerEnt, taskId):
    if taskId <= 0:
        return False, '执行失败, 任务ID错误'
    playerEnt.gmForceSubmitTask(taskId)
    return True, 'command success'


@gm_cmd('$resetTask', (Player("gbId or Id"), Int('taskId'),), RARG(0), BASE, '重置任务', ALLSIDE, GOD_GROUPS)
def gm_gmResetTask(superUser, playerEnt, taskId):
    if taskId <= 0:
        return False, '执行失败, 任务ID错误'
    playerEnt.gmResetTask(taskId)
    return True, 'command success'


@gm_cmd('$settaskstate', (Player("gbId or Id"), Int('taskId'), Int('state'), Int('child state')), RARG(0), BASE,
        '设置taskId及其子任务的状态', ALLSIDE, GOD_GROUPS, minArgs=3)
def gm_gmSetTaskState(superUser, playerEnt, taskId, state, childState=0):
    if taskId <= 0:
        return False, '执行失败, 任务ID错误'

    if state > gameconst.TaskStatEnum.TASK_STAT_QUIT:
        LOG_ERR('invalid task state', state)
        return False, '执行失败, 任务state错误'

    playerEnt.gmSetTaskState(taskId, state, childState)
    return True, 'command success'


@gm_cmd('$playcinema', (Player("gbId or Id"), Int('cinemaId'),), RARG(0), CELL, '播放剧情动画', ALLSIDE, GOD_GROUPS)
def gm_gmPlaycinema(superUser, playerEnt, cinemaId):
    playerEnt.prepareStartPlayCinema(cinemaId)
    return True, 'command success'


@gm_cmd('$addAllTitle', (Player("gbId or Id"),), RARG(0), BASE, '激活所有的称号', ALLSIDE, GOD_GROUPS)
def gm_addAllTitle(superUser, playerEnt):
    playerEnt.gmAddAllTitle()
    return True, 'command success'


@gm_cmd('$killent', (Player("gbId or Id"), Int('entityId'),), RARG(0), CELL, 'kill目标', ALLSIDE, GOD_GROUPS, minArgs=1)
def gm_killEnt(superUser, playerEnt, eid=0):
    eid = eid or playerEnt.selectedTargetId
    entity = KBEngine.entities.get(eid)
    if not entity or not entity.IsCombatUnit:
        return False, '%s不存在或者不是战斗单位' % eid

    entity.modifyHP(-entity.hp, playerEnt.id, gameconst.SourceType.SrcTpSkill, 0)
    return True, 'command success'


@gm_cmd('$destroyent', (Player("gbId or Id"), Int('entityId'),), RARG(0), CELL, '销毁目标', ALLSIDE, GOD_GROUPS,
        minArgs=1)
def gm_destroyEnt(superUser, playerEnt, eid=0):
    eid = eid or playerEnt.selectedTargetId
    entity = KBEngine.entities.get(eid)
    if not entity:
        return False, '%s不存在' % eid

    if entity.__class__.__name__ not in ('Space', 'Avatar', 'Account'):
        entity.safeDestroy()

    return True, 'command success'


@gm_cmd('$setcfg', (Str('name'), Str('value')), RONE, BASE, '修改数据库中的游戏开关配置', ALLSIDE, DEVE_GROUPS)
def gm_setGameConfig(superUser, name, val):
    # 这里输入的string 是经过xml转义的 &apos;是' &quot;是"
    if val == '&apos;&apos;' or val == '&quot;&quot;':
        _newValue = ''
    else:
        _newValue = val

    err, succ = gameconfig.gmSetCutomConfig(name, _newValue)
    if succ:
        return True, 'command success'
    return False, '执行失败：%s' % err


@gm_cmd('$getcfg', (Str('cfgName'),), RONE, BASE, '获取数据库中的游戏开关配置', ALLSIDE, DEVE_GROUPS)
def gm_getGameConfig(superUser, configName):
    value = gameconfig.gmGetCutomConfig(configName)

    return True, '执行成功：%s' % str(value)


@gm_cmd('$setcachecfg', (Str('name'), Str('val')), RONE, BASE, '修改xml中的配置的游戏开关配置.', ALLSIDE, DEVE_GROUPS)
def gm_setGameCacheConfig(superUser, name, value):
    # 这里输入的string 是经过xml转义的 &apos;是' &quot;是"
    if value == '&apos;&apos;' or value == '&quot;&quot;':
        newValue = ''
    else:
        newValue = value

    callOnApps(gameconst.BASE, 'gameconfig.setCacheConfig', (name, newValue))
    callOnApps(gameconst.CELL, 'gameconfig.setCacheConfig', (name, newValue))
    gameglobal.localBaseApp.notifyInterfaceCacheConfigChanged(name, value)

    if name == 'permitLogin':
        # permitLogin要更新redis
        key = gameconst.RedisKey.SERVER_OPEN_STATE + str(gameconfig.serverId())
        redisUtils.RedisUtils.cmdSet(key, str(newValue))
        LOG_INFO('update redis server open state: ', key, str(newValue))
    return True, 'command success'


@gm_cmd('$getcachecfg', (Str('cfgName'),), RONE, BASE, '读取xml中配置的游戏开关配置', ALLSIDE, DEVE_GROUPS)
def gm_getGameCacheConfig(superUser, cfgName):
    value = gameconfig.getCacheConfig(cfgName)
    return True, '执行成功：%s' % str(value)


@gm_cmd('$gmCleanAllTasks', (Player("gbId or Id"),), RARG(0), BASE, '清除身上所有任务', ALLSIDE, GOD_GROUPS)
def gm_gmCleanAllTasks(superUser, playerEnt):
    import tutorConst_guideConfig as TCGCD
    playerEnt.taskInfo.tasks.clear()
    playerEnt.taskInfo.taskRecordDic.clear()
    playerEnt.newbieStep = TCGCD.datas['firstStep']['value']
    playerEnt.gmFinishedNewbie(0)
    return True, 'command success'


@gm_cmd('$botFinishNewbie', (Player("gbId or Id"),), RARG(0), BASE, '机器人完成新手', ALLSIDE, GOD_GROUPS)
def gm_botFinishNewbie(superUser, playerEnt):
    playerEnt.gmBotFinishedNewbie()
    return True, 'command success'


@gm_cmd('$findEntity', (Int('entityId'),), RONE, CELL, '实体所在进程', ALLSIDE, GOD_GROUPS)
def gm_findEntity(superUser, eid):
    forwardGMCommand(superUser, '$_findEntity-cell', eid)
    forwardGMCommand(superUser, '$_findEntity-base', eid)


@gm_cmd('$_findEntity-cell', (Int('entityId'),), RALL, CELL, '实体所在进程', ALLSIDE, GOD_GROUPS)
def gm_findEntityCell(superUser, eid):
    import utils
    entity = KBEngine.entities.get(eid)
    if not entity:
        return

    processIp = utils.getPythonAddr()
    return True, 'findEntity-cell执行成功,进程IP：cellapp{:0>2}-{}'.format(KBEngine.getComponentGroupOrder(), processIp)


@gm_cmd('$_findEntity-base', (Int('entityId'),), RALL, BASE, '实体所在进程', ALLSIDE, GOD_GROUPS)
def gm_findEntityBase(superUser, eid):
    import utils
    entity = KBEngine.entities.get(eid)
    if not entity:
        return

    processIp = utils.getPythonAddr()
    return True, 'findEntity base执行成功,进程IP：baseapp{:0>2}-{}'.format(KBEngine.getComponentGroupOrder(), processIp)


@gm_cmd('$findStub', (Str('stub name'),), RONE, BASE, 'stub所在de进程', ALLSIDE, GOD_GROUPS)
def gm_findStub(superUser, stubName):
    forwardGMCommand(superUser, '$_findStub-base', stubName)


@gm_cmd('$_findStub-base', (Str('stub name'),), RALL, BASE, 'stub所在进程', ALLSIDE, GOD_GROUPS)
def gm_findStubBase(superUser, stubName):
    import utils

    _baseStub = gameengine.getGlobalBase(stubName)

    if isinstance(_baseStub, (utils.Swallower,)):
        return
    else:
        entity = KBEngine.entities.get(_baseStub.id)
        if not entity:
            return

        processIp = utils.getPythonAddr()
        return True, '执行成功 进程IP：baseapp{:0>2}-{}，stub id ：{}'.format(KBEngine.getComponentGroupOrder(), processIp,
                                                                           _baseStub.id)


@gm_cmd('$getlinest', (Int('lineType'),), RONE, BASE, '获取分线line状态', ALLSIDE, GOD_GROUPS)
def gm_getlinest(superUser, lineType):
    forwardGMCommand(superUser, '$_getlinest-base', lineType)


@gm_cmd('$_getlinest-base', (Int('lineType'),), RALL, BASE, '获取分线状态', INSIDE, GOD_GROUPS)
def gm_getlinestBase(superUser, lineType):
    import utils

    _line = gameengine.getLineStub(lineType)
    if isinstance(_line, (utils.Swallower,)):
        return
    else:
        entity = KBEngine.entities.get(_line.id)
        if not entity:
            return
        else:
            _sum = 0
            result = ''
            for key, value in entity.allPlayers.items():
                _sum += len(value)
                result += ('%s线有%d人，' % (key, len(value)))

            return True, '执行成功,%s共有%d人' % (result, _sum)


@gm_cmd('$me', (Player('playerEnt id'),), RARG(0), CELL, '获取玩家自己信息', ALLSIDE, GOD_GROUPS)
def gm_me(superUser, entity):
    import utils

    processIp = utils.getPythonAddr()
    playerName = entity.name
    playerId = entity.id
    playerGbId = entity.gbId
    playerSchool = entity.school
    playerSelectedTargetId = entity.selectedTargetId

    return True, '执行成功,name:{},gbId:{},id:{},school:{},selectedTargetId:{},进程IP:cellapp{:0>2}-{} base:{}'.format(
        playerName, playerGbId, playerId, playerSchool, playerSelectedTargetId, KBEngine.getComponentGroupOrder(),
        processIp, entity.base)


@gm_cmd('$findavatar', (Player("gbId or Id"),), RARG(0), CELL, '通过玩家名字找到avatar', ALLSIDE, GOD_GROUPS)
def gm_findavatar(superUser, playerEnt):
    import utils

    processIp = utils.getPythonAddr()
    playerName = playerEnt.name
    playerId = playerEnt.id
    playerGbId = playerEnt.gbId
    playerSchool = playerEnt.school
    playerSpaceNo = playerEnt.spaceNo
    playerSelectedTargetId = playerEnt.selectedTargetId

    return True, '{}:{}:{},school:{},selectId:{},spaceNo:{},cellapp:{:0>2}-{} base:{}'.format(
        playerName, playerGbId, playerId, playerSchool, playerSelectedTargetId, playerSpaceNo,
        KBEngine.getComponentGroupOrder(), processIp, playerEnt.base)


@gm_cmd('$findclient', (Player("gbId or Id"),), RARG(0), BASE, '查看client', ALLSIDE, GOD_GROUPS)
def gm_findClient(superUser, playerEnt):
    return True, 'client:{}'.format(playerEnt.client)


@gm_cmd('$getpropCell', (Entity('entity'), Str("str propName")), RARG(0), CELL, '输出CELL实体属性值', ALLSIDE, GOD_GROUPS)
def gm_getpropCell(superUser, ent, propname):
    if not hasattr(ent, propname):
        return

    superUser.feedbackCommandSucc('执行成功,[{}]:[{}]'.format(propname, str(getattr(ent, propname, ''))))


@gm_cmd('$getpropBase', (Entity('entity'), Str("str propName")), RARG(0), BASE, '输出BASE实体属性值', ALLSIDE, GOD_GROUPS)
def gm_getpropBase(superUser, ent, propName):
    if not hasattr(ent, propName):
        return

    superUser.feedbackCommandSucc('执行成功,{}:{}'.format(propName, str(getattr(ent, propName, ''))))

@gm_cmd('$statAvatarNum', (), RALL, ALL, '统计Avatar数量', ALLSIDE, GOD_GROUPS)
def gm_statAvatarNum(superUser):
    componentNo = KBEngine.getComponentGroupOrder()
    avatarNumber = len(utils.getEntityList('Avatar'))
    if IS_BASE:
        superUser.feedbackCommandSucc('执行成功,baseapp{:0>2}:{}'.format(componentNo, avatarNumber))
    else:
        superUser.feedbackCommandSucc('执行成功,cellapp{:0>2}:{}'.format(componentNo, avatarNumber))
    return


@gm_cmd('$_statAvatarNum-cell', (), RALL, CELL, '统计Avatar数量', ALLSIDE, GOD_GROUPS)
def gm_statAvatarNumCell(superUser):
    componentNo = KBEngine.getComponentGroupOrder()
    baseAppNum = gameconfig.baseAppCount()
    delayTime = baseAppNum * 5 + componentNo * 2

    def _delayStatAvarNumCell(superUser):
        avatarNumber = len(utils.getEntityList('Avatar'))
        superUser.feedbackCommandSucc('执行成功,cellapp{:0>2}:{}'.format(componentNo, avatarNumber))

    KBEngine.addTimer(delayTime, 0, lambda timeId: _delayStatAvarNumCell(superUser))


@gm_cmd('$_statAvatarNum-base', (), RALL, BASE, '统计Avatar数量', ALLSIDE, GOD_GROUPS)
def gm_statAvatarNumBase(superUser):
    componentNo = KBEngine.getComponentGroupOrder()
    delayTime = componentNo

    def _delayStatAvarNumBase(superUser):
        avatarNumber = len(utils.getEntityList('Avatar'))
        superUser.feedbackCommandSucc('执行成功,baseapp{:0>2}:{}'.format(componentNo, avatarNumber))

    KBEngine.addTimer(delayTime, 0, lambda timerId: _delayStatAvarNumBase(superUser))


@gm_cmd('$spaceWeightStat', (), RALL, CELL, 'spaceWeight统计', ALLSIDE, GOD_GROUPS)
def gm_spaceWeightStat(superUser):
    _spaceList = utils.getEntityList('Space')
    totalWeight = 0
    _spaceDic = {}
    for _spaceEntity in _spaceList:
        spaceWeight = _spaceEntity.getSpaceWeight(_spaceEntity.spaceID)
        totalWeight += spaceWeight
        mapId = formula.fetchMapId(_spaceEntity.spaceNo)
        _spaceDic.setdefault(mapId, 0)
        _spaceDic[mapId] += spaceWeight

    superUser.feedbackCommandSucc(
        '执行成功,cellapp{:0>2}:{},total:{}'.format(KBEngine.getComponentGroupOrder(), str(_spaceDic), totalWeight))


@gm_cmd('$doEval', (Str("str compGroupOrder"), Str("str evalStr"),), RONE, BASE, 'eval', ALLSIDE, GOD_GROUPS)
def gm_doEval(superUser, compGroupOrder, evalStr):
    forwardGMCommand(superUser, '$_doEval-cell', compGroupOrder, evalStr)
    forwardGMCommand(superUser, '$_doEval-base', compGroupOrder, evalStr)
    return


@gm_cmd('$_doEval-cell', (Str("str compGroupOrder"), Str("str evalStr"),), RALL, CELL, 'eval', ALLSIDE, GOD_GROUPS)
def gm_doEvalCell(superUser, compGroupOrder, evalStr):
    LOG_DBG('cellapp{:0>2}'.format(KBEngine.getComponentGroupOrder()))
    if 'cellapp{:0>2}'.format(KBEngine.getComponentGroupOrder()) == compGroupOrder:
        result = str(eval(evalStr))
        superUser.feedbackCommandSucc('执行成功,{}'.format(result))


@gm_cmd('$_doEval-base', (Str("str compGroupOrder"), Str("str evalStr"),), RALL, BASE, 'eval', ALLSIDE, GOD_GROUPS)
def gm_doEvalBase(superUser, compGroupOrder, evalStr):
    LOG_DBG('BASEAPP{:0>2}'.format(KBEngine.getComponentGroupOrder()))
    if 'baseapp{:0>2}'.format(KBEngine.getComponentGroupOrder()) == compGroupOrder:
        result = str(eval(evalStr))
        superUser.feedbackCommandSucc('执行成功,{}'.format(result))


@gm_cmd('$switchline', (Player("gbId or Id"), Int('lineNo')), RARG(0), CELL, '切换分线', ALLSIDE, GOD_GROUPS)
def gm_switchline(superUser, playerEnt, lineNo):
    playerEnt.applySwitchLine(playerEnt.id, lineNo)
    return True, 'command success'


@gm_cmd('$setgmgroup', (Player("gbId or Id", raw=True), Int('group')), RARG(0), BASE, '设置gm组', ALLSIDE, GOD_GROUPS)
def gm_setgmgroup(superUser, playerEnt, group):
    if gmCommand.isRawPlayer(playerEnt):
        sql = "update tbl_Avatar set sm_gmGroup = %d where sm_gbID =%s" % (
            group, gmCommand.fetchGbIdFromRawPlayer(playerEnt))
        KBEngine.executeRawDatabaseCommand(sql)
    else:
        playerEnt.gmGroup = group
    return True, 'command success'


@gm_cmd('$loadentity', (Player('playerEnt id'), Str('class name'), Int('object id'), Int('entityId'), Int('num')),
        RARG(0), CELL, '创建entity实体', ALLSIDE, GOD_GROUPS)
def gm_loadentity(superUser, playerEnt, className, objId, entityId, num):
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

    _bornPosition = tuple(playerEnt.position)

    _bornDirection = tuple(playerEnt.direction)

    tmpProps = {}
    params = {
        'spaceNo': playerEnt.spaceNo,
        'direction': _bornDirection,
        'position': _bornPosition,
        'spaceno': playerEnt.spaceNo,
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

        for i in utils.genGameEntityId(entityId, count_):
            params.update({
                'gameEntityId': i,
            })
            gid, gct = utils.splitFromGameEntityId(i)
            tmpProps['createIndex'] = gct
            playerEnt.base.callMethod('gmCreateEntityHasBase', (className, params))

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
        for i in utils.genGameEntityId(entityId, count_):
            params.update({
                'gameEntityId': i,
            })
            gid, gct = utils.splitFromGameEntityId(i)
            tmpProps['createIndex'] = gct
            # KBEngine.createEntityLocally(className, params)
            playerEnt.base.callMethod('gmCreateEntityHasBase', (className, params))

        flag = '执行Collection'

    return True, '执行成功,' + flag


@gm_cmd('$delentity', (Int('entityId'),), RSU, CELL, '删除实体', INSIDE, GOD_GROUPS)
def gm_delentity(superUser, entityId):
    for entity in KBEngine.entities.values():
        if hasattr(entity, 'gameEntityId'):
            if entityId == utils.parseGidFromGameEntityId(entity.gameEntityId):
                entity.safeDestroy()

    return True, 'command success'


@gm_cmd('$modifyServertime', (Str('modifyTime'),), RONE, BASE, '修改服务器时间', ALLSIDE, GOD_GROUPS)
def gm_modifyServertime(superUser, modifyTime):
    if KBEngine.publish():
        return False, 'modify on dev only'
    if '.' and '-' not in modifyTime:
        return False, '时间格式错误'
    forwardGMCommand(superUser, '$modifyServertime-cell', modifyTime)
    forwardGMCommand(superUser, '$modifyServertime-base', modifyTime)
    return True, '$modifyServertime执行成功'

@gm_cmd('$advanceServertime', (Int('days'), Int('hours'), Int('minutes')), RONE, BASE, '推进服务器时间(天/时/分)', ALLSIDE, GOD_GROUPS)
def gm_advanceServertime(superUser, days, hours, minutes):
    if KBEngine.publish():
        return False, 'modify on dev only'
    deltaSeconds = days * 86400 + hours * 3600 + minutes * 60
    if deltaSeconds <= 0:
        return False, '推进时间必须大于0'
    forwardGMCommand(superUser, '$advanceServertime-cell', deltaSeconds)
    forwardGMCommand(superUser, '$advanceServertime-base', deltaSeconds)
    return True, '$advanceServertime执行成功，推进%d天%d时%d分' % (days, hours, minutes)

@gm_cmd('$advanceServertime-cell', (Int('deltaSeconds'),), RALL, CELL, '推进服务器时间', ALLSIDE, GOD_GROUPS)
def gm_advanceServertimeCell(superUser, deltaSeconds):
    LOG_DBG('advanceServertimeCell', deltaSeconds)
    import time
    _currentTempTime = utils.tempTime
    utils.tempTime = lambda: _currentTempTime() + deltaSeconds
    time.time = utils.tempTime

@gm_cmd('$advanceServertime-base', (Int('deltaSeconds'),), RALL, BASE, '推进服务器时间', ALLSIDE, GOD_GROUPS)
def gm_advanceServertimeBase(superUser, deltaSeconds):
    LOG_DBG('advanceServertimeBase', deltaSeconds)
    import time
    _currentTempTime = utils.tempTime
    utils.tempTime = lambda: _currentTempTime() + deltaSeconds
    time.time = utils.tempTime

@gm_cmd('$modifyAllServertimeInCrossGroup', (Str('modifyTime'),), RONE, BASE, '修改跨服组服务器时间', ALLSIDE, GOD_GROUPS)
def gm_modifyAllServertimeInCrossGroup(superUser, modifyTime):
    if KBEngine.publish():
        return False, 'modify on dev only'
    LOG_DBG("modifyAllServertimeInCrossGroup", modifyTime)
    import iRouter
    _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossServerStub')
    _stub.onGmModifyAllServertimeInCrossGroup(superUser, modifyTime)
    return True, '$modifyServertime执行成功'


@gm_cmd('$modifyServertime-cell', (Str('modifyTime'),), RALL, CELL, '修改服务器de时间', ALLSIDE, GOD_GROUPS)
def gm_modifyServertimeCell(superUser, modifyTime):
    LOG_DBG('modifyServertime of cell')
    import datetime
    import time

    time.time = utils.tempTime

    _format = "%Y.%m.%d-%H.%M.%S"
    _mtime = datetime.datetime.strptime(modifyTime, _format)
    _nowDatetime = datetime.datetime.fromtimestamp(time.time())
    _timeDelta = (_mtime - _nowDatetime).total_seconds()
    utils.tempTime = time.time
    time.time = lambda: utils.tempTime() + _timeDelta

@gm_cmd('$modifyServertime-base', (Str('modifyTime'),), RALL, BASE, '修改服务器de时间', ALLSIDE, GOD_GROUPS)
def gm_modifyServertimeBase(superUser, modifyTime):
    LOG_DBG('modifyServertimeBase')
    import datetime
    import time

    time.time = utils.tempTime

    _format = "%Y.%m.%d-%H.%M.%S"
    _mtime = datetime.datetime.strptime(modifyTime, _format)
    _nowDatetime = datetime.datetime.fromtimestamp(time.time())
    timeDelta = (_mtime - _nowDatetime).total_seconds()
    utils.tempTime = time.time
    time.time = lambda: utils.tempTime() + timeDelta


@gm_cmd('$getServertime', (Player('gbId or Id'),), RARG(0), BASE, '获取服务器时间', ALLSIDE, GOD_GROUPS)
def gm_getServertime(superUser,playerEnt):
    if gmCommand.isRawPlayer(playerEnt):
        return False, '执行失败'
    LOG_DBG('getServertime')
    import time
    import datetime
    timestamp = time.time()
    _dateObject = datetime.datetime.fromtimestamp(timestamp)
    _format = "%Y.%m.%d-%H.%M.%S"
    _timeStr = _dateObject.strftime(_format)
    superUser.onCommandResult(0, _timeStr, {})
    return True, '%s' % _timeStr


@gm_cmd('$recoverServertime', (), RONE, BASE, '恢复服务器时间', ALLSIDE, GOD_GROUPS)
def gm_recoverServertime(superUser):
    forwardGMCommand(superUser, '$recoverServertime-cell')
    forwardGMCommand(superUser, '$recoverServertime-base')
    return True, 'recoverServertime执行成功'


@gm_cmd('$recoverServertime-cell', (), RALL, CELL, '恢复服务器时间', ALLSIDE, GOD_GROUPS)
def gm_recoverServertimeCell(superUser):
    LOG_DBG('recoverServertimeCell')
    import time
    time.time = utils.tempTime


@gm_cmd('$recoverServertime-base', (), RALL, BASE, '恢复服务器de时间', ALLSIDE, GOD_GROUPS)
def gm_recoverServertimeBase(superUser):
    LOG_DBG('recoverServertimeBase')
    import time
    time.time = utils.tempTime


@gm_cmd('$onlinenum', (), RSTUB('PlayerStub'), BASE, '获取在线人数', ALLSIDE, GOD_GROUPS)
def gm_getOnlineNum(superUser, playerStub):
    return True, '%s' % playerStub.getOnlineNum()


@gm_cmd('$showmsg', (Player("gbId or Id"), Int('msg id'), Str('模板参数arg'), Str('分隔符', default='|')), RARG(0),
        gameconst.BASE, '发送测试msg到客户端', ALLSIDE, DEVE_GROUPS, minArgs=2)
def gm_showClientMsg(superUser, playerEnt, msgId, argStr: str, seperator):
    if argStr:
        _args = argStr.split(seperator)
    else:
        _args = list(['参数%i' % i for i in range(4)])
    print('showClientMsg', msgId, _args, playerEnt, playerEnt.id)
    playerEnt.onMessagePre(msgId, _args)
    return True, 'command success'


@gm_cmd('$exportAvatarData', (Player("gbId or Id"), Int('serverId'), Str('playerName')), RARG(0), CELL, '导出数据',
        ALLSIDE, GOD_GROUPS)
def gm_exportAvatarData(superUser, playerEnt, serverId, playerName):
    blacklistPro = ['brothersList', 'coinAuctionInfo', 'friendsInfo', 'marriage', 'moneyAuctionInfo']
    persistProList = KBEngine.getPersistentProperties('Avatar')
    avatarDict = playerEnt.__dict__
    _postDataDict = {}
    for proKey, avatarPro in avatarDict.items():
        if proKey in persistProList and proKey not in blacklistPro:
            _postDataDict[proKey] = avatarPro

    playerEnt.base.postAvatarProp(_postDataDict, blacklistPro, persistProList, serverId, playerName)

    return True, 'command success'


@gm_cmd('$importAvatar', (Int("int targetAvatarGbId"), Str("str accountName"),), RONE, BASE, '导入角色', ALLSIDE, GOD_GROUPS)
def gm_importAvatar(superUser, targetAvatarGbId, accountName):
    import const_const

    def _innerFunc(result, rows, insertid, error):
        if len(result) == 1 and not result[0][1]:
            _characterNum = 0
        elif len(result) > 0:
            _characterNum = len(result)
        else:
            superUser.feedbackCommandFail("账号不存在，do failed")
            return

        maxChars = const_const.datas.get('createConst_CharLimit', {}).get('value', 3)
        if _characterNum >= min(maxChars, 4):
            superUser.feedbackCommandFail("角色列表已满，do failed")
            return

        gamesql.updateCharacterParentID(accountName, targetAvatarGbId)
        superUser.feedbackCommandSucc("do success")

    gamesql.countCharacterNum(accountName, _innerFunc)


# 测试专用GM 测试后删除
@gm_cmd('$testAccountGM', (PlayerAccount("accountName"),), RONE, BASE, '测试账号GM', ALLSIDE, GOD_GROUPS)
def gm_testAccountGM(superUser, account):
    LOG_DBG("testAccountGM", account)
    return True, 'command success'


@gm_cmd('$getaccountinfo', (Player("gbId or Id", raw=True),), RARG(0), BASE, '获取角色的账号信息', ALLSIDE, GOD_GROUPS)
def gm_getAccountInfo(superUser, playerEnt):
    if gmCommand.isRawPlayer(playerEnt):
        gbId = gmCommand.fetchGbIdFromRawPlayer(playerEnt)
        _accSql = 'select ta.sm_accountType from tbl_Account as ta,tbl_Account_characters_characters as tacc where ta.id=tacc.parentID and tacc.sm_gbId={}'.format(gbId)
        _sql = "select accType.sm_accountType, ta.sm_accountName from tbl_Avatar as ta, ({}) as accType where ta.sm_gbID ={}".format(
            _accSql, gbId)
        KBEngine.executeRawDatabaseCommand(_sql,
                                           lambda ret, num, insertId, err: _onGetAccountInfo(ret, num, insertId, err,
                                                                                             superUser))
    else:
        return True, "玩家账号类型：%s, 账号名：%s" % (playerEnt.accountEntity.accountType, playerEnt.accountName)


def _onGetAccountInfo(ret, num, insertId, err, superUser):
    if err:
        LOG_ERR('get account info err:', err)
        return

    _accoutType, accountName = ret[0]
    _accoutType = _accoutType.decode('utf-8')
    _accountName = _accountName.decode('utf-8')
    superUser.feedbackCommandSucc("玩家账号类型：%s, 账号名：%s" % (_accoutType, _accountName))


@gm_cmd('$paotu', (Player("gbId or Id"), Int('rideFlag'), Int('pathId')), RARG(0), CELL, '跑图', ALLSIDE, GOD_GROUPS)
def gm_paotu(superUser, playerEnt, rideFlag, pathId):
    import path_path

    if rideFlag:
        playerEnt.enterRiding(playerEnt.id, False)
    else:
        playerEnt.exitRiding(playerEnt.id)
    firstPosition = path_path.datas[pathId]['pointList'][0]
    playerEnt.position = firstPosition
    playerEnt.addTimerCB(5, 'setRoute', (pathId,), gametimer.TIMER_TAG_SET_ROUTE)
    return True, 'command success'


@gm_cmd('$checkRandomNameZk', (), RONE, BASE, '随机姓名检测字库', ALLSIDE, GOD_GROUPS)
def gm_checkRandomNameZk(superUser):
    import randomName_playerName as RNP
    import validate_chars

    _surnamesList = RNP.datas.get('surname')
    _femaleNameList = RNP.datas.get('femaleName')
    _maleNameList = RNP.datas.get('maleName')
    _nameList = _maleNameList + _femaleNameList

    ilegalList = []
    _charSet = set()

    for _surname in _surnamesList:
        for name in _nameList:
            nameSet = set(_surname + name)
            _charSet = _charSet | nameSet

    for char in _charSet:
        if not validate_chars.RE_VALIDATE_SPECIAL_COMPILE.fullmatch(char):
            ilegalList.append(char)

    superUser.feedbackCommandSucc("随机玩家非法字库列表：{}".format(ilegalList))

    return True, 'command success'


@gm_cmd('$checkRandomBotNameZk', (), RONE, BASE, '随机机器人姓名检测字库', ALLSIDE, GOD_GROUPS)
def gm_checkRandomBotNameZk(superUser):
    import randomName_robotName as RNR
    import validate_chars

    _surnamesList = RNR.datas.get('surname')
    _femaleNameList = RNR.datas.get('femaleName')
    _maleNameList = RNR.datas.get('maleName')
    _nameList = _maleNameList + _femaleNameList

    ilegalList = []
    charSet = set()

    for _surname in _surnamesList:
        for name in _nameList:
            nameSet = set(_surname + name)
            charSet = charSet | nameSet

    for _char in charSet:
        if not validate_chars.RE_VALIDATE_SPECIAL_COMPILE.fullmatch(_char):
            ilegalList.append(_char)

    superUser.feedbackCommandSucc("随机机器人非法字库列表：{}".format(ilegalList))

    return True, 'command success'


@gm_cmd('$gmBlockExposedMethod', (Int('isAdd'), Str('funcName'), Int('msg id')), RONE, BASE, '禁止对外接口', ALLSIDE,
        GOD_GROUPS)
def gm_gmBlockExposedMethod(superUser, isAdd, method, msgId):
    gameengine.callAllApps('gameengine.modifyGlobalExposedFunc', (isAdd, method, msgId))
    return True, 'command success'


@gm_cmd('$gmAutoRunTask', (Player("gbId or Id"), Int('taskId')), RARG(0), BASE, '自动进行任务', ALLSIDE, GOD_GROUPS)
def gm_gmAutoRunTask(superUser, playerEnt, taskId):
    playerEnt.gmAutoRunTask(taskId)
    return True, 'command success'

@gm_cmd('$getItemUniqueId', (Player("gbId or Id"), Int('itemId'),), RONE, BASE, 'get item uniqueId', ALLSIDE, GOD_GROUPS)
def gm_getItemUniqueId(superUser, playerEnt, itemId):
    uId = playerEnt.getItemUniqueId(itemId)
    return True, '' + str(uId)


@gm_cmd('$gmSignIn', (Player("gbId or Id"), Int('activityId'),), RONE, BASE, 'sign in', ALLSIDE, GOD_GROUPS)
def gm_gmSignIn(superUser, playerEnt, aId):
    playerEnt.reqSignInfo(aId)
    playerEnt.reqSignIn(aId)
    return True, 'command success'


@gm_cmd('$offline', (Player("entityId"),), RARG(0), CELL, 'offline', ALLSIDE, GOD_GROUPS)
def gm_gmOffline(superUser, playerEnt):
    playerEnt.offline(playerEnt.id, gameconst.OFFLINE_REASON_MANNUALLY)
    return True, 'command success'


@gm_cmd('$modifyName', (Player("gbId or Id", raw=True), Str('newName')), RARG(0), BASE, '改名', ALLSIDE, GOD_GROUPS)
def gm_modifyName(superUser, playerEnt, newName):
    if gmCommand.isRawPlayer(playerEnt):
        gbId, name, accountName, dbId = playerEnt
        gamesql.recordAvatarOfflineCallback(gbId, 'IDIPModifyName', (newName,))
    else:
        playerEnt.IDIPModifyName(newName)
    return True, 'command success'

@gm_cmd('$modifyscore', (Player("gbId or Id", raw=True), Int('newScore')), RARG(0), CELL, '修改战力', ALLSIDE, GOD_GROUPS)
def gm_modifyscore(superUser, playerEnt, newScore):
    playerEnt._changeScore("rewardFightProp", newScore)
    return True, 'command success'



@gm_cmd('$modifyNameByItem', (Player("entityId"), Str('newName'), Int("int gridId")), RARG(0), CELL, '道具改名', ALLSIDE,
        GOD_GROUPS)
def gm_modifyNameByItem(superUser, playerEnt, newName, gridId):
    itemId = 30010100
    playerEnt.reqUseItems(playerEnt.id, 0, gridId, itemId, None, 1, [newName, ])
    return True, 'command success'


@gm_cmd('$testPickupExtractItem',
        (Player("gbId or Id", raw=True), Int('boxId'), Int('boxNum'), Int('tarNum'), Int('fillId')), RARG(0), BASE,
        '拆解奖励接口测试', ALLSIDE, GOD_GROUPS)
def gm_testPickupExtractItem(superUser, playerEnt, boxId, boxNum, tarNum, fillId):
    LOG_DBG('GM testPickupExtractItem~')
    itemGroup = playerEnt.pickExtractItems(boxId, boxNum, tarNum, fillId, dataUtils.getItemDefaultBindType())
    return True, '执行成功_%s' % str(itemGroup)


@gm_cmd('$deleteAvatar', (Player("gbId"),), RARG(0), BASE, 'set did limit', ALLSIDE, GOD_GROUPS)
def gm_deleteAvatar(superUser, playerEnt):
    playerEnt.reqDeleteAvatar()




@gm_cmd('$addPlayerCalendarPoint', (Player("gbId"), Int('point'),), RARG(0), BASE, 'add playerEnt calendar point', ALLSIDE,
        GOD_GROUPS)
def gm_addPlayerCalendarPoint(superUser, playerEnt, point):
    playerEnt.calendarPoint += point
    return True, 'command success'


@gm_cmd('$setforbiddenflag', (Player("gbId or Id", raw=True), Int('flagType'), Int('forbiddenTime'), Str('reason')),
        RARG(0), BASE, '封禁指定功能', ALLSIDE, GOD_GROUPS)
def gm_setForbiddenFlag(superUser, playerEnt, forbiddenType, forbidTime, reason):
    tEnd = utils.curTS() + forbidTime
    if gmCommand.isRawPlayer(playerEnt):
        gbId, name, accountName, dbId = playerEnt
        gamesql.recordAvatarOfflineCallback(gbId, 'setForbiddenFlag', (forbiddenType, (tEnd, reason)))
    else:
        playerEnt.setForbiddenFlag(forbiddenType, (tEnd, reason))

    superUser.onCommandResult(0, '', {})
    return True, 'command success'


@gm_cmd('$addWPWhiteList', (Player("gbId or Id", raw=True),), RARG(0), BASE, '添加白名单', ALLSIDE, GOD_GROUPS)
def gm_addWPWhiteList(superUser, playerEnt):
    if not gmCommand.isRawPlayer(playerEnt):
        playerGbId = playerEnt.gbID
        isOffline = False
    else:
        playerGbId, *_ = playerEnt
        isOffline = True

    def _onAdd(success, value):
        if success:
            superUser.onCommandResult(0, '', {})
        else:
            valueStr = ','.join(value)
            superUser.onCommandResult(gameconst.GMCommandErr.GM_RET_REDIS_OP_ERR, '', {"values": valueStr})

    def _onOfflineSetWpList(ret, num, insertId, err):
        if not err:
            gbIds = [playerGbId, ]
            redisUtils.SetUtils.sadd(gameconst.RedisKey.WP_WHITE_LSIT_KEY, gbIds, _onAdd)
        else:
            LOG_INFO("_onOfflineSetWpList failed", ret, num, err, playerGbId)
            superUser.onCommandResult(gameconst.GMCommandErr.GM_RET_DB_OP_ERR, '', {})

    if isOffline:
        sql = f'update tbl_Avatar set sm_isWpWhiteList=1 where sm_gbID={playerGbId}'
        KBEngine.executeRawDatabaseCommand(sql,
                                           lambda ret, num, insertId, err: _onOfflineSetWpList(ret, num, insertId, err))
    else:
        playerEnt.isWpWhiteList = 1
        gbIds = [playerGbId, ]
        redisUtils.SetUtils.sadd(gameconst.RedisKey.WP_WHITE_LSIT_KEY, gbIds, _onAdd)


@gm_cmd('$remWPWhiteList', (Player("gbId or Id", raw=True),), RARG(0), BASE, '删除白名单', ALLSIDE, GOD_GROUPS)
def gm_remWPWhiteList(superUser, playerEnt):
    if not gmCommand.isRawPlayer(playerEnt):
        playerGbId = playerEnt.gbID
        isOffline = False
    else:
        playerGbId, *_ = playerEnt
        isOffline = True

    def _onDel(success, value):
        if success:
            superUser.onCommandResult(0, '', {})
        else:
            superUser.onCommandResult(gameconst.GMCommandErr.GM_RET_REDIS_OP_ERR, '', {"values": str(value)})

    def _onOfflineDelWpList(ret, num, insertId, err):
        LOG_INFO('_onOfflineDelWpList', ret, num, err)
        if not err:
            redisUtils.SetUtils.srem(gameconst.RedisKey.WP_WHITE_LSIT_KEY, playerGbId, _onDel)
        else:
            LOG_INFO("_onOfflineDelWpList failed", ret, num, err, playerGbId)
            superUser.onCommandResult(gameconst.GMCommandErr.GM_RET_DB_OP_ERR, '', {})

    if isOffline:
        sql = f'update tbl_Avatar set sm_isWpWhiteList=0 where sm_gbID={playerGbId}'
        LOG_INFO('_onOfflineDelWpList', sql)
        KBEngine.executeRawDatabaseCommand(sql,
                                           lambda ret, num, insertId, err: _onOfflineDelWpList(ret, num, insertId, err))
    else:
        playerEnt.isWpWhiteList = 0
        redisUtils.SetUtils.srem(gameconst.RedisKey.WP_WHITE_LSIT_KEY, playerGbId, _onDel)


@gm_cmd('$queryWPWhiteList', (), RONE, BASE, '查询白名单', ALLSIDE, GOD_GROUPS)
def gm_queryWPWhiteList(superUser):
    def _onLoadAll(success, values):
        if success:
            valuesStr = ','.join(values)
            superUser.onCommandResult(0, '', {"values": valuesStr})
        else:
            superUser.onCommandResult(gameconst.GMCommandErr.GM_RET_REDIS_OP_ERR, '', {})

    redisUtils.SetUtils.loadAllFromRedis(gameconst.RedisKey.WP_WHITE_LSIT_KEY, _onLoadAll)

@gm_cmd('$queryChatForbidden', (Player("gbId or Id", raw=True),), RARG(0), BASE, '查询聊天禁止', ALLSIDE, GOD_GROUPS)
def gm_queryChatForbidden(superUser, playerEnt):
    # 离线玩家处理
    if gmCommand.isRawPlayer(playerEnt):
        gbId, name, accountName, dbId = playerEnt
        LOG_INFO(f"gm offline queryChatForbidden, gbID:{gbId}")

        def onGetForbiddenInfo(ret, num, insertId, err, superUser, gbId):
            if err:
                superUser.onCommandResult(gameconst.ChatSysGMErr.DBERR, '',
                                   {'gbId': gbId, 'isOffline': True, 'forbiddenExpireTime': 0, 'forbiddenCount': 0})
                LOG_ERR("gm offline queryChatForbidden fail, ", gbId, num, insertId, err)
            else:
                forbiddenExpireTime = int(ret[0][0].decode())
                forbiddenCount = int(ret[0][1].decode())
                superUser.onCommandResult(gameconst.ChatSysGMErr.OK, '',
                                   {'gbId': gbId, 'isOffline': True, 'forbiddenExpireTime': forbiddenExpireTime,
                                    'forbiddenCount': forbiddenCount})
                LOG_INFO("gm offline queryChatForbidden success, ", gbId, num, insertId, err)

        gamesql.queryForbiddenInfo(playerEnt[0],
                                   lambda ret, num, insert, err: onGetForbiddenInfo(ret, num, insert, err, superUser, gbId))

    # 在线玩家处理
    else:
        LOG_INFO(f"gm online queryChatForbidden, gbID:{playerEnt.gbID}")
        forbiddenExpireTime, forbiddenCount = playerEnt.getChatForbiddenInfo()
        superUser.onCommandResult(gameconst.ChatSysGMErr.OK, '',
                           {'gbId': playerEnt.gbID, 'isOffline': False, 'forbiddenExpireTime': forbiddenExpireTime,
                            'forbiddenCount': forbiddenCount})
    return True, 'command success'


@gm_cmd('$setPKModel', (Player('gbId or Id'), Int('mode')), RARG(0), CELL, '设置战斗模式', ALLSIDE, GOD_GROUPS)
def gm_setPKModel(superUser, playerEnt, pkMode):
    playerEnt.setPKModel(pkMode)


@gm_cmd('$setAllPKModel', (Int('mode'), ), RONE, BASE, '设置所有战斗模式', ALLSIDE, GOD_GROUPS)
def gm_setAllPKModel(superUser, pkMode):
    gameengine.broadcastBaseapp(
        'broadcastToAllAvatar',
        (
            gameconst.CELL, 
            'setPKModel',
            (pkMode,), ()))


@gm_cmd('$addBuff', (Entity('entityId'), Int('buffId'), Int('lv'), Int('duration')), RARG(0), CELL, '添加buff', ALLSIDE, GOD_GROUPS, minArgs=2)
def gm_addBuff(superUser, entity, buffId, buffLv=1, duration=-1):
    if buffId in B_BD.datas and entity.IsCombatUnit:
        entity.addBuff(buffId, buffLv, entity.id, duration)
        return True, 'command success'
    else:
        return False, '执行失败'


@gm_cmd('$setlv', (Player("gbId or Id"), Int("int lv"),), RARG(0), gameconst.CELL, '设置人物等级', ALLSIDE, GOD_GROUPS)
def gm_setPlayerlv(superUser, playerEnt, lv):
    if lv < playerEnt.level:
        return False, '等级不能降低'
    _opUUID = KBEngine.genUUID64()
    src = AAC_AACDD.datas.BONUS_SRC_GM
    detail = gameclass.AwardDetailCls(gm_cmd='$setlv', level=lv)
    import utils
    playerEnt.levelUp(min(utils.getMaxPlayerLevel(), lv), _opUUID, src, detail)
    return True, 'command success'

@gm_cmd('$clearCD', (Player("gbId or Id"),), RARG(0), CELL, '清除技能CD', ALLSIDE, GOD_GROUPS)
def gm_clearCD(superUser, playerEnt ):
    if not playerEnt.skillDic:
        return False, '执行失败，没有装备任何技能'

    for skill in playerEnt.skillDic.values():
        skill.clearCD(playerEnt)
    return True, 'command success'

@gm_cmd('$getAllSkills', (Player("gbId or Id"),), RARG(0), CELL, '获得所有技能', ALLSIDE, GOD_GROUPS)
def gm_getAllSkills(superUser, playerEnt ):
    if not playerEnt.skillDic:
        return False, '执行失败，没有装备任何技能'

    for skillID, skillData in playerEnt.skillDic.items():
        LOG_INFO('getAllSkills:', skillID, skillData)
    LOG_INFO('getAllSkills:', playerEnt.skillDic.skillSwitches)
    return True, 'command success'

@gm_cmd('$destroyEntity', (Entity('entityId'), ), RARG(0), CELL, '销毁实体', INSIDE, GOD_GROUPS)
def gm_destroyEntity(superUser, entity):
    if entity:
        entity.safeDestroy()
        return True, 'command success'
    else:
        return False, '执行失败'


@gm_cmd('$switchServer', (Player("gbId"), Int('serverId')), RARG(0), BASE, '转服', ALLSIDE, GOD_GROUPS)
def gm_switchServer(superUser, playerEnt, serverId):
    playerEnt.switchAvatarServer(serverId)
    return True, 'command success'


@gm_cmd('$enterMap', (Player("gbId or Id"), Int("int mapId")), RARG(0), CELL, '进入地图', ALLSIDE, GOD_GROUPS)
def gm_enterMap(superUser, playerEnt, mapId):
    enterPos, direction = formula.getSpaceBornPosAndDir(mapId)
    playerEnt.applyEnterLineInternal(mapId, 0, enterPos, direction, {'isForceEnter': True})
    return True, 'command success'

@gm_cmd('$EnterAbyss', (Player("gbId or Id"), Int("int floor")), RARG(0), BASE, '进入归墟', ALLSIDE, GOD_GROUPS)
def gm_EnterAbyss(superUser, playerEnt, floor):
    playerEnt.checkAndEnterAbyss(floor)
    return True, 'command success'

@gm_cmd('$LeaveAbyss', (Player("gbId or Id"),), RARG(0), BASE, '离开归墟', ALLSIDE, GOD_GROUPS)
def gm_LeaveAbyss(superUser, playerEnt):
    playerEnt.cell.gmLeaveAbyss()
    return True, 'command success'

@gm_cmd('$EnterWonderLand', (Player("gbId or Id"), Int("int mapId")), RARG(0), BASE, '进入秘境峰', ALLSIDE, GOD_GROUPS)
def gm_EnterWonderLand(superUser, playerEnt, mapId):
    gameengine.getWonderLandStub(mapId).doEnterWonderLand(playerEnt, playerEnt.gbID, {})
    return True, 'command success'

@gm_cmd('$enterCube', (Player("gbId or Id"), Int("int floor")), RARG(0), CELL, '进入魔方阵', ALLSIDE, GOD_GROUPS)
def gm_enterCube(superUser, playerEnt, floor):
    playerEnt.enterCubeInternal(floor)
    return True, 'command success'

@gm_cmd('$enterYanwu', (Player("gbId or Id"), Int("int mapId")), RARG(0), CELL, '进入演武场', ALLSIDE, GOD_GROUPS)
def gm_enterYanwu(superUser, playerEnt, mapId):
    playerEnt.enterLineByNpc(mapId)
    return True, 'command success'

@gm_cmd('$leaveSingleDungeon', (Player("gbId or Id"),), RARG(0), CELL, '离开当前副本', ALLSIDE, GOD_GROUPS)
def gm_leaveSingleDungeon(superUser, playerEnt):
    import gamePlay_gamePlay as GGD
    import dungeonSrc
    import tutorConst_newbieStep as TCNSD
    lockdun = []
    for _,v in TCNSD.datas.items():
        lockdun.append(v.get('lockDun'))
    dungeonNo = formula.parseDungeonNoBySpaceNo(playerEnt.spaceNo)

    if  GGD.datas[dungeonNo].get('sceneType') not in [1,2]:
        return False,f'{dungeonNo}不是副本'

    if dungeonNo in lockdun:     #如果是新手副本，先跳过新手任务，在离开副本。
        forwardGMCommand(superUser,"$SkipNewbieTask",playerEnt.id)

    src = dungeonSrc.DungeonFromClientSrc(playerEnt.base, playerEnt.gbId)
    playerEnt.doLeaveSingleDungeon(dungeonNo, src, 'client leave')
    return True, 'command success'

@gm_cmd('$SkipNewbieTask', (Player("gbId or Id"),), RARG(0), BASE, '跳过新手任务', ALLSIDE, GOD_GROUPS)
def gm_SkipNewbieTask(superUser, playerEnt):
    import tutorConst_newbieStep as TCNSD
    stepLimit = max(TCNSD.datas.keys())
    for step, data in TCNSD.datas.items():
        if playerEnt.newbieStep <= step < stepLimit:
            taskId = data['taskTag']
            if taskId:
                for subTaskId in playerEnt.taskInfo.getChildTaskIds(taskId):
                    playerEnt.taskInfo.tasks.pop(subTaskId, None)
                playerEnt.gmForceSubmitTask(taskId)
                playerEnt.taskInfo.tasks.pop(taskId, None)
                playerEnt.taskInfo.taskRecordDic[taskId] = gameconst.TaskStatEnum.TASK_STAT_SUBMITTED
            playerEnt.newbieStep = max(TCNSD.datas.keys())
    return True, 'command success'


@gm_cmd('$AllPlayerEnterMap', (Player("gbId or Id"), Int("int mapId"), Int("int floor")), RARG(0), gameconst.CELL, '所有人进入指定地图', ALLSIDE, GOD_GROUPS,minArgs=2)
def gm_AllPlayerEnterMap(superUser,playerEnt,mapId,floor=1):
    import gamePlay_gamePlay as GGD
    mapInfo = GGD.datas[mapId]
    sceneType = mapInfo.get('sceneType')
    type = mapInfo.get('type')
    if not sceneType or not type:
        return False, f'地图 {mapId} 配置错误：缺少sceneType或type字段'

    if (sceneType == 4 or sceneType == 7) and type == 6:  #大世界场景
        for entity in KBEngine.entities.values():
            if entity.className == 'Avatar':
                forwardGMCommand(superUser,"$enterMap",entity.id,mapId)
    elif (sceneType == 1 or sceneType == 2) and (type == 1 or type == 2): #副本场景
        for entity in KBEngine.entities.values():
            if entity.className == 'Avatar':
                forwardGMCommand(superUser,"$gmenterDungeon",entity.id,mapId)
    elif sceneType == 3 and type == 3:
        for entity in KBEngine.entities.values():
            if entity.className == 'Avatar':
                forwardGMCommand(superUser,"$enterCube",entity.id,floor)
    elif sceneType == 5 and type == 7:
        for entity in KBEngine.entities.values():
            if entity.className == 'Avatar':
                forwardGMCommand(superUser,"$EnterWonderLand",entity.id,mapId)
    elif sceneType == 6 and type == 8:
        for entity in KBEngine.entities.values():
            if entity.className == 'Avatar':
                forwardGMCommand(superUser,"$enterCityBattle",entity.id)
    elif sceneType == 7 and type == 6:
        for entity in KBEngine.entities.values():
            if entity.className == 'Avatar':
                entity.enterLineByNpc(mapId)
    return True, 'command success'


@gm_cmd('$finishNewbie', (Player("gbId or Id"), Int('step')), RARG(0), BASE, '完成新手', ALLSIDE, GOD_GROUPS)
def gm_finishNewbie(superUser,playerEnt, step):
    # if not playerEnt.newbieStep :
    #     return False, '已跳过新手'
    playerEnt.gmFinishedNewbie(step)
    return True, 'command success'

@gm_cmd('$ALLfinishNewbie', (Player("gbId or Id"), Int('step')), RARG(0), BASE, '所有人完成新手', ALLSIDE, GOD_GROUPS)
def gm_ALLfinishNewbie(superUser,playerEnt, step):
    for entity in KBEngine.entities.values():
        if entity.className == 'Avatar':
            entity.gmFinishedNewbie(step)
    return True, 'command success'


@gm_cmd('$createDuelFlag', (Player("gbId or Id"),), RARG(0), CELL, '创建决斗旗子', ALLSIDE, GOD_GROUPS)
def gm_createDuelFlag(superUser, playerEnt):
    params = {
        'position': playerEnt.position,
        'direction': playerEnt.direction,
        'avatarInDuelDatas': [],
        'spaceNo': playerEnt.spaceNo,
    }

    KBEngine.createEntity('DuelFlag', playerEnt.spaceID, playerEnt.position, playerEnt.direction, params)
    return True, 'command success'



@gm_cmd('$finishAchievement', (Player("gbId or Id"), Int('AchievementID')), RARG(0), BASE, '完成指定成就', ALLSIDE, GOD_GROUPS)
def gm_finishAchievement(superUser,playerEnt, AchievementID):
    if AchievementID in playerEnt.achievementInfo.finishedIds:
            LOG_WARN('AchievementID already exists', AchievementID)
    else:
        playerEnt.achievementInfo.finishedIds.add(AchievementID)
    playerEnt.achievementInfo.sendInitDataToClient(playerEnt)
    return True, 'command success'

@gm_cmd('$AddGuildExp', (Player("gbId or Id"), Int('GuildExp')), RARG(0), BASE, '增加当前帮会经验', ALLSIDE, GOD_GROUPS)
def gm_addguildexp(superUser, playerEnt,exp):
    _opUUID = KBEngine.genUUID64()
    src = AAC_AACDD.datas.BONUS_SRC_GM
    detail = gameclass.AwardDetailCls(gm_cmd='$SetGuildLevel', exp=exp)
    if exp < 1:
        return False, '执行失败，经验不能小于1'
    elif playerEnt.guildBox is None:
        return False, '当前玩家没有帮会'
    playerEnt.guildBox.addGuildExp(exp, src, _opUUID, detail)
    playerEnt._sendGuildInfo()
    return True, 'command success'

@gm_cmd('$modifyBuildingExp', (Player("gbId or Id"),Int('building'),Int('Exp')), RARG(0), BASE, '增加帮会建筑经验', ALLSIDE, GOD_GROUPS)
def gm_modifybuildingexp(superUser, playerEnt,building,exp):
    if building not in (gameconst.GuildBuilding.JU_YING,gameconst.GuildBuilding.WU_HUA,gameconst.GuildBuilding.XIANG_FANG,gameconst.GuildBuilding.YAN_WU,gameconst.GuildBuilding.CANG_KU, gameconst.GuildBuilding.JUN_XU):
        return False, '执行失败，帮会建筑不存在'
    _opUUID = KBEngine.genUUID64()
    src = AAC_AACDD.datas.BONUS_SRC_GM
    detail = gameclass.AwardDetailCls(gm_cmd='$modifyBuildingExp', building=building,exp=exp)
    if exp < 1:
        return False, '执行失败，经验不能小于1'
    elif playerEnt.guildBox is None:
        return False, '当前玩家没有帮会'
    playerEnt.guildBox.modifyBuildingExp(building,exp,src,_opUUID,detail)
    playerEnt._sendGuildInfo()
    return True, 'command success'

@gm_cmd('$welfareSignInDay', (Player("gbId or Id"), Int("int flag"), Str('welfareType')), RARG(0), gameconst.BASE, '福利签到天数累计', ALLSIDE, GOD_GROUPS)
def gm_welfareSignInDay(superUser, playerEnt, flag, welfareType):
    flag %= 2
    return playerEnt.gmUpdateWelfareSignIn(flag, welfareType)

@gm_cmd('$enterCityBattle', (Player("gbId or Id"),), RARG(0), gameconst.BASE, '进城战场景', ALLSIDE, GOD_GROUPS)
def gm_enterCityBattle(superUser, playerEnt):
    return playerEnt.cell.gmEnterSiegeWarSpace()

@gm_cmd('$fastBidding', (Player("gbId or Id"), Int('cnt')), RARG(0), gameconst.BASE, '快速报名+竞拍', ALLSIDE, GOD_GROUPS)
def gm_fastBidding(superUser, playerEnt, cnt):
    playerEnt.gmFastBidding(cnt)
    return True, 'command success'

@gm_cmd('$clearCityRecentRecord', (Player("gbId or Id"),), RARG(0), gameconst.BASE, '清空城池操作记录', ALLSIDE, GOD_GROUPS)
def gm_clearCityRecentRecord(superUser, playerEnt):
    _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
    _stub.clearCityRecentRecord()

@gm_cmd('$addCityMoney', (Player("gbId or Id"), Int('money')), RARG(0), gameconst.BASE, '城池加钱', ALLSIDE, GOD_GROUPS)
def gm_addCityMoney(superUser, playerEnt, money):
    _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
    _stub.gmAddCityMoney(money)
    return True, 'command success'

@gm_cmd('$clearCityOwner', (Player("gbId or Id"),), RARG(0), gameconst.BASE, '清空城池归属', ALLSIDE, GOD_GROUPS)
def gm_clearCityOwner(superUser, playerEnt):
    _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
    _stub.gmClearCityOwner()
    return True, 'command success'

@gm_cmd('$RemoveCityOwnerFlag', (Player("gbId or Id"),), RARG(0), gameconst.BASE, '移除帮会标记', ALLSIDE, GOD_GROUPS)
def gm_RemoveCityOwnerFlag(superUser, playerEnt):
    playerEnt.guildBox.onChangeCityOwnerFlag(False)
    return True, 'command success'

@gm_cmd('$changeSiegeWarState', (Player("gbId or Id"), Int('state'), Int('endTime')), RARG(0), gameconst.BASE, '修改城战状态', ALLSIDE, GOD_GROUPS)
def gm_gmChangeSiegeWarState(superUser, playerEnt, state, endTime):
    _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
    _stub.gmChangeSiegeWarState(state, endTime, 0)
    return True, 'command success'

@gm_cmd('$changeSiegeWarStateOfficial', (Player("gbId or Id"), Int('state'), Int('endTime')), RARG(0), gameconst.BASE, '修改城战状态(线上用)', ALLSIDE, GOD_GROUPS)
def gm_gmChangeSiegeWarStateOfficial(superUser, playerEnt, state, endTime):
    _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
    _stub.gmChangeSiegeWarState(state, endTime, (0, 1))
    return True, 'command success'

@gm_cmd('$siegeWarBattleFastForward', (Player("gbId or Id"), Int('minutes')), RARG(0), gameconst.BASE, '城战战斗快进', ALLSIDE, GOD_GROUPS)
def gm_gmSiegeWarBattleFastForward(superUser, playerEnt, minutes):
    gameengine.getGlobalBase("SiegeWarSpaceStub").onGmAddTime(minutes)
    playerEnt.sendWorldChatMsg(playerEnt, "城战战斗快进"+str(minutes)+"分钟")

    _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
    _stub.gmChangeSiegeWarState(4, 0, minutes)
    return True, 'command success'

@gm_cmd('$siegeWarTestScores', (Player("gbId or Id"),), RARG(0), gameconst.BASE, '城战测试分数', ALLSIDE, GOD_GROUPS)
def gm_siegeWarTestScores(superUser, playerEnt):
    gameengine.getGlobalBase("SiegeWarSpaceStub").onGmTestScores()
    return True, 'command success'

@gm_cmd('$resetMailStubTime', (Player("gbId or Id"),), RARG(0), gameconst.BASE, '改数据库重置邮件lasttime', ALLSIDE, GOD_GROUPS)
def gm_resetMailStubTime(superUser, playerEnt):
    now = utils.curTS()
    sql = "UPDATE tbl_GlobalMailStub SET sm_lastSendTime = %s WHERE id = 1;" % (now)
    KBEngine.executeRawDatabaseCommand(sql)
    playerEnt.sendWorldChatMsg(playerEnt, "邮件数据库lasttime已重置:"+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)))+"重启服务器生效")
    return True, 'command success'

@gm_cmd('$createCreationByFixedPosition', (Player("gbId or Id"), Int('creationId'), Int('x'),Int('y'),Int('z')), RARG(0), CELL, '创建固定位置的创建物', ALLSIDE, GOD_GROUPS)
def gm_createCreationByFixedPosition(superUser, playerEnt, creationId, x,y,z):
    context = actionContext.ActionContext()
    context.actionType = actionContext.ACTION_USE_SKILL
    context.skillId = 0
    positionList = [playerEnt.position]
    positionList.append(Math.Vector3(x,y,z))
    playerEnt.createCreationByFixedPos(playerEnt,context,creationId,1,1,0,1,positionList)
    return True,'command success'


@gm_cmd('$sendrewardIDglobalmail', (Int('mailId'), Int('rewardID'), Str('despArgsStr'), Str('title'), Str('cont'), Int('minRoleTime'), Int('maxRoleTime'),
                                    Int('dueTime'),Int('minRoleLevel'), Int('maxRoleLevel'), Int('channel')),
        RSU, gameconst.BASE, '发送一封全服邮件', INSIDE, GOD_GROUPS)
def gm_sendrewardIDglobalmail(superUser, mailId, rewardID, despArgsStr, title, cont, minRoleTime, maxRoleTime, dueTime, minRoleLevel, maxRoleLevel, channel):
    # attachStr: 多个物品用分号';'分隔; 每个物品有itemId, itemNum，若有绑定属性配置在第三个位置，例如：[30000001,100; 30001031,1,1]
    import dropAward
    import awardContext
    import itemData_set as IDSD
    COIN_ID = IDSD.datas['itemID_coin']['value']
    MONEY_ID = IDSD.datas['itemID_money']['value']
    _attach = dropAward.MailAttachVal()

    dropCtx = awardContext.DropAwardCtx(1234, 20, {'lv': 20}, eventTipId=5678,
                                    monsterId=5678,
                                    monsterSpaceNo=10020000, activityId=0)
    award = dropAward.getAwardOne(rewardID, dropCtx)

    if award.itemWealth.itemsObjs:
        equipdata = award.itemWealth.itemsObjs
        for equip in equipdata:
            _attach.addWealthByItemId(equip.itemId, equip.itemNum, 0)

    if award.itemWealth.data:
        itemWealthData = award.itemWealth.data
        for itemId, bindTypeDict in itemWealthData.items():
            for bindType, itemNum in bindTypeDict.items():
                _attach.addWealthByItemId(itemId, itemNum, bindType)

    _despArgs = mailAssistor.parseDespStr(despArgsStr)
    _title = title.strip("[] ")
    cont = cont.strip("[] ")
    gameengine.getGlobalBase('GlobalMailStub').sendGlobalMail(mailId, _attach, _despArgs, _title, cont, minRoleTime, maxRoleTime, dueTime, 
                                                              minRoleLevel, maxRoleLevel, channel, AAC_AACDD.datas.BONUS_SRC_GM)
    return True, 'command success'


@gm_cmd('$changeAllSkill', (Player("gbId or Id"), Str('skillList')),RARG(0), gameconst.CELL, '指定怪物替换技能', ALLSIDE, GOD_GROUPS)
def gm_changeAllSkill(superUser, playerEnt,skillList):
    import ast
    newSkillList = ast.literal_eval(skillList)
    eid = playerEnt.selectedTargetId
    entity = KBEngine.entities.get(eid)
    if not entity or not entity.IsCombatUnit:
        return superUser.onCommandResult(0, 'False,技能替换失败', {})
    entity.changeAllSkill(newSkillList)
    return superUser.onCommandResult(0, 'ok,怪物技能替换成功', {})

@gm_cmd('$setProp', (Player("gbId or Id"),Str("str propName"), Float("value"),), RARG(0), gameconst.CELL, '设置人物属性', ALLSIDE, GOD_GROUPS)
def gm_setProp(superUser, playerEnt,propName,value):
    if value or propName:
        playerEnt.setProp(f'{propName}', value, gameconst.SourceType.SrcTpDefault)
        return True, 'command success'
    return False, f'检查propName:{propName}'

@gm_cmd('$enterCubeRoom', (Player("gbId or Id"), Int("int mapId"),), RARG(0), gameconst.CELL, '进入魔方阵指定房间', ALLSIDE, GOD_GROUPS)
def gm_enterCubeRoom(superUser, playerEnt, mapId):
    if playerEnt.gmEnterCubeRoom(mapId):
        return True, 'command success'
    else:
        return False, '执行失败'

@gm_cmd('$createCubeCowTeleport', (Player("gbId or Id"), ), RARG(0), gameconst.CELL, '创建进入魔方阵的传送门', ALLSIDE, GOD_GROUPS)
def gm_createCubeCowTeleport(superUser, playerEnt):
    if not formula.inCubeScene(playerEnt.spaceNo):
        return False, '当前不在魔方空间'

    playerEnt.spaceMgr.createTeleporterToCow(playerEnt.position)
    return True, 'command success'


@gm_cmd('$changeSceneStates', (Player("gbId or Id"), Str("str states")), RARG(0), gameconst.CELL, '设置场景状态', ALLSIDE, GOD_GROUPS)
def gm_changeSceneStates(superUser, playerEnt, states):
    if not formula.inWolrdBossScene(playerEnt.spaceNo):
        return False, '当前不在boss场景'

    _state = []
    for i, _st in enumerate(states):
        _st = 1 if _st == '1' else 0
        if _st:
            _state.append(i)

    LOG_DBG('setSceneStates', _state)
    playerEnt.setSceneStates(_state)
    return True, 'command success'


@gm_cmd('$levelUpSkill', (Player("gbId or Id"), Int("int skillId"), Int("int level")), RARG(0), gameconst.BASE, '升级指定技能到指定等级', ALLSIDE, GOD_GROUPS)
def gm_levelUpSkill(superUser, playerEnt, skillId, level):
    if not playerEnt:
        return False, "玩家不存在"

    import skill_skill as SSD
    if skillId not in SSD.datas:
        return False, f"技能ID {skillId} 不存在"

    newLevel = level
    playerEnt.buildDic.skillLevels[skillId] = newLevel
    playerEnt.cell.onChangeSkillLv(skillId, newLevel)
    playerEnt.updateSkillLevelSetSummonSlotIdx(skillId, newLevel)

    # 处理相关联的被动技能升级（参考原有逻辑）
    relatedSkills = SSD.datas.get(skillId, {}).get('conflictSkill') or ()
    for sid in relatedSkills:
        if sid in playerEnt.buildDic.skillLevels:
            playerEnt.buildDic.skillLevels[sid] = newLevel
            playerEnt.updateSkillLevelSetSummonSlotIdx(sid, newLevel)

    playerEnt.client.onUpdateSkillLevel([skillId], [newLevel])

    return True, f"技能 {skillId} 已升级到等级 {level}"

@gm_cmd('$gotoLinePos', (Player("gbId or Id"), Int('spaceNo'),  Float('x'), Float('y'), Float('z')), RARG(0), CELL,
        '传送到大世界地图指定位置', ALLSIDE, GOD_GROUPS, minArgs=2)
def gm_gotoLinePos(superUser, playerEnt, spaceNo=0, x=0, y=0, z=0):
    if spaceNo == 0:
        spaceNo = playerEnt.spaceNo

    pos = Math.Vector3(x, y, z)
    if x == 0 and y == 0 and z == 0:
        pos, _ = utils.getPlayerBornInfo()

    try:
        lineNo = formula.parseLineNo(spaceNo)
        lineType = formula.parseLineType(spaceNo)
        if formula.fetchMapId(playerEnt.spaceNo) == lineType:
            return False, '执行失败'

        playerEnt.applyEnterLineInternal(lineType, lineNo, pos, playerEnt.direction, False)
    except:
        gameengine.panicStack('gm gotoLinePos error')
        return False, '执行失败'
    return True, 'command success'

@gm_cmd('$applyFinishGather', (Player("gbId or Id"),), RARG(0), gameconst.CELL, '主动结束采集', ALLSIDE, GOD_GROUPS)
def gm_applyFinishGather(superUser, playerEnt):
    gatherTarget = playerEnt.getTempMiscProp(gameconst.EntityPropsEnum.gatherTarget, None)
    if not gatherTarget or 'timer' not in gatherTarget:
        return False, '当前没有采集物体'
    playerEnt.applyFinishGather(playerEnt.id, gatherTarget['targetId'])

@gm_cmd('$clearPickedCollections', (Player("gbId or Id"), Int("int collection id"),), RARG(0), gameconst.CELL, '主动结束采集', ALLSIDE, GOD_GROUPS)
def gm_clearPickedCollections(superUser, playerEnt, collectionId):
    curAOI = playerEnt.getViewRadius()
    for m in playerEnt.entitiesInRange(curAOI, 'Collection'):
        if m.collectionId != collectionId:
            continue

        playerEnt.pickedCollections.pop(collectionId, None)
        m.gatherAvatars.pop(playerEnt.gbId, None)
        playerEnt.checkCollectionGatherFlag(m.id)
        if m.type == gameconst.CollectionType.VIEWPOINT:
            playerEnt.checkRelationType(m)

    return True, 'command success'

@gm_cmd('$setVIP', (Player("gbId or Id"), Str("str account"),), RARG(0), gameconst.BASE, '设置特权', ALLSIDE, GOD_GROUPS)
def gm_setVIP(superUser, playerEnt, account):
    redisUtils.RedisUtils.cmdSet(gameconst.PrivilegeRedisKey.VIP + account, "1")
    return True, 'command success'

@gm_cmd('$setSVIP', (Player("gbId or Id"), Str("str account"),), RARG(0), gameconst.BASE, '设置特权', ALLSIDE, GOD_GROUPS)
def gm_setSVIP(superUser, playerEnt, account):
    redisUtils.RedisUtils.cmdSet(gameconst.PrivilegeRedisKey.SVIP + account, "1")
    return True, 'command success'

@gm_cmd('$gmOpForbiddenTaskIds', (Int('opType'), Int('taskId')), RONE, BASE, '禁止任务', ALLSIDE, GOD_GROUPS)
def gm_gmOpForbiddenTaskIds(superUser, opType, taskId):
    if opType != gameconst.ForbiddenTaskIdOpType.QUERY and str(taskId) not in TDD.datas:
        return False, '执行失败'
    if opType == gameconst.ForbiddenTaskIdOpType.QUERY:
        taskIds = gameengine.quertForbiddenTaskIds()
        return True, '执行成功, taskIds:' + ','.join([str(i) for i in taskIds])
    elif opType == gameconst.ForbiddenTaskIdOpType.ADD:
        gameengine.callAllApps('gameengine.addForbiddenTaskIds', (taskId,))
        return True, 'command success'
    elif opType == gameconst.ForbiddenTaskIdOpType.REMOVE:
        gameengine.callAllApps('gameengine.removeForbiddenTaskIds', (taskId,))
        return True, 'command success'
    return False, '执行失败'

@gm_cmd('$showBountyInfo', (Player("gbId or Id"),), RARG(0), BASE, '显示当前悬赏列表', ALLSIDE, GOD_GROUPS)
def gm_showBountyInfo(superUser, playerEnt):
    gameengine.getGlobalBase('BountyStub').gmShowBountyInfo()
    return True, 'command success'

@gm_cmd('$reqPublishBounty', (Player("gbId or Id"),), RARG(0), BASE, '发布悬赏', ALLSIDE, GOD_GROUPS)
def gm_reqPublishBounty(superUser, playerEnt):
    playerEnt.reqPublishBounty(playerEnt.gbID, "", 100, 0, "")
    return True, 'command success'

@gm_cmd('$reqAcceptBounty', (Player("gbId or Id"), Int('uuid'),), RARG(0), BASE, '揭取悬赏', ALLSIDE, GOD_GROUPS)
def gm_reqAcceptBounty(superUser, playerEnt, uuid):
    playerEnt.reqAcceptBounty(playerEnt.gbID, uuid)
    return True, 'command success'

@gm_cmd('$reqGetAvatarBountyInfo', (Player("gbId or Id"), Int('type'),), RARG(0), BASE, '获取与玩家相关的悬赏单信息', ALLSIDE, GOD_GROUPS)
def gm_reqGetAvatarBountyInfo(superUser, playerEnt, type):
    playerEnt.reqGetAvatarBountyInfo(playerEnt.gbID, type)
    return True, 'command success'

@gm_cmd('$reqReplyAssignedHunter', (Player("gbId or Id"), Int('uuid'), Int('res'),), RARG(0), BASE, '被指定杀手玩家回复', ALLSIDE, GOD_GROUPS)
def gm_reqReplyAssignedHunter(superUser, playerEnt, uuid, res):
    playerEnt.reqReplyAssignedHunter(playerEnt.gbID, uuid, res)
    return True, 'command success'

@gm_cmd('$reqGetPublicRankList', (Player("gbId or Id"), Int('type'), Int('vid'),), RARG(0), BASE, '获取排行榜数据', ALLSIDE, GOD_GROUPS)
def gm_reqGetPublicRankList(superUser, playerEnt, type, vid):
    playerEnt.reqGetPublicRankList(playerEnt.gbID, type, vid)
    return True, 'command success'

@gm_cmd('$reqGetPublicBountyList', (Player("gbId or Id"), Int('startIdx'),), RARG(0), BASE, '获取悬赏列表', ALLSIDE, GOD_GROUPS)
def gm_reqGetPublicBountyList(superUser, playerEnt, startIdx):
    playerEnt.reqGetPublicBountyList(playerEnt.gbID, startIdx)
    return True, 'command success'
