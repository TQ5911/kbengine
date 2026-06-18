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

GM指令可以直接用return 'command success',True 这样的形式来显示反馈，与su.feedbackCommandSucc('command success')或者
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
import gameconst
import utils
import gameengine
import gameconfig
import gameglobal
import time
import userType
import gamesql
import random

import gmAdmin

import gmGroup
import LogTrackingMgr

from KBEDebug import *
import proto.centralLogin_pb2 as centralLogin

# --- 开发者组
# 开发者权限
GOD_GROUPS, DEVE_GROUPS, NON_GROUPS = (gmGroup.MANAGER_GROUP_GOD,),\
    (gmGroup.MANAGER_GROUP_DEV, gmGroup.MANAGER_GROUP_GOD,), ()

if KBEngine.component == 'cellapp':
    COMPONENT = gameconst.CELL
elif KBEngine.component == 'baseapp':
    COMPONENT = gameconst.BASE

COMMAND_SPLIT_SEP = ' '

RSU, RONE, RALL, SELF = 'RSU', 'RONE', 'RALL', 'SELF'


class _DUMMY_SU(userType.UserSingleType):
    def __init__(self):
        self.spaceNo = 0
        self.id = 0
        self.who = ''
        self.accountRole = ''
        self.accountName = ''
        self.roleAccount = ''
        self.group = frozenset(GOD_GROUPS)
        self.roleName = ''

    def feedbackCommandSucc(self, msg):
        LOG_INFO('_DUMMY_SU.feedbackCommandSucc', msg)

    def feedbackCommandFail(self, msg):
        LOG_INFO('_DUMMY_SU.feedbackCommandFail', msg)


DUMMY_SU = _DUMMY_SU()


class GMAgentBase(userType.UserSingleType):
    def __getattr__(self, name):
        if name == 'cell':
            return self

        if name == 'base':
            return self

        if name == 'client':
            return self

        if name in ('id', 'spaceID',):
            return 0

        if name in ('gbID', 'gbId'):
            return 0

        if name in ('playerName', 'roleName'):
            return self.account

        return ''

    def feedbackCommandSucc(self, message):
        LOG_INFO('feedbackCommandSucc', message)

    def feedbackCommandFail(self, message):
        LOG_INFO('feedbackCommandFail', message)

    def onCommandResult(self, result, retErrMsg, resultObj):
        if type(resultObj) is dict:
            res = resultObj
        else:
            res = resultObj.__dict__ if resultObj else 'None'
        LOG_INFO('onCommandResult', result, retErrMsg, res)


class GMAgent(GMAgentBase):
    IsAvatar = False

    def __getstate__(self):
        return {
            'account': self.account,
            'owner': self.owner,
            'group': self.group,
            'tag': self.tag,
            'cmdUUID': self.cmdUUID,
        }

    def __init__(self, owner, tag, account, group=0, cmdUUID=b'', ):
        self.account = account
        self.owner = owner
        self.group = group
        self.tag = tag
        self.cmdUUID = cmdUUID

    def __setstate__(self, state):
        self.__dict__.update(state)

    def feedbackCommandSucc(self, message):
        LOG_INFO('gm command succ:', message)
        self.owner.doReplyCommand(self.tag, self.account, self.cmdUUID, message, 1)

    def feedbackCommandFail(self, message):
        LOG_INFO('gm command fail:', message)
        self.owner.doReplyCommand(self.tag, self.account, self.cmdUUID, message, 0)


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
            'group': self.group,
            'account': self.account,
            'cmdUUID': self.cmdUUID,
            'seqIdStr': self.seqIdStr,
            'tag': self.tag,
            'cmdStr': self.cmdStr,
            'baseAppBox': self.baseAppBox,
        }

    def __setstate__(self, state):
        self.__dict__.update(state)

    def onCommandResult(self, result, retErrMsg, resultObj):
        resultObj = resultObj or {}
        self.replyHttpCmd(result, retErrMsg, resultObj)
        LOG_INFO('onCommandResult HTTPAgent', result, retErrMsg, resultObj, self.seqIdStr, self.cmdStr, resultObj)

        if self.seqIdStr and self.cmdStr in gameconfig.httpCmdIdempotent():
            gamesql.recordAdminCmdSucc(self.seqIdStr, result, retErrMsg, resultObj)

    def feedbackCommandSucc(self, message):
        result = {}
        LOG_INFO('feedbackCommandSucc HTTPAgent', self.tag, self.cmdUUID, 0, message, result)
        self.replyHttpCmd(0, message, result)

    def feedbackCommandFail(self, message):
        result = {}
        LOG_INFO('feedbackCommandFail HTTPAgent', self.tag, self.cmdUUID, -1, message, result)
        self.replyHttpCmd(-1, message, result)

    def replyHttpCmd(self, result, retErrMsg, resultBytes):
        cmd = GM_CMDS.get(self.cmdStr)
        if cmd.route == RALL:
            self.baseAppBox.replyHttpCommand(self.owner, self.tag, self.cmdUUID, result, retErrMsg, resultBytes, self.cmdStr)
        else:
            self.owner.replyHttpCommand(self.tag, self.cmdUUID, result, retErrMsg, resultBytes)


def RSTUB(stub):
    assert (type(stub) is str)
    return stub


def RARG(index):
    assert (type(index) is int and index >= 0)
    return index


def _isRSTUB(r):
    return type(r) is str and r not in (RSU, RONE, RALL, SELF)


def _isRARG(r):
    return type(r) is int


class ConvertErrorException(Exception):
    pass


