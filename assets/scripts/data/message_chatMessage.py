# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: message/chatMessage
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    58000001: _tools.RODict({
        "ID": 58000001,
        "name": "chat_getGear",
        "Message": "获得<link item id={0} gbid={1}>{2}",
        "channelID": (6,)
    }),
    58000002: _tools.RODict({
        "ID": 58000002,
        "name": "killPlayer",
        "Message": "你击败了<color=#28b4a5><link player name={0} gbid={1}></color>",
        "channelID": (6,)
    }),
    58000003: _tools.RODict({
        "ID": 58000003,
        "name": "beKilledByPlayer",
        "Message": "你被<color=#28b4a5><link player name={0} gbid={1}></color>击败了",
        "channelID": (6,)
    }),
    58000004: _tools.RODict({
        "ID": 58000004,
        "name": "beKilledByOtherUnit",
        "Message": "你被<color=#28b4a5> {0} </color>击败了",
        "channelID": (6,)
    }),
    58000005: _tools.RODict({
        "ID": 58000005,
        "name": "relationBeFriendMsg",
        "Message": "我们现在已经是朋友啦，今后还请多多指教！",
        "channelID": (96,)
    }),
    58000006: _tools.RODict({
        "ID": 58000006,
        "name": "petQuality3Broadcast",
        "Message": "<link player name={0} gbid={1}>获得<color=#a677c6>史诗</color>精灵<color=#a677c6>{2}</color>！",
        "channelID": (2, 99)
    }),
    58000007: _tools.RODict({
        "ID": 58000007,
        "name": "petQuality4Broadcast",
        "Message": "<link player name={0} gbid={1}>获得<color=#beab67>传说</color>精灵<color=#beab67>{2}</color>！",
        "channelID": (2, 99)
    }),
    58000008: _tools.RODict({
        "ID": 58000008,
        "name": "guild_recruit_chat",
        "Message": "<color=#ffb638>{0}</color>级帮会<color=#739cc9>[{1}]</color>收人啦！期待各路朋友加盟！<color=#ae6fee><link guildApply name=\"申请加入\" gbid={2}></color>",
        "channelID": (2,)
    }),
    58000009: _tools.RODict({
        "ID": 58000009,
        "name": "guild_offcialResigned",
        "Message": "<color=#dea050>{0}</color>辞去了本帮<color=#ae6fee>{1}</color>职位！",
        "channelID": (3,)
    }),
    58000010: _tools.RODict({
        "ID": 58000010,
        "name": "guild_offcialAppointed",
        "Message": "<color=#dea050>{0}</color>被<color=#dea050>{1}</color>任命为本帮<color=#ae6fee>{2}</color>！",
        "channelID": (3,)
    }),
    58000011: _tools.RODict({
        "ID": 58000011,
        "name": "guild_offcialFired",
        "Message": "<color=#dea050>{0}</color>被<color=#dea050>{1}</color>免去了本帮<color=#ae6fee>{2}</color>职位！",
        "channelID": (3,)
    }),
    58000012: _tools.RODict({
        "ID": 58000012,
        "name": "guild_presidentTransferred",
        "Message": "<color=#dea050>{0}</color>已将<color=#ae6fee>帮主</color>之位禅让给了<color=#dea050>{1}</color>，恭迎新帮主",
        "channelID": (3,)
    }),
    58000013: _tools.RODict({
        "ID": 58000013,
        "name": "guild_join_chat",
        "Message": "欢迎新人<color=#dea050>{0}</color>加入帮会",
        "channelID": (3,)
    }),
    58000014: _tools.RODict({
        "ID": 58000014,
        "name": "guild_buildUpgraded",
        "Message": "<color=#b35b00>{0}</color>等级已提升至<color=#718bad>{1}</color>级",
        "channelID": (3,)
    }),
    58000018: _tools.RODict({
        "ID": 58000018,
        "name": "teamChannel_enterTeamMsg",
        "Message": "<color=#28b4a5>{0}</color>加入了队伍",
        "channelID": (4,)
    }),
    58000019: _tools.RODict({
        "ID": 58000019,
        "name": "teamChannel_initiativeLeaveTeamMsg",
        "Message": "<color=#28b4a5>{0}</color>主动离开了队伍",
        "channelID": (4,)
    }),
    58000020: _tools.RODict({
        "ID": 58000020,
        "name": "teamChannel_kickedMsg",
        "Message": "<color=#28b4a5>{0}</color>离开了队伍",
        "channelID": (4,)
    }),
    58000021: _tools.RODict({
        "ID": 58000021,
        "name": "teamChannel_applyCaptainMsg",
        "Message": "<color=#28b4a5>{0}</color>申请成为队长，正在等待<color=#28b4a5>{1}</color>选择…",
        "channelID": (4,)
    }),
    58000022: _tools.RODict({
        "ID": 58000022,
        "name": "teamChannel_becomeCaptainMsg",
        "Message": "<color=#28b4a5>{0}</color>成为了队长",
        "channelID": (4,)
    }),
    58000023: _tools.RODict({
        "ID": 58000023,
        "name": "highFallingMsg",
        "Message": "你失足坠落摔死了!",
        "channelID": (6,)
    }),
    58000024: _tools.RODict({
        "ID": 58000024,
        "name": "achFinishMessage1",
        "Message": "达成成就<color=#ffe671><link achievement id={0}></color>！",
        "channelID": (1,)
    }),
    58000025: _tools.RODict({
        "ID": 58000025,
        "name": "achFinishMessage2",
        "Message": "恭喜<color=#28b4a5><link player name={1} gbid={2}></color>达成了成就<color=#ffe671><link achievement id={0}></color>！",
        "channelID": (2, 99)
    }),
    58000026: _tools.RODict({
        "ID": 58000026,
        "name": "raidCreated",
        "Message": "<color=#718bad>团队创建成功</color>",
        "channelID": (7,)
    }),
    58000027: _tools.RODict({
        "ID": 58000027,
        "name": "raid_unready",
        "Message": "<color=#dea050>{0}</color>尚未准备就绪！",
        "channelID": (7,)
    }),
    58000028: _tools.RODict({
        "ID": 58000028,
        "name": "teamChannel_applyTeamMsg",
        "Message": "目标：{0}\n招募信息：{1}\n队伍人数：{2}/{3}<link team name=申请加入 teamId={4} isRaid={5} teamTarget={6}>",
        "channelID": (2,)
    }),
    58000029: _tools.RODict({
        "ID": 58000029,
        "name": "teamChannel_applyRaidMsg",
        "Message": "目标：{0}\n招募信息：{1}\n团队人数：{2}/{3}<link team name=申请加入 teamId={4} isRaid={5} teamTarget={6}>",
        "channelID": (2,)
    }),
    58000030: _tools.RODict({
        "ID": 58000030,
        "name": "raid_playerLeft",
        "Message": "<color=#dea050>{0}</color>退出了团队",
        "channelID": (7,)
    }),
    58000031: _tools.RODict({
        "ID": 58000031,
        "name": "raid_playerKicked",
        "Message": "<color=#dea050>{0}</color>被请离了团队",
        "channelID": (7,)
    }),
    58000032: _tools.RODict({
        "ID": 58000032,
        "name": "guild_declareWar",
        "Message": "众志成城，热血争锋，帮会<color=#ffe671>{0}</color>向帮会<color=#ffe671>{1}</color>宣战！",
        "channelID": (3, 99)
    }),
    58000033: _tools.RODict({
        "ID": 58000033,
        "name": "guild_pkPrompt",
        "Message": "<color=#dea050>{0}</color>在<color=#65b276>{1}</color>被<color=#c60c0c>{2}</color>击败",
        "channelID": (3,)
    }),
    58000034: _tools.RODict({
        "ID": 58000034,
        "name": "guild_pkPrompt2",
        "Message": "<color=#dea050>{0}</color>在<color=#65b276>{1}</color>击败了<color=#c60c0c>{2}</color>！",
        "channelID": (3,)
    }),
    58000060: _tools.RODict({
        "ID": 58000060,
        "name": "teamChannel_createTeamMsg",
        "Message": "队伍创建成功",
        "channelID": (4,)
    }),
    58000061: _tools.RODict({
        "ID": 58000061,
        "name": "chat_getItemType1",
        "Message": "获得{0}<link item id={1} gbid={2}>{3}",
        "channelID": (6,)
    }),
    58000062: _tools.RODict({
        "ID": 58000062,
        "name": "chat_getItemType2",
        "Message": "获得<link item id={1} gbid={2}>×{0}{3}",
        "channelID": (6,)
    }),
    58000063: _tools.RODict({
        "ID": 58000063,
        "name": "chat_login",
        "Message": "欢迎",
        "channelID": (1,)
    }),
    58000155: _tools.RODict({
        "ID": 58000155,
        "name": "gearDisassembled",
        "Message": "装备自动分解成功！",
        "channelID": (6,)
    }),
    58000108: _tools.RODict({
        "ID": 58000108,
        "name": "petQuality4Broadcast",
        "Message": "<color=#28b4a5><link player name={0} gbid={1}></color>获得<color=#a53131>神话</color>精灵<color=#a53131>{2}</color>！",
        "channelID": (2, 99)
    }),
    58000201: _tools.RODict({
        "ID": 58000201,
        "name": "mineBattle_chatChannelMsg1",
        "Message": "矿区争夺战已开始，攻破矿区核心的帮会，可获得矿区归属，群雄逐鹿，舍我其谁！",
        "channelID": (2, 3, 99)
    }),
    58000202: _tools.RODict({
        "ID": 58000202,
        "name": "mineBattle_chatChannelMsg2",
        "Message": "经过浴血奋战，<color=#45a6f1>{0}</color>的帮主<color=#dea050>{1}</color>率领帮众占领了<color=#65b276>{2}</color>矿区",
        "channelID": (2, 3, 99)
    }),
    58000203: _tools.RODict({
        "ID": 58000203,
        "name": "mineBattle_chatChannelMsg3",
        "Message": "<color=#65b276>{0}</color>矿区的荣誉旗帜正在遭受攻击，请前往保护",
        "channelID": (3,)
    }),
    58000204: _tools.RODict({
        "ID": 58000204,
        "name": "mineBattle_chatChannelMsg4",
        "Message": "<color=#65b276>{0}</color>矿区荣誉旗帜被破坏，本周已被破坏{1}/{2}次，帮会权威受到挑战",
        "channelID": (3,)
    }),
    58000205: _tools.RODict({
        "ID": 58000205,
        "name": "mineBattle_chatChannelMsg5",
        "Message": "<color=#65b276>{0}</color>矿区荣誉旗帜被破坏，本周已被破坏{1}/{2}次，不再获得矿区额外收益",
        "channelID": (3,)
    }),
    58000206: _tools.RODict({
        "ID": 58000206,
        "name": "mineBattle_chatChannelMsg6",
        "Message": "<color=#65b276>{0}</color>矿区的旗帜血量已不足50%，请及时修复",
        "channelID": (3,)
    }),
    58000207: _tools.RODict({
        "ID": 58000207,
        "name": "mineBattle_chatChannelMsg7",
        "Message": "<color=#739cc9>{0}</color>帮会占领的<color=#65b276>{1}</color>矿区被多次破坏，帮会颜面扫地，不再获得该矿区额外收益",
        "channelID": (3, 99)
    }),
    58000208: _tools.RODict({
        "ID": 58000208,
        "name": "cityBattle_auctionStart",
        "Message": "群雄逐鹿，谁与争锋？奉现任新元城城主<color=#dea050>{0}</color>之命布告天下，凡自认实力超群者，皆可于接下来的5天内猎杀任意魔物，以获取魔物灵核。所得灵核将于5天后上缴至新元城府衙，上缴数量最多之帮派，可获取本期新元城攻城令。\n<color=#dea050>{1}</color>",
        "channelID": (3, 99)
    }),
    58000209: _tools.RODict({
        "ID": 58000209,
        "name": "cityBattle_declareWar1",
        "Message": "<color=#fe6a6a>{0}</color>帮会对新元城宣战，此次新元城决战，攻城帮会：<color=#fe6a6a>{1}</color>，守城帮会：<color=#45a6f1>{2}</color>。<color=#038304>{3}年{4}月{5}号21点</color>，本次新元城战正式开始。烽烟再起，舍我其谁！\n<color=#dea050>{6}</color>",
        "channelID": (3, 99)
    }),
    58000210: _tools.RODict({
        "ID": 58000210,
        "name": "cityBattle_declareWar2",
        "Message": "此次新元城决战，攻城帮会：无，守城帮会：<color=#45a6f1>{0}</color>。<color=#038304>{1}年{2}月{3}号21点</color>，本次新元城战正式开始。烽烟再起，舍我其谁！",
        "channelID": (3, 99)
    }),
    58000211: _tools.RODict({
        "ID": 58000211,
        "name": "cityBattle_declareWar3",
        "Message": "<color=#fe6a6a>{0}</color>帮会对新元城宣战，此次新元城决战，攻城帮会：<color=#fe6a6a>{1}</color>，守城帮会：无。<color=#038304>{2}年{3}月{4}号21点</color>，本次新元城战正式开始。烽烟再起，舍我其谁！",
        "channelID": (3, 99)
    })
})
minKey = 58000001
maxKey = 58000211