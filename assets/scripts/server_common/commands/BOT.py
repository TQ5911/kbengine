# -*- coding: utf-8 -*-
from commands.CMD_COMMON import *

RAID_PLAYER_IDS = list()
HOME_GROUP_LIST = list()
ENTER_ID_LIST = list()




@gm_cmd('$botassemble', (Int('num'),), RSU, CELL, '召集num个机器人到身边，不能跨地图', INSIDE, GOD_GROUPS)
def botAsseble(su, num):
    avatarList = utils.getEntityList("Avatar")
    num = min(num, len(avatarList))
    if not num:
        return False, '找不到机器人'

    avatars = []
    for avatar in avatarList:
        if not avatar.isClientBot():
            continue

        if avatar.spaceNo != su.spaceNo:
            continue
        avatars.append(avatar)

    for avatar in random.sample(avatars, num):
        posList = su.getRandomPoints(su.position, 10, 1, 0)
        if posList:
            pos = posList[0]
            pos = (pos[0], su.position[1], pos[2])
        else:
            pos = su.position

        avatar.position = pos
    return True, '执行成功'


@gm_cmd('$botleaveview', (), RSU, CELL, '当前地图的bot移到互相看不到的位置，不考虑地形', INSIDE, GOD_GROUPS)
def botLeaveView(su):
    avatarList = utils.getEntityList("Avatar")

    avatars = []
    for avatar in avatarList:
        if not avatar.isClientBot():
            continue

        if avatar.spaceNo != su.spaceNo:
            continue
        avatars.append(avatar)

    if not avatars:
        return True, '执行成功，没有机器人'

    getPoints = lambda b: [(b.position[0] + 35, b.position[1], b.position[2]), (b.position[0], b.position[1], b.position[2] + 35), (b.position[0] + 35, b.position[1], b.position[2] + 35)]

    moveToPoints = getPoints(avatars[0])
    for bot in avatars[1:]:
        bot.position = moveToPoints[0]
        moveToPoints.pop(0)
        if not moveToPoints:
            moveToPoints = getPoints(bot)
    return True, '执行成功'


@gm_cmd('$botdissemble', (Entity('entity id'), Int('num'), Int('range')), RARG(0), CELL, '让num个机器人随机散开', ALLSIDE, GOD_GROUPS, minArgs=1)
def botDisseble(su, entity, num, r=200):
    avatarList = utils.getEntityList("Avatar")
    num = min(num, len(avatarList))
    if not num:
        return False, '找不到机器人'

    for avatar in random.sample(avatarList, num):
        if not avatar.isClientBot():
            continue

        posList = avatar.getRandomPoints(avatar.position, r, 1, 0)
        if posList:
            pos = posList[0]
            pos = (pos[0], avatar.position[1], pos[2])
        else:
            pos = avatar.position

        avatar.position = pos
    return True, '执行成功'


@gm_cmd('$randpos', (Int('range'),), RSU, CELL, '半径range范围随机设个位置', INSIDE, GOD_GROUPS)
def botRandPos(su, r):
    posList = su.getRandomPoints(su.position, r, 1, 0)
    if posList:
        pos = posList[0]
        pos = (pos[0], su.position[1], pos[2])
    else:
        pos = su.position

    su.position = pos
    return True, '执行成功'


@gm_cmd('$botarounddocmd', (Player("gbId/Id"), Int('range'), Str('cmd'), Int('num')), RARG(0), CELL, '让附近的bot执行命令，距离为0时让当前地图所有bot执行', ALLSIDE, GOD_GROUPS, minArgs=3)
def botDoCommand(su, player, r, cmd, num=0):
    avatarList = player.entitiesInRange('Avatar', r)
    nAvatar = len(avatarList)
    if not nAvatar:
        return False, '找不到机器人'

    num = min(num or nAvatar, nAvatar)
    cmd = cmd.replace('&nbsp', ' ')

    for avatar in random.sample(avatarList, num):
        if not avatar.isClientBot():
            continue

        avatar.base.runGmCommand(cmd)
    return True, '执行成功'


