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
        "Message": "你在<color=#54e7f2>{2}</color>击败了<color=#98cf48>{3}</color> <color=#d35a66> <link player name={0} gbid={1}></color>",
        "channelID": (6,)
    }),
    58000003: _tools.RODict({
        "ID": 58000003,
        "name": "beKilledByPlayer",
        "Message": "你在<color=#54e7f2>{2}</color>被<color=#98cf48>{3}</color>  <color=#d35a66><link player name={0} gbid={1}></color>击败了",
        "channelID": (6,)
    }),
    58000004: _tools.RODict({
        "ID": 58000004,
        "name": "beKilledByOtherUnit",
        "Message": "你被<color=#d35a66>{0}</color>击败了",
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
        "Message": "<color=#ffb638>{0}</color>级帮会<color=#98cf48>[{1}]</color>收人啦！期待各路朋友加盟！<color=#ae6fee><link guildApply name=\"申请加入\" gbid={2}></color>",
        "channelID": (2,)
    }),
    58000009: _tools.RODict({
        "ID": 58000009,
        "name": "guild_offcialResigned",
        "Message": "<color=#beab67><link player name={0} gbid={2}></color>辞去了本帮<color=#dea050>{1}</color>职位！",
        "channelID": (3,)
    }),
    58000010: _tools.RODict({
        "ID": 58000010,
        "name": "guild_offcialAppointed",
        "Message": "<color=#beab67><link player name={0} gbid={3}></color>被<color=#beab67><link player name={1} gbid={4}></color>任命为本帮<color=#dea050>{2}</color>！",
        "channelID": (3,)
    }),
    58000011: _tools.RODict({
        "ID": 58000011,
        "name": "guild_offcialFired",
        "Message": "<color=#beab67><link player name={0} gbid={3}></color>被<color=#beab67><link player name={1} gbid={4}></color>免去了本帮<color=#dea050>{2}</color>职位！",
        "channelID": (3,)
    }),
    58000012: _tools.RODict({
        "ID": 58000012,
        "name": "guild_presidentTransferred",
        "Message": "<color=#beab67><link player name={0} gbid={2}></color>已将<color=#dea050>帮主</color>之位禅让给了<color=#beab67><link player name={1} gbid={3}></color>，恭迎新帮主",
        "channelID": (3,)
    }),
    58000013: _tools.RODict({
        "ID": 58000013,
        "name": "guild_join_chat",
        "Message": "欢迎新人<color=#beab67><link player name={0} gbid={1}></color>加入帮会",
        "channelID": (3,)
    }),
    58000014: _tools.RODict({
        "ID": 58000014,
        "name": "guild_buildUpgraded",
        "Message": "<color=#b35b00>{0}</color>等级已提升至<color=#718bad>{1}</color>级",
        "channelID": (3,)
    }),
    58000015: _tools.RODict({
        "ID": 58000015,
        "name": "guild_union_recruit_chat",
        "Message": "联盟<color=#98cf48>{1}</color>寻找结盟伙伴，期待各方豪杰加盟！<color=#ae6fee><link allianceApply name=\"申请加入\" gbid={0}></color>",
        "channelID": (2,)
    }),
    58000018: _tools.RODict({
        "ID": 58000018,
        "name": "teamChannel_enterTeamMsg",
        "Message": "<color=#beab67><link player name={0} gbid={1}></color>加入了队伍",
        "channelID": (4,)
    }),
    58000019: _tools.RODict({
        "ID": 58000019,
        "name": "teamChannel_initiativeLeaveTeamMsg",
        "Message": "<color=#beab67><link player name={0} gbid={1}></color>主动离开了队伍",
        "channelID": (4,)
    }),
    58000020: _tools.RODict({
        "ID": 58000020,
        "name": "teamChannel_kickedMsg",
        "Message": "<color=#beab67><link player name={0} gbid={1}></color>离开了队伍",
        "channelID": (4,)
    }),
    58000021: _tools.RODict({
        "ID": 58000021,
        "name": "teamChannel_applyCaptainMsg",
        "Message": "<color=#beab67><link player name={0} gbid={2}></color>申请成为队长，正在等待<color=#beab67><link player name={1} gbid={3}></color>选择…",
        "channelID": (4,)
    }),
    58000022: _tools.RODict({
        "ID": 58000022,
        "name": "teamChannel_becomeCaptainMsg",
        "Message": "<color=#beab67><link player name={0} gbid={1}></color>成为了队长",
        "channelID": (4,)
    }),
    58000023: _tools.RODict({
        "ID": 58000023,
        "name": "highFallingMsg",
        "Message": "你从高处坠落，失去意识！",
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
        "Message": "恭喜<color=#beab67><link player name={1} gbid={2}></color>达成了成就<color=#ffe671><link achievement id={0}></color>！",
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
        "Message": "<color=#beab67>{0}</color>尚未准备就绪！",
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
        "Message": "<color=#beab67><link player name={0} gbid={1}></color>退出了团队",
        "channelID": (7,)
    }),
    58000031: _tools.RODict({
        "ID": 58000031,
        "name": "raid_playerKicked",
        "Message": "<color=#beab67><link player name={0} gbid={1}></color>被请离了团队",
        "channelID": (7,)
    }),
    58000032: _tools.RODict({
        "ID": 58000032,
        "name": "guild_declareWar1",
        "Message": "众志成城，热血争锋，帮会<color=#98cf48>{0}</color>向帮会<color=#98cf48>{1}</color>宣战！",
        "channelID": (2, 3, 99)
    }),
    58000033: _tools.RODict({
        "ID": 58000033,
        "name": "guild_pkPrompt",
        "Message": "<color=#beab67><link player name={0} gbid={1}></color>在<color=#54e7f2>{2}</color>被<color=#98cf48>{3}</color> <color=#d35a66><link player name={4} gbid={5}></color>击败",
        "channelID": (3,)
    }),
    58000034: _tools.RODict({
        "ID": 58000034,
        "name": "guild_pkPrompt2",
        "Message": "<color=#beab67><link player name={0} gbid={1}></color>在<color=#54e7f2>{2}</color>击败了<color=#98cf48>{3}</color> <color=#d35a66><link player name={4} gbid={5}></color>",
        "channelID": (3,)
    }),
    58000035: _tools.RODict({
        "ID": 58000035,
        "name": "auctionChannel_jumpToBuy",
        "Message": "<link auctionItem id={0} auctionid={1}>已上架交易行，手快有手慢无<link business itemId={2}><color=#54e7f2>前往查看</color></link>",
        "channelID": (10,)
    }),
    58000036: _tools.RODict({
        "ID": 58000036,
        "name": "guild_declareWar2",
        "Message": "众志成城，热血争锋，帮会<color=#98cf48>{0}</color>向联盟<color=#98cf48>{1}</color>宣战！",
        "channelID": (2, 3, 99)
    }),
    58000037: _tools.RODict({
        "ID": 58000037,
        "name": "guild_declareWar3",
        "Message": "众志成城，热血争锋，联盟<color=#98cf48>{0}</color>向联盟<color=#98cf48>{1}</color>宣战！",
        "channelID": (2, 3, 99)
    }),
    58000038: _tools.RODict({
        "ID": 58000038,
        "name": "guild_declareWar4",
        "Message": "众志成城，热血争锋，联盟<color=#98cf48>{0}</color>向帮会<color=#98cf48>{1}</color>宣战！",
        "channelID": (2, 3, 99)
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
        "Message": "自动分解获得<link item id={1} gbid={2}>×{0}",
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
        "Message": "经过浴血奋战，<color=#98cf48>{0}</color>的帮主<color=#beab67><link player name={1} gbid={3}></color>率领帮众占领了<color=#54e7f2>{2}</color>矿区",
        "channelID": (2, 3, 99)
    }),
    58000203: _tools.RODict({
        "ID": 58000203,
        "name": "mineBattle_chatChannelMsg3",
        "Message": "<color=#54e7f2>{0}</color>矿区的荣誉旗帜正在遭受攻击，请前往保护！<link mineBattleTeleport mapId={1}><color=#54e7f2>立即前往</color></link>",
        "channelID": (3,)
    }),
    58000204: _tools.RODict({
        "ID": 58000204,
        "name": "mineBattle_chatChannelMsg4",
        "Message": "<color=#54e7f2>{0}</color>矿区荣誉旗帜被破坏，本周已被破坏{1}/{2}次，本次损失{3}玄铁，帮会权威受到挑战",
        "channelID": (2, 3)
    }),
    58000205: _tools.RODict({
        "ID": 58000205,
        "name": "mineBattle_chatChannelMsg5",
        "Message": "<color=#54e7f2>{0}</color>矿区荣誉旗帜被破坏，本周已被破坏{1}/{2}次，矿区额外收益大幅降低",
        "channelID": (2, 3)
    }),
    58000206: _tools.RODict({
        "ID": 58000206,
        "name": "mineBattle_chatChannelMsg6",
        "Message": "<color=#54e7f2>{0}</color>矿区的旗帜血量已不足50%，请及时修复",
        "channelID": (3,)
    }),
    58000207: _tools.RODict({
        "ID": 58000207,
        "name": "mineBattle_chatChannelMsg7",
        "Message": "<color=#98cf48>{0}</color>帮会占领的<color=#54e7f2>{1}</color>矿区被多次破坏，帮会颜面扫地，矿区额外收益大幅降低",
        "channelID": (2, 3, 99)
    }),
    58000208: _tools.RODict({
        "ID": 58000208,
        "name": "cityBattle_auctionStart",
        "Message": "群雄逐鹿，谁与争锋？奉现任新元城城主<color=#beab67><link player name={0} gbid={2}></color>之命布告天下，凡自认实力超群者，皆可于接下来的5天内猎杀任意魔物，以获取魔物灵核。所得灵核将于5天后上缴至新元城府衙，上缴数量最多之帮派，可获取本期新元城攻城令。\n<color=#dea050>{1}</color>",
        "channelID": (3, 99)
    }),
    58000209: _tools.RODict({
        "ID": 58000209,
        "name": "cityBattle_declareWar1",
        "Message": "<color=#98cf48>{0}</color>帮会对新元城宣战，此次新元城决战，攻城帮会：<color=#d35a66>{1}</color>，守城帮会：<color=#54e7f2>{2}</color>。<color=#038304>{3}年{4}月{5}号21点</color>，本次新元城战正式开始。烽烟再起，舍我其谁！\n<color=#dea050>{6}</color>",
        "channelID": (3, 99)
    }),
    58000210: _tools.RODict({
        "ID": 58000210,
        "name": "cityBattle_declareWar2",
        "Message": "此次新元城决战，攻城帮会：无，守城帮会：<color=#54e7f2>{0}</color>。<color=#038304>{1}年{2}月{3}号21点</color>，本次新元城战正式开始。烽烟再起，舍我其谁！",
        "channelID": (3, 99)
    }),
    58000211: _tools.RODict({
        "ID": 58000211,
        "name": "cityBattle_declareWar3",
        "Message": "<color=#98cf48>{0}</color>帮会对新元城宣战，此次新元城决战，攻城帮会：<color=#d35a66>{1}</color>，守城帮会：无。<color=#038304>{2}年{3}月{4}号21点</color>，本次新元城战正式开始。烽烟再起，舍我其谁！",
        "channelID": (3, 99)
    }),
    58000212: _tools.RODict({
        "ID": 58000212,
        "name": "boss_born5001",
        "Message": "天地灵气骤然翻涌，<color=#fe6a6a>深海之王</color>现身于<color=#54e7f2>月光海港五层·精英</color>，各路豪侠可速速前往，御强敌，夺机缘！",
        "channelID": (2, 99)
    }),
    58000213: _tools.RODict({
        "ID": 58000213,
        "name": "boss_born5002",
        "Message": "天地灵气骤然翻涌，<color=#fe6a6a>祖珂教主</color>现身于<color=#54e7f2>祖珂地堡五层·精英</color>，各路豪侠可速速前往，御强敌，夺机缘！",
        "channelID": (2, 99)
    }),
    58000214: _tools.RODict({
        "ID": 58000214,
        "name": "unknownCauseMsg",
        "Message": "你因异常伤害，失去意识！",
        "channelID": (6,)
    }),
    58000215: _tools.RODict({
        "ID": 58000215,
        "name": "boss_born5004",
        "Message": "天地灵气骤然翻涌，<color=#fe6a6a>蚀日蛊后</color>现身于<color=#54e7f2>五毒石窟五层·精英</color>，各路豪侠可速速前往，御强敌，夺机缘！",
        "channelID": (2, 99)
    }),
    58000216: _tools.RODict({
        "ID": 58000216,
        "name": "boss_born5003",
        "Message": "天地灵气骤然翻涌，<color=#fe6a6a>空域王</color>现身于<color=#54e7f2>流沙故城五层·精英</color>，各路豪侠可速速前往，御强敌，夺机缘！",
        "channelID": (2, 99)
    }),
    58000217: _tools.RODict({
        "ID": 58000217,
        "name": "boss_born5005",
        "Message": "天地灵气骤然翻涌，<color=#fe6a6a>杜格教主</color>现身于<color=#54e7f2>杜格教廷五层·精英</color>，各路豪侠可速速前往，御强敌，夺机缘！",
        "channelID": (2, 99)
    }),
    58000218: _tools.RODict({
        "ID": 58000218,
        "name": "guild_unionSupport1",
        "Message": "我帮向帮会{0}援助{1}",
        "channelID": (3,)
    }),
    58000219: _tools.RODict({
        "ID": 58000219,
        "name": "guild_unionSupport2",
        "Message": "帮会{0}向我帮援助{1}",
        "channelID": (3,)
    }),
    58000220: _tools.RODict({
        "ID": 58000220,
        "name": "guild_unionSupport3",
        "Message": "帮会{0}向帮会{1}援助{2}",
        "channelID": (3,)
    }),
    58000221: _tools.RODict({
        "ID": 58000221,
        "name": "guildChat_switchOn",
        "Message": "帮会语音已被{0}[{1}]开启",
        "channelID": (3,)
    }),
    58000222: _tools.RODict({
        "ID": 58000222,
        "name": "guildChat_switchOff",
        "Message": "帮会语音已关闭",
        "channelID": (3,)
    })
})
minKey = 58000001
maxKey = 58000222