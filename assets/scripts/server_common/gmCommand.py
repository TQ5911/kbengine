# -*- coding: utf-8 -*-
'''
新GM指令系统说明文档

所有的GM指令需要用@gm_cmd进行修饰，会自动把被该装饰器修饰的函数变为GM指令

def gm_cmd(cmds, args, route, component, desc, kind, side, groups, pub) 参数说明：

cmds:    GM指令列表，可以是tuple of str(别名)，或者单独一个str:
    例子：('$teleport', '$goto') or '$teleport'

args:    参数列表，类型在本文件中定义，可以是 Int, Str, Float, Python, BaseEntity, CellEntity,
    Entity, Player等类型。这些类的构造函数第一个参数一般是该参数的描述，用于在$help中显示。
    具体的类型有不同的构造参数。比如Int('spaceNo', min=10, max=20)则定义了一个最小值为10，
    最大值为20的Int型参数。
    Int, Str, Float: 为普通类型参数，不做多余说明，看该类的构造参数列表即可。
    Python: 任意类型参数，仅限于forwarCommand时使用，所谓的forwarCommand即一个GM指令内部调
        用另一个GM指令。具体可以参考$come指令。
    BaseEntity, CellEntity, Entity: 用户输入该Entity的EntityID，则底层会自动找到这个Entity的
        mailbox传给GM指令使用，输入0代表su自己。BaseEntity表示要该Entity的base mailbox，
        CellEntity则要cell mailbox。在base中，Entity=BaseEntity, 在cell中，Entity=CellEntity。
        当route参数为RARG时，这个参数会自动从mailbox转变为Entity再传入GM指令。
        当指定的Entity找不到时，会自动提示错误而不继续调用GM指令。
    Player: 用户输入角色名或Avatar的EntityID，则底层会自动把该Avatar的base mailbox传入给GM指令。
        与Entity参数不同，不管在cell还是base，这里都只传入Avatar的base mailbox。当指定的
        Avatar找不到或不在线时，会自动提示错误而不继续调用GM指令。输入0代表su自己。
        如果把该参数的第二个构造参数raw=True，则当该玩家存在但是不在线时，会用该Avatar的
        角色名作为参数传入GM指令。需要配合isRawPlayer函数使用。当raw=True时不允许通过
        输入EntityID来调用该指令。
        以后就不需要同一个功能各写一份xxxByName和xxxByID了，直接写一个xxx，name和id都可以用。

route:    路由模式，定义了该GM指令需要在哪个App中执行。包括：
    RSU:    该GM指令会自动在su所在的BaseApp或CellApp运行(Base or Cell取决于component参数)，
        并且su会自动转换为Avatar而不再是mailbox传入GM指令。此路由模式只允许在side=gmAdmin.INSIDE
        时使用。(因为GmProxy不是真的Entity，没有对应的mailbox和Entity)
    RONE:    在任意一个BaseApp或CellApp中运行该GM指令，基于GmProxy的指令多用这种。
    RALL:    在所有的BaseApp或CellApp中运行该GM指令。
    RARG:    该类型需要指定参数，比如RARG(0)。意思是，在第0个参数对应的Entity所在App运行该
        GM指令。这要求这个参数必须是Entity或者Player。同时，这个参数会被转换为Entity传入
        GM指令。
    RSTUB:    该类型需要指定参数，比如RSTUB('ClanStub')。使用了这种路由模式的GM指令，会在这个
        Stub所在的BaseApp运行，并且会自动在函数的第二个参数处插入该Stub的Entity(跟在su后面)

component: gameconst.BASE/gameconst.CELL，定义了该GM指令是在base跑还是cell跑。如果需要既在cell又在base跑，可以用后面
    介绍的forwardCommand。

desc:    该指令的功能描述。同时会在$help中显示。
kind:    指令分类，PERSONAL, P_MANAGE ...
side:    gmAdmin.INSIDE/gmAdmin.OUTSIDE/gmAdmin.ALLSIDE 默认是INSIDE
groups:    权限控制，允许执行该GM指令的权限组。推荐使用DEV_GROUPS/GM_GROUPS/GM_GROUPS/PUB_GROUPS等预
    先定义好的组。默认是DEV_GROUPS。
pub:    False/True，如果是False，则该指令不允许在正式服务器使用，否则则允许。默认是False。

pushCommand: 使用该函数可以在GM指令内部调用另一个GM指令。$come, $ps等指令都用到了该功能。
    所有GM指令都可以用pushCommand来进行内部调用，但是只有$_开头的指令才允许使用Python类型参数，
    该类型参数允许直接使用任意类型的参数调用GM指令。比如需要传递个mailbox什么的...

GM指令可以直接用return '执行成功',True 这样的形式来显示反馈，与su.feedbackCommandSucc('执行成功')或者
su.feedbackCommandFail('执行失败')
应用举例：
EXAMPLE 1:
@gm_cmd('$test', (Int('参数1', min=10), Str('参数2'), Float('参数3')), RSU, gameconst.CELL, '测试', GAME_M, gmAdmin.INSIDE,
    PUB_GROUPS, True)
def test(su, arg1, arg2, arg3):
    return '%d %s %f' % (arg1, arg2, arg3), True

该GM指令名为$test，有3个参数，分别是int, string, float。会在su所在在CellApp中运行，只允许在游戏内
部调用(不允许在gmtools中调用)。允许在外服使用该指令。
如果输入$test 20 GOOD 1.0，会执行成功并反馈：20 GOOD 1.0
如果输入$test 5 GOOD 1.0，会执行失败，提示：错误，10不是有效的Int(10-)，指令格式：$test Int(10-) Str Float

EXAMPLE 2:
@gm_cmd(('$teleport', '$goto'), (Float('x'), Float('y'), Float('z'), Int('spaceNo')), RSU, gameconst.CELL, '跳转(根据位置)',
    GAME_M, gmAdmin.INSIDE, PUB_GROUPS, True)
def teleport(su, x, y, z, spaceNo):
    if su.spaceNo != spaceNo:
    ...

该GM指令名为$teleport或$goto，有4个参数，会在su所在在CellApp中运行，只允许在游戏内部调用。允许在外
服使用该指令。su参数会转换为Avatar对象传入teleport函数。由于是Entity，所以可以直接访问su.spaceNo.

EXAMPLE 3:
@gm_cmd('$go', (Entity('EntityID'),), RARG(0), gameconst.CELL, '跳转(根据ID)', PERSONAL, gmAdmin.INSIDE, PUB_GROUPS, True)
def go(su, e):
    if e.IsAvatar:
        return '跳转玩家使用gobyid', False

    su.teleportByBox(e, e.spaceNo, e.position, e.direction, '', (), 0)
    x, y, z = e.position
    return '跳转到id:%d位置[%d(%d), (%.2f, %.2f, %.2f)]' % (e.id, e.spaceNo, e.spaceID, x, y, z), True

该GM指令名为$go，有1个参数Entity。由于运行环境是CELL，所以Entity参数会自动被转换为CellEntity，意思是
返回一个相应id的CellEntity的mailbox。而由于路由模式为RARG(0)，则代表该指令会在这个Entity所在的CellApp
执行，并且该Entity参数还会从mailbox转变为Entity传入GM指令。在本例中，su是一个mailbox, e是一个Entity。
所以可以直接访问e.IsAvatar，e.spaceNo等。

EXAMPLE 4:
@gm_cmd('$comebyname', (Player('角色名'),), RARG(0), gameconst.CELL, 'come玩家', P_MANAGE, gmAdmin.INSIDE, PUB_GROUPS, True)
def comeByName(su, e):
    if not e.IsAvatar:
        return '拉npc用come'
    forwardGMCommand(su, '$_comeby', e.roleName, e.base)

@gm_cmd('$_comeby', (Str('角色名'), Python('mailbox')), RSU, gameconst.CELL)
def _comeBy(su, roleName, base):
    base.teleportByBox(su, su.spaceNo, su.position, su.direction, '', (), 0)
    x, y, z = su.position
    return '玩家%s(id:%d)跳转到你的位置[%d(%d), (%.2f, %.2f, %.2f)]' % (roleName, base.id, su.spaceNo, su.spaceID, x, y, z), True

该GM指令为$comebyname，附带一个供它调用的$_comeby内部指令。$comebyname有一个参数Player，意思是用户输
入一个角色名或EntityID，底层就会自动根据该角色名找到对应的Avatar的base mailbox传入该GM指令。当角色不
存在或者不在线时，底层会直接提示错误，并且不执行该GM指令。同上个例子，由于路由模式为RARG(0)，则该指令
会在这个玩家所在的CellApp执行，并且会把这个mailbox转换为这个玩家的CellEntity传入。由于该功能需要同时
获取e.roleName和su.spaceNo，而su和Player不在同一个App。所以该GM指令需要分两步，在$comebyname中获取
e.roleName等，然后作为参数传给$_comeby指令继续另一半功能。
使用forwardCommand函数就可以在GM指令内部调用另一个GM指令，如果参数不是Int，Str，Float等常规类型，就需
要把forward的指令的参数声明为Python类型。
$_comeby指令是一个仅供GM指令内部自己调用的指令，它不会被$help显示，也不能直接被用户执行。它有2个参数，
Str，Python。Python类型表示此参数不希望底层做任何转换，直接使用forwarCommand传入的值。该指令路由模式
为RSU，表示该GM指令会在su所在的CellApp跑。su也会从mailbox升级为Entiy。所以可以直接访问su.spaceNo等。
如果指令涉及离线修改玩家数据，当玩家存在但不在线时也希望能进行操作，可以在构造Player参数时加上raw=True，
即Player('角色名', raw=True)，代表希望当该玩家不在线时，也能执行该指令。这时传入的e就会是用户输入的
原始角色名，而不是mailbox或Entity。由于无法定位该玩家所在的CellApp，RARG(0)也会退化为RONE。

以后就不需要同一个功能各写一份xxxByName和xxxByID了。直接写一个xxx，name和id都可以用。

EXAMPLE 5:
@gm_cmd('$ps', (), RSU, gameconst.BASE, '获取自己所在pythonServer', MISC, gmAdmin.INSIDE, PUB_GROUPS, True)
def ps(su):
    forwardGMCommand(su, '$_psbase')
    forwardGMCommand(su, '$_pscell')

@gm_cmd(('$_psbase', ), (), RSU, gameconst.BASE)
def _psbase(su):
    return 'gameconst.BASE：%s' % Netease.getPythonAddr()

@gm_cmd(('$_pscell', ), (), RSU, gameconst.CELL)
def _pscell(su):
    return 'gameconst.CELL：%s' % Netease.getPythonAddr()

该指令需要显示su所在的baseApp和cellApp，所以就写了$_psbase和$_pscell来分别实现base和cell部分的功能。
然后在$ps中用forwarCommand函数调用这两个指令即可。

EXAMPLE 6:
@gm_cmd('$stub-test', (), RSTUB('ClanStub'), gameconst.BASE, '测试RSTUB', MISC, gmAdmin.INSIDE, PUB_GROUPS, True)
def stubTest(su, clanStub):
    clanStub._hasExistName('xxx')

把路由模式设为RSTUB('StubName')，则会自动在该stub对应的BaseApp执行该指令。该stub参数不需要在参数列表
中列出，但是在GM函数体时会多出一个参数紧跟着su，它就是找到的stub的Entity。
是的，以后写stub的GM指令再也不用写远程函数了: )

EXAMPLE 7:
@gm_cmd('$cash', (Player('角色名', raw=True), Int('银两')), RARG(0), gameconst.BASE, '设置玩家银两', MISC, gmAdmin.ALLSIDE, PUB_GROUPS, True)
def cash(su, avatar, cash):
    if isRawPlayer(avatar):
        gbid, roleName, accountName = avatar
        sql = """UPDATE tbl_Avatar SET sm_cash=%d WHERE sm_playerName=BINARY'%s' """ %\
            (cash, Netease.mysqlEscape(roleName))
        BigWorld.executeRawDatabaseCommand(sql)
        return '执行成功[离线]，该玩家银两被设为了%d' % (cash,)
    else:
        avatar._setCash(cash, const.DC_CASH_GM)
        avatar.client.show_msg_gm('你的银两被设为了%d' % (cash,))
        return '执行成功[在线]，%s的银两被设为了%d' % (avatar.playerName, cash,)
    return

通过把Player的第二个构造参数raw设置为True，代表不管玩家在不在线，都执行该GM指令。如果玩家不在线，
则isRawPlayer(avatar)会返回True。这时avatar就是用户输入的角色的简单信息(GBID, 角色名, URS)，可以用于直接修改db。如果玩家在
线，则返回Avatar，可以直接调用它的函数进行修改。
'''
import KBEngine
import ResMgr
import gameconst
import utils
import gameengine
import gameconfig
import gameglobal
import json
import time
import userType
import gamesql
import gamelog
import random