@gm_cmd('$allbotdo', (Str('cmd'), Int('num')), RALL, BASE, '所有机器人或num个机器人执行gm命令', ALLSIDE, GOD_GROUPS, minArgs=1)
def allBotDoCommand(su, cmd, num=0):
    cmd = cmd.replace('&nbsp', ' ')
    avatarList = utils.getEntityList("Avatar")
    if num:
        avatarList = random.sample(avatarList, num)
    for avatar in avatarList:
        if not avatar.isBotBase:
            continue
        avatar.runGmCommand(cmd)


@gm_cmd('$allbotToPos', (), RALL, CELL, '机器人传到指定位置', ALLSIDE, GOD_GROUPS)
def allbotToPos(su):
    import utils

    avatarList = utils.getEntityList("Avatar")
    regionPositionList = [(5136, 309, 5662), (5113, 320, 5862)]
    for i, avatar in enumerate(avatarList):
        if not avatar.isClientBot():
            continue

        avatar.position = regionPositionList[i % 2]


@gm_cmd('$allbotToDesPos', (Float('x'), Float('y'), Float('z'),), RALL, CELL, '机器人一起移动到指定位置', ALLSIDE, GOD_GROUPS, minArgs=0)
def allbotToDesPos(su, x, y, z):
    import utils

    if not x or not y or not z:
        x = 5126
        y = 313
        z = 5780
    regionDesPosition = (x, y, z)
    avatarList = utils.getEntityList("Avatar")

    for avatar in avatarList:
        if not avatar.isClientBot():
            continue

        avatar.scriptNavigate(regionDesPosition, avatar.speed)


@gm_cmd('$allbotAutoFight', (Int('mode'),), RALL, CELL, '机器人开启自动战斗', ALLSIDE, GOD_GROUPS)
def allbotAutoFight(su, mode):
    import utils

    avatarList = utils.getEntityList("Avatar")
    for avatar in avatarList:
        if not avatar.isClientBot():
            continue
        if mode == 1:
            avatar._startAutoCombat()
        else:
            avatar.stopAutoCombat(avatar.id)
        # avatar.switchPKModel(avatar.id, gameconst.PKModel.ATTACK)


@gm_cmd('$allbotRelive', (), RALL, CELL, '机器人复活', ALLSIDE, GOD_GROUPS)
def allbotRelive(su):
    import utils

    avatarList = utils.getEntityList("Avatar")
    for avatar in avatarList:
        if not avatar.isClientBot():
            continue
        avatar.relive(avatar.id, gameconst.RELIVE_TYPE_DIRECTLY)



@gm_cmd('$allbotTestbird', (), RALL, BASE, '所有机器人执行testbird', ALLSIDE, GOD_GROUPS)
def allbotTestbird(su):
    avatarList = utils.getEntityList("Avatar")
    avatarOne = None
    for avatar in avatarList:
        if not avatar.isBotBase:
            continue

        if not avatarOne:
            avatarOne = avatar
        # # 跳新手
        # avatar.runGmCommand('$botFinishNewbie 0')
        # 升级
        avatar.runGmCommand('$setlv 0 99')
        # 获取装备
        avatar.runGmCommand('$getequipsuit 0 4 1')
        # 装备
        avatar.runGmCommand('$dressEquipsByQuality 0 4 0')
        # 强化等级
        avatar.runGmCommand('$gearTolv 0 10')


@gm_cmd('$allbotTestbirdLevelUp', (Int('newLv'),), RALL, BASE, '所有机器人升级', ALLSIDE, GOD_GROUPS)
def allbotTestbirdLevelUp(su, newLv):
    avatarList = utils.getEntityList("Avatar")
    avatarOne = None
    for avatar in avatarList:
        if not avatar.isBotBase:
            continue

        if not avatarOne:
            avatarOne = avatar
        avatar.runGmCommand('$setlv 0 %s'%newLv)


