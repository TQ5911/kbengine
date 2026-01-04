# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: mail/mail
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    37000001: _tools.RODict({
        "ID": 37000001,
        "type": 2,
        "title": "掉落奖励补偿",
        "content": "由于您的背包已满，掉落的奖励无法拾取，现通过邮件发放给您。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000002: _tools.RODict({
        "ID": 37000002,
        "type": 2,
        "title": "未进入背包物品补偿",
        "content": "由于您的背包已满，获得的奖励无法领取，现通过邮件发放给您。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000003: _tools.RODict({
        "ID": 37000003,
        "type": 2,
        "title": "礼包奖励",
        "content": "由于您的背包空间不足，您的礼包奖励通过邮件发送。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000004: _tools.RODict({
        "ID": 37000004,
        "type": 2,
        "title": "加入帮会通知",
        "content": "您成功加入了帮会：<color=#739cc9>{0}</color>",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000005: _tools.RODict({
        "ID": 37000005,
        "type": 2,
        "title": "帮会解散通知",
        "content": "由于长期未运营帮会，我们遗憾的通知您，您之前所在的帮会已经解散。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000006: _tools.RODict({
        "ID": 37000006,
        "type": 2,
        "title": "您已被移出了帮会",
        "content": "您已被{0}<color=#dea050>{1}</color>移出了帮会。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000007: _tools.RODict({
        "ID": 37000007,
        "type": 2,
        "title": "创建帮会通知",
        "content": "您成功创建了帮会：<color=#739cc9>{0}</color>",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000008: _tools.RODict({
        "ID": 37000008,
        "type": 2,
        "title": "装备受损通知",
        "content": "您的<link item id={0} gbid={1}>已受损，能量晶核遗失在<link position x={2} z={3} spaceNo={4}>。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "1",
        "event": "",
        "parm": ""
    }),
    37000009: _tools.RODict({
        "ID": 37000009,
        "type": 2,
        "title": "装备修复通知",
        "content": "受损装备<link item id={0} gbid={1}>的能量晶核已遗失，请尽快修复，否则将在<link time={2} format=yyyy-MM-dd HH:mm:ss>后彻底破碎。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "24",
        "event": "",
        "parm": ""
    }),
    37000010: _tools.RODict({
        "ID": 37000010,
        "type": 2,
        "title": "装备破碎通知",
        "content": "您的<link item id={0} gbid=0>未修复，已彻底损毁。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "24",
        "event": "",
        "parm": ""
    }),
    37000011: _tools.RODict({
        "ID": 37000011,
        "type": 2,
        "title": "能量晶核退回通知",
        "content": "<link item id={0} gbid={1}>遗失的能量晶核已被退回，该装备将在30分钟后完成修复。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000012: _tools.RODict({
        "ID": 37000012,
        "type": 2,
        "title": "装备破碎通知",
        "content": "<link item id={0} gbid=0>未修复，彻底损毁，能量晶核已消散。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000013: _tools.RODict({
        "ID": 37000013,
        "type": 2,
        "title": "红包过期退回",
        "content": "您发放的红包超过12小时未被领取",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000014: _tools.RODict({
        "ID": 37000014,
        "type": 2,
        "title": "未进入背包药水寄存",
        "content": "由于您背包内可持有的回天甘露总量已超过{0}瓶，新获得的无法领取，现通过邮件发放给您。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000015: _tools.RODict({
        "ID": 37000015,
        "type": 2,
        "title": "召唤未领取奖励寄存",
        "content": "由于限时召唤活动时间已结束，您还有奖励尚未领取，现通过邮件发放给您。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000016: _tools.RODict({
        "ID": 37000016,
        "type": 2,
        "title": "离线收益补发",
        "content": "您上次离线收益未及时领取，已为您发放至邮件，请查收！",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000017: _tools.RODict({
        "ID": 37000017,
        "type": 2,
        "title": "帮会伏魔预约开启",
        "content": "您所在帮会已预约于{0}开启帮会伏魔 - {1}，请于预约时间准时参加！",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000018: _tools.RODict({
        "ID": 37000018,
        "type": 2,
        "title": "帮会伏魔准备开启",
        "content": "您所在帮会预约的帮会伏魔 - {0}即将开启，请于倒计时结束后入场！",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000019: _tools.RODict({
        "ID": 37000019,
        "type": 2,
        "title": "帮会伏魔已开启",
        "content": "您所在帮会已开启帮会伏魔 - {0}，请尽快进场，击败首领可获得丰厚奖励！",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000020: _tools.RODict({
        "ID": 37000020,
        "type": 2,
        "title": "帮会伏魔成功奖励",
        "content": "您在本次帮会伏魔 - {0}中表现优秀，根据您的伤害贡献，已发放对应档位奖励，请查收~",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37000030: _tools.RODict({
        "ID": 37000030,
        "type": 2,
        "title": "精灵秘宝调整通知",
        "content": "由于版本更新，精灵装备栏位数量发生变化，为避免您的损失，我们自动为您回收了精灵秘宝{0}，现通过邮件发放给您，请查收！",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001001: _tools.RODict({
        "ID": 37001001,
        "type": 1,
        "title": "全服邮件",
        "content": "全服邮件（GM发邮件使用）",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001002: _tools.RODict({
        "ID": 37001002,
        "type": 4,
        "title": "账号共享邮件测试",
        "content": "第一个登陆的角色才能获得哦！",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001003: _tools.RODict({
        "ID": 37001003,
        "type": 4,
        "title": "定制内容邮件",
        "content": "定制内容邮件",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001004: _tools.RODict({
        "ID": 37001004,
        "type": 1,
        "title": "新元起烽烟，群雄共逐鹿",
        "content": "群雄逐鹿，谁与争锋？奉现任新元城城主<color=#e4dabd>{0}</color>之命布告天下，凡自认实力超群者，皆可于接下来的5天内猎杀任意魔物，以获取魔物灵核。所得灵核将于5天后上缴至新元城府衙，上缴数量最多之帮派，可获取本期新元城攻城令。\n<color=#dea050>{1}</color>",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001005: _tools.RODict({
        "ID": 37001005,
        "type": 1,
        "title": "竞拍结束通知",
        "content": "恭喜<color=#b69fff>[{0}]</color><color=#739cc9>{1}</color> <color=#e4dabd>{2}</color> 出价<color=#038304>{3}</color>魔物灵核[帮]获得本期新元城攻城令归属。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001006: _tools.RODict({
        "ID": 37001006,
        "type": 1,
        "title": "宣战通知",
        "content": "<color=#fe6a6a>{0}</color>帮会对新元城宣战，此次新元城决战，攻城帮会：<color=#fe6a6a>{1}</color>，守城帮会：<color=#45a6f1>{2}</color>。<color=#038304>{3}年{4}月{5}号21点</color>，本次新元城战正式开始。烽烟再起，舍我其谁！\n<color=#dea050>{6}</color>",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001007: _tools.RODict({
        "ID": 37001007,
        "type": 2,
        "title": "阵营积分排名奖励",
        "content": "您在本次新元城战中获得了{0}积分，特予如下奖励，还请及时查收。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001008: _tools.RODict({
        "ID": 37001008,
        "type": 2,
        "title": "奖赏通知",
        "content": "您的英勇表现获得了城主的青睐，这是您的奖赏，请及时查收。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001009: _tools.RODict({
        "ID": 37001009,
        "type": 2,
        "title": "被通缉通知",
        "content": "您被通缉了。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001010: _tools.RODict({
        "ID": 37001010,
        "type": 1,
        "title": "城战结束通告",
        "content": "恭喜<color=#b69fff>[{0}]</color><color=#739cc9>{1}</color>获得了本次新元城战的胜利，<color=#e4dabd>{2}</color>荣登城主宝座！",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001011: _tools.RODict({
        "ID": 37001011,
        "type": 1,
        "title": "MVP奖励",
        "content": "您在本次新元城战中表现英勇，荣获MVP，特予如下奖励，还请及时查收。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001012: _tools.RODict({
        "ID": 37001012,
        "type": 1,
        "title": "竞猜返还",
        "content": "有更高的竞价出现，拍卖行已返还您参与竞拍的攻城令，请注意查收。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001013: _tools.RODict({
        "ID": 37001013,
        "type": 2,
        "title": "任命通知",
        "content": "恭喜您被任命为{0}，请再接再厉！",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001014: _tools.RODict({
        "ID": 37001014,
        "type": 1,
        "title": "竞拍结束通知",
        "content": "本期新元城攻城令已流拍。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001015: _tools.RODict({
        "ID": 37001015,
        "type": 1,
        "title": "宣战通知",
        "content": "此次新元城决战，攻城帮会：无，守城帮会：<color=#45a6f1>{0}</color>。<color=#038304>{1}年{2}月{3}号21点</color>，本次新元城战正式开始。烽烟再起，舍我其谁！",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001016: _tools.RODict({
        "ID": 37001016,
        "type": 1,
        "title": "宣战通知",
        "content": "<color=#fe6a6a>{0}</color>帮会对新元城宣战，此次新元城决战，攻城帮会：<color=#fe6a6a>{1}</color>，守城帮会：无。<color=#038304>{2}年{3}月{4}号21点</color>，本次新元城战正式开始。烽烟再起，舍我其谁！\n<color=#dea050>{5}</color>",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001017: _tools.RODict({
        "ID": 37001017,
        "type": 1,
        "title": "矿区争夺战开始",
        "content": "矿区争夺战已开始，攻破矿区核心的帮会，可获得矿区归属，群雄逐鹿，舍我其谁",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001018: _tools.RODict({
        "ID": 37001018,
        "type": 1,
        "title": "矿区收益分红",
        "content": "您对帮会的贡献，获得了帮主的认可，您获得了帮主<color=#dea050>{0}</color>犒赏的{1}",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001019: _tools.RODict({
        "ID": 37001019,
        "type": 1,
        "title": "矿区占领",
        "content": "经过浴血奋战，帮主<color=#dea050>{0}</color>率领帮众占领了<color=#65b276>{1}</color>矿区",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37001020: _tools.RODict({
        "ID": 37001020,
        "type": 1,
        "title": "矿战积分奖励",
        "content": "您在本次<color=#65b276>{0}</color>矿区争夺战中表现英勇，特予如下奖励，还请及时查收。",
        "isOpen": 1,
        "rewardId": 0,
        "period": "360",
        "event": "",
        "parm": ""
    }),
    37990001: _tools.RODict({
        "ID": 37990001,
        "type": 2,
        "title": "链接测试1",
        "content": "<link查看任务>",
        "isOpen": 1,
        "rewardId": 0,
        "period": "2025-05-31-23-59",
        "event": "Openinterface",
        "parm": "UITaskInfoPanel"
    })
})
minKey = 37000001
maxKey = 37990001

MailArgsNumMap = _tools.RODict({ 
        37000001:0,
        37000002:0,
        37000003:0,
        37000004:1,
        37000005:0,
        37000006:2,
        37000007:1,
        37000008:5,
        37000009:3,
        37000010:1,
        37000011:2,
        37000012:1,
        37000013:0,
        37000014:1,
        37000015:0,
        37000016:0,
        37000017:2,
        37000018:1,
        37000019:1,
        37000020:1,
        37000030:1,
        37001001:0,
        37001002:0,
        37001003:0,
        37001004:2,
        37001005:4,
        37001006:7,
        37001007:1,
        37001008:0,
        37001009:0,
        37001010:3,
        37001011:0,
        37001012:0,
        37001013:1,
        37001014:0,
        37001015:4,
        37001016:6,
        37001017:0,
        37001018:2,
        37001019:2,
        37001020:1,
        37990001:0,
})