class GmCmdArgBase(object):
    def __init__(self, desc):
        self.data = ""
        self.desc = desc

    def fetchDesc(self):
        return self.desc

    def convert(self, data):
        raise RuntimeError('Not implemented!')

    def fetchTypeDesc(self):
        raise RuntimeError('Not implemented!')

    def fetchFullDesc(self):
        return '%s(%s)' % (self.fetchDesc(), self.fetchTypeDesc())

    def fetchDefault(self):
        raise RuntimeError('Not implemented!')

    def fetchErrorStr(self, data):
        return '%s 不是有效的 %s' % (data, self.fetchTypeDesc())

    def toString(self):
        return str(self.data)

    def toStr(self, value):
        return str(value)


class Int(GmCmdArgBase):
    def __init__(self, desc, min=None, max=None, range=None, default=0, **kwargs):
        super(Int, self).__init__(desc)
        self.max = max
        self.min = min
        self.range = range
        self.data = str(default)
        self.default = default

    def convert(self, data):
        try:
            _d = int(data)
        except:
            raise ConvertErrorException(self.fetchErrorStr(data))

        if self.min != None and _d < self.min:
            raise ConvertErrorException(self.fetchErrorStr(data))

        if self.max != None and _d > self.max:
            raise ConvertErrorException(self.fetchErrorStr(data))

        if self.range != None and _d not in self.range:
            raise ConvertErrorException(self.fetchErrorStr(data))
        self.data = data
        return _d

    def fetchTypeDesc(self):
        _extra = ''
        if self.min != None or self.max != None:
            _extra = '['
            if self.min != None:
                _extra += str(self.min)
            _extra += '-'
            if self.max != None:
                _extra += str(self.max)
            _extra += ']'
        elif self.range != None:
            _extra = repr(list(self.range)).replace(' ', '')
        return 'Int' + _extra

    def fetchDefault(self):
        return self.default


class Str(GmCmdArgBase):
    def __init__(self, desc, default='', **kwargs):
        super(Str, self).__init__(desc)
        self.data = str(default)
        self.default = default

    def convert(self, data):
        if type(data) != str:
            raise ConvertErrorException(self.fetchErrorStr(data))
        self.data = data
        return data

    def fetchTypeDesc(self):
        return 'Str'

    def fetchDefault(self):
        return self.default


class TimeStr(GmCmdArgBase):
    def __init__(self, desc, *args, **kwargs):
        super(TimeStr, self).__init__(desc)

    def convert(self, inputData):
        if type(inputData) != str:
            raise ConvertErrorException(self.fetchErrorStr(inputData))
        try:
            self.data = int(time.mktime(time.strptime(inputData, '%Y.%m.%d.%H.%M.%S')))
        except:
            raise ConvertErrorException("%s is not a valid time str. eg.[2015.9.9.20.0.0]" % (inputData,))
        return self.data

    def fetchTypeDesc(self):
        return 'TimeStr'

    def fetchDefault(self):
        return utils.curTS()


class Float(GmCmdArgBase):
    def __init__(self, desc, min=None, max=None, default=0.0, **kwargs):
        super(Float, self).__init__(desc)
        self.max = max
        self.min = min

        self.data = str(default)
        self.default = default

    def convert(self, data):
        try:
            d = float(data)
        except:
            raise ConvertErrorException(self.fetchErrorStr(data))

        if self.min != None and d < self.min:
            raise ConvertErrorException(self.fetchErrorStr(data))

        if self.max != None and d > self.max:
            raise ConvertErrorException(self.fetchErrorStr(data))

        self.data = data
        return d

    def fetchTypeDesc(self):
        _extra = ''
        if self.min != None or self.max != None:
            _extra = '['
            if self.min != None:
                _extra += str(self.min)
            _extra += '-'
            if self.max != None:
                _extra += str(self.max)
            _extra += ']'
        return 'Float' + _extra

    def fetchDefault(self):
        return self.default


class Rgba(GmCmdArgBase):
    def __init__(self, desc, *args, **kwargs):
        super(Rgba, self).__init__(desc)

    def convert(self, data):
        try:
            _r, _g, _b, _a = data.split(',')
            rgba = '%d,%d,%d,%d' % (int(_r), int(_g), int(_b), int(_a))
        except:
            raise ConvertErrorException(self.fetchErrorStr(data))
        self.data = data
        return rgba

    def fetchTypeDesc(self):
        return 'R,G,B,A'

    def fetchDefault(self):
        return '255,255,255,255'


class Python(GmCmdArgBase):
    def __init__(self, desc, *args, **kwargs):
        super(Python, self).__init__(desc)

    def convert(self, inputData):
        self.data = str(inputData)
        return inputData

    def fetchTypeDesc(self):
        return 'Python'

    def fetchDefault(self):
        return ''

    def toStr(self, value):
        return 'python'


class EntityArg(GmCmdArgBase):
    def getEntity(self, arg):
        raise RuntimeError('Not implemented!')

    def getComponent(self):
        raise RuntimeError('Not implemented!')

    def checkValue(self, arg, val):
        raise RuntimeError('Not implemented!')


class NormalEntityArg(EntityArg):
    def __init__(self, desc, extra=None, **kwargs):
        super(NormalEntityArg, self).__init__(desc)

        if extra and (type(extra) is not tuple and len(extra) == 2):
            raise RuntimeError('Wrong extra data %s' % (extra,))

        self.extra = extra

    def convert(self, inputData):
        if self.extra:
            return inputData

        try:
            # 处理@开头的玩家Entity
            if inputData.startswith("@"):
                int(inputData[1:])
            else:
                int(inputData)
        except:
            raise ConvertErrorException(self.fetchErrorStr(inputData))
        self.data = inputData
        return inputData

    def fetchTypeDesc(self):
        if self.extra:
            return 'Str'
        else:
            return 'Int/@数字'

    def fetchDefault(self):
        if self.extra:
            return ''
        else:
            return 0

    def checkValue(self, arg, val):
        if type(val) in (int, str):
            if self.extra:
                return 'Entity(%s:%s=%s) not exists' % (self.extra[0], self.extra[1], arg)
            else:
                return 'Entity(%s) not exists' % (arg,)
        return ''

    def getEntity(self, arg):
        _ent = None
        if hasattr(arg, 'id'):
            _ent = KBEngine.entities.get(arg.id)
        if not _checkEntityExist(_ent):
            return None
        return _ent

    def getMailBox(self, uid, index, gbId):
        gbId = int(gbId)
        gameengine.getGlobalBase('PlayerStub').gmLookUpAvatar(gameglobal.localBaseApp, \
                                                               gbId, uid, index, False)


