# coding:utf-8
from KBEDebug import *
import KBEngine
import gamesql
import gameglobal
import redisUtils
import elasticUtils
import gameconst
import gameengine
import gzip
import utils
import _pickle as cPickle
import base64
import functools
import SwitchGlobalVal


class SwitchContext(object):
    def __init__(self, gbId, dbId, rootTbName, serverId, accountName, accountType):
        self.rootTbName = rootTbName
        self.serverId = serverId
        self.gbId = gbId
        self.dbId = dbId
        self.accountName = accountName
        self.accountType = accountType
        # dump data start
        self.iter = None
        self.curTbName = None
        # dump data end

        # save data start
        self.writeIter = None
        self.idMapper = {}
        self.curWriteTbName = None
        # save data end

        self.tbDataCache = {}
        self.mailRows = None

    def newDbId(self):
        for _newDbId in self.idMapper['tbl_Avatar'].values():
            return _newDbId

        return None

    @classmethod
    def fromDbDataCache(cls, data):
        _dic = cPickle.loads(data)
        _rootTbname = 'tbl_Avatar'

        _gbId = _dic['gbId']
        _ctx = SwitchContext(_gbId, 0, _rootTbname, 0, _dic['account'], _dic['accountType'])
        _ctx.tbDataCache = _dic['cache']
        _ctx.mailRows = _dic['mailRows']
        return _ctx

    def setMailRows(self, rows):
        self.mailRows = rows

    def setTbDataCache(self, tbName, ids, rows):
        self.tbDataCache[tbName] = {
            'ids': ids,
            'rows': rows,
        }

    def toDumpData(self):
        _dic = {
            'cache': self.tbDataCache,
            'account': self.accountName,
            'accountType': self.accountType,
            'gbId': self.gbId,
            'mailRows': self.mailRows,
        }

        return cPickle.dumps(_dic)


class TbNode(object):
    def __init__(self, tbName, fatherName=''):
        self.tbName = tbName
        self.fatherName = fatherName
        self.children = []

    def setFatherName(self, fatherName):
        self.fatherName = fatherName

    def addSonNode(self, sonNode):
        self.children.append(sonNode)


