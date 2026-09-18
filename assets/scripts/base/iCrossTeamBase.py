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
    # 上线查询组队数据
    def queryCrossTeamInfo(self):
        gameengine.getCrossTeamStub(self.gbID).queryPlayerTeam(self, self.gbID)

    # ------------------------------------------------------------------
    # Stub 下行中继：playerBox 失效时经 PlayerStub 到 base 再转 cell
    # ------------------------------------------------------------------

    def onCrossTeamCellRelay(self, method, args):
        if self.cell:
            getattr(self.cell, method)(*args)

    def syncCrossTeamIdToBase(self, teamId):
        # cell 同步跨服队伍 id 镜像（聊天等 base 方法用）
        self.crossTeamIdBase = teamId

    def onCrossGhostReturnCityDone(self, citySpaceNo):
        # 本服幽灵回城完成（cell 落地后上报）：同步跨服镜像的回程落点为主城，
        # 玩家 goback 时客户端预加载图与幽灵实际位置一致（回本服落在主城）
        LOG_INFO('onCrossGhostReturnCityDone', self.gbID, citySpaceNo)
        self.syncMethodCallToCrossServerBase('setCrossGhostReturnSpaceNo', (citySpaceNo,))

    # ------------------------------------------------------------------
    # 跨服队伍聊天（客户端 -> base，本服完成检查后上行中心）
    # ------------------------------------------------------------------

    @gamedecorator.limitcall(0.5)
    def sendCrossTeamChatMsg(self, exposed, msg):
        LOG_DBG('sendCrossTeamChatMsg', self.gbID, msg)
        _teamId = self.crossTeamIdBase
        if not _teamId:
            self.onMessagePre(C_C_DD.datas['teamChannel_NotInTeam_msg']['value'], ())
            return

        if self.isAllServerForbidChat():
            self.onMessagePre(
                int(C_C_DD.datas['chat_banned']['value']),
                [str(self.idipBanDict.get(gameconst.IDIPBanType.CHAT, 0))]
            )
            return

        _now = utils.curTS()
        if _now < self.sendCrossTeamMsgTime + int(CCCH.datas[gameconst.ChatChannelEnum.TEAM]['channelCD']):
            _timeDelta = self.sendCrossTeamMsgTime + int(CCCH.datas[gameconst.ChatChannelEnum.TEAM]['channelCD']) - _now
            self.onMessagePre(int(C_C_DD.datas['msgId_worldChannelCD']['value']), [str(_timeDelta)])
            return

        self.sendCrossTeamMsgTime = _now
        self.logChatMsg(
            msg.get('msgType', 0),
            _teamId,
            gameconst.ChatChannelEnum.TEAM,
            msg.get('msg', ''),
            self.sendCrossTeamMsgTime
        )

        _roleData = gameglobal.roleCache[self.id]
        # 上行完整 CHAT_MSG_DATA（msg/code/voiceUrl/msgType，修复语音消息丢失）与
        # 拼 CHAT_CHANNEL_AVATAR_INFO 所需发送者信息（中心转发后由接收方本服组包下发）
        _senderInfo = {
            'school': _roleData['school'],
            'level': _roleData['level'],
            'sex': _roleData['sex'],
            'picFrameId': _roleData['picFrameId'],
        }
        gameengine.getCrossTeamStub(_teamId).sendTeamChat(
            _teamId,
            self.gbID,
            _roleData['name'],
            msg,
            _senderInfo
        )

    # ------------------------------------------------------------------
    # Stub -> base：跨服队伍聊天批量下行（拆包后逐条走本服队伍频道链路下发）
    # ------------------------------------------------------------------

    def onCrossTeamChatBatch(self, msgList):
        LOG_DBG('onCrossTeamChatBatch', self.gbID, len(msgList) if msgList else 0)
        if not self.client:
            return

        for _msg in msgList:
            # 方案B：复用本服通用频道消息下发（iChat.onRecvChannelMsg，含好友屏蔽检查，
            # 内部经 localCrossClient.onRecvAvatarChannelMsg 推客户端），客户端聊天框零适配；
            # avatarInfo.id(ENTITY_ID) 跨服无本服实体，置 0（决策 D1，字段保留）
            _avatarInfo = utils.buildChatChannelAvatarData(
                0,
                _msg.get('senderGbId', 0),
                _msg.get('senderSchool', 0),
                _msg.get('senderName', ''),
                _msg.get('senderLevel', 0),
                _msg.get('senderSex', 0),
                _msg.get('senderPicFrameId', 0)
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