class CellEntity(NormalEntityArg):
    def __init__(self, desc, extra=None, **kwargs):
        super(CellEntity, self).__init__(desc, extra)
        return

    def getComponent(self):
        return gameconst.CELL


class BaseEntity(NormalEntityArg):
    def __init__(self, desc, extra=None, **kwargs):
        super(BaseEntity, self).__init__(desc, extra)
        return

    def getComponent(self):
        return gameconst.BASE


# 不是一个GmCmdArg，而是一个proxy
class Entity(object):
    def __init__(self, desc, extra=None, **kwargs):
        self.desc = desc
        self.extra = extra
        return

    def getArg(self, comp):
        if comp == gameconst.BASE:
            return BaseEntity(self.desc, self.extra)
        elif comp == gameconst.CELL:
            return CellEntity(self.desc, self.extra)
        raise Exception()


class MgrStub(GmCmdArgBase):
    def __init__(self, desc, **kwargs):
        super(MgrStub, self).__init__(desc)

    def convert(self, data):
        raise RuntimeError('Not implemented!')

    def getEntity(self, arg):
        raise RuntimeError('Not implemented!')

    def fetchTypeDesc(self):
        raise RuntimeError('Not implemented!')


class Player(EntityArg):
    def __init__(self, desc, raw=False, **kwargs):
        super(Player, self).__init__(desc)

        # raw为True代表当这个玩家不在线时，返回该玩家名，而不做错误处理
        # 一般用于需要离线操作的指令，配合isRawPlayer函数使用。
        self.raw = raw

    def convert(self, data):
        if self.raw and not utils.isEntityId(data):
            # 只有gbid, rolename支持离线模式
            if data != '0' and not (utils.isGbId(data) or utils.checkRoleName(data)):
                raise ConvertErrorException(self.fetchErrorStr(data))
        self.data = data
        return data

    def fetchTypeDesc(self):
        if self.raw:
            return '汉字/Long'
        else:
            return '汉字/Int/Long'

    def fetchDefault(self):
        return ''

    def getMailBox(self, uid, index, gbId):
        gbId = int(gbId)
        gameengine.getGlobalBase('PlayerStub').gmLookUpAvatar(gameglobal.localBaseApp, \
                                                               gbId, uid, index, self.raw)

    def getComponent(self):
        return gameconst.BASE

    def checkValue(self, arg, val):
        if val == False:
            return '角色(%s)不存在' % (arg,)
        if val == True:
            return '角色(%s)不在线' % (arg,)
        if not self.raw and type(val) is str:
            return '角色(e_rolename:%s)不存在' % (arg,)
        if not self.raw and utils.isGbId(val):
            return '角色(e_gbid:%d)不存在' % (arg,)
        if self.raw and utils.isEntityId(val):
            return '角色(e_eid:%s)不存在' % (arg,)
        return ''

    def getEntity(self, arg):
        if isRawPlayer(arg):
            return arg

        _ent = None
        if arg.__class__.__name__ == 'EntityCall':
            _ent = KBEngine.entities.get(arg.id)
        elif isinstance(arg, (KBEngine.Entity,)):
            _ent = arg

        if not _checkEntityExist(_ent):
            return None

        return _ent


class PlayerAccount(NormalEntityArg):
    def __init__(self, desc, raw=False, **kwargs):
        super(PlayerAccount, self).__init__(desc)
        self.raw = raw

    def convert(self, inputData):
        self.data = inputData
        return inputData

    def fetchTypeDesc(self):
        return 'Str'

    def fetchDefault(self):
        return ''

    def getComponent(self):
        return gameconst.BASE

    def checkValue(self, arg, val):
        if val == False:
            return '账号(%s)不存在' % (arg,)
        if val == True:
            return '账号(%s)不在线' % (arg,)

        return ''

    def getEntity(self, arg):
        if checkRawAccount(arg):
            return arg

        _ent = None
        if arg.__class__.__name__ == 'EntityCall':
            _ent = KBEngine.entities.get(arg.id)
        elif isinstance(arg, (KBEngine.Entity,)):
            _ent = arg

        if not _checkEntityExist(_ent):
            return None

        return _ent

    def getAccount(self, uid, index, realAccountName):
        stubs = gameengine.getLoginStubsByAccountName(realAccountName)
        if stubs:
            stubs[0].gmLookUpAccount(gameglobal.localBaseApp, \
                                     realAccountName, uid, index, self.raw)


def isRawPlayer(player):
    if (type(player) is tuple or type(player) is list) and len(player) == gameconst.GM_RAW_PLAYER_FIELDS:
        return True


def checkRawAccount(account):
    if type(account) is str:
        return True


def fetchGbIdFromRawPlayer(player):
    return player[0]


GM_CMD_FUNC_NAMES = gameglobal.GM_CMD_FUNC_NAMES
GM_CMD_ARG_PERMISSION_CHECKER = gameglobal.GM_CMD_ARG_PERMISSION_CHECKER
GM_CMDS = gameglobal.GM_CMDS