import gmAdmin

import gmGroup
import LogTrackingMgr

from KBEDebug import *
import proto.centralLogin_pb2 as centralLogin

# --- 开发者组
# 开发者权限
GOD_GROUPS = (gmGroup.MANAGER_GROUP_GOD,)
DEV_GROUPS = (gmGroup.MANAGER_GROUP_DEV, gmGroup.MANAGER_GROUP_GOD,)

NON_GROUPS = ()

if KBEngine.component == 'baseapp':
    COMPONENT = gameconst.BASE
elif KBEngine.component == 'cellapp':
    COMPONENT = gameconst.CELL

RSU = 'RSU'
RONE = 'RONE'
RALL = 'RALL'
SELF = 'SELF'

COMMAND_SPLIT_SEP = ' '


class _DUMMY_SU(userType.UserSingleType):
    def __init__(self):
        self.id = 0
        self.spaceNo = 0
        self.who = ''
        self.accountName = ''
        self.accountRole = ''
        self.roleAccount = ''
        self.roleName = ''
        self.group = frozenset(GOD_GROUPS)

    def feedbackCommandSucc(self, msg):
        LOG_IFO('_DUMMY_SU.feedbackCommandSucc', msg)

    def feedbackCommandFail(self, msg):
        LOG_IFO('_DUMMY_SU.feedbackCommandFail', msg)


DUMMY_SU = _DUMMY_SU()


class GMAgentBase(userType.UserSingleType):
    def __getattr__(self, name):
        if name == 'base':
            return self

        if name == 'cell':
            return self

        if name == 'client':
            return self

        if name in ('id', 'spaceID',):
            return 0

        if name in ('playerName', 'roleName'):
            return self.account

        if name in ('gbID', 'gbId'):
            return 0

        return ''

    def feedbackCommandSucc(self, message):
        LOG_IFO('feedbackCommandSucc', message)

    def feedbackCommandFail(self, message):
        LOG_IFO('feedbackCommandFail', message)

    def onCommandResult(self, result, retErrMsg, resultObj):
        if type(resultObj) is dict:
            res = resultObj
        else:
            res = resultObj.__dict__ if resultObj else 'None'
        LOG_IFO('onCommandResult', result, retErrMsg, res)

    def idipCheckOpenId(self, player):
        return True

    def idipCheckAccountOpenId(self, account):
        return True


class GMAgent(GMAgentBase):
    IsAvatar = False

    def __init__(self, owner, tag, account, group=0, cmdUUID=b'', ):
        self.owner = owner
        self.account = account
        self.group = group
        self.cmdUUID = cmdUUID
        self.tag = tag

    def __getstate__(self):
        return {
            'owner': self.owner,
            'account': self.account,
            'group': self.group,
            'cmdUUID': self.cmdUUID,
            'tag': self.tag
        }

    def __setstate__(self, state):
        self.__dict__.update(state)

    def feedbackCommandSucc(self, message):
        LOG_IFO('gm command succ:', message)
        self.owner.replyCommand(self.tag, self.account, self.cmdUUID, message, 1)

    def feedbackCommandFail(self, message):
        LOG_IFO('gm command fail:', message)
        self.owner.replyCommand(self.tag, self.account, self.cmdUUID, message, 0)


