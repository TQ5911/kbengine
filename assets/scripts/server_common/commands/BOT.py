# -*- coding: utf-8 -*-
from commands.CMD_COMMON import *

RAID_PLAYER_IDS = list()
HOME_GROUP_LIST = list()
ENTER_ID_LIST = list()


@gm_cmd('$botassemble', (Int('bot num'),), RSU, CELL, '召集num个机器人到身边，不能跨地图', INSIDE, GOD_GROUPS)
def botAsseble(su, num):
    _avatarList = utils.getEntityList("Avatar")
    _num = min(num, len(_avatarList))
    if not _num:
        return False, '找不到机器人'

    _avatars = []
    for avatar in _avatarList:
        if not avatar.isClientBot():
            continue

        if avatar.spaceNo != su.spaceNo:
            continue
        _avatars.append(avatar)

    for _avatar in random.sample(_avatars, _num):
        _posList = su.getRandomPoints(su.position, 10, 1, 0)
        if _posList:
            _pos = _posList[0]
            _pos = (_pos[0], su.position[1], _pos[2])
        else:
            _pos = su.position

        _avatar.position = _pos
    return True, 'command success'


@gm_cmd('$botleaveview', (), RSU, CELL, '当前地图的bot移到互相看不到的位置，不考虑地形', INSIDE, GOD_GROUPS)
def botLeaveView(su):
    _avatarList = utils.getEntityList("Avatar")

    _avatars = []
    for avatar in _avatarList:
        if not avatar.isClientBot():
            continue

        if avatar.spaceNo != su.spaceNo:
            continue
        _avatars.append(avatar)

    if not _avatars:
        return True, 'done success，没有机器人'

    getPoints = lambda bot: [(bot.position[0] + 35, bot.position[1], bot.position[2]), (bot.position[0], bot.position[1], bot.position[2] + 35), (bot.position[0] + 35, bot.position[1], bot.position[2] + 35)]

    moveToPoints = getPoints(_avatars[0])
    for _bot in _avatars[1:]:
        _bot.position = moveToPoints[0]
        moveToPoints.pop(0)
        if not moveToPoints:
            moveToPoints = getPoints(_bot)
    return True, 'command success'


@gm_cmd('$botdissemble', (Entity('entity id'), Int('num'), Int('range')), RARG(0), CELL, '让num个bot随机散开', ALLSIDE, GOD_GROUPS, minArgs=1)
def botDisseble(su, entity, num, r=200):
    _avatarList = utils.getEntityList("Avatar")
    num = min(num, len(_avatarList))
    if not num:
        return False, '找不到机器人'

    for _avatar in random.sample(_avatarList, num):
        if not _avatar.isClientBot():
            continue

        _posList = _avatar.getRandomPoints(_avatar.position, r, 1, 0)
        if _posList:
            pos = _posList[0]
            pos = (pos[0], _avatar.position[1], pos[2])
        else:
            pos = _avatar.position

        _avatar.position = pos
    return True, 'command success'


@gm_cmd('$randpos', (Int('range'),), RSU, CELL, '半径range范围内随机设个位置', INSIDE, GOD_GROUPS)
def botRandPos(su, r):
    _posList = su.getRandomPoints(su.position, r, 1, 0)
    if _posList:
        _pos = _posList[0]
        _pos = (_pos[0], su.position[1], _pos[2])
    else:
        _pos = su.position

    su.position = _pos
    return True, 'command success'


@gm_cmd('$botarounddocmd', (Player("gbId or Id"), Int('range'), Str('cmd'), Int('num')), RARG(0), CELL, '让附近的bot执行command，距离为0时让当前地图所有bot执行', ALLSIDE, GOD_GROUPS, minArgs=3)
def botDoCommand(su, player, r, command, num=0):
    _avatarList = player.entitiesInRange('Avatar', r)
    _nAvatar = len(_avatarList)
    if not _nAvatar:
        return False, '找不到机器人'

    num = min(num or _nAvatar, _nAvatar)
    command = command.replace('&nbsp', ' ')

    for avatar in random.sample(_avatarList, num):
        if not avatar.isClientBot():
            continue

        avatar.base.runGmCommand(command)
    return True, 'command success'