class GmCommand(object):
    def __init__(self, name, funcName, args, route, kind, desc, component, side, groups, pub, minArgs, logDisable,
                 callLimitNum=0, **kwargs):
        self.name = name
        self.func = funcName
        self.args = list(args)
        self.kind = kind
        self.route = route
        self.desc = desc
        self.side = side
        self.component = component
        self.groups = frozenset(groups)
        self.pub = pub
        self.minArgs = minArgs
        self.callLimitNum = callLimitNum
        self.logDisable = logDisable

    def getRealGroup(self):
        return self.groups

    def checkPermission(self, superUser):
        # 如果服务器配置文件中设置不检查权限
        if not gameconfig.gmVerifyByGroup():
            return True

        return superUser.group in self.getRealGroup()

    def checkComponent(self):
        return self.component == COMPONENT or self.component == gameconst.ALL

    def isPub(self):
        if not self.pub:
            return False

        return True

    def isKind(self, kind):
        return self.kind == kind

    def checkSide(self, side):
        if self.side == gmAdmin.ALLSIDE:
            return True

        return self.side == side

    def fetchCommandDesc(self):
        return '%s %s' % (self.name, ' '.join([arg.fetchFullDesc() for arg in self.args]))

    def fetchHelpInfo(self):
        _args_desc = {}
        args_default = {}
        for i, arg in enumerate(self.args):
            _args_desc[i] = arg.fetchDesc()
            args_default[i] = arg.fetchDefault()

        return (self.desc, _args_desc, args_default)

    def getMatchInfo(self):
        return '指令:[%s, ] 作用:%s,  参数:[ %s ]' % (
            self.name[1:], 
            self.desc,
            ' '.join([_arg.fetchDesc() for _arg in self.args])
        )

    def strArgs(self, args):
        _new_args = []
        for i, arg in enumerate(self.args):
            if type(arg) is Python:
                _new_args.append(args[i])
            else:
                if self.minArgs >= 0 and i >= len(args):
                    _new_args.append(arg.toStr(arg.fetchDefault()))
                else:
                    _new_args.append(arg.toStr(args[i]))
        return _new_args

    # 增加了对default参数的支持
    def convertArgs(self, args, realArgs):
        error_msgs = []
        input_arg_count = len(args) 
        defined_arg_count = len(self.args)

        # 参数个数完全匹配或者大于等于最小参数个数
        if self.minArgs < 0:
            # 不限制最小参数 → 必须严格匹配定义的参数数量
            if input_arg_count != defined_arg_count:
                error_msgs.append("参数个数错误")
                return error_msgs
        else:
            # 有最小必填参数 → 不能少，也不能多
            if input_arg_count < self.minArgs or input_arg_count > defined_arg_count:
                error_msgs.append("参数个数错误")
                return error_msgs

        for _i, arg in enumerate(self.args):
            try:
                if self.minArgs >= 0 and _i >= len(args):
                    realArgs.append(arg.fetchDefault())
                else:
                    realArgs.append(arg.convert(args[_i]))
            except ConvertErrorException as inst:
                error_msgs.append(inst.args[0])

        return error_msgs

    def checkHasEntityArgs(self):
        for arg in self.args:
            if isinstance(arg, EntityArg):
                return True
        return False

    def fetchEntityArgs(self):
        _args = set()
        for _i, _arg in enumerate(self.args):
            if isinstance(_arg, EntityArg):
                _args.add(_i)
        return _args

    def fetchArgMailBoxes(self, su, command, args, raw_args=None, reason="", **kwargs):
        if raw_args is None:
            raw_args = []

        _uid = utils.generateUUID()
        need = self.fetchEntityArgs()
        _data = {
            'command': command, 
            'su': su, 
            'total': 0,
            'num': 0, 
            'args': args, 
            'need': need, 
            'reason': reason,
            'done': set(), 
        }

        if raw_args:
            _data["raw_args"] = raw_args

        gameglobal.gmCmdData[_uid] = _data

        pending_args = {}
        for i in need:
            _arg = self.args[i]
            if not isinstance(_arg, EntityArg):
                continue

            if type(_arg) is Player:
                # 0代表su自己
                if args[i] == '0':
                    _onUpdateCmdArg(_uid, i, su)
                elif utils.isEntityId(args[i]):
                    pending_args.setdefault(_arg.getComponent(), []).append(
                        (i, (int(args[i]), _arg.__class__.__name__)))
                else:
                    # 可能传入gbId(long) 或  roleName(str)
                    _arg.getMailBox(_uid, i, args[i])
            elif type(_arg) is PlayerAccount:
                _data['total'] += _getComponentCount(gameconst.BASE)
                _arg.getAccount(_uid, i, args[i])
            else:
                if _arg.extra:
                    pending_args.setdefault(_arg.getComponent(), []).append(
                        (i, _arg.extra + (args[i], _arg.__class__.__name__)))
                elif args[i].startswith('@'):
                    _arg.getMailBox(_uid, i, args[i])
                elif args[i] == '0':
                    _onUpdateCmdArg(_uid, i, su)
                else:
                    pending_args.setdefault(_arg.getComponent(), []).append(
                        (i, (int(args[i]), _arg.__class__.__name__)))

        for k in pending_args.keys():
            _data['total'] += _getComponentCount(k)
        for _k, _v in pending_args.items():
            _callApps(_k, 'gmCommand.findEntity', (gameglobal.localBaseApp, _v, _uid))

    def reportError(self, data):
        error_msgs = []
        _args = _splitCommand(data['command'])[1]
        LOG_WARN('do command error:', data)
        for _i in data['need']:
            _arg = self.args[_i]
            _msg = _arg.checkValue(_args[_i], data['args'][_i])
            if isinstance(_arg, Player):
                if data['args'][_i] == False:
                    data['su'].onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_NOT_EXISTS, _msg, None)
                    return
                elif data['args'][_i] == True:
                    data['su'].onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, _msg, None)
                    return
                else:
                    data['su'].onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_NOT_EXISTS, _msg, None)
                    return

            elif isinstance(_arg, PlayerAccount) and not data['args'][_i]:
                data['su'].onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_NOT_EXISTS, _msg, None)
                return

            if _msg:
                error_msgs.append(_msg)
        data['su'].feedbackCommandFail('错误，%s' % ('，'.join(error_msgs)))

    def checkArgValues(self, data):
        _args = _splitCommand(data['command'])[1]
        for _i in data['need']:
            if self.args[_i].checkValue(_args[_i], data['args'][_i]):
                return False
        return True

    def buildCmdString(self, args):
        _fields = []
        _fields.append(self.name)
        for _i, arg in enumerate(self.args):
            if self.minArgs >= 0 and _i >= len(args):
                _fields.append(arg.toStr(arg.fetchDefault()))
            else:
                _fields.append(arg.toStr(args[_i]))

        return ' '.join(_fields)

    def _playerLog(self, su, ent, data):
        pass

    def _gmCallback(self, data, name):
        if not data or not name:
            return

        _uid = data.get('uid')
        target = data.get('target')
        if not _uid or not target:
            return

        func = getattr(target, data.get(name), None)
        if func:
            func(_uid)

    def do(self, superUser, args, data=None):
        if not self.checkComponent():
            return
        _stub = None

        if self.route == RSU:
            superUser = KBEngine.entities.get(superUser.id)
            if not _checkEntityExist(superUser):
                self._gmCallback(data, 'failCallback')
                return

        elif self.route == RONE:
            if self.component == gameconst.CELL:
                if not gameengine.isFirstCellApp():
                    return

        elif self.route == RALL:
            pass

        elif _isRARG(self.route):
            _index = self.route
            ent = self.args[_index].getEntity(args[_index])

            if type(self.args[_index]) is Player:
                if isRawPlayer(ent):
                    if self.component == gameconst.BASE and not gameengine.isFirstBaseApp():
                        self._gmCallback(data, 'failCallback')
                        return
                    if self.component == gameconst.CELL and not gameengine.isFirstCellApp():
                        self._gmCallback(data, 'failCallback')
                        return
                elif not _checkEntityExist(ent):
                    self._gmCallback(data, 'failCallback')
                    return

            if type(self.args[_index]) is PlayerAccount:
                if checkRawAccount(ent):
                    if self.component == gameconst.BASE and not gameengine.isFirstBaseApp():
                        self._gmCallback(data, 'failCallback')
                        return
                elif not _checkEntityExist(ent):
                    self._gmCallback(data, 'failCallback')
                    return

            if isinstance(self.args[_index], (Entity, CellEntity, BaseEntity)):
                if not _checkEntityExist(ent):
                    self._gmCallback(data, 'failCallback')
                    return

            args[_index] = ent

        elif _isRSTUB(self.route):
            base = gameengine.getGlobalBase(self.route)
            _stub = KBEngine.entities.get(base.id)
            if not _stub:
                return
        try:
            _pl = None
            for arg in args:
                if isRawPlayer(arg):
                    _pl = arg
                    break
                elif arg.__class__.__name__ == "Avatar":
                    _pl = arg
                    break
            if _pl:
                self._playerLog(superUser, _pl, data)

            if _stub:
                _ret = self.func(superUser, _stub, *args)
            else:
                _ret = self.func(superUser, *args)

            if type(_ret) is bool:
                if _ret:
                    superUser.feedbackCommandSucc('执行 %s 成功' % (self.name,))
                else:
                    superUser.feedbackCommandFail('执行 %s 失败' % (self.name,))
            elif type(_ret) is str:
                raise Exception("GM指令(%r)返回参数错误, 正确格式(msg, succ)" % (self.name,))
            elif type(_ret) is tuple:
                if len(_ret) == 2:
                    succ, msg = _ret
                    if succ:
                        superUser.feedbackCommandSucc(msg)
                    else:
                        superUser.feedbackCommandFail(msg)
                else:
                    raise Exception("GM指令(%r)返回参数错误, 正确格式(msg, succ)" % (self.name,))
            self._gmCallback(data, 'succCallback')
        except Exception as exc:
            import sys
            gameengine.exceptHook(*sys.exc_info())
            LOG_ERR('do command failed:', exc)
            superUser.feedbackCommandFail('服务端指令执行 %s 失败, 执行没有生效, 请联系服务端开发.' % (self.name))