class SwitchServerUtils(object):
    @classmethod
    def doSwitchServer(cls, ctx):
        _root = gameglobal.switchGlobalVal.getNode(ctx.rootTbName)
        _iter = cls.enumIter(_root)
        ctx.iter = _iter

        cls.loadColumns(ctx)

    @classmethod
    def enumIter(cls, curNode):
        yield curNode.tbName
        for _node in curNode.children:
            yield from cls.enumIter(_node)

    # ----------------------------------- load data start -------------------------
    @classmethod
    def modifyGbId(cls, ctx, times):
        if times == 0:
            LOG_ERR('modifyGbId times=0', ctx.gbId)
            return

        _newGbId = utils.generateUniqGlobalId()
        gamesql.afterSwitchServerModifyGbId(
            ctx.gbId,
            _newGbId,
            lambda ret, num, insertId, err: cls.afterModifyGbId(ret, num, insertId, err, ctx, times)
        )

    @classmethod
    def afterModifyGbId(cls, ret, num, insertId, err, ctx, times):
        if err:
            LOG_ERR("afterModifyGbId error={}".format(err))
            cls.modifyGbId(ctx, times - 1)
            return

        # dump data finish

        _data = ctx.toDumpData()
        LOG_ERR('dump data len={}'.format(len(_data)))
        _data = gzip.compress(_data)
        LOG_ERR('dump data compress len={}'.format(len(_data)))
        base64Data = base64.b64encode(_data).decode('utf-8')
        redisUtils.RedisUtils.saveTestStr(base64Data)
        redisUtils.FriendUtils.deleteAllFriendRedis(ctx.gbId)

        import iRouter
        _stub = iRouter.RemoteServerStubEntityCall(ctx.serverId, 'CrossServerStub')
        _stub.onGetSwitchServerData(_data)

        # 删除好友相关
        cls.removeAllFriends(ctx)
        # 删除 es 防止搜索到
        row = ctx.tbDataCache['tbl_Avatar']['rows'][0]

        _columnVal = gameglobal.switchGlobalVal.getColumnVal('tbl_Avatar')
        _obId = cls.getCellVal(row, 'sm_obId', _columnVal.columnToIdxDic)
        _obId = int(_obId)
        elasticUtils.ElasticUtils.deleteById(_obId)

    @classmethod
    def removeAllFriends(cls, ctx):
        gamesql.loadFriends(ctx.gbId, functools.partial(cls.onGetFriends, ctx))

    @classmethod
    def onGetFriends(cls, ctx, ret, num, insertId, err):
        if err:
            LOG_ERR("onGetFriends error={}".format(err))
            return

        _friends = []
        for _gbId, in ret:
            _friends.append(int(_gbId))

        if not _friends:
            return

        gamesql.removeAllFriends(ctx.gbId, functools.partial(cls.onDeleteFriends, ctx, _friends))

    @classmethod
    def onDeleteFriends(cls, ctx, friends, ret, num, insertId, err):
        if err:
            LOG_ERR("onDeleteFriends error={}".format(err))
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            friends,
            'onFriendRemoveYou',
            (ctx.gbId,),
            None,
            '',
            ())


    @classmethod
    def loadMails(cls, ctx):
        _columnVal = gameglobal.switchGlobalVal.getColumnVal(gameconst.TABLE_NAME_GAME_MAIL)
        _condition = f'toGBID="{ctx.gbId}"'
        _columnVal.loadData(
            _condition,
            functools.partial(cls.onGetMails, ctx)
        )

    @classmethod
    def onGetMails(cls, ctx, rows):
        ctx.setMailRows(rows)
        cls.modifyGbId(ctx, 3)

    @classmethod
    def loadColumns(cls, ctx):
        _tbName = next(ctx.iter, None)
        if _tbName is None:
            cls.loadMails(ctx)
            return

        ctx.curTbName = _tbName
        cls.loadData(ctx)

    @classmethod
    def loadData(cls, ctx):
        _curNode = gameglobal.switchGlobalVal.getNode(ctx.curTbName)
        _columnVal = gameglobal.switchGlobalVal.getColumnVal(ctx.curTbName)

        if not _curNode.fatherName:
            _condition = f'id={ctx.dbId}'

        else:
            _fatherCache = ctx.tbDataCache[_curNode.fatherName]
            _ids = _fatherCache['ids']
            if not _ids:
                cls.onGetTableData(ctx, [])
                return

            _idsStr = ','.join(map(str, _ids))
            _condition = f'parentID IN ({_idsStr})'

        _columnVal.loadData(
            _condition,
            functools.partial(cls.onGetTableData, ctx)
        )

    @staticmethod
    def getCellVal(row, column, columnToIdxDic):
        return row[columnToIdxDic[column]]

    @classmethod
    def onGetTableData(cls, ctx, rows):
        _columnVal = gameglobal.switchGlobalVal.getColumnVal(ctx.curTbName)

        _ids = []
        for _row in rows:
            _id = cls.getCellVal(_row, 'id', _columnVal.columnToIdxDic)
            _id = int(_id)

            _ids.append(_id)

        ctx.setTbDataCache(ctx.curTbName, _ids, rows)
        cls.loadColumns(ctx)
    # ----------------------------------- load data end -------------------------

    @classmethod
    def onGetAvatarOnlineInfo(cls, ret, num, insertId, err, ctx):
        LOG_INFO("onGetAvatarOnlineInfo ret=%s, num=%s, insertId=%s, err=%s" % (ret, num, insertId, err))
        if err:
            LOG_ERR("onGetAvatarOnlineInfo error={}".format(err))
            return

        if len(ret) > 0:
            KBEngine.addTimer(1, 0, lambda tid: cls.switchServer(ctx.gbId, ctx.dbId, ctx.serverId, ctx.accountName, ctx.accountType))
            return

        # cls.doSwitchServer(ctx)
        cls.checkGlobalDataOk(ctx)

    @classmethod
    def checkGlobalDataOk(cls, ctx):
        if not SwitchGlobalVal.SwitchGlobalVal.checkRootOk(ctx.rootTbName):
            SwitchGlobalVal.SwitchGlobalVal.loadLevelData(
                ctx.rootTbName,
                functools.partial(cls.doSwitchServer, ctx))
            return

        cls.doSwitchServer(ctx)

    @classmethod
    def switchServer(cls, gbId, dbId, serverId, accountName, accountType):
        LOG_INFO('switchServer gbId={}, dbId={}'.format(gbId, dbId))
        _ctx = SwitchContext(gbId, dbId, 'tbl_Avatar', serverId, accountName, accountType)
        _entityType = KBEngine.getUTType('Avatar')
        gamesql.queryAvatarOnline(
            _entityType,
            dbId,
            lambda ret, num, insertId, err: cls.onGetAvatarOnlineInfo(ret, num, insertId, err, _ctx))

    # ---------------------------------- save data start -------------------------
    @classmethod
    def saveData(cls, dataBytes):
        LOG_DBG('saveData len={}'.format(len(dataBytes)))
        _data = gzip.decompress(dataBytes)
        _ctx = SwitchContext.fromDbDataCache(_data)

        if not SwitchGlobalVal.SwitchGlobalVal.checkRootOk(_ctx.rootTbName):
            SwitchGlobalVal.SwitchGlobalVal.loadLevelData(
                _ctx.rootTbName,
                functools.partial(cls.doSaveData, _ctx))
            return

        cls.doSaveData(_ctx)

    @classmethod
    def doSaveData(cls, ctx):
        _rootNode = gameglobal.switchGlobalVal.getNode(ctx.rootTbName)
        ctx.writeIter = cls.enumIter(_rootNode)
        cls.saveTableData(ctx)

    @classmethod
    def escape_string(cls, val):
        if val is None:
            return 'NULL'

        elif type(val) in (bytes, bytearray):
            if len(val) == 0:
                return "x''"
            return '0x%s' % val.hex()

        elif type(val) is not str:
            return str(val)

        return utils.escape_string(val)

    @classmethod
    def afterSaveSwitchServerRecord(cls, accountName, *args):
        LOG_INFO('afterSaveSwitchServerRecord args={}'.format(args))

        gameglobal.localLoginStub.unlockLoginSwitchServer(accountName)

    @classmethod
    def saveMailData(cls, ctx):
        _rows = ctx.mailRows
        if not _rows:
            cls.onSaveMailsData(0, 0, 0, None, ctx)
            return

        _columnVal = gameglobal.switchGlobalVal.getColumnVal(gameconst.TABLE_NAME_GAME_MAIL)
        _columnStr = _columnVal.toColumnStrWithoutId()

        _writeRows = []
        for _row in _rows:
            _vals = []
            for _idx, _columOne in enumerate(_columnVal.columns):
                _field = _columOne.name
                if _field == 'id':
                    continue

                _val = _row[_idx]
                _vals.append(cls.escape_string(_val))

            _vals = ','.join(_vals)
            _writeRows.append('({})'.format(_vals))

        _writeRows = ','.join(_writeRows)
        gamesql.saveTableData(
            gameconst.TABLE_NAME_GAME_MAIL,
            _columnStr,
            _writeRows,
            lambda ret, num, insertId, err: cls.onSaveMailsData(ret, num, insertId, err, ctx)
        )

    @classmethod
    def onSaveMailsData(cls, ret, num, insertId, err, ctx):
        LOG_INFO("onSaveMailsData ret=%s, num=%s, insertId=%s, err=%s" % (ret, num, insertId, err))
        if err:
            LOG_ERR("onSaveMailsData error={}".format(err))
            return

        _accountName = utils.mixRealAccountName(ctx.accountType, ctx.accountName)
        gamesql.addSwitchServerRecord(
            _accountName,
            ctx.newDbId(),
            lambda *args: cls.afterSaveSwitchServerRecord(ctx.accountName, *args)
        )

    @classmethod
    def saveTableData(cls, ctx):
        _tbName = next(ctx.writeIter, None)
        LOG_DBG('saveTableData', _tbName)
        if _tbName is None:
            LOG_WARN('saveTableData finish')
            # save common data finish
            # will save mail
            cls.saveMailData(ctx)
            return

        _curNode = gameglobal.switchGlobalVal.getNode(_tbName)
        if not _curNode.fatherName:
            _fatherIdMapper = None
        else:
            _fatherIdMapper = ctx.idMapper[_curNode.fatherName]

        ctx.curWriteTbName = _tbName

        _tbCache = ctx.tbDataCache[_tbName]
        _rows = _tbCache['rows']

        if not _rows:
            cls.onSaveTableData(0, 0, None, None, ctx)
            return

        _columnVal = gameglobal.switchGlobalVal.getColumnVal(_tbName)
        _columnStr = _columnVal.toColumnStrWithoutId()

        _writeRows = []
        for _row in _rows:
            _vals = []
            for _idx, _columOne in enumerate(_columnVal.columns):
                _field = _columOne.name
                if _field == 'id':
                    continue

                _val = _row[_idx]
                if _fatherIdMapper is not None and _field == 'parentID':
                    _val = _fatherIdMapper[_val]

                _vals.append(cls.escape_string(_val))

            _vals = ','.join(_vals)
            _writeRows.append('({})'.format(_vals))

        _writeRows = ','.join(_writeRows)
        gamesql.saveTableData(
            _tbName,
            _columnStr,
            _writeRows,
            lambda ret, num, insertId, err: cls.onSaveTableData(ret, num, insertId, err, ctx)
        )

    @classmethod
    def onSaveTableData(cls, ret, num, insertId, err, ctx):
        LOG_INFO("onSaveTableData ret=%s, num=%s, insertId=%s, err=%s" % (ret, num, insertId, err))
        if err:
            LOG_ERR("onSaveTableData error={} {}".format(err, ctx.curWriteTbName))
            return

        _tbCache = ctx.tbDataCache[ctx.curWriteTbName]
        _idMapper = {}

        _columnVal = gameglobal.switchGlobalVal.getColumnVal(ctx.curWriteTbName)

        for _idx, _row in enumerate(_tbCache['rows']):
            _id = cls.getCellVal(_row, 'id', _columnVal.columnToIdxDic)
            _id = int(_id)

            _newId = insertId + _idx
            _idMapper[_id] = _newId

        ctx.idMapper[ctx.curWriteTbName] = _idMapper
        cls.saveTableData(ctx)

    @classmethod
    def testSaveData(cls):
        redisUtils.RedisUtils.getTestStr(cls.onGetTestSaveData)

    @classmethod
    def onGetTestSaveData(cls, cid, err, ret):
        LOG_INFO('onGetTestSaveData cid={}, err={}, ret={}'.format(cid, err, ret))
        if err:
            LOG_ERR('onGetTestSaveData error={}'.format(err))
            return

        baseData = base64.b64decode(ret)
        cls.saveData(baseData)
        # data = gzip.decompress(baseData)
        # _ctx = SwitchContext.fromDbDataCache(data)

    # ---------------------------------- save data end -------------------------