@gm_cmd('$allbotdo', (Str('cmd'), Int('num')), RALL, BASE, '所有机器人或num个机器人执行gm command', ALLSIDE, GOD_GROUPS, minArgs=1)
def allBotDoCommand(su, command, num=0):
    command = command.replace('&nbsp', ' ')
    _avatarList = utils.getEntityList("Avatar")
    if num:
        _avatarList = random.sample(_avatarList, num)
    for avatar in _avatarList:
        if not avatar.isBotBase:
            continue
        avatar.runGmCommand(command)


@gm_cmd('$allbotToPos', (), RALL, CELL, '机器人传到指定位置', ALLSIDE, GOD_GROUPS)
def allbotToPos(su):
    import utils

    _avatarList = utils.getEntityList("Avatar")
    _regionPositionList = [(5136, 309, 5662), (5113, 320, 5862)]
    for i, _avatar in enumerate(_avatarList):
        if not _avatar.isClientBot():
            continue

        _avatar.position = _regionPositionList[i % 2]


@gm_cmd('$allbotToDesPos', (Float('xx'), Float('yy'), Float('zz'),), RALL, CELL, '机器人一起move到指定位置', ALLSIDE, GOD_GROUPS, minArgs=0)
def allbotToDesPos(su, xx, yy, zz):
    import utils

    if not xx or not yy or not zz:
        xx = 5126
        yy = 313
        zz = 5780
    _regionDesPosition = (xx, yy, zz)
    _avatarList = utils.getEntityList("Avatar")

    for _avatar in _avatarList:
        if not _avatar.isClientBot():
            continue

        _avatar.scriptNavigate(_regionDesPosition, _avatar.speed)


@gm_cmd('$allbotAutoFight', (Int('Mode'),), RALL, CELL, '机器人开启自动战斗', ALLSIDE, GOD_GROUPS)
def allbotAutoFight(su, mode):
    import utils

    _avatarList = utils.getEntityList("Avatar")
    for _avatar in _avatarList:
        if not _avatar.isClientBot():
            continue
        if mode == 1:
            _avatar._startAutoCombat()
        else:
            _avatar.stopAutoCombat(_avatar.id)


@gm_cmd('$allbotRelive', (), RALL, CELL, '机器人复活', ALLSIDE, GOD_GROUPS)
def allbotRelive(su):
    import utils

    _avatarList = utils.getEntityList("Avatar")
    for avatar in _avatarList:
        if not avatar.isClientBot():
            continue
        avatar.relive(avatar.id, gameconst.RELIVE_TYPE_DIRECTLY)



@gm_cmd('$allbotTestbird', (), RALL, BASE, '所有机器人执行testbird', ALLSIDE, GOD_GROUPS)
def allbotTestbird(su):
    _avatarList = utils.getEntityList("Avatar")
    _avatarOne = None
    for _avatar in _avatarList:
        if not _avatar.isBotBase:
            continue

        if not _avatarOne:
            avatarOne = _avatar
        # # 跳新手
        # _avatar.runGmCommand('$botFinishNewbie 0')
        # 升级
        _avatar.runGmCommand('$setlv 0 99')
        # 获取装备
        _avatar.runGmCommand('$getequipsuit 0 4 1')
        # 装备
        _avatar.runGmCommand('$dressEquipsByQuality 0 4 0')
        # 强化等级
        _avatar.runGmCommand('$gearTolv 0 10')


@gm_cmd('$allbotTestbirdLevelUp', (Int('new level'),), RALL, BASE, '所有机器人升级', ALLSIDE, GOD_GROUPS)
def allbotTestbirdLevelUp(su, newLv):
    _avatarList = utils.getEntityList("Avatar")
    _avatarOne = None
    for _avatar in _avatarList:
        if not _avatar.isBotBase:
            continue

        if not _avatarOne:
            avatarOne = _avatar
        _avatar.runGmCommand('$setlv 0 %s'%newLv)