@gm_cmd('$allbotTestbirdLevelUpRdm', (Int('minLv'), Int('maxLv')), RALL, BASE, '所有机器人升级至随机等级', ALLSIDE, GOD_GROUPS)
def allbotTestbirdLevelUpRdm(su, minLv, maxLv):
    import random

    minLv = max(1, minLv)
    maxLv = max(minLv, maxLv)
    avatarList = utils.getEntityList("Avatar")
    for avatar in avatarList:
        if not avatar.isBotBase:
            continue
        avatar.runGmCommand('$setlv 0 {}'.format(random.randint(minLv, maxLv)))


# ----------------------------------------------------------------------------------------------------------------
@gm_cmd('$botToPos', (Player("gbId/Id"), Int('posType'), Int('back')), RARG(0), CELL, '机器人传到指定位置', ALLSIDE, GOD_GROUPS)
def botToPos(su, player, posType, back):
    import Math

    dstPosList = []
    if posType == 1:
        dstPosList = [Math.Vector3(7683, 208.5, 4632)]

    elif posType == 2:
        dstPosList = [Math.Vector3(6578, 166.03, 4603),
                      Math.Vector3(6730.313, 166.09, 4603), Math.Vector3(6650, 166.14, 4603)]
    elif posType == 3:
        dstPosList = [Math.Vector3(6578, 166.03, 4603),
                      Math.Vector3(6730.313, 166.09, 4603), Math.Vector3(6650, 166.14, 4603),
                      Math.Vector3(5680, 165, 4048), Math.Vector3(5586.7, 164.3221, 4067), Math.Vector3(5532, 163.4, 4001),
                      Math.Vector3(5266, 196, 4176), Math.Vector3(5260, 176.7, 4069), Math.Vector3(5235, 165, 3949)
                      ]

    if not back:
        player.position = dstPosList[random.randint(0, len(dstPosList) - 1)]
        posList = player.getRandomPoints(player.position, 80, 1, 0)
        if posList:
            pos = posList[0]
            pos = (pos[0], player.position[1], pos[2])
        else:
            pos = player.position
        player.position = pos
    else:
        avatarList = utils.getEntityList("Avatar")
        for avatar in avatarList:
            if not avatar.isClientBot():
                continue
            posList = player.getRandomPoints(dstPosList[random.randint(0, 2)], 80 , 1, 0)
            if posList:
                pos = posList[0]
                pos = (pos[0], player.position[1], pos[2])
            else:
                pos = avatar.position
            avatar.position = pos
    return True, '执行成功'


@gm_cmd('$botMove', (Int('mode'),), RALL, CELL, '所有机器人开始移动', ALLSIDE, GOD_GROUPS)
def startAllBotMove(su, mode):
    import Math

    avatarList = utils.getEntityList("Avatar")
    avatars = []
    for avatar in avatarList:
        if not avatar.isClientBot():
            continue
        avatars.append(avatar)

    for avatar in avatars:
        if mode == 1:  # 开始移动
            if avatar.position[0] > 6400 and avatar.position[0] < 7000:
                dstPos = Math.Vector3(6669, 166.1, 4601)
                avatar.botMoveTo(avatar.id, dstPos)
        else:
            if avatar.position[0] > 6400 and avatar.position[0] < 7000:
                avatar.botStopMove(avatar.id)


@gm_cmd('$botCall', (Int('num'), Int('type'), Float('x'), Float('y'), Float('z'),), RALL, CELL, '召集指定数量的机器人到一个位置', ALLSIDE, GOD_GROUPS)
def botCall(su, num, type, x, y, z):
    avatarList = utils.getEntityList("Avatar")
    num = min(num, len(avatarList))
    if not num:
        return

    avatars = []
    for avatar in avatarList:
        if not avatar.isClientBot():
            continue
        if type == 1:
            if  avatar.position[0] > 6400 and avatar.position[0] < 7000:
                avatars.append(avatar)
        if type == 2:
            if  avatar.position[0] > 5000 and avatar.position[0] < 6000:
                avatars.append(avatar)
        if type == 3:
            if  avatar.position[0] > 7000 and avatar.position[0] < 8000:
                avatars.append(avatar)

    num = min(num, len(avatars))
    regionDesPosition = (x, y, z)
    for avatar in random.sample(avatars, num):
        posList = avatar.getRandomPoints(regionDesPosition, 80, 1, 0)
        if posList:
            pos = posList[0]
            pos = (pos[0], y, pos[2])
        else:
            pos = regionDesPosition

        avatar.position = pos