def findEntity(base, args, uid):
    _result = []
    for _i, _t in args:
        if len(_t) == 2:
            arg, argType = _t
            if type(arg) is int:
                if arg > gameconst.GBID_BASE:
                    # 是GBID
                    ent = _findEntityByGbId(arg)
                    if ent:
                        _result.append((_i, ent))
                else:
                    # 是普通的entityId
                    ent = KBEngine.entities.get(arg)
                    if _checkEntityExist(ent):
                        if argType == 'Player':
                            if ent.__class__.__name__ == 'Avatar':
                                _result.append((_i, ent))
                            else:
                                pass
                        else:
                            _result.append((_i, ent))

    base.onGmFindEntity(_result, uid)


def _findEntityByGbId(gbId):
    if KBEngine.component == 'cellapp':
        for _e in KBEngine.entities.values():
            if hasattr(_e, 'gbId') and _e.gbId == gbId and _checkEntityExist(_e):
                return _e
    elif KBEngine.component == 'baseapp':
        for _e in KBEngine.entities.values():
            if hasattr(_e, 'gbID') and _e.gbID == gbId and _checkEntityExist(_e):
                return _e
    return None


def onFindEntity(result, uid):
    _data = gameglobal.gmCmdData.get(uid)
    if not _data:
        return

    for i, val in result:
        _onUpdateCmdArg(uid, i, val)

    _data['num'] += 1
    if _data['num'] >= _data['total']:
        gameglobal.gmCmdData.pop(uid, None)
        if _data['done'] != _data['need']:
            cmd = _fetchCommand(_data['command'])
            cmd.reportError(_data)