class HTTPAgent(GMAgentBase):
    IsAvatar = False

    def __init__(self, owner, tag, account, group=0, cmdUUID='', seqIdStr='', cmdStr='', baseAppBox=gameglobal.localBaseApp):
        self.owner = owner
        self.account = account
        self.group = group
        self.cmdUUID = cmdUUID
        self.tag = tag
        self.seqIdStr = seqIdStr
        self.cmdStr = cmdStr
        self.baseAppBox = baseAppBox

    def __getstate__(self):
        return {
            'owner': self.owner,
            'account': self.account,
            'group': self.group,
            'cmdUUID': self.cmdUUID,
            'tag': self.tag,
            'seqIdStr': self.seqIdStr,
            'cmdStr': self.cmdStr,
            'baseAppBox': self.baseAppBox,
        }

    def __setstate__(self, state):
        self.__dict__.update(state)

    def onCommandResult(self, result, retErrMsg, resultObj):
        resultObj = resultObj or {}
        self.replyHttpCmd(result, retErrMsg, resultObj)
        LOG_IFO('onCommandResult HTTPAgent', result, retErrMsg, resultObj, self.seqIdStr, self.cmdStr, resultObj)

        if self.seqIdStr and self.cmdStr in gameconfig.httpCmdIdempotent():
            gamesql.recordAdminCmdSucc(self.seqIdStr, result, retErrMsg, resultObj)

    def feedbackCommandSucc(self, message):
        result = {}
        LOG_IFO('feedbackCommandSucc HTTPAgent', self.tag, self.cmdUUID, 0, message, result)
        self.replyHttpCmd(0, message, result)

    def feedbackCommandFail(self, message):
        result = {}
        LOG_IFO('feedbackCommandFail HTTPAgent', self.tag, self.cmdUUID, -1, message, result)
        self.replyHttpCmd(-1, message, result)

    def replyHttpCmd(self, result, retErrMsg, resultBytes):
        cmd = GM_CMDS.get(self.cmdStr)
        if cmd.route == RALL:
            self.baseAppBox.replyHttpCommand(self.owner, self.tag, self.cmdUUID, result, retErrMsg, resultBytes, self.cmdStr)
        else:
            self.owner.replyHttpCommand(self.tag, self.cmdUUID, result, retErrMsg, resultBytes)


class IDIPGMAgent(GMAgentBase):
    IsAvatar = False

    def __init__(self, owner, tag, account, cmdId, cmdUUID, requestArgs):
        self.owner = owner
        self.account = account
        self.group = gmGroup.MANAGER_GROUP_GOD
        self.cmdId = cmdId
        self.uuid = cmdUUID
        self.requestArgs = requestArgs
        self.tag = tag

    def __getstate__(self):
        return {
            'owner': self.owner,
            'account': self.account,
            'uuid': self.uuid,
            'cmdId': self.cmdId,
            'requestArgs': self.requestArgs,
            'tag': self.tag
        }

    def __setstate__(self, state):
        self.group = gmGroup.MANAGER_GROUP_GOD
        self.__dict__.update(state)

    def onCommandResult(self, result, retErrMsg, resultObj):
        if result == 0 and hasattr(self.requestArgs, 'Serial'):
            gamesql.recordIDIPCmdSucc(self.requestArgs.Serial)
        resultBytes = resultObj.toJsonBytes() if resultObj else b''
        self.owner.replyIDIPCommand(self.tag, self.uuid, result, retErrMsg, resultBytes)

    def idipCheckOpenId(self, player):
        if isRawPlayer(player):
            gbid, roleName, accountName, dbid, lv, school = player
        else:
            accountName = player.accountName if KBEngine.component == 'baseapp' else player.roleAccount

        if self.requestArgs.OpenId != accountName:
            self.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_NOT_EXISTS, '', None)
            return False

        return True

    def idipCheckAccountOpenId(self, account):
        if isRawAccount(account):
            accountName = utils.fetchAccountTypeAndName(account)[1]
        else:
            accountName = account.accountName

        if self.requestArgs.OpenId != accountName:
            self.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_NOT_EXISTS, '', None)
            return False

        return True


def RARG(index):
    assert (type(index) is int and index >= 0)
    return index


def RSTUB(stub):
    assert (type(stub) is str)
    return stub


def _isRARG(r):
    return type(r) is int


def _isRSTUB(r):
    return type(r) is str and r not in (RSU, RONE, RALL, SELF)


class ConvertError(Exception):
    pass


class GmCmdArg(object):
    def __init__(self, desc):
        self.desc = desc
        self.data = ""

    def getDesc(self):
        return self.desc

    def convert(self, data):
        raise RuntimeError('Not implemented!')

    def getTypeDesc(self):
        raise RuntimeError('Not implemented!')

    def getFullDesc(self):
        return '%s(%s)' % (self.getDesc(), self.getTypeDesc())

    def getDefault(self):
        raise RuntimeError('Not implemented!')

    def getErrorStr(self, data):
        return '%s 不是有效的 %s' % (data, self.getTypeDesc())

    def toStr(self, value):
        return str(value)

    def toString(self):
        return str(self.data)


class Int(GmCmdArg):
    def __init__(self, desc, min=None, max=None, range=None, default=0):
        super(Int, self).__init__(desc)

        self.min = min
        self.max = max
        self.range = range
        self.default = default
        self.data = str(default)

    def convert(self, data):
        try:
            d = int(data)
        except:
            raise ConvertError(self.getErrorStr(data))

        if self.min != None and d < self.min:
            raise ConvertError(self.getErrorStr(data))

        if self.max != None and d > self.max:
            raise ConvertError(self.getErrorStr(data))

        if self.range != None and d not in self.range:
            raise ConvertError(self.getErrorStr(data))
        self.data = data
        return d

    def getTypeDesc(self):
        extra = ''
        if self.min != None or self.max != None:
            extra = '['
            if self.min != None:
                extra += str(self.min)
            extra += '-'
            if self.max != None:
                extra += str(self.max)
            extra += ']'
        elif self.range != None:
            extra = repr(list(self.range)).replace(' ', '')
        return 'Int' + extra

    def getDefault(self):
        return self.default


class Str(GmCmdArg):
    def __init__(self, desc, default=''):
        super(Str, self).__init__(desc)

        self.default = default
        self.data = str(default)

    def convert(self, data):
        if type(data) != str:
            raise ConvertError(self.getErrorStr(data))
        self.data = data
        return data

    def getTypeDesc(self):
        return 'Str'

    def getDefault(self):
        return self.default


class TimeStr(GmCmdArg):
    def __init__(self, desc):
        super(TimeStr, self).__init__(desc)

    def convert(self, data):
        if type(data) != str:
            raise ConvertError(self.getErrorStr(data))
        try:
            self.data = int(time.mktime(time.strptime(data, '%Y.%m.%d.%H.%M.%S')))
        except:
            raise ConvertError("%s is not a valid time str. eg.[2015.9.9.20.0.0]" % (data,))
        return self.data

    def getTypeDesc(self):
        return 'TimeStr'

    def getDefault(self):
        return utils.curTS()


class Float(GmCmdArg):
    def __init__(self, desc, min=None, max=None, default=0.0):
        super(Float, self).__init__(desc)

        self.min = min
        self.max = max

        self.default = default
        self.data = str(default)

    def convert(self, data):
        try:
            d = float(data)
        except:
            raise ConvertError(self.getErrorStr(data))

        if self.min != None and d < self.min:
            raise ConvertError(self.getErrorStr(data))

        if self.max != None and d > self.max:
            raise ConvertError(self.getErrorStr(data))

        self.data = data
        return d

    def getTypeDesc(self):
        extra = ''
        if self.min != None or self.max != None:
            extra = '['
            if self.min != None:
                extra += str(self.min)
            extra += '-'
            if self.max != None:
                extra += str(self.max)
            extra += ']'
        return 'Float' + extra

    def getDefault(self):
        return self.default


class Rgba(GmCmdArg):
    def __init__(self, desc):
        super(Rgba, self).__init__(desc)

    def convert(self, data):
        try:
            r, g, b, a = data.split(',')
            rgba = '%d,%d,%d,%d' % (int(r), int(g), int(b), int(a))
        except:
            raise ConvertError(self.getErrorStr(data))
        self.data = data
        return rgba

    def getTypeDesc(self):
        return 'R,G,B,A'

    def getDefault(self):
        return '255,255,255,255'


class Python(GmCmdArg):
    def __init__(self, desc):
        super(Python, self).__init__(desc)

    def convert(self, data):
        self.data = str(data)
        return data

    def getTypeDesc(self):
        return 'Python'

    def getDefault(self):
        return ''

    def toStr(self, value):
        return 'python'