@gm_cmd('$botStartFight', (Int('mode'),), RALL, CELL, '机器人切换战斗模式', ALLSIDE, GOD_GROUPS)
def botStartFight(su, mode):
    avatarList = utils.getEntityList("Avatar")
    for avatar in avatarList:
        if not avatar.isClientBot():
            continue
        if avatar.position[0] < 7000 or avatar.position[0] > 8000:
            continue
        if mode == 1:
            avatar.switchPKModel(avatar.id, gameconst.PKModel.ATTACK)
            avatar.startAutoCombat(avatar.id,False)
        else:
            avatar.stopAutoCombat(avatar.id)
            avatar.switchPKModel(avatar.id, gameconst.PKModel.PEACE)

@gm_cmd('$botStartFightMode', (Player("gbId/Id"), Int('mode')), RARG(0), CELL, '机器人开始战斗模式', ALLSIDE, GOD_GROUPS)
def botStartFightMode(su, player, mode):
    if mode == 1:
        return True, '开始战斗'
    else:
        return True, '停止战斗'

@gm_cmd('$botStartRunMode', (Player("gbId/Id"), Int('mode')), RARG(0), BASE, '机器人开始跑图模式', ALLSIDE, GOD_GROUPS)
def botStartRunMode(su, player, mode):
    if mode == 1:
        return True, '开始跑图'
    else:
        return True, '停止跑图'


@gm_cmd('$botSwitchLine', (Int('number'), Int('line'),), RSU, BASE, '机器人选择分线', INSIDE, GOD_GROUPS)
def botSwitchLine(su, number, line):
    avatarList = utils.getEntityList("Avatar")
    if number and number <= len(avatarList):
        avatarList = random.sample(avatarList, number)
    for avatar in avatarList:
        if not avatar.isBotBase:
            continue
        avatar.runGmCommand('$switchline 0 %s' % line)
    return True, '执行成功'


@gm_cmd('$botNewbie', (), RALL, BASE, '机器人跳新手', ALLSIDE, GOD_GROUPS)
def botNewbie(su):
    avatarList = utils.getEntityList("Avatar")
    for avatar in avatarList:
        if not avatar.isBotBase:
            continue

        avatar.runGmCommand('$finishNewbie 0 0')

@gm_cmd('$kickAllBot', (), RALL, BASE, '所有机器人踢下线', ALLSIDE, GOD_GROUPS)
def kickAllBot(su):
    import gameglobal
    avatarList = utils.getEntityList("Avatar")
    for avatar in avatarList:
        if not avatar.isBotBase:
            continue

        if not avatar.hasClient:
            continue

        avatar.destroySelf(gameconst.AVATAR_OFFLINE_REASON_GMKICK)

    return True, '执行成功'

@gm_cmd('$allBotStartRandomTeleport', (), RALL, BASE, '所有机器人开始随机传送', ALLSIDE, GOD_GROUPS)
def allBotStartRandomTeleport(su):
    avatarList = utils.getEntityList("Avatar")
    for avatar in avatarList:
        if not avatar.isBotBase:
            continue

        if not avatar.hasClient:
            continue

        avatar.client.randomTeleport()
    return True, '执行成功'

@gm_cmd('$debugPlayerAreaNum', (Int('lineType'), ), RONE, BASE, '打印分线人数调试信息', ALLSIDE, GOD_GROUPS)
def debugPlayerAreaNum(su, lineType):
    import gameengine
    gameengine.getLineStub(lineType).debugPlayerAreaInfo()
    return True, '执行成功'