@gm_cmd('$allbotTestbirdLevelUpRdm', (Int('min level'), Int('max level')), RALL, BASE, '所有机器人升级至随机等级', ALLSIDE, GOD_GROUPS)
def allbotTestbirdLevelUpRdm(su, minLevel, maxLevel):
    import random

    minLevel = max(1, minLevel)
    maxLevel = max(minLevel, maxLevel)
    _avatarList = utils.getEntityList("Avatar")
    for avatar in _avatarList:
        if not avatar.isBotBase:
            continue
        avatar.runGmCommand('$setlv 0 {}'.format(random.randint(minLevel, maxLevel)))


# ----------------------------------------------------------------------------------------------------------------
@gm_cmd('$botToPos', (Player("gbId or Id"), Int('pos type'), Int('back')), RARG(0), CELL, '机器人传到指定位置', ALLSIDE, GOD_GROUPS)
def botToPos(su, playerEnt, positionType, back):
    import Math

    _dstPosList = []
    if positionType == 1:
        _dstPosList = [Math.Vector3(7683, 208.5, 4632)]

    elif positionType == 2:
        _dstPosList = [Math.Vector3(6578.0, 166.03, 4603.0),
                      Math.Vector3(6730.313, 166.09, 4603.0), Math.Vector3(6650, 166.14, 4603)]
    elif positionType == 3:
        _dstPosList = [Math.Vector3(6578, 166.03, 4603.0),
                      Math.Vector3(6730.313, 166.09, 4603.0), Math.Vector3(6650, 166.14, 4603),
                      Math.Vector3(5680.0, 165, 4048.0), Math.Vector3(5586.7, 164.3221, 4067.0), Math.Vector3(5532.0, 163.4, 4001.0),
                      Math.Vector3(5266, 196, 4176), Math.Vector3(5260.0, 176.7, 4069.0), Math.Vector3(5235.0, 165, 3949)
                      ]

    if not back:
        playerEnt.position = _dstPosList[random.randint(0, len(_dstPosList) - 1)]
        _posList = playerEnt.getRandomPoints(playerEnt.position, 80, 1, 0)
        if _posList:
            pos = _posList[0]
            pos = (pos[0], playerEnt.position[1], pos[2])
        else:
            pos = playerEnt.position
        playerEnt.position = pos
    else:
        _avatarList = utils.getEntityList("Avatar")
        for avatar in _avatarList:
            if not avatar.isClientBot():
                continue
            _posList = playerEnt.getRandomPoints(_dstPosList[random.randint(0, 2)], 80 , 1, 0)
            if _posList:
                _pos = _posList[0]
                _pos = (_pos[0], playerEnt.position[1], _pos[2])
            else:
                _pos = avatar.position
            avatar.position = _pos
    return True, 'command success'


@gm_cmd('$botMove', (Int('Mode'),), RALL, CELL, '所有机器人开始移动', ALLSIDE, GOD_GROUPS)
def startAllBotMove(su, mode):
    import Math

    _avatarList = utils.getEntityList("Avatar")
    _avatars = []
    for avatar in _avatarList:
        if not avatar.isClientBot():
            continue
        _avatars.append(avatar)

    for _avatar in _avatars:
        if mode == 1:  # 开始移动
            if _avatar.position[0] > 6400 and _avatar.position[0] < 7000:
                dstPos = Math.Vector3(6669, 166.1, 4601)
                _avatar.botMoveTo(_avatar.id, dstPos)
        else:
            if _avatar.position[0] > 6400 and _avatar.position[0] < 7000:
                _avatar.botStopMove(_avatar.id)


@gm_cmd('$botCall', (Int('num'), Int('type'), Float('xx'), Float('yy'), Float('zz'),), RALL, CELL, '召集指定数量的bot到一个位置', ALLSIDE, GOD_GROUPS)
def botCall(su, num, type, x, y, z):
    _avatarList = utils.getEntityList("Avatar")
    num = min(num, len(_avatarList))
    if not num:
        return

    _avatars = []
    for _avatar in _avatarList:
        if not _avatar.isClientBot():
            continue
        if type == 1:
            if  _avatar.position[0] > 6400 and _avatar.position[0] < 7000:
                _avatars.append(_avatar)
        if type == 2:
            if  _avatar.position[0] > 5000 and _avatar.position[0] < 6000:
                _avatars.append(_avatar)
        if type == 3:
            if  _avatar.position[0] > 7000 and _avatar.position[0] < 8000:
                _avatars.append(_avatar)

    num = min(num, len(_avatars))
    regionDesPosition = (x, y, z)
    for _avatar in random.sample(_avatars, num):
        _posList = _avatar.getRandomPoints(regionDesPosition, 80, 1, 0)
        if _posList:
            pos = _posList[0]
            pos = (pos[0], y, pos[2])
        else:
            pos = regionDesPosition

        _avatar.position = pos