class EntityArg(GmCmdArg):
    def getEntity(self, arg):
        raise RuntimeError('Not implemented!')

    def checkValue(self, arg, value):
        raise RuntimeError('Not implemented!')

    def getComponent(self):
        raise RuntimeError('Not implemented!')


class NormalEntityArg(EntityArg):
    def __init__(self, desc, extra=None):
        super(NormalEntityArg, self).__init__(desc)

        if extra and not (type(extra) is tuple and len(extra) == 2):
            raise RuntimeError('Wrong extra %s' % (extra,))

        self.extra = extra

    def convert(self, data):
        if self.extra:
            return data

        try:
            # 处理@开头的玩家Entity
            if data.startswith("@"):
                int(data[1:])
            else:
                int(data)
        except:
            raise ConvertError(self.getErrorStr(data))
        self.data = data
        return data

    def getTypeDesc(self):
        if self.extra:
            return 'Str'
        else:
            return 'Int/@数字'

    def getDefault(self):
        if self.extra:
            return ''
        else:
            return 0

    def checkValue(self, arg, value):
        if type(value) in (int, str):
            if self.extra:
                return 'Entity(%s:%s=%s)不存在' % (self.extra[0], self.extra[1], arg)
            else:
                return 'Entity(%s)不存在' % (arg,)
        return ''

    def getEntity(self, arg):
        ent = None
        if hasattr(arg, 'id'):
            ent = KBEngine.entities.get(arg.id)
        if not _isEntityExist(ent):
            return None
        return ent

    def getMailBox(self, uid, index, gbId):
        gbId = int(gbId)
        gameengine.getGlobalBase('PlayerStub').gmLookUpAvatar(gameglobal.localBaseApp, \
                                                               gbId, uid, index, False)


class CellEntity(NormalEntityArg):
    def __init__(self, desc, extra=None):
        super(CellEntity, self).__init__(desc, extra)

    def getComponent(self):
        return gameconst.CELL


class BaseEntity(NormalEntityArg):
    def __init__(self, desc, extra=None):
        super(BaseEntity, self).__init__(desc, extra)

    def getComponent(self):
        return gameconst.BASE


# 不是一个GmCmdArg，而是一个proxy
class Entity(object):
    def __init__(self, desc, extra=None):
        self.desc = desc
        self.extra = extra

    def getArg(self, component):
        if component == gameconst.BASE:
            return BaseEntity(self.desc, self.extra)
        elif component == gameconst.CELL:
            return CellEntity(self.desc, self.extra)
        raise Exception()


class MgrStub(GmCmdArg):
    def __init__(self, desc):
        super(MgrStub, self).__init__(desc)

    def convert(self, data):
        raise RuntimeError('Not implemented!')

    def getTypeDesc(self):
        raise RuntimeError('Not implemented!')

    def getEntity(self, arg):
        raise RuntimeError('Not implemented!')


class Player(EntityArg):
    def __init__(self, desc, raw=False):
        super(Player, self).__init__(desc)

        # raw为True代表当这个玩家不在线时，返回该玩家名，而不做错误处理
        # 一般用于需要离线操作的指令，配合isRawPlayer函数使用。
        self.raw = raw

    def convert(self, data):
        if self.raw and not utils.isEntityId(data):
            # 只有gbid, rolename支持离线模式
            if data != '0' and not (utils.isGbId(data) or utils.checkRoleName(data)):
                raise ConvertError(self.getErrorStr(data))
        self.data = data
        return data

    def getTypeDesc(self):
        if self.raw:
            return '汉字/Long'
        else:
            return '汉字/Int/Long'

    def getDefault(self):
        return ''

    def getMailBox(self, uid, index, gbId):
        gbId = int(gbId)
        gameengine.getGlobalBase('PlayerStub').gmLookUpAvatar(gameglobal.localBaseApp, \
                                                               gbId, uid, index, self.raw)

    def getComponent(self):
        return gameconst.BASE

    def checkValue(self, arg, value):
        if value == False:
            return '角色(%s)不存在' % (arg,)
        if value == True:
            return '角色(%s)不在线' % (arg,)
        if not self.raw and type(value) is str:
            return '角色(e_rolename:%s)不存在' % (arg,)
        if not self.raw and utils.isGbId(value):
            return '角色(e_gbid:%d)不存在' % (arg,)
        if self.raw and utils.isEntityId(value):
            return '角色(e_eid:%s)不存在' % (arg,)
        return ''

    def getEntity(self, arg):
        if isRawPlayer(arg):
            return arg

        ent = None
        if arg.__class__.__name__ == 'EntityCall':
            ent = KBEngine.entities.get(arg.id)
        elif isinstance(arg, (KBEngine.Entity,)):
            ent = arg

        if not _isEntityExist(ent):
            return None

        return ent


class PlayerAccount(NormalEntityArg):
    def __init__(self, desc, raw=False):
        super(PlayerAccount, self).__init__(desc)
        self.raw = raw

    def convert(self, data):
        self.data = data
        return data

    def getTypeDesc(self):
        return 'Str'

    def getDefault(self):
        return ''

    def checkValue(self, arg, value):
        if value == False:
            return '账号(%s)不存在' % (arg,)
        if value == True:
            return '账号(%s)不在线' % (arg,)

        return ''

    def getComponent(self):
        return gameconst.BASE

    def getEntity(self, arg):
        if isRawAccount(arg):
            return arg

        ent = None
        if arg.__class__.__name__ == 'EntityCall':
            ent = KBEngine.entities.get(arg.id)
        elif isinstance(arg, (KBEngine.Entity,)):
            ent = arg

        if not _isEntityExist(ent):
            return None

        return ent

    def getAccount(self, uid, index, realAccountName):
        # accountType, _ = utils.fetchAccountTypeAndName(arg)
        # if not accountType: #centralLogin.ACCOUNT_UNKNOW = 0
        #     _updateCmdArg(uid, index, None)
        #     return
        stubs = gameengine.getLoginStubsByAccountName(realAccountName)
        if stubs:
            stubs[0].gmLookUpAccount(gameglobal.localBaseApp, \
                                     realAccountName, uid, index, self.raw)


def isRawPlayer(player):
    if (type(player) is tuple or type(player) is list) and len(player) == gameconst.GM_RAW_PLAYER_FIELDS:
        return True


def isRawAccount(account):
    if type(account) is str:
        return True


def getGbIdFromRawPlayer(player):
    return player[0]


def getDbIdFromRawPlayer(player):
    return player[3]


GM_CMDS = gameglobal.GM_CMDS
GM_CMD_FUNC_NAMES = gameglobal.GM_CMD_FUNC_NAMES
GM_CMD_ARG_PERMISSION_CHECKER = gameglobal.GM_CMD_ARG_PERMISSION_CHECKER


def getSuAccount(su):
    if hasattr(su, 'who'):
        return su.who
    elif hasattr(su, 'accountName'):
        return su.accountName
    elif hasattr(su, 'roleAccount'):
        return su.roleAccount
    else:
        return None


