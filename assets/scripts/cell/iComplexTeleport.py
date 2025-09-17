# coding: utf-8
from KBEDebug import *
import KBEngine

import collections
import math

import gamedecorator
import gameengine
import gameglobal
import gameconst
import gameclass
import formula
import gametimer
import sMath
import utils
import dataUtils
import dungeonSrc
import outsideRecord
import complexTeleportOption
import gameconfig

import gamePlay_gamePlay as GP_GP
import conflict_conflict_def as CCD
import gamePlay_singleSceneData as GPSSDD
import gamePlay_enterScene as GP_ESD
import const_const as CONST

class IComplexTeleport(object):
    """处理所有诸如从 场景A --传送--> 场景B 的问题,

    所有场景都包含4个方法:
        进入前置(_beforeEnter_XXX)
        进入后置(_afterEnter_XXX)
        离开前置(_beforeLeave_XXX)
        离开后置(_afterLeave_XXX)

    e.g. 场景A传送至场景B, 默认调用关系:

    _beforeLeave_A -> _beforeEnter_B -(T.)-> _afterLeave_A -> _afterEnter_B

    调用关系可以通过传入配置交替

    所有前置/后置方法必须满足入参出参定义:

        def _fn_X(self, FROM_SPACE_NO, TO_SPACE_NO, OPTIONS, USER_CONTEXT):
            return TRUE/FALSE

    """

    @gamedecorator.limitcall(1)
    def enterWorldLine(self, exposed, lineType, lineNo, desTelId):
        """进入大世界分线"""
        INFO_MSG('enterWorldLine::~', lineType, lineNo, desTelId)
        src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        self._enterWorldLine(lineType, lineNo, desTelId, src)

    def _enterWorldLine(self, lineType, lineNo, desTelId, src, position=None, direction=None):
        """进入大世界分线"""
        if not self.canDoCompleteTeleport(canLeaveFromLine=True, noErrorMsg=True):
            WARNING_MSG('_enterWorldLine:: can\'t enter space from current spaceNo', self.spaceNo)
            return
        if lineNo >= utils.getLineMaxNumber(gameconst.MapIdDef.mapWorldLine):
            WARNING_MSG("_enterWorldLine:: can\'t enter lineNo", lineNo)
            return
        if formula.spaceInWorldLine(self.spaceNo):
            # NOTE(): 客户端不允许在大世界接口使用·enterWorldLine·重新进入大世界
            WARNING_MSG("_enterWorldLine:: can\'t enter line if already in worldline", lineNo, self.spaceNo)
            return

        self.doEnterWorldLine(lineType, lineNo, src, desTelId, position, direction)

    def doEnterWorldLine(self, lineType, lineNo, src, desTelId, position=None, direction=None):
        INFO_MSG("doEnterWorldLine::", lineType, lineNo, src, desTelId, position, direction)
        lContext = {'extra': {}}
        eContext = {'lineNo': lineNo, 'lineType': lineType}
        context = {'l': lContext, 'e': eContext, 'src': src}
        options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.ENTER)

        spaceNo = formula.getLineSpaceNo(lineType, lineNo)
        if desTelId:
            telEnt = utils.getTeleporterByID(desTelId, spaceNo)
            if telEnt:
                entityData = utils.getDunModuleData(lineType)
                telInfo = entityData.get(str(utils.getGidFromGameEntityId(telEnt.gameEntityId)), None)
                if telInfo:
                    dstPos = (telInfo['PosX'], telInfo['PosY'], telInfo['PosZ'])
                    eContext.setdefault('overwrite', {}).update({'position': dstPos})

        if position:
            eContext.setdefault('overwrite', {}).update({'position': position})
        if direction:
            eContext.setdefault('overwrite', {}).update({'direction': direction})

        canLeave = self.packageComplexTeleportLeaveData(lContext, canLeaveFromLine=True)
        if not canLeave:
            if canLeave.extra not in gameconst.CompleteTeleportLeaveFailedReason.COLL_USEROPRERRNO:
                gameengine.reportCritical('enterWorldLine::fatal error when try to enter world line', self.spaceNo, context)
            else:
                WARNING_MSG("enterWorldLine::failed, errno={}".format(canLeave.extra), self.spaceNo, context)
            return

        self.teleportFromSpaceToSpace(self.spaceNo, spaceNo, options=options, context=context)

    def switchSelfLine(self, lineNo, src):
        INFO_MSG("switchSelfLine::", lineNo, src)
        assert lineNo >= 0
        lContext = {'extra': {}}
        eContext = {'lineNo': lineNo}
        context = {'l': lContext, 'e': eContext, 'src': src}
        options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.ENTER)

        canLeave = self.packageComplexTeleportLeaveData(lContext, canLeaveFromLine=True)
        if not canLeave:
            if canLeave.extra not in gameconst.CompleteTeleportLeaveFailedReason.COLL_USEROPRERRNO:
                gameengine.reportCritical('switchSelfLine::fatal error when try to enter world line', self.spaceNo, context)
            else:
                WARNING_MSG("switchSelfLine::failed, errno={}".format(canLeave.extra), self.spaceNo, context)
            return

        fromSpaceNo = self.spaceNo
        fromSpaceLineNo = formula.getLineNo(fromSpaceNo)
        if fromSpaceLineNo == lineNo:
            gameengine.reportCritical('switchSelfLine::cant enter smae lineno', fromSpaceNo, fromSpaceLineNo, lineNo)
            return

        if not self._checkSwitchLine(lineNo):
            ERROR_MSG("switchSelfLine:: check switch line failed", fromSpaceNo, fromSpaceLineNo, lineNo)
            return

        toSpaceNo = formula.getLineSpaceNo(formula.getMapId(fromSpaceNo), lineNo)
        self.teleportFromSpaceToSpace(self.spaceNo, toSpaceNo, options=options, context=context)

    @property
    def lastTeleportSpaceNoRecord(self):
        return self.getTempMiscProp(gameconst.AvatarProps.lastTeleportSpaceNoRecord, 0)

    @lastTeleportSpaceNoRecord.setter
    def lastTeleportSpaceNoRecord(self, spaceNo):
        self.popTempMiscProp(gameconst.AvatarProps.lastTeleportSpaceNoRecord, spaceNo)

    @property
    def lastTeleportWorldlinePosRecord(self):
        return self.getPersistentMiscProp(gameconst.AvatarProps.lastTeleportWorldlinePosRecord, 0)

    @lastTeleportWorldlinePosRecord.setter
    def lastTeleportWorldlinePosRecord(self, position):
        self.setPersistentMiscProp(gameconst.AvatarProps.lastTeleportWorldlinePosRecord, position)

    @property
    def complexTeleportTypeFnMap(self):
        return gameglobal.complexTeleportTypeFnMap

    def getTeleportOutsideRecord(self):
        _m_rcdDic = self.getPersistentMiscProp(gameconst.AvatarProps.outsideRecords)
        if _m_rcdDic is None or not isinstance(_m_rcdDic, collections.OrderedDict):
            _m_rcdDic = collections.OrderedDict()
            self.setPersistentMiscProp(gameconst.AvatarProps.outsideRecords, _m_rcdDic)
        return _m_rcdDic

    def updateTeleportOutsideRecord(self, outRcd):
        _m_rcdDic = self.getTeleportOutsideRecord()
        _m_mapId = formula.getMapId(outRcd.spaceNo)
        _m_rcdDic.pop(_m_mapId, None)
        _m_rcdDic[_m_mapId] = outRcd
        return _m_rcdDic

    def popTeleportOutsideRecord(self, mapId, default=None):
        return self.getTeleportOutsideRecord().pop(mapId, default)

    def clearTeleportOutsideRecord(self):
        self.getTeleportOutsideRecord().clear()

    def tryRegiTeleportOutsideRecord(self, spaceNo, options):
        if self._shouldRecordTeleportOutsideRecord(spaceNo, options.teleportType):
            _m_outsideRecord = outsideRecord.OutsideRecord(
                self.spaceNo, self.position, self.direction, self.hp, self.mp, self.isDie())
            self.updateTeleportOutsideRecord(_m_outsideRecord)

    def tryUnRegiTeleportOutsideRecord(self, spaceNo):
        m_mapId = formula.getMapId(spaceNo)
        self.popTeleportOutsideRecord(m_mapId)

    def tryGetTeleportOutesideRecord(self, spaceNo, default=None):
        return self.getTeleportOutsideRecord().get(formula.getMapId(spaceNo), default)

    def _shouldRecordTeleportOutsideRecord(self, spaceNo, teleportType):
        if teleportType != gameconst.ComplexTeleportType.ENTER:
            return False

        m_mapId = formula.getMapId(spaceNo)
        if m_mapId in gameconst.MapIdDef.mapWorldSet:
            return True

        return False

    def tryGetLastTeleportOutesideRecord(self, fromSpaceNo, spaceType=0):
        # if gameconst.DungeonType.isBigWorldDungeon(spaceType):
        #     return gameconst.MapIdDef.mapUnknown, None

        _m_records = self.getTeleportOutsideRecord()
        for i_mapId in reversed(list(_m_records)):
            # 大世界分线
            if i_mapId in gameconst.MapIdDef.mapWorldSet:
                return i_mapId, _m_records[i_mapId]

            # 其他情况-跳出循环走默认处理
            break

        return gameconst.MapIdDef.mapUnknown, None

    def packageComplexTeleportLeaveData(self, leaveContext: dict, canLeaveFromLine=True, canLeaveFromGuild=True,
                                        canLeaveFromSingleDungeon=True, canLeaveFromTeamDungeon=True,
                                        canLeaveFromRaidDungeon=True,
                                        noErrorMsg=False, **options):
        DEBUG_MSG('packageComplexTeleportLeaveData::', self.spaceNo, leaveContext)

        leaveFnName = self._spaceToComplexTeleportDefinedName(self.spaceNo)
        if not leaveFnName:
            not noErrorMsg and ERROR_MSG('packageComplexTeleportLeaveData:: leave from current space un-supported', self.spaceNo)
            return gameclass.BoolResult(False, gameconst.CompleteTeleportLeaveFailedReason.UNDEFINED_FUNC)
        elif leaveFnName == 'worldLine':
            return gameclass.BoolResult(canLeaveFromLine, gameconst.CompleteTeleportLeaveFailedReason.ARGS_DEFINED)
        elif leaveFnName == 'singleDungeon':
            leaveContext.update({'spaceMgrBox': self.spaceMgr.base, 'spaceUUID': self.spaceMgr.dungeonPlayMode.spaceUUID})
            judgeLeaveSrc = options.get('judgeLeaveSrc')
            if not (self.canNewbieLeaveCurDungeon() or\
                    (judgeLeaveSrc and judgeLeaveSrc.srcId in gameconst.DungeonSrcEnum.COLL_FROM_TASK)):
                # self.showMsg(MMD.datas.newbie_LockDun, [])
                return gameclass.BoolResult(False, gameconst.CompleteTeleportLeaveFailedReason.PLAYER_IN_NEWBIEDUN)

            return gameclass.BoolResult(canLeaveFromSingleDungeon, gameconst.CompleteTeleportLeaveFailedReason.ARGS_DEFINED)

        elif leaveFnName == 'teamDungeon':
            leaveContext.update({'teamUUID': self.teamId, 'spaceMgrBox': self.spaceMgr.base})
            return gameclass.BoolResult(canLeaveFromTeamDungeon, gameconst.CompleteTeleportLeaveFailedReason.ARGS_DEFINED)

        elif leaveFnName == 'raidDungeon':
            leaveContext.update({'raidUUID': self.raidUUID, 'spaceMgrBox': self.spaceMgr.base, 'extra': {}})
            return gameclass.BoolResult(canLeaveFromRaidDungeon, gameconst.CompleteTeleportLeaveFailedReason.ARGS_DEFINED)

        elif leaveFnName == 'cube':
            leaveContext.update({'spaceMgrCell': self.spaceMgr})
            return gameclass.BoolResult(True, gameconst.CompleteTeleportLeaveFailedReason.ARGS_DEFINED)

        elif leaveFnName == 'wonderLand':
            leaveContext.update({'spaceMgrCell': self.spaceMgr})
            return gameclass.BoolResult(True, gameconst.CompleteTeleportLeaveFailedReason.ARGS_DEFINED)

        elif leaveFnName == 'siegeWar':
            leaveContext.update({'spaceMgrCell': self.spaceMgr})
            return gameclass.BoolResult(True, gameconst.CompleteTeleportLeaveFailedReason.ARGS_DEFINED)

        else:
            not noErrorMsg and ERROR_MSG('packageComplexTeleportLeaveData:: leave from current space unknown', self.spaceNo, leaveFnName)
            return gameclass.BoolResult(False, gameconst.CompleteTeleportLeaveFailedReason.UNDEFINED_SPACE)

    def _fetchCommonLeavePosAndDir(self, spaceSpaceNo, toSpaceNo, options, context):
        if options.teleportType == gameconst.ComplexTeleportType.LEAVE:
            _m_outRecord = self.tryGetTeleportOutesideRecord(toSpaceNo) # type: outsideRecord.OutsideRecord
            if _m_outRecord:
                m_pos, m_dir = _m_outRecord.position, _m_outRecord.direction
                m_spaceNo = toSpaceNo
                return m_pos, m_dir, m_spaceNo

        elif options.teleportType == gameconst.ComplexTeleportType.ENTER:
            if formula.spaceInWorldLine(toSpaceNo):
                _m_outRecord = self.tryGetTeleportOutesideRecord(toSpaceNo)
                if _m_outRecord:
                    m_pos, m_dir = _m_outRecord.position, _m_outRecord.direction
                    m_spaceNo = formula.getLineSpaceNo(formula.getLineType(toSpaceNo))
                    return m_pos, m_dir, m_spaceNo

        m_pos = formula.whatSpaceBornPoint(toSpaceNo)
        m_dir = (0, 0, 0)
        if formula.spaceInWorldLine(toSpaceNo):
            m_spaceNo = formula.getLineSpaceNo(formula.getLineType(toSpaceNo))
        else:
            m_spaceNo = toSpaceNo
        return m_pos, m_dir, m_spaceNo

    def doLeaveFromSapceToSpace(self, fromSpaceNo, toSpaceNo, options, context,
                                spaceType=0, noCheckGamePlayLeave=True):
        """统一离开场景方法

        Arguments:
            fromSpaceNo {SPACE_NO} -- 当前所处场景
            toSpaceNo {SPACE_NO} -- 到达场景
            options {complexTeleportOption.ComplexTeleportOptions} -- 传送选项
            context {PY_DICT} -- 传送上下文

        Keyword Arguments:
            spaceType {int} -- 指明当前spaceType, 大世界副本需要使用, 一般使用默认值即可 (default: {0})
            noCheckGamePlayLeave {bool} -- 强制玩家离开, 战场场景使用 (default: {True})
        """
        INFO_MSG("doLeaveFromSapceToSpace::", fromSpaceNo, toSpaceNo, options, context, spaceType, noCheckGamePlayLeave)
        lContext, eContext = context['l'], context['e']
        canLeave = self.packageComplexTeleportLeaveData(lContext, judgeLeaveSrc=context.get('src'))
        if not canLeave:
            ERROR_MSG("doLeaveFromSapceToSpace:: can\'t package leave context", canLeave,
                      fromSpaceNo, toSpaceNo, options, context, spaceType, noCheckGamePlayLeave,)
            return

        _m_mapId, _m_outsideRecord = self.tryGetLastTeleportOutesideRecord(fromSpaceNo, spaceType=spaceType)
        toSpaceNo = _m_outsideRecord.spaceNo if _m_outsideRecord else toSpaceNo
        DEBUG_MSG('     doLeaveFromSapceToSpace, _m_outsideRecord:', _m_mapId, _m_outsideRecord)
        self.teleportFromSpaceToSpace(self.spaceNo, toSpaceNo, options=options, context=context)

    def canDoCompleteTeleport(self, **options):
        return self.packageComplexTeleportLeaveData({}, **options)

    def tryDisableAutoCombatWhenLeaveSpace(self, dungeonNo):
        if self.autoCombat and self._getPrmBydungeonNo(dungeonNo, 'leaveSceneDisableAutoFight'):
            self.stopAutoCombat(self.id)

    def tryEnableAutoCombatAfterEnterSpace(self, dungeonNo):
        if not self.autoCombat and GP_GP.datas[dungeonNo].get('enterSceneAutoFight', 0):
            self.startAutoCombat(self.id, False)

    def tryRecoverHPAfterEnterSpace(self, gamePlayId):
        return GP_GP.datas[gamePlayId].get('recover', gameconst.GamePlayRecoverEnum.RCV_NO_ACTION) in gameconst.GamePlayRecoverEnum.COLL_ENTER_RCV

    def tryRecoverHPAfterLeaveSpace(self, gamePlayId):
        if gameconfig.isCrossServer() and gamePlayId == 0:
            return 0
        return GP_GP.datas[gamePlayId].get('recover', gameconst.GamePlayRecoverEnum.RCV_NO_ACTION) in gameconst.GamePlayRecoverEnum.COLL_LEAVE_RCV

    def __init__(self):
        pass

    @classmethod
    def regrAllComplexTeleportMethods(cls):
        gameglobal.complexTeleportTypeFnMap.clear()
        data = cls.buildCompleteTeleportMethodDefines()
        gameglobal.complexTeleportTypeFnMap.clear()
        gameglobal.complexTeleportTypeFnMap.update(data)

    @classmethod
    def buildCompleteTeleportMethodDefines(cls):
        """在此注册可传送方法, key为定义名称, val为自定义build方法,

        注: 自定方法需要遵循`_buildSTDComplexTeleportMethodDefine`方法定义
        """
        definedName = {
            'worldLine': '',        # 大世界分线
            'singleDungeon': '',    # 单人副本
            'teamDungeon': '',      # 小队副本
            'raidDungeon': '',      # 团队副本
            'cube': '',             # 魔方
            'wonderLand': '',       # 秘境峰
            'siegeWar': '',         # 城战
        }

        # ----------------------------------------------------------
        _data = {}
        for definedName, definedCustomFn in definedName.items():
            _fn = getattr(cls, definedCustomFn, None)
            _fn = cls._buildSTDComplexTeleportMethodDefine if not _fn else _fn
            _data[definedName] = _fn(definedName)
        # ----------------------------------------------------------
        return _data

    @staticmethod
    def _buildSTDComplexTeleportMethodDefine(definedName):
        _enum = gameconst.ComplexTeleportMethodTypeEnum
        return {
            _enum.beforeEnter: '_beforeEnter_{}'.format(definedName),
            _enum.afterEnter: '_afterEnter_{}'.format(definedName),
            _enum.beforeLeave: '_beforeLeave_{}'.format(definedName),
            _enum.afterLeave: '_afterLeave_{}'.format(definedName),
            _enum.postAfterEnter: '_postAfterEnter_{}'.format(definedName),
            _enum.postAfterLeave: '_postAfterLeave_{}'.format(definedName)
        }

    @staticmethod
    def _spaceToComplexTeleportDefinedName(spaceNo):
        if formula.isLineSpace(spaceNo):
            return 'worldLine'
        elif formula.isSingleDungeonSpace(spaceNo):
            return 'singleDungeon'
        elif formula.isTeamDungeonSpace(spaceNo):
            return 'teamDungeon'
        elif formula.isRaidDungeonSpace(spaceNo):
            return 'raidDungeon'
        elif formula.isCubeSpace(spaceNo):
            return 'cube'
        elif formula.isWonderLandSpace(spaceNo):
            return 'wonderLand'
        elif formula.isSiegeWarSpace(spaceNo):
            return 'siegeWar'
        else:
            return ''

    def _getComplexTeleportSpaceMethods(self, spaceNo):
        if spaceNo == 0 and gameconfig.isCrossServer():
            return None
        definedName = self._spaceToComplexTeleportDefinedName(spaceNo)
        if not definedName:
            ERROR_MSG('_getComplexTeleportSpaceMethods:: spaceNo not support', spaceNo)
            return None
        complexTeleportTypeFnMap = self.complexTeleportTypeFnMap
        return {k: getattr(self, v, None) for k, v in complexTeleportTypeFnMap[definedName].items()}


    def enterSpaceCommonNeedCast(self, callbackFn, callbackArgs, **kwargs):
        kwargs.setdefault("castTime", 3)
        return self._commonNeedCast(
            CCD.datas.teleportCast,
            gameconst.State.Teleporting,
            gameconst.CastType.teleport,
            callbackFn, callbackArgs,
            **kwargs)

    def teleportFromSpaceToSpaceRpc(self, toSpaceNo,
                                 options=complexTeleportOption.ComplexTeleportOptions(),
                                 context=None):
        self.teleportFromSpaceToSpace(self.spaceNo, toSpaceNo, options, context)

    def teleportFromSpaceToSpace(self, fromSpaceNo, toSpaceNo,
                                 options=complexTeleportOption.ComplexTeleportOptions(),
                                 context=None):
        assert context

        if not utils.checkCanChangeSceneAndShowMsg(self, fromSpaceNo, toSpaceNo):
            ERROR_MSG('teleportFromSpaceToSpace:: can\'t teleport', fromSpaceNo, toSpaceNo)
            return

        lineNo = -1
        # NOTE(): 切换至大世界分线特殊情况处理，如果不确定切换分线，则不在这里断言
        if formula.spaceInWorldLine(toSpaceNo):
            lineType = context['e'].get('lineType', -1)
            lineNo = context['e'].get('lineNo', -1)
            if lineNo >= 0 and lineType >= 0:
                toSpaceNo = formula.getLineSpaceNo(lineType, lineNo)

        if fromSpaceNo == toSpaceNo:
            gameengine.reportCritical('teleportFromSpaceToSpace:: {} == {}, can\'t teleport, lineNo={}', fromSpaceNo, toSpaceNo, lineNo)
            return
        INFO_MSG('teleportFromSpaceToSpace:: {} -> {}, options={}, context={}, lineNo={}'.format(
            fromSpaceNo, toSpaceNo, options, context, context['e'].get('lineNo', -1)))

        src = context.get('src')

        # XXX(): [进入单人相关场景]传送读条最好在真正传送前做好, 防止传送失败造成了资源浪费(e.g. 副本不应该创建)
        # 已知单人场景:
        #   1. DONE: 单人副本
        if context.get('hasCast') \
                or not utils.isComplexTeleportNeedCast(fromSpaceNo, toSpaceNo, options.teleportType, src, owner=self):
            self.teleportFromSpaceToSpaceContinue(fromSpaceNo, toSpaceNo, options, context)

        else:
            context['hasCast'] = True
            self.enterSpaceCommonNeedCast(
                "teleportFromSpaceToSpaceContinue",
                (fromSpaceNo, toSpaceNo, options, context),
                castTime=3)

    def teleportFromSpaceToSpaceContinue(self, fromSpaceNo, toSpaceNo,
                                 options=complexTeleportOption.ComplexTeleportOptions(),
                                 context=None):
        fromSpaceMethods = self._getComplexTeleportSpaceMethods(fromSpaceNo)
        toSpaceMethods = self._getComplexTeleportSpaceMethods(toSpaceNo)

        if not fromSpaceMethods or not toSpaceMethods:
            if not gameconfig.isCrossServer():
                ERROR_MSG('teleportFromSpaceToSpaceContinue:: fromSpaceMethods or toSpaceMethods is None', fromSpaceNo, toSpaceNo)
                return

        _enum = gameconst.ComplexTeleportMethodTypeEnum
        beforeEnterMethod = toSpaceMethods[_enum.beforeEnter]
        beforeLeaveMethod = fromSpaceMethods[_enum.beforeLeave] if fromSpaceMethods else None

        enterMethods = [beforeEnterMethod, beforeLeaveMethod]
        if options.beforeLeaveFirst:
            enterMethods[0], enterMethods[1] = enterMethods[1], enterMethods[0]

        _gotErr = False
        self._changeSpacSetRadius(fromSpaceNo, toSpaceNo, True)
        for fn in enterMethods:
            if not fn:
                continue
            try:
                r = fn(fromSpaceNo, toSpaceNo, options, context)
            except:
                _gotErr = True
                gameengine.reportCritical('teleportFromSpaceToSpace:: fn exception got')
            else:
                if not r:
                    # NOTE(): errorMSg由方法内部处理并报出
                    WARNING_MSG('teleportFromSpaceToSpace:: pre-enter failed',
                                fromSpaceNo, toSpaceNo, options, context)
                    return

        if _gotErr:
            return

        # overwrite toSpaceNo to context defined
        _orgToSpaceNo = toSpaceNo
        if context['spaceNo'] != toSpaceNo:
            WARNING_MSG("teleportFromSpaceToSpaceContinue:: overwrite toSapceNo {} => {}".format(
                toSpaceNo, context['spaceNo']))
            toSpaceNo = context['spaceNo']

        INFO_MSG('teleportFromSpaceToSpaceContinue:: {} -> {} ==> {}, lineNo={}, options={}, context={}'.format(
            fromSpaceNo, _orgToSpaceNo, toSpaceNo, context['e'].get('lineNo', -1), options, context))

        src = context.get('src')
        position, direction = context['position'], context['direction']

        cbFn = 'onTeleportFromSpaceToSpaceSucceed'
        cbArgs = (fromSpaceNo, toSpaceNo, options, context)
        failCB = 'onTeleportFromSpaceToLineSpaceFail'

        if formula.isLineSpace(toSpaceNo):
            lineType = formula.getMapId(toSpaceNo)
            lineNo = context['e'].get('lineNo', -1)
            # overwrite toSpaceNo
            toSpaceNo = formula.getLineSpaceNo(lineType, lineNo=lineNo)
            cbArgs = (fromSpaceNo, toSpaceNo, options, context)
            extra = {'callback': cbFn, 'callbackArgs': cbArgs, 'failCallback': failCB}
            if 'hasCast' in context:
                extra['hasCast'] = context['hasCast']

            if sMath.distance2D(self.position, position) < 1:
                direction = self.direction

            fromLineType = formula.getMapId(fromSpaceNo)
            if fromLineType != lineType:
                extra['toLine'] = True # 如果从副本进入大世界只有走这里
                self.applyEnterLineInternal(lineType, lineNo, position, direction, extra=extra)
            else:
                self.switchLineAndPosition(lineNo, position, src=src, extra=extra)

            if lineNo < 0:
                captainToSpaceNo = 0

        else:
            # NOTE(): 刺客取消濒死状态
            # self.cancelImmuneDeath()
            spaceBox = context['e']['spaceBox']
            self.teleportToCell(spaceBox.cell, toSpaceNo, position, direction, cbFn, cbArgs)

    def _changeSpacSetRadius(self, fromSpaceNo, toSpaceNo, isBefore):
        if not self.hasWitness:
            return
        srcAOI = gameconst.DEFAULT_AOI
        if fromSpaceNo != 0 or not gameconfig.isCrossServer():
            srcAOI = GP_GP.datas[formula.getMapId(fromSpaceNo)]['AOI']
        dstAOI = GP_GP.datas[formula.getMapId(toSpaceNo)]['AOI']
        if dstAOI != 0 and srcAOI == dstAOI:
            return

        srcAOI = srcAOI if srcAOI else gameconst.DEFAULT_AOI
        dstAOI = dstAOI if dstAOI else gameconst.DEFAULT_AOI
        if isBefore and dstAOI > srcAOI:
            return
        elif (not isBefore) and dstAOI < srcAOI:
            return

        curAOI = self.getViewRadius()
        if abs(curAOI - dstAOI) < 0.001:
            return

        DEBUG_MSG('will change AOI:', curAOI, dstAOI, isBefore)
        self.setViewRadius(dstAOI, gameconst.DEFAULT_HYST)

    def onTeleportFromSpaceToSpaceSucceed(self, fromSpaceNo, toSpaceNo,
                                          options: complexTeleportOption.ComplexTeleportOptions,
                                          context=None):
        assert context

        INFO_MSG('onTeleportFromSpaceToSpaceSucceed:: {} -> {} ==> {}, lineNo={}, options={}, context={}'.format(
            fromSpaceNo, toSpaceNo, self.spaceNo, context['e'].get('lineNo', -1), options, context))


        fromSpaceMethods = self._getComplexTeleportSpaceMethods(fromSpaceNo)
        toSpaceMethods = self._getComplexTeleportSpaceMethods(toSpaceNo)

        if not fromSpaceMethods or not toSpaceMethods:
            if not gameconfig.isCrossServer():
                ERROR_MSG('teleportFromSpaceToSpaceContinue:: fromSpaceMethods or toSpaceMethods is None', fromSpaceNo, toSpaceNo)
                return

        _enum = gameconst.ComplexTeleportMethodTypeEnum
        afterEnterMethod = toSpaceMethods[_enum.afterEnter]
        afterLeaveMethod = fromSpaceMethods[_enum.afterLeave] if fromSpaceMethods else None
        postAfterEnterMethod = toSpaceMethods[_enum.postAfterEnter]
        postAfterLeaveMethod = fromSpaceMethods[_enum.postAfterLeave] if fromSpaceMethods else None


        leaveMethods = [afterLeaveMethod, afterEnterMethod]
        postLeaveMethods = [postAfterEnterMethod, postAfterLeaveMethod]
        if options.afterEnterFirst:
            leaveMethods[0], leaveMethods[1] = leaveMethods[1], leaveMethods[0]
            postLeaveMethods[0], postLeaveMethods[1] = postLeaveMethods[1], postLeaveMethods[0]

        _gotErr = False
        for fn in leaveMethods:
            if not fn:
                continue
            try:
                fn(fromSpaceNo, toSpaceNo, options, context)
            except:
                _gotErr = True
                gameengine.reportCritical('onTeleportFromSpaceToSpaceSucceed:: fn exception got')

        for postFn in postLeaveMethods:
            if not postFn:
                continue

            try:
                postFn(fromSpaceNo, toSpaceNo, options, context)
            except:
                _gotErr = True
                gameengine.reportCritical('onTeleportFromSpaceToSpaceSucceed:: postFn exception got')

        self._changeSpacSetRadius(fromSpaceNo, toSpaceNo, False)
        self._changeSpacRecycleMount(context.get('isFromEdge', False))

        _toGamePlayId = formula.getDungeonNoBySpaceNo(toSpaceNo)
        _fromGamePlayId = formula.getDungeonNoBySpaceNo(fromSpaceNo)
        if self.tryRecoverHPAfterEnterSpace(_toGamePlayId) or self.tryRecoverHPAfterLeaveSpace(_fromGamePlayId):
            self.modifyHP(self.fullHp, self.id, gameconst.SourceType.Teleport, self.id)

        callback = context.get('callback', None)
        callbackArgs = context.get('callbackArgs', None)
        if callback:
            getattr(self, callback)(*callbackArgs)

        if _gotErr:
            return

    def onTeleportFromSpaceToLineSpaceFail(self, checkCode, fromSpaceNo, toSpaceNo,
                                          options: complexTeleportOption.ComplexTeleportOptions,
                                          context=None):
        WARNING_MSG("onTeleportFromSpaceToLineSpaceFail::", checkCode, fromSpaceNo, toSpaceNo, options, context)
        self.releaseTeleportLock(self.teleportLock)
    # ----------------------------------------------------------------------
    # RAID DUNGEON
    # ----------------------------------------------------------------------

    @gamedecorator.checkTeleportLock(gameconst.TeleportLock.ENTER_DUNGEON)
    def _beforeEnter_raidDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_beforeEnter_raidDungeon::~')
        dungeonNo = formula.getDungeonNoBySpaceNo(toSpaceNo)

        self.tryRegiTeleportOutsideRecord(fromSpaceNo, options)

        # get dungeon position
        position = self._getPrmBydungeonNo(dungeonNo, 'entrance')
        dungeonSpaceType = self._getPrmBydungeonNo(dungeonNo, 'type')
        dungeonEnterType = self._getPrmBydungeonNo(dungeonNo, 'enterType')
        if not position:
            if gameconst.DungeonType.isNormalRaidDungeon(dungeonSpaceType, dungeonEnterType):
                # NOTE: position in common raid dungeon must set position
                gameengine.reportCritical('_beforeEnter_raidDungeon:: common dungeon entrance position not defined', dungeonNo, toSpaceNo)
                return

            # 【【任务】副本类型扩展-帮会副本】
            elif gameconst.DungeonType.isGuildRaidDungeon(dungeonSpaceType, dungeonEnterType):
                WARNING_MSG('_beforeEnter_raidDungeon:: try resetting guild dungeon entrance position to guild entrance', dungeonNo, toSpaceNo)
                position = self._getPrmBydungeonNo(gameconst.MapIdDef.mapGuildSpace, 'entrance')
                if not position:
                    # NOTE: position in guild raid dungeon must set position in self or guild space
                    gameengine.reportCritical('_beforeEnter_raidDungeon:: guild dungeon entrance position not defined', dungeonNo, toSpaceNo)
                    return

            # 【【任务】副本类型支持小世界场景副本】
            elif gameconst.DungeonType.isHomeRaidDungeon(dungeonSpaceType, dungeonEnterType):
                WARNING_MSG('_beforeEnter_raidDungeon:: try resetting home dungeon entrance position to home entrance', dungeonNo, toSpaceNo)
                position = self._getPrmBydungeonNo(gameconst.MapIdDef.mapMyHome, 'entrance')
                if not position:
                    # NOTE: position in home raid dungeon must set position in self or home space
                    gameengine.reportCritical('_beforeEnter_raidDungeon:: home dungeon entrance position not defined', dungeonNo, toSpaceNo)
                    return

            else:
                WARNING_MSG('_beforeEnter_raidDungeon:: reset entrance position to self position', dungeonNo, toSpaceNo, self.position)
                position = self.position

        direction = self._getEntranceDirByDungeonNo(formula.getMapId(toSpaceNo))

        if direction is not None:
            direction = (0, 0, direction * math.pi / 180)

        else:
            # 【【任务】副本类型扩展-帮会副本】
            if gameconst.DungeonType.isGuildRaidDungeon(dungeonSpaceType, dungeonEnterType):
                WARNING_MSG('_beforeEnter_raidDungeon:: try resetting guild dungeon entrance direction to guild entrance', dungeonNo, toSpaceNo)
                direction = self._getEntranceDirByDungeonNo(gameconst.MapIdDef.mapGuildSpace)
                direction = (0, 0, direction * math.pi / 180) if direction is not None else self.direction

            # 【【任务】副本类型支持小世界场景副本】
            elif gameconst.DungeonType.isHomeRaidDungeon(dungeonSpaceType, dungeonEnterType):
                WARNING_MSG('_beforeEnter_raidDungeon:: try resetting home dungeon entrance direction to home entrance', dungeonNo, toSpaceNo)
                direction = self._getEntranceDirByDungeonNo(gameconst.MapIdDef.mapMyHome)
                direction = (0, 0, direction * math.pi / 180) if direction is not None else self.direction

            else:
                WARNING_MSG('_beforeEnter_raidDungeon:: reset entrance direction to self direction', dungeonNo, toSpaceNo, self.position)
                direction = self.direction

        # set teleport lock
        self.aquireTeleportLock(gameconst.TeleportLock.ENTER_DUNGEON)

        # completed context
        context['position'] = position
        context['direction'] = direction
        context['spaceNo'] = toSpaceNo
        return True

    def _afterEnter_raidDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_afterEnter_raidDungeon::~')
        dungeonNo = formula.getDungeonNoBySpaceNo(toSpaceNo)
        spaceUUID = context['e']['spaceUUID']
        spaceBox = context['e']['spaceBox']
        spaceMgrBox = context['e']['spaceMgrBox']
        extra = context['e']['extra']
        src = context['src']

        # release lock
        self.releaseTeleportLock(gameconst.TeleportLock.ENTER_DUNGEON)
        self.releaseGlobalTeleportLock('telsucc')
        # set props
        self.spaceMgrId = spaceMgrBox.id
        self.spaceMgr.onPlayerEnter(self.id)

        # if self.spaceMgr.dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.GUILD_CHALLENGE:
        #     _kwargs = dict(
        #         GameSvrId=None, dtEventTime=None, vGameAppid=None,
        #         iBattleType=gametlog.BATTLETYPE.RaidChallenge,
        #         iBattleID=dungeonNo,
        #         iTeamID=self.raidUUID,
        #         TeamUserNum=self.raidInfo.raidPlayerNum,
        #         SingleOrteam=gametlog.SingleOrteam.RAID
        #     )
        #     extra['tlogProps'] = _kwargs
        #     extra['actId'] = gameconst.ACT_ID_CONST.ACTIVITY_GUILD_CHALLENGE_ID

        # 【【死亡复活】玩家在大世界内死亡后，通过点击个人资料-头像-驭灵殿按钮进入副本后需要复活玩家】
        # NOTE(): 进入副本前复活会导致hp同步不到客户端导致显示问题, 先放在后面
        if self.isDie():
            self._relive()
            self.modifyHP(self.getDefaultReliveHp(), self.id, gameconst.SourceType.Default, self.id)

        # callback base
        extra['raidId'] = self.raidId
        if self.spaceMgr.dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.CHIEF:
            self.base.onEnterChiefDungeon(self.spaceNo, spaceMgrBox, extra)
        else:
            self.base.onEnterDungeon(self.spaceNo, spaceMgrBox, extra)
        self._createRaidDungeonTrap(dungeonNo)

        # set dungeon timeout
        endTime = int(self.spaceMgr.dungeonPlayMode.getTEnd(dungeonNo))
        endTime and self.client.changeDungeonRemainTime(self.spaceNo, endTime)
        # set autoCombat
        self.tryEnableAutoCombatAfterEnterSpace(dungeonNo)
        # callback raidDungeonStub
        extra = extra or {}
        extra.update({'src': src, 'playerName': self.name})
        dungeonStub = gameengine.getDungeonStubBySpaceNo(toSpaceNo)
        dungeonStub.enterDungeonSpaceSucc(toSpaceNo, self.base, self.gbId, self.raidUUID, extra)

        # if dataUtils.isDongfuWarDungeon(dungeonNo):
        #     actName = dataUtils.getActName(gameconst.ACT_ID_CONST.ACTIVITY_GUILD_DONGFU_WAR_ID)
        #     detail = {
        #         'guildUUID':self.guildUUID,
        #         'raidUUID':self.raidUUID,
        #         'spaceNo':toSpaceNo,
        #     }
        #     gamelog.makeDongfuWarActLog(self.gbId, gameconst.ACT_ID_CONST.ACTIVITY_GUILD_DONGFU_WAR_ID, actName,
        #                                 gameconst.ActivityLogType.EnterSucc, detail)
        #     self.base.activityComplete(gameconst.ACT_ID_CONST.ACTIVITY_GUILD_DONGFU_WAR_ID)
        #     teamMemNum = self.teamInfo.howManyMember() if self.teamInfo else 1
        #     self.base.onEnterDongfuWarDungeon(dungeonNo, toSpaceNo, self.teamId, teamMemNum, self.teamId==0)
        return True

    def _beforeLeave_raidDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_beforeLeave_raidDungeon::~')
        dungeonNo = formula.getDungeonNoBySpaceNo(fromSpaceNo)
        spaceMgr = self.spaceMgr
        if spaceMgr:
            spaceMgr.onLeaveWholeAureoleSpace(self.id)

        # stop auto combat
        self.tryDisableAutoCombatWhenLeaveSpace(dungeonNo)

        # remove dungeon buff
        self.removeBuffByTag(gameconst.BuffTag.Dungeon)

        position, direction, spaceNo = self._fetchCommonLeavePosAndDir(fromSpaceNo, toSpaceNo, options, context)

        if options.teleportType == gameconst.ComplexTeleportType.LEAVE:
            self.tryUnRegiTeleportOutsideRecord(toSpaceNo)

        if formula.isLineSpace(toSpaceNo):
            self.clearTeleportOutsideRecord()

        # if spaceMgr and spaceMgr.dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.GUILD_CHALLENGE:
        #     _kwargs = dict(
        #         GameSvrId=None, dtEventTime=None, vGameAppid=None,
        #         iBattleType=gametlog.BATTLETYPE.RaidChallenge,
        #         iBattleID=dungeonNo,
        #         iRoundTime=max(0, utils.getNow() - self.getSpaceEnterT()),
        #         iResult=int(spaceMgr.isDungeonWin),
        #         iRank=0
        #     )
        #     self.base.beforeLeaveDungeonHandleTLog(fromSpaceNo, toSpaceNo, _kwargs)

        # fix big world position
        bigWorldDungeonLeaveType = self._getPrmBydungeonNo(dungeonNo, 'leave')
        dungeonSpaceType = self._getPrmBydungeonNo(dungeonNo, 'type')
        if dungeonSpaceType and gameconst.DungeonType.isBigWorldDungeon(dungeonSpaceType) \
                and not bigWorldDungeonLeaveType:
            leave = GP_GP.datas[dungeonNo].get('leave', 0)
            if leave == 0:
                sceneRes = GP_GP.datas[dungeonNo].get('sceneRes', '')
                if sceneRes:
                    defaultMapID = GPSSDD.datas[sceneRes]['defaultMapID']
                    position = self.position
                    direction = self.direction
                    spaceNo = defaultMapID

        context['position'] = position
        context['direction'] = direction
        context['spaceNo'] = spaceNo
        return True

    def _afterLeave_raidDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_afterLeave_raidDungeon::~')
        raidUUID = context['l']['raidUUID']
        spaceMgrBox = context['l']['spaceMgrBox']
        extra = context['l']['extra']
        dungeonNo = formula.getDungeonNoBySpaceNo(fromSpaceNo)

        self.base.onLeaveDungeon(self.spaceNo, fromSpaceNo)
        if spaceMgrBox:
            spaceMgrBox.cell.onPlayerLeave(self.gbId, self.id, self.base)
        self.spaceMgrId = 0

        # callback raidDungeonStub
        dungeonStub = gameengine.getDungeonStubBySpaceNo(fromSpaceNo)
        dungeonStub.leaveDungeonSpaceSucc(fromSpaceNo, self.base, self.gbId, raidUUID, extra)

        if self.isDie():
            self._relive()
            self.modifyHP(self.getDefaultReliveHp(), self.id, gameconst.SourceType.Default, self.id)

        self.selfStopAutoCombat('leave raid dungeon')
        # 离开团队副本了，清理奖励记录
        if not formula.isRaidDungeonSpace(toSpaceNo):
            gameengine.getRaidStub(raidUUID).clearRaidDungeonRewardRecord(raidUUID, self.gbId)
        return True

    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # SINGLE DUNGEON
    # ----------------------------------------------------------------------

    @gamedecorator.checkTeleportLock(gameconst.TeleportLock.ENTER_DUNGEON)
    def _beforeEnter_singleDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        WARNING_MSG('_beforeEnter_singleDungeon::~')
        extra = context['e']['extra']

        self.tryRegiTeleportOutsideRecord(fromSpaceNo, options)

        dungeonNo = formula.getDungeonNoBySpaceNo(toSpaceNo)
        dungeonSpaceType = self._getPrmBydungeonNo(dungeonNo, 'type')
        dungeonEnterType = self._getPrmBydungeonNo(dungeonNo, 'enterType')

        position = extra.get('position')
        if not position:
            if gameconst.DungeonType.isNormalSingleDungeon(dungeonSpaceType, dungeonEnterType):
                # common dungeon un-support no entrance configs
                gameengine.reportCritical('_beforeEnter_singleDungeon:: common dungeon entrance position not define', dungeonNo, toSpaceNo)
                return

            # 【【任务】副本类型扩展-帮会副本】
            elif gameconst.DungeonType.isGuildSingleDungeon(dungeonSpaceType, dungeonEnterType):
                WARNING_MSG('_beforeEnter_singleDungeon:: try to reset entrance position to guild entrance', dungeonNo, toSpaceNo)
                position = self._getPrmBydungeonNo(gameconst.MapIdDef.mapGuildSpace, 'entrance')
                if not position:
                    # NOTE: position in guild single dungeon must set position in self or guild space
                    gameengine.reportCritical('_beforeEnter_singleDungeon:: guild dungeon entrance position not defined', dungeonNo, toSpaceNo)
                    return

            # 【【任务】副本类型支持小世界场景副本】
            elif gameconst.DungeonType.isHomeSingleDungeon(dungeonSpaceType, dungeonEnterType):
                WARNING_MSG('_beforeEnter_singleDungeon:: try to reset entrance position to guild entrance', dungeonNo, toSpaceNo)
                position = self._getPrmBydungeonNo(gameconst.MapIdDef.mapMyHome, 'entrance')
                if not position:
                    # NOTE: position in home single dungeon must set position in self or home space
                    gameengine.reportCritical('_beforeEnter_singleDungeon:: home dungeon entrance position not defined', dungeonNo, toSpaceNo)
                    return

            else:
                WARNING_MSG('_beforeEnter_singleDungeon:: reset entrance position to self position', dungeonNo, toSpaceNo, self.position)
                position = self.position

        direction = extra.get('direction')
        if not direction:
            direction = self._getEntranceDirByDungeonNo(formula.getMapId(toSpaceNo))
        if direction is not None:
            direction = (0, 0, direction * math.pi / 180)

        else:
            # 【【任务】副本类型扩展-帮会副本】
            if gameconst.DungeonType.isGuildSingleDungeon(dungeonSpaceType, dungeonEnterType):
                WARNING_MSG('_beforeEnter_singleDungeon:: try resetting guild dungeon entrance direction to guild entrance', dungeonNo, toSpaceNo)
                direction = self._getEntranceDirByDungeonNo(gameconst.MapIdDef.mapGuildSpace)
                direction = (0, 0, direction * math.pi / 180) if direction is not None else self.direction

            # 【【任务】副本类型支持小世界场景副本】
            elif gameconst.DungeonType.isHomeSingleDungeon(dungeonSpaceType, dungeonEnterType):
                WARNING_MSG("_beforeEnter_singleDungeon:: try resetting home dungeon entrance direction to home entrance", dungeonNo, toSpaceNo)
                direction = self._getEntranceDirByDungeonNo(gameconst.MapIdDef.mapMyHome)
                direction = (0, 0, direction * math.pi / 180) if direction is not None else self.direction

            else:
                WARNING_MSG('_beforeEnter_singleDungeon:: reset entrance direction to self direction', dungeonNo, toSpaceNo, self.position)
                direction = self.direction

        # set teleport lock
        self.aquireTeleportLock(gameconst.TeleportLock.ENTER_DUNGEON)

        context['position'] = position
        context['direction'] = direction
        context['spaceNo'] = toSpaceNo
        return True

    def _afterEnter_singleDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_afterEnter_singleDungeon::~')
        spaceMgrBox = context['e']['spaceMgrBox']
        spaceMgrId = spaceMgrBox.id
        playerBox = context['e']['playerBox']
        playerGbId = context['e']['playerGbId']
        teamUUID = context['e']['teamUUID']
        extra = context['e']['extra']

        # release lock
        self.releaseTeleportLock(gameconst.TeleportLock.ENTER_DUNGEON)
        self.releaseGlobalTeleportLock('telsucc')

        # create dungeon trap
        dungeonNo = formula.getMapId(toSpaceNo)
        self._createSingleDungeonTrap(dungeonNo)

        self.spaceMgrId = spaceMgrId
        spaceMgr = self.spaceMgr
        spaceMgr.onPlayerEnter(self.id)

        # 【【死亡复活】玩家在大世界内死亡后，通过点击个人资料-头像-驭灵殿按钮进入副本后需要复活玩家】
        # NOTE(): 进入副本前复活会导致hp同步不到客户端导致显示问题, 先放在后面
        if self.isDie():
            self._relive()
            self.modifyHP(self.getDefaultReliveHp(), self.id, gameconst.SourceType.Default, self.id)

        # send real end time to avatar self client
        endTime = int(spaceMgr.dungeonPlayMode.getTEnd(dungeonNo))
        endTime and self.client.changeDungeonRemainTime(toSpaceNo, endTime)

        self.base.onEnterDungeon(toSpaceNo, spaceMgrBox, extra)

        self.tryEnableAutoCombatAfterEnterSpace(dungeonNo)
        extra['spaceUUID'] = spaceMgr.dungeonPlayMode.spaceUUID
        gameengine.getDungeonStubBySpaceNo(toSpaceNo).enterDungeonSpaceSucc(
            toSpaceNo, playerBox, playerGbId, teamUUID, extra)

        return True

    def _beforeLeave_singleDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_beforeLeave_singleDungeon::~')
        overwrite = context['l'].get('overwrite')
        dungeonNo = formula.getDungeonNoBySpaceNo(fromSpaceNo)
        spaceMgr = self.spaceMgr
        if spaceMgr:
            spaceMgr.onLeaveWholeAureoleSpace(self.id)

        self.tryDisableAutoCombatWhenLeaveSpace(dungeonNo)

        self.removeBuffByTag(gameconst.BuffTag.Dungeon)

        position, direction, spaceNo = self._fetchCommonLeavePosAndDir(fromSpaceNo, toSpaceNo, options, context)
        _m_outRecord = self.tryGetTeleportOutesideRecord(toSpaceNo)
        if _m_outRecord and _m_outRecord.isDie:
            context['needRelive'] = False
            if not self.isDie():
                self.modifyHP(-self.hp, self.id, gameconst.SourceType.Default, self.id)
        else:
            if self.isDie():
                self._relive()
                self.modifyHP(self.getDefaultReliveHp(), self.id, gameconst.SourceType.Default, self.id)

        if options.teleportType == gameconst.ComplexTeleportType.LEAVE:
            self.tryUnRegiTeleportOutsideRecord(toSpaceNo)

        if formula.isLineSpace(toSpaceNo):
            self.clearTeleportOutsideRecord()

        dungeonPlayMode = spaceMgr.dungeonPlayMode.playMode if spaceMgr else gameconst.DungeonPlayModeEnum.UNKNOWN

        # fix big world position
        bigWorldDungeonLeaveType = self._getPrmBydungeonNo(dungeonNo, 'leave')
        dungeonSpaceType = self._getPrmBydungeonNo(dungeonNo, 'type')
        if dungeonSpaceType and gameconst.DungeonType.isBigWorldDungeon(dungeonSpaceType) \
                and not bigWorldDungeonLeaveType:
            leave = GP_GP.datas[dungeonNo].get('leave', 0)
            if leave == 0:
                sceneRes = GP_GP.datas[dungeonNo].get('sceneRes', '')
                if sceneRes:
                    defaultMapID = GPSSDD.datas[sceneRes]['defaultMapID']
                    position = self.position
                    direction = self.direction
                    spaceNo = defaultMapID

        context['position'] = position
        context['direction'] = direction
        context['spaceNo'] = spaceNo
        # 兼容特殊位置传送
        if overwrite:
            if 'position' in overwrite:
                context['position'] = overwrite['position']
            if 'direction' in overwrite:
                context['direction'] = overwrite['direction']
        return True

    def _afterLeave_singleDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_afterLeave_singleDungeon::~')
        spaceMgrBox = context['l']['spaceMgrBox']
        dungeonNo = formula.getDungeonNoBySpaceNo(fromSpaceNo)


        self.base.onLeaveDungeon(self.spaceNo, fromSpaceNo)
        if spaceMgrBox:
            spaceMgrBox.cell.onPlayerLeave(self.gbId, self.id, self.base)
        self.spaceMgrId = 0

        if formula.isDungeonSpace(fromSpaceNo):
            gameengine.getDungeonStubByDungeonNo(
                dungeonNo, gameconst.DungeonEnterType.SINGLE).leaveDungeonSpaceSucc(
                    fromSpaceNo, self.base, self.gbId, self.teamId, {'spaceNo': self.spaceNo,
                    'spaceUUID': context['l']['spaceUUID']})
        else:
            pass

        # if self.isDie():
        #     self._relive()
        #     self.modifyHP(self.getDefaultReliveHp(), self.id, gameconst.SourceType.Default, self.id)

        self.selfStopAutoCombat('leave single dungeon')

        return True

    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # TEAM DUNGEON
    # ----------------------------------------------------------------------

    @gamedecorator.checkTeleportLock(gameconst.TeleportLock.ENTER_DUNGEON)
    def _beforeEnter_teamDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_beforeEnter_teamDungeon::~')
        extra = context['e']['extra']

        self.tryRegiTeleportOutsideRecord(fromSpaceNo, options)

        dungeonNo = formula.getDungeonNoBySpaceNo(toSpaceNo)
        position = extra.get("position") or self._getPrmBydungeonNo(dungeonNo, 'entrance')
        dungeonSpaceType = self._getPrmBydungeonNo(dungeonNo, 'type')
        dungeonEnterType = self._getPrmBydungeonNo(dungeonNo, 'enterType')
        if not position:
            if gameconst.DungeonType.isNormalTeamDungeon(dungeonSpaceType, dungeonEnterType):
                # common dungeon un-support no entrance configs
                gameengine.reportCritical('_beforeEnter_teamDungeon:: common dungeon entrance position not define', dungeonNo, toSpaceNo)
                return

            # 【【任务】副本类型扩展-帮会副本】
            elif gameconst.DungeonType.isGuildTeamDungeon(dungeonSpaceType, dungeonEnterType):
                WARNING_MSG('_beforeEnter_teamDungeon:: try to reset entrance position to guild entrance', dungeonNo, toSpaceNo)
                position = self._getPrmBydungeonNo(gameconst.MapIdDef.mapGuildSpace, 'entrance')
                if not position:
                    # NOTE: position in guild team dungeon must set position in self or guild space
                    gameengine.reportCritical('_beforeEnter_teamDungeon:: guild dungeon entrance position not defined', dungeonNo, toSpaceNo)
                    return

            # 【【任务】副本类型支持小世界场景副本】
            elif gameconst.DungeonType.isHomeTeamDungeon(dungeonSpaceType, dungeonEnterType):
                WARNING_MSG('_beforeEnter_teamDungeon:: try to reset entrance position to home entrance', dungeonNo, toSpaceNo)
                position = self._getPrmBydungeonNo(gameconst.MapIdDef.mapMyHome, 'entrance')
                if not position:
                    # NOTE: position in home team dungeon must set position in self or home space
                    gameengine.reportCritical('_beforeEnter_teamDungeon:: home dungeon entrance position not defined', dungeonNo, toSpaceNo)
                    return

            else:
                WARNING_MSG('_beforeEnter_teamDungeon:: reset entrance position to self position', dungeonNo, toSpaceNo, self.position)
                position = self.position

        direction = extra.get("direction") or self._getEntranceDirByDungeonNo(formula.getMapId(toSpaceNo))
        if direction is not None:
            direction = (0, 0, direction * math.pi / 180)

        else:
            # 【【任务】副本类型扩展-帮会副本】
            if gameconst.DungeonType.isGuildTeamDungeon(dungeonSpaceType, dungeonEnterType):
                WARNING_MSG('_beforeEnter_teamDungeon:: try resetting guild dungeon entrance direction to guild entrance', dungeonNo, toSpaceNo)
                direction = self._getEntranceDirByDungeonNo(gameconst.MapIdDef.mapGuildSpace)
                direction = (0, 0, direction * math.pi / 180) if direction is not None else self.direction

            # 【【任务】副本类型支持小世界场景副本】
            elif gameconst.DungeonType.isHomeTeamDungeon(dungeonSpaceType, dungeonEnterType):
                WARNING_MSG('_beforeEnter_teamDungeon:: try resetting home dungeon entrance direction to home entrance', dungeonNo, toSpaceNo)
                direction = self._getEntranceDirByDungeonNo(gameconst.MapIdDef.mapMyHome)
                direction = (0, 0, direction * math.pi / 180) if direction is not None else self.direction

            else:
                WARNING_MSG('_beforeEnter_teamDungeon:: reset entrance direction to self direction', dungeonNo, toSpaceNo, self.position)
                direction = self.direction

        # set teleport lock
        self.aquireTeleportLock(gameconst.TeleportLock.ENTER_DUNGEON)

        context['position'] = position
        context['direction'] = direction
        context['spaceNo'] = toSpaceNo
        return True

    def _afterEnter_teamDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_afterEnter_teamDungeon::~')
        spaceMgrBox = context['e']['spaceMgrBox']
        dungeonNo = formula.getDungeonNoBySpaceNo(toSpaceNo)
        teamUUID = context['e']['teamUUID']
        extra = context['e']['extra']

        # release lock
        self.releaseTeleportLock(gameconst.TeleportLock.ENTER_DUNGEON)
        self.releaseGlobalTeleportLock('telsucc')

        # create dungeon trap
        self._createTeamDungeonTrap(dungeonNo)

        self.spaceMgrId = spaceMgrBox.id
        self.spaceMgr.onPlayerEnter(self.id)
        self.spaceMgr.dungeonGoodManColl.update(extra.get("goodManList", ()))
        if not self.spaceMgr.dungeonGoodManActId:
            self.spaceMgr.dungeonGoodManActId = extra.get("goodManActId", 0)

        # 【【死亡复活】玩家在大世界内死亡后，通过点击个人资料-头像-驭灵殿按钮进入副本后需要复活玩家】
        # NOTE(): 进入副本前复活会导致hp同步不到客户端导致显示问题, 先放在后面
        if self.isDie():
            self._relive()
            self.modifyHP(self.getDefaultReliveHp(), self.id, gameconst.SourceType.Default, self.id)

        # send real end time to avatar self client
        endTime = int(self.spaceMgr.dungeonPlayMode.getTEnd(dungeonNo))
        endTime and self.client.changeDungeonRemainTime(toSpaceNo, endTime)

        if self.spaceMgr.dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            _kwargs = dict(
                GameSvrId=None, dtEventTime=None, vGameAppid=None,
                iBattleID=dungeonNo,
                iTeamID=self.teamId,
                TeamUserNum=self.teamInfo.howManyMember(),
            )
            extra['tlogProps'] = _kwargs
            extra['actId'] = gameconst.ACT_ID_CONST.ACTIVITY_CRUSADE_ID
            self.base.onEnterCrusadeDungeon(toSpaceNo, spaceMgrBox, extra)
        else:
            self.base.onEnterDungeon(toSpaceNo, spaceMgrBox, extra)

        self.tryEnableAutoCombatAfterEnterSpace(dungeonNo)

        teamStub = gameengine.getTeamStub(self.teamId)
        teamStub.onEnterTeamDungeon(
            self.base, self.gbId, teamUUID, dungeonNo, toSpaceNo)
        return True

    def _beforeLeave_teamDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_beforeLeave_teamDungeon::~')
        dungeonNo = formula.getDungeonNoBySpaceNo(fromSpaceNo)
        spaceMgr = self.spaceMgr
        if spaceMgr:
            spaceMgr.onLeaveWholeAureoleSpace(self.id)

        dungeonSpaceType = self._getPrmBydungeonNo(dungeonNo, 'type')
        dungeonEnterType = self._getPrmBydungeonNo(dungeonNo, 'enterType')
        if not gameconst.DungeonType.isTeamDungeon(dungeonSpaceType, dungeonEnterType):
            ERROR_MSG('error dungeonType: {}/{}'.format(dungeonNo, dungeonSpaceType))
            return

        self.tryDisableAutoCombatWhenLeaveSpace(dungeonNo)

        self.removeBuffByTag(gameconst.BuffTag.Dungeon)

        position, direction, spaceNo = self._fetchCommonLeavePosAndDir(fromSpaceNo, toSpaceNo, options, context)
        _m_outRecord = self.tryGetTeleportOutesideRecord(toSpaceNo)
        if _m_outRecord and _m_outRecord.isDie:
            context['needRelive'] = False
            if not self.isDie():
                self.modifyHP(-self.hp, self.id, gameconst.SourceType.Default, self.id)
        else:
            if self.isDie():
                self._relive()
                self.modifyHP(self.getDefaultReliveHp(), self.id, gameconst.SourceType.Default, self.id)

        # dungeonPlayMode = spaceMgr.dungeonPlayMode.playMode if spaceMgr else gameconst.DungeonPlayModeEnum.UNKNOWN

        bigWorldDungeonLeaveType = self._getPrmBydungeonNo(dungeonNo, 'leave')
        dungeonSpaceType = self._getPrmBydungeonNo(dungeonNo, 'type')
        if dungeonSpaceType and gameconst.DungeonType.isBigWorldDungeon(dungeonSpaceType) \
                and not bigWorldDungeonLeaveType:
            leave = GP_GP.datas[dungeonNo].get('leave', 0)
            if leave == 0:
                sceneRes = GP_GP.datas[dungeonNo].get('sceneRes', '')
                if sceneRes:
                    defaultMapID = GPSSDD.datas[sceneRes]['defaultMapID']
                    position = self.position
                    direction = self.direction
                    spaceNo = defaultMapID

        if options.teleportType == gameconst.ComplexTeleportType.LEAVE:
            self.tryUnRegiTeleportOutsideRecord(toSpaceNo)

        if formula.isLineSpace(toSpaceNo):
            self.clearTeleportOutsideRecord()

        context['position'] = position
        context['direction'] = direction
        context['spaceNo'] = spaceNo
        return True

    def _afterLeave_teamDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_afterLeave_teamDungeon::~')
        teamUUID = context['l']['teamUUID']
        dungeonNo = formula.getDungeonNoBySpaceNo(fromSpaceNo)
        spaceMgrBox = context['l']['spaceMgrBox']

        self.base.onLeaveDungeon(self.spaceNo, fromSpaceNo)
        if spaceMgrBox:
            spaceMgrBox.cell.onPlayerLeave(self.gbId, self.id, self.base)
        self.spaceMgrId = 0

        # callback teamDungeonStub
        dungeonStub = gameengine.getDungeonStubBySpaceNo(fromSpaceNo)
        dungeonStub.leaveDungeonSpaceSucc(fromSpaceNo, self.base, self.gbId, teamUUID, {})


        # if self.isDie():
        #     self._relive()
        #     self.modifyHP(self.getDefaultReliveHp(), self.id, gameconst.SourceType.Default, self.id)

        self.selfStopAutoCombat('leave team dungeon')
        # 离开组队副本了，清理奖励记录
        if not formula.isTeamDungeonSpace(toSpaceNo):
            gameengine.getTeamStub(teamUUID).clearTeamDungeonRewardRecord(teamUUID, self.gbId)
        return True

    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # WORLD LINE
    # ----------------------------------------------------------------------

    def _beforeEnter_worldLine(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_beforeEnter_worldLine::~')
        context.setdefault('position', self.position)
        context.setdefault('direction', self.direction)
        context.setdefault('spaceNo', toSpaceNo)

        if formula.getMapId(fromSpaceNo) == formula.getMapId(toSpaceNo):
            r = self.aquireTeleportLock(gameconst.TeleportLock.SWITCH_LINE)
        else:
            r = self.aquireTeleportLock(gameconst.TeleportLock.ENTER_LINE)
        if not r:
            ERROR_MSG("_beforeEnter_worldLine:: aquire teleportlock failed", self.teleportLock, self.teleportLockRlsT)
            return r

        overwrite = context['e'].get('overwrite')
        if overwrite:
            if 'position' in overwrite:
                context['position'] = overwrite['position']
            if 'direction' in overwrite:
                context['direction'] = overwrite['direction']
            if 'spaceNo' in overwrite:
                context['spaceNo'] = overwrite['spaceNo']

        return True

    def _afterEnter_worldLine(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_afterEnter_worldLine::~')

        self.releaseTeleportLock(gameconst.TeleportLock.ENTER_LINE)
        self.releaseGlobalTeleportLock('telsucc')

        self.resetStatisticsData()
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed

        # 【【任务】离开场景关闭自动战斗对gamePlay全部生效】
        self.tryEnableAutoCombatAfterEnterSpace(formula.getDungeonNoBySpaceNo(toSpaceNo))

        # clear all records
        self.clearTeleportOutsideRecord()
        if context.get('needRelive', True):
            self._onEnterLineRelive()
        return True

    def _beforeLeave_worldLine(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_beforeLeave_worldLine::~')

        # 【【任务】离开场景关闭自动战斗对gamePlay全部生效】
        self.tryDisableAutoCombatWhenLeaveSpace(formula.getDungeonNoBySpaceNo(fromSpaceNo))
        if not formula.isLineSpace(toSpaceNo):
            self._applyLeaveLineInternal(fromSpaceNo, 0, gameconst.POSITION_ZERO, gameconst.DIRECTION_ZERO)

        context['spaceMgrCell'] = self.spaceMgr

        return True

    def _afterLeave_worldLine(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_afterLeave_worldLine::~', fromSpaceNo, toSpaceNo)
        context['spaceMgrCell'].onPlayerLeave(self.gbId, self.id, self.base)
        self.spaceMgrId = 0

        return True

    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # cube
    # ----------------------------------------------------------------------

    def _beforeEnter_cube(self, fromSpaceNo, toSpaceNo, options, context):
        self.tryRegiTeleportOutsideRecord(fromSpaceNo, options)

        _extra = context['cube']
        _dir = self._getEntranceDirByDungeonNo(formula.getMapId(toSpaceNo))
        if _extra.get('followPos'):
            context['position'] = _extra['followPos']
        else:
            context['position'] = self._getEntranceByDungeonNo(formula.getMapId(toSpaceNo))

        context['direction'] = (0, 0, _dir * math.pi / 180) if _dir is not None else self.direction
        context['spaceNo'] = toSpaceNo
        return True

    def _afterEnter_cube(self, fromSpaceNo, toSpaceNo, options, context):
        self.spaceMgrId = context['e']['spaceMgrId']
        self.spaceMgr.onPlayerEnter(self.id)

        gameengine.getGlobalBase('CubeStub').onEnterCubeSuccess(self.gbId, toSpaceNo)

        _extra = context['cube']
        if _extra.get('needSetLeftTime'):
            self.onEnterCubeSetTime()

        _toMapId = formula.getMapId(toSpaceNo)
        if dataUtils.isCubeCow(_toMapId):
            _fromMapId = formula.getMapId(fromSpaceNo)
            self.fromCubeMapId = _fromMapId
            self.startCubeCowTimer()

        return True

    def _beforeLeave_cube(self, fromSpaceNo, toSpaceNo, options, context):
        position, direction, spaceNo = self._fetchCommonLeavePosAndDir(fromSpaceNo, toSpaceNo, options, context)

        if options.teleportType == gameconst.ComplexTeleportType.LEAVE:
            self.tryUnRegiTeleportOutsideRecord(toSpaceNo)

        if formula.isLineSpace(toSpaceNo):
            self.clearTeleportOutsideRecord()

        context['position'] = position
        context['direction'] = direction
        context['spaceNo'] = spaceNo

        return True

    def _afterLeave_cube(self, fromSpaceNo, toSpaceNo, options, context):
        _spaceMgrCell = context['l']['spaceMgrCell']
        _spaceMgrCell.onPlayerLeave(self.gbId, self.id, self.base)

        self.spaceMgrId = 0
        gameengine.getGlobalBase('CubeStub').onLeaveCube(self.gbId, fromSpaceNo, toSpaceNo)
        if not formula.isCubeSpace(toSpaceNo):
            if self.getTempMiscProp(gameconst.AvatarProps.cubeAutoRenewSwitch) is not None:
                self._changeCubeAutoRenewSwitch(False, {})

            self.setCubeRoomLeftTime(0)

            if self.cubeRoomTimerId:
                self._cancelDatetimeCallback(self.cubeRoomTimerId, gametimer.TIMER_TAG_CUBE_ROOM)

            self.clearCubeRoomRewardRecord()

        return True
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # wonderland
    # ----------------------------------------------------------------------

    def _beforeEnter_wonderLand(self, fromSpaceNo, toSpaceNo, options, context):
        self.tryRegiTeleportOutsideRecord(fromSpaceNo, options)

        _dir = self._getEntranceDirByDungeonNo(formula.getMapId(toSpaceNo))
        context['position'] = self._getEntranceByDungeonNo(formula.getMapId(toSpaceNo))
        context['direction'] = (0, 0, _dir * math.pi / 180) if _dir is not None else self.direction
        context['spaceNo'] = toSpaceNo
        return True

    def _afterEnter_wonderLand(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_afterEnter_wonderland::~')
        self.spaceMgrId = context['e']['spaceMgrId']
        self.spaceMgr.onPlayerEnter(self.id)

        gameengine.getWonderLandStubBySpaceNo(toSpaceNo).onEnterWonderLandSuccess(self.gbId, toSpaceNo)
        self._startWonderLandTimerOnEnter()
        _bossList = list(self.spaceMgr.collToBoss.values())
        self.client.onWonderLandBossInfo(_bossList)
        self.base.afterEnterWonderLandDeductTimes()
        return True

    def _beforeLeave_wonderLand(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_beforeLeave_wonderland::~')
        position, direction, spaceNo = self._fetchCommonLeavePosAndDir(fromSpaceNo, toSpaceNo, options, context)

        if options.teleportType == gameconst.ComplexTeleportType.LEAVE:
            self.tryUnRegiTeleportOutsideRecord(toSpaceNo)

        if formula.isLineSpace(toSpaceNo):
            self.clearTeleportOutsideRecord()

        context['position'] = position
        context['direction'] = direction
        context['spaceNo'] = spaceNo

        return True

    def _afterLeave_wonderLand(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_afterLeave_wonderland::~')
        _spaceMgrCell = context['l']['spaceMgrCell']
        _spaceMgrCell.onPlayerLeave(self.gbId, self.id, self.base)

        self.spaceMgrId = 0
        gameengine.getWonderLandStubBySpaceNo(fromSpaceNo).onLeaveWonderLand(self.gbId)
        self.afterLeaveWonderLand()
        return True
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # siegeWar
    # ----------------------------------------------------------------------

    def _beforeEnter_siegeWar(self, fromSpaceNo, toSpaceNo, options, context):
        self.tryRegiTeleportOutsideRecord(fromSpaceNo, options)
        camp = self.siegeWarCamp

        _dir = self._getEntranceDirByDungeonNo(formula.getMapId(toSpaceNo))

        
        dunSData = utils.getDunStructureModuleData(formula.getMapId(toSpaceNo))
        if camp == 1:
            d, *_ = dunSData['attackRevive'].values()
        elif camp == 2:
            d, *_ = dunSData['defendRevive'].values()
        
        context['position'] = (d['PosX'], d['PosY'], d['PosZ'])
        context['direction'] = (0, 0, _dir * math.pi / 180) if _dir is not None else self.direction
        context['spaceNo'] = toSpaceNo
        return True

    def _afterEnter_siegeWar(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_afterEnter_siegeWar::~')
        self.spaceMgrId = context['e']['spaceMgrId']
        self.spaceMgr.onPlayerEnter(self.id)
        return True

    def _beforeLeave_siegeWar(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_beforeLeave_siegeWar::~')
        position, direction, spaceNo = self._fetchCommonLeavePosAndDir(fromSpaceNo, toSpaceNo, options, context)

        if options.teleportType == gameconst.ComplexTeleportType.LEAVE:
            self.tryUnRegiTeleportOutsideRecord(toSpaceNo)

        if formula.isLineSpace(toSpaceNo):
            self.clearTeleportOutsideRecord()

        context['position'] = position
        context['direction'] = direction
        context['spaceNo'] = spaceNo

        return True

    def _afterLeave_siegeWar(self, fromSpaceNo, toSpaceNo, options, context):
        INFO_MSG('_afterLeave_siegeWar::~')
        _spaceMgrCell = context['l']['spaceMgrCell']
        _spaceMgrCell.onPlayerLeave(self.gbId, self.id, self.base)

        self.spaceMgrId = 0
        return True

# -----------------------------------------
# INIT
if not gameglobal.complexTeleportTypeFnMap:
    IComplexTeleport.regrAllComplexTeleportMethods()
# -----------------------------------------