def onLookUpAvatar(base, role, uid, index, raw):
    if base == True and raw:
        gbid, roleName, accoutName, dbid = role
        t = gbid, roleName, accoutName, dbid
        _onUpdateCmdArg(uid, index, t)
    else:
        _onUpdateCmdArg(uid, index, base)


def onFindAccount(result, realAccountName, index, raw, uid):
    _data = gameglobal.gmCmdData.get(uid)
    if not _data:
        return

    if result:
        _onUpdateCmdArg(uid, index, result)
        gameglobal.gmCmdData.pop(uid, None)
    else:
        _accountType, _accName = utils.fetchAccountTypeAndName(realAccountName)
        if _accountType == centralLogin.ACCOUNT_UNKNOW:
            _sql = "select accountName from kbe_accountinfos where accountName = {} or accountName={}".format(
                utils.escape_string(realAccountName), utils.escape_string(_accName))
        else:
            _sql = "select accountName from kbe_accountinfos where accountName = {}".format(
                utils.escape_string(realAccountName))

        KBEngine.executeRawDatabaseCommand(_sql,
                                           lambda ret, num, insertid, err: _queryAccountNameCallback(ret, num, insertid,
                                                                                                     err, raw,
                                                                                                     realAccountName,
                                                                                                     uid, index))


def _queryAccountNameCallback(ret, num, insertid, err, raw, accountName, uid, index):
    if len(ret) == 0:
        _onUpdateCmdArg(uid, index, False)
    else:
        if raw:
            _onUpdateCmdArg(uid, index, accountName)
        else:
            _onUpdateCmdArg(uid, index, True)

    gameglobal.gmCmdData.pop(uid, None)


def onBroadcastCmdSuccess(uid):
    gameglobal.gmCmdData.pop(uid, None)


def onBroadcastCmdFail(uid):
    _data = gameglobal.gmCmdData.get(uid)
    if not _data:
        return

    cmd = _fetchCommand(_data['command'])
    compCnt = _data.get('failCompCnt', 0)
    _data['failCompCnt'] = compCnt + 1
    if _data['failCompCnt'] >= _getComponentCount(cmd.component):
        _data.pop('failCompCnt', 0)
        retryCnt = _data.get('retryCnt', 0)
        if retryCnt < 3:
            _data['retryCnt'] = retryCnt + 1
            LOG_ERR('zt: retry gm command', _data['command'], retryCnt)
            gmBCastRealDoCommand(cmd.component, _data['su'], _data['command'], _data['args'], _data)
        else:
            _data['su'].feedbackCommandFail('执行失败: ' + _data['command'])
            gameglobal.gmCmdData.pop(uid, None)


def _onUpdateCmdArg(uid, index, value):
    _data = gameglobal.gmCmdData.get(uid)
    if not _data:
        return
    _data['args'][index] = value
    _data['done'].add(index)
    if _data['done'] == _data['need']:
        # Netease.gmCmdData.pop(uid, None)
        cmd = _fetchCommand(_data['command'])
        if cmd.checkArgValues(_data):
            _data.update({'uid': uid, 'target': gameglobal.localBaseApp, 'succCallback': 'onDoCmdSucc',
                         'failCallback': 'onDoCmdFail'})
            gmBCastRealDoCommand(cmd.component, _data['su'], _data['command'], _data['args'], _data)
        else:
            cmd.reportError(_data)


def _checkEntityExist(entity):
    if not entity:
        return False
    return COMPONENT != gameconst.CELL or entity.isReal()


def _callApps(component, funcName, args):
    if component == gameconst.BASE:
        gameengine.callBaseApps(funcName, args)
    elif component == gameconst.CELL:
        gameengine.callCellApps(funcName, args)
    else:
        gameengine.callBaseApps(funcName, args)
        gameengine.callCellApps(funcName, args)


def _getComponentCount(component):
    if component == gameconst.BASE:
        _app_count = gameconfig.baseAppCount()
    else:
        _app_count = gameconfig.cellAppCount()

    return _app_count


def _fetchCommand(command):
    return GM_CMDS.get(command.split(COMMAND_SPLIT_SEP)[0])


def _splitCommand(command):
    _fields = command.split(COMMAND_SPLIT_SEP)
    return _fields[0], _fields[1:]


def isForwardCommand(cmd):
    return cmd.startswith('$_')


def lowerCommand(command):
    _cmd_name, cmd_args = _splitCommand(command.strip())
    if not cmd_args:
        return _cmd_name.lower()
    return _cmd_name.lower() + ' ' + ' '.join(cmd_args)


def _isMatchCommand(command):
    _cmd_name, cmd_args = _splitCommand(command.strip())
    return not cmd_args and len(_cmd_name) > 1 and _cmd_name[-1] == '$'