class GmCommand(object):
    def __init__(self, name, func, args, route, kind, desc, component, side, groups, pub, minArgs, logDisable,
                 callLimitNum=0):
        self.name = name
        self.func = func
        self.args = list(args)
        self.route = route
        self.kind = kind
        self.desc = desc
        self.component = component
        self.side = side
        self.groups = frozenset(groups)
        self.pub = pub
        self.minArgs = minArgs
        self.logDisable = logDisable
        self.callLimitNum = callLimitNum

    def getRealGroup(self):
        return self.groups

    def checkPermission(self, su):
        # 如果服务器配置文件中设置不检查权限
        if not gameconfig.gmVerifyByGroup():
            return True

        return su.group in self.getRealGroup()

    def checkComponent(self):
        return self.component == COMPONENT or self.component == gameconst.ALL

    def checkPub(self):
        if not self.pub:
            return False

        return True

    def checkKind(self, kind):
        return self.kind == kind

    def checkSide(self, side):
        return self.side == gmAdmin.ALLSIDE or self.side == side

    def getCommandDesc(self):
        return '%s %s' % (self.name, ' '.join([arg.getFullDesc() for arg in self.args]))

    def getHelpInfo(self):
        args_desc = {}
        args_default = {}
        for i, arg in enumerate(self.args):
            args_desc[i] = arg.getDesc()
            args_default[i] = arg.getDefault()

        return (self.desc, args_desc, args_default)

    def getMatchInfo(self):
        return '指令:[%s, ] 作用:%s,  参数:[ %s ]' % (self.name[1:], self.desc, \
                                                      ' '.join([arg.getDesc() for arg in self.args]))

    def strArgs(self, args):
        new_args = []
        for i, arg in enumerate(self.args):
            if type(arg) is Python:
                new_args.append(args[i])
            else:
                if self.minArgs >= 0 and i >= len(args):
                    new_args.append(arg.toStr(arg.getDefault()))
                else:
                    new_args.append(arg.toStr(args[i]))
        return new_args

    # 增加了对default参数的支持
    def convertArgs(self, args, realArgs):
        error_msgs = []

        # 参数个数完全匹配或者大于等于最小参数个数
        if (self.minArgs < 0 and len(self.args) != len(args)) or (
                self.minArgs >= 0 and (len(args) < self.minArgs or len(args) > len(self.args))):
            error_msgs.append('参数个数错误')
            return error_msgs

        for i, arg in enumerate(self.args):
            try:
                if self.minArgs >= 0 and i >= len(args):
                    realArgs.append(arg.getDefault())
                else:
                    realArgs.append(arg.convert(args[i]))
            except ConvertError as inst:
                error_msgs.append(inst.args[0])

        return error_msgs

    def hasEntityArgs(self):
        for arg in self.args:
            if isinstance(arg, EntityArg):
                return True
        return False

    def getEntityArgs(self):
        args = set()
        for i, arg in enumerate(self.args):
            if isinstance(arg, EntityArg):
                args.add(i)
        return args

    def getArgMailBoxes(self, su, command, args, raw_args=None, reason=""):
        if raw_args is None:
            raw_args = []

        uid = utils.generateUUID()
        need = self.getEntityArgs()
        data = {'su': su, 'command': command, 'total': 0,
                'num': 0, 'args': args, 'need': need, 'done': set(), 'reason': reason}
        if raw_args:
            data["raw_args"] = raw_args
        gameglobal.gmCmdData[uid] = data

        pending_args = {}
        for i in need:
            arg = self.args[i]
            if isinstance(arg, EntityArg):
                if type(arg) is Player:
                    # 0代表su自己
                    if args[i] == '0':
                        _updateCmdArg(uid, i, su)
                    elif utils.isEntityId(args[i]):
                        pending_args.setdefault(arg.getComponent(), []).append(
                            (i, (int(args[i]), arg.__class__.__name__)))
                    else:
                        # 可能传入gbId(long) 或  roleName(str)
                        arg.getMailBox(uid, i, args[i])
                elif type(arg) is PlayerAccount:
                    data['total'] += _getAppCount(gameconst.BASE)
                    arg.getAccount(uid, i, args[i])
                else:
                    if arg.extra:
                        pending_args.setdefault(arg.getComponent(), []).append(
                            (i, arg.extra + (args[i], arg.__class__.__name__)))
                    elif args[i].startswith('@'):
                        arg.getMailBox(uid, i, args[i])
                    elif args[i] == '0':
                        _updateCmdArg(uid, i, su)
                    else:
                        pending_args.setdefault(arg.getComponent(), []).append(
                            (i, (int(args[i]), arg.__class__.__name__)))

        for k in pending_args.keys():
            data['total'] += _getAppCount(k)
        for k, v in pending_args.items():
            _callApps(k, 'gmCommand.findEntity', (gameglobal.localBaseApp, v, uid))

    def reportError(self, data):
        error_msgs = []
        args = _splitCommand(data['command'])[1]
        LOG_WARN('do command error:', data)
        for i in data['need']:
            arg = self.args[i]
            if isinstance(arg, Player):
                if data['args'][i] == False:
                    data['su'].onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_NOT_EXISTS, '', None)
                elif data['args'][i] == True:
                    data['su'].onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '', None)
                else:
                    data['su'].onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_NOT_EXISTS, '', None)

            elif isinstance(arg, PlayerAccount) and not data['args'][i]:
                data['su'].onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_NOT_EXISTS, '', None)

            msg = arg.checkValue(args[i], data['args'][i])
            if msg:
                error_msgs.append(msg)
        data['su'].feedbackCommandFail('错误，%s' % ('，'.join(error_msgs)))

    def checkArgValues(self, data):
        args = _splitCommand(data['command'])[1]
        for i in data['need']:
            if self.args[i].checkValue(args[i], data['args'][i]):
                return False
        return True

    def buildCmdString(self, args):
        fields = []
        fields.append(self.name)
        for i, arg in enumerate(self.args):
            if self.minArgs >= 0 and i >= len(args):
                fields.append(arg.toStr(arg.getDefault()))
            else:
                fields.append(arg.toStr(args[i]))

        return ' '.join(fields)

    def _playerLog(self, su, ent, data):
        if not self.logDisable and data != None:
            sAccount = ""
            sRoleName = ""
            if su.__class__.__name__ == "GmProxy":
                sAccount = su.who
                sRoleName = su.who

            if self.component == gameconst.CELL:
                if su.__class__.__name__ == "Avatar":
                    sAccount = su.roleAccount
                    sRoleName = su.name

                if isRawPlayer(ent):
                    pass
                elif ent.IsAvatar:
                    pass
            elif self.component == gameconst.BASE:
                if su.__class__.__name__ == "Avatar":
                    sAccount = su.accountName
                    sRoleName = su.characterName
                if isRawPlayer(ent):
                    pass
                elif ent.__class__.__name__ == "Avatar":
                    pass

    def _gmCallback(self, data, name):
        if not data or not name:
            return

        uid = data.get('uid')
        target = data.get('target')
        if not uid or not target:
            return

        func = getattr(target, data.get(name), None)
        if func:
            func(uid)

    def do(self, su, args, data=None):
        if not self.checkComponent():
            return
        stub = None

        if self.route == RSU:
            su = KBEngine.entities.get(su.id)
            if not _isEntityExist(su):
                self._gmCallback(data, 'failCallback')
                return

        elif self.route == RONE:
            # if self.component == gameconst.BASE and not gameengine.isFirstBaseApp():
            #     return
            if self.component == gameconst.CELL and not gameengine.isFirstCellApp():
                return
        elif self.route == RALL:
            pass

        elif _isRARG(self.route):
            index = self.route
            ent = self.args[index].getEntity(args[index])

            if type(self.args[index]) is Player:
                if isRawPlayer(ent):
                    if self.component == gameconst.BASE and not gameengine.isFirstBaseApp():
                        self._gmCallback(data, 'failCallback')
                        return
                    if self.component == gameconst.CELL and not gameengine.isFirstCellApp():
                        self._gmCallback(data, 'failCallback')
                        return
                elif not _isEntityExist(ent):
                    self._gmCallback(data, 'failCallback')
                    return

            if type(self.args[index]) is PlayerAccount:
                if isRawAccount(ent):
                    if self.component == gameconst.BASE and not gameengine.isFirstBaseApp():
                        self._gmCallback(data, 'failCallback')
                        return
                elif not _isEntityExist(ent):
                    self._gmCallback(data, 'failCallback')
                    return

            if isinstance(self.args[index], (Entity, CellEntity, BaseEntity)):
                if not _isEntityExist(ent):
                    self._gmCallback(data, 'failCallback')
                    return

            args[index] = ent

        elif _isRSTUB(self.route):
            base = gameengine.getGlobalBase(self.route)
            stub = KBEngine.entities.get(base.id)
            if not stub:
                return
        try:
            pl = None
            for arg in args:
                if isRawPlayer(arg):
                    pl = arg
                    break
                elif arg.__class__.__name__ == "Avatar":
                    pl = arg
                    break
            if pl:
                self._playerLog(su, pl, data)

            if stub:
                ret = self.func(su, stub, *args)
            else:
                ret = self.func(su, *args)

            if type(ret) is bool:
                if ret:
                    su.feedbackCommandSucc('执行 %s 成功' % (self.name,))
                else:
                    su.feedbackCommandFail('执行 %s 失败' % (self.name,))
            elif type(ret) is str:
                raise Exception("GM指令(%r)返回参数错误, 正确格式(msg, succ)" % (self.name,))
            elif type(ret) is tuple:
                if len(ret) == 2:
                    succ, msg = ret
                    if succ:
                        su.feedbackCommandSucc(msg)
                    else:
                        su.feedbackCommandFail(msg)
                else:
                    raise Exception("GM指令(%r)返回参数错误, 正确格式(msg, succ)" % (self.name,))
            self._gmCallback(data, 'succCallback')
        except Exception as e:
            import sys
            gameengine.exceptHook(*sys.exc_info())
            LOG_ERR('do command failed:', e)
            su.feedbackCommandFail('服务端指令执行 %s 失败, 执行没有生效, 请联系服务端开发' % (self.name))


