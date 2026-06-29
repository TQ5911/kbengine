# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: chatConfig/chatConfig
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "textMaxLength": _tools.RODict({
        "ID": "textMaxLength",
        "value": 45,
    }),
    "textLimitExceeded_msg": _tools.RODict({
        "ID": "textLimitExceeded_msg",
        "value": 54000027,
    }),
    "playerNameColor_link": _tools.RODict({
        "ID": "playerNameColor_link",
        "value": 35,
    }),
    "msgID_channel_noItem": _tools.RODict({
        "ID": "msgID_channel_noItem",
        "value": 54000865,
    }),
    "msgId_worldChannelCD": _tools.RODict({
        "ID": "msgId_worldChannelCD",
        "value": 54000374,
    }),
    "msgId_worldChannel_LevelNotEnough": _tools.RODict({
        "ID": "msgId_worldChannel_LevelNotEnough",
        "value": 54000375,
    }),
    "msgId_labaNoText": _tools.RODict({
        "ID": "msgId_labaNoText",
        "value": 54001381,
    }),
    "teamChannel_NotInTeam_msg": _tools.RODict({
        "ID": "teamChannel_NotInTeam_msg",
        "value": 54000377,
    }),
    "guildChannel_NotInGuild_msg": _tools.RODict({
        "ID": "guildChannel_NotInGuild_msg",
        "value": 54000378,
    }),
    "channel_chatShield_msg": _tools.RODict({
        "ID": "channel_chatShield_msg",
        "value": 54000376,
    }),
    "positionLinkColor": _tools.RODict({
        "ID": "positionLinkColor",
        "value": 138,
    }),
    "interactTeamMatchGoal": _tools.RODict({
        "ID": "interactTeamMatchGoal",
        "value": "队伍目标：{0}",
    }),
    "positionLink": _tools.RODict({
        "ID": "positionLink",
        "value": "{0}:({1},{2}),{3}线",
    }),
    "positionLinkNoLine": _tools.RODict({
        "ID": "positionLinkNoLine",
        "value": "{0}:({1},{2})",
    }),
    "redPacket": _tools.RODict({
        "ID": "redPacket",
        "value": "UIRedPacketPanel",
    }),
    "blessingLength": _tools.RODict({
        "ID": "blessingLength",
        "value": 16,
    }),
    "sendPacketLimit": _tools.RODict({
        "ID": "sendPacketLimit",
        "value": 20,
    }),
    "sendPacketLimitMsg": _tools.RODict({
        "ID": "sendPacketLimitMsg",
        "value": 54000330,
    }),
    "receivePacketLimit": _tools.RODict({
        "ID": "receivePacketLimit",
        "value": 50,
    }),
    "receivePacketLimitMsg": _tools.RODict({
        "ID": "receivePacketLimitMsg",
        "value": 54000331,
    }),
    "receivePacketEmptyMsg": _tools.RODict({
        "ID": "receivePacketEmptyMsg",
        "value": 54000332,
    }),
    "returnPacketMail": _tools.RODict({
        "ID": "returnPacketMail",
        "value": 37000013,
    }),
    "displayPacketLimit": _tools.RODict({
        "ID": "displayPacketLimit",
        "value": 50,
    }),
    "returnPacketTime": _tools.RODict({
        "ID": "returnPacketTime",
        "value": 12,
    }),
    "usePacketLvLimit": _tools.RODict({
        "ID": "usePacketLvLimit",
        "value": 9,
    }),
    "usePacketLvLimitMsg": _tools.RODict({
        "ID": "usePacketLvLimitMsg",
        "value": 54000333,
    }),
    "sendPacketCoin": _tools.RODict({
        "ID": "sendPacketCoin",
        "value": 30000001,
    }),
    "redPacketType1": _tools.RODict({
        "ID": "redPacketType1",
        "value": "平均红包",
    }),
    "redPacketType2": _tools.RODict({
        "ID": "redPacketType2",
        "value": "拼手气红包",
    }),
    "receivePacketThankMsg": _tools.RODict({
        "ID": "receivePacketThankMsg",
        "value": ('<color=#c4971d>{0}</color> 老板大气！祝你爆神装！', '多谢 <color=#c4971d>{0}</color> 的红包，大佬霸气！', '<color=#c4971d>{0}</color>红包给力！小弟拜谢！', '感谢 <color=#c4971d>{0}</color> 的红包！战力+10086！', '<color=#c4971d>{0}</color> 红包威武，小弟拜谢！'),
    }),
    "sendPacketMsg": _tools.RODict({
        "ID": "sendPacketMsg",
        "value": "恭喜发财，大吉大利！#祝福收下，好运连连！#手气最佳，非你莫属！#财源广进，万事如意！",
    }),
    "mainRedPacketMsgShow": _tools.RODict({
        "ID": "mainRedPacketMsgShow",
        "value": "<color=#00000000><sprite anim=\"425,432,30\"></color><color=#C4971D>{0}</color>",
    }),
    "sendPacketNumLimitMsg": _tools.RODict({
        "ID": "sendPacketNumLimitMsg",
        "value": 54000339,
    }),
    "chat_banned": _tools.RODict({
        "ID": "chat_banned",
        "value": 54001558,
    }),
    "thankMsgRateLimit": _tools.RODict({
        "ID": "thankMsgRateLimit",
        "value": 1000,
    }),
    "thankMsgRate": _tools.RODict({
        "ID": "thankMsgRate",
        "value": 0.01,
    }),
    "positionColor_link": _tools.RODict({
        "ID": "positionColor_link",
        "value": 236,
    }),
    "sendTimeOut": _tools.RODict({
        "ID": "sendTimeOut",
        "value": 5,
    }),
    "hornFunctionText": _tools.RODict({
        "ID": "hornFunctionText",
        "value": "传音",
    }),
    "hornMsgWordsLimitTip": _tools.RODict({
        "ID": "hornMsgWordsLimitTip",
        "value": 54001820,
    }),
    "hornMsgCdTip": _tools.RODict({
        "ID": "hornMsgCdTip",
        "value": 54000953,
    }),
    "voiceChat_otherVolume": _tools.RODict({
        "ID": "voiceChat_otherVolume",
        "value": 0.2,
    }),
    "voiceChat_voiceVolumeDefault": _tools.RODict({
        "ID": "voiceChat_voiceVolumeDefault",
        "value": 1.0,
    }),
    "voiceChat_micVolumeDefault": _tools.RODict({
        "ID": "voiceChat_micVolumeDefault",
        "value": 0.5,
    }),
    "voiceChat_cancelSendText1": _tools.RODict({
        "ID": "voiceChat_cancelSendText1",
        "value": "手指滑动，取消发送",
    }),
    "voiceChat_cancelSendText2": _tools.RODict({
        "ID": "voiceChat_cancelSendText2",
        "value": "松开手指，取消发送",
    }),
    "voiceChat_cancelSendMsg": _tools.RODict({
        "ID": "voiceChat_cancelSendMsg",
        "value": 54001600,
    }),
    "voiceChat_minTime": _tools.RODict({
        "ID": "voiceChat_minTime",
        "value": 1,
    }),
    "voiceChat_maxTime": _tools.RODict({
        "ID": "voiceChat_maxTime",
        "value": 20,
    }),
    "voiceChat_tooShortMsg": _tools.RODict({
        "ID": "voiceChat_tooShortMsg",
        "value": 54001601,
    }),
    "voiceChat_toTextFail": _tools.RODict({
        "ID": "voiceChat_toTextFail",
        "value": "[语音内容无法识别]",
    }),
    "teamChat_switchOnMsg": _tools.RODict({
        "ID": "teamChat_switchOnMsg",
        "value": 54001602,
    }),
    "teamChat_switchOffMsg": _tools.RODict({
        "ID": "teamChat_switchOffMsg",
        "value": 54001603,
    }),
    "teamChat_switchUnavailable": _tools.RODict({
        "ID": "teamChat_switchUnavailable",
        "value": 54001604,
    }),
    "teamChat_micModeSwitchOn": _tools.RODict({
        "ID": "teamChat_micModeSwitchOn",
        "value": 54001605,
    }),
    "teamChat_teamMuteSwitchOn": _tools.RODict({
        "ID": "teamChat_teamMuteSwitchOn",
        "value": 54001606,
    }),
    "teamChat_personalMuteSwitchOn": _tools.RODict({
        "ID": "teamChat_personalMuteSwitchOn",
        "value": 54001607,
    }),
    "teamChat_voiceVolumeMuteMsg": _tools.RODict({
        "ID": "teamChat_voiceVolumeMuteMsg",
        "value": 54001608,
    }),
    "teamChat_voiceVolumeDefault": _tools.RODict({
        "ID": "teamChat_voiceVolumeDefault",
        "value": 0.2,
    }),
    "teamChat_micVolumeMuteMsg": _tools.RODict({
        "ID": "teamChat_micVolumeMuteMsg",
        "value": 54001609,
    }),
    "teamChat_micVolumeDefault": _tools.RODict({
        "ID": "teamChat_micVolumeDefault",
        "value": 0.3,
    }),
    "teamChat_voiceVolumeMuteTip": _tools.RODict({
        "ID": "teamChat_voiceVolumeMuteTip",
        "value": 54001610,
    }),
    "teamChat_micVolumeMuteTip": _tools.RODict({
        "ID": "teamChat_micVolumeMuteTip",
        "value": 54001611,
    }),
    "guildChat_switchOnMsg": _tools.RODict({
        "ID": "guildChat_switchOnMsg",
        "value": 54001612,
    }),
    "guildChat_switchOffMsg": _tools.RODict({
        "ID": "guildChat_switchOffMsg",
        "value": 54001613,
    }),
    "guildChat_micModeSwitch": _tools.RODict({
        "ID": "guildChat_micModeSwitch",
        "value": 54001614,
    }),
    "guildChat_allInvitationCd": _tools.RODict({
        "ID": "guildChat_allInvitationCd",
        "value": 60,
    }),
    "guildChat_oneInvitationCd": _tools.RODict({
        "ID": "guildChat_oneInvitationCd",
        "value": 10,
    }),
    "guildChat_allInvitationCheck": _tools.RODict({
        "ID": "guildChat_allInvitationCheck",
        "value": 54000630,
    }),
    "guildChat_allInvitationSend": _tools.RODict({
        "ID": "guildChat_allInvitationSend",
        "value": 54000631,
    }),
    "guildChat_invitationCd": _tools.RODict({
        "ID": "guildChat_invitationCd",
        "value": 54000632,
    }),
    "guildChat_invitationEmpty": _tools.RODict({
        "ID": "guildChat_invitationEmpty",
        "value": 54000635,
    }),
    "guildChat_joinMsg": _tools.RODict({
        "ID": "guildChat_joinMsg",
        "value": 54001615,
    }),
    "guildChat_noAuthorization": _tools.RODict({
        "ID": "guildChat_noAuthorization",
        "value": 54001616,
    }),
    "guildChat_autoOffMsg": _tools.RODict({
        "ID": "guildChat_autoOffMsg",
        "value": 54001617,
    }),
    "voiceChat_micSwitch": _tools.RODict({
        "ID": "voiceChat_micSwitch",
        "value": 54001618,
    }),
    "teamChat_micModeSwitchOff": _tools.RODict({
        "ID": "teamChat_micModeSwitchOff",
        "value": 54001619,
    }),
    "teamChat_teamMuteSwitchOff": _tools.RODict({
        "ID": "teamChat_teamMuteSwitchOff",
        "value": 54001621,
    }),
    "teamChat_personalMuteSwitchOff": _tools.RODict({
        "ID": "teamChat_personalMuteSwitchOff",
        "value": 54001622,
    }),
    "guildChat_numberMax": _tools.RODict({
        "ID": "guildChat_numberMax",
        "value": 15,
    }),
    "guildChat_numberMaxMsg": _tools.RODict({
        "ID": "guildChat_numberMaxMsg",
        "value": 54001623,
    }),
    "chat_voiceExchange": _tools.RODict({
        "ID": "chat_voiceExchange",
        "value": 54001624,
    }),
    "chat_voiceError": _tools.RODict({
        "ID": "chat_voiceError",
        "value": 54001625,
    }),
    "chat_voicePermission": _tools.RODict({
        "ID": "chat_voicePermission",
        "value": 54001626,
    }),
    "buyTranssion": _tools.RODict({
        "ID": "buyTranssion",
        "value": "Openinterface,UIPayStorePanel,1",
    }),
    "voiceChat_teamChannelName": _tools.RODict({
        "ID": "voiceChat_teamChannelName",
        "value": "队伍语音",
    }),
    "voiceChat_raidChannelName": _tools.RODict({
        "ID": "voiceChat_raidChannelName",
        "value": "团队语音",
    }),
    "voiceChat_guildChannelName": _tools.RODict({
        "ID": "voiceChat_guildChannelName",
        "value": "帮会语音",
    }),
    "freeModeName": _tools.RODict({
        "ID": "freeModeName",
        "value": "自由模式",
    }),
    "leaderModeName": _tools.RODict({
        "ID": "leaderModeName",
        "value": "权限模式",
    }),
    "forbindModeName": _tools.RODict({
        "ID": "forbindModeName",
        "value": "全员禁音",
    })
})