@gm_cmd('$botStartFight', (Int('Mode'),), RALL, CELL, '机器人切换battle mode', ALLSIDE, GOD_GROUPS)
def botStartFight(su, mode):
    _avatarList = utils.getEntityList("Avatar")
    for _avatar in _avatarList:
        if not _avatar.isClientBot():
            continue
        if _avatar.position[0] < 7000 or _avatar.position[0] > 8000:
            continue
        if mode == 1:
            _avatar.switchPKModel(_avatar.id, gameconst.PKModel.ATTACK)
            _avatar.startAutoCombat(_avatar.id,False)
        else:
            _avatar.stopAutoCombat(_avatar.id)
            _avatar.switchPKModel(_avatar.id, gameconst.PKModel.PEACE)

@gm_cmd('$botStartFightMode', (Player("gbId or Id"), Int('mode')), RARG(0), CELL, '机器人开始battle mode', ALLSIDE, GOD_GROUPS)
def botStartFightMode(su, player, fightMode):
    if fightMode == 1:
        return True, '开始战斗'
    else:
        return True, '停止战斗'

@gm_cmd('$botStartRunMode', (Player("gbId or Id"), Int('mode')), RARG(0), BASE, '机器人开始跑图模式', ALLSIDE, GOD_GROUPS)
def botStartRunMode(su, player, fightMode):
    if fightMode == 1:
        return True, '开始跑图'
    else:
        return True, '停止跑图'


@gm_cmd('$botSwitchLine', (Int('number'), Int('line'),), RSU, BASE, '机器人select line', INSIDE, GOD_GROUPS)
def botSwitchLine(su, number, line):
    _avatarList = utils.getEntityList("Avatar")
    if number and number <= len(_avatarList):
        _avatarList = random.sample(_avatarList, number)
    for avatar in _avatarList:
        if not avatar.isBotBase:
            continue
        avatar.runGmCommand('$switchline 0 %s' % line)
    return True, 'command success'


@gm_cmd('$botNewbie', (), RALL, BASE, '机器人跳新手', ALLSIDE, GOD_GROUPS)
def botNewbie(su):
    _avatarList = utils.getEntityList("Avatar")
    for _avatar in _avatarList:
        if not _avatar.isBotBase:
            continue

        _avatar.runGmCommand('$finishNewbie 0 0')

@gm_cmd('$kickAllBot', (), RALL, BASE, '所有机器人kick offline', ALLSIDE, GOD_GROUPS)
def kickAllBot(su):
    import gameglobal
    _avatarList = utils.getEntityList("Avatar")
    for avatar in _avatarList:
        if not avatar.isBotBase:
            continue

        if not avatar.hasClient:
            continue

        avatar.destroySelf(gameconst.OFFLINE_REASON_GMKICK)

    return True, 'command success'

@gm_cmd('$allBotStartRandomTeleport', (), RALL, BASE, '所有机器人开始随机传送', ALLSIDE, GOD_GROUPS)
def allBotStartRandomTeleport(su):
    _avatarList = utils.getEntityList("Avatar")
    for avatar in _avatarList:
        if not avatar.isBotBase:
            continue

        if not avatar.hasClient:
            continue

        avatar.client.randomTeleport()
    return True, 'command success'

@gm_cmd('$debugPlayerAreaNum', (Int('lineType'), ), RONE, BASE, '打印分线人数调试信息', ALLSIDE, GOD_GROUPS)
def debugPlayerAreaNum(su, linetype):
    import gameengine
    gameengine.getLineStub(linetype).debugPlayerAreaInfo()
    return True, 'command success'
