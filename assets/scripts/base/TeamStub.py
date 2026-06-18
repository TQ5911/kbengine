# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import copy

import gameengine
import gameconst
import gametimer
import formula
import gameglobal
import gameconfig

import iBaseNoCell
import iGlobal
import iTimer
import team
import dataUtils
import dungeonSrc
import utils
import message_Message_def as M_M_DD
import gamePlay_gamePlay as DDL
import gamePlay_set as GP_S
import teamMatch_matchConfig as TM_MCD
import teamMatch_activity as TMACTD
import raid_raidConst as RAID_CONST
import teamDunChallenge_config as TDC_CFG
import visible_visible as UVVD


class DungeonStubMixin(object):
    """dungeon methods mixin teamStub"""

    def _getParamBydungeonNo(self, dungeonNo, pName):
        if dungeonNo not in DDL.datas:
            return

        prm = DDL.datas[dungeonNo]
        if pName not in prm:
            return
        
        return prm[pName]

    def isTeamMemberSkipCheck(self, dungeonNo):
        return True if self._getParamBydungeonNo(dungeonNo, 'teamMemberSkipCheck') else False

    def getDungeonTeamRange(self, dungeonNo):
        _minPlayerNum = self._getParamBydungeonNo(dungeonNo, 'minNum') or 0
        _maxPlayerNum = self._getParamBydungeonNo(dungeonNo, 'maxNum') or 0

        if _minPlayerNum > _maxPlayerNum:
            LOG_ERR('Error setting player number range in dungeon: {}'.format(dungeonNo))
            _minPlayerNum = _maxPlayerNum

        return _minPlayerNum, _maxPlayerNum

    def _isOutOfTeamDungeonRange(self, box, dungeonNo, teamUUID):
        if teamUUID not in self.teamDict:
            return

        _team = self.teamDict[teamUUID]

        def _filter(fVal):
            if fVal.hasAvatar():
                return fVal

        _foundersNum = len(list(filter(_filter, _team.teamDungeonDict[dungeonNo].founders.values())))
        _, maxNum = self.getDungeonTeamRange(dungeonNo)

        if _foundersNum >= maxNum:
            LOG_WARN('team dungeon out of range, max {}, now {}'.format(maxNum, _foundersNum))
            box.onMessagePre(M_M_DD.datas.dungeonMaxNum, [str(maxNum)])
            return True

        return False

    def _isTeamInDungeonPlayerRange(self, box, dungeonNo, teamUUID):
        """Note: only check when create dungeon"""
        _minNum, _maxNum = self.getDungeonTeamRange(dungeonNo)
        if teamUUID not in self.teamDict:
            return

        _team = self.teamDict[teamUUID]

        _teamNum = len(_team.teamPlayerDict)

        if _minNum <= _teamNum <= _maxNum:
            return True
        elif _minNum > _teamNum:
            box.onMessagePre(M_M_DD.datas.dungeonMinNum, [str(_minNum)])
        elif _maxNum < _teamNum:
            box.onMessagePre(M_M_DD.datas.dungeonMaxNum, [str(_maxNum)])

        LOG_WARN('TeamDungeon::Captain dungeon player range checker failed')
        return False

    def createTeamDungeon(self, playerBox, gbId, dungeonNo, teamUUID, extraInfo):
        _src = extraInfo.get('src')
        _gmEnter = True if \
            _src and _src.srcId == gameconst.DungeonSrcEnum.FROM_CLIENT_GM \
            else False

        if teamUUID not in self.teamDict:
            return

        if not self._isTeamInDungeonPlayerRange(playerBox, dungeonNo, teamUUID) and not _gmEnter:
            return

        dungeonStub = gameengine.getDungeonStubByDungeonNo(
            dungeonNo, gameconst.DungeonEnterTypeEnum.TEAM)
        extraInfo = extraInfo or {}

        _team = self.teamDict[teamUUID]

        if _team.teamCaptainGbId != gbId and not _gmEnter:
            LOG_ERR('createTeamDungeon::Only captain can create dungeon')
            return

        if _team.isTeamDungeonCreating(dungeonNo):
            # 玩家连续创建副本导致此问题, 可以加个弹窗别点太频繁
            LOG_WARN('createTeamDungeon::dungeon "{}" is creating'.format(dungeonNo))
            return

        elif _team.isTeamDungeonCreated(dungeonNo):
            LOG_WARN('createTeamDungeon::dungeon "{}" created'.format(dungeonNo))
            return

        else:
            self._addTeamDungeonSpaceByUUID(teamUUID, dungeonNo, 0, 0)

        extraInfo['maxLevel'] = _team.maxLevel
        extraInfo['spaceLevel'] = _team.averageLevel
        dungeonStub.applyCreateDungeon(playerBox, gbId, teamUUID, extraInfo)

    def afterCreateTeamDungeon(self, teamUUID, dungeonNo, spaceNo, spaceUUID, playerBox, extra):
        self._addTeamDungeonSpaceByUUID(teamUUID, dungeonNo, spaceNo, spaceUUID)
        if 'createAndEnter' in extra and extra['createAndEnter']:
            LOG_INFO('afterCreateTeamDungeon::auto enter space', dungeonNo, spaceNo)
            playerGBID = extra['createAndEnter']
            self._enterTeamDungeonInStub(playerBox, playerGBID, teamUUID, dungeonNo, extra)

            _team = self.teamDict[teamUUID]
            for _tGbId, _tVal in _team.teamPlayerDict.items():
                if _tGbId == playerGBID\
                        or (not _tVal.playerBox)\
                        or _team.getCaptainGbId() != _tGbId:
                    continue

                self._enterTeamDungeonInStub(_tVal.playerBox, _tGbId, teamUUID, dungeonNo, extra)
                break

            for _tGbId, _tVal in _team.teamPlayerDict.items():
                if _tGbId == playerGBID\
                        or (not _tVal.playerBox)\
                        or _team.getCaptainGbId() == _tGbId:
                    continue

                self._enterTeamDungeonInStub(_tVal.playerBox, _tGbId, teamUUID, dungeonNo, extra)

    def enterTeamDungeon(self, box, gbId, teamUUID, dungeonNo, extra):
        LOG_INFO('teamStub:enterTeamDungeon::', teamUUID, dungeonNo, extra)
        extra = extra or {}
        self._enterTeamDungeonInStub(box, gbId, teamUUID, dungeonNo, extra)

    def enterTeamCrusadeDungeon(self, box, gbId, teamUUID, dungeonNo, extra):
        LOG_INFO('teamStub:enterTeamCrusadeDungeon::', gbId, dungeonNo, extra)
        if teamUUID not in self.teamDict:
            return

        _team = self.teamDict[teamUUID]
        remainTime = _team.lastDungeonFinishedTime - utils.curTS()
        if remainTime > 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                                [gbId, ], 'onMessagePre', (TDC_CFG.datas['raid_rejoinCd']['value'], [str(remainTime)]),
                                None, '', ())
            return
        self._enterTeamDungeonInStub(box, gbId, teamUUID, dungeonNo, extra)

    def enterTeamDungeonDirectly(self, box, gbId, teamUUID, dungeonNo, extra):
        LOG_INFO("enterTeamDungeonDirectly::", box, gbId, teamUUID, dungeonNo, extra)
        if teamUUID not in self.teamDict:
            LOG_WARN("enterTeamDungeonDirectly:: teamId not found", gbId, teamUUID, dungeonNo)
            return

        _team = self.teamDict[teamUUID]
        if not _team.isTeamDungeonCreated(dungeonNo):
            LOG_WARN("enterTeamDungeonDirectly::team dungeon not created", gbId, teamUUID, dungeonNo)
            return

        self._directEnterDungeonTeam(box, gbId, teamUUID, dungeonNo, extra)

    def _directEnterDungeonTeam(self, box, gbId, teamUUID, dungeonNo, extra):
        LOG_INFO("_directEnterDungeonTeam  ", gbId, teamUUID, dungeonNo, extra)
        if teamUUID not in self.teamDict:
            return

        _team = self.teamDict[teamUUID]
        _spaceNo = _team.getDungeonSpaceNo(dungeonNo)
        _spaceUUID = _team.getDungeonSpaceUUID(dungeonNo)
        extra.update({'dungeonNo': dungeonNo, 'teamUUID': teamUUID, 'spaceUUID': _spaceUUID})

        _dungeonStub = gameengine.getDungeonStubByDungeonNo(
            dungeonNo, gameconst.DungeonEnterTypeEnum.TEAM)
        _dungeonStub.doEnterDungeon(
            box, gbId, teamUUID, _spaceNo, extra)

    def onEnterDungeonFailedSpaceNotFound(self, box, gbId, teamUUID, dungeonNo, spaceNo, extra):
        LOG_WARN("onEnterDungeonFailedSpaceNotFound::", box, gbId, teamUUID, dungeonNo, spaceNo, extra)
        _spaceUUID = extra.get('spaceUUID', 0)
        if teamUUID not in self.teamDict:
            LOG_WARN("onEnterDungeonFailedSpaceNotFound::team not found", box, gbId, teamUUID, dungeonNo, spaceNo, extra)
            return

        _team = self.teamDict[teamUUID]
        _team.removeDungeonSpaceCache(dungeonNo, spaceNo, _spaceUUID)

    def _enterTeamDungeonInStub(self, box, gbId, teamUUID, dungeonNo, extra):
        LOG_INFO("_enterTeamDungeonInStub ", box, gbId, teamUUID, dungeonNo, extra)
        src = extra.get('src')
        _gmEnter = True if src and src.srcId == gameconst.DungeonSrcEnum.FROM_CLIENT_GM else False

        if teamUUID not in self.teamDict:
            LOG_INFO("_enterTeamDungeonInStub ... teamUUID is existed !!!")
            return

        _team = self.teamDict[teamUUID]
        if not _team.checkDungeonNo(dungeonNo):
            if 'createAndEnter' in extra:
                LOG_ERR('enterTeamDungeon::Create Team Dungeon Failed')
                return

            if _gmEnter:
                extra.update({'createAndEnter': gbId})
                self.createTeamDungeon(box, gbId, dungeonNo, teamUUID, extra)
                LOG_INFO('gm create and enter team dungeon: {}'.format(dungeonNo))
                return

            if _team.teamCaptainGbId != gbId:
                LOG_WARN('Captain must create dungeon first: {}-{}'.format(
                    teamUUID, dungeonNo))
                box.onMessagePre(M_M_DD.datas.createDungeonCondition, [])
                return
            else:
                # check offline condition
                _offlinePLayersName = []
                for m in _team.teamPlayerDict.values():
                    if not m.playerBox:
                        _offlinePLayersName.append(m.playerName)
                if _offlinePLayersName:
                    LOG_WARN('some player offline', teamUUID, _offlinePLayersName)
                    box.onMessagePre(M_M_DD.datas.dungeonTeamNearby, ['、'.join(_offlinePLayersName)])
                    return

                # captain auto create dungeon
                extra.update({'createAndEnter': gbId})
                box.cell.doCheckTeamDungeonConditions(box, gbId, dungeonNo, teamUUID, extra)
                return

        if self._isOutOfTeamDungeonRange(box, dungeonNo, teamUUID):
            LOG_ERR('team dungeon out of range', teamUUID, dungeonNo)
            # team dungeon is full
            return

        def _enterDirectly():
            extra.update({'skipUseNeedItem': True,
                              'teamEnterCheckDic': {_gbId: 1 for _gbId in _team.teamPlayerDict}})
            self._directEnterDungeonTeam(box, gbId, teamUUID, dungeonNo, extra)

        # gm enter
        if _gmEnter:
            _enterDirectly()
            return

        # need SelfItemCheck
        if (gbId in _team.teamDungeonDict[dungeonNo].founders
                and _team.teamDungeonDict[dungeonNo].founders[gbId].isEnter):
            if gameconst.DungeonTypeJudge.isBigWorldDungeon(self._getParamBydungeonNo(dungeonNo, 'type')):
                LOG_WARN('player {} can\'t enter bigWorldDungeon {} again'.format(gbId, dungeonNo))
                # box.onMessagePre(M_M_DD.datas.ERR_MESSAGE_NOT_FOUND, ['无法重新进入此组队世界副本'])
                box.onMessagePre(GP_S.datas["enterDunFailTeammateInDun"]["value"], [])
                return

            _enterDirectly()
            return

        extra.setdefault("teamEnterCheckDic", {}).update({gbId: 1})
        box.selfCheckAndEnterTeamDungeon(teamUUID, dungeonNo, extra)

    def onEnterTeamDungeon(self, box, gbId, teamUUID, dunNo, spaceNo):
        if teamUUID not in self.teamDict:
            return

        _team = self.teamDict[teamUUID]
        if not _team.isTeamDungeonCreated(dunNo):
            LOG_WARN("onEnterTeamDungeon:: team dungeon not created", teamUUID, dunNo, spaceNo)
            _src = dungeonSrc.KickoutFromDungeon(kickReason=gameconst.DungeonSrcKickReason.FORCE)
            box.cell.selfLeaveTeamDungeon(_src)
            return

        _team.onAvatarEnter(dunNo, spaceNo, gbId, box)

    def leaveTeamDungeon(self, box, gbId, teamUUID, dungeonNo, leaveTeam):
        LOG_INFO('leaveTeamDungeon', gbId, teamUUID, dungeonNo, leaveTeam)
        if teamUUID not in self.teamDict:
            return
        if leaveTeam:
            _team = self.teamDict[teamUUID]
            _team.onAvatarLeave(dungeonNo, gbId, isOffline=False)

            self._leaveTeam(box, teamUUID, gbId)
        
        _isBigWorldDungeon = gameconst.DungeonTypeJudge.isBigWorldDungeon(
            DDL.datas[dungeonNo]['type'])

        if _isBigWorldDungeon:
            # 大世界副本由于不能重新进入, 没有玩家后大世界副本本身没有存在的意义,
            # 可以直接销毁
            self._destroyTeamDungeonImme(teamUUID, dungeonNo)

    def onAvatarOffline(self, gbId, teamUUID, dungeonNo):
        if teamUUID not in self.teamDict:
            return

        _team = self.teamDict[teamUUID]
        _team.onAvatarLeave(dungeonNo, gbId, isOffline=True)

        _isBigWorldDungeon = gameconst.DungeonTypeJudge.isBigWorldDungeon(
            DDL.datas[dungeonNo]['type'])

        if _isBigWorldDungeon:
            # 大世界副本由于不能重新进入, 没有玩家后大世界副本本身没有存在的意义,
            # 可以直接销毁
            self._destroyTeamDungeonImme(teamUUID, dungeonNo)

    def _destroyTeamDungeonImme(self, teamUUID, dungeonNo):
        _team = self.teamDict[teamUUID]
        _teamDungeonSpaceVal = _team.teamDungeonDict.get(dungeonNo)
        if not _teamDungeonSpaceVal:
            return

        for gbId, founderVal in _teamDungeonSpaceVal.founders.items():
            if founderVal.hasAvatar():
                break
        else:
            dungeonStub = gameengine.getDungeonStubByDungeonNo(
                dungeonNo, gameconst.DungeonEnterTypeEnum.TEAM)
            self._kickoutPlayer(teamUUID, dungeonNo)
            dungeonStub.destoryDungeonSpace(
                _teamDungeonSpaceVal.spaceNo, _teamDungeonSpaceVal.spaceUUID, 'noPlayer')

    def destroyTeamDungeonDelay(self, teamUUID, dungeonNo, spaceNo, reason, extra):
        LOG_INFO("destroyTeamDungeonDelay ", teamUUID, dungeonNo, spaceNo, reason, extra)
        if teamUUID not in self.teamDict:
            LOG_WARN("destroyTeamDungeonDelay:: team is not found", teamUUID, dungeonNo, spaceNo, reason, extra)
            return

        _team = self.teamDict[teamUUID]

        if dungeonNo not in _team.teamDungeonDict:
            LOG_WARN("destroyTeamDungeonDelay:: dungeon is not found", teamUUID, dungeonNo, spaceNo, reason, extra)
            return

        _teamDungeonSpaceVal = _team.teamDungeonDict[dungeonNo]

        if _teamDungeonSpaceVal.spaceNo != spaceNo:
            LOG_ERR('destroyTeamDungeonDelay::spaceNo not match, this: {}, got: {}'.format(
                _teamDungeonSpaceVal.spaceNo, spaceNo))
            return

        dungeonStub = gameengine.getDungeonStubByDungeonNo(
            dungeonNo, gameconst.DungeonEnterTypeEnum.TEAM)

        dungeonTimeout = self._getParamBydungeonNo(dungeonNo, 'timeOut')
        extra.update({'tTimeout': dungeonTimeout})
        checkBox, reason = _teamDungeonSpaceVal.isDungeonSpaceCanBeDestoried(**extra)

        if checkBox:
            if reason == 'timeout':
                LOG_WARN('dungeon {} timeout({}), destroyed'.format(spaceNo, dungeonTimeout))
            elif reason == 'complete':
                LOG_WARN('dungeon {} already complete, destroyed'.format(spaceNo))
            elif reason == 'noPlayer':
                LOG_WARN('dungeon {} no players in dungeon, destroyed'.format(spaceNo))
            self._kickoutPlayer(teamUUID, dungeonNo)
            dungeonStub.destoryDungeonSpace(spaceNo, _teamDungeonSpaceVal.spaceUUID, reason)
        else:
            if reason == 'timeout':
                LOG_WARN('dungeon {} will be timeout as 60s'.format(spaceNo))

    def _kickoutPlayer(self, teamUUID, dungeonNo):
        if teamUUID not in self.teamDict:
            return

        _team = self.teamDict[teamUUID]
        founders = _team.teamDungeonDict.getDungeonCache(dungeonNo).founders
        _needDestoryGBIDs = []
        _src = dungeonSrc.KickoutFromDungeon(kickReason=gameconst.DungeonSrcKickReason.TIMEOUT)
        for _gbId, _fVal in founders.items():
            base = _fVal.playerBox
            if _fVal.hasAvatar() and base and not utils.checkBoxOffline(base) and base.cell:
                base.cell.selfLeaveTeamDungeon(_src)
            else:
                _needDestoryGBIDs.append(_gbId)

        for _i in _needDestoryGBIDs:
            founders.destoryFounder(_i)

    def onDestroyTeamDungeon(self, teamUUID, dungeonNo, spaceNo, spaceUUID):
        LOG_INFO('onDestroyTeamDungeon:: {} {}'.format(teamUUID, dungeonNo), spaceNo, spaceUUID)
        _team = self.teamDict[teamUUID]
        _team.removeDungeonSpaceCache(dungeonNo, spaceNo, spaceUUID)
        #self.teamDungeonFinished(teamUUID)

    def _addTeamDungeonSpaceByUUID(self, teamUUID, dungeonNo, spaceNo, spaceUUID):
        if teamUUID not in self.teamDict:
            return

        _team = self.teamDict[teamUUID]
        self._addTeamDungeonSpaceByVal(_team, dungeonNo, spaceNo, spaceUUID)

    def _addTeamDungeonSpaceByVal(self, _team, dunNo, spaceNo, spaceUUID):
        _team.addDungeonSpaceCache(dunNo, spaceNo, spaceUUID)

    def onTeammateBeConfirmedTimeout(self, box, gbId, teamUUID, dungeonNo, extra):
        LOG_INFO("onTeammateBeConfirmedTimeout::", box, gbId, teamUUID, dungeonNo, extra)
        if teamUUID not in self.teamDict:
            LOG_WARN("onTeammateBeConfirmedTimeout:: teamUUID not found", teamUUID, dungeonNo)
            return

        _team = self.teamDict[teamUUID]
        teamEnterCheckDic = extra.get('teamEnterCheckDic', {})
        _reason = extra.get('reason', gameconst.TeammateConfirmFailedReason.REJECT)

        if _reason == gameconst.TeammateConfirmFailedReason.TEAM_STATUS_CHANGE:
            pass
        else:
            _rejectPlayerNames = []
            for _playerGBID, _checkBox in teamEnterCheckDic.items():
                if not _team.isInTeam(_playerGBID):
                    continue
                if _checkBox == 0 or (_reason == gameconst.TeammateConfirmFailedReason.TIMEOUT and _checkBox != 1):
                    _rejectPlayerNames.append(_team.getPlayerName(_playerGBID))

            if not _rejectPlayerNames:
                LOG_WARN("onTeammateBeConfirmedTimeout:: not reject name", teamUUID, dungeonNo, extra)
            _team.broadcastToAllMembersBase('onMessagePre', [TDC_CFG.datas['enterRefusedMsg']['value'], ['、'.join(_rejectPlayerNames), ]])


