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
        "log": "<color=#beab67>{0}</color>创立了帮会<color=#98cf48>{1}</color>",
    }),
    38000002: _tools.RODict({
        "ID": 38000002,
        "name": "guildLog_memberJoined",
        "log": "<color=#beab67>{0}</color>加入了<color=#98cf48>{1}</color>，热烈欢迎！",
    }),
    38000003: _tools.RODict({
        "ID": 38000003,
        "name": "guildLog_memberLeave",
        "log": "<color=#beab67>{0}</color>退出了<color=#98cf48>{1}</color>",
    }),
    38000004: _tools.RODict({
        "ID": 38000004,
        "name": "guildLog_memberKicked",
        "log": "<color=#beab67>{0}</color>被<color=#beab67>{1}</color>请离了<color=#98cf48>{2}</color>",
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
        "log": "<color=#beab67>{0}</color>辞去了本帮<color=#dea050>{1}</color>职务！",
    }),
    38000008: _tools.RODict({
        "ID": 38000008,
        "name": "guildLog_guildOfficialAdjusted",
        "log": "<color=#beab67>{0}</color>被<color=#dea050>{1}</color><color=#beab67>{2}</color>从<color=#dea050>{3}</color>调整为<color=#dea050>{4}</color>！",
    }),
    38000009: _tools.RODict({
        "ID": 38000009,
        "name": "guildLog_guildLeaderChanged",
        "log": "原帮主<color=#beab67>{0}</color>任命<color=#beab67>{1}</color>成为本帮新任<color=#dea050>帮主</color>！",
    }),
    38000010: _tools.RODict({
        "ID": 38000010,
        "name": "guildLog_guildNameChanged",
        "log": "本帮帮会名更新为<color=#98cf48>{0}</color>！",
    }),
    38000011: _tools.RODict({
        "ID": 38000011,
        "name": "guildLog_guildMoneyUsed",
        "log": "<color=#beab67>{0}</color>将<color=#b35b00>{1}帮会元宝</color>转化为<color=#038304>{2}帮会资金</color>",
    }),
    38000012: _tools.RODict({
        "ID": 38000012,
        "name": "guild_unionDesc",
        "log": "我帮与帮会<color=#98cf48>{0}</color>结为同盟",
    }),
    38000013: _tools.RODict({
        "ID": 38000013,
        "name": "guild_relieveUnionDes",
        "log": "我帮与帮会<color=#98cf48>{0}</color>解除同盟",
    }),
    38000014: _tools.RODict({
        "ID": 38000014,
        "name": "guild_enmityDesc1",
        "log": "我帮向帮会<color=#d35a66>{0}</color>宣战",
    }),
    38000015: _tools.RODict({
        "ID": 38000015,
        "name": "guild_enmityDesc2",
        "log": "帮会<color=#d35a66>{0}</color>向我帮宣战",
    }),
    38000016: _tools.RODict({
        "ID": 38000016,
        "name": "guild_siegeOrderExpire",
        "log": "仓库中的<color=#b35b00>{0}帮会灵核</color>已过期删除",
    }),
    38000017: _tools.RODict({
        "ID": 38000017,
        "name": "guild_biddingReturn",
        "log": "竞价被超过，返还<color=#b35b00>{0}帮会灵核</color>",
    }),
    38000018: _tools.RODict({
        "ID": 38000018,
        "name": "guild_unionCreate",
        "log": "{0}创建了帮会联盟{1}，开创了联盟的历史",
    }),
    38000019: _tools.RODict({
        "ID": 38000019,
        "name": "guild_unionJoin",
        "log": "帮会{0}加入了{1}，大家热烈欢迎！",
    }),
    38000020: _tools.RODict({
        "ID": 38000020,
        "name": "guild_unionExit",
        "log": "帮会{0}退出了{1}，江湖路远有缘再见！",
    }),
    38000021: _tools.RODict({
        "ID": 38000021,
        "name": "guild_enmityDeclare",
        "log": "{0}对帮会{1}进行宣战，热血争锋，舍我其谁！",
    }),
    38000022: _tools.RODict({
        "ID": 38000022,
        "name": "guild_unionDeclare",
        "log": "{0}对联盟{1}进行宣战，热血争锋，舍我其谁！",
    }),
    38000023: _tools.RODict({
        "ID": 38000023,
        "name": "guild_enmityDeclare2",
        "log": "帮会{0}对我方联盟{1}进行宣战！",
    }),
    38000024: _tools.RODict({
        "ID": 38000024,
        "name": "guild_unionDeclare2",
        "log": "联盟{0}对我方联盟{1}进行宣战！",
    }),
    38000025: _tools.RODict({
        "ID": 38000025,
        "name": "guild_unionSupport1",
        "log": "我帮向帮会{0}援助{1}",
    }),
    38000026: _tools.RODict({
        "ID": 38000026,
        "name": "guild_unionSupport2",
        "log": "帮会{0}向我帮援助{1}",
    }),
    38000027: _tools.RODict({
        "ID": 38000027,
        "name": "guild_unionSupport3",
        "log": "帮会{0}向帮会{1}援助{2}",
    })
})
minKey = 38000001
maxKey = 38000027