def findEntity(base, args, uid):
    result = []
    for i, t in args:
        if len(t) == 2:
            arg, argType = t
            if type(arg) is int:
                if arg > gameconst.GBID_BASE:
                    # 是GBID
                    ent = _findEntityByGbId(arg)
                    if ent:
                        result.append((i, ent))
                else:
                    # 是普通的entityId
                    ent = KBEngine.entities.get(arg)
                    if _isEntityExist(ent):
                        if argType == 'Player':
                            if ent.__class__.__name__ == 'Avatar':
                                result.append((i, ent))
                            else:
                                pass
                        else:
                            result.append((i, ent))

        else:
            ent_type, prop_name, prop, argType = t
            pass
    base.onGmFindEntity(result, uid)


def _findEntityByGbId(gbId):
    if KBEngine.component == 'baseapp':
        for e in KBEngine.entities.values():
            if hasattr(e, 'gbID') and e.gbID == gbId and _isEntityExist(e):
                return e
    elif KBEngine.component == 'cellapp':
        for e in KBEngine.entities.values():
            if hasattr(e, 'gbId') and e.gbId == gbId and _isEntityExist(e):
                return e
    return None


def onFindEntity(result, uid):
    data = gameglobal.gmCmdData.get(uid)
    if not data:
        return

    for i, val in result:
        _updateCmdArg(uid, i, val)

    data['num'] += 1
    if data['num'] >= data['total']:
        gameglobal.gmCmdData.pop(uid, None)
        if data['done'] != data['need']:
            cmd = _getCommand(data['command'])
            cmd.reportError(data)


def onLookUpAvatar(base, role, uid, index, raw):
    if base == True and raw:
        gbid, roleName, accoutName, dbid = role
        t = gbid, roleName, accoutName, dbid
        _updateCmdArg(uid, index, t)
    else:
        _updateCmdArg(uid, index, base)


def onFindAccount(result, realAccountName, index, raw, uid):
    data = gameglobal.gmCmdData.get(uid)
    if not data:
        return

    if result:
        _updateCmdArg(uid, index, result)
        gameglobal.gmCmdData.pop(uid, None)
    else:
        accountType, accName = utils.fetchAccountTypeAndName(realAccountName)
        if accountType == centralLogin.ACCOUNT_UNKNOW:
            sql = "select accountName from kbe_accountinfos where accountName = {} or accountName={}".format(
                utils.escape_string(realAccountName), utils.escape_string(accName))
        else:
            sql = "select accountName from kbe_accountinfos where accountName = {}".format(
                utils.escape_string(realAccountName))

        KBEngine.executeRawDatabaseCommand(sql,
                                           lambda ret, num, insertId, err: _queryAccountNameCallback(ret, num, insertId,
                                                                                                     err, raw,
                                                                                                     realAccountName,
                                                                                                     uid, index))


def _queryAccountNameCallback(ret, num, insertId, err, raw, accountName, uid, index):
    if len(ret) == 0:
        _updateCmdArg(uid, index, False)
    else:
        if raw:
            _updateCmdArg(uid, index, accountName)
        else:
            _updateCmdArg(uid, index, True)

    gameglobal.gmCmdData.pop(uid, None)


def onBroadcastCmdSucc(uid):
    gameglobal.gmCmdData.pop(uid, None)


def onBroadcastCmdFail(uid):
    data = gameglobal.gmCmdData.get(uid)
    if not data:
        return

    cmd = _getCommand(data['command'])
    compCnt = data.get('failCompCnt', 0)
    data['failCompCnt'] = compCnt + 1
    if data['failCompCnt'] >= _getAppCount(cmd.component):
        data.pop('failCompCnt', 0)
        retryCnt = data.get('retryCnt', 0)
        if retryCnt < 3:
            data['retryCnt'] = retryCnt + 1
            LOG_ERR('zt: retry gm command', data['command'], retryCnt)
            gmBCastRealDoCommand(cmd.component, data['su'], data['command'], data['args'], data)
        else:
            data['su'].feedbackCommandFail('执行失败: ' + data['command'])
            gameglobal.gmCmdData.pop(uid, None)


def _updateCmdArg(uid, index, value):
    data = gameglobal.gmCmdData.get(uid)
    if not data:
        return
    data['args'][index] = value
    data['done'].add(index)
    if data['done'] == data['need']:
        # Netease.gmCmdData.pop(uid, None)
        cmd = _getCommand(data['command'])
        if cmd.checkArgValues(data):
            data.update({'uid': uid, 'target': gameglobal.localBaseApp, 'succCallback': 'onDoCmdSucc',
                         'failCallback': 'onDoCmdFail'})
            gmBCastRealDoCommand(cmd.component, data['su'], data['command'], data['args'], data)
        else:
            cmd.reportError(data)


def _isEntityExist(ent):
    if not ent:
        return False
    return COMPONENT != gameconst.CELL or ent.isReal()


def _callApps(component, func, args):
    if component == gameconst.BASE:
        gameengine.callBaseApps(func, args)
    elif component == gameconst.CELL:
        gameengine.callCellApps(func, args)
    else:
        gameengine.callBaseApps(func, args)
        gameengine.callCellApps(func, args)


def _getAppCount(component):
    if component == gameconst.BASE:
        app_count = gameconfig.baseAppCount()
    else:
        app_count = gameconfig.cellAppCount()

    return app_count


def _getCommand(command):
    return GM_CMDS.get(command.split(COMMAND_SPLIT_SEP)[0])


def _splitCommand(command):
    fields = command.split(COMMAND_SPLIT_SEP)
    return fields[0], fields[1:]


def _getFirstArg(command):
    return command.split(COMMAND_SPLIT_SEP)[1]


def _isForwardCommand(command):
    return command.startswith('$_')


def _lowerCommand(command):
    cmd_name, cmd_args = _splitCommand(command.strip())
    if not cmd_args:
        return cmd_name.lower()
    return cmd_name.lower() + ' ' + ' '.join(cmd_args)


def _isMatchCommand(command):
    cmd_name, cmd_args = _splitCommand(command.strip())
    return not cmd_args and len(cmd_name) > 1 and cmd_name[-1] == '$'


# decorator for gm commands
def gm_cmd(cmds, args, route, component, desc='', side=gmAdmin.INSIDE, groups=DEV_GROUPS, pub=False, minArgs=-1,
           logDisable=False, callLimitNum=0):
    if type(cmds) is str:
        cmds = (cmds,)
    assert (type(cmds) is tuple)
    assert (type(args) is tuple)
    assert (route in (RSU, RONE, RALL, SELF) or _isRARG(route) or _isRSTUB(route))
    assert (component in (gameconst.CELL, gameconst.BASE, gameconst.ALL))
    assert (side in (gmAdmin.INSIDE, gmAdmin.OUTSIDE, gmAdmin.ALLSIDE))
    assert (pub in (True, False))

    if route == RSU:
        assert (side == gmAdmin.INSIDE)
    elif _isRARG(route):
        assert (route < len(args))
        assert (isinstance(args[route], EntityArg) or type(args[route]) is Entity or isinstance(args[route], MgrStub))
    elif _isRSTUB(route):
        assert (component == gameconst.BASE)

    has_python_arg = False
    args = list(args)
    for i, arg in enumerate(args):
        if type(arg) is Python:
            has_python_arg = True
        elif type(arg) is Entity:
            args[i] = arg.getArg(component)
        else:
            assert (isinstance(arg, GmCmdArg))

    def _gm_cmd(func):
        global GM_CMDS
        global GM_CMD_FUNC_NAMES

        func_name = func.__name__
        if func_name in GM_CMD_FUNC_NAMES:
            raise RuntimeError('GM command func %s duplicated!' % (func_name,))
        GM_CMD_FUNC_NAMES.add(func_name)

        for cmd_name in cmds:
            cmd_name = cmd_name.lower()
            assert (len(cmd_name) > 1 and cmd_name[0] == '$')
            if has_python_arg and not _isForwardCommand(cmd_name):
                raise RuntimeError('CM command %s error! Only internal command can use Python arg' % \
                                   (cmd_name,))

            if cmd_name in GM_CMDS:
                raise RuntimeError('GM command %s duplicated!' % (cmd_name,))

            GM_CMDS[cmd_name] = GmCommand(cmd_name, func, args, route, '', \
                                          desc, component, side, groups, pub, minArgs, logDisable,
                                          callLimitNum=callLimitNum)

        return func

    return _gm_cmd