class _RaidMixin(object):

    def createRaidWithTeam(self, srcPlayerBox, srcPlayerGbId, teamUUID, raidUUID, capacity, extraProps):
        LOG_INFO('createRaidWithTeam::', srcPlayerBox, srcPlayerGbId, teamUUID, raidUUID, capacity, extraProps)
        if extraProps is None:
            extraProps = {}

        def _createRaid():
            if teamUUID not in self.teamDict:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_NOT_FOUND.initkvbody(source='createRaidWithTeam',
                                                                                teamId=teamUUID)

            if not dataUtils.isRaidCapacityValidate(capacity):
                return None, gameconst.RaidErrno.ENUM_RAID_UNKNOWN_CAPACITY.initkvbody(source='createRaidWithTeam')

            teamVal = self.teamDict[teamUUID]

            if capacity < len(teamVal.teamPlayerDict):
                return None, gameconst.RaidErrno.ENUM_RAID_CREATE_RAID_OFR.initkvbody(source='createRaidWithTeam',
                                                                                 teamId=teamUUID,
                                                                                 capacity=capacity)

            captainGBID, captainBox = srcPlayerGbId, srcPlayerBox

            if srcPlayerGbId != teamVal.getCaptainGbId():
                LOG_WARN('_createRaidGetMemberProps:: auto fix captain to new one')
                captainGBID = teamVal.getCaptainGbId()
                captainBox = teamVal.fetchCaptainBox()

            if not self._isCanDisbandTeamInStub(teamUUID, captainGBID):
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_CANT_DISBAND.initkvbody(source='createRaidWithTeam',
                                                                                   teamId=teamUUID,
                                                                                   captainGBID=captainGBID,
                                                                                   srcPlayerGbId=srcPlayerGbId)

            _memberDataList = []
            for memberVal in teamVal.teamPlayerDict.values():
                _memberDataList.append(memberVal.toRaidTransDict())

            gameengine.getRaidStub(raidUUID).createRaid(
                captainBox, captainGBID, raidUUID, capacity, _memberDataList, extraProps)

            try:
                markDataInfo = teamVal.teamMark.toClientData()
                markDataInfo['onlyCaptainCanMark'] = teamVal.onlyCaptainCanMark

                gameengine.getRaidStub(raidUUID).addTeamMarkDataFromTeam(raidUUID, markDataInfo)
                # 怪物的话，重新加一下
                for pDic in markDataInfo.get('playerList', []):
                    if pDic['type'] == gameconst.TeamMarkType.MARK_ENEMY and pDic['entId'] in self.teamMarkMonsterRec:
                        ent = self.teamMarkMonsterRec[pDic['entId']].get(0, None)
                        if not ent:
                            continue
                        gameengine.getRaidStub(raidUUID).reqAddRaidMarkMember(raidUUID, None, pDic['type'], pDic['index'], pDic['name'], pDic['gbId'], pDic['entId'], pDic.get('pos'), ent)
            except Exception as e:
                LOG_INFO("addTeamMarkDataFromTeam::error", e)

            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, err = _createRaid()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('createRaidWithTeam:: failed, {}'.format(err))
            return

        self._disbandTeam(teamUUID)

    def applyJoinRaidWithTeam(self, srcPlayerBox, srcPlayerGbId, teamUUID, raidUUID, extraProps):
        LOG_INFO('applyJoinRaidWithTeam::', srcPlayerBox, srcPlayerGbId, teamUUID, raidUUID, extraProps)
        if extraProps is None:
            extraProps = {}

        memberDataList = []
        captainBox, captainGBID = srcPlayerBox, srcPlayerGbId
        def _applyJoinRaid():
            if teamUUID not in self.teamDict:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_NOT_FOUND

            teamVal = self.teamDict[teamUUID]
            if captainGBID != teamVal.getCaptainGbId():
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_TEAM_CAPTAIN

            lvLimit = UVVD.datas.get(RAID_CONST.datas["raidUIVisibleId"]["value"], {}).get('level', utils.getMaxPlayerLevel()+1)
            for memberVal in teamVal.teamPlayerDict.values():
                memberDataList.append(memberVal.toSavedDict())
                if memberVal.level < lvLimit:
                    return None, gameconst.RaidErrno.ENUM_RAID_UI_DENIED

            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, err = _applyJoinRaid()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('applyJoinRaidWithTeam:: failed, {}'.format(
                err.initkvbody(source=_applyJoinRaid.__name__, raidUUID=raidUUID, teamId=teamUUID)))

            if err == gameconst.RaidErrno.ENUM_RAID_UI_DENIED:
                LOG_WARN("applyJoinRaidWithTeam:: some player level check failed", raidUUID)
                srcPlayerBox.onMessagePre(RAID_CONST.datas["raidPartyApply_underLevel_msg"]["value"], [])
            return

        teamVal = self.teamDict[teamUUID]
        extraProps["siegeWarCamp"] = teamVal.siegeWarCamp
        gameengine.getRaidStub(raidUUID).applyJoinRaidWithTeam(
                captainBox, captainGBID, teamUUID, raidUUID, memberDataList, extraProps)


    def replyJoinRaidWithTeam(self, srcPlayerBox, srcPlayerGbId, raidUUID,
                              joinedPlayerGbId, teamUUID, joinMemberList, extraProps):
        LOG_INFO('replyJoinRaidWithTeam::', srcPlayerBox, srcPlayerGbId, raidUUID, joinedPlayerGbId,
                  teamUUID, joinMemberList, extraProps)
        if extraProps is None:
            extraProps = {}

        def _replyJoinRaid():
            if teamUUID not in self.teamDict:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_NOT_FOUND

            teamVal = self.teamDict[teamUUID]
            if joinedPlayerGbId != teamVal.getCaptainGbId():
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_TEAM_CAPTAIN

            memberGBIDSet = set(i['gbId'] for i in joinMemberList)
            if len(teamVal.teamPlayerDict) != len(memberGBIDSet):
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_NUM_NOT_MATCH

            for memberVal in teamVal.teamPlayerDict.values():
                if memberVal.playerGbId not in memberGBIDSet:
                    return None, gameconst.RaidErrno.ENUM_RAID_TEAM_MEMBER_NOT_MATCH

            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, err = _replyJoinRaid()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            err = err.initkvbody(source=_replyJoinRaid.__name__, teamId=teamUUID, raidUUID=raidUUID)
            LOG_ERR('replyJoinRaidWithTeam:: failed, {}'.format(err))

        gameengine.getRaidStub(raidUUID).onTeamReplyJoinRaidWithTeam(
            srcPlayerBox, srcPlayerGbId, raidUUID, joinedPlayerGbId, err, extraProps)

    def raidApplyInvitedRaid(self, raidTarget, srcPlayerBox, srcPlayerGbId, raidUUID, srcPlayerName,
                             raidLeaderGBID, raidLeaderName, invitedPlayerGbId, invitedPlayerName,
                             invitedTeamUUID, raidScore, raidLevel, extraProps):
        LOG_INFO("raidApplyInvitedRaid::", raidTarget, srcPlayerBox, srcPlayerGbId, raidUUID, 
                    srcPlayerName, raidLeaderGBID, raidLeaderName, invitedPlayerGbId, invitedPlayerName,
                    invitedTeamUUID, raidScore, raidLevel, extraProps)
        inviteType = extraProps.get('inviteType', gameconst.InviteType.DEFAULT)
        needMsg = inviteType != gameconst.InviteType.GUILD
        def _raidApplyInvitedRaid():
            if invitedTeamUUID not in self.teamDict:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_NOT_FOUND

            lvLimit = UVVD.datas.get(RAID_CONST.datas["raidUIVisibleId"]["value"], {}).get('level', utils.getMaxPlayerLevel()+1)
            teamVal = self.teamDict[invitedTeamUUID]
            for memberVal in teamVal.teamPlayerDict.values():
                if memberVal.raidUUID and memberVal.raidUUID != raidUUID:
                    return None, gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID
                if memberVal.level < lvLimit:
                    return None, gameconst.RaidErrno.ENUM_RAID_UI_DENIED

            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, _errno = _raidApplyInvitedRaid()
        if _errno != gameconst.RaidErrno.ENUM_RAID_OK:
            if _errno == gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID:
                LOG_WARN("raidApplyInvitedRaid:: some player already in raid", raidUUID)
                if needMsg:
                    srcPlayerBox.onMessagePre(M_M_DD.datas.raid_teamInvitationCheck_sectionTeam, [])
            elif _errno == gameconst.RaidErrno.ENUM_RAID_UI_DENIED:
                LOG_WARN("raidApplyInvitedRaid:: some player level check failed", raidUUID)
                if needMsg:
                    srcPlayerBox.onMessagePre(RAID_CONST.datas["raidPartyInivte_underLevel_msg"]["value"], [])
            else:
                LOG_WARN(f"raidApplyInvitedRaid:: failed, errno={_errno}")
            return
        if needMsg:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [invitedPlayerGbId], 'invitedPlayerOnApplyInvitedRaid',
                (raidUUID, raidTarget, srcPlayerGbId, srcPlayerName, raidLeaderName, raidScore, raidLevel, extraProps),
                self, 'onPlayerIsOffline', (srcPlayerGbId, invitedPlayerName))
        else:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [invitedPlayerGbId], 'invitedPlayerOnApplyInvitedRaid',
                (raidUUID, raidTarget, srcPlayerGbId, srcPlayerName, raidLeaderName, raidScore, raidLevel, extraProps),
                None, '', ())

    def onReplyInviteRaidAndTeamFail(self, playerBox, playerGBID, raidId, srcPlayerGbId, teamId, errno, extra):
        LOG_INFO("onReplyInviteRaidAndTeamFail::", playerBox, playerGBID, raidId, srcPlayerGbId, teamId, errno, extra)
        if teamId not in self.teamDict:
            LOG_WARN('onReplyInviteRaidAndTeamFail:: teamId error', teamId)
            return
        teamVal = self.teamDict[teamId]
        errno = gameconst.RaidErrno._errno(errno)

        _offlinePlayerList = []
        if errno == gameconst.RaidErrno.ENUM_RAID_TEAM_MEMBER_OFFLINE:
            for gbId, teamPlayerVal in teamVal.teamPlayerDict.items():
                if teamPlayerVal.bOnline:
                    continue

                _offlinePlayerList.append((gbId, teamPlayerVal.playerName))

        if _offlinePlayerList:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [srcPlayerGbId, ], 'onMessagePre',
                (M_M_DD.datas.raid_applicantOffline, ['、'.join([_i[1] for _i in _offlinePlayerList])]),
                None, 
                '', 
                ())


class TeamStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer,\
               DungeonStubMixin, _RaidMixin):

    def __init__(self):
        super(TeamStub, self).__init__()
        self.teamDict = {}
        self.teamMarkMonsterRec = {}
        return

    def postReloadScript(self):
        super(TeamStub, self).postReloadScript()
        for v in self.teamDict.values():
            v.reloadScript()

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())

        return

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)

    def getTeamByTeamId(self, teamId) -> team.TeamVal:
        if teamId not in self.teamDict:
            LOG_WARN('getTeamByTeamId teamId error', teamId)
            return
        _teamVal = self.teamDict.get(teamId)
        return _teamVal

    def notifyRemoveApplyInfo(self, teamId, gbId):
        team = self.getTeamByTeamId(teamId)
        if not team:
            return

        captainBox = team.fetchCaptainBox()
        if captainBox and captainBox.client:
            captainBox.client.onRemoveFromApplyList(gbId)
        self.addTimerCB(2, 'removeApplyJoinPlayer', (teamId, gbId), gametimer.TIMER_TAG_REMOVE_APPLY_JOIN_PLAYER)

    def removeApplyJoinPlayer(self, teamId, gbId):
        _teamVal = self.getTeamByTeamId(teamId)
        if _teamVal:
            _teamVal.removeFromApplyDic(gbId)
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [gbId, ], 
                'onRemoveApplyJoinPlayer', 
                (teamId, ), 
                None, 
                '', 
                ())

    def addTeamMemberInStub(self, teamId, teamPlayerInfoDic):
        box = teamPlayerInfoDic['box']
        gbId = teamPlayerInfoDic['gbId']
        playerName = teamPlayerInfoDic['playerName']
        level = teamPlayerInfoDic['level']
        sex = teamPlayerInfoDic['sex']
        school = teamPlayerInfoDic['school']
        picFrameId = teamPlayerInfoDic['picFrameId']
        score = teamPlayerInfoDic['score']
        joinType = teamPlayerInfoDic['joinType']
        openId = teamPlayerInfoDic['openId']

        teamVal = self.teamDict.get(teamId, None)
        if not teamVal:
            return False, gameconst.RaidErrno.ENUM_RAID_TEAM_IS_EMPTY
        return teamVal.addMemberForStub(gbId, box, playerName, level, school, sex, picFrameId, score=score, openId=openId, joinType=joinType)

    def isCanCreateTeam(self, teamId):
        if teamId in self.teamDict:
            LOG_ERR('isCanCreateTeam', teamId, self.teamDict)
            return False
        return True

    def _createTeam(self, teamId, teamTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition, teamPlayerInfoDic):
        box = teamPlayerInfoDic['box']
        gbId = teamPlayerInfoDic['gbId']
        playerName = teamPlayerInfoDic['playerName']
        level = teamPlayerInfoDic['level']
        sex = teamPlayerInfoDic['sex']
        school = teamPlayerInfoDic['school']
        picFrameId = teamPlayerInfoDic['picFrameId']
        score = teamPlayerInfoDic['score']
        siegeWarCamp = teamPlayerInfoDic['siegeWarCamp']
        openId = teamPlayerInfoDic['openId']
        if gameconfig.isCrossServer() and siegeWarCamp != 0:
            teamTarget = gameconst.SIEGEWAR_PARE_ACTIVITY_ID
        teamVal = team.TeamVal(
            teamId, 
            teamTarget, 
            gbId, 
            level, 
            score=score, 
            siegeWarCamp=siegeWarCamp)

        teamVal.teamMinLv = minLevel
        teamVal.teamMinScore = minScore
        teamVal.recruitInfo = recruitInfo
        teamVal.password = password
        teamVal.isAutoExpedition = isAutoExpedition
        teamVal.addMemberForStub(gbId, box, playerName, level, school, sex, picFrameId, True, score=score,
                          mountState=0, isDead=False, openId=openId, joinType = gameconst.TeamJoinType.CREATE)

        self.teamDict[teamId] = teamVal

        # 没有密码的属于公开
        if len(teamVal.password) == 0:
            teamVal.isPublish = True
            # 自由组队目标大于2，才进匹配队列
            if teamVal.teamTarget > gameconst.PARE_ACTIVITY_ID:
                self.teamPrepareAutoMatch(teamId, teamPlayerInfoDic.get('guildUUID', 0))

        # 定时启动自动检查是否自动开始
        self.checkAutoStart(teamId)

        LOG_INFO('_createTeam', self.teamDict)

    def createTeam(self, box, teamId, teamTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition, teamPlayerInfoDic):
        LOG_INFO('createTeam', teamId, teamTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition, teamPlayerInfoDic)
        if not self.isCanCreateTeam(teamId):
            if box and box.cell:
                box.cell.resetTryAddTeamCD()

        else:
            self._createTeam(teamId, teamTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition, teamPlayerInfoDic)

    def checkAutoStart(self, teamID):
        teamVal = self.teamDict.get(teamID)
        if not teamVal:
            return

        if teamVal.autoStartTimer > 0:
            self.cancelTimerCB(teamVal.autoStartTimer, gametimer.TIMER_TAG_TEAM_AUTO_START)
            teamVal.autoStartTimer = 0

        if teamVal.isAutoExpedition and teamVal.teamTarget > gameconst.PARE_ACTIVITY_ID:
            if teamVal.isTeamFull():
                captainBox = teamVal.fetchCaptainBox()
                if captainBox and captainBox.cell:
                    captainBox.cell.autoStartCrusadeDungeon()
                    return
            teamVal.autoStartTimer = self.addTimerCB(5, 'checkAutoStart', (teamID,), gametimer.TIMER_TAG_TEAM_AUTO_START)

    def isCanApplyJoinTeam(self, box, teamId, gbId, level, score, password, ignorePassword, siegeWarCamp, applySource, isTeamUIVisibleId, isTeamDungeonUIVisibleId):
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal:
            box.client and box.client.onApplyJoinTeamFailed(gameconst.TeamApplyResult.TEAM_IS_NOT_EXIST, 0, 0, 0, '', applySource)
            return False

        if teamVal.teamTarget > gameconst.PARE_ACTIVITY_ID:
            if not isTeamUIVisibleId:
                box.client and box.client.onApplyJoinTeamFailed(gameconst.TeamApplyResult.TEAM_APPLY_RAID_UI_IS_NOT_VISIBLE, teamVal.teamId, teamVal.teamMinLv, teamVal.teamMinScore, teamVal.password, applySource)
                box.CheckFuncConditions(dataUtils.getRaidConstDataValue("teamUIVisibleId"))
                return False

            if not isTeamDungeonUIVisibleId:
                box.client and box.client.onApplyJoinTeamFailed(gameconst.TeamApplyResult.TEAM_APPLY_RAID_UI_IS_NOT_VISIBLE, teamVal.teamId, teamVal.teamMinLv, teamVal.teamMinScore, teamVal.password, applySource)
                box.CheckFuncConditions(dataUtils.getRaidConstDataValue("teamDungeonUIVisibleId"))
                return False
            
        if self.checkInDungeon(teamId):
            if box.client:
                box.client.onApplyJoinTeamFailed(gameconst.TeamApplyResult.TEAM_APPLY_IS_IN_DUNGEON, teamVal.teamId, teamVal.teamMinLv, teamVal.teamMinScore, teamVal.password, applySource)
            return False

        if teamVal.isTeamFull():
            if box.client:
                box.onMessagePre(TM_MCD.datas['teamFullMsg']['value'], [])
            return False

        if teamVal.isApplyJoinPlayersFull():
            if box.client:
                box.onMessagePre(TM_MCD.datas['applyFullMsg']['value'], [])
            return False

        if level < teamVal.teamMinLv:
            box.client and box.client.onApplyJoinTeamFailed(gameconst.TeamApplyResult.TEAM_APPLY_LEVEL_IS_NOT_ENOUGH, teamVal.teamId, teamVal.teamMinLv, teamVal.teamMinScore, teamVal.password, applySource)
            return False

        if score < teamVal.teamMinScore:
            box.client and box.client.onApplyJoinTeamFailed(gameconst.TeamApplyResult.TEAM_APPLY_SCORE_IS_NOT_ENOUGH, teamVal.teamId, teamVal.teamMinLv, teamVal.teamMinScore, teamVal.password, applySource)
            return False

        if not ignorePassword:
            if len(teamVal.password) > 0:
                if len(password) == 0:
                    box.client and box.client.onApplyJoinTeamFailed(gameconst.TeamApplyResult.TEAM_APPLY_NEED_PASSWORD, teamVal.teamId, teamVal.teamMinLv, teamVal.teamMinScore, teamVal.password, applySource)
                    return False
                if password != teamVal.password:
                    box.client and box.client.onApplyJoinTeamFailed(gameconst.TeamApplyResult.TEAM_APPLY_WRONG_PASSWORD, teamVal.teamId, teamVal.teamMinLv, teamVal.teamMinScore, teamVal.password, applySource)
                    return False

        if gameconfig.isCrossServer():
            if siegeWarCamp != teamVal.siegeWarCamp and siegeWarCamp != 0 and teamVal.siegeWarCamp != 0:
                if box.client:
                    box.onMessagePre(M_M_DD.datas.teamMatch_differentFactions, [])
                box.client and box.client.onApplyJoinTeamFailed(gameconst.TeamApplyResult.TEAM_APPLY_FAIL, teamVal.teamId, teamVal.teamMinLv, teamVal.teamMinScore, teamVal.password, applySource)
                return False
        box.client and box.client.onApplyJoinTeamFailed(gameconst.TeamApplyResult.TEAM_APPLY_OK, teamVal.teamId, teamVal.teamMinLv, teamVal.teamMinScore, teamVal.password, applySource)
        return True

    def isCanJoinTeam(self, box, teamId, gbId):
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal:
            LOG_WARN('isCanJoinTeam, not found team:', teamId, gbId)
            return
        if teamVal.isTeamFull():
            if box and box.client:
                box.onMessagePre(TM_MCD.datas['teamFullMsg']['value'], [])
            return False
        if not teamVal.isInApplyJoinDic(gbId):
            LOG_WARN('isCanJoinTeam not in applyJoinDict', teamId, gbId, teamVal.applyJoinDict)
            if box and box.client:
                box.onMessagePre(TM_MCD.datas['cancelApplication']['value'], [])
            return False
        return True

    def _applyJoinTeam(self, teamId, teamPlayerInfoDic, applySource):
        LOG_INFO('_applyJoinTeam', teamId, teamPlayerInfoDic, applySource)
        teamVal = self.getTeamByTeamId(teamId)

        gbId = teamPlayerInfoDic['gbId']
        box = teamPlayerInfoDic['box']
        if gbId in teamVal.applyJoinDict:
            if box.client:
                box.onMessagePre(TM_MCD.datas['isAppliedMsg']['value'], [])
            return

        _level = teamPlayerInfoDic['level']
        _playerName = teamPlayerInfoDic['playerName']
        _school = teamPlayerInfoDic['school']
        _sex = teamPlayerInfoDic['sex']
        _score = teamPlayerInfoDic['score']

        teamVal.addApplyJoinPlayer(gbId, _playerName, _level, _school, _sex, applySource, score=_score)

        box.cell.onApplyJoinTeam(teamId, teamVal.teamCaptainGbId)

        captainBox = teamVal.fetchCaptainBox()
        if captainBox and not utils.checkBoxOffline(captainBox) and captainBox.cell:
            teamVal.fetchCaptainBox().cell.procJoinTeamMsg(gbId, _playerName, _level, _school, _sex, _score)

        self.addTimerCB(60, 'notifyRemoveApplyInfo', (teamId, gbId), gametimer.TIMER_TAG_NOTIFY_REMOVE_APPLY_INFO)

    def applyJoinTeam(self, teamId, password, teamPlayerInfoDic, ignorePassword, applySource, datas):
        gbId = teamPlayerInfoDic['gbId']
        box = teamPlayerInfoDic['box']
        level = teamPlayerInfoDic['level']
        score = teamPlayerInfoDic['score']
        siegeWarCamp = teamPlayerInfoDic['siegeWarCamp']
        isTeamUIVisibleId = datas.get('isTeamUIVisibleId', True)
        isTeamDungeonUIVisibleId = datas.get('isTeamDungeonUIVisibleId', True)
        if self.isCanApplyJoinTeam(box, teamId, gbId, level, score, password, ignorePassword, siegeWarCamp, applySource, isTeamUIVisibleId, isTeamDungeonUIVisibleId):
            self._applyJoinTeam(teamId, teamPlayerInfoDic, applySource)


    def replyJoinTeam(self, box, captainGbId, teamId, gbId, bAgree):
        LOG_INFO('replyJoinTeam', captainGbId, teamId, gbId, bAgree)
        if not bAgree:
            # 发送拒绝申请加入的信息
            self.removeApplyJoinPlayer(teamId, gbId)
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([gbId], 'onMessagePre',
                                                                  (TM_MCD.datas['applyCaptainDeniedMsg']['value'], []), None, '', ())
            return

        if not self.isCanJoinTeam(box, teamId, gbId):
            LOG_INFO('isCanJoinTeam fail', captainGbId, teamId, gbId, bAgree)
            if box and box.cell:
                box.cell.resetTryAddTeamCD()

        else:
            _teamVal = self.getTeamByTeamId(teamId)
            _jVal = _teamVal.getApplyJoinPlayerInfo(gbId)
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [gbId], 
                'onReplyJoinTeam',
                (
                    captainGbId, teamId, gbId, _jVal.playerName, _jVal.level, 
                    _jVal.school, _jVal.applySource), 
                self, 
                'onPlayerIsOffline',
                (captainGbId, _jVal.playerName))
        self.removeApplyJoinPlayer(teamId, gbId)

    def clearApplyJoinDicInStub(self, gbId, teamId):
        _teamVal = self.getTeamByTeamId(teamId)
        if gbId != _teamVal.getCaptainGbId():
            LOG_ERR('clearApplyJoinDic error, is not captain', gbId, _teamVal.getCaptainGbId())
            return False

        _teamVal.clearApplyJoinDic()

    def onPlayerIsOffline(self, offlineGbId, gbId, name):
        LOG_INFO('onPlayerIsOffline', offlineGbId, gbId, name)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [gbId], 
            'onMessagePre', 
            (TM_MCD.datas['raid_applicantOffline']['value'], [name]), 
            None, 
            '', 
            ())

    def _isCanDisbandTeamInStub(self, teamId, gbId):
        if teamId not in self.teamDict:
            LOG_ERR('_isCanDisbandTeamInStub teamId error', teamId, gbId)
            return False

        teamVal = self.teamDict.get(teamId)
        if gbId != teamVal.teamCaptainGbId:
            LOG_ERR('_isCanDisbandTeamInStub gbId error', teamId, gbId)
            return False

        return True

    def _disbandTeam(self, teamId):
        teamVal = self.getTeamByTeamId(teamId)
        LOG_INFO('_disbandTeam:', teamId, teamVal.teamPlayerDict.keys())
        for teamPlayerVal in teamVal.teamPlayerDict.values():
            _box = teamPlayerVal.playerBox
            if _box and _box.cell:
                _box.cell.onTeamDisband(True)

            if _box and _box.client:
                _box.onMessagePre(TM_MCD.datas['teamDisbandMsg']['value'], [])

        if (teamVal.teamAutoMatchTime > 0):
            teamVal.teamAutoMatchTime = 0
            gameengine.getGlobalBase('TeamMatchStub').doTeamStopAutoMatch(teamId)

        if teamVal.captainOfflineTimer > 0:
            self.cancelTimerCB(teamVal.captainOfflineTimer, gametimer.TIMER_TAG_CAPTAIN_OFFLINE)
            teamVal.captainOfflineTimer = 0

        try:
            teamVal.clearMarkRecord(self)
        except Exception as e:
            LOG_ERR('doDisbandTeam:: clearMarkRecord exception: {}'.format(e))

        self.teamDict.pop(teamId)

        for dungeonNo, dunVal in teamVal.teamDungeonDict.items():
            stub = gameengine.getDungeonStubBySpaceNo(dunVal.spaceNo)
            stub.completeTeamDungeon(dunVal.spaceNo, teamId, False, 0, gameconst.DunegonCompleteReasonType.LEAVE)
            LOG_WARN('doDisbandTeam:: _disbandTeam and complete dungeon in force ', dungeonNo, dunVal)
        return True

    def doDisbandTeam(self, box, gbId, teamId):
        if self._isCanDisbandTeamInStub(teamId, gbId):
            self._disbandTeam(teamId)

        # todo 自动匹配列表中删除

    def teamDungeonFinished(self, teamId):
        self._disbandTeam(teamId)

    def isCanInviteTeam(self, box, srcTeamId, srcPlayerGbId, invitedPlayerGbId, datas, needMsg=True):
        teamVal = self.teamDict.get(srcTeamId)
        if not teamVal:
            LOG_WARN('isCanInviteTeam teamId error', srcTeamId, srcPlayerGbId)
            if needMsg:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase([invitedPlayerGbId], 'onMessagePre',
                                        (TM_MCD.datas['teamDisbandMsg']['value'], []), None, '', ())
            return False
        
        if teamVal.teamTarget > gameconst.PARE_ACTIVITY_ID:
            isTeamUIVisibleId = datas.get('isTeamUIVisibleId', True)
            isTeamDungeonUIVisibleId = datas.get('isTeamDungeonUIVisibleId', True)
            if not isTeamUIVisibleId:
                if needMsg:
                    box.CheckFuncConditions(dataUtils.getRaidConstDataValue("teamUIVisibleId"))
                return False
            if not isTeamDungeonUIVisibleId:
                if needMsg:
                    box.CheckFuncConditions(dataUtils.getRaidConstDataValue("teamDungeonUIVisibleId"))
                return False
        if teamVal.isTeamFull():
            if needMsg:
                box.onMessagePre(TM_MCD.datas['teamFullMsg']['value'], [])
            return False
        
        return True

    def _applyInviteTeam(self, srcTeamId, srcPlayerGbId, srcLevel, srcSchool, invitedPlayerGbId, name, inviteType):
        needMsg = inviteType != gameconst.InviteType.GUILD
        teamVal = self.getTeamByTeamId(srcTeamId)
        captainGbId = teamVal.getCaptainGbId()
        isDirect = False
        if captainGbId == srcPlayerGbId and teamVal.isInApplyJoinDic(invitedPlayerGbId):
            teamVal.removeFromApplyDic(invitedPlayerGbId)
            isDirect = True

        _captainName = teamVal.getPlayerName(captainGbId)
        _srcPlayerName = teamVal.getPlayerName(srcPlayerGbId)
        if needMsg:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [invitedPlayerGbId], 
                'procInviteTeamMsg', 
                (
                    srcTeamId, teamVal.teamTarget, srcPlayerGbId, _srcPlayerName, 
                    _captainName, srcLevel, srcSchool, teamVal.teamMinScore, 
                    teamVal.teamMinLv, isDirect, inviteType
                ), 
                self, 
                'onPlayerIsOffline', 
                (srcPlayerGbId, name)
            )
        else:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [invitedPlayerGbId], 
                'procInviteTeamMsg', 
                (
                    srcTeamId, teamVal.teamTarget, srcPlayerGbId, _srcPlayerName, 
                    _captainName, srcLevel, srcSchool, teamVal.teamMinScore, 
                    teamVal.teamMinLv, isDirect, inviteType
                ), 
                None, 
                '', 
                ()
            )

    def applyInviteTeam(self, box, srcTeamId, srcPlayerGbId, srcLevel, srcSchool, invitedPlayerGbId, name, datas):
        needMsg = datas.get('inviteType', gameconst.InviteType.DEFAULT) != gameconst.InviteType.GUILD
        if self.isCanInviteTeam(box, srcTeamId, srcPlayerGbId, invitedPlayerGbId, datas):
            self._applyInviteTeam(srcTeamId, srcPlayerGbId, srcLevel, srcSchool, invitedPlayerGbId, name, datas.get('inviteType', gameconst.InviteType.DEFAULT))

    def replyInviteTeamInStub(self, srcTeamId, srcPlayerGbId, teamPlayerInfoDic, inviteType):
        needMsg = inviteType != gameconst.InviteType.GUILD
        _invitedPlayerGbId = teamPlayerInfoDic['gbId']
        _box = teamPlayerInfoDic['box']

        if not self.isCanInviteTeam(_box, srcTeamId, srcPlayerGbId, _invitedPlayerGbId, {}, needMsg):
            if _box and _box.cell:
                _box.cell.resetTryAddTeamCD()
        else:
            teamVal = self.getTeamByTeamId(srcTeamId)
            if srcPlayerGbId == teamVal.getCaptainGbId():
                self.addTeamMemberInStub(srcTeamId, teamPlayerInfoDic)
            else:
                self.applyJoinTeam(srcTeamId, '', teamPlayerInfoDic, True, gameconst.ApplySource.RECRUIT, {'inviteType':inviteType})

    def isCanLeaveTeam(self, teamId, gbId):
        if not teamId:
            LOG_ERR('isCanLeaveTeam teamId param err', teamId, gbId)
            return False
        if teamId not in self.teamDict:
            LOG_WARN('isCanLeaveTeam teamId error', teamId, gbId)
            return False
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal.isInTeam(gbId):
            LOG_WARN("isCanLeaveTeam:: player not found in team", teamId, gbId)
            return False
        return True

    def _leaveTeam(self, leaveBox, teamId, gbId, notifySelf=True):
        LOG_INFO('_leaveTeam', leaveBox, teamId, gbId, notifySelf)
        _teamVal = self.getTeamByTeamId(teamId)
        if len(_teamVal.teamPlayerDict) < 1:
            if not _teamVal.isInDungeon:
                self._disbandTeam(teamId)
        if not _teamVal.isInTeam(gbId):
            LOG_WARN("_leaveTeam:: player not found in team", teamId, gbId)
            return
        leavePlayerName = _teamVal.getPlayerName(gbId)
        _teamVal.delMember(gbId, notifySelf)
        _teamVal.broadcastToAllMembersBase(
            'onMessagePre',
            [TM_MCD.datas['teamChannel_initiativeLeaveTeamMsg']['value'], [leavePlayerName, str(gbId)]])

        if gbId == _teamVal.getCaptainGbId():
            ranCaptainId = _teamVal.getRandomCaptainGbId()
            if ranCaptainId != -1:
                _teamVal.setCaptainGbId(ranCaptainId)
                box = _teamVal.getPlayerBox(ranCaptainId)
                if box and not utils.checkBoxOffline(box) and box.client:
                    box.onMessagePre(TM_MCD.datas['beCaptainMsg']['value'], [])
            elif len(_teamVal.teamPlayerDict) < 1:
                if not _teamVal.isInDungeon:
                    self._disbandTeam(teamId)

    def leaveTeam(self, spaceNo, box, teamId, gbId, notifySelf=True):
        LOG_INFO('leaveTeam', spaceNo, teamId, gbId, notifySelf)
        if not self.isCanLeaveTeam(teamId, gbId):
            return

        self._leaveTeam(box, teamId, gbId, notifySelf)

    def _canKickTeamMemberInStub(self, teamId, gbId, kickGbId):
        _teamVal = self.getTeamByTeamId(teamId)
        if not _teamVal:
            return False
        if not _teamVal.isInTeam(gbId):
            return False
        if _teamVal.getCaptainGbId() != gbId:
            return False
        return True

    def _kickTeamMember(self, teamId, kickGbId, isMemOffline=False):
        LOG_INFO('_kickTeamMember', teamId, kickGbId, isMemOffline)
        teamVal = self.getTeamByTeamId(teamId)
        kickPlayerName = teamVal.getPlayerName(kickGbId)
        teamVal.delMember(kickGbId)
        if isMemOffline:
            msgId = TM_MCD.datas['teamChannel_initiativeLeaveTeamMsg']['value']
        else:
            msgId = TM_MCD.datas['teamChannel_kickedMsg']['value']
        teamVal.broadcastToAllMembersBase('onMessagePre',  [msgId, [kickPlayerName, str(kickGbId)]])

    def kickTeamMember(self, teamId, gbId, kickGbId, isMemOffline):
        if not self._canKickTeamMemberInStub(teamId, gbId, kickGbId):
            return

        self._kickTeamMember(teamId, kickGbId, isMemOffline=isMemOffline)
        if isMemOffline:
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [kickGbId], 
            'onMessagePre',
            (TM_MCD.datas['kickFromTeamMsg']['value'], []), None, '', ())

    def _canTransferCaptainInStub(self, box, teamId, gbId, transferGbId):
        _teamVal = self.getTeamByTeamId(teamId)
        if gbId != _teamVal.getCaptainGbId():
            LOG_ERR('_canTransferCaptainInStub error', gbId, _teamVal.getCaptainGbId())
            return False

        if not _teamVal.isInTeam(transferGbId):
            LOG_INFO('_canTransferCaptainInStub not in team', transferGbId, teamId)
            return False

        if not _teamVal.isTeamMemOnline(transferGbId):
            box.onMessagePre(M_M_DD.datas.approveCaptainOffline , [])
            return False

        return True

    def _transferCaptain(self, teamId, transferGbId):
        _teamVal = self.getTeamByTeamId(teamId)
        _teamVal.setCaptainGbId(transferGbId)
        return _teamVal

    def doTransferCaptain(self, box, teamId, gbId, transferGbId):
        ret = True
        if not self._canTransferCaptainInStub(box, teamId, gbId, transferGbId):
            ret = False

        if not ret:
            return

        _teamVal = self._transferCaptain(teamId, transferGbId)
        _teamVal.broadcastToAllMembersCell('onTransferCaptain', (gbId, transferGbId))
        if _teamVal.captainOfflineTimer > 0:
            self.cancelTimerCB(_teamVal.captainOfflineTimer, gametimer.TIMER_TAG_CAPTAIN_OFFLINE)
            _teamVal.captainOfflineTimer = 0
        if not _teamVal.isTeamMemOnline(transferGbId):
            _teamVal.captainOfflineTimer = self.addTimerCB(TM_MCD.datas["team_TLDownGradeOfflineTime"]["value"], '_onCaptainOffline', (teamId, transferGbId, ), gametimer.TIMER_TAG_CAPTAIN_OFFLINE)

    def isCanApplyBecomeCaptain(self, teamId, gbId):
        _teamVal = self.getTeamByTeamId(teamId)
        if gbId == _teamVal.getCaptainGbId():
            LOG_ERR('isCanApplyBecomeCaptain captainGbId error:', gbId, _teamVal.getCaptainGbId())
            return False

        if not _teamVal.isInTeam(gbId):
            return False

        return True

    def _doApplyBecomeCaptain(self, teamId, gbId, captainGbId, name):
        gameengine\
            .getGlobalBase('PlayerStub')\
            .doOnOthersCell(
                [captainGbId], 
                'processBecomeCaptainMsg',
                (teamId, gbId, name), None, '', ())

        _teamVal = self.getTeamByTeamId(teamId)
        if _teamVal:
            _teamVal.broadcastToAllMembersBase('onMessagePre',
                                            [TM_MCD.datas['teamChannel_applyCaptainMsg']['value'],
                                             [_teamVal.getPlayerName(gbId), _teamVal.getPlayerName(captainGbId), str(gbId), str(captainGbId)]])

    def doApplyBecomeCaptain(self, teamId, gbId, name):
        _teamVal = self.getTeamByTeamId(teamId)
        if not _teamVal:
            return

        if not self.isCanApplyBecomeCaptain(teamId, gbId):
            return

        self._doApplyBecomeCaptain(teamId, gbId, _teamVal.getCaptainGbId(), name)

    def _becomeCaptain(self, teamId, becomeGbId):
        _teamVal = self.getTeamByTeamId(teamId)
        if not _teamVal:
            return None
        if not _teamVal.isInTeam(becomeGbId):
            return None
        _teamVal.setCaptainGbId(becomeGbId)
        return _teamVal

    def replyBecomeCaptainInStub(self, box, teamId, gbId, becomeGbId):
        _teamVal = self._becomeCaptain(teamId, becomeGbId)
        if not _teamVal:
            return
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([becomeGbId], 'onMessagePre',
                                                  (TM_MCD.datas['beCaptainMsg']['value'], []), None, '', ())
        if _teamVal.captainOfflineTimer > 0:
            self.cancelTimerCB(_teamVal.captainOfflineTimer, gametimer.TIMER_TAG_CAPTAIN_OFFLINE)
            _teamVal.captainOfflineTimer = 0
        if not _teamVal.isTeamMemOnline(becomeGbId):
            _teamVal.captainOfflineTimer = self.addTimerCB(TM_MCD.datas["team_TLDownGradeOfflineTime"]["value"], '_onCaptainOffline', (teamId, becomeGbId, ), gametimer.TIMER_TAG_CAPTAIN_OFFLINE)

    def cancelTeamJoinRequest(self, box, gbId, teamId):
        LOG_INFO("cancelTeamJoinRequest::", box, gbId, teamId)
        self.removeApplyJoinPlayer(teamId, gbId)

    def fetchTeamInfoOnLogin(self, box, gbId, teamId):
        _teamVal = self.getTeamByTeamId(teamId)

        if _teamVal:
            if not _teamVal.isInTeam(gbId):
                box.cell.onLeaveTeam()
            else:
                self.updateOnlineState(box, teamId, gbId, True)
                box.cell.onAddTeamCell(_teamVal)
        else:
            box.cell.onTeamDisband(False)

    def notifyPlayerLogon(self, box, gbId, teamId, isRelogin):
        _teamVal = self.getTeamByTeamId(teamId)

        if not _teamVal:
            return

        if _teamVal.isInTeam(gbId):
            box.client.onAddTeam(_teamVal.getClientData())

        if _teamVal.teamCaptainGbId == gbId:
            _teamVal.notifyApplyJoinInfo(gbId)

        _teamVal.fetchCaptainBox().cell.notifyTeamMemberLogon(box, gbId, teamId, isRelogin)

    def teamLogonEnterLine(self, lineType, box, gbId, teamId, extra):
        self.notifyPlayerLogon(box, gbId, teamId, False)

        _teamVal = self.getTeamByTeamId(teamId)
        if _teamVal and _teamVal.isInTeam(gbId):
            extra['teamUUID'] = teamId
            extra['isLeader'] = _teamVal.getCaptainGbId() == gbId

        gameengine.getLineStub(lineType).autoSwitchLine(box, gbId, 0, extra, 'onLogonGetLineNo', (lineType, extra))

    def askAllMemberFollowTeamStub(self, box, teamId, gbId, spaceNo, pos):
        _teamVal = self.getTeamByTeamId(teamId)
        if not _teamVal:
            LOG_ERR("askAllMemberFollowTeamStub team not found", teamId, gbId)
            return

        if gbId != _teamVal.getCaptainGbId():
            LOG_ERR('askAllMemberFollowTeamStub not captain', teamId, gbId)
            return

        _teamVal.askAllMemberFollow(spaceNo, pos)

    def updateMemberAttr(self, box, teamId, gbId, attrDic):
        _teamVal = self.getTeamByTeamId(teamId)
        if not _teamVal or not _teamVal.isInTeam(gbId):
            LOG_WARN('updateMemberAttr not in team', gbId)
            return

        _teamVal.updateMemberAttr(gbId, attrDic)

    def updateMemberVolatileAttr(self, teamId, gbId, attrDic):
        _teamVal = self.getTeamByTeamId(teamId)
        if not _teamVal:
            return
        _teamVal.updateMemberVolatileAttr(gbId, attrDic)

    def _onCaptainOffline(self, teamId, gbId):
        LOG_INFO('_onCaptainOffline::', teamId, gbId)
        _teamVal = self.getTeamByTeamId(teamId)
        if not _teamVal or not _teamVal.isInTeam(gbId):
            LOG_WARN('_onCaptainOffline not in team', gbId)
            return

        if _teamVal.captainOfflineTimer > 0:
            self.cancelTimerCB(_teamVal.captainOfflineTimer, gametimer.TIMER_TAG_CAPTAIN_OFFLINE)
            _teamVal.captainOfflineTimer = 0

        if gbId != _teamVal.getCaptainGbId():
            LOG_WARN('_onCaptainOffline:: failed', teamId, gbId, _teamVal.getCaptainGbId())
            return

        if _teamVal.isTeamMemOnline(gbId):
            return

        if _teamVal.isAllMembersOffline():
            self._disbandTeam(teamId)
        else:
            ranCaptainId = _teamVal.getRandomCaptainGbId()
            _teamVal.setCaptainGbId(ranCaptainId)
            box = _teamVal.getPlayerBox(ranCaptainId)
            if box and box.client:
                box.onMessagePre(TM_MCD.datas['beCaptainMsg']['value'], [])

    def updateOnlineState(self, box, teamId, gbId, bOnline):
        LOG_INFO('updateOnlineState', box, teamId, bOnline, gbId)
        _teamVal = self.getTeamByTeamId(teamId)
        if not _teamVal or not _teamVal.isInTeam(gbId):
            LOG_WARN('updateOnlineState not in team', gbId)
            return

        _teamVal.updateMemberOnlineState(gbId, bOnline, box)
        if gbId == _teamVal.getCaptainGbId():
            if _teamVal.captainOfflineTimer > 0:
                self.cancelTimerCB(_teamVal.captainOfflineTimer, gametimer.TIMER_TAG_CAPTAIN_OFFLINE)
                _teamVal.captainOfflineTimer = 0
            if not bOnline:
                _teamVal.captainOfflineTimer = self.addTimerCB(TM_MCD.datas["team_TLDownGradeOfflineTime"]["value"], '_onCaptainOffline', (teamId, gbId, ), gametimer.TIMER_TAG_CAPTAIN_OFFLINE)

    def sendChatMsgFromTeamMember(self, teamId, gbId, avatarInfo, msg):
        _teamVal = self.getTeamByTeamId(teamId)
        if not _teamVal or not _teamVal.isInTeam(gbId):
            return

        _teamVal.broadcastToAllMembersBase( 'onRecvChannelMsg', (gameconst.ChatChannelEnum.TEAM, avatarInfo, msg), (gbId,))

    def fetchTeamMemberInfo(self, box, teamId, method, args):
        _teamVal = self.getTeamByTeamId(teamId)
        if not _teamVal:
            return
        levels = []
        for _teamPlayerVal in _teamVal.teamPlayerDict.values():
            levels.append(_teamPlayerVal.level)

        info = {'teamId':teamId, 'levels':levels}
        getattr(box, method)(info, *args)

    def challengeDunNotifyMsg(self, teamId, msgId, gbIds):
        _teamVal = self.getTeamByTeamId(teamId)
        if not _teamVal:
            return

        names = []
        for gbId in gbIds:
            names.append(_teamVal.getPlayerName(gbId))

        if names:
            nameStr = '.'.join(names)
            _teamVal.broadcastToAllMembersBase(
                'onMessagePre',
                (
                    msgId,
                    [nameStr]
                )
            )

    def teamPrepareAutoMatch(self, teamId, guildUUID):
        LOG_INFO('in teamPrepareAutoMatch:', teamId, guildUUID)
        _teamVal = self.getTeamByTeamId(teamId)
        if not _teamVal:
            return
        if not _teamVal.checkTeamTarget(_teamVal.teamMinLv, _teamVal.teamMinScore):
            return
        if _teamVal.isTeamFull():
            LOG_WARN('   in teamPrepareAutoMatch, team full:', teamId)
            _teamVal.fetchCaptainBox().onMessagePre(TM_MCD.datas['teamMatch_fullMsg']['value'], [])
            return
        _teamVal.startAutoMatch(guildUUID)

    def doTeamPrepareStopAutoMatch(self, teamId):
        LOG_INFO('in doTeamPrepareStopAutoMatch:', teamId)
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal:
            return
        teamVal.stopAutoMatch()

    def newPlayerMatched(self, teamId, newPlayerDic):
        teamVal = self.getTeamByTeamId(teamId)
        LOG_INFO('in newPlayerMatched:', teamId, newPlayerDic, teamVal)
        if not teamVal:
            return
        newPlayerDic['joinType'] = gameconst.TeamJoinType.MATCH
        self.addTeamMemberInStub(teamId, newPlayerDic)
        return

    def setTeamTarget(self, gbID, teamId, teamTarget, minLv, minScore, recruitInfo, password, isAutoExpedition, guildUUID):
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal:
            LOG_ERR('in setTeamTarget: missing team, ', teamId, teamTarget, minLv, minScore, recruitInfo, isAutoExpedition)
            return
        if teamVal.teamCaptainGbId != gbID:
            LOG_ERR('in setTeamTarget: only leader can set team target, ', teamId, teamTarget, minLv, minScore, recruitInfo, isAutoExpedition)
            return
        if teamTarget != teamVal.teamTarget:
            LOG_ERR('in setTeamTarget: target not same, ', teamId, teamTarget, minLv, minScore, recruitInfo, isAutoExpedition)
            return
        if minLv != teamVal.teamMinLv or minScore != teamVal.teamMinScore or password != teamVal.password:
            LOG_ERR('in setTeamTarget: base team info is not same, ', teamId, teamTarget, minLv, minScore, recruitInfo, isAutoExpedition)
            return
        if recruitInfo == teamVal.recruitInfo and isAutoExpedition == teamVal.isAutoExpedition:
            LOG_ERR('in setTeamTarget: set team info is same, ', teamId, teamTarget, minLv, minScore, recruitInfo, isAutoExpedition)
            return
        # check team member's level and score
        if not teamVal.setTarget(teamTarget, minLv, minScore, recruitInfo, password, isAutoExpedition):
            return

        # 改完队伍的目标之后，统一刷一遍匹配条件
        self.doTeamPrepareStopAutoMatch(teamId)
        if teamVal.isPublish and teamVal.teamTarget > gameconst.PARE_ACTIVITY_ID:
            self.teamPrepareAutoMatch(teamId, guildUUID)

        self.checkAutoStart(teamId)

    def getTeamInfo(self, box, teamId):
        pass

    def getTeamList(self, box, teamTarget, checkTime, checkTeamstubNum, sendTeamNum, startTeamStubIndex):
        LOG_INFO('in getTeamList:', teamTarget, checkTime, checkTeamstubNum, sendTeamNum, startTeamStubIndex)
        _teamList = []
        # 根据队伍的创建时间排序，最晚创建的队伍在最前面
        _releaseNum = gameconst.TEAM_MAX_LIST_NUM - sendTeamNum
        _sortedDic = sorted(self.teamDict.items(), key=lambda x: x[1].tCreated, reverse=True)
        for _teamId, _teamVal in _sortedDic:
            if len(_teamList) >= _releaseNum:
                break
            if _teamVal.teamTarget != teamTarget:
                continue
            if _teamVal.isTeamFull():
                continue
            if _teamVal.isAllMembersOffline():
                continue
            if self.checkInDungeon(_teamId):
                continue
            _teamList.append(_teamVal.getClientData())

        box.client.onGetTeamList(checkTime, teamTarget, _teamList)
        sendTeamNum += len(_teamList)
        checkTeamstubNum += 1
        if checkTeamstubNum >= gameconst.TEAMSTUB_CONF_NUM:
            box.cell.onGetTeamListFinished(checkTeamstubNum - 1, teamTarget)
            return

        if sendTeamNum >= gameconst.TEAM_MAX_LIST_NUM:
            box.cell.onGetTeamListFinished(checkTeamstubNum - 1, teamTarget)
            return

        gameengine\
            .getTeamStub(startTeamStubIndex + checkTeamstubNum)\
            .getTeamList(
                box, teamTarget, checkTime, checkTeamstubNum, 
                sendTeamNum, startTeamStubIndex)

    def updateTeamSilentFlag(self, teamId, isSilent):
        LOG_INFO('updateTeamSilentFlag:', teamId, isSilent)
        _teamVal = self.getTeamByTeamId(teamId)
        if not teamId:
            LOG_WARN('not found _teamVal:', teamId)
            return

        _teamVal.setSilentFlag(bool(isSilent))

    def sendTeamMemberMsg(self,teamId,messageId,messageArgs):
        _teamVal = self.getTeamByTeamId(teamId)
        if not _teamVal :
            return

        _teamVal.sendTeamMemberMsg(messageId,messageArgs)

    def sendTeamMemberMessage_localCross(self,teamId, messageId, messageArgs):
        _teamVal = self.getTeamByTeamId(teamId)
        if not _teamVal :
            return

        _teamVal.sendTeamMemberMsg(messageId,messageArgs, localCross=True)

    # --------------------------------------------------------------------
    # TEAM MICS
    def switchTeamMicsMode(self, srcPlayerBox, srcPlayerGbId, teamId, mode, extraProps):
        LOG_INFO("switchTeamMicsMode::", srcPlayerBox, srcPlayerGbId, teamId, mode, extraProps)
        _teamVal, err = self._switchTeamMicsMode(srcPlayerBox, srcPlayerGbId, teamId, mode, extraProps)
        if err:
            LOG_WARN('switchTeamMicsMode:: failed, {}'.format(err))
            return

        _teamVal.getAllTeamMemberMiscStatus()

    def _switchTeamMicsMode(self, srcPlayerBox, srcPlayerGbId, teamId, mode, extraProps):
        if teamId not in self.teamDict:
            return None, "TEAM_ID_NOT_FOUND"

        _teamVal = self.teamDict[teamId]
        return _teamVal.switchTeamMiscMode(srcPlayerGbId, mode, extraProps)

    def turnOnTeamMics(self, srcPlayerBox, srcPlayerGbId, teamId, playerGBID, extraProps):
        LOG_INFO("turnOnTeamMics::", srcPlayerBox, srcPlayerGbId, teamId, playerGBID, extraProps)
        _, err = self._turnOnTeamMics(srcPlayerBox, srcPlayerGbId, teamId, playerGBID)
        if err:
            LOG_WARN('turnOnTeamMics:: failed, {}'.format(err))

    def _turnOnTeamMics(self, srcPlayerBox, srcPlayerGbId, teamId, playerGBID):
        if teamId not in self.teamDict:
            return None, "TEAM_ID_NOT_FOUND"

        teamVal = self.teamDict[teamId]
        return teamVal.turnOnTeamMemberMics(srcPlayerGbId, playerGBID, toClient=True)

    def turnOffTeamMics(self, srcPlayerBox, srcPlayerGbId, teamId, playerGBID, extraProps):
        LOG_INFO("turnOffTeamMics::", srcPlayerBox, srcPlayerGbId, teamId, playerGBID, extraProps)
        _, err = self._turnOffTeamMics(srcPlayerBox, srcPlayerGbId, teamId, playerGBID)
        if err:
            LOG_WARN('turnOffTeamMics:: failed, {}'.format(err))

    def _turnOffTeamMics(self, srcPlayerBox, srcPlayerGbId, teamId, playerGBID):
        if teamId not in self.teamDict:
            return None, "TEAM_ID_NOT_FOUND"

        teamVal = self.teamDict[teamId]
        return teamVal.turnOffTeamMemberMics(srcPlayerGbId, playerGBID, blockMics=False, toClient=True)

    def blockTeamMemberMics(self, srcPlayerBox, srcPlayerGbId, teamId, playerGBID, extraProps):
        LOG_INFO("blockTeamMemberMics::", srcPlayerBox, srcPlayerGbId, teamId, playerGBID, extraProps)
        _, err = self._blockTeamMemberMics(srcPlayerBox, srcPlayerGbId, teamId, playerGBID)
        if err:
            LOG_WARN('blockTeamMemberMics:: failed, {}'.format(err))

    def _blockTeamMemberMics(self, srcPlayerBox, srcPlayerGbId, teamId, playerGBID):
        if teamId not in self.teamDict:
            return None, "TEAM_ID_NOT_FOUND"

        teamVal = self.teamDict[teamId]
        return teamVal.turnOffTeamMemberMics(srcPlayerGbId, playerGBID, blockMics=True, toClient=True)

    def unblockTeamMemberMics(self, srcPlayerBox, srcPlayerGbId, teamId, playerGBID, extraProps):
        LOG_INFO("unblockTeamMemberMics::", srcPlayerBox, srcPlayerGbId, teamId, playerGBID, extraProps)
        _, err = self._unblockTeamMemberMics(srcPlayerBox, srcPlayerGbId, teamId, playerGBID)
        if err:
            LOG_WARN('unblockTeamMemberMics:: failed, {}'.format(err))
            if err == 'TEAM_ALL_MISC_BLOCKED':
                srcPlayerBox.onMessagePre(M_M_DD.datas.voiceChat_allMicBanned, [])

    def _unblockTeamMemberMics(self, srcPlayerBox, srcPlayerGbId, teamId, playerGBID):
        if teamId not in self.teamDict:
            return None, "TEAM_ID_NOT_FOUND"

        teamVal = self.teamDict[teamId]
        return teamVal.unblockTeamMemberMisc(playerGBID, toClient=True)

    def blockAllTeamMemberMics(self, srcPlayerBox, srcPlayerGbId, teamId, extraProps):
        LOG_INFO("blockAllTeamMemberMics::", srcPlayerBox, srcPlayerGbId, teamId, extraProps)
        teamVal, err = self._blockAllTeamMemberMics(srcPlayerBox, srcPlayerGbId, teamId)
        if err:
            LOG_WARN('blockAllTeamMemberMics:: failed, {}'.format(err))
            return

        teamVal.broadcastToAllMembersClient('onBlockAllTeamMemberMics', (srcPlayerGbId, teamId))

    def _blockAllTeamMemberMics(self, srcPlayerBox, srcPlayerGbId, teamId):
        if teamId not in self.teamDict:
            return None, "TEAM_ID_NOT_FOUND"

        teamVal = self.teamDict[teamId]
        if not teamVal.teamMicsSwitch:
            return None, "TEAM_MICS_SWITCH_OFF"

        if teamVal.teamMicsBlocked:
            return None, "TEAM_ALL_MISC_BLOCKED"

        for playerGBID, playerVal in teamVal.teamPlayerDict.items():
            if playerGBID == srcPlayerGbId:
                continue
            _, err = teamVal.turnOffTeamMemberMics(srcPlayerGbId, playerGBID, blockMics=True, toClient=False)
            if err:
                LOG_WARN("_blockAllTeamMemberMics::failed, err={}".format(err),
                            srcPlayerGbId, teamId, playerGBID, playerVal)

        teamVal.teamMicsBlocked = True
        return teamVal, ""

    def unblockAllTeamMemberMics(self, srcPlayerBox, srcPlayerGbId, teamId, extraProps):
        LOG_INFO("unblockAllTeamMemberMics::", srcPlayerBox, srcPlayerGbId, teamId, extraProps)
        teamVal, err = self._unblockAllTeamMemberMics(srcPlayerBox, srcPlayerGbId, teamId)
        if err:
            LOG_WARN('unblockAllTeamMemberMics:: failed, {}'.format(err))
            return

        teamVal.broadcastToAllMembersClient('onUnblockAllTeamMemberMics', (srcPlayerGbId, teamId))

    def _unblockAllTeamMemberMics(self, srcPlayerBox, srcPlayerGbId, teamId):
        if teamId not in self.teamDict:
            return "TEAM_ID_NOT_FOUND"

        teamVal = self.teamDict[teamId]
        if not teamVal.teamMicsSwitch:
            return None, "TEAM_MICS_SWITCH_OFF"

        teamVal.teamMicsBlocked = False
        for playerGBID, playerVal in teamVal.teamPlayerDict.items():
            _, err = teamVal.unblockTeamMemberMisc(playerGBID, toClient=False)
            if err:
                LOG_WARN("_unblockAllTeamMemberMics::failed, err={}".format(err),
                            srcPlayerGbId, teamId, playerGBID, playerVal)
        return teamVal, ""

    # --------------------------------------------------------------------

    def debugAllTeamInfo(self):
        LOG_INFO('!!!!!!!========== debug all team info start ==========')
        for teamid, info in self.teamDict.items():
            LOG_INFO('!!!!!!!teamid:', teamid)
            LOG_INFO('!!!!!!!        组队目标:{}, 等级区间{}~{}'.format(TMACTD.datas[info.teamTarget]['value'], info.teamMinLv, info.teamMinScore))
            LOG_INFO('!!!!!!!        组队人数:{}}'.format(len(info.teamPlayerDict)))
        LOG_INFO('!!!!!!!========== debug all team info end ==========')

    # --------------------------------------------------------------------
    # TEAM CROSS SERVER

    # --------------------------------------------------------------------

    def getCaptainName(self, teamId, box, callBackFuncName, bossId):
        if teamId not in self.teamDict:
            return

        teamVal = self.teamDict[teamId]

        fn = getattr(box.cell, callBackFuncName, None)
        fn and fn(teamId, teamVal.getCaptainName(), bossId)


    # 标记相关
    def reqAddMarkMember(self, teamId, playerBox, type, index, name, gbId, entId, pos, box):
        LOG_INFO('reqAddMarkMember', teamId, type, index, name, gbId, entId, pos, box)
        if teamId not in self.teamDict:
            return

        # 要先执行删除
        self.reqDelMarkMember(teamId, playerBox, type, index)

        teamVal = self.teamDict[teamId]
        teamVal.addMarkMember(playerBox, type, index, name, gbId, entId, pos)
        # 记录
        if type == gameconst.TeamMarkType.MARK_ENEMY and entId > 0:
            self.addTeamMarkMonsterRec(teamId, entId, index, box)

    def addTeamMarkMonsterRec(self, teamId, entId, index, box):
        # 满了说明处理逻辑有问题，功能暂停
        if len(self.teamMarkMonsterRec) >= 20000:
            LOG_INFO('addTeamMarkMonsterRec, mark monster rec full ', len(self.teamMarkMonsterRec))
            return
        if not self.teamMarkMonsterRec.get(entId, None):
            self.teamMarkMonsterRec[entId] = {0: box}

        if len(self.teamMarkMonsterRec[entId]) >= 10000:
            LOG_INFO('addTeamMarkMonsterRec, mark monster rec full for entId: ', entId, len(self.teamMarkMonsterRec[entId]))
            return
        self.teamMarkMonsterRec[entId][teamId] = index
        LOG_INFO('addTeamMarkMonsterRec, mark monster rec:', entId, teamId, index)
        #
        box.onBeMarkedAsEnemy(teamId, gameconst.TeamType.TEAM, index)

    def delMarkMonsterRec(self, teamId, entId):
        if entId not in self.teamMarkMonsterRec:
            return
        if teamId in self.teamMarkMonsterRec[entId]:
            self.teamMarkMonsterRec[entId].pop(teamId)
            LOG_INFO('delMonsterRec, del mark monster rec:', entId, teamId)
            box = self.teamMarkMonsterRec[entId].get(0, None)
            if box:
                box.delBeMarkedAsEnemy(teamId, gameconst.TeamType.TEAM)

        if len(self.teamMarkMonsterRec[entId]) <= 1:   # 最后只剩box了
            self.teamMarkMonsterRec.pop(entId)
            LOG_INFO('delMonsterRec, remove mark monster rec box:', entId)

    def reqDelMarkMember(self, teamId, playerBox, type, index):
        LOG_INFO('reqDelMarkMember', teamId, type, index)
        if teamId not in self.teamDict:
            return
        teamVal = self.teamDict[teamId]
        entId = teamVal.delMarkMember(playerBox, type, index)

        self.delMarkMonsterRec(teamId, entId)

    def onMarkMonsterDead(self, entId):
        if entId not in self.teamMarkMonsterRec:
            return
        teamInfo = self.teamMarkMonsterRec.get(entId, {})
        LOG_INFO('onMarkMonsterDead, remove mark monster:', entId, teamInfo.keys())
        teamInfo = copy.deepcopy(teamInfo)
        for teamId, index in teamInfo.items():
            self.reqDelMarkMember(teamId, None, gameconst.TeamMarkType.MARK_ENEMY, index)

    def reqChangeOnlyCaptain(self, teamId, playerBox, state):
        LOG_INFO('reqChangeOnlyCaptain', teamId, state)
        if teamId not in self.teamDict:
            return
        teamVal = self.teamDict[teamId]
        teamVal.changeOnlyCaptainState(playerBox, state)

    def reqJoinTeam(self, playerBox, teamID, password, playerProps):
        err = self._reqJoinTeamCheck(teamID, password, playerProps)
        # 加入成功，刷新一下成员的cache
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR("reqJoinRaid, err:", err, playerProps)
            return

    def _reqJoinTeamCheck(self, teamID, password, playerProps):
        teamVal = self.getTeamByTeamId(teamID)
        LOG_INFO('in _reqJoinTeamCheck:', teamID, playerProps, teamVal)
        if not teamVal:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_NOT_FOUND

        # 非公开的需要检查一下密码
        if not teamVal.isPublish:
            if teamVal.password != password:
                return None, gameconst.RaidErrno.ENUM_RAID_PASSWORD_IS_WRONG

        teamTargetInfo = TMACTD.datas.get(teamVal.teamTarget)
        if teamTargetInfo is None:
            LOG_ERR("_reqJoinTeamCheck, misssing teamTarget", teamVal.teamTarget)
            return None, gameconst.RaidErrno.ENUM_UNKNOWN

        score = playerProps['score']
        level = playerProps['level']
        cfgMinLv = teamTargetInfo['minLevel']
        cfgMinScore = teamTargetInfo['minScore']
        if level < cfgMinLv:
            return None, gameconst.RaidErrno.ENUM_RAID_LEVEL_IS_LIMITED
        if score < cfgMinScore:
            return None, gameconst.RaidErrno.ENUM_RAID_SCORE_LIMITED
        _, err = self.addTeamMemberInStub(teamID, playerProps)
        return err

    def setInDungeon(self, teamId, status):
        teamVal = self.teamDict.get(teamId, None)
        if not teamVal:
            LOG_WARN('setInDungeon, not found team:', teamId)
            return
        teamVal.isInDungeon = status

    def checkInDungeon(self, teamId):
        teamVal = self.teamDict.get(teamId, None)
        if not teamVal:
            LOG_WARN('checkInDungeon, not found team:', teamId)
            return False
        return teamVal.isInDungeon

    def refreshLastDungeonFinishedTime(self, teamId, lastDungeonFinishedTime):
        LOG_INFO("refreshLastDungeonFinishedTime", teamId, lastDungeonFinishedTime)
        teamVal = self.teamDict.get(teamId, None)
        if not teamVal:
            LOG_WARN('refreshLastDungeonFinishedTime, not found team:', teamId)
            return
        teamVal.lastDungeonFinishedTime = lastDungeonFinishedTime + TDC_CFG.datas['raid_rejoinCdTime']['value']

        teamVal.broadcastToAllMembersClient('onRefreshLastDungeonFinishedTime', (gameconst.TeamType.TEAM, teamVal.lastDungeonFinishedTime))

    def modifyPlayerName(self, box, teamId, gbId, newName, oldName):
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal or not teamVal.isInTeam(gbId):
            LOG_WARN('modifyPlayerName not in team', gbId)
            return
        self.updateMemberVolatileAttr(teamId, gbId, {'playerName': newName})
        teamVal.broadcastToAllMembersBase('onMessagePre', (TM_MCD.datas['teammateChangeNameMsg']['value'], [oldName, newName]), exclude=(gbId,))

    def broadcastToAllMembers(self, box, gbId, teamId, exclude, comp, func, args):
        LOG_INFO("broadcastToAllMembers team", gbId, teamId, exclude, comp, func, args)
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal or not teamVal.isInTeam(gbId):
            LOG_WARN('broadcastToAllMembers not in team')
            return

        if gameconst.CELL == comp:
            teamVal.broadcastToAllMembersCell(func, args, exclude)
        else:
            teamVal.broadcastToAllMembersBase(func, args, exclude)
