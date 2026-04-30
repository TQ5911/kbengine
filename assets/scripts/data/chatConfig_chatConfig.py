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
        "value": "<color=#00000000><sprite name=\"48_00\"></color><color=#C4971D>{0}</color>",
    }),
    "sendPacketNumLimitMsg": _tools.RODict({
        "ID": "sendPacketNumLimitMsg",
        "value": 54000339,
    }),
    "chat_banned": _tools.RODict({
        "ID": "chat_banned",
        "value": 54001558,
    }),
    "thankMsgLimit": _tools.RODict({
        "ID": "thankMsgLimit",
        "value": 7,
    }),
    "thankMsgRate": _tools.RODict({
        "ID": "thankMsgRate",
        "value": 0.1,
    })
})