############################################
# 用于runscript更新或添加gm指令
# 注意：与@gm_cmd相比，增加了第一个参数为类型，如在ITEM.py的gm指令则为gmAdmin.ITEM，直接将带有decorator的指令放在run_in_cell()和run_in_base()就可以了。
############################################
''' 例如
def run_in_base():
    import gmAdmin
    @update_gm_cmd(gmAdmin.ITEM, '$itemrecoverbyid', (Player('角色名', raw=True), Int('组操作号'), Int('物品id'), Int('物品数量'), Str('guid'), Int('Cash')), RARG(0), gameconst.CELL,\
        '恢复无镜像道具', gmAdmin.ALLSIDE, OM_DEV_EX_GROUPS, True)
    def itemRecoverById(su, e, op_nuid, itemId, itemNum, guid, cash):
        pass
    pass

def run_in_cell():
    import gmAdmin
    @update_gm_cmd(gmAdmin.ITEM, '$itemrecoverbyid', (Player('角色名', raw=True), Int('组操作号'), Int('物品id'), Int('物品数量'), Str('guid'), Int('Cash')), RARG(0), gameconst.CELL,\
        '恢复无镜像道具', gmAdmin.ALLSIDE, OM_DEV_EX_GROUPS, True)
    def itemRecoverById(su, e, op_nuid, itemId, itemNum, guid, cash):
        pass
    pass
'''


def update_gm_cmd(kind, cmds, args, route, component, desc='', side=gmAdmin.INSIDE, groups=DEV_GROUPS, pub=False,
                  minArgs=-1, logDisable=False):
    if type(cmds) is str:
        cmds = (cmds,)
    assert (type(cmds) is tuple)
    assert (type(args) is tuple)
    assert (type(kind) is str)
    assert (route in (RSU, RONE, RALL, SELF) or _isRARG(route) or _isRSTUB(route))
    assert (component in (gameconst.CELL, gameconst.BASE))
    assert (side in (gmAdmin.INSIDE, gmAdmin.OUTSIDE, gmAdmin.ALLSIDE))
    assert (pub in (True, False))

    if route == RSU:
        assert (side == gmAdmin.INSIDE)
    elif _isRARG(route):
        assert (route < len(args))
        assert (isinstance(args[route], EntityArg) or type(args[route]) is Entity)
    elif _isRSTUB(route):
        assert (component == gameconst.BASE)

    has_python_arg = False
    args = list(args)
    for i, arg in enumerate(args):
        if type(arg) is Python:
            has_python_arg = True
        elif type(arg) is Entity:
            args[i] = arg.getArg(component)
        else:
            assert (isinstance(arg, GmCmdArg))

    def _gm_cmd(func):
        global GM_CMDS
        global GM_CMD_FUNC_NAMES

        func_name = func.__name__
        if func_name not in GM_CMD_FUNC_NAMES:
            GM_CMD_FUNC_NAMES.add(func_name)

        for cmd_name in cmds:
            cmd_name = cmd_name.lower()
            assert (len(cmd_name) > 1 and cmd_name[0] == '$')
            if has_python_arg and not _isForwardCommand(cmd_name):
                raise RuntimeError('CM command %s error! Only internal command can use Python arg' % \
                                   (cmd_name,))

            GM_CMDS[cmd_name] = GmCommand(cmd_name, func, args, route, '', \
                                          desc, component, side, groups, pub, minArgs, logDisable)

        return func

    return _gm_cmd


def isGMCommand(command):
    cmd_name = _splitCommand(command)[0].lower()
    return cmd_name in ('$help', '$helpkind') or _isMatchCommand(command) or cmd_name in GM_CMDS


def _exportAllCommands(fn=None):
    pass


# 显示拥有权限的GM指令集
def _showHelp(su):
    resDecs = []
    # 新指令
    for cmd in GM_CMDS.values():
        if cmd.checkPermission(su) and cmd.checkPub() and not _isForwardCommand(cmd.name) and cmd.desc != "No Desc":
            resDecs.append("%s:%s" % (cmd.name[1:], cmd.desc))

    if resDecs:
        su.client.sendGmMsg(resDecs, 'help')


# 搜索拥有权限的GM指令集
def _showHelpSearch(su, keyword):
    cmds = []
    cmdPattern = keyword[:-1]

    for cmd in GM_CMDS.values():
        if cmd.checkPermission(su) and cmd.checkPub() and not _isForwardCommand(cmd.name) and cmd.desc != "No Desc":
            cmds.append(cmd)

    resCmd = []
    for cmd in cmds:
        side = cmd.side
        if side != gmAdmin.ALLSIDE:
            if su.id == 0 and side != gmAdmin.OUTSIDE:
                continue
            elif su.id != 0 and side != gmAdmin.INSIDE:
                continue

        if cmdPattern in cmd.name or cmdPattern in cmd.desc:
            resCmd.append('指令:%s\n作用:%s\n参数:\n%s' % (
            cmd.name, cmd.desc, '\n'.join([arg.getFullDesc() for arg in cmd.args])))

    if not resCmd:
        su.feedbackCommandFail('无效匹配')
        return True

    su.client.sendGmMsg(resCmd, 'gmmatch')


def _showHelpKind(su, kind):
    # 旧指令
    # cmds = _whatKind(su, su.roleName, su.group, kind)
    cmds = {}

    # 新指令
    for cmd_name, cmd in GM_CMDS.items():
        if cmd.checkPermission(su) and cmd.checkPub() and cmd.checkKind(kind) and not \
                _isForwardCommand(cmd_name):
            cmds[cmd_name[1:]] = cmd.getHelpInfo()

    # TODO:


#    if cmds:
#        su.transProxyData(const.PROXY_KEY_CONSOLE, ('someone_console_option', cmds))

def _showMatchCommand(su, command):
    # 旧指令
    # cmds = _matchCommand(su, su.roleName, su.group, command[1:])
    cmds = []

    # 新指令
    for cmd_name, cmd in GM_CMDS.items():
        if cmd.checkPermission(su) and cmd.checkPub() and not _isForwardCommand(cmd_name) and \
                command[:-1] in cmd_name:
            cmds.append(cmd.getMatchInfo())

    for cmd in cmds:
        su.feedbackCommandSucc(cmd)

    return


def searchCommand(su, role, group, keyword):
    # 旧指令
    # cmds = _searchCommand(su, role, group, keyword)
    cmds = {}

    # 新指令
    for cmd_name, cmd in GM_CMDS.items():
        if cmd.checkPermission(su) and cmd.checkPub() and not _isForwardCommand(cmd_name) \
                and (cmd_name.find(keyword.lower()) != -1 or cmd.desc.lower().find(keyword.lower()) != -1):
            cmds[cmd_name[1:]] = cmd.getHelpInfo()

    # TODO:
    #    su.transProxyData(const.PROXY_KEY_CONSOLE, ('someone_console_option', cmds))

    return


# 用于cell/impAdmin.py
def init():
    pass


def doCommandInside(su, command):
    LOG_IFO("doCommandInside: %s" % command)

    if len(command) <= 1:
        return

    command = _lowerCommand(command)
    cmd_name, cmd_args = _splitCommand(command)

    if _isForwardCommand(command):
        return

    _doCommand(su, command, gmAdmin.INSIDE)