# decorator for gm commands
def gm_cmd(cmds, args, route, component, desc='', side=gmAdmin.INSIDE, groups=DEVE_GROUPS, pub=False, minArgs=-1,
           logDisable=False, callLimitNum=0, **kwargs):
    if type(cmds) is str:
        cmds = (cmds,)
    assert (type(args) is tuple)
    assert (type(cmds) is tuple)
    assert (route in (RSU, RONE, RALL, SELF) or _isRARG(route) or _isRSTUB(route))
    assert (side in (gmAdmin.INSIDE, gmAdmin.OUTSIDE, gmAdmin.ALLSIDE))
    assert (component in (gameconst.CELL, gameconst.BASE, gameconst.ALL))
    assert (pub in (True, False))

    if route == RSU:
        assert (side == gmAdmin.INSIDE)
    elif _isRSTUB(route):
        assert (component == gameconst.BASE)
    elif _isRARG(route):
        assert (route < len(args))
        assert (isinstance(args[route], EntityArg)\
                or type(args[route]) is Entity\
                or isinstance(args[route], MgrStub))

    _has_python_arg = False
    args = list(args)
    for _i, _arg in enumerate(args):
        if type(_arg) is Python:
            _has_python_arg = True
        elif type(_arg) is Entity:
            args[_i] = _arg.getArg(component)
        else:
            assert (isinstance(_arg, GmCmdArgBase))

    def _gm_cmd(innerFunc):
        global GM_CMD_FUNC_NAMES
        global GM_CMDS

        _func_name = innerFunc.__name__
        if _func_name in GM_CMD_FUNC_NAMES:
            raise RuntimeError('GM command innerFunc %s duplicated!' % (_func_name,))
        GM_CMD_FUNC_NAMES.add(_func_name)

        for _cmd_name in cmds:
            _cmd_name = _cmd_name.lower()
            assert (len(_cmd_name) > 1 and _cmd_name[0] == '$')
            if _has_python_arg and not isForwardCommand(_cmd_name):
                raise RuntimeError('CM command %s error! Only internal command can use Python arg' % \
                                   (_cmd_name,))

            if _cmd_name in GM_CMDS:
                raise RuntimeError('GM command %s duplicated!' % (_cmd_name,))

            GM_CMDS[_cmd_name] = GmCommand(
                _cmd_name, innerFunc, args, route, '',
                desc, component, side, groups, pub, minArgs, logDisable,
                callLimitNum=callLimitNum)

        return innerFunc

    return _gm_cmd


############################################
# 用于runscript更新或添加gm指令
# 注意：与@gm_cmd相比，增加了第一个参数为类型，如在ITEM.py的gm指令则为gmAdmin.ITEM，直接将带有decorator的指令放在run_in_cell()和run_in_base()就可以了。
############################################
''' 例如
def example_run_in_base():
    import gmAdmin
    @update_gm_cmd(gmAdmin.ITEM, '$itemrecoverbyid', (Player('角色名', raw=True), Int('组操作号'), Int('物品id'), Int('物品数量'), Str('guid'), Int('Cash')), RARG(0), gameconst.CELL,\
        '恢复无镜像道具', gmAdmin.ALLSIDE, OM_DEV_EX_GROUPS, True)
    def itemRecoverById(su, e, op_nuid, itemId, itemNum, guid, cash):
        pass
    pass

def example_run_in_cell():
    import gmAdmin
    @update_gm_cmd(gmAdmin.ITEM, '$itemrecoverbyid', (Player('角色名', raw=True), Int('组操作号'), Int('物品id'), Int('物品数量'), Str('guid'), Int('Cash')), RARG(0), gameconst.CELL,\
        '恢复无镜像道具', gmAdmin.ALLSIDE, OM_DEV_EX_GROUPS, True)
    def itemRecoverById(su, e, op_nuid, itemId, itemNum, guid, cash):
        pass
    pass
'''


def update_gm_cmd(kind, cmds, args, route, component, desc='', side=gmAdmin.INSIDE, groups=DEVE_GROUPS, pub=False,
                  minArgs=-1, logDisable=False):
    if isinstance(cmds, str):
        cmds = (cmds,)
    assert (type(args) is tuple)
    assert (type(cmds) is tuple)
    assert (type(kind) is str)
    assert (component in (gameconst.CELL, gameconst.BASE))
    assert (route in (RSU, RONE, RALL, SELF) or _isRARG(route) or _isRSTUB(route))
    assert (pub in (True, False))
    assert (side in (gmAdmin.INSIDE, gmAdmin.OUTSIDE, gmAdmin.ALLSIDE))

    if route == RSU:
        assert (side == gmAdmin.INSIDE)
    elif _isRSTUB(route):
        assert (component == gameconst.BASE)
    elif _isRARG(route):
        assert (route < len(args))
        assert (isinstance(args[route], EntityArg)\
                or type(args[route]) is Entity)

    _has_python_arg = False
    args = list(args)
    for i, _arg in enumerate(args):
        if type(_arg) is Python:
            _has_python_arg = True
        elif type(_arg) is Entity:
            args[i] = _arg.getArg(component)
        else:
            assert (isinstance(_arg, GmCmdArgBase))

    def _gm_cmd(innerFunc):
        global GM_CMDS
        global GM_CMD_FUNC_NAMES

        _func_name = innerFunc.__name__
        if _func_name not in GM_CMD_FUNC_NAMES:
            GM_CMD_FUNC_NAMES.add(_func_name)

        for _cmd_name in cmds:
            _cmd_name = _cmd_name.lower()
            assert (len(_cmd_name) > 1 and _cmd_name[0] == '$')
            if _has_python_arg and not isForwardCommand(_cmd_name):
                raise RuntimeError('CM command %s error! Only internal command can use Python _arg' % \
                                   (_cmd_name,))

            GM_CMDS[_cmd_name] = GmCommand(_cmd_name, innerFunc, args, route, '', \
                                          desc, component, side, groups, pub, minArgs, logDisable)

        return innerFunc

    return _gm_cmd


# 用于cell/impAdmin.py
def init():
    pass


def doCommandInside(su, command):
    LOG_INFO("doCommandInside: %s" % command)

    if len(command) <= 1:
        return

    command = lowerCommand(command)
    cmd_name, cmd_args = _splitCommand(command)

    if isForwardCommand(command):
        return

    _doCommand(su, command, gmAdmin.INSIDE)


def doCommandOutside(su, command, reason):
    LOG_INFO("doCommandOutside: %s" % command)

    if len(command) <= 1:
        return

    command = lowerCommand(command)

    if isForwardCommand(command):
        return

    _doCommand(su, command, gmAdmin.OUTSIDE, reason=reason)


