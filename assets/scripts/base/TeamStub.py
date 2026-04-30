# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

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
import message_Message_def as MMD
import gamePlay_gamePlay as DDL
import gamePlay_set as GP_S
import teamMatch_matchConfig as TMMCD
import teamMatch_activity as TMACTD
import raid_raidConst as RAID_CONST
import teamDunChallenge_config as TDC_CFG
import visible_visible as UVVD
import copy


class DungeonStubMixin(object):
    """dungeon methods mixin teamStub"""

    def _getPrmBydungeonNo(self, dungeonNo, pName):
        if dungeonNo in DDL.datas:
            prm = DDL.datas[dungeonNo]
            if pName in prm:
                return prm[pName]

    def isTeamMemberSkipCheck(self, dungeonNo):
        return True if self._getPrmBydungeonNo(dungeonNo, 'teamMemberSkipCheck') else False

    def getDungeonTeamRange(self, dungeonNo):
        minPlayerNum = self._getPrmBydungeonNo(dungeonNo, 'minNum') or 0
        maxPlayerNum = self._getPrmBydungeonNo(dungeonNo, 'maxNum') or 0

        if minPlayerNum > maxPlayerNum:
            LOG_ERR('Error setting player number range in dungeon: {}'.format(dungeonNo))
            minPlayerNum = maxPlayerNum

        return minPlayerNum, maxPlayerNum

    def _isOutOfTeamDungeonRange(self, box, dungeonNo, teamUUID):
        if teamUUID not in self.teamDic:
            return

        _team = self.teamDic[teamUUID]

        def _filter(fVal):
            if fVal.hasAvatar():
                return fVal

        _foundersNum = len(list(filter(_filter, _team.teamDungeonDic[dungeonNo].founders.values())))
        _, maxNum = self.getDungeonTeamRange(dungeonNo)

        if _foundersNum >= maxNum:
            LOG_WARN('team dungeon out of range, max {}, now {}'.format(maxNum, _foundersNum))
            box.onMessagePre(MMD.datas.dungeonMaxNum, [str(maxNum)])
            return True

        return False

    def _isTeamInDungeonPlayerRange(self, box, dungeonNo, teamUUID, ignoreMin=False):
        """Note: only check when create dungeon"""
        minNum, maxNum = self.getDungeonTeamRange(dungeonNo)
        if teamUUID not in self.teamDic:
            return

        _team = self.teamDic[teamUUID]

        _teamNum = len(_team.teamPlayerDic)

        if minNum <= _teamNum <= maxNum:
            return True
        elif minNum > _teamNum:
            box.onMessagePre(MMD.datas.dungeonMinNum, [str(minNum)])
        elif maxNum < _teamNum:
            box.onMessagePre(MMD.datas.dungeonMaxNum, [str(maxNum)])

        LOG_WARN('TeamDungeon::Captain dungeon player range checker failed')
        return False

    def createTeamDungeon(self, playerBox, gbId, dungeonNo, teamUUID, extraInfo):
        src = extraInfo.get('src')
        _gmEnter = True if \
            src and src.srcId == gameconst.DungeonSrcEnum.FROM_CLIENT_GM \
            else False

        if teamUUID not in self.teamDic:
            return

        if not self._isTeamInDungeonPlayerRange(playerBox, dungeonNo, teamUUID) and not _gmEnter:
            return

        dungeonStub = gameengine.getDungeonStubByDungeonNo(
            dungeonNo, gameconst.DungeonEnterTypeEnum.TEAM)
        extraInfo = extraInfo or {}

        _team = self.teamDic[teamUUID]

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
            self.addTeamDungeonSpace(teamUUID, dungeonNo, 0, 0)

        extraInfo['spaceLevel'] = _team.averageLevel
        extraInfo['maxLevel'] = _team.maxLevel
        dungeonStub.applyCreateDungeon(playerBox, gbId, teamUUID, extraInfo)

    def onCreateTeamDungeon(self, teamUUID, dungeonNo, spaceNo, spaceUUID, playerBox, extra):
        self.addTeamDungeonSpace(teamUUID, dungeonNo, spaceNo, spaceUUID)
        if 'createAndEnter' in extra and extra['createAndEnter']:
            LOG_IFO('onCreateTeamDungeon::auto enter space', dungeonNo, spaceNo)
            playerGBID = extra['createAndEnter']
            self._enterTeamDungeon(playerBox, playerGBID, teamUUID, dungeonNo, extra)

            _team = self.teamDic[teamUUID]
            for _tGbId, _tVal in _team.teamPlayerDic.items():
                if _tGbId == playerGBID or (not _tVal.playerBox) or _team.getCaptainGbId() != _tGbId:
                    continue
                self._enterTeamDungeon(_tVal.playerBox, _tGbId, teamUUID, dungeonNo, extra)
                break

            for _tGbId, _tVal in _team.teamPlayerDic.items():
                if _tGbId == playerGBID or (not _tVal.playerBox) or _team.getCaptainGbId() == _tGbId:
                    continue
                self._enterTeamDungeon(_tVal.playerBox, _tGbId, teamUUID, dungeonNo, extra)

    def enterTeamDungeon(self, box, gbId, teamUUID, dungeonNo, extra):
        LOG_IFO('teamStub:enterTeamDungeon::', teamUUID, dungeonNo, extra)
        extra = extra or {}
        self._enterTeamDungeon(box, gbId, teamUUID, dungeonNo, extra)

    def enterTeamCrusadeDungeon(self, box, gbId, teamUUID, dungeonNo, extra):
        LOG_IFO('teamStub:enterTeamCrusadeDungeon::', gbId, dungeonNo, extra)
        self._enterTeamDungeon(box, gbId, teamUUID, dungeonNo, extra)

    def enterTeamDungeonDirectly(self, box, gbId, teamUUID, dungeonNo, extra):
        LOG_IFO("enterTeamDungeonDirectly::", box, gbId, teamUUID, dungeonNo, extra)
        if teamUUID not in self.teamDic:
            LOG_WARN("enterTeamDungeonDirectly:: teamId not found", gbId, teamUUID, dungeonNo)
            return

        _team = self.teamDic[teamUUID]
        if not _team.isTeamDungeonCreated(dungeonNo):
            LOG_WARN("enterTeamDungeonDirectly::team dungeon not created", gbId, teamUUID, dungeonNo)
            return

        self._enterTeamDungeonDirectly(box, gbId, teamUUID, dungeonNo, extra)

    def _enterTeamDungeonDirectly(self, box, gbId, teamUUID, dungeonNo, extra):
        LOG_IFO("_enterTeamDungeonDirectly  ", gbId, teamUUID, dungeonNo, extra)
        if teamUUID not in self.teamDic:
            return

        _team = self.teamDic[teamUUID]
        spaceNo = _team.getDungeonSpaceNo(dungeonNo)
        spaceUUID = _team.getDungeonSpaceUUID(dungeonNo)
        extra.update({'dungeonNo': dungeonNo, 'teamUUID': teamUUID, 'spaceUUID': spaceUUID})

        dungeonStub = gameengine.getDungeonStubByDungeonNo(
            dungeonNo, gameconst.DungeonEnterTypeEnum.TEAM)
        dungeonStub.doEnterDungeon(
            box, gbId, teamUUID, spaceNo, extra)

    def onEnterDungeonFailedSpaceNotFound(self, box, gbId, teamUUID, dungeonNo, spaceNo, extra):
        LOG_WARN("onEnterDungeonFailedSpaceNotFound::", box, gbId, teamUUID, dungeonNo, spaceNo, extra)
        spaceUUID = extra.get('spaceUUID', 0)
        if teamUUID not in self.teamDic:
            LOG_WARN("onEnterDungeonFailedSpaceNotFound::team not found", box, gbId, teamUUID, dungeonNo, spaceNo, extra)
            return

        _team = self.teamDic[teamUUID]
        _team.removeDungeonSpaceCache(dungeonNo, spaceNo, spaceUUID)

    def _enterTeamDungeon(self, box, gbId, teamUUID, dungeonNo, extraInfo):
        LOG_IFO("_enterTeamDungeon ", box, gbId, teamUUID, dungeonNo, extraInfo)
        src = extraInfo.get('src')
        _gmEnter = True if src and src.srcId == gameconst.DungeonSrcEnum.FROM_CLIENT_GM else False

        if teamUUID not in self.teamDic:
            LOG_IFO("_enterTeamDungeon ... teamUUID is existed !!!")
            return

        _team = self.teamDic[teamUUID]
        if not _team.checkDungeonNo(dungeonNo):
            if 'createAndEnter' in extraInfo:
                LOG_ERR('enterTeamDungeon::Create Team Dungeon Failed')
                return

            if _gmEnter:
                extraInfo.update({'createAndEnter': gbId})
                self.createTeamDungeon(box, gbId, dungeonNo, teamUUID, extraInfo)
                LOG_IFO('gm create and enter team dungeon: {}'.format(dungeonNo))
                return

            if _team.teamCaptainGbId != gbId:
                LOG_WARN('Captain must create dungeon first: {}-{}'.format(
                    teamUUID, dungeonNo))
                box.onMessagePre(MMD.datas.createDungeonCondition, [])
                return
            else:
                # check offline condition
                _offlinePLayersName = []
                for m in _team.teamPlayerDic.values():
                    if not m.playerBox:
                        _offlinePLayersName.append(m.playerName)
                if _offlinePLayersName:
                    LOG_WARN('some player offline', teamUUID, _offlinePLayersName)
                    box.onMessagePre(MMD.datas.dungeonTeamNearby, ['、'.join(_offlinePLayersName)])
                    return

                # captain auto create dungeon
                extraInfo.update({'createAndEnter': gbId})
                box.cell.doCheckTeamDungeonConditions(box, gbId, dungeonNo, teamUUID, extraInfo)
                return

        if self._isOutOfTeamDungeonRange(box, dungeonNo, teamUUID):
            LOG_ERR('team dungeon out of range', teamUUID, dungeonNo)
            # team dungeon is full
            return

        def _enterDirectly():
            extraInfo.update({'skipUseNeedItem': True,
                              'teamEnterCheckDic': {_gbId: 1 for _gbId in _team.teamPlayerDic}})
            self._enterTeamDungeonDirectly(box, gbId, teamUUID, dungeonNo, extraInfo)

        # gm enter
        if _gmEnter:
            _enterDirectly()
            return

        # need SelfItemCheck
        if (gbId in _team.teamDungeonDic[dungeonNo].founders
                and _team.teamDungeonDic[dungeonNo].founders[gbId].isEnter):
            if gameconst.DungeonTypeJudge.isBigWorldDungeon(self._getPrmBydungeonNo(dungeonNo, 'type')):
                LOG_WARN('player {} can\'t enter bigWorldDungeon {} again'.format(gbId, dungeonNo))
                # box.onMessagePre(MMD.datas.ERR_MESSAGE_NOT_FOUND, ['无法重新进入此组队世界副本'])
                box.onMessagePre(GP_S.datas["enterDunFailTeammateInDun"]["value"], [])
                return

            _enterDirectly()
            return

        extraInfo.setdefault("teamEnterCheckDic", {}).update({gbId: 1})
        box.selfCheckAndEnterTeamDungeon(teamUUID, dungeonNo, extraInfo)

    def onEnterTeamDungeon(self, box, gbId, teamUUID, dungeonNo, spaceNo):
        if teamUUID not in self.teamDic:
            return

        _team = self.teamDic[teamUUID]
        if not _team.isTeamDungeonCreated(dungeonNo):
            LOG_WARN("onEnterTeamDungeon:: team dungeon not created", teamUUID, dungeonNo, spaceNo)
            src = dungeonSrc.KickoutFromDungeon(kickReason=gameconst.DungeonSrcKickReason.FORCE)
            box.cell.selfLeaveTeamDungeon(src)
            return

        _team.onAvatarEnter(dungeonNo, spaceNo, gbId, box)

    def leaveTeamDungeon(self, box, gbId, teamUUID, dungeonNo):
        if teamUUID not in self.teamDic:
            return

        _team = self.teamDic[teamUUID]
        _team.onAvatarLeave(dungeonNo, gbId, isOffline=False)

        self._leaveTeam(box, teamUUID, gbId)
        isBigWorldDungeon = gameconst.DungeonTypeJudge.isBigWorldDungeon(
            DDL.datas[dungeonNo]['type'])

        if isBigWorldDungeon:
            # 大世界副本由于不能重新进入, 没有玩家后大世界副本本身没有存在的意义,
            # 可以直接销毁
            self._destroyTeamDungeonImme(teamUUID, dungeonNo)

    def onAvatarOffline(self, gbId, teamUUID, dungeonNo):
        if teamUUID not in self.teamDic:
            return

        _team = self.teamDic[teamUUID]
        _team.onAvatarLeave(dungeonNo, gbId, isOffline=True)

        isBigWorldDungeon = gameconst.DungeonTypeJudge.isBigWorldDungeon(
            DDL.datas[dungeonNo]['type'])

        if isBigWorldDungeon:
            # 大世界副本由于不能重新进入, 没有玩家后大世界副本本身没有存在的意义,
            # 可以直接销毁
            self._destroyTeamDungeonImme(teamUUID, dungeonNo)

    def _destroyTeamDungeonImme(self, teamUUID, dungeonNo):
        _team = self.teamDic[teamUUID]
        teamDungeonSpaceVal = _team.teamDungeonDic.get(dungeonNo)
        if not teamDungeonSpaceVal:
            return

        for gbId, founderVal in teamDungeonSpaceVal.founders.items():
            if founderVal.hasAvatar():
                break
        else:
            dungeonStub = gameengine.getDungeonStubByDungeonNo(
                dungeonNo, gameconst.DungeonEnterTypeEnum.TEAM)
            self._kickoutPlayer(teamUUID, dungeonNo)
            dungeonStub.destoryDungeonSpace(
                teamDungeonSpaceVal.spaceNo, teamDungeonSpaceVal.spaceUUID, 'noPlayer')

    def destroyTeamDungeonDelay(self, teamUUID, dungeonNo, spaceNo, reason, extra):
        LOG_IFO("destroyTeamDungeonDelay ", teamUUID, dungeonNo, spaceNo, reason, extra)
        if teamUUID not in self.teamDic:
            LOG_WARN("destroyTeamDungeonDelay:: team is not found", teamUUID, dungeonNo, spaceNo, reason, extra)
            return

        _team = self.teamDic[teamUUID]

        if dungeonNo not in _team.teamDungeonDic:
            LOG_WARN("destroyTeamDungeonDelay:: dungeon is not found", teamUUID, dungeonNo, spaceNo, reason, extra)
            return

        teamDungeonSpaceVal = _team.teamDungeonDic[dungeonNo]

        if teamDungeonSpaceVal.spaceNo != spaceNo:
            LOG_ERR('destroyTeamDungeonDelay::spaceNo not match, this: {}, got: {}'.format(
                teamDungeonSpaceVal.spaceNo, spaceNo))
            return

        dungeonStub = gameengine.getDungeonStubByDungeonNo(
            dungeonNo, gameconst.DungeonEnterTypeEnum.TEAM)

        dungeonTimeout = self._getPrmBydungeonNo(dungeonNo, 'timeOut')
        extra.update({'tTimeout': dungeonTimeout})
        checkBox, reason = teamDungeonSpaceVal.isDungeonSpaceCanBeDestoried(**extra)

        if checkBox:
            if reason == 'timeout':
                LOG_WARN('dungeon {} timeout({}), destroyed'.format(spaceNo, dungeonTimeout))
            elif reason == 'complete':
                LOG_WARN('dungeon {} already complete, destroyed'.format(spaceNo))
            elif reason == 'noPlayer':
                LOG_WARN('dungeon {} no players in dungeon, destroyed'.format(spaceNo))
            self._kickoutPlayer(teamUUID, dungeonNo)
            dungeonStub.destoryDungeonSpace(spaceNo, teamDungeonSpaceVal.spaceUUID, reason)
        else:
            if reason == 'timeout':
                LOG_WARN('dungeon {} will be timeout as 60s'.format(spaceNo))
                # _team.broadcastAllMembersClient('onMessage', [MMD.datas.ERR_MESSAGE_NOT_FOUND, '副本将在60s后超时, 请玩家尽快完成副本.'])

    def _kickoutPlayer(self, teamUUID, dungeonNo):
        if teamUUID not in self.teamDic:
            return

        _team = self.teamDic[teamUUID]
        founders = _team.teamDungeonDic.getDungeonCache(dungeonNo).founders
        _needDestoryGBIDs = []
        src = dungeonSrc.KickoutFromDungeon(kickReason=gameconst.DungeonSrcKickReason.TIMEOUT)
        for gbId, fVal in founders.items():
            base = fVal.playerBox
            if fVal.hasAvatar() and base and not utils.checkBoxOffline(base) and base.cell:
                base.cell.selfLeaveTeamDungeon(src)
            else:
                _needDestoryGBIDs.append(gbId)

        for i in _needDestoryGBIDs:
            founders.destoryFounder(i)

    def onDestroyTeamDungeon(self, teamUUID, dungeonNo, spaceNo, spaceUUID):
        LOG_IFO('onDestroyTeamDungeon:: {} {}'.format(teamUUID, dungeonNo), spaceNo, spaceUUID)
        _team = self.teamDic[teamUUID]
        _team.removeDungeonSpaceCache(dungeonNo, spaceNo, spaceUUID)
        self.teamDungeonFinished(teamUUID)

    def addTeamDungeonSpace(self, teamUUID, dungeonNo, spaceNo, spaceUUID):
        if teamUUID not in self.teamDic:
            return

        _team = self.teamDic[teamUUID]
        self._addTeamDungeonSpace(_team, dungeonNo, spaceNo, spaceUUID)

    def _addTeamDungeonSpace(self, _team, dungeonNo, spaceNo, spaceUUID):
        _team.addDungeonSpaceCache(dungeonNo, spaceNo, spaceUUID)

    def onTeammateBeConfirmedTimeout(self, box, gbId, teamUUID, dungeonNo, extra):
        LOG_IFO("onTeammateBeConfirmedTimeout::", box, gbId, teamUUID, dungeonNo, extra)
        if teamUUID not in self.teamDic:
            LOG_WARN("onTeammateBeConfirmedTimeout:: teamUUID not found", teamUUID, dungeonNo)
            return

        _team = self.teamDic[teamUUID]
        teamEnterCheckDic = extra.get('teamEnterCheckDic', {})
        reason = extra.get('reason', gameconst.TeammateConfirmFailedReason.REJECT)

        if reason == gameconst.TeammateConfirmFailedReason.TEAM_STATUS_CHANGE:
            pass
        else:
            _rejectPlayerNames = []
            for playerGBID, checkBox in teamEnterCheckDic.items():
                if not _team.isInTeam(playerGBID):
                    continue
                if checkBox == 0 or (reason == gameconst.TeammateConfirmFailedReason.TIMEOUT and checkBox != 1):
                    _rejectPlayerNames.append(_team.getPlayerName(playerGBID))

            if not _rejectPlayerNames:
                LOG_WARN("onTeammateBeConfirmedTimeout:: not reject name", teamUUID, dungeonNo, extra)
            _team.broadcastAllMembersBase('onMessagePre', [TDC_CFG.datas['enterRefusedMsg']['value'], ['、'.join(_rejectPlayerNames), ]])


