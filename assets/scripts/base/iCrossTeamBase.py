# -*- coding: utf-8 -*-
# 跨服组队 base 侧 mixin（仅保留确属 base 职责的部分）：
# - 跨服队伍聊天：敏感词/禁言/CD 检查在发送方本服完成后上行中心；
# - Stub 下行中继（playerBox 失效时经 PlayerStub 到 base 再转 cell）。
# 讨伐条件检查/跨服迁移/镜像直进副本已迁至 base/impCrossTeamDungeonBase.py（跨服组队全覆盖·第二步）。
# 队伍缓存/匹配状态/客户端入口/下行推送均在 cell（cell/iCrossTeamCell.py）。

from KBEDebug import *

import utils
import gameengine
import gameconst
import gameglobal
import gameconfig
import formula

import chatConfig_channel as CCCH
import chatConfig_chatConfig as C_C_DD
import gamedecorator


class ICrossTeamBase(object):
    def onCrossTeamCellRelay(self, method, args):
        if self.cell:
            getattr(self.cell, method)(*args)

    def syncCrossTeamIdToBase(self, teamId):
        # cell 同步跨服队伍 id 镜像（聊天等 base 方法用）
        self.crossTeamIdBase = teamId

    def doCrossGuildInviteCheck(self, inviteInfo):
        # 帮会邀请入团的目标侧检查（Guild base 遍历投递，批量邀请静默语义对齐本服 GUILD 链路）：
        # 已在跨服队（含副本中）/拉黑了邀请人的目标直接跳过，通过则转 cell 弹邀请窗
        if self.friendship.isBlock(inviteInfo.get('gbId', 0)):
            return

        if self.cell:
            self.cell.doApplyCrossGuildInvite(inviteInfo)

    def onCrossGhostReturnCityDone(self, citySpaceNo):
        # 本服幽灵回城完成（cell 落地后上报）：同步跨服镜像的回程落点为主城，
        # 玩家 goback 时客户端预加载图与幽灵实际位置一致（回本服落在主城）
        LOG_INFO('onCrossGhostReturnCityDone', self.gbID, citySpaceNo)
        self.syncMethodCallToCrossServerBase('setCrossGhostReturnSpaceNo', (citySpaceNo,))

    # ------------------------------------------------------------------
    # 跨服队伍聊天
    # ------------------------------------------------------------------

    def sendCrossTeamChatMsg(self, msg):
        LOG_DBG('sendCrossTeamChatMsg', msg)
        _roleData = gameglobal.roleCache[self.id]
        _senderInfo = {
            'entId': self.id,
            'school': _roleData['school'],
            'level': _roleData['level'],
            'sex': _roleData['sex'],
            'picFrameId': _roleData['picFrameId'],
        }
        gameengine.getCrossTeamStub(self.crossTeamIdBase).sendTeamChat(
            self.crossTeamIdBase,
            self.gbID,
            _roleData['name'],
            msg,
            _senderInfo
        )

    def onCrossTeamChatBatch(self, msgList):
        LOG_DBG('onCrossTeamChatBatch', self.gbID, len(msgList) if msgList else 0)
        if not self.client:
            return

        for _msg in msgList:
            # 方案B：复用本服通用频道消息下发（iChat.onRecvChannelMsg，含好友屏蔽检查，
            # 内部经 localCrossClient.onRecvAvatarChannelMsg 推客户端），客户端聊天框零适配；
            # avatarInfo.id(ENTITY_ID) 带发信人实体 id，由发送方上行、中心透传；
            # serverId 取发言者归属服（中心按成员数据盖戳），客户端跨服标记用
            _avatarInfo = utils.buildChatChannelAvatarData(
                _msg.get('senderEntId', 0),
                _msg.get('senderGbId', 0),
                _msg.get('senderSchool', 0),
                _msg.get('senderName', ''),
                _msg.get('senderLevel', 0),
                _msg.get('senderSex', 0),
                _msg.get('senderPicFrameId', 0),
                _msg.get('senderServerId', 0)
            )
            _msgData = {
                'msg': _msg.get('content', ''),
                'code': _msg.get('code', 0),
                'voiceUrl': _msg.get('voiceUrl', ''),
                'msgType': _msg.get('msgType', 0),
            }
            self.onRecvChannelMsg(
                gameconst.ChatChannelEnum.TEAM,
                _avatarInfo,
                _msgData
            )