def _doCommand(superUser, command, side, args=None, reason=""):
    _cmd_name, _cmd_args = _splitCommand(command)
    cmd = GM_CMDS.get(_cmd_name)
    if not cmd:
        return

    if args is None:
        is_forward_cmd = False
    else:
        is_forward_cmd = True

    if is_forward_cmd:
        _cmd_args = args
    else:
        if not cmd.checkPermission(superUser):
            superUser.feedbackCommandFail('权限不足')
            return

        if not cmd.checkSide(side):
            superUser.feedbackCommandFail('使用环境错误')
            return

    real_args = []
    error_msgs = cmd.convertArgs(_cmd_args, real_args)
    if error_msgs:
        superUser.feedbackCommandFail('错误，%s。指令格式：%s 理由: %s' % ('、'.join(error_msgs), cmd.fetchCommandDesc(), reason))
        return

    # 这里检查参数与指令的合法性
    if not is_forward_cmd:
        try:
            if cmd.func.__name__ in GM_CMD_ARG_PERMISSION_CHECKER:
                if not GM_CMD_ARG_PERMISSION_CHECKER[cmd.func.__name__](superUser, cmd, real_args):
                    return
        except:
            import sys
            gameengine.exceptHook(*sys.exc_info())

    if not cmd.checkHasEntityArgs():
        gmBCastRealDoCommand(cmd.component, superUser, command, real_args)
    else:
        cmd.fetchArgMailBoxes(superUser, command, real_args, _cmd_args, reason)
    
    
    srcStr = superUser.__getstate__() if hasattr(superUser, '__getstate__') else str(superUser)
    LogTrackingMgr.LogTrackingMgr.GM_GM(
        'GM',
        '',
        srcStr,
        _cmd_name,
        ' '.join(_cmd_args)
    )


# 直接在系统内部发起的GM调用，不做相关权限检查
def doCommandSystem(su, command):
    LOG_INFO("gmCommand system: %s" % command)

    _cmd_name, _cmd_args = _splitCommand(command)
    cmd = GM_CMDS.get(_cmd_name)
    if not cmd:
        return

    real_args = []
    error_msgs = cmd.convertArgs(_cmd_args, real_args)
    if error_msgs:
        su.feedbackCommandFail('错误，%s。指令格式：%s' % ('、'.join(error_msgs), cmd.fetchCommandDesc(),))
        return

    if not cmd.checkHasEntityArgs():
        gmBCastRealDoCommand(cmd.component, su, command, real_args)
    else:
        cmd.fetchArgMailBoxes(su, command, real_args, _cmd_args, '系统内部执行')


def getBaseMailBox(comp):
    if utils.checkBaseMailBox(comp):
        return comp

    if utils.checkCellMailBox(comp):
        return comp.base

    if KBEngine.component == 'cellapp':
        return comp.base

    if KBEngine.component == 'baseapp':
        return comp


def getCellMailBox(comp):
    if utils.checkCellMailBox(comp):
        return comp

    if utils.checkBaseMailBox(comp):
        return comp.cell

    if KBEngine.component == 'baseapp':
        return comp.cell

    if KBEngine.component == 'cellapp':
        return comp


def gmBCastRealDoCommand(component, superUser, command, real_args, data=None):
    _cmd_name = _splitCommand(command)[0]
    _cmd = GM_CMDS.get(_cmd_name)

    if _cmd.route == RONE:
        if _cmd.component == gameconst.BASE:
            _baseappBox = random.choice(gameengine.getAllBaseApps())
            _baseappBox.doRONECommand((superUser, command, real_args, data))
        else:
            _callApps(component, 'gmCommand.realDoCommand', (superUser, command, real_args, data))
    elif _cmd.route == SELF:
        if _cmd.component == gameconst.BASE:
            gameglobal.localBaseApp.doRONECommand((superUser, command, real_args, data))
        else:
            LOG_ERR("gmCommand route error", _cmd.route, _cmd.component)
    elif _cmd.route == RSU or (_isRARG(_cmd.route) and superUser == real_args[_cmd.route]):
        cond = (KBEngine.component, _cmd.component)
        if _cmd.checkComponent():
            realDoCommand(superUser, command, real_args, data)
        elif cond == ('baseapp', gameconst.CELL):
            getCellMailBox(superUser).realDoGmCommandProxy((superUser, command, real_args, data))
        elif cond == ('cellapp', gameconst.BASE):
            getBaseMailBox(superUser).realDoGmCommandProxy((superUser, command, real_args, data))
        else:
            gameengine.panicStack("wrong cond %s %s" % (cond, command))
    else:
        _callApps(component, 'gmCommand.realDoCommand', (superUser, command, real_args, data))


def realDoCommand(su, command, args, data=None):
    _cmd_name = _splitCommand(command)[0]
    GM_CMDS.get(_cmd_name).do(su, args, data)


def forwardGMCommand(su, cmdName, *args):
    cmdName = cmdName.lower()
    _cmd = GM_CMDS.get(cmdName)
    _callApps(gameconst.BASE, 'gmCommand.realForwardCommand', (su, _cmd.buildCmdString(args), _cmd.strArgs(args)))


def realForwardCommand(superUser, command, args):
    if gameengine.isFirstBaseApp():
        _doCommand(superUser, command, gmAdmin.ALLSIDE, args)


# 转发到各baseapp/cellapp的gm调用
# @param su
# @param params:原始参数
# @param component: gameconst.BASE/gameconst.CELL/-1 BASE表示发送到所有的baseapp CELL表示发送到所有的cellapp -1表示发送到所有的baseapp和cellapp 如果为str表示某个baseapp/cellapp servername(ip:port)
# @param realFunc:实际执行的gm函数名，返回值类型必须为tuple(Bool,resultObj)
# @param callback:收集完所有结果后的回调函数  如果为None则简单反馈执行成功  如果为True 返回JOSN格式化的结果数组  如果出错返回JSON格式化的错误信息数组

