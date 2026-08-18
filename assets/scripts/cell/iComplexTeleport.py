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
import LogTrackingMgr

import cube_config
import cube_floor
import cube_room
import gamePlay_gamePlay as GP_GPD
import conflict_conflict_def as C_C_DD
import message_Message_def as MMD
import gamePlay_singleSceneData as GPSSDD
import wonderLand_floor as WL_FD
import wonderLand_config as WL_CD
import abyss_floor as AB_FD
import abyss_config as AB_CD

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
        LOG_INFO('enterWorldLine::~', lineType, lineNo, desTelId)
        src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        self._enterWorldLine(lineType, lineNo, desTelId, src)

    def _enterWorldLine(self, lineType, lineNo, desTelId, src, position=None, direction=None):
        """进入大世界分线"""
        if not self.canDoCompleteTeleport(canLeaveFromLine=True, noErrorMsg=True):
            LOG_WARN('_enterWorldLine:: can\'t enter space from current spaceNo', self.spaceNo)
            return
        if lineNo >= utils.fetchLineMaxNumber(gameconst.MapIdDef.mapWorldLine):
            LOG_WARN("_enterWorldLine:: can\'t enter lineNo", lineNo)
            return
        if formula.inWorldLineScene(self.spaceNo):
            # NOTE(): 客户端不允许在大世界接口使用·enterWorldLine·重新进入大世界
            LOG_WARN("_enterWorldLine:: can\'t enter line if already in worldline", lineNo, self.spaceNo)
            return

        self.doEnterWorldLine(lineType, lineNo, src, desTelId, position, direction)

    def doEnterWorldLine(self, lineType, lineNo, src, desTelId, position=None, direction=None):
        LOG_INFO("doEnterWorldLine::", lineType, lineNo, src, desTelId, position, direction)
        lCtx = {'extra': {}}
        eCtx = {
            'lineType': lineType,
            'lineNo': lineNo, 
        }
        context = {'l': lCtx, 'e': eCtx, 'src': src}
        options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.ENTER)

        spaceNo = formula.combineLineSpaceNo(lineType, lineNo)
        if desTelId:
            telEnt = utils.getTeleporterByID(desTelId, spaceNo)
            if telEnt:
                entityData = utils.getDunModuleData(lineType)
                _telInfo = entityData.get(str(utils.parseGidFromGameEntityId(telEnt.gameEntityId)), None)
                if _telInfo:
                    dstPos = (_telInfo['PosX'], _telInfo['PosY'], _telInfo['PosZ'])
                    eCtx.setdefault('overwrite', {}).update({'position': dstPos})

        if position:
            eCtx.setdefault('overwrite', {}).update({'position': position})
        if direction:
            eCtx.setdefault('overwrite', {}).update({'direction': direction})

        canLeave = self.packComplexTeleportLeaveData(lCtx, canLeaveFromLine=True)
        if not canLeave:
            if canLeave.extra not in gameconst.CompleteTeleportLeaveFailReason.COLL_USEROPRERRNO:
                gameengine.panicStack('enterWorldLine::fatal error when try to enter world line', self.spaceNo, context)
            else:
                LOG_WARN("enterWorldLine::failed, errno={}".format(canLeave.extra), self.spaceNo, context)
            return

        if not self.onCheckMapUnlocked(lineType):
            return

        self.telFromSpaceToSpace(self.spaceNo, spaceNo, options=options, context=context)

    def switchSelfLine(self, lineNo, src):
        LOG_INFO("switchSelfLine::", lineNo, src)
        assert lineNo >= 0
        lCtx = {'extra': {}}
        eCtx = {'lineNo': lineNo}
        _context = {'l': lCtx, 'e': eCtx, 'src': src}
        options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.ENTER)

        canLeave = self.packComplexTeleportLeaveData(lCtx, canLeaveFromLine=True)
        if not canLeave:
            if canLeave.extra not in gameconst.CompleteTeleportLeaveFailReason.COLL_USEROPRERRNO:
                gameengine.panicStack('switchSelfLine::fatal error when try to enter world line', self.spaceNo, _context)
            else:
                LOG_WARN("switchSelfLine::failed, errno={}".format(canLeave.extra), self.spaceNo, _context)
            return

        fromSpaceNo = self.spaceNo
        fromSpaceLineNo = formula.parseLineNo(fromSpaceNo)
        if fromSpaceLineNo == lineNo:
            gameengine.panicStack('switchSelfLine::cant enter smae lineno', fromSpaceNo, fromSpaceLineNo, lineNo)
            return

        if not self._checkSwitchLine(lineNo):
            LOG_ERR("switchSelfLine:: check switch line failed", fromSpaceNo, fromSpaceLineNo, lineNo)
            return

        toSpaceNo = formula.combineLineSpaceNo(formula.fetchMapId(fromSpaceNo), lineNo)
        self.telFromSpaceToSpace(self.spaceNo, toSpaceNo, options=options, context=_context)

    @property
    def lastTeleportSpaceNoRecord(self):
        return self.getTempMiscProp(gameconst.EntityPropsEnum.lastTeleportSpaceNoRecord, 0)

    @lastTeleportSpaceNoRecord.setter
    def lastTeleportSpaceNoRecord(self, spaceNo):
        self.setTempMiscProp(gameconst.EntityPropsEnum.lastTeleportSpaceNoRecord, spaceNo)

    @property
    def lastTeleportWorldlinePosRecord(self):
        return self.getPersistentMiscProp(gameconst.EntityPropsEnum.lastTeleportWorldlinePosRecord, 0)

    @property
    def complexTeleportTypeFnMap(self):
        return gameglobal.complexTeleportTypeFnMap

    @lastTeleportWorldlinePosRecord.setter
    def lastTeleportWorldlinePosRecord(self, position):
        self.setPersistentMiscProp(gameconst.EntityPropsEnum.lastTeleportWorldlinePosRecord, position)

    def getTeleportOutsideRecord(self):
        _mRcdDic = self.getPersistentMiscProp(gameconst.EntityPropsEnum.outsideRecords)
        if _mRcdDic is None or not isinstance(_mRcdDic, collections.OrderedDict):
            _mRcdDic = collections.OrderedDict()
            self.setPersistentMiscProp(gameconst.EntityPropsEnum.outsideRecords, _mRcdDic)
        return _mRcdDic

    def updateWithTeleportOutsideRecord(self, outRcd):
        _mRcdDic = self.getTeleportOutsideRecord()
        _mMapId = formula.fetchMapId(outRcd.spaceNo)
        _mRcdDic.pop(_mMapId, None)
        _mRcdDic[_mMapId] = outRcd
        return _mRcdDic

    def clearTeleportOutsideRecord(self):
        self.getTeleportOutsideRecord().clear()

    def popTeleportOutsideRecord(self, mapId, default=None):
        return self.getTeleportOutsideRecord().pop(mapId, default)

    def tryRegiTeleportOutsideRecord(self, spaceNo, options, reg=False):
        if self._shouldRecordTeleportOutsideRecord(spaceNo, options.teleportType) or reg:
            _mOutsideRecord = outsideRecord.OutsideRecord(
                self.spaceNo, self.position, self.direction, self.hp, self.mp,\
                self.isDie())

            self.updateWithTeleportOutsideRecord(_mOutsideRecord)

    def tryUnRegiTeleportOutsideRecord(self, spaceNo):
        m_mapId = formula.fetchMapId(spaceNo)
        self.popTeleportOutsideRecord(m_mapId)

    def fetchTeleportOutesideRecord(self, spaceNo, default=None):
        return self.getTeleportOutsideRecord().get(formula.fetchMapId(spaceNo), default)

    def _shouldRecordTeleportOutsideRecord(self, spaceNo, teleportType):
        if teleportType != gameconst.ComplexTeleportEnum.ENTER:
            return False

        m_mapId = formula.fetchMapId(spaceNo)
        if m_mapId in gameconst.MapIdDef.mapWorldSet:
            return True

        return False

    def tryGetLastTeleportOutesideRecord(self, fromSpaceNo, spaceType=0):
        _m_records = self.getTeleportOutsideRecord()
        self.mineWarChangeOutsideRecord(_m_records)
        for i_mapId in reversed(list(_m_records)):
            # 大世界分线
            if i_mapId in gameconst.MapIdDef.mapWorldSet or formula._isInnerDemonSpace(_m_records[i_mapId].spaceNo):
                # BOSS互斥组冷却中的地图不能回传，跳过该记录，由调用方走兜底(回主城)
                # 记录中的 spaceNo 可精确到分线，同分线（触发冷却的源分线）允许回传
                _toLineNo = formula.parseLineNo(_m_records[i_mapId].spaceNo)
                _isBlocked, _leftSec = self.checkBossMutexBlock(i_mapId, _toLineNo)
                if _isBlocked:
                    self.showMsg(MMD.datas.mutexSceneMsg, [str(_leftSec)])
                    continue
                return i_mapId, _m_records[i_mapId]

            # 其他情况-跳出循环走默认处理
            break

        return gameconst.MapIdDef.mapUnknown, None

    def packComplexTeleportLeaveData(self, leaveContext: dict, canLeaveFromLine=True, canLeaveFromGuild=True,
                                        canLeaveFromSingleDungeon=True, canLeaveFromTeamDungeon=True,
                                        canLeaveFromRaidDungeon=True,
                                        noErrorMsg=False, **options):
        LOG_DBG('packComplexTeleportLeaveData::', self.spaceNo, leaveContext)

        leaveFnName = self._spaceToComplexTeleportDefinedName(self.spaceNo)
        if not leaveFnName:
            not noErrorMsg and LOG_ERR('packComplexTeleportLeaveData:: leave from current space un-supported', self.spaceNo)
            return gameclass.ResultBool(False, gameconst.CompleteTeleportLeaveFailReason.UNDEFINED_FUNC)

        elif leaveFnName == 'worldLine':
            return gameclass.ResultBool(canLeaveFromLine, gameconst.CompleteTeleportLeaveFailReason.ARGS_DEFINED)

        elif leaveFnName == 'singleDungeon':
            leaveContext.update({
                'spaceUUID': self.spaceMgr.dungeonPlayMode.spaceUUID,
                'spaceMgrBox': self.spaceMgr.base, 
            })

            _judgeLeaveSrc = options.get('judgeLeaveSrc')
            if not (self.canNewbieLeaveCurDungeon() or\
                    (_judgeLeaveSrc and _judgeLeaveSrc.srcId in gameconst.DunSrcEnum.COLL_FROM_TASK)):
                return gameclass.ResultBool(False, gameconst.CompleteTeleportLeaveFailReason.PLAYER_IN_NEWBIEDUN)

            return gameclass.ResultBool(canLeaveFromSingleDungeon, gameconst.CompleteTeleportLeaveFailReason.ARGS_DEFINED)

        elif leaveFnName == 'raidDungeon':
            leaveContext.update({
                'spaceMgrBox': self.spaceMgr.base, 
                'extra': {},
            })
            return gameclass.ResultBool(canLeaveFromRaidDungeon, gameconst.CompleteTeleportLeaveFailReason.ARGS_DEFINED)

        elif leaveFnName == 'teamDungeon':
            leaveContext.update({
                'spaceMgrBox': self.spaceMgr.base,
            })
            return gameclass.ResultBool(canLeaveFromTeamDungeon, gameconst.CompleteTeleportLeaveFailReason.ARGS_DEFINED)

        elif leaveFnName == 'cube':
            leaveContext.update({'spaceMgrCell': self.spaceMgr})
            return gameclass.ResultBool(True, gameconst.CompleteTeleportLeaveFailReason.ARGS_DEFINED)

        elif leaveFnName == 'wonderLand':
            leaveContext.update({'spaceMgrCell': self.spaceMgr})
            return gameclass.ResultBool(True, gameconst.CompleteTeleportLeaveFailReason.ARGS_DEFINED)

        elif leaveFnName == 'siegeWar':
            leaveContext.update({'spaceMgrCell': self.spaceMgr})
            return gameclass.ResultBool(True, gameconst.CompleteTeleportLeaveFailReason.ARGS_DEFINED)

        elif leaveFnName == 'guildBossDungeon':
            leaveContext.update({'guildUUID': self.guildUUID, 'spaceMgrBox': self.spaceMgr.base, 'spaceMgrCell': self.spaceMgr})
            return gameclass.ResultBool(True, gameconst.CompleteTeleportLeaveFailReason.ARGS_DEFINED)
        elif leaveFnName == 'abyss':
            leaveContext.update({'spaceMgrCell': self.spaceMgr})
            return gameclass.ResultBool(True, gameconst.CompleteTeleportLeaveFailReason.ARGS_DEFINED)
        else:
            not noErrorMsg and LOG_ERR('packComplexTeleportLeaveData:: leave from current space unknown', self.spaceNo, leaveFnName)
            return gameclass.ResultBool(False, gameconst.CompleteTeleportLeaveFailReason.UNDEFINED_SPACE)

    def _fetchCommonLeavePosAndDir(self, spaceSpaceNo, toSpaceNo, options, context):
        if options.teleportType == gameconst.ComplexTeleportEnum.LEAVE:
            _m_outRecord = self.fetchTeleportOutesideRecord(toSpaceNo) # type: outsideRecord.OutsideRecord
            if _m_outRecord:
                m_pos, m_dir = _m_outRecord.position, _m_outRecord.direction
                m_spaceNo = toSpaceNo
                return m_pos, m_dir, m_spaceNo

        elif options.teleportType == gameconst.ComplexTeleportEnum.ENTER:
            if formula.inWorldLineScene(toSpaceNo):
                _m_outRecord = self.fetchTeleportOutesideRecord(toSpaceNo)
                if _m_outRecord:
                    m_pos, m_dir = _m_outRecord.position, _m_outRecord.direction
                    m_spaceNo = formula.combineLineSpaceNo(formula.parseLineType(toSpaceNo))
                    return m_pos, m_dir, m_spaceNo

        m_pos = formula.getSpaceBornPoint(toSpaceNo)
        m_dir = (0, 0, 0)
        if formula.inWorldLineScene(toSpaceNo):
            m_spaceNo = formula.combineLineSpaceNo(formula.parseLineType(toSpaceNo))
        else:
            m_spaceNo = toSpaceNo
        return m_pos, m_dir, m_spaceNo

    def doLeaveFromSapceToSpace(self, fromSpaceNo, toSpaceNo, options, context,
                                spaceType=0, noCheckGamePlayLeave=True):
        """统一离开场景方法

        Arguments:
            fromSpaceNo {SPACE_NO} -- 当前所处场景
            toSpaceNo {SPACE_NO} -- 到达场景
            options {complexTeleportOption.ComplexTeleportOpt} -- 传送选项
            context {PY_DICT} -- 传送上下文

        Keyword Arguments:
            spaceType {int} -- 指明当前spaceType, 大世界副本需要使用, 一般使用默认值即可 (default: {0})
            noCheckGamePlayLeave {bool} -- 强制玩家离开, 战场场景使用 (default: {True})
        """
        LOG_INFO("doLeaveFromSapceToSpace::", fromSpaceNo, toSpaceNo, options, context, spaceType, noCheckGamePlayLeave)
        lCtx, eCtx = context['l'], context['e']
        canLeave = self.packComplexTeleportLeaveData(lCtx, judgeLeaveSrc=context.get('src'))
        if not canLeave:
            LOG_ERR("doLeaveFromSapceToSpace:: can\'t package leave context", canLeave,
                      fromSpaceNo, toSpaceNo, options, context, spaceType, noCheckGamePlayLeave,)
            return

        _mMapId, _mOutsideRecord = self.tryGetLastTeleportOutesideRecord(fromSpaceNo, spaceType=spaceType)
        toSpaceNo = _mOutsideRecord.spaceNo if _mOutsideRecord else toSpaceNo
        LOG_DBG('     doLeaveFromSapceToSpace, _mOutsideRecord:', _mMapId, _mOutsideRecord)
        self.telFromSpaceToSpace(self.spaceNo, toSpaceNo, options=options, context=context)

    def canDoCompleteTeleport(self, **options):
        return self.packComplexTeleportLeaveData({}, **options)

    def tryDisableAutoCombatWhenLeaveSpace(self, dungeonNo):
        if self.autoCombat and self._getParamBydungeonNo(dungeonNo, 'leaveSceneDisableAutoFight'):
            self.stopAutoCombat(self.id)

    def enableAutoCombatAfterEnterSpace(self, dungeonNo):
        # if not self.autoCombat and GP_GPD.datas[dungeonNo].get('enterSceneAutoFight', 0):
        #     self._startAutoCombat()
        pass

    def tryRecoverHPAfterEnterSpace(self, gamePlayId):
        return GP_GPD.datas[gamePlayId].get('recover', gameconst.GameSpaceRecoverEnum.RCV_NO_ACTION) in gameconst.GameSpaceRecoverEnum.COLL_ENTER_RCV

    def tryRecoverHPAfterLeaveSpace(self, gamePlayId):
        if gameconfig.isCrossServer() and gamePlayId == 0:
            return 0
        return GP_GPD.datas[gamePlayId].get('recover', gameconst.GameSpaceRecoverEnum.RCV_NO_ACTION) in gameconst.GameSpaceRecoverEnum.COLL_LEAVE_RCV

    def __init__(self):
        pass

    @classmethod
    def regrAllComplexTeleportMethods(cls):
        gameglobal.complexTeleportTypeFnMap.clear()
        _data = cls.buildCompleteTeleportMethodDefines()
        gameglobal.complexTeleportTypeFnMap.clear()
        gameglobal.complexTeleportTypeFnMap.update(_data)

    @classmethod
    def buildCompleteTeleportMethodDefines(cls):
        """在此注册可传送方法, key为定义名称, val为自定义build方法,

        注: 自定方法需要遵循`_buildSTDComplexTeleportMethodDefine`方法定义
        """
        _definedNames = {
            'worldLine': '',        # 大世界分线
            'singleDungeon': '',    # 单人副本
            'teamDungeon': '',      # 小队副本
            'raidDungeon': '',      # 团队副本
            'cube': '',             # 魔方
            'wonderLand': '',       # 秘境峰
            'siegeWar': '',         # 城战
            'guildBossDungeon': '',         # 公会boss
            'abyss': '',             # 归墟
        }

        # ----------------------------------------------------------
        _data = {}
        for _definedName, definedCustomFn in _definedNames.items():
            _fn = getattr(cls, definedCustomFn, None)
            _fn = cls._buildSTDComplexTeleportMethodDefine if not _fn else _fn
            _data[_definedName] = _fn(_definedName)
        # ----------------------------------------------------------
        return _data

    @staticmethod
    def _buildSTDComplexTeleportMethodDefine(defName):
        _enum = gameconst.ComplexTeleportMethodTypeEnum
        return {
            _enum.beforeEnter: '_beforeEnter_{}'.format(defName),
            _enum.afterEnter: '_afterEnter_{}'.format(defName),
            _enum.beforeLeave: '_beforeLeave_{}'.format(defName),
            _enum.afterLeave: '_afterLeave_{}'.format(defName),
            _enum.postAfterEnter: '_postAfterEnter_{}'.format(defName),
            _enum.postAfterLeave: '_postAfterLeave_{}'.format(defName)
        }

    @staticmethod
    def _spaceToComplexTeleportDefinedName(spaceNo):
        if formula.inLineScene(spaceNo):
            return 'worldLine'
        elif formula.inSingleDungeonScene(spaceNo):
            return 'singleDungeon'
        elif formula.inTeamDungeonScene(spaceNo):
            return 'teamDungeon'
        elif formula.inRaidDungeonScene(spaceNo):
            return 'raidDungeon'
        elif formula.inCubeScene(spaceNo):
            return 'cube'
        elif formula.inWonderLandScene(spaceNo):
            return 'wonderLand'
        elif formula.inSiegeWarScene(spaceNo):
            return 'siegeWar'
        elif formula.inGuildBossDungeonScene(spaceNo):
            return 'guildBossDungeon'
        elif formula.inAbyssScene(spaceNo):
            return 'abyss'
        else:
            return ''

    def _getComplexTeleportSpaceMethods(self, spaceNo):
        if spaceNo == 0 and gameconfig.isCrossServer():
            return None
        definedName = self._spaceToComplexTeleportDefinedName(spaceNo)
        if not definedName:
            LOG_ERR('_getComplexTeleportSpaceMethods:: spaceNo not support', spaceNo)
            return None
        _complexTeleportTypeFnMap = self.complexTeleportTypeFnMap
        return {k: getattr(self, v, None) for k, v in _complexTeleportTypeFnMap[definedName].items()}

    def enterSpaceCommonNeedCast(self, callbackFn, callbackArgs, **kwargs):
        kwargs.setdefault("castTime", 3)
        return self._commonNeedCast(
            C_C_DD.datas.teleportCast,
            gameconst.StateEnum.Teleporting,
            gameconst.CastEnum.teleport,
            callbackFn, callbackArgs,
            **kwargs)

    def onTeleFromSpaceToSpaceFailed(self, fromSpaceNo, toSpaceNo, options, context):
        if formula.inCubeScene(toSpaceNo):
            gameengine.getCubeStubBySpaceNo(toSpaceNo).enterSpaceFailed(
                self.gbId,
                toSpaceNo,
            )

    def teleportFromSpaceToSpaceRpc(self, toSpaceNo,
                                 options=complexTeleportOption.ComplexTeleportOpt(),
                                 context=None):
        self.telFromSpaceToSpace(self.spaceNo, toSpaceNo, options, context)

    def telFromSpaceToSpace(self, fromSpaceNo, toSpaceNo,
                                 options=complexTeleportOption.ComplexTeleportOpt(),
                                 context=None, failedFunc='', failedArgs=None):
        assert context

        hasCheck = context.get('hasCheck', False) if context else False
        if not hasCheck and not utils.checkCanChangeSceneAndShowMsg(self, fromSpaceNo, toSpaceNo):
            LOG_ERR('telFromSpaceToSpace:: can\'t teleport', fromSpaceNo, toSpaceNo)
            return

        context['hasCheck'] = True
        lineNo = -1
        # NOTE(): 切换至大世界分线特殊情况处理，如果不确定切换分线，则不在这里断言
        if formula.inWorldLineScene(toSpaceNo):
            lineType = context['e'].get('lineType', -1)
            lineNo = context['e'].get('lineNo', -1)
            if lineNo >= 0 and lineType >= 0:
                toSpaceNo = formula.combineLineSpaceNo(lineType, lineNo)

        if fromSpaceNo == toSpaceNo:
            gameengine.panicStack('telFromSpaceToSpace:: {} == {}, can\'t teleport, lineNo={}', fromSpaceNo, toSpaceNo, lineNo)
            return

        LOG_INFO('telFromSpaceToSpace:: {} -> {}, context={}, options={}, lineNo={}'.format(
            fromSpaceNo, 
            toSpaceNo, 
            context, 
            options, 
            context['e'].get('lineNo', -1),
        ))

        src = context.get('src')

        # XXX(): [进入单人相关场景]传送读条最好在真正传送前做好, 防止传送失败造成了资源浪费(e.g. 副本不应该创建)
        # 已知单人场景:
        #   1. DONE: 单人副本
        if context.get('hasCast') \
                or not utils.checkComplexTeleportNeedCast(fromSpaceNo, toSpaceNo, options.teleportType, src, owner=self):
            self.telFromSpaceToSpaceContinue(fromSpaceNo, toSpaceNo, options, context)

        else:
            context['hasCast'] = True
            self.enterSpaceCommonNeedCast(
                "telFromSpaceToSpaceContinue",
                (fromSpaceNo, toSpaceNo, options, context),
                castTime=3, failedFunc=failedFunc, failedArgs=failedArgs)

    def telFromSpaceToSpaceContinue(self, fromSpaceNo, toSpaceNo,
                                 options=complexTeleportOption.ComplexTeleportOpt(),
                                 context=None):
        fromSpaceMethods = self._getComplexTeleportSpaceMethods(fromSpaceNo)
        toSpaceMethods = self._getComplexTeleportSpaceMethods(toSpaceNo)

        if not fromSpaceMethods or not toSpaceMethods:
            if not gameconfig.isCrossServer():
                LOG_ERR('telFromSpaceToSpaceContinue:: fromSpaceMethods or toSpaceMethods is None', fromSpaceNo, toSpaceNo)
                return

        _enum = gameconst.ComplexTeleportMethodTypeEnum
        beforeEnterMethod = toSpaceMethods[_enum.beforeEnter]
        beforeLeaveMethod = fromSpaceMethods[_enum.beforeLeave] if fromSpaceMethods else None

        _enterMethods = [beforeEnterMethod, beforeLeaveMethod]
        if options.beforeLeaveFirst:
            _enterMethods[0], _enterMethods[1] = _enterMethods[1], _enterMethods[0]

        _gotErr = False
        self._changeSpacSetRadius(fromSpaceNo, toSpaceNo, True)
        for fn in _enterMethods:
            if not fn:
                continue
            try:
                r = fn(fromSpaceNo, toSpaceNo, options, context)
            except:
                _gotErr = True
                gameengine.panicStack('telFromSpaceToSpace:: fn exception got')
            else:
                if not r:
                    # NOTE(): errorMSg由方法内部处理并报出
                    LOG_WARN('telFromSpaceToSpace:: pre-enter failed',
                                fromSpaceNo, toSpaceNo, options, context)
                    self.onTeleFromSpaceToSpaceFailed(fromSpaceNo, toSpaceNo, options, context)
                    return

        if _gotErr:
            return

        # overwrite toSpaceNo to context defined
        _orgToSpaceNo = toSpaceNo
        if context['spaceNo'] != toSpaceNo:
            LOG_WARN("telFromSpaceToSpaceContinue:: overwrite toSapceNo {} => {}".format(
                toSpaceNo, context['spaceNo']))
            toSpaceNo = context['spaceNo']

        LOG_INFO('telFromSpaceToSpaceContinue:: {} -> {} ==> {}, lineNo={}, options={}, context={}'.format(
            fromSpaceNo, _orgToSpaceNo, toSpaceNo, context['e'].get('lineNo', -1), options, context))

        _src = context.get('src')
        position, direction = context['position'], context['direction']

        cbFn = 'onTeleportFromSpaceToSpaceSucceed'
        _cbArgs = (fromSpaceNo, toSpaceNo, options, context)
        failCB = 'onTeleportFromSpaceToLineSpaceFail'

        if formula.inLineScene(toSpaceNo):
            lineType = formula.fetchMapId(toSpaceNo)
            lineNo = context['e'].get('lineNo', -1)
            # overwrite toSpaceNo
            toSpaceNo = formula.combineLineSpaceNo(lineType, lineNo=lineNo)
            _cbArgs = (fromSpaceNo, toSpaceNo, options, context)
            extra = {'callback': cbFn, 'callbackArgs': _cbArgs, 'failCallback': failCB}
            if 'hasCast' in context:
                extra['hasCast'] = context['hasCast']

            if sMath.distance2D(self.position, position) < 1:
                direction = self.direction

            fromLineType = formula.fetchMapId(fromSpaceNo)
            if fromLineType != lineType:
                extra['toLine'] = True # 如果从副本进入大世界只有走这里
                extra["telToMainCityWhenFull"] = True
                self.applyEnterLineInternal(lineType, lineNo, position, direction, extra)
            else:
                self.switchLineAndPosition(lineNo, position, src=_src, extra=extra)

        else:
            # NOTE(): 刺客取消濒死状态
            # self.cancelImmuneDeath()
            spaceBox = context['e']['spaceBox']
            self.teleportToCell(spaceBox.cell, toSpaceNo, position, direction, cbFn, _cbArgs)

    def _changeSpacSetRadius(self, fromSpaceNo, toSpaceNo, isBefore):
        if not self.hasWitness:
            return
        _srcAOI = gameconst.DEFAULT_AOI
        if fromSpaceNo != 0 or not gameconfig.isCrossServer():
            _srcAOI = GP_GPD.datas[formula.fetchMapId(fromSpaceNo)]['AOI']
        _dstAOI = GP_GPD.datas[formula.fetchMapId(toSpaceNo)]['AOI']
        if _dstAOI != 0 and _srcAOI == _dstAOI:
            return

        _srcAOI = _srcAOI if _srcAOI else gameconst.DEFAULT_AOI
        _dstAOI = _dstAOI if _dstAOI else gameconst.DEFAULT_AOI
        if isBefore and _dstAOI > _srcAOI:
            return
        elif (not isBefore) and _dstAOI < _srcAOI:
            return

        _curAOI = self.getViewRadius()
        if abs(_curAOI - _dstAOI) < 0.001:
            return

        LOG_DBG('will change AOI:', _curAOI, _dstAOI, isBefore)
        self.setViewRadius(_dstAOI, gameconst.DEFAULT_HYST)

    def onTeleportFromSpaceToSpaceSucceed(self, fromSpaceNo, toSpaceNo,
                                          options: complexTeleportOption.ComplexTeleportOpt,
                                          context=None):
        assert context

        LOG_INFO('onTeleportFromSpaceToSpaceSucceed:: {} -> {} ==> {}, lineNo={}, context={}, options={}'.format(
            fromSpaceNo, 
            toSpaceNo, 
            self.spaceNo, 
            context['e'].get('lineNo', -1), 
            context,
            options, 
        ))


        fromSpaceMethods = self._getComplexTeleportSpaceMethods(fromSpaceNo)
        toSpaceMethods = self._getComplexTeleportSpaceMethods(toSpaceNo)

        if not fromSpaceMethods or not toSpaceMethods:
            if not gameconfig.isCrossServer():
                LOG_ERR('telFromSpaceToSpaceContinue:: fromSpaceMethods or toSpaceMethods is None', fromSpaceNo, toSpaceNo)
                return

        _enum = gameconst.ComplexTeleportMethodTypeEnum
        afterEnterMethod = toSpaceMethods[_enum.afterEnter]
        afterLeaveMethod = fromSpaceMethods[_enum.afterLeave] if fromSpaceMethods else None
        postAfterEnterMethod = toSpaceMethods[_enum.postAfterEnter]
        postAfterLeaveMethod = fromSpaceMethods[_enum.postAfterLeave] if fromSpaceMethods else None


        _leaveMethods = [afterLeaveMethod, afterEnterMethod]
        _postLeaveMethods = [postAfterEnterMethod, postAfterLeaveMethod]
        if options.afterEnterFirst:
            _leaveMethods[0], _leaveMethods[1] = _leaveMethods[1], _leaveMethods[0]
            _postLeaveMethods[0], _postLeaveMethods[1] = _postLeaveMethods[1], _postLeaveMethods[0]

        _gotErr = False
        for fn in _leaveMethods:
            if not fn:
                continue
            try:
                fn(fromSpaceNo, toSpaceNo, options, context)
            except:
                _gotErr = True
                gameengine.panicStack('onTeleportFromSpaceToSpaceSucceed:: fn exception got')

        for postFn in _postLeaveMethods:
            if not postFn:
                continue

            try:
                postFn(fromSpaceNo, toSpaceNo, options, context)
            except:
                _gotErr = True
                gameengine.panicStack('onTeleportFromSpaceToSpaceSucceed:: postFn exception got')

        self._changeSpacSetRadius(fromSpaceNo, toSpaceNo, False)
        self._changeSpacRecycleMount(context.get('isFromEdge', False))

        _toGameMapId = formula.parseDungeonNoBySpaceNo(toSpaceNo)
        _fromGameMapId = formula.parseDungeonNoBySpaceNo(fromSpaceNo)
        if self.tryRecoverHPAfterEnterSpace(_toGameMapId) or self.tryRecoverHPAfterLeaveSpace(_fromGameMapId):
            self.modifyHP(self.fullHp, self.id, gameconst.SourceType.SrcTpTeleport, self.id)

        _callback = context.get('callback', None)
        callbackArgs = context.get('callbackArgs', None)
        if _callback:
            getattr(self, _callback)(*callbackArgs)

        if _gotErr:
            return

    def onTeleportFromSpaceToLineSpaceFail(self, checkCode, fromSpaceNo, toSpaceNo,
                                          options: complexTeleportOption.ComplexTeleportOpt,
                                          context=None):
        LOG_WARN("onTeleportFromSpaceToLineSpaceFail::", checkCode, fromSpaceNo, toSpaceNo, options, context)
        self.releaseTeleportLock(self.teleportLock)
    # ----------------------------------------------------------------------
    # RAID DUNGEON
    # ----------------------------------------------------------------------

    @gamedecorator.checkTeleportLock(gameconst.TeleportLockEnum.ENTER_DUNGEON)
    def _beforeEnter_raidDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeEnter_raidDungeon::~')
        dungeonNo = formula.parseDungeonNoBySpaceNo(toSpaceNo)

        self.tryRegiTeleportOutsideRecord(fromSpaceNo, options)

        # get dungeon position
        _position = self._getParamBydungeonNo(dungeonNo, 'entrance')
        if not _position:
            LOG_WARN('_beforeEnter_raidDungeon:: reset entrance position to self position', dungeonNo, toSpaceNo, self.position)
            _position = self.position

        _direction = self._getEntranceDirByDungeonNo(formula.fetchMapId(toSpaceNo))

        if _direction is not None:
            _direction = (0, 0, _direction * math.pi / 180)
        else:
            _direction = self.direction

        # set teleport lock
        self.aquireTeleportLock(gameconst.TeleportLockEnum.ENTER_DUNGEON)

        # completed context
        context['position'] = _position
        context['direction'] = _direction
        context['spaceNo'] = toSpaceNo
        return True

    def _afterEnter_raidDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterEnter_raidDungeon::~ ', context)
        dungeonNo = formula.parseDungeonNoBySpaceNo(toSpaceNo)
        spaceMgrBox = context['e']['spaceMgrBox']
        _extra = context['e']['extra']
        _src = context['src']

        # release lock
        self.releaseTeleportLock(gameconst.TeleportLockEnum.ENTER_DUNGEON)
        self.releaseGlobalTeleportLock('telsucc')
        # set props
        self.spaceMgrId = spaceMgrBox.id
        self.spaceMgr.onPlayerEnter(self.id)

        # 【【死亡复活】玩家在大世界内死亡后，通过点击个人资料-头像-驭灵殿按钮进入副本后需要复活玩家】
        # NOTE(): 进入副本前复活会导致hp同步不到客户端导致显示问题, 先放在后面
        if self.isDie():
            self._relive()
            self.modifyHP(self.getDefaultReliveHP(), self.id, gameconst.SourceType.SrcTpDefault, self.id)

        # callback base
        _extra['raidId'] = self.raidUUID
        _extra['totalNum'] = self.raidInfo.raidPlayerNum
        _extra['joinType'] = self.joinType
        
        if self.spaceMgr.dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.CHIEF:
            self.base.onEnterChiefDungeon(self.spaceMgr.dungeonPlayMode.spaceUUID, self.spaceNo, dungeonNo, spaceMgrBox, _extra)
        else:
            self.base.onEnterDungeon(self.spaceNo, spaceMgrBox, _extra)
        self._createRaidDungeonTrap(dungeonNo)

        # set dungeon timeout
        endTime = int(self.spaceMgr.dungeonPlayMode.getTEnd(dungeonNo))
        if endTime:
            self.client.changeDungeonRemainTime(self.spaceNo, endTime)

        # set autoCombat
        self.enableAutoCombatAfterEnterSpace(dungeonNo)
        # callback raidDungeonStub
        _extra = _extra or {}
        _extra.update({'src': _src, 'playerName': self.name})
        _dungeonStub = gameengine.getDungeonStubBySpaceNo(toSpaceNo)
        _dungeonStub.enterDungeonSpaceSuccess(toSpaceNo, self.base, self.gbId, self.raidUUID, _extra)
        return True

    def _beforeLeave_raidDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeLeave_raidDungeon::~')
        dungeonNo = formula.parseDungeonNoBySpaceNo(fromSpaceNo)
        _spaceMgr = self.spaceMgr
        if _spaceMgr:
            _spaceMgr.onLeaveWholeAureoleSpace(self.id)

        # stop auto combat
        self.tryDisableAutoCombatWhenLeaveSpace(dungeonNo)

        # remove dungeon buff
        self.removeBuffByTag(gameconst.BuffTag.TagDungeon)

        position, direction, spaceNo = self._fetchCommonLeavePosAndDir(fromSpaceNo, toSpaceNo, options, context)

        if options.teleportType == gameconst.ComplexTeleportEnum.LEAVE:
            self.tryUnRegiTeleportOutsideRecord(toSpaceNo)

        if formula.inLineScene(toSpaceNo) and not formula.inYanWuScene(toSpaceNo):
            self.clearTeleportOutsideRecord()

        # fix big world position
        bigWorldDungeonLeaveType = self._getParamBydungeonNo(dungeonNo, 'leave')
        dungeonSpaceType = self._getParamBydungeonNo(dungeonNo, 'type')
        if dungeonSpaceType and gameconst.DungeonTypeJudge.isBigWorldDungeon(dungeonSpaceType) \
                and not bigWorldDungeonLeaveType:
            leave = GP_GPD.datas[dungeonNo].get('leave', 0)
            if leave == 0:
                sceneRes = GP_GPD.datas[dungeonNo].get('sceneRes', '')
                if sceneRes:
                    defaultMapID = GPSSDD.datas[sceneRes]['defaultMapID']
                    position = self.position
                    direction = self.direction
                    spaceNo = defaultMapID

        context['direction'] = direction
        context['position'] = position
        context['spaceNo'] = spaceNo
        return True

    def _afterLeave_raidDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterLeave_raidDungeon::~ ', context)
        _spaceMgrBox = context['l']['spaceMgrBox']
        raidUUID = context['l']['raidUUID']
        
        self.base.onLeaveDungeon(self.spaceNo, fromSpaceNo)
        if _spaceMgrBox:
            _spaceMgrBox.cell.onPlayerLeave(self.gbId, self.id, self.base)
        self.spaceMgrId = 0

        self.selfStopAutoCombat('leave raid dungeon')

        # callback raidDungeonStub
        extraProps = {}
        extraProps['src'] = context['src']
        _dungeonStub = gameengine.getDungeonStubBySpaceNo(fromSpaceNo)
        _dungeonStub.leaveDungeonSpaceSucc(fromSpaceNo, self.base, self.gbId, raidUUID, extraProps)

        if self.isDie():
            self._relive()
            self.modifyHP(self.getDefaultReliveHP(), self.id, gameconst.SourceType.SrcTpDefault, self.id)

        return True

    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # SINGLE DUNGEON
    # ----------------------------------------------------------------------

    @gamedecorator.checkTeleportLock(gameconst.TeleportLockEnum.ENTER_DUNGEON)
    def _beforeEnter_singleDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_WARN('_beforeEnter_singleDungeon::~')
        extra = context['e']['extra']

        reg = False
        if formula._isInnerDemonSpace(fromSpaceNo):
            reg = True
        self.tryRegiTeleportOutsideRecord(fromSpaceNo, options, reg)

        dungeonNo = formula.parseDungeonNoBySpaceNo(toSpaceNo)
        dungeonSpaceType = self._getParamBydungeonNo(dungeonNo, 'type')
        dungeonEnterType = self._getParamBydungeonNo(dungeonNo, 'enterType')

        position = extra.get('position')
        if not position:
            if gameconst.DungeonTypeJudge.isNormalSingleDungeon(dungeonSpaceType, dungeonEnterType):
                # common dungeon un-support no entrance configs
                gameengine.panicStack('_beforeEnter_singleDungeon:: common dungeon entrance position not define', dungeonNo, toSpaceNo)
                return
            else:
                LOG_WARN('_beforeEnter_singleDungeon:: reset entrance position to self position', dungeonNo, toSpaceNo, self.position)
                position = self.position

        _direction = extra.get('direction')
        if not _direction:
            _direction = self._getEntranceDirByDungeonNo(formula.fetchMapId(toSpaceNo))
        if _direction is not None:
            _direction = (0, 0, _direction * math.pi / 180)
        else:
            _direction = self.direction

        # set teleport lock
        self.aquireTeleportLock(gameconst.TeleportLockEnum.ENTER_DUNGEON)

        context['position'] = position
        context['direction'] = _direction
        context['spaceNo'] = toSpaceNo
        return True

    def _afterEnter_singleDungeon(self, fromSpaceNo, toSpaceNo, options, ctx):
        LOG_INFO('_afterEnter_singleDungeon::~')
        spaceMgrBox = ctx['e']['spaceMgrBox']
        spaceMgrId = spaceMgrBox.id
        playerBox = ctx['e']['playerBox']
        playerGbId = ctx['e']['playerGbId']
        extra = ctx['e']['extra']
        teamUUID = ctx['e']['teamUUID']

        # release lock
        self.releaseTeleportLock(gameconst.TeleportLockEnum.ENTER_DUNGEON)
        self.releaseGlobalTeleportLock('telsucc')

        # create dungeon trap
        dungeonNo = formula.fetchMapId(toSpaceNo)
        self._createSingleDungeonTrap(dungeonNo)

        self.spaceMgrId = spaceMgrId
        spaceMgr = self.spaceMgr
        spaceMgr.onPlayerEnter(self.id)

        # 【【死亡复活】玩家在大世界内死亡后，通过点击个人资料-头像-驭灵殿按钮进入副本后需要复活玩家】
        # NOTE(): 进入副本前复活会导致hp同步不到客户端导致显示问题, 先放在后面
        if self.isDie():
            self._relive()
            self.modifyHP(self.getDefaultReliveHP(), self.id, gameconst.SourceType.SrcTpDefault, self.id)

        # send real end time to avatar self client
        endTime = int(spaceMgr.dungeonPlayMode.getTEnd(dungeonNo))
        if endTime:
            self.client.changeDungeonRemainTime(toSpaceNo, endTime)

        self.base.onEnterDungeon(toSpaceNo, spaceMgrBox, extra)

        self.enableAutoCombatAfterEnterSpace(dungeonNo)
        extra['spaceUUID'] = spaceMgr.dungeonPlayMode.spaceUUID
        gameengine.getDungeonStubBySpaceNo(toSpaceNo).enterDungeonSpaceSuccess(
            toSpaceNo, playerBox, playerGbId, teamUUID, extra)

        return True

    def _beforeLeave_singleDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeLeave_singleDungeon::~')
        overwrite = context['l'].get('overwrite')
        dungeonNo = formula.parseDungeonNoBySpaceNo(fromSpaceNo)
        _spaceMgr = self.spaceMgr
        if _spaceMgr:
            _spaceMgr.onLeaveWholeAureoleSpace(self.id)

        self.tryDisableAutoCombatWhenLeaveSpace(dungeonNo)

        self.removeBuffByTag(gameconst.BuffTag.TagDungeon)

        position, direction, spaceNo = self._fetchCommonLeavePosAndDir(fromSpaceNo, toSpaceNo, options, context)
        _m_outRecord = self.fetchTeleportOutesideRecord(toSpaceNo)
        if _m_outRecord and _m_outRecord.isDie:
            context['needRelive'] = False
            if not self.isDie():
                self.modifyHP(-self.hp, self.id, gameconst.SourceType.SrcTpDefault, self.id)
        else:
            if self.isDie():
                self._relive()
                self.modifyHP(self.getDefaultReliveHP(), self.id, gameconst.SourceType.SrcTpDefault, self.id)

        unReg = False
        if formula._isInnerDemonSpace(toSpaceNo):
            unReg = True
        if options.teleportType == gameconst.ComplexTeleportEnum.LEAVE or unReg:
            self.tryUnRegiTeleportOutsideRecord(toSpaceNo)

        if formula.inLineScene(toSpaceNo) and not formula.inYanWuScene(toSpaceNo):
            self.clearTeleportOutsideRecord()

        # fix big world position
        bigWorldDungeonLeaveType = self._getParamBydungeonNo(dungeonNo, 'leave')
        dungeonSpaceType = self._getParamBydungeonNo(dungeonNo, 'type')
        if dungeonSpaceType and gameconst.DungeonTypeJudge.isBigWorldDungeon(dungeonSpaceType) \
                and not bigWorldDungeonLeaveType:
            leave = GP_GPD.datas[dungeonNo].get('leave', 0)
            if leave == 0:
                sceneRes = GP_GPD.datas[dungeonNo].get('sceneRes', '')
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
            if 'direction' in overwrite:
                context['direction'] = overwrite['direction']
            if 'position' in overwrite:
                context['position'] = overwrite['position']
        return True

    def _afterLeave_singleDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterLeave_singleDungeon::~')
        _spaceMgrBox = context['l']['spaceMgrBox']
        dungeonNo = formula.parseDungeonNoBySpaceNo(fromSpaceNo)


        self.base.onLeaveDungeon(self.spaceNo, fromSpaceNo)
        if _spaceMgrBox:
            _spaceMgrBox.cell.onPlayerLeave(self.gbId, self.id, self.base)
        self.spaceMgrId = 0

        if formula.inDungeonScene(fromSpaceNo):
            gameengine\
                .getDungeonStubByDungeonNo(dungeonNo, gameconst.DungeonEnterTypeEnum.SINGLE)\
                .leaveDungeonSpaceSucc(
                    fromSpaceNo, 
                    self.base, 
                    self.gbId, 
                    self.teamId, 
                    {
                        'spaceUUID': context['l']['spaceUUID'],
                        'spaceNo': self.spaceNo,
                    })
        else:
            pass

        self.selfStopAutoCombat('leave single dungeon')

        return True

    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # TEAM DUNGEON
    # ----------------------------------------------------------------------

    @gamedecorator.checkTeleportLock(gameconst.TeleportLockEnum.ENTER_DUNGEON)
    def _beforeEnter_teamDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeEnter_teamDungeon::~ ', context)
        extra = context['e']['extra']

        self.tryRegiTeleportOutsideRecord(fromSpaceNo, options)

        dungeonNo = formula.parseDungeonNoBySpaceNo(toSpaceNo)
        position = extra.get("position") or self._getParamBydungeonNo(dungeonNo, 'entrance')
        dungeonSpaceType = self._getParamBydungeonNo(dungeonNo, 'type')
        dungeonEnterType = self._getParamBydungeonNo(dungeonNo, 'enterType')
        if not position:
            if gameconst.DungeonTypeJudge.isNormalTeamDungeon(dungeonSpaceType, dungeonEnterType):
                # common dungeon un-support no entrance configs
                gameengine.panicStack('_beforeEnter_teamDungeon:: common dungeon entrance position not define', dungeonNo, toSpaceNo)
                return
            else:
                LOG_WARN('_beforeEnter_teamDungeon:: reset entrance position to self position', dungeonNo, toSpaceNo, self.position)
                position = self.position

        _direction = extra.get("direction") or self._getEntranceDirByDungeonNo(formula.fetchMapId(toSpaceNo))
        if _direction is not None:
            _direction = (0, 0, _direction * math.pi / 180)

        # set teleport lock
        self.aquireTeleportLock(gameconst.TeleportLockEnum.ENTER_DUNGEON)

        context['direction'] = _direction
        context['position'] = position
        context['spaceNo'] = toSpaceNo
        return True

    def _afterEnter_teamDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterEnter_teamDungeon::~ ', context)
        spaceMgrBox = context['e']['spaceMgrBox']
        dungeonNo = formula.parseDungeonNoBySpaceNo(toSpaceNo)
        extra = context['e']['extra']

        # release lock
        self.releaseTeleportLock(gameconst.TeleportLockEnum.ENTER_DUNGEON)
        self.releaseGlobalTeleportLock('telsucc')

        # create dungeon trap
        self._doCreateTeamDungeonTrap(dungeonNo)

        self.spaceMgrId = spaceMgrBox.id
        self.spaceMgr.onPlayerEnter(self.id)

        # 【【死亡复活】玩家在大世界内死亡后，通过点击个人资料-头像-驭灵殿按钮进入副本后需要复活玩家】
        # NOTE(): 进入副本前复活会导致hp同步不到客户端导致显示问题, 先放在后面
        if self.isDie():
            self._relive()
            self.modifyHP(self.getDefaultReliveHP(), self.id, gameconst.SourceType.SrcTpDefault, self.id)

        # send real end time to avatar self client
        endTime = int(self.spaceMgr.dungeonPlayMode.getTEnd(dungeonNo))
        if endTime:
            self.client.changeDungeonRemainTime(toSpaceNo, endTime)

        if self.spaceMgr.dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            _kwargs = dict(
                GameSvrId=None, dtEventTime=None, vGameAppid=None,
                iBattleID=dungeonNo,
                iTeamID=self.teamId,
                TeamUserNum=self.teamInfo.howManyMember(),
            )
            extra['tlogProps'] = _kwargs
            extra['actId'] = gameconst.ACT_ID_CONST.ACTIVITY_CRUSADE_ID
            extra['teamUUID'] = self.teamId
            extra['totalNum'] = self.teamInfo.howManyMember()
            extra['joinType'] = self.joinType
            self.base.onEnterCrusadeDungeon(self.spaceMgr.dungeonPlayMode.spaceUUID, toSpaceNo, dungeonNo, spaceMgrBox, extra)
        else:
            self.base.onEnterDungeon(toSpaceNo, spaceMgrBox, extra)

        self.enableAutoCombatAfterEnterSpace(dungeonNo)

        gameengine.getTeamStub(self.teamId).onEnterTeamDungeon(self.base, self.gbId, self.teamId, dungeonNo, toSpaceNo)
        return True

    def _beforeLeave_teamDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeLeave_teamDungeon::~')
        dungeonNo = formula.parseDungeonNoBySpaceNo(fromSpaceNo)
        spaceMgr = self.spaceMgr
        if spaceMgr:
            spaceMgr.onLeaveWholeAureoleSpace(self.id)

        dungeonSpaceType = self._getParamBydungeonNo(dungeonNo, 'type')
        dungeonEnterType = self._getParamBydungeonNo(dungeonNo, 'enterType')
        if not gameconst.DungeonTypeJudge.isTeamDungeon(dungeonSpaceType, dungeonEnterType):
            LOG_ERR('error dungeonType: {}/{}'.format(dungeonNo, dungeonSpaceType))
            return

        self.tryDisableAutoCombatWhenLeaveSpace(dungeonNo)

        self.removeBuffByTag(gameconst.BuffTag.TagDungeon)

        position, direction, spaceNo = self._fetchCommonLeavePosAndDir(fromSpaceNo, toSpaceNo, options, context)
        _m_outRecord = self.fetchTeleportOutesideRecord(toSpaceNo)
        if _m_outRecord and _m_outRecord.isDie:
            context['needRelive'] = False
            if not self.isDie():
                self.modifyHP(-self.hp, self.id, gameconst.SourceType.SrcTpDefault, self.id)
        else:
            if self.isDie():
                self._relive()
                self.modifyHP(self.getDefaultReliveHP(), self.id, gameconst.SourceType.SrcTpDefault, self.id)

        # dungeonPlayMode = spaceMgr.dungeonPlayMode.playMode if spaceMgr else gameconst.DungeonPlayModeEnum.UNKNOWN

        bigWorldDungeonLeaveType = self._getParamBydungeonNo(dungeonNo, 'leave')
        dungeonSpaceType = self._getParamBydungeonNo(dungeonNo, 'type')
        if dungeonSpaceType and gameconst.DungeonTypeJudge.isBigWorldDungeon(dungeonSpaceType) \
                and not bigWorldDungeonLeaveType:
            leave = GP_GPD.datas[dungeonNo].get('leave', 0)
            if leave == 0:
                sceneRes = GP_GPD.datas[dungeonNo].get('sceneRes', '')
                if sceneRes:
                    defaultMapID = GPSSDD.datas[sceneRes]['defaultMapID']
                    position = self.position
                    direction = self.direction
                    spaceNo = defaultMapID

        if options.teleportType == gameconst.ComplexTeleportEnum.LEAVE:
            self.tryUnRegiTeleportOutsideRecord(toSpaceNo)

        if formula.inLineScene(toSpaceNo) and not formula.inYanWuScene(toSpaceNo):
            self.clearTeleportOutsideRecord()

        context['direction'] = direction
        context['position'] = position
        context['spaceNo'] = spaceNo
        return True

    def _afterLeave_teamDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterLeave_teamDungeon::~ ', context)
        _spaceMgrBox = context['l']['spaceMgrBox']
        teamUUID = context['l']['teamUUID']
        
        self.base.onLeaveDungeon(self.spaceNo, fromSpaceNo)
        if _spaceMgrBox:
            _spaceMgrBox.cell.onPlayerLeave(self.gbId, self.id, self.base)
        self.spaceMgrId = 0

        self.selfStopAutoCombat('leave team dungeon')

        # callback teamDungeonStub
        extraProps = {}
        extraProps['src'] = context['src']
        _dungeonStub = gameengine.getDungeonStubBySpaceNo(fromSpaceNo)
        _dungeonStub.leaveDungeonSpaceSucc(fromSpaceNo, self.base, self.gbId, teamUUID, extraProps)

        return True

    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # WORLD LINE
    # ----------------------------------------------------------------------

    def _beforeEnter_worldLine(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeEnter_worldLine::~')
        context.setdefault('direction', self.direction)
        context.setdefault('position', self.position)
        context.setdefault('spaceNo', toSpaceNo)

        if formula.fetchMapId(fromSpaceNo) == formula.fetchMapId(toSpaceNo):
            r = self.aquireTeleportLock(gameconst.TeleportLockEnum.SWITCH_LINE)
        else:
            r = self.aquireTeleportLock(gameconst.TeleportLockEnum.ENTER_LINE)
        if not r:
            LOG_ERR("_beforeEnter_worldLine:: aquire teleportlock failed", self.teleportLock, self.teleportLockRlsT)
            return r

        _overwrite = context['e'].get('overwrite')
        if _overwrite:
            if 'position' in _overwrite:
                context['position'] = _overwrite['position']
            if 'direction' in _overwrite:
                context['direction'] = _overwrite['direction']
            if 'spaceNo' in _overwrite:
                context['spaceNo'] = _overwrite['spaceNo']

        return True

    def _afterEnter_worldLine(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterEnter_worldLine::~')

        self.releaseTeleportLock(gameconst.TeleportLockEnum.ENTER_LINE)
        self.releaseGlobalTeleportLock('telsucc')

        self.resetStatisticsData()
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed

        # 【【任务】离开场景关闭自动战斗对gamePlay全部生效】
        self.enableAutoCombatAfterEnterSpace(formula.parseDungeonNoBySpaceNo(toSpaceNo))

        if formula.inLineScene(toSpaceNo) and not formula.inYanWuScene(toSpaceNo):
            # clear all records
            self.clearTeleportOutsideRecord()
        if context.get('needRelive', True):
            self._onEnterLineRelive()
        return True

    def _beforeLeave_worldLine(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeLeave_worldLine::~')

        # 【【任务】离开场景关闭自动战斗对gamePlay全部生效】
        self.tryDisableAutoCombatWhenLeaveSpace(formula.parseDungeonNoBySpaceNo(fromSpaceNo))
        if not formula.inLineScene(toSpaceNo):
            self._applyLeaveLineInternal(fromSpaceNo, 0, gameconst.POSITION_ZERO, gameconst.DIRECTION_ZERO)

        context['spaceMgrCell'] = self.spaceMgr

        return True

    def _afterLeave_worldLine(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterLeave_worldLine::~', fromSpaceNo, toSpaceNo)
        context['spaceMgrCell'].onPlayerLeave(self.gbId, self.id, self.base)
        self.spaceMgrId = 0

        return True

    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # cube
    # ----------------------------------------------------------------------

    @gamedecorator.checkTeleportLock(gameconst.TeleportLockEnum.ENTER_CUBE)
    def _beforeEnter_cube(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeEnter_cube::~')
        self.aquireTeleportLock(gameconst.TeleportLockEnum.ENTER_CUBE)
        self.tryRegiTeleportOutsideRecord(fromSpaceNo, options)

        _extra = context['cube']
        _dir = self._getEntranceDirByDungeonNo(formula.fetchMapId(toSpaceNo))
        if _extra.get('followPos'):
            context['position'] = _extra['followPos']
        else:
            context['position'] = self._getEntranceByDungeonNo(formula.fetchMapId(toSpaceNo))

        if _extra.get('isMerge'):
            if _extra.get('oriPos'):
                context['position'] = _extra['oriPos']

        context['direction'] = (0, 0, _dir * math.pi / 180) if _dir is not None else self.direction
        context['spaceNo'] = toSpaceNo
        return True

    def _afterEnter_cube(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterEnter_cube::~')
        self.releaseTeleportLock(gameconst.TeleportLockEnum.ENTER_CUBE)
        self.spaceMgrId = context['e']['spaceMgrId']
        self.spaceMgr.onPlayerEnter(self.id)

        gameengine.getCubeStubBySpaceNo(toSpaceNo).onEnterCubeSuccess(self.gbId, toSpaceNo)

        _extra = context['cube']
        _type = _extra.get('enterCubeType')
        floor = _extra.get('floor', 0)

        if _extra.get('isMerge'):
            if _extra.get('isAutoFight'):
                self._startAutoCombat()

        if _type == gameconst.ENTER_CUBE_DEDUCT_TIMES:
            _dur = cube_config.datas['cubeNumTime']['value'] * 60
            self.cubeQuota.addCubeLeftTime(self, _dur)
            self.base.afterEnterCubeDeductTimes({'floor': floor})
            self.base.activityComplete(cube_config.datas['cubeActID']['value'])
        elif _type == gameconst.ENTER_CUBE_HAS_LEFT_TIME and floor:
            LogTrackingMgr.LogTrackingMgr.cube_enter(
                self.gbId,
                self.clientDistinctIdCell,
                floor,
                utils.curTS(),
                0,
                0,
            )

        if not formula.inCubeScene(fromSpaceNo):
            self.base.completeGuildTask(gameconst.GuildTaskType.ENTERMAP, cube_config.datas['cubeActID']['value'], 1)

        self._dealWithCubeKickTimer(fromSpaceNo, toSpaceNo)
        self._dealWithCubeTimer(fromSpaceNo, toSpaceNo)

        _toMapId = formula.fetchMapId(toSpaceNo)
        if dataUtils.isCubeCow(_toMapId):
            _fromMapId = formula.fetchMapId(fromSpaceNo)
            self.fromCubeMapId = _fromMapId

            _floor = cube_room.datas[_toMapId]['floor']
            _buffId = cube_floor.datas[_floor]['cowPassBuffID']
            # 这个buffID会在切换场景时候自动删除
            self.addBuff(_buffId, 1, self.id)

        _floor = cube_room.datas[_toMapId]['floor']
        LogTrackingMgr.LogTrackingMgr.Cube_Info(
            self.gbId,
            self.clientDistinctIdCell,
            self.gbId,
            gameconfig.gameId(),
            _floor,
            _toMapId,
            gameconst.CUBE_EVENT_ENTER,
            self.cubeQuota.calcLeftTime()
        )

        return True

    def _beforeLeave_cube(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeLeave_cube::~')
        position, direction, spaceNo = self._fetchCommonLeavePosAndDir(fromSpaceNo, toSpaceNo, options, context)

        if options.teleportType == gameconst.ComplexTeleportEnum.LEAVE:
            self.tryUnRegiTeleportOutsideRecord(toSpaceNo)

        if formula.inLineScene(toSpaceNo) and not formula.inYanWuScene(toSpaceNo):
            self.clearTeleportOutsideRecord()

        context['position'] = position
        context['direction'] = direction
        context['spaceNo'] = spaceNo

        return True

    def _afterLeave_cube(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterLeave_cube::~')
        _spaceMgrCell = context['l']['spaceMgrCell']
        _spaceMgrCell.onPlayerLeave(self.gbId, self.id, self.base)

        self.spaceMgrId = 0
        gameengine.getCubeStubBySpaceNo(fromSpaceNo).onLeaveCube(self.gbId, fromSpaceNo, toSpaceNo)
        if not formula.inCubeScene(toSpaceNo):
            if self.getTempMiscProp(gameconst.EntityPropsEnum.cubeAutoRenewSwitch) is not None:
                self._changeCubeAutoRenewSwitch(False, {})

            self.clearCubeRoomRewardRecord()

        if not formula.inCubeScene(toSpaceNo):
            self._dealWithCubeKickTimer(fromSpaceNo, toSpaceNo)
            self._dealWithCubeTimer(fromSpaceNo, toSpaceNo)

        if formula._isArenaSpace(fromSpaceNo):
            preCubePKModel = self.popPersistentMiscProp(gameconst.EntityPropsEnum.preCubePKModel, None)
            if preCubePKModel != None:
                self.onSwitchPKModel(preCubePKModel)

        _fromMapId = formula.fetchMapId(fromSpaceNo)
        _floor = cube_room.datas[_fromMapId]['floor']
        LogTrackingMgr.LogTrackingMgr.Cube_Info(
            self.gbId,
            self.clientDistinctIdCell,
            self.gbId,
            gameconfig.gameId(),
            _floor,
            _fromMapId,
            gameconst.CUBE_EVENT_EXIT,
            self.cubeQuota.calcLeftTime(),
        )
        _src = context['src']
        if _src.srcId:
            LogTrackingMgr.LogTrackingMgr.cube_leave(
                self.gbId,
                self.clientDistinctIdCell,
                utils.curTS(),
                _src.srcId,
            )
        return True
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # wonderland
    # ----------------------------------------------------------------------

    @gamedecorator.checkTeleportLock(gameconst.TeleportLockEnum.ENTER_WONDERLAND)
    def _beforeEnter_wonderLand(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeEnter_wonderland::~')
        self.aquireTeleportLock(gameconst.TeleportLockEnum.ENTER_WONDERLAND)

        self.tryRegiTeleportOutsideRecord(fromSpaceNo, options)

        _dir = self._getEntranceDirByDungeonNo(formula.fetchMapId(toSpaceNo))
        context['position'] = self._getEntranceByDungeonNo(formula.fetchMapId(toSpaceNo))
        context['direction'] = (0, 0, _dir * math.pi / 180) if _dir is not None else self.direction
        context['spaceNo'] = toSpaceNo
        
        _extra = context.get('wonderlandExtra')
        if _extra.get('isMerge'):
            if _extra.get('oriPos'):
                context['position'] = _extra['oriPos']
        return True

    def _afterEnter_wonderLand(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterEnter_wonderland::~')
        self.releaseTeleportLock(gameconst.TeleportLockEnum.ENTER_WONDERLAND)
        self.spaceMgrId = context['e']['spaceMgrId']
        self.spaceMgr.onPlayerEnter(self.id)

        gameengine.getWonderLandStubBySpaceNo(toSpaceNo).onEnterWonderLandSuccess(self.gbId, toSpaceNo)

        _extra = context.get('wonderlandExtra')
        if _extra.get('isMerge'):
            if _extra.get('isAutoFight'):
                self._startAutoCombat()

        enterType = context.get('enterType')
        floor = context.get('floor', 0)
        if enterType == gameconst.WONDER_LAND_ENTER_TYPE_TICKET:
            self.wonderLandQuota.addWonderLandLeftTime(self, WL_CD.datas['wonderLandNumTime']['value'] * 60)
            self.base.afterEnterWonderLandDeductTimes({'floor': floor})
            self.base.activityComplete(WL_CD.datas['wonderLandActID']['value'])
        elif enterType == gameconst.WONDER_LAND_ENTER_TYPE_LEFT_TIME and floor:
            LogTrackingMgr.LogTrackingMgr.wonderland_enter(
                self.gbId,
                self.clientDistinctIdCell,
                floor,
                utils.curTS(),
                0,
                0,
            )

        self.base.completeGuildTask(gameconst.GuildTaskType.ENTERMAP, WL_CD.datas['wonderLandActID']['value'], 1)
        self._dealWithWonderLandTimer(fromSpaceNo, toSpaceNo)

        _mapId = formula.fetchMapId(toSpaceNo)
        LogTrackingMgr.LogTrackingMgr.Wonderland_Info(
            self.gbId,
            self.clientDistinctIdCell,
            self.gbId,
            gameconfig.gameId(),
            WL_FD.id2floor[_mapId],
            gameconst.WONDER_LAND_EVENT_ENTER,
            self.wonderLandQuota.calcLeftTime(),
        )
        return True

    def _beforeLeave_wonderLand(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeLeave_wonderland::~')
        position, direction, spaceNo = self._fetchCommonLeavePosAndDir(fromSpaceNo, toSpaceNo, options, context)

        if options.teleportType == gameconst.ComplexTeleportEnum.LEAVE:
            self.tryUnRegiTeleportOutsideRecord(toSpaceNo)

        if formula.inLineScene(toSpaceNo) and not formula.inYanWuScene(toSpaceNo):
            self.clearTeleportOutsideRecord()

        context['position'] = position
        context['direction'] = direction
        context['spaceNo'] = spaceNo

        return True

    def _afterLeave_wonderLand(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterLeave_wonderland::~')
        _spaceMgrCell = context['l']['spaceMgrCell']
        _spaceMgrCell.onPlayerLeave(self.gbId, self.id, self.base)

        self.spaceMgrId = 0
        gameengine.getWonderLandStubBySpaceNo(fromSpaceNo).onLeaveWonderLandWithToSpaceNo(self.gbId, toSpaceNo)
        self.afterLeaveWonderLand()

        if not formula.inWonderLandScene(toSpaceNo):
            self._dealWithWonderLandTimer(fromSpaceNo, toSpaceNo)

        _mapId = formula.fetchMapId(fromSpaceNo)

        LogTrackingMgr.LogTrackingMgr.Wonderland_Info(
            self.gbId,
            self.clientDistinctIdCell,
            self.gbId,
            gameconfig.gameId(),
            WL_FD.id2floor[_mapId],
            gameconst.WONDER_LAND_EVENT_EXIT,
            self.wonderLandQuota.calcLeftTime(),
        )
        _src = context['src']
        if _src.srcId:
            LogTrackingMgr.LogTrackingMgr.wonderland_leave(
                self.gbId,
                self.clientDistinctIdCell,
                utils.curTS(),
                _src.srcId,
            )
        return True
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # abyss
    # ----------------------------------------------------------------------

    @gamedecorator.checkTeleportLock(gameconst.TeleportLockEnum.ENTER_ABYSS)
    def _beforeEnter_abyss(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeEnter_abyss::~')
        self.aquireTeleportLock(gameconst.TeleportLockEnum.ENTER_ABYSS)

        self.tryRegiTeleportOutsideRecord(fromSpaceNo, options)

        _dir = self._getEntranceDirByDungeonNo(formula.fetchMapId(toSpaceNo))
        context['position'] = self._getEntranceByDungeonNo(formula.fetchMapId(toSpaceNo))
        context['direction'] = (0, 0, _dir * math.pi / 180) if _dir is not None else self.direction
        context['spaceNo'] = toSpaceNo
        
        _extra = context.get('abyssExtra')
        if _extra.get('isMerge'):
            if _extra.get('oriPos'):
                context['position'] = _extra['oriPos']
        return True

    def _afterEnter_abyss(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterEnter_abyss::~')
        self.releaseTeleportLock(gameconst.TeleportLockEnum.ENTER_ABYSS)
        self.spaceMgrId = context['e']['spaceMgrId']
        self.spaceMgr.onPlayerEnter(self.id)

        gameengine.getAbyssStubBySpaceNo(toSpaceNo).onEnterAbyssSuccess(self.gbId, toSpaceNo)

        _extra = context.get('abyssExtra')
        if _extra.get('isMerge'):
            if _extra.get('isAutoFight'):
                self._startAutoCombat()

        self.base.completeGuildTask(gameconst.GuildTaskType.ENTERMAP, AB_CD.datas['abyssActID']['value'], 1)
        self._dealWithAbyssTimer(fromSpaceNo, toSpaceNo)

        _mapId = formula.fetchMapId(toSpaceNo)
        return True

    def _beforeLeave_abyss(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeLeave_abyss::~')
        position, direction, spaceNo = self._fetchCommonLeavePosAndDir(fromSpaceNo, toSpaceNo, options, context)

        if options.teleportType == gameconst.ComplexTeleportEnum.LEAVE:
            self.tryUnRegiTeleportOutsideRecord(toSpaceNo)

        if formula.inLineScene(toSpaceNo) and not formula.inYanWuScene(toSpaceNo):
            self.clearTeleportOutsideRecord()

        context['position'] = position
        context['direction'] = direction
        context['spaceNo'] = spaceNo

        return True

    def _afterLeave_abyss(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterLeave_abyss::~')
        _spaceMgrCell = context['l']['spaceMgrCell']
        _spaceMgrCell.onPlayerLeave(self.gbId, self.id, self.base)

        self.spaceMgrId = 0
        gameengine.getAbyssStubBySpaceNo(fromSpaceNo).onLeaveAbyssWithToSpaceNo(self.gbId, toSpaceNo)
        self.afterLeaveAbyss()

        if not formula.inAbyssScene(toSpaceNo):
            self._dealWithAbyssTimer(fromSpaceNo, toSpaceNo)

        _mapId = formula.fetchMapId(fromSpaceNo)

        LogTrackingMgr.LogTrackingMgr.abyss_leave(
            self.gbId,
            self.clientDistinctIdCell,
            utils.curTS()
        )
        return True
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # siegeWar
    # ----------------------------------------------------------------------

    def _beforeEnter_siegeWar(self, fromSpaceNo, toSpaceNo, options, context):
        self.tryRegiTeleportOutsideRecord(fromSpaceNo, options)
        camp = self.siegeWarCamp

        _dir = self._getEntranceDirByDungeonNo(formula.fetchMapId(toSpaceNo))


        dunSData = utils.getDunStructModData(formula.fetchMapId(toSpaceNo))
        if camp == 1:
            d, *_ = dunSData['attackRevive'].values()
        elif camp == 2:
            d, *_ = dunSData['defendRevive'].values()

        context['position'] = (d['PosX'], d['PosY'], d['PosZ'])
        context['direction'] = (0, 0, _dir * math.pi / 180) if _dir is not None else self.direction
        context['spaceNo'] = toSpaceNo
        return True

    def _afterEnter_siegeWar(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterEnter_siegeWar::~')
        self.spaceMgrId = context['e']['spaceMgrId']
        self.spaceMgr.onPlayerEnter(self.id)
        return True

    def _beforeLeave_siegeWar(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeLeave_siegeWar::~')
        position, direction, spaceNo = self._fetchCommonLeavePosAndDir(fromSpaceNo, toSpaceNo, options, context)

        if options.teleportType == gameconst.ComplexTeleportEnum.LEAVE:
            self.tryUnRegiTeleportOutsideRecord(toSpaceNo)

        if formula.inLineScene(toSpaceNo) and not formula.inYanWuScene(toSpaceNo):
            self.clearTeleportOutsideRecord()

        context['position'] = position
        context['direction'] = direction
        context['spaceNo'] = spaceNo

        return True

    def _afterLeave_siegeWar(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterLeave_siegeWar::~')
        _spaceMgrCell = context['l']['spaceMgrCell']
        _spaceMgrCell.onPlayerLeave(self.gbId, self.id, self.base)

        self.spaceMgrId = 0
        return True

    # ----------------------------------------------------------------------
    # Guild Boss DUNGEON
    # ----------------------------------------------------------------------

    @gamedecorator.checkTeleportLock(gameconst.TeleportLockEnum.ENTER_DUNGEON)
    def _beforeEnter_guildBossDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeEnter_guildBossDungeon::~')
        extra = context['e']['extra']

        self.tryRegiTeleportOutsideRecord(fromSpaceNo, options)

        dungeonNo = formula.parseDungeonNoBySpaceNo(toSpaceNo)
        position = extra.get("position") or self._getParamBydungeonNo(dungeonNo, 'entrance')
        dungeonSpaceType = self._getParamBydungeonNo(dungeonNo, 'type')
        dungeonEnterType = self._getParamBydungeonNo(dungeonNo, 'enterType')
        if not position:
            if gameconst.DungeonTypeJudge.isNormalTeamDungeon(dungeonSpaceType, dungeonEnterType):
                # common dungeon un-support no entrance configs
                gameengine.panicStack('_beforeEnter_guildBossDungeon:: common dungeon entrance position not define', dungeonNo, toSpaceNo)
                return
            else:
                LOG_WARN('_beforeEnter_guildBossDungeon:: reset entrance position to self position', dungeonNo, toSpaceNo, self.position)
                position = self.position

        direction = extra.get("direction") or self._getEntranceDirByDungeonNo(formula.fetchMapId(toSpaceNo))
        if direction is not None:
            direction = (0, 0, direction * math.pi / 180)

        # set teleport lock
        self.aquireTeleportLock(gameconst.TeleportLockEnum.ENTER_DUNGEON)

        context['position'] = position
        context['direction'] = direction
        context['spaceNo'] = toSpaceNo
        return True

    def _afterEnter_guildBossDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterEnter_guildBossDungeon::~')
        spaceMgrBox = context['e']['spaceMgrBox']
        dungeonNo = formula.parseDungeonNoBySpaceNo(toSpaceNo)
        guildUUID = context['e']['guildUUID']
        extra = context['e']['extra']

        # release lock
        self.releaseTeleportLock(gameconst.TeleportLockEnum.ENTER_DUNGEON)
        self.releaseGlobalTeleportLock('telsucc')


        self.spaceMgrId = spaceMgrBox.id
        self.spaceMgr.onPlayerEnter(self.id)

        # 【【死亡复活】玩家在大世界内死亡后，通过点击个人资料-头像-驭灵殿按钮进入副本后需要复活玩家】
        # NOTE(): 进入副本前复活会导致hp同步不到客户端导致显示问题, 先放在后面
        if self.isDie():
            self._relive()
            self.modifyHP(self.getDefaultReliveHP(), self.id, gameconst.SourceType.SrcTpDefault, self.id)

        # send real end time to avatar self client
        endTime = int(self.spaceMgr.dungeonPlayMode.getTEnd(dungeonNo))
        if endTime:
            self.client.changeDungeonRemainTime(toSpaceNo, endTime)

        dungeonStub = gameengine.getDungeonStubBySpaceNo(toSpaceNo)
        dungeonStub.enterDungeonSpaceSuccess(toSpaceNo, self.base, self.gbId, guildUUID, extra)
        return True

    def _beforeLeave_guildBossDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_beforeLeave_guildBossDungeon::~')
        dungeonNo = formula.parseDungeonNoBySpaceNo(fromSpaceNo)
        spaceMgr = self.spaceMgr
        if spaceMgr:
            spaceMgr.onLeaveWholeAureoleSpace(self.id)

        dungeonSpaceType = self._getParamBydungeonNo(dungeonNo, 'type')
        dungeonEnterType = self._getParamBydungeonNo(dungeonNo, 'enterType')
        if not gameconst.DungeonTypeJudge.isGuildBossDungeon(dungeonSpaceType, dungeonEnterType):
            LOG_ERR('error dungeonType: {}/{}'.format(dungeonNo, dungeonSpaceType))
            return

        self.tryDisableAutoCombatWhenLeaveSpace(dungeonNo)

        self.removeBuffByTag(gameconst.BuffTag.TagDungeon)

        position, direction, spaceNo = self._fetchCommonLeavePosAndDir(fromSpaceNo, toSpaceNo, options, context)
        _m_outRecord = self.fetchTeleportOutesideRecord(toSpaceNo)
        if _m_outRecord and _m_outRecord.isDie:
            context['needRelive'] = False
            if not self.isDie():
                self.modifyHP(-self.hp, self.id, gameconst.SourceType.SrcTpDefault, self.id)
        else:
            if self.isDie():
                self._relive()
                self.modifyHP(self.getDefaultReliveHP(), self.id, gameconst.SourceType.SrcTpDefault, self.id)

        bigWorldDungeonLeaveType = self._getParamBydungeonNo(dungeonNo, 'leave')
        dungeonSpaceType = self._getParamBydungeonNo(dungeonNo, 'type')
        if dungeonSpaceType and gameconst.DungeonTypeJudge.isBigWorldDungeon(dungeonSpaceType) \
                and not bigWorldDungeonLeaveType:
            leave = GP_GPD.datas[dungeonNo].get('leave', 0)
            if leave == 0:
                sceneRes = GP_GPD.datas[dungeonNo].get('sceneRes', '')
                if sceneRes:
                    defaultMapID = GPSSDD.datas[sceneRes]['defaultMapID']
                    position = self.position
                    direction = self.direction
                    spaceNo = defaultMapID

        if options.teleportType == gameconst.ComplexTeleportEnum.LEAVE:
            self.tryUnRegiTeleportOutsideRecord(toSpaceNo)

        if formula.inLineScene(toSpaceNo) and not formula.inYanWuScene(toSpaceNo):
            self.clearTeleportOutsideRecord()

        context['position'] = position
        context['direction'] = direction
        context['spaceNo'] = spaceNo
        return True

    def _afterLeave_guildBossDungeon(self, fromSpaceNo, toSpaceNo, options, context):
        LOG_INFO('_afterLeave_guildBossDungeon::~')
        guildUUID = context['l']['guildUUID']
        _spaceMgrBox = context['l']['spaceMgrBox']

        self.base.onLeaveDungeon(self.spaceNo, fromSpaceNo)
        if _spaceMgrBox:
            _spaceMgrBox.cell.onPlayerLeave(self.gbId, self.id, self.base)
        self.spaceMgrId = 0

        self.selfStopAutoCombat('leave guild boss dungeon')
        dungeonStub = gameengine.getDungeonStubBySpaceNo(fromSpaceNo)
        dungeonStub.leaveDungeonSpaceSucc(fromSpaceNo, self.base, self.gbId, guildUUID, {})
        return True

# -----------------------------------------
# INIT
if not gameglobal.complexTeleportTypeFnMap:
    IComplexTeleport.regrAllComplexTeleportMethods()
# -----------------------------------------
