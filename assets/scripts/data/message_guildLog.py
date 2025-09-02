# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: message/guildLog
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    38000001: _tools.RODict({
        "ID": 38000001,
        "name": "guildLog_guildEstablished",
        "log": "<color=#b35b00>{0}</color>创立了帮会<color=#038304>{1}</color>",
    }),
    38000002: _tools.RODict({
        "ID": 38000002,
        "name": "guildLog_memberJoined",
        "log": "<color=#b35b00>{0}</color>加入了<color=#038304>{1}</color>，热烈欢迎！",
    }),
    38000003: _tools.RODict({
        "ID": 38000003,
        "name": "guildLog_memberLeave",
        "log": "<color=#b35b00>{0}</color>退出了<color=#038304>{1}</color>",
    }),
    38000004: _tools.RODict({
        "ID": 38000004,
        "name": "guildLog_memberKicked",
        "log": "<color=#b35b00>{0}</color>被<color=#b35b00>{1}</color>请离了<color=#038304>{2}</color>",
    }),
    38000005: _tools.RODict({
        "ID": 38000005,
        "name": "guildLog_guildUpgraded",
        "log": "帮会等级已提升至<color=#718bad>{0}</color>级！",
    }),
    38000006: _tools.RODict({
        "ID": 38000006,
        "name": "guildLog_buildUpgraded",
        "log": "<color=#b35b00>{0}</color>等级已提升至<color=#718bad>{1}</color>级",
    }),
    38000007: _tools.RODict({
        "ID": 38000007,
        "name": "guildLog_guildOfficialResign",
        "log": "<color=#b35b00>{0}</color>辞去了本帮<color=#763e9b>{1}</color>职务！",
    }),
    38000008: _tools.RODict({
        "ID": 38000008,
        "name": "guildLog_guildOfficialAdjusted",
        "log": "<color=#b35b00>{0}</color>被<color=#763e9b>{1}</color><color=#b35b00>{2}</color>从<color=#763e9b>{3}</color>调整为<color=#763e9b>{4}</color>！",
    }),
    38000009: _tools.RODict({
        "ID": 38000009,
        "name": "guildLog_guildLeaderChanged",
        "log": "原帮主<color=#b35b00>{0}</color>任命<color=#b35b00>{1}</color>成为本帮新任<color=#763e9b>帮主</color>！",
    }),
    38000010: _tools.RODict({
        "ID": 38000010,
        "name": "guildLog_guildNameChanged",
        "log": "本帮帮会名更新为<color=#038304>{0}</color>！",
    }),
    38000011: _tools.RODict({
        "ID": 38000011,
        "name": "guildLog_guildMoneyUsed",
        "log": "<color=#b35b00>{0}</color>将<color=#b35b00>{1}帮会金币</color>转化为<color=#038304>{2}帮会资金</color>",
    }),
    38000012: _tools.RODict({
        "ID": 38000012,
        "name": "guild_unionDesc",
        "log": "我帮与帮会<color=#b35b00>{0}</color>结为同盟",
    }),
    38000013: _tools.RODict({
        "ID": 38000013,
        "name": "guild_relieveUnionDes",
        "log": "我帮与帮会<color=#b35b00>{0}</color>解除同盟",
    }),
    38000014: _tools.RODict({
        "ID": 38000014,
        "name": "guild_enmityDesc1",
        "log": "我帮向帮会<color=#b35b00>{0}</color>宣战",
    }),
    38000015: _tools.RODict({
        "ID": 38000015,
        "name": "guild_enmityDesc2",
        "log": "帮会<color=#b35b00>{0}</color>向我帮宣战",
    }),
    38000016: _tools.RODict({
        "ID": 38000016,
        "name": "guild_siegeOrderExpire",
        "log": "仓库中的<color=#b35b00>{0}魔物灵核（帮）</color>已过期删除",
    }),
    38000017: _tools.RODict({
        "ID": 38000017,
        "name": "guild_biddingReturn",
        "log": "竞价被超过，返还<color=#b35b00>{0}魔物灵核（帮）</color>",
    })
})
minKey = 38000001
maxKey = 38000017