class RaidMixin(object):

    def createRaidWithTeam(self, srcPlayerBox, srcPlayerGBID, teamUUID, raidUUID, capacity, extraProps):
        LOG_IFO('createRaidWithTeam::', srcPlayerBox, srcPlayerGBID, teamUUID, raidUUID, capacity, extraProps)
        if extraProps is None:
            extraProps = {}

        def _createRaid():
            if teamUUID not in self.teamDic:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_NOT_FOUND.initkvbody(source='createRaidWithTeam',
                                                                                teamId=teamUUID)

            if not dataUtils.isRaidCapacityValidate(capacity):
                return None, gameconst.RaidErrno.ENUM_RAID_UNKNOWN_CAPACITY.initkvbody(source='createRaidWithTeam')

            teamVal = self.teamDic[teamUUID]

            if capacity < len(teamVal.teamPlayerDic):
                return None, gameconst.RaidErrno.ENUM_RAID_CREATE_RAID_OFR.initkvbody(source='createRaidWithTeam',
                                                                                 teamId=teamUUID,
                                                                                 capacity=capacity)

            captainGBID, captainBox = srcPlayerGBID, srcPlayerBox

            if srcPlayerGBID != teamVal.getCaptainGbId():
                LOG_WARN('_createRaidGetMemberProps:: auto fix captain to new one')
                captainGBID = teamVal.getCaptainGbId()
                captainBox = teamVal.getCaptainBox()

            if not self.isCanDisbandTeam(teamUUID, captainGBID):
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_CANT_DISBAND.initkvbody(source='createRaidWithTeam',
                                                                                   teamId=teamUUID,
                                                                                   captainGBID=captainGBID,
                                                                                   srcPlayerGBID=srcPlayerGBID)

            memberDataList = []
            for memberVal in teamVal.teamPlayerDic.values():
                memberDataList.append(memberVal.toRaidTransDict())

            gameengine.getRaidStub(raidUUID).createRaid(
                captainBox, captainGBID, raidUUID, capacity, memberDataList, extraProps)

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
                LOG_IFO("addTeamMarkDataFromTeam::error", e)

            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, err = _createRaid()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('createRaidWithTeam:: failed, {}'.format(err))
            return

        self._disbandTeam(teamUUID)

    def applyJoinRaidWithTeam(self, srcPlayerBox, srcPlayerGBID, teamUUID, raidUUID, extraProps):
        LOG_IFO('applyJoinRaidWithTeam::', srcPlayerBox, srcPlayerGBID, teamUUID, raidUUID, extraProps)
        if extraProps is None:
            extraProps = {}

        memberDataList = []
        captainBox, captainGBID = srcPlayerBox, srcPlayerGBID
        def _applyJoinRaid():
            if teamUUID not in self.teamDic:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_NOT_FOUND

            teamVal = self.teamDic[teamUUID]
            if captainGBID != teamVal.getCaptainGbId():
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_TEAM_CAPTAIN

            lvLimit = UVVD.datas.get(RAID_CONST.datas["raidUIVisibleId"]["value"], {}).get('level', utils.getPlayerMaxLevel()+1)
            for memberVal in teamVal.teamPlayerDic.values():
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

        teamVal = self.teamDic[teamUUID]
        extraProps["siegeWarCamp"] = teamVal.siegeWarCamp
        gameengine.getRaidStub(raidUUID).applyJoinRaidWithTeam(
                captainBox, captainGBID, teamUUID, raidUUID, memberDataList, extraProps)


    def replyJoinRaidWithTeam(self, srcPlayerBox, srcPlayerGBID, raidUUID,
                              joinedPlayerGBID, teamUUID, joinMemberList, extraProps):
        LOG_IFO('replyJoinRaidWithTeam::', srcPlayerBox, srcPlayerGBID, raidUUID, joinedPlayerGBID,
                  teamUUID, joinMemberList, extraProps)
        if extraProps is None:
            extraProps = {}

        def _replyJoinRaid():
            if teamUUID not in self.teamDic:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_NOT_FOUND

            teamVal = self.teamDic[teamUUID]
            if joinedPlayerGBID != teamVal.getCaptainGbId():
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_TEAM_CAPTAIN

            memberGBIDSet = set(i['gbId'] for i in joinMemberList)
            if len(teamVal.teamPlayerDic) != len(memberGBIDSet):
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_NUM_NOT_MATCH

            for memberVal in teamVal.teamPlayerDic.values():
                if memberVal.playerGbId not in memberGBIDSet:
                    return None, gameconst.RaidErrno.ENUM_RAID_TEAM_MEMBER_NOT_MATCH

            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, err = _replyJoinRaid()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            err = err.initkvbody(source=_replyJoinRaid.__name__, teamId=teamUUID, raidUUID=raidUUID)
            LOG_ERR('replyJoinRaidWithTeam:: failed, {}'.format(err))

        gameengine.getRaidStub(raidUUID).onTeamReplyJoinRaidWithTeam(
            srcPlayerBox, srcPlayerGBID, raidUUID, joinedPlayerGBID, err, extraProps)

    def raidApplyInvitedRaid(self, raidTarget, srcPlayerBox, srcPlayerGBID, raidUUID, srcPlayerName,
                             raidLeaderGBID, raidLeaderName, invitedPlayerGBID, invitedPlayerName,
                             invitedTeamUUID, raidScore, raidLevel, extraProps):
        LOG_IFO("raidApplyInvitedRaid::", raidTarget, srcPlayerBox, srcPlayerGBID, raidUUID, 
                    srcPlayerName, raidLeaderGBID, raidLeaderName, invitedPlayerGBID, invitedPlayerName,
                    invitedTeamUUID, raidScore, raidLevel, extraProps)

        def _raidApplyInvitedRaid():
            if invitedTeamUUID not in self.teamDic:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_NOT_FOUND

            lvLimit = UVVD.datas.get(RAID_CONST.datas["raidUIVisibleId"]["value"], {}).get('level', utils.getPlayerMaxLevel()+1)
            teamVal = self.teamDic[invitedTeamUUID]
            for memberVal in teamVal.teamPlayerDic.values():
                if memberVal.raidUUID and memberVal.raidUUID != raidUUID:
                    return None, gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID
                if memberVal.level < lvLimit:
                    return None, gameconst.RaidErrno.ENUM_RAID_UI_DENIED

            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, _errno = _raidApplyInvitedRaid()
        if _errno != gameconst.RaidErrno.ENUM_RAID_OK:
            if _errno == gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID:
                LOG_WARN("raidApplyInvitedRaid:: some player already in raid", raidUUID)
                srcPlayerBox.onMessagePre(MMD.datas.raid_teamInvitationCheck_sectionTeam, [])
            elif _errno == gameconst.RaidErrno.ENUM_RAID_UI_DENIED:
                LOG_WARN("raidApplyInvitedRaid:: some player level check failed", raidUUID)
                srcPlayerBox.onMessagePre(RAID_CONST.datas["raidPartyInivte_underLevel_msg"]["value"], [])
            else:
                LOG_WARN(f"raidApplyInvitedRaid:: failed, errno={_errno}")
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [invitedPlayerGBID], 'invitedPlayerOnApplyInvitedRaid',
            (raidUUID, raidTarget, srcPlayerGBID, srcPlayerName, raidLeaderName, raidScore, raidLevel, extraProps),
            self, 'onPlayerIsOffline', (srcPlayerGBID, invitedPlayerName))

    def onReplyInviteRaidWithTeamFail(self, playerBox, playerGBID, raidId, srcPlayerGBID, teamId, errno, extra):
        LOG_IFO("onReplyInviteRaidWithTeamFail::", playerBox, playerGBID, raidId, srcPlayerGBID, teamId, errno, extra)
        if teamId not in self.teamDic:
            LOG_WARN('onReplyInviteRaidWithTeamFail:: teamId error', teamId)
            return
        teamVal = self.teamDic[teamId]
        errno = gameconst.RaidErrno._errno(errno)

        _offlinePlayerList = []
        if errno == gameconst.RaidErrno.ENUM_RAID_TEAM_MEMBER_OFFLINE:
            for gbId, teamPlayerVal in teamVal.teamPlayerDic.items():
                if not teamPlayerVal.bOnline:
                    _offlinePlayerList.append((gbId, teamPlayerVal.playerName))

        if _offlinePlayerList:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [srcPlayerGBID, ], 'onMessagePre',
                (MMD.datas.raid_applicantOffline, ['、'.join([i[1] for i in _offlinePlayerList])]),
                None, '', ())


class TeamStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer,
               DungeonStubMixin, RaidMixin):

    def __init__(self):
        super(TeamStub, self).__init__()
        self.teamDic = {}
        self.teamMarkMonsterRec = {}
        return

    def postReloadScript(self):
        super(TeamStub, self).postReloadScript()
        for v in self.teamDic.values():
            v.reloadScript()

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())

        return

    def onTimer(self, tid, userArg):
        self._onTimer(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)

    def getTeamByTeamId(self, teamId) -> team.TeamVal:
        if teamId not in self.teamDic:
            LOG_WARN('getTeamByTeamId teamId error', teamId)
            return
        teamVal = self.teamDic.get(teamId)
        return teamVal

    def notifyRemoveApplyInfo(self, teamId, gbId):
        team = self.getTeamByTeamId(teamId)
        if not team:
            return

        captainBox = team.getCaptainBox()
        if captainBox and captainBox.client:
            captainBox.client.onRemoveFromApplyList(gbId)
        self.addTimerCB(2, 'removeApplyJoinPlayer', (teamId, gbId), gametimer.TIMER_TAG_REMOVE_APPLY_JOIN_PLAYER)

    def removeApplyJoinPlayer(self, teamId, gbId):
        teamVal = self.getTeamByTeamId(teamId)
        if teamVal:
            teamVal.removeFromApplyDic(gbId)
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [gbId, ], 'onRemoveApplyJoinPlayer', (teamId, ), None, '', ())

    def addTeamMember(self, teamId, teamPlayerInfoDic):
        gbId = teamPlayerInfoDic['gbId']
        box = teamPlayerInfoDic['box']
        playerName = teamPlayerInfoDic['playerName']
        level = teamPlayerInfoDic['level']
        school = teamPlayerInfoDic['school']
        sex = teamPlayerInfoDic['sex']
        picFrameId = teamPlayerInfoDic['picFrameId']
        score = teamPlayerInfoDic['score']
        openId = teamPlayerInfoDic['openId']
        joinType = teamPlayerInfoDic['joinType']

        return self.teamDic[teamId].addMemberForStub(
            gbId, box, playerName, level, school, sex, picFrameId, score=score, openId=openId, joinType=joinType)

    def isCanCreateTeam(self, teamId):
        if teamId in self.teamDic:
            LOG_ERR('isCanCreateTeam', teamId, self.teamDic)
            return False
        return True

    def _createTeam(self, teamId, teamTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition, teamPlayerInfoDic):
        gbId = teamPlayerInfoDic['gbId']
        box = teamPlayerInfoDic['box']
        playerName = teamPlayerInfoDic['playerName']
        level = teamPlayerInfoDic['level']
        school = teamPlayerInfoDic['school']
        sex = teamPlayerInfoDic['sex']
        picFrameId = teamPlayerInfoDic['picFrameId']
        score = teamPlayerInfoDic['score']
        mountState = teamPlayerInfoDic['mountState']
        openId = teamPlayerInfoDic['openId']
        siegeWarCamp = teamPlayerInfoDic['siegeWarCamp']
        if gameconfig.isCrossServer() and siegeWarCamp != 0:
            teamTarget = gameconst.SIEGEWAR_PARE_ACTIVITY_ID
        teamVal = team.TeamVal(teamId, teamTarget, gbId, box, playerName, level, school, sex, picFrameId,
                                                 score=score, mountState=mountState, openId=openId, siegeWarCamp=siegeWarCamp)

        teamVal.teamMinLv = minLevel
        teamVal.teamMinScore = minScore
        teamVal.recruitInfo = recruitInfo
        teamVal.password = password
        teamVal.isAutoExpedition = isAutoExpedition
        teamVal.addMemberForStub(gbId, box, playerName, level, school, sex, picFrameId, True, score=score,
                          mountState=0, isDead=False, openId=openId, joinType = gameconst.TeamJoinType.CREATE)

        self.teamDic[teamId] = teamVal

        # 没有密码的属于公开
        if len(teamVal.password) == 0:
            teamVal.isPublish = True
            # 自由组队目标大于2，才进匹配队列
            if teamVal.teamTarget > gameconst.PARE_ACTIVITY_ID:
                self.teamPrepareAutoMatch(teamId, teamPlayerInfoDic.get('guildUUID', 0))

        # 定时启动自动检查是否自动开始
        self.checkAutoStart(teamId)

        LOG_IFO('_createTeam', self.teamDic)

    def createTeam(self, box, teamId, teamTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition, teamPlayerInfoDic):
        LOG_IFO('createTeam', teamId, teamTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition, teamPlayerInfoDic)
        if not self.isCanCreateTeam(teamId):
            box and box.cell and box.cell.resetTryAddTeamCD()
        else:
            self._createTeam(teamId, teamTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition, teamPlayerInfoDic)

    def checkAutoStart(self, teamID):
        teamVal = self.teamDic.get(teamID)
        if not teamVal:
            return

        if teamVal.autoStartTimer > 0:
            self.cancelTimerCB(teamVal.autoStartTimer, gametimer.TIMER_TAG_TEAM_AUTO_START)
            teamVal.autoStartTimer = 0

        if teamVal.isAutoExpedition and teamVal.teamTarget > gameconst.PARE_ACTIVITY_ID:
            if teamVal.isTeamFull():
                captainBox = teamVal.getCaptainBox()
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
            box.client and box.client.onApplyJoinTeamFailed(gameconst.TeamApplyResult.TEAM_APPLY_IS_IN_DUNGEON, teamVal.teamId, teamVal.teamMinLv, teamVal.teamMinScore, teamVal.password, applySource)
            return False
        if teamVal.isTeamFull():
            if box.client:
                box.onMessagePre(TMMCD.datas['teamFullMsg']['value'], [])
            return False
        if teamVal.isApplyJoinPlysFull():
            if box.client:
                box.onMessagePre(TMMCD.datas['applyFullMsg']['value'], [])
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
                    box.onMessagePre(MMD.datas.teamMatch_differentFactions, [])
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
                box.onMessagePre(TMMCD.datas['teamFullMsg']['value'], [])
            return False
        if not teamVal.isInApplyJoinDic(gbId):
            LOG_WARN('isCanJoinTeam not in applyJoinDic', teamId, gbId, teamVal.applyJoinDic)
            if box and box.client:
                box.onMessagePre(TMMCD.datas['cancelApplication']['value'], [])
            return False
        return True

    def _applyJoinTeam(self, teamId, teamPlayerInfoDic, applySource):
        LOG_IFO('_applyJoinTeam', teamId, teamPlayerInfoDic, applySource)
        teamVal = self.getTeamByTeamId(teamId)
        captainGbId = teamVal.getCaptainGbId()

        gbId = teamPlayerInfoDic['gbId']
        box = teamPlayerInfoDic['box']
        if gbId in teamVal.applyJoinDic:
            if box.client:
                box.onMessagePre(TMMCD.datas['isAppliedMsg']['value'], [])
            return

        level = teamPlayerInfoDic['level']
        score = teamPlayerInfoDic['score']

        playerName = teamPlayerInfoDic['playerName']
        school = teamPlayerInfoDic['school']
        sex = teamPlayerInfoDic['sex']
        score = teamPlayerInfoDic['score']

        teamVal.addApplyJoinPlayer(gbId, playerName, level, school, sex, applySource, score=score)

        box.cell.onApplyJoinTeam(teamId, teamVal.teamCaptainGbId)

        captainBox = teamVal.getCaptainBox()
        if captainBox and not utils.checkBoxOffline(captainBox) and captainBox.cell:
            teamVal.getCaptainBox().cell.procJoinTeamMsg(gbId, playerName, level, school, sex, score)

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
        LOG_IFO('replyJoinTeam', captainGbId, teamId, gbId, bAgree)
        if not bAgree:
            # 发送拒绝申请加入的信息
            self.removeApplyJoinPlayer(teamId, gbId)
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([gbId], 'onMessagePre',
                                                                  (TMMCD.datas['applyCaptainDeniedMsg']['value'], []), None, '', ())
            return

        if not self.isCanJoinTeam(box, teamId, gbId):
            LOG_IFO('isCanJoinTeam fail', captainGbId, teamId, gbId, bAgree)
            box and box.cell and box.cell.resetTryAddTeamCD()
        else:
            team = self.getTeamByTeamId(teamId)
            jVal = team.getApplyJoinPlayerInfo(gbId)
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell([gbId], 'onReplyJoinTeam',
                                                                  (captainGbId, teamId, gbId, jVal.playerName,
                                                                   jVal.level, jVal.school, jVal.applySource), self, 'onPlayerIsOffline',
                                                                  (captainGbId, jVal.playerName))
        self.removeApplyJoinPlayer(teamId, gbId)

    def clearApplyJoinDic(self, box, gbId, teamId):
        teamVal = self.getTeamByTeamId(teamId)
        if gbId != teamVal.getCaptainGbId():
            LOG_ERR('clearApplyJoinDic error, is not captain', gbId, teamVal.getCaptainGbId())
            return False

        teamVal.clearApplyJoinDic()

    def onPlayerIsOffline(self, offlineGbId, gbId, name):
        LOG_IFO('onPlayerIsOffline', offlineGbId, gbId, name)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([gbId], 'onMessagePre', (54000108, [name]), None, '', ())

    def isCanDisbandTeam(self, teamId, gbId):
        if teamId not in self.teamDic:
            LOG_ERR('isCanDisbandTeam teamId error', teamId, gbId)
            return False

        teamVal = self.teamDic.get(teamId)
        if gbId != teamVal.teamCaptainGbId:
            LOG_ERR('isCanDisbandTeam gbId error', teamId, gbId)
            return False

        return True

    def _disbandTeam(self, teamId):
        teamVal = self.getTeamByTeamId(teamId)
        LOG_IFO('_disbandTeam:', teamId, teamVal.teamPlayerDic.keys())
        for gbId, teamPlayerVal in teamVal.teamPlayerDic.items():
            box = teamPlayerVal.playerBox
            if box and box.cell:
                box.cell.onTeamDisband(True)
            if box and box.client:
                box.onMessagePre(TMMCD.datas['teamDisbandMsg']['value'], [])

        if teamVal.teamAutoMatchTime > 0:
            teamVal.teamAutoMatchTime = 0
            gameengine.getGlobalBase('TeamMatchStub').teamStopAutoMatch(teamId)

        if teamVal.captainOfflineTimer > 0:
            self.cancelTimerCB(teamVal.captainOfflineTimer, gametimer.TIMER_TAG_CAPTAIN_OFFLINE)
            teamVal.captainOfflineTimer = 0

        try:
            teamVal.clearMarkRecord(self)
        except Exception as e:
            LOG_ERR('doDisbandTeam:: clearMarkRecord exception: {}'.format(e))

        self.teamDic.pop(teamId)

        for dungeonNo, dunVal in teamVal.teamDungeonDic.items():
            stub = gameengine.getDungeonStubBySpaceNo(dunVal.spaceNo)
            stub.completeTeamDungeon(dunVal.spaceNo, teamId, False, 0, gameconst.DunegonCompleteReasonType.LEAVE)
            LOG_WARN('doDisbandTeam:: _disbandTeam and complete dungeon in force ', dungeonNo, dunVal)
        return True

    def disbandTeam(self, box, gbId, teamId):
        if self.isCanDisbandTeam(teamId, gbId):
            self._disbandTeam(teamId)

        # todo 自动匹配列表中删除

    def teamDungeonFinished(self, teamId):
        self._disbandTeam(teamId)

    def isCanInviteTeam(self, box, srcTeamId, srcPlayerGbId, invitedPlayerGbId, datas):
        teamVal = self.teamDic.get(srcTeamId)
        if not teamVal:
            LOG_WARN('isCanInviteTeam teamId error', srcTeamId, srcPlayerGbId)
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([invitedPlayerGbId], 'onMessagePre',
                                      (TMMCD.datas['teamDisbandMsg']['value'], []), None, '', ())
            return False
        
        if teamVal.teamTarget > gameconst.PARE_ACTIVITY_ID:
            isTeamUIVisibleId = datas.get('isTeamUIVisibleId', True)
            isTeamDungeonUIVisibleId = datas.get('isTeamDungeonUIVisibleId', True)
            if not isTeamUIVisibleId:
                box.CheckFuncConditions(dataUtils.getRaidConstDataValue("teamUIVisibleId"))
                return False
            if not isTeamDungeonUIVisibleId:
                box.CheckFuncConditions(dataUtils.getRaidConstDataValue("teamDungeonUIVisibleId"))
                return False
        if teamVal.isTeamFull():
            box.onMessagePre(TMMCD.datas['teamFullMsg']['value'], [])
            return False
        
        return True

    def _applyInviteTeam(self, srcTeamId, srcPlayerGbId, srcLevel, srcSchool, invitedPlayerGbId, name):
        teamVal = self.getTeamByTeamId(srcTeamId)
        captainGbId = teamVal.getCaptainGbId()
        isDirect = False
        if captainGbId == srcPlayerGbId and teamVal.isInApplyJoinDic(invitedPlayerGbId):
            teamVal.removeFromApplyDic(invitedPlayerGbId)
            isDirect = True
        captainName = teamVal.getPlayerName(captainGbId)
        srcPlayerName = teamVal.getPlayerName(srcPlayerGbId)
        gameengine.getGlobalBase('PlayerStub').doOnOthersCell([invitedPlayerGbId], 'procInviteTeamMsg', (
            srcTeamId, teamVal.teamTarget, srcPlayerGbId, srcPlayerName, captainName, srcLevel, srcSchool, teamVal.teamMinScore, teamVal.teamMinLv, isDirect), self, 'onPlayerIsOffline', (srcPlayerGbId, name))

    def applyInviteTeam(self, box, srcTeamId, srcPlayerGbId, srcLevel, srcSchool, invitedPlayerGbId, name, datas):
        if self.isCanInviteTeam(box, srcTeamId, srcPlayerGbId, invitedPlayerGbId, datas):
            self._applyInviteTeam(srcTeamId, srcPlayerGbId, srcLevel, srcSchool, invitedPlayerGbId, name)

    def replyInviteTeam(self, srcTeamId, srcPlayerGbId, teamPlayerInfoDic):
        invitedPlayerGbId = teamPlayerInfoDic['gbId']
        box = teamPlayerInfoDic['box']

        if not self.isCanInviteTeam(box, srcTeamId, srcPlayerGbId, invitedPlayerGbId, {}):
            box and box.cell and box.cell.resetTryAddTeamCD()
        else:
            teamVal = self.getTeamByTeamId(srcTeamId)
            if srcPlayerGbId == teamVal.getCaptainGbId():
                self.addTeamMember(srcTeamId, teamPlayerInfoDic)
            else:
                self.applyJoinTeam(srcTeamId, '', teamPlayerInfoDic, True, gameconst.ApplySource.RECRUIT, {})

    def isCanLeaveTeam(self, teamId, gbId):
        if not teamId:
            LOG_ERR('isCanLeaveTeam teamId param err', teamId, gbId)
            return False
        if teamId not in self.teamDic:
            LOG_WARN('isCanLeaveTeam teamId error', teamId, gbId)
            return False
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal.isInTeam(gbId):
            LOG_WARN("isCanLeaveTeam:: player not found in team", teamId, gbId)
            return False
        return True

    def _leaveTeam(self, leaveBox, teamId, gbId, notifySelf=True):
        LOG_IFO('_leaveTeam', leaveBox, teamId, gbId, notifySelf)
        teamVal = self.getTeamByTeamId(teamId)
        if len(teamVal.teamPlayerDic) < 1:
            if not teamVal.isInDungeon:
                self._disbandTeam(teamId)
        if not teamVal.isInTeam(gbId):
            LOG_WARN("_leaveTeam:: player not found in team", teamId, gbId)
            return
        leavePlayerName = teamVal.getPlayerName(gbId)
        teamVal.delMember(gbId, notifySelf)
        teamVal.broadcastAllMembersBase('onMessagePre',
                                          [TMMCD.datas['teamChannel_initiativeLeaveTeamMsg']['value'], [leavePlayerName, str(gbId)]])
        if gbId == teamVal.getCaptainGbId():
            ranCaptainId = teamVal.getRandomCaptainGbId()
            if ranCaptainId != -1:
                teamVal.setCaptainGbId(ranCaptainId)
                box = teamVal.getPlayerBox(ranCaptainId)
                if box and not utils.checkBoxOffline(box) and box.client:
                    box.onMessagePre(TMMCD.datas['beCaptainMsg']['value'], [])
            elif len(teamVal.teamPlayerDic) < 1:
                if not teamVal.isInDungeon:
                    self._disbandTeam(teamId)

    def leaveTeam(self, spaceNo, box, teamId, gbId, notifySelf=True):
        LOG_IFO('leaveTeam', spaceNo, teamId, gbId, notifySelf)
        if not self.isCanLeaveTeam(teamId, gbId):
            return

        self._leaveTeam(box, teamId, gbId, notifySelf)

    def isCanKickTeamMember(self, teamId, gbId, kickGbId):
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal:
            return False
        if not teamVal.isInTeam(gbId):
            return False
        if teamVal.getCaptainGbId() != gbId:
            return False
        return True

    def _kickTeamMember(self, teamId, kickGbId, isMemOffline=False):
        LOG_IFO('_kickTeamMember', teamId, kickGbId, isMemOffline)
        teamVal = self.getTeamByTeamId(teamId)
        kickPlayerName = teamVal.getPlayerName(kickGbId)
        teamVal.delMember(kickGbId)
        if isMemOffline:
            msgId = TMMCD.datas['teamChannel_initiativeLeaveTeamMsg']['value']
        else:
            msgId = TMMCD.datas['teamChannel_kickedMsg']['value']
        teamVal.broadcastAllMembersBase('onMessagePre',  [msgId, [kickPlayerName, str(kickGbId)]])

    def kickTeamMember(self, box, teamId, gbId, kickGbId, isMemOffline):
        if not self.isCanKickTeamMember(teamId, gbId, kickGbId):
            return
        self._kickTeamMember(teamId, kickGbId, isMemOffline=isMemOffline)
        if not isMemOffline:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([kickGbId], 'onMessagePre',
                                      (TMMCD.datas['kickFromTeamMsg']['value'], []), None, '', ())

    def isCanTransferCaptain(self, box, teamId, gbId, transferGbId):
        teamVal = self.getTeamByTeamId(teamId)
        if gbId != teamVal.getCaptainGbId():
            LOG_ERR('isCanTransferCaptain error', gbId, teamVal.getCaptainGbId())
            return False

        if not teamVal.isInTeam(transferGbId):
            LOG_IFO('isCanTransferCaptain not in team', transferGbId, teamId)
            return False

        if not teamVal.isTeamMemOnline(transferGbId):
            box.onMessagePre(MMD.datas.approveCaptainOffline , [])
            return False

        return True

    def _transferCaptain(self, teamId, transferGbId):
        teamVal = self.getTeamByTeamId(teamId)
        teamVal.setCaptainGbId(transferGbId)
        return teamVal

    def transferCaptain(self, box, teamId, gbId, transferGbId):
        ret = True
        if not self.isCanTransferCaptain(box, teamId, gbId, transferGbId):
            ret = False

        if not ret:
            return

        teamVal = self._transferCaptain(teamId, transferGbId)
        teamVal.broadcastAllMembersCell('onTransferCaptain', (gbId, transferGbId))
        if teamVal.captainOfflineTimer > 0:
            self.cancelTimerCB(teamVal.captainOfflineTimer, gametimer.TIMER_TAG_CAPTAIN_OFFLINE)
            teamVal.captainOfflineTimer = 0
        if not teamVal.isTeamMemOnline(transferGbId):
            teamVal.captainOfflineTimer = self.addTimerCB(TMMCD.datas["team_TLDownGradeOfflineTime"]["value"], '_onCaptainOffline', (teamId, transferGbId, ), gametimer.TIMER_TAG_CAPTAIN_OFFLINE)

    def isCanApplyBecomeCaptain(self, teamId, gbId):
        teamVal = self.getTeamByTeamId(teamId)
        if gbId == teamVal.getCaptainGbId():
            LOG_ERR('isCanApplyBecomeCaptain captainGbId error:', gbId, teamVal.getCaptainGbId())
            return False

        if not teamVal.isInTeam(gbId):
            return False

        return True

    def _applyBecomeCaptain(self, teamId, gbId, captainGbId, name):
        gameengine.getGlobalBase('PlayerStub').doOnOthersCell([captainGbId], 'procBecomeCaptainMsg',
                                                              (teamId, gbId, name), None, '', ())
        teamVal = self.getTeamByTeamId(teamId)
        if teamVal:
            teamVal.broadcastAllMembersBase('onMessagePre',
                                            [TMMCD.datas['teamChannel_applyCaptainMsg']['value'],
                                             [teamVal.getPlayerName(gbId), teamVal.getPlayerName(captainGbId), str(gbId), str(captainGbId)]])

    def applyBecomeCaptain(self, box, teamId, gbId, captainGbId, name):
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal:
            return

        if not self.isCanApplyBecomeCaptain(teamId, gbId):
            return
        self._applyBecomeCaptain(teamId, gbId, teamVal.getCaptainGbId(), name)
        return

    def _becomeCaptain(self, teamId, becomeGbId):
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal:
            return None
        if not teamVal.isInTeam(becomeGbId):
            return None
        teamVal.setCaptainGbId(becomeGbId)
        return teamVal

    def replyBecomeCaptain(self, box, teamId, gbId, becomeGbId):
        teamVal = self._becomeCaptain(teamId, becomeGbId)
        if not teamVal:
            return
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([becomeGbId], 'onMessagePre',
                                                  (TMMCD.datas['beCaptainMsg']['value'], []), None, '', ())
        if teamVal.captainOfflineTimer > 0:
            self.cancelTimerCB(teamVal.captainOfflineTimer, gametimer.TIMER_TAG_CAPTAIN_OFFLINE)
            teamVal.captainOfflineTimer = 0
        if not teamVal.isTeamMemOnline(becomeGbId):
            teamVal.captainOfflineTimer = self.addTimerCB(TMMCD.datas["team_TLDownGradeOfflineTime"]["value"], '_onCaptainOffline', (teamId, becomeGbId, ), gametimer.TIMER_TAG_CAPTAIN_OFFLINE)

    def cancelTeamJoinRequest(self, box, gbId, teamId):
        LOG_IFO("cancelTeamJoinRequest::", box, gbId, teamId)
        self.removeApplyJoinPlayer(teamId, gbId)

    def getTeamInfoOnLogin(self, box, gbId, teamId):
        teamVal = self.getTeamByTeamId(teamId)

        if teamVal:
            if not teamVal.isInTeam(gbId):
                box.cell.onLeaveTeam()
            else:
                self.updateOnlineState(box, teamId, gbId, True)
                box.cell.onAddTeamCell(teamVal)
        else:
            box.cell.onTeamDisband(False)

    def notifyPlayerLogon(self, box, gbId, teamId, isRelogin):
        teamVal = self.getTeamByTeamId(teamId)

        if not teamVal:
            return

        if teamVal.isInTeam(gbId):
            box.client.onAddTeam(teamVal.getClientData())

        if teamVal.teamCaptainGbId == gbId:
            teamVal.notifyApplyJoinInfo(gbId)

        teamVal.getCaptainBox().cell.notifyTeamMemberLogon(box, gbId, teamId, isRelogin)

    def logonEnterLine(self, lineType, box, gbId, teamId, extra):
        self.notifyPlayerLogon(box, gbId, teamId, False)

        teamVal = self.getTeamByTeamId(teamId)
        if teamVal and teamVal.isInTeam(gbId):
            extra['teamUUID'] = teamId
            extra['isLeader'] = teamVal.getCaptainGbId() == gbId

        gameengine.getLineStub(lineType).autoSwitchLine(box, gbId, 0, extra, 'onLogonGetLineNo', (lineType, extra))

    def logonEnterMyHome(self, box, gbId, teamId, extra):
        self.notifyPlayerLogon(box, gbId, teamId, False)

        teamVal = self.getTeamByTeamId(teamId)
        if teamVal and teamVal.isInTeam(gbId):
            extra['teamUUID'] = teamId
            extra['isLeader'] = teamVal.getCaptainGbId() == gbId

        gameengine.getGlobalBase('HomeStub').doApplyEnterPlayerHome(box, gbId, gbId, 0, gameconst.MapIdDef.mapMyHome, extra)

    def logonEnterGuildSpace(self, box, gbId, teamId, guildUUID, extra):
        self.notifyPlayerLogon(box, gbId, teamId, False)

        teamVal = self.getTeamByTeamId(teamId)
        if teamVal and teamVal.isInTeam(gbId):
            extra['teamUUID'] = teamId
            extra['isLeader'] = teamVal.getCaptainGbId() == gbId

        gameengine.getGlobalBase('GuildStub').logonEnterGuildSpace(gbId, box, guildUUID, extra)

    def askAllMemberFollow(self, box, teamId, gbId, spaceNo, pos):
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal:
            LOG_ERR("askAllMemberFollow team not found", teamId, gbId)
            return

        if gbId != teamVal.getCaptainGbId():
            LOG_ERR('askAllMemberFollow not captain', teamId, gbId)
            return

        teamVal.askAllMemberFollow(spaceNo, pos)

    def updateMemberAttr(self, box, teamId, gbId, attrDic):
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal or not teamVal.isInTeam(gbId):
            LOG_WARN('updateMemberAttr not in team', gbId)
            return

        teamVal.updateMemberAttr(gbId, attrDic)

    def updateMemberVolatileAttr(self, teamId, gbId, attrDic):
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal:
            return
        teamVal.updateMemberVolatileAttr(gbId, attrDic)

    def _onCaptainOffline(self, teamId, gbId):
            LOG_IFO('_onCaptainOffline::', teamId, gbId)
            teamVal = self.getTeamByTeamId(teamId)
            if not teamVal or not teamVal.isInTeam(gbId):
                LOG_WARN('_onCaptainOffline not in team', gbId)
                return

            if teamVal.captainOfflineTimer > 0:
                self.cancelTimerCB(teamVal.captainOfflineTimer, gametimer.TIMER_TAG_CAPTAIN_OFFLINE)
                teamVal.captainOfflineTimer = 0

            if gbId != teamVal.getCaptainGbId():
                LOG_WARN('_onCaptainOffline:: failed', teamId, gbId, teamVal.getCaptainGbId())
                return

            if teamVal.isTeamMemOnline(gbId):
                return

            if teamVal.isAllMembersOffline():
                self._disbandTeam(teamId)
            else:
                ranCaptainId = teamVal.getRandomCaptainGbId()
                teamVal.setCaptainGbId(ranCaptainId)
                box = teamVal.getPlayerBox(ranCaptainId)
                if box and box.client:
                    box.onMessagePre(TMMCD.datas['beCaptainMsg']['value'], [])

    def updateOnlineState(self, box, teamId, gbId, bOnline):
        LOG_IFO('updateOnlineState', box, teamId, gbId, bOnline)
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal or not teamVal.isInTeam(gbId):
            LOG_WARN('updateOnlineState not in team', gbId)
            return

        teamVal.updateMemberOnlineState(gbId, bOnline, box)
        if gbId == teamVal.getCaptainGbId():
            if teamVal.captainOfflineTimer > 0:
                self.cancelTimerCB(teamVal.captainOfflineTimer, gametimer.TIMER_TAG_CAPTAIN_OFFLINE)
                teamVal.captainOfflineTimer = 0
            if not bOnline:
                teamVal.captainOfflineTimer = self.addTimerCB(TMMCD.datas["team_TLDownGradeOfflineTime"]["value"], '_onCaptainOffline', (teamId, gbId, ), gametimer.TIMER_TAG_CAPTAIN_OFFLINE)

    def sendChatMsgFromTeamMember(self, teamId, gbId, avatarInfo, msg):
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal or not teamVal.isInTeam(gbId):
            return

        teamVal.broadcastAllMembersBase( 'onRecvChannelMsg', (gameconst.ChatChannelEnum.TEAM, avatarInfo, msg), (gbId,))

    def getTeamMemberInfo(self, box, teamId, method, args):
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal:
            return
        levels = []
        for ranGbId, teamPlayerVal in teamVal.teamPlayerDic.items():
            levels.append(teamPlayerVal.level)
        info = {'teamId':teamId, 'levels':levels}
        getattr(box, method)(info, *args)

    def challengeDunNotifyMsg(self, teamId, msgId, gbIds):
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal:
            return

        names = []
        for gbId in gbIds:
            names.append(teamVal.getPlayerName(gbId))

        if names:
            nameStr = '.'.join(names)
            teamVal.broadcastAllMembersBase(
                'onMessagePre',
                (
                    msgId,
                    [nameStr]
                )
            )

    def teamPrepareAutoMatch(self, teamId, guildUUID):
        LOG_IFO('in teamPrepareAutoMatch:', teamId, guildUUID)
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal:
            return
        if not teamVal.checkTeamTarget(teamVal.teamMinLv, teamVal.teamMinScore):
            return
        if teamVal.isTeamFull():
            LOG_WARN('   in teamPrepareAutoMatch, team full:', teamId)
            teamVal.getCaptainBox().onMessagePre(TMMCD.datas['teamMatch_fullMsg']['value'], [])
            return
        teamVal.startAutoMatch(guildUUID)

    def teamPrepareStopAutoMatch(self, teamId):
        LOG_IFO('in teamPrepareStopAutoMatch:', teamId)
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal:
            return
        teamVal.stopAutoMatch()

    def newPlayerMatched(self, teamId, newPlayerDic):
        teamVal = self.getTeamByTeamId(teamId)
        LOG_IFO('in newPlayerMatched:', teamId, newPlayerDic, teamVal)
        if not teamVal:
            return
        newPlayerDic['joinType'] = gameconst.TeamJoinType.MATCH
        self.addTeamMember(teamId, newPlayerDic)
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
        self.teamPrepareStopAutoMatch(teamId)
        if teamVal.isPublish and teamVal.teamTarget > gameconst.PARE_ACTIVITY_ID:
            self.teamPrepareAutoMatch(teamId, guildUUID)

        self.checkAutoStart(teamId)

    def getTeamInfo(self, box, teamId):
        pass

    def getTeamList(self, box, teamTarget, checkTime, checkTeamstubNum, sendTeamNum, startTeamStubIndex):
        LOG_IFO('in getTeamList:', teamTarget, checkTime, checkTeamstubNum, sendTeamNum, startTeamStubIndex)
        teamList = []
        # 根据队伍的创建时间排序，最晚创建的队伍在最前面
        releaseNum = gameconst.TEAM_LIST_MAX_NUM - sendTeamNum
        sortedDic = sorted(self.teamDic.items(), key=lambda x: x[1].tCreated, reverse=True)
        for teamId, teamVal in sortedDic:
            if len(teamList) >= releaseNum:
                break
            if teamVal.teamTarget != teamTarget:
                continue
            if teamVal.isTeamFull():
                continue
            if teamVal.isAllMembersOffline():
                continue
            if self.checkInDungeon(teamId):
                continue
            teamList.append(teamVal.getClientData())
        box.client.onGetTeamList(checkTime, teamTarget, teamList)
        checkTeamstubNum += 1
        sendTeamNum += len(teamList)
        if checkTeamstubNum >= gameconst.TEAMSTUB_CONFIG_NUM:
            box.cell.onGetTeamListFinished(checkTeamstubNum-1, teamTarget)
            return
        if sendTeamNum >= gameconst.TEAM_LIST_MAX_NUM:
            box.cell.onGetTeamListFinished(checkTeamstubNum-1, teamTarget)
            return
        gameengine.getTeamStub(startTeamStubIndex+checkTeamstubNum).getTeamList(box, teamTarget, checkTime,
                                                                       checkTeamstubNum, sendTeamNum, startTeamStubIndex)
        return

    def killMonster(self, teamId, spaceNo, monsterId, monsterUID, killerGBID):
        LOG_IFO('huyf: killMonster', teamId, spaceNo, monsterId, monsterUID, killerGBID)
        # teamVal = self.getTeamByTeamId(teamId)
        # if not teamVal:
        #     LOG_WARN('not find teamVal', teamId)
        #     return
        #
        # for gbId, teamPlayerVal in teamVal.teamPlayerDic.items():
        #     box = teamPlayerVal.playerBox
        #     if not teamPlayerVal.bOnline:
        #         continue
        #     #if not formula.isGuildSpace(teamPlayerVal.spaceNo):
        #     #   continue
        #     if box:
        #         box.onTaskKillMonster(spaceNo, monsterId, monsterUID, killerGBID)
        #         break
        # teamVal.checkKillGuildLeaderMirror(spaceNo, monsterId)
        return

    def updateTeamSilentFlag(self, teamId, isSilent):
        LOG_IFO('updateTeamSilentFlag:', teamId, isSilent)
        teamVal = self.getTeamByTeamId(teamId)
        if not teamId:
            LOG_WARN('not found teamVal:', teamId)
            return
        teamVal.setSilentFlag(bool(isSilent))
        return

    def sendTeamMemberMessage(self,teamId,messageId,messageArgs):
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal :
            return

        teamVal.sendTeamMemberMessage(messageId,messageArgs)

    def sendTeamMemberMessage_localCross(self,teamId, messageId, messageArgs):
        teamVal = self.getTeamByTeamId(teamId)
        if not teamVal :
            return

        teamVal.sendTeamMemberMessage(messageId,messageArgs, localCross=True)

    # --------------------------------------------------------------------
    # TEAM MICS
    def switchTeamMicsMode(self, srcPlayerBox, srcPlayerGBID, teamId, mode, extraProps):
        LOG_IFO("switchTeamMicsMode::", srcPlayerBox, srcPlayerGBID, teamId, mode, extraProps)
        teamVal, err = self._switchTeamMicsMode(srcPlayerBox, srcPlayerGBID, teamId, mode, extraProps)
        if err:
            LOG_WARN('switchTeamMicsMode:: failed, {}'.format(err))
            return

        teamVal.getAllTeamMemberMiscStatus(toClient=True)

    def _switchTeamMicsMode(self, srcPlayerBox, srcPlayerGBID, teamId, mode, extraProps):
        if teamId not in self.teamDic:
            return None, "TEAM_ID_NOT_FOUND"

        teamVal = self.teamDic[teamId]
        return teamVal.switchTeamMiscMode(srcPlayerGBID, mode, extraProps, toClient=True)

    def turnOnTeamMics(self, srcPlayerBox, srcPlayerGBID, teamId, playerGBID, extraProps):
        LOG_IFO("turnOnTeamMics::", srcPlayerBox, srcPlayerGBID, teamId, playerGBID, extraProps)
        _, err = self._turnOnTeamMics(srcPlayerBox, srcPlayerGBID, teamId, playerGBID)
        if err:
            LOG_WARN('turnOnTeamMics:: failed, {}'.format(err))

    def _turnOnTeamMics(self, srcPlayerBox, srcPlayerGBID, teamId, playerGBID):
        if teamId not in self.teamDic:
            return None, "TEAM_ID_NOT_FOUND"

        teamVal = self.teamDic[teamId]
        return teamVal.turnOnTeamMemberMics(srcPlayerGBID, playerGBID, toClient=True)

    def turnOffTeamMics(self, srcPlayerBox, srcPlayerGBID, teamId, playerGBID, extraProps):
        LOG_IFO("turnOffTeamMics::", srcPlayerBox, srcPlayerGBID, teamId, playerGBID, extraProps)
        _, err = self._turnOffTeamMics(srcPlayerBox, srcPlayerGBID, teamId, playerGBID)
        if err:
            LOG_WARN('turnOffTeamMics:: failed, {}'.format(err))

    def _turnOffTeamMics(self, srcPlayerBox, srcPlayerGBID, teamId, playerGBID):
        if teamId not in self.teamDic:
            return None, "TEAM_ID_NOT_FOUND"

        teamVal = self.teamDic[teamId]
        return teamVal.turnOffTeamMemberMics(srcPlayerGBID, playerGBID, blockMics=False, toClient=True)

    def blockTeamMemberMics(self, srcPlayerBox, srcPlayerGBID, teamId, playerGBID, extraProps):
        LOG_IFO("blockTeamMemberMics::", srcPlayerBox, srcPlayerGBID, teamId, playerGBID, extraProps)
        _, err = self._blockTeamMemberMics(srcPlayerBox, srcPlayerGBID, teamId, playerGBID)
        if err:
            LOG_WARN('blockTeamMemberMics:: failed, {}'.format(err))

    def _blockTeamMemberMics(self, srcPlayerBox, srcPlayerGBID, teamId, playerGBID):
        if teamId not in self.teamDic:
            return None, "TEAM_ID_NOT_FOUND"

        teamVal = self.teamDic[teamId]
        return teamVal.turnOffTeamMemberMics(srcPlayerGBID, playerGBID, blockMics=True, toClient=True)

    def unblockTeamMemberMics(self, srcPlayerBox, srcPlayerGBID, teamId, playerGBID, extraProps):
        LOG_IFO("unblockTeamMemberMics::", srcPlayerBox, srcPlayerGBID, teamId, playerGBID, extraProps)
        _, err = self._unblockTeamMemberMics(srcPlayerBox, srcPlayerGBID, teamId, playerGBID)
        if err:
            LOG_WARN('unblockTeamMemberMics:: failed, {}'.format(err))
            if err == 'TEAM_ALL_MISC_BLOCKED':
                srcPlayerBox.onMessagePre(MMD.datas.voiceChat_allMicBanned, [])

    def _unblockTeamMemberMics(self, srcPlayerBox, srcPlayerGBID, teamId, playerGBID):
        if teamId not in self.teamDic:
            return None, "TEAM_ID_NOT_FOUND"

        teamVal = self.teamDic[teamId]
        return teamVal.unblockTeamMemberMisc(playerGBID, toClient=True)

    def blockAllTeamMemberMics(self, srcPlayerBox, srcPlayerGBID, teamId, extraProps):
        LOG_IFO("blockAllTeamMemberMics::", srcPlayerBox, srcPlayerGBID, teamId, extraProps)
        teamVal, err = self._blockAllTeamMemberMics(srcPlayerBox, srcPlayerGBID, teamId)
        if err:
            LOG_WARN('blockAllTeamMemberMics:: failed, {}'.format(err))
            return

    def _blockAllTeamMemberMics(self, srcPlayerBox, srcPlayerGBID, teamId):
        if teamId not in self.teamDic:
            return None, "TEAM_ID_NOT_FOUND"

        teamVal = self.teamDic[teamId]
        if not teamVal.teamMicsSwitch:
            return None, "TEAM_MICS_SWITCH_OFF"

        if teamVal.teamMicsBlocked:
            return None, "TEAM_ALL_MISC_BLOCKED"

        for playerGBID, playerVal in teamVal.teamPlayerDic.items():
            if playerGBID == srcPlayerGBID:
                continue
            _, err = teamVal.turnOffTeamMemberMics(srcPlayerGBID, playerGBID, blockMics=True, toClient=False)
            if err:
                LOG_WARN("_blockAllTeamMemberMics::failed, err={}".format(err),
                            srcPlayerGBID, teamId, playerGBID, playerVal)

        teamVal.teamMicsBlocked = True
        return teamVal, ""

    def unblockAllTeamMemberMics(self, srcPlayerBox, srcPlayerGBID, teamId, extraProps):
        LOG_IFO("unblockAllTeamMemberMics::", srcPlayerBox, srcPlayerGBID, teamId, extraProps)
        teamVal, err = self._unblockAllTeamMemberMics(srcPlayerBox, srcPlayerGBID, teamId)
        if err:
            LOG_WARN('unblockAllTeamMemberMics:: failed, {}'.format(err))
            return

    def _unblockAllTeamMemberMics(self, srcPlayerBox, srcPlayerGBID, teamId):
        if teamId not in self.teamDic:
            return "TEAM_ID_NOT_FOUND"

        teamVal = self.teamDic[teamId]
        if not teamVal.teamMicsSwitch:
            return None, "TEAM_MICS_SWITCH_OFF"

        teamVal.teamMicsBlocked = False
        for playerGBID, playerVal in teamVal.teamPlayerDic.items():
            _, err = teamVal.unblockTeamMemberMisc(playerGBID, toClient=False)
            if err:
                LOG_WARN("_unblockAllTeamMemberMics::failed, err={}".format(err),
                            srcPlayerGBID, teamId, playerGBID, playerVal)
        return teamVal, ""

    # --------------------------------------------------------------------

    def debugAllTeamInfo(self):
        LOG_IFO('!!!!!!!========== debug all team info start ==========')
        for teamid, info in self.teamDic.items():
            LOG_IFO('!!!!!!!teamid:', teamid)
            LOG_IFO('!!!!!!!        组队目标:{}, 等级区间{}~{}'.format(TMACTD.datas[info.teamTarget]['value'], info.teamMinLv, info.teamMinScore))
            LOG_IFO('!!!!!!!        组队人数:{}}'.format(len(info.teamPlayerDic)))
        LOG_IFO('!!!!!!!========== debug all team info end ==========')

    # --------------------------------------------------------------------
    # TEAM CROSS SERVER

    # --------------------------------------------------------------------

    def getCaptainName(self, teamId, box, callBackFuncName, bossId):
        if teamId not in self.teamDic:
            return

        teamVal = self.teamDic[teamId]

        fn = getattr(box.cell, callBackFuncName, None)
        fn and fn(teamId, teamVal.getCaptainName(), bossId)


    # 标记相关
    def reqAddMarkMember(self, teamId, playerBox, type, index, name, gbId, entId, pos, box):
        LOG_IFO('reqAddMarkMember', teamId, type, index, name, gbId, entId, pos, box)
        if teamId not in self.teamDic:
            return

        # 要先执行删除
        self.reqDelMarkMember(teamId, playerBox, type, index)

        teamVal = self.teamDic[teamId]
        teamVal.addMarkMember(playerBox, type, index, name, gbId, entId, pos)
        # 记录
        if type == gameconst.TeamMarkType.MARK_ENEMY and entId > 0:
            self.addTeamMarkMonsterRec(teamId, entId, index, box)

    def addTeamMarkMonsterRec(self, teamId, entId, index, box):
        # 满了说明处理逻辑有问题，功能暂停
        if len(self.teamMarkMonsterRec) >= 20000:
            LOG_IFO('addTeamMarkMonsterRec, mark monster rec full ', len(self.teamMarkMonsterRec))
            return
        if not self.teamMarkMonsterRec.get(entId, None):
            self.teamMarkMonsterRec[entId] = {0: box}

        if len(self.teamMarkMonsterRec[entId]) >= 10000:
            LOG_IFO('addTeamMarkMonsterRec, mark monster rec full for entId: ', entId, len(self.teamMarkMonsterRec[entId]))
            return
        self.teamMarkMonsterRec[entId][teamId] = index
        LOG_IFO('addTeamMarkMonsterRec, mark monster rec:', entId, teamId, index)
        #
        box.onBeMarkedAsEnemy(teamId, gameconst.TeamType.TEAM, index)

    def delMarkMonsterRec(self, teamId, entId):
        if entId not in self.teamMarkMonsterRec:
            return
        if teamId in self.teamMarkMonsterRec[entId]:
            self.teamMarkMonsterRec[entId].pop(teamId)
            LOG_IFO('delMonsterRec, del mark monster rec:', entId, teamId)
            box = self.teamMarkMonsterRec[entId].get(0, None)
            if box:
                box.delBeMarkedAsEnemy(teamId, gameconst.TeamType.TEAM)

        if len(self.teamMarkMonsterRec[entId]) <= 1:   # 最后只剩box了
            self.teamMarkMonsterRec.pop(entId)
            LOG_IFO('delMonsterRec, remove mark monster rec box:', entId)

    def reqDelMarkMember(self, teamId, playerBox, type, index):
        LOG_IFO('reqDelMarkMember', teamId, type, index)
        if teamId not in self.teamDic:
            return
        teamVal = self.teamDic[teamId]
        entId = teamVal.delMarkMember(playerBox, type, index)

        self.delMarkMonsterRec(teamId, entId)

    def onMarkMonsterDead(self, entId):
        if entId not in self.teamMarkMonsterRec:
            return
        teamInfo = self.teamMarkMonsterRec.get(entId, {})
        LOG_IFO('onMarkMonsterDead, remove mark monster:', entId, teamInfo.keys())
        teamInfo = copy.deepcopy(teamInfo)
        for teamId, index in teamInfo.items():
            self.reqDelMarkMember(teamId, None, gameconst.TeamMarkType.MARK_ENEMY, index)

    def reqChangeOnlyCaptain(self, teamId, playerBox, state):
        LOG_IFO('reqChangeOnlyCaptain', teamId, state)
        if teamId not in self.teamDic:
            return
        teamVal = self.teamDic[teamId]
        teamVal.changeOnlyCaptainState(playerBox, state)

    def reqJoinTeam(self, playerBox, teamID, password, playerProps):
        err = self._reqJoinTeamCheck(teamID, password, playerProps)
        # 加入成功，刷新一下成员的cache
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR("reqJoinRaid, err:", err, playerProps)
            return

    def _reqJoinTeamCheck(self, teamID, password, playerProps):
        teamVal = self.getTeamByTeamId(teamID)
        LOG_IFO('in _reqJoinTeamCheck:', teamID, playerProps, teamVal)
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
        _, err = self.addTeamMember(teamID, playerProps)
        return err

    def setInDungeon(self, teamId):
        teamVal = self.teamDic.get(teamId, None)
        if not teamVal:
            LOG_WARN('setInDungeon, not found team:', teamId)
            return
        teamVal.isInDungeon = True

    def checkInDungeon(self, teamId):
        teamVal = self.teamDic.get(teamId, None)
        if not teamVal:
            LOG_WARN('checkInDungeon, not found team:', teamId)
            return False
        return teamVal.isInDungeon