def doCommandOutside(su, command, reason):
    LOG_IFO("doCommandOutside: %s" % command)

    if len(command) <= 1:
        return

    command = _lowerCommand(command)

    if _isForwardCommand(command):
        return

    _doCommand(su, command, gmAdmin.OUTSIDE, reason=reason)


def _doCommand(su, command, side, args=None, reason=""):
    cmd_name, cmd_args = _splitCommand(command)
    cmd = GM_CMDS.get(cmd_name)
    if not cmd:
        return

    if args is None:
        is_forward_cmd = False
    else:
        is_forward_cmd = True

    if is_forward_cmd:
        cmd_args = args
    else:
        if not cmd.checkPermission(su):
            su.feedbackCommandFail('权限不足')
            return

        if not cmd.checkSide(side):
            su.feedbackCommandFail('使用环境错误')
            return

    real_args = []
    error_msgs = cmd.convertArgs(cmd_args, real_args)
    if error_msgs:
        su.feedbackCommandFail('错误，%s。指令格式：%s 理由: %s' % ('、'.join(error_msgs), cmd.getCommandDesc(), reason))
        return

    # 这里检查参数与指令的合法性
    if not is_forward_cmd:
        try:
            if cmd.func.__name__ in GM_CMD_ARG_PERMISSION_CHECKER:
                if not GM_CMD_ARG_PERMISSION_CHECKER[cmd.func.__name__](su, cmd, real_args):
                    return
        except:
            import sys
            gameengine.exceptHook(*sys.exc_info())

    if not cmd.hasEntityArgs():
        gmBCastRealDoCommand(cmd.component, su, command, real_args)
    else:
        cmd.getArgMailBoxes(su, command, real_args, cmd_args, reason)
    
    
    srcStr = su.__getstate__() if hasattr(su, '__getstate__') else str(su)
    LogTrackingMgr.LogTrackingMgr.GM_GM(
        srcStr,
        cmd_name,
        ' '.join(cmd_args)
    )


# 直接在系统内部发起的GM调用，不做相关权限检查
def doCommandSystem(su, command):
    LOG_IFO("gmCommand system: %s" % command)

    cmd_name, cmd_args = _splitCommand(command)
    cmd = GM_CMDS.get(cmd_name)
    if not cmd:
        return

    real_args = []
    error_msgs = cmd.convertArgs(cmd_args, real_args)
    if error_msgs:
        su.feedbackCommandFail('错误，%s。指令格式：%s' % ('、'.join(error_msgs), cmd.getCommandDesc(),))
        return

    if not cmd.hasEntityArgs():
        gmBCastRealDoCommand(cmd.component, su, command, real_args)
    else:
        cmd.getArgMailBoxes(su, command, real_args, cmd_args, '系统内部执行')


def getBaseMailBox(comp):
    if utils.checkBaseMailBox(comp):
        return comp
    if utils.checkCellMailBox(comp):
        return comp.base

    if KBEngine.component == 'baseapp':
        return comp

    if KBEngine.component == 'cellapp':
        return comp.base


def getCellMailBox(comp):
    if utils.checkCellMailBox(comp):
        return comp

    if utils.checkBaseMailBox(comp):
        return comp.cell

    if KBEngine.component == 'cellapp':
        return comp

    if KBEngine.component == 'baseapp':
        return comp.cell


def gmBCastRealDoCommand(component, su, command, real_args, data=None):
    cmd_name = _splitCommand(command)[0]
    cmd = GM_CMDS.get(cmd_name)

    if cmd.route == RONE:
        if cmd.component == gameconst.BASE:
            baseappBox = random.choice(gameengine.getAllBaseApps())
            baseappBox.doRONECommand((su, command, real_args, data))
        else:
            _callApps(component, 'gmCommand.realDoCommand', (su, command, real_args, data))
    elif cmd.route == SELF:
        if cmd.component == gameconst.BASE:
            gameglobal.localBaseApp.doRONECommand((su, command, real_args, data))
        else:
            LOG_ERR("gmCommand route error", cmd.route, cmd.component)
    elif cmd.route == RSU or (_isRARG(cmd.route) and su == real_args[cmd.route]):
        cond = (KBEngine.component, cmd.component)
        if cmd.checkComponent():
            realDoCommand(su, command, real_args, data)
        elif cond == ('baseapp', gameconst.CELL):
            getCellMailBox(su).realDoGmCommandProxy((su, command, real_args, data))
        elif cond == ('cellapp', gameconst.BASE):
            getBaseMailBox(su).realDoGmCommandProxy((su, command, real_args, data))
        else:
            gameengine.panicStack("wrong cond %s %s" % (cond, command))
    else:
        _callApps(component, 'gmCommand.realDoCommand', (su, command, real_args, data))


def realDoCommand(su, command, args, data=None):
    cmd_name = _splitCommand(command)[0]
    GM_CMDS.get(cmd_name).do(su, args, data)


def forwardGMCommand(su, cmdName, *args):
    cmdName = cmdName.lower()
    cmd = GM_CMDS.get(cmdName)
    _callApps(gameconst.BASE, 'gmCommand.realForwardCommand', (su, cmd.buildCmdString(args), cmd.strArgs(args)))


def realForwardCommand(su, command, args):
    if gameengine.isFirstBaseApp():
        _doCommand(su, command, gmAdmin.ALLSIDE, args)


def gm_arg_permission_checker(checkFunc):
    def _gm_arg_checker(func):
        global GM_CMD_ARG_PERMISSION_CHECKER
        GM_CMD_ARG_PERMISSION_CHECKER[func.__name__] = checkFunc
        return func

    return _gm_arg_checker


# 转发到各baseapp/cellapp的gm调用
# @param su
# @param params:原始参数
# @param component: gameconst.BASE/gameconst.CELL/-1 BASE表示发送到所有的baseapp CELL表示发送到所有的cellapp -1表示发送到所有的baseapp和cellapp 如果为str表示某个baseapp/cellapp servername(ip:port)
# @param realFunc:实际执行的gm函数名，返回值类型必须为tuple(Bool,resultObj)
# @param callback:收集完所有结果后的回调函数  如果为None则简单反馈执行成功  如果为True 返回JOSN格式化的结果数组  如果出错返回JSON格式化的错误信息数组
def callServers(su, params, component, realFunc, callback):
    maxNum = 0
    if component == gameconst.BASE:
        maxNum = gameconfig.desiredBaseApps()
    elif component == gameconst.CELL:
        maxNum = gameconfig.desiredCellApps()
    else:
        maxNum = gameconfig.desiredBaseApps() + gameconfig.desiredCellApps()
    uid = 0
    if not isinstance(component, str):
        uid = utils.generateUUID()
        gameglobal.gmCmdData[uid] = {'num': 0, 'maxNum': maxNum}

    if component == gameconst.BASE:
        forwardGMCommand(su, '$_callserversbase', component, realFunc, params,
                       (gameglobal.localBaseApp, uid, callback, params))
    elif component == gameconst.CELL:
        forwardGMCommand(su, '$_callserverscell', component, realFunc, params,
                       (gameglobal.localBaseApp, uid, callback, params))
    else:
        forwardGMCommand(su, '$_callserversbase', component, realFunc, params,
                       (gameglobal.localBaseApp, uid, callback, params))
        forwardGMCommand(su, '$_callserverscell', component, realFunc, params,
                       (gameglobal.localBaseApp, uid, callback, params))


def updateUserPrivileges(info):
    gameglobal.GM_USER_PRIVILEGES[info['urs']] = info


def updateGroupPrivileges(group, cmds):
    gameglobal.GM_CMD_GROUPS = {k: v for k, v in gameglobal.GM_CMD_GROUPS.items() if v != group}
    for cmd in cmds:
        gameglobal.GM_CMD_GROUPS[cmd] = group


def delUserPrivileges(urs):
    if urs in gameglobal.GM_USER_PRIVILEGES:
        del gameglobal.GM_USER_PRIVILEGES[urs]


def canSkipCallLimitCheck(group):
    return group in GOD_GROUPS


def removeOldGmCommand(cmds):
    if cmds not in GM_CMDS:
        return
    GM_CMD_FUNC_NAMES.discard(GM_CMDS[cmds].func.__name__)
    GM_CMDS.pop(cmds, None)
