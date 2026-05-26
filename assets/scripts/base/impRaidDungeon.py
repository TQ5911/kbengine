# coding: utf-8
from KBEDebug import *

import gameconst

class ImpRaidDungeon(object):
    def createAndEnterRaidDungeonMemberPreCheck(self, srcPlayerBox, raidUUID, dungeonNo, dungeonSrc, extraData):
        LOG_INFO("createAndEnterRaidDungeonMemberPreCheck 1 ", srcPlayerBox, raidUUID, dungeonNo, dungeonSrc, extraData)
        dungeonPlayMode = extraData['dungeonPlayMode']
        errno = gameconst.RaidDungeonErrno.ENUM_RAIDDUN_REWARD_NUM_CHECK_FAIL
        if dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.CHIEF:
            LOG_INFO("createAndEnterRaidDungeonMemberPreCheck 2 ", srcPlayerBox, raidUUID, dungeonNo, dungeonSrc, extraData)
            if self.chiefInfo.isCanTakeReward():
                LOG_INFO("createAndEnterRaidDungeonMemberPreCheck 3 ", srcPlayerBox, raidUUID, dungeonNo, dungeonSrc, extraData)
                errno = gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK
        extraData.pop('dungeonPlayMode', None)
        srcPlayerBox.cell.onCreateAndEnterRaidDungeonAllMemberPreCheck(
            errno.errno, raidUUID, dungeonNo, dungeonSrc, extraData['_avatarProps']['gbId'], extraData['_avatarProps']['name'], extraData)
    
    def doEnterRaidDungeonSelfCheck(self, dungeonNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox, src, extraProps):
        extraProps.update({

            'name': self.characterName,
            'school': self.getRoleCacheAttr('school', 0),
            'level': self.getRoleCacheAttr('level', 0),
            'sex': self.getRoleCacheAttr('sex', 0),
            'gbId': self.gbID,
            'eId': self.id,
        })
        LOG_INFO('doEnterRaidDungeonSelfCheck::', dungeonNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox, src, extraProps)
        self.cell.doEnterRaidDungeonAfterCheck(dungeonNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox, src, extraProps)
