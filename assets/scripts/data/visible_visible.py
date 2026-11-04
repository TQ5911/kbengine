# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: visible/visible
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "_": _tools.RODict({
        "function": "_",
        "type": "_",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "x": _tools.RODict({
        "function": "x",
        "type": "_",
        "level": 999,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIBagPanel": _tools.RODict({
        "function": "UIBagPanel",
        "type": "bag",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 1
    }),
    "ChangeTarget": _tools.RODict({
        "function": "ChangeTarget",
        "type": "changeTarget",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 1
    }),
    "UI_camera": _tools.RODict({
        "function": "UI_camera",
        "type": "UI_camera",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 2,
        "demon": 0
    }),
    "UI_cards": _tools.RODict({
        "function": "UI_cards",
        "type": "UI_cards",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 2,
        "demon": 0
    }),
    "UI_hp": _tools.RODict({
        "function": "UI_hp",
        "type": "UI_hp",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 2,
        "demon": 0
    }),
    "UI_level": _tools.RODict({
        "function": "UI_level",
        "type": "UI_level",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 2,
        "demon": 0
    }),
    "UI_score": _tools.RODict({
        "function": "UI_score",
        "type": "UI_score",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 2,
        "demon": 0
    }),
    "QuickSettings": _tools.RODict({
        "function": "QuickSettings",
        "type": "quickSettings",
        "level": 0,
        "task": 86010006,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "queueServer": _tools.RODict({
        "function": "queueServer",
        "type": "queueServer",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "photograph": _tools.RODict({
        "function": "photograph",
        "type": "photograph",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "shareBtn": _tools.RODict({
        "function": "shareBtn",
        "type": "shareBtn",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "shareSystem": _tools.RODict({
        "function": "shareSystem",
        "type": "shareSystem",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "Enemy": _tools.RODict({
        "function": "Enemy",
        "type": "enemy",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "Duel": _tools.RODict({
        "function": "Duel",
        "type": "duel",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "TenSign": _tools.RODict({
        "function": "TenSign",
        "type": "welfare_tenSign",
        "level": 999,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "Meridian": _tools.RODict({
        "function": "Meridian",
        "type": "UIPracticePanel",
        "level": 0,
        "task": 86030033,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "Attention": _tools.RODict({
        "function": "Attention",
        "type": "welfare_attention",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "phoneBind": _tools.RODict({
        "function": "phoneBind",
        "type": "welfare_phoneBind",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "LevelReward": _tools.RODict({
        "function": "LevelReward",
        "type": "welfare_levelReward",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "Questionnaire": _tools.RODict({
        "function": "Questionnaire",
        "type": "questionnaire",
        "level": 25,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "PcLoginReward": _tools.RODict({
        "function": "PcLoginReward",
        "type": "welfare_pcLogin",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "ResourceRecovery": _tools.RODict({
        "function": "ResourceRecovery",
        "type": "welfare_resourceRecovery",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIActivitiesPanel": _tools.RODict({
        "function": "UIActivitiesPanel",
        "type": "welfare",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "SevenSign": _tools.RODict({
        "function": "SevenSign",
        "type": "welfare_sevenSign",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UISkillSystemPanel": _tools.RODict({
        "function": "UISkillSystemPanel",
        "type": "skillUpgrade",
        "level": 0,
        "task": 86030027,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIRewardTaskPanel": _tools.RODict({
        "function": "UIRewardTaskPanel",
        "type": "rewardTask",
        "level": 19,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "Stronger": _tools.RODict({
        "function": "Stronger",
        "type": "stronger",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIAppearancePanel": _tools.RODict({
        "function": "UIAppearancePanel",
        "type": "appearance",
        "level": 0,
        "task": 86030030,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIDrawPetPanel": _tools.RODict({
        "function": "UIDrawPetPanel",
        "type": "drawPet",
        "level": 0,
        "task": 86030011,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIPetPanel": _tools.RODict({
        "function": "UIPetPanel",
        "type": "pet",
        "level": 0,
        "task": 86030009,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIEquipTrainingPanel": _tools.RODict({
        "function": "UIEquipTrainingPanel",
        "type": "equip",
        "level": 0,
        "task": 86030038,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIEquipMakePanel": _tools.RODict({
        "function": "UIEquipMakePanel",
        "type": "equip_make",
        "level": 0,
        "task": 86030028,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIEquipWashPanel": _tools.RODict({
        "function": "UIEquipWashPanel",
        "type": "equip_unbundle",
        "level": 29,
        "task": 86030038,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UITaskPanel": _tools.RODict({
        "function": "UITaskPanel",
        "type": "task",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UITaskInfoPanel": _tools.RODict({
        "function": "UITaskInfoPanel",
        "type": "task",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "Team": _tools.RODict({
        "function": "Team",
        "type": "team",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 2,
        "demon": 0
    }),
    "UIWarehousePanel": _tools.RODict({
        "function": "UIWarehousePanel",
        "type": "warehouse",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "ExitDun": _tools.RODict({
        "function": "ExitDun",
        "type": "exitDun",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIAttributePanel": _tools.RODict({
        "function": "UIAttributePanel",
        "type": "myPage",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIFriendPanel": _tools.RODict({
        "function": "UIFriendPanel",
        "type": "friend",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "GrowthGuide": _tools.RODict({
        "function": "GrowthGuide",
        "type": "growth",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "Chat": _tools.RODict({
        "function": "Chat",
        "type": "chat",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIAchievementPanel": _tools.RODict({
        "function": "UIAchievementPanel",
        "type": "achievement",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "Line": _tools.RODict({
        "function": "Line",
        "type": "line",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIMailPanel": _tools.RODict({
        "function": "UIMailPanel",
        "type": "mail",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIMapPanel": _tools.RODict({
        "function": "UIMapPanel",
        "type": "map",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIPayStorePanel": _tools.RODict({
        "function": "UIPayStorePanel",
        "type": "pay",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIPKProtectPanel": _tools.RODict({
        "function": "UIPKProtectPanel",
        "type": "pkProtect",
        "level": 0,
        "task": 86060137,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIPortableSetPanel": _tools.RODict({
        "function": "UIPortableSetPanel",
        "type": "quickSettings",
        "level": 0,
        "task": 86010006,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "Raid": _tools.RODict({
        "function": "Raid",
        "type": "raid",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 2,
        "demon": 0
    }),
    "UIRankPanel": _tools.RODict({
        "function": "UIRankPanel",
        "type": "rank",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "DeathDrop": _tools.RODict({
        "function": "DeathDrop",
        "type": "deathDrop",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "AutoCombat": _tools.RODict({
        "function": "AutoCombat",
        "type": "autoCombat",
        "level": 0,
        "task": 86030032,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "AutoCollect": _tools.RODict({
        "function": "AutoCollect",
        "type": "autoCollect",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIRedPacketPanel": _tools.RODict({
        "function": "UIRedPacketPanel",
        "type": "redPacket",
        "level": 9,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "MonthCard": _tools.RODict({
        "function": "MonthCard",
        "type": "monthCard",
        "level": 9,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "quickTips": _tools.RODict({
        "function": "quickTips",
        "type": "quickTips",
        "level": 9,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIPracticePanel": _tools.RODict({
        "function": "UIPracticePanel",
        "type": "UIPracticePanel",
        "level": 0,
        "task": 86030033,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIEquipIntensifyPage": _tools.RODict({
        "function": "UIEquipIntensifyPage",
        "type": "equip_strengthen",
        "level": 0,
        "task": 86030038,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "Guild": _tools.RODict({
        "function": "Guild",
        "type": "guild",
        "level": 18,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIGuildPanel": _tools.RODict({
        "function": "UIGuildPanel",
        "type": "guild",
        "level": 18,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIGuildLobbyPanel": _tools.RODict({
        "function": "UIGuildLobbyPanel",
        "type": "guild",
        "level": 18,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "Union": _tools.RODict({
        "function": "Union",
        "type": "guild_union",
        "level": 18,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UnionCrossServer": _tools.RODict({
        "function": "UnionCrossServer",
        "type": "guild_unionCrossServer",
        "level": 999,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UITeamDunPanel": _tools.RODict({
        "function": "UITeamDunPanel",
        "type": "teamDungeon",
        "level": 0,
        "task": 86010064,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UISquarePanel": _tools.RODict({
        "function": "UISquarePanel",
        "type": "square",
        "level": 20,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UICollectionPanel": _tools.RODict({
        "function": "UICollectionPanel",
        "type": "collection",
        "level": 0,
        "task": 86010005,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UISynthesisSystemPanel": _tools.RODict({
        "function": "UISynthesisSystemPanel",
        "type": "synthesis",
        "level": 16,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIPropMakePanel": _tools.RODict({
        "function": "UIPropMakePanel",
        "type": "workshop",
        "level": 15,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "GuildBossChallenge": _tools.RODict({
        "function": "GuildBossChallenge",
        "type": "guildBossChallenge",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIBusinessPanel": _tools.RODict({
        "function": "UIBusinessPanel",
        "type": "business",
        "level": 20,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIEquipClassPage": _tools.RODict({
        "function": "UIEquipClassPage",
        "type": "equip_class",
        "level": 19,
        "task": 86030038,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIWonderLandPanel": _tools.RODict({
        "function": "UIWonderLandPanel",
        "type": "wonderLand",
        "level": 25,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIEquipEnchantingPage": _tools.RODict({
        "function": "UIEquipEnchantingPage",
        "type": "equip_spirit",
        "level": 22,
        "task": 86030038,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UICrusadeSystemPanel": _tools.RODict({
        "function": "UICrusadeSystemPanel",
        "type": "raidDungeon",
        "level": 24,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIEquipRunePage": _tools.RODict({
        "function": "UIEquipRunePage",
        "type": "equip_weaponGlyph",
        "level": 27,
        "task": 86030038,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIEquipBlessPage": _tools.RODict({
        "function": "UIEquipBlessPage",
        "type": "equip_bless",
        "level": 28,
        "task": 86030038,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "MineBattle": _tools.RODict({
        "function": "MineBattle",
        "type": "mineBattle",
        "level": 30,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIMineBattleManagePanel": _tools.RODict({
        "function": "UIMineBattleManagePanel",
        "type": "mineBattle",
        "level": 30,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIRoleAuthorizationPanel": _tools.RODict({
        "function": "UIRoleAuthorizationPanel",
        "type": "roleAuthorization",
        "level": 30,
        "task": 86010002,
        "day": 0,
        "monthCard": 3,
        "secondPwd": 1,
        "switch": 0,
        "demon": 0
    }),
    "CityBattle": _tools.RODict({
        "function": "CityBattle",
        "type": "cityBattle",
        "level": 999,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UICityBattlePanel": _tools.RODict({
        "function": "UICityBattlePanel",
        "type": "cityBattle",
        "level": 999,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIAbyssPanel": _tools.RODict({
        "function": "UIAbyssPanel",
        "type": "abyss",
        "level": 45,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "GeneralAttack": _tools.RODict({
        "function": "GeneralAttack",
        "type": "skill",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "Dodge": _tools.RODict({
        "function": "Dodge",
        "type": "skill",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "Sprint": _tools.RODict({
        "function": "Sprint",
        "type": "skill",
        "level": 0,
        "task": 86060003,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "Jump": _tools.RODict({
        "function": "Jump",
        "type": "skill",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "Fly": _tools.RODict({
        "function": "Fly",
        "type": "skill",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "MageSkill01": _tools.RODict({
        "function": "MageSkill01",
        "type": "skillMage",
        "level": 0,
        "task": 86060055,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "MageSkill02": _tools.RODict({
        "function": "MageSkill02",
        "type": "skillMage",
        "level": 0,
        "task": 86060061,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "MageSkill03": _tools.RODict({
        "function": "MageSkill03",
        "type": "skillMage",
        "level": 0,
        "task": 86060070,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "MageSkill04": _tools.RODict({
        "function": "MageSkill04",
        "type": "skillMage",
        "level": 6,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "MageSkill05": _tools.RODict({
        "function": "MageSkill05",
        "type": "skillMage",
        "level": 10,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "MageSkill06": _tools.RODict({
        "function": "MageSkill06",
        "type": "skillMage",
        "level": 15,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "MageSkill07": _tools.RODict({
        "function": "MageSkill07",
        "type": "skillMage",
        "level": 20,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "MageSkill08": _tools.RODict({
        "function": "MageSkill08",
        "type": "skillMage",
        "level": 25,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "MageSkill09": _tools.RODict({
        "function": "MageSkill09",
        "type": "skillMage",
        "level": 30,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "MageSkill10": _tools.RODict({
        "function": "MageSkill10",
        "type": "skillMage",
        "level": 35,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "MageSkill11": _tools.RODict({
        "function": "MageSkill11",
        "type": "skillMage",
        "level": 40,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "MageSkill12": _tools.RODict({
        "function": "MageSkill12",
        "type": "skillMage",
        "level": 48,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "MageSkillUlt": _tools.RODict({
        "function": "MageSkillUlt",
        "type": "skillMage",
        "level": 0,
        "task": 86060098,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "TaoistSkill01": _tools.RODict({
        "function": "TaoistSkill01",
        "type": "skillTaoist",
        "level": 0,
        "task": 86060055,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "TaoistSkill02": _tools.RODict({
        "function": "TaoistSkill02",
        "type": "skillTaoist",
        "level": 0,
        "task": 86060061,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "TaoistSkill03": _tools.RODict({
        "function": "TaoistSkill03",
        "type": "skillTaoist",
        "level": 0,
        "task": 86060070,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "TaoistSkill04": _tools.RODict({
        "function": "TaoistSkill04",
        "type": "skillTaoist",
        "level": 6,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "TaoistSkill05": _tools.RODict({
        "function": "TaoistSkill05",
        "type": "skillTaoist",
        "level": 10,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "TaoistSkill06": _tools.RODict({
        "function": "TaoistSkill06",
        "type": "skillTaoist",
        "level": 15,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "TaoistSkill07": _tools.RODict({
        "function": "TaoistSkill07",
        "type": "skillTaoist",
        "level": 20,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "TaoistSkill08": _tools.RODict({
        "function": "TaoistSkill08",
        "type": "skillTaoist",
        "level": 25,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "TaoistSkill09": _tools.RODict({
        "function": "TaoistSkill09",
        "type": "skillTaoist",
        "level": 30,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "TaoistSkill10": _tools.RODict({
        "function": "TaoistSkill10",
        "type": "skillTaoist",
        "level": 35,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "TaoistSkill11": _tools.RODict({
        "function": "TaoistSkill11",
        "type": "skillTaoist",
        "level": 40,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "TaoistSkill12": _tools.RODict({
        "function": "TaoistSkill12",
        "type": "skillTaoist",
        "level": 48,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "TaoistSkillUlt": _tools.RODict({
        "function": "TaoistSkillUlt",
        "type": "skillTaoist",
        "level": 0,
        "task": 86060098,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "WarriorSkill01": _tools.RODict({
        "function": "WarriorSkill01",
        "type": "skillWarrior",
        "level": 0,
        "task": 86060055,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "WarriorSkill02": _tools.RODict({
        "function": "WarriorSkill02",
        "type": "skillWarrior",
        "level": 0,
        "task": 86060061,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "WarriorSkill03": _tools.RODict({
        "function": "WarriorSkill03",
        "type": "skillWarrior",
        "level": 0,
        "task": 86060070,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "WarriorSkill04": _tools.RODict({
        "function": "WarriorSkill04",
        "type": "skillWarrior",
        "level": 6,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "WarriorSkill05": _tools.RODict({
        "function": "WarriorSkill05",
        "type": "skillWarrior",
        "level": 10,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "WarriorSkill06": _tools.RODict({
        "function": "WarriorSkill06",
        "type": "skillWarrior",
        "level": 15,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "WarriorSkill07": _tools.RODict({
        "function": "WarriorSkill07",
        "type": "skillWarrior",
        "level": 20,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "WarriorSkill08": _tools.RODict({
        "function": "WarriorSkill08",
        "type": "skillWarrior",
        "level": 25,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "WarriorSkill09": _tools.RODict({
        "function": "WarriorSkill09",
        "type": "skillWarrior",
        "level": 30,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "WarriorSkill10": _tools.RODict({
        "function": "WarriorSkill10",
        "type": "skillWarrior",
        "level": 35,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "WarriorSkill11": _tools.RODict({
        "function": "WarriorSkill11",
        "type": "skillWarrior",
        "level": 40,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "WarriorSkill12": _tools.RODict({
        "function": "WarriorSkill12",
        "type": "skillWarrior",
        "level": 48,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "WarriorSkillUlt": _tools.RODict({
        "function": "WarriorSkillUlt",
        "type": "skillWarrior",
        "level": 0,
        "task": 86060098,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "xinyuanchengopentask": _tools.RODict({
        "function": "xinyuanchengopentask",
        "type": "mapTask",
        "level": 0,
        "task": 86060137,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "tongxingguopentask": _tools.RODict({
        "function": "tongxingguopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "feishayaosaiopentask": _tools.RODict({
        "function": "feishayaosaiopentask",
        "type": "mapTask",
        "level": 35,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "jinglingcunopentask": _tools.RODict({
        "function": "jinglingcunopentask",
        "type": "mapTask",
        "level": 0,
        "task": 86010087,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "jinglingbaodianopentask": _tools.RODict({
        "function": "jinglingbaodianopentask",
        "type": "mapTask",
        "level": 0,
        "task": 86010087,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "shikuzoulangopentask": _tools.RODict({
        "function": "shikuzoulangopentask",
        "type": "mapTask",
        "level": 35,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "xinyuanchenjiaoopentask": _tools.RODict({
        "function": "xinyuanchenjiaoopentask",
        "type": "mapTask",
        "level": 25,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "zuke1Fopentask": _tools.RODict({
        "function": "zuke1Fopentask",
        "type": "mapTask",
        "level": 26,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "zuke2Fopentask": _tools.RODict({
        "function": "zuke2Fopentask",
        "type": "mapTask",
        "level": 26,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "zuke3Fopentask": _tools.RODict({
        "function": "zuke3Fopentask",
        "type": "mapTask",
        "level": 26,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "zuke4Fopentask": _tools.RODict({
        "function": "zuke4Fopentask",
        "type": "mapTask",
        "level": 26,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "zuke5Fopentask": _tools.RODict({
        "function": "zuke5Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "zuke6Fopentask": _tools.RODict({
        "function": "zuke6Fopentask",
        "type": "mapTask",
        "level": 40,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "yueguang1Fopentask": _tools.RODict({
        "function": "yueguang1Fopentask",
        "type": "mapTask",
        "level": 10,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "yueguang2Fopentask": _tools.RODict({
        "function": "yueguang2Fopentask",
        "type": "mapTask",
        "level": 22,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "yueguang3Fopentask": _tools.RODict({
        "function": "yueguang3Fopentask",
        "type": "mapTask",
        "level": 26,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "yueguang4Fopentask": _tools.RODict({
        "function": "yueguang4Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "yueguang5Fopentask": _tools.RODict({
        "function": "yueguang5Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "wudu1Fopentask": _tools.RODict({
        "function": "wudu1Fopentask",
        "type": "mapTask",
        "level": 40,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "wudu2Fopentask": _tools.RODict({
        "function": "wudu2Fopentask",
        "type": "mapTask",
        "level": 44,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "wudu3Fopentask": _tools.RODict({
        "function": "wudu3Fopentask",
        "type": "mapTask",
        "level": 48,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "liusha1Fopentask": _tools.RODict({
        "function": "liusha1Fopentask",
        "type": "mapTask",
        "level": 60,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "liusha2Fopentask": _tools.RODict({
        "function": "liusha2Fopentask",
        "type": "mapTask",
        "level": 60,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "liusha3Fopentask": _tools.RODict({
        "function": "liusha3Fopentask",
        "type": "mapTask",
        "level": 60,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "liusha4Fopentask": _tools.RODict({
        "function": "liusha4Fopentask",
        "type": "mapTask",
        "level": 60,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UISettingsPanel": _tools.RODict({
        "function": "UISettingsPanel",
        "type": "settings",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIRedeemCodePanel": _tools.RODict({
        "function": "UIRedeemCodePanel",
        "type": "settings_giftKey",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIMainMenu": _tools.RODict({
        "function": "UIMainMenu",
        "type": "menu",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "HotGift": _tools.RODict({
        "function": "HotGift",
        "type": "pay_hotGift",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "HolidayGift": _tools.RODict({
        "function": "HolidayGift",
        "type": "pay_holidayGift",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "Rmb": _tools.RODict({
        "function": "Rmb",
        "type": "pay_rmb",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIGrowthGuidePanel": _tools.RODict({
        "function": "UIGrowthGuidePanel",
        "type": "stronger",
        "level": 10,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "PKStateArea": _tools.RODict({
        "function": "PKStateArea",
        "type": "PKState",
        "level": 0,
        "task": 86060137,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 2,
        "demon": 0
    }),
    "UISocialPanel": _tools.RODict({
        "function": "UISocialPanel",
        "type": "chat",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "Hotkey": _tools.RODict({
        "function": "Hotkey",
        "type": "settings_hotKey",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "MountBtn": _tools.RODict({
        "function": "MountBtn",
        "type": "appearance",
        "level": 0,
        "task": 86010027,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "CardChangeBtn": _tools.RODict({
        "function": "CardChangeBtn",
        "type": "pet",
        "level": 0,
        "task": 86030011,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIDeathPunishmentPanel": _tools.RODict({
        "function": "UIDeathPunishmentPanel",
        "type": "deathDrop",
        "level": 0,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIMainLockPanel": _tools.RODict({
        "function": "UIMainLockPanel",
        "type": "mainLock",
        "level": 15,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "CurrencyExchange": _tools.RODict({
        "function": "CurrencyExchange",
        "type": "currencyExchange",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "worldLevel": _tools.RODict({
        "function": "worldLevel",
        "type": "worldLevel",
        "level": 50,
        "task": 0,
        "day": 1,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIActivityNotice": _tools.RODict({
        "function": "UIActivityNotice",
        "type": "activityNotice",
        "level": 30,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "UIWorldBoss": _tools.RODict({
        "function": "UIWorldBoss",
        "type": "worldBoss",
        "level": 30,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIEquipSoul": _tools.RODict({
        "function": "UIEquipSoul",
        "type": "equip_soul",
        "level": 23,
        "task": 86030038,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "Rental": _tools.RODict({
        "function": "Rental",
        "type": "lease",
        "level": 25,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIReportPanel": _tools.RODict({
        "function": "UIReportPanel",
        "type": "report",
        "level": 20,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 2,
        "demon": 0
    }),
    "WorldTrumpet": _tools.RODict({
        "function": "WorldTrumpet",
        "type": "chat",
        "level": 9,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIRoleAppearancePanel": _tools.RODict({
        "function": "UIRoleAppearancePanel",
        "type": "appearance",
        "level": 999,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIBountyPanel": _tools.RODict({
        "function": "UIBountyPanel",
        "type": "order",
        "level": 20,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "RefundRecharge": _tools.RODict({
        "function": "RefundRecharge",
        "type": "welfare_refundRecharge",
        "level": 999,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIActionVideoPanel": _tools.RODict({
        "function": "UIActionVideoPanel",
        "type": "posture",
        "level": 999,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "Operation": _tools.RODict({
        "function": "Operation",
        "type": "settings_operation",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "ModeChange": _tools.RODict({
        "function": "ModeChange",
        "type": "modeChange",
        "level": 20,
        "task": 86060137,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIPetReshapeTipPanel": _tools.RODict({
        "function": "UIPetReshapeTipPanel",
        "type": "pet",
        "level": 0,
        "task": 86030009,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 1,
        "demon": 0
    }),
    "PowerRush": _tools.RODict({
        "function": "PowerRush",
        "type": "welfare_powerpankpanel",
        "level": 999,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "VocabularyBlock": _tools.RODict({
        "function": "VocabularyBlock",
        "type": "vocabularyBlock",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "secondPwd": _tools.RODict({
        "function": "secondPwd",
        "type": "settings_secondPwd",
        "level": 0,
        "task": 0,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "ReturnReward": _tools.RODict({
        "function": "ReturnReward",
        "type": "welfare_returnReward",
        "level": 20,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIDrawMountsPanel": _tools.RODict({
        "function": "UIDrawMountsPanel",
        "type": "drawMount",
        "level": 0,
        "task": 86030011,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIBattlePassPanel": _tools.RODict({
        "function": "UIBattlePassPanel",
        "type": "battlePass",
        "level": 35,
        "task": 86010002,
        "day": 3,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "phaseTask1": _tools.RODict({
        "function": "phaseTask1",
        "type": "beginnerJourneyTask",
        "level": 19,
        "task": 0,
        "day": 1,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "phaseTask2": _tools.RODict({
        "function": "phaseTask2",
        "type": "beginnerJourneyTask",
        "level": 23,
        "task": 0,
        "day": 1,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "phaseTask3": _tools.RODict({
        "function": "phaseTask3",
        "type": "beginnerJourneyTask",
        "level": 27,
        "task": 0,
        "day": 2,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "phaseTask4": _tools.RODict({
        "function": "phaseTask4",
        "type": "beginnerJourneyTask",
        "level": 30,
        "task": 0,
        "day": 2,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "phaseTask5": _tools.RODict({
        "function": "phaseTask5",
        "type": "beginnerJourneyTask",
        "level": 32,
        "task": 0,
        "day": 3,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "phaseTask6": _tools.RODict({
        "function": "phaseTask6",
        "type": "beginnerJourneyTask",
        "level": 34,
        "task": 0,
        "day": 4,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "phaseTask7": _tools.RODict({
        "function": "phaseTask7",
        "type": "beginnerJourneyTask",
        "level": 36,
        "task": 0,
        "day": 5,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "phaseTask8": _tools.RODict({
        "function": "phaseTask8",
        "type": "beginnerJourneyTask",
        "level": 38,
        "task": 0,
        "day": 6,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "phaseTask9": _tools.RODict({
        "function": "phaseTask9",
        "type": "beginnerJourneyTask",
        "level": 40,
        "task": 0,
        "day": 7,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "beginnerJourney": _tools.RODict({
        "function": "beginnerJourney",
        "type": "beginnerJourneyTask",
        "level": 19,
        "task": 0,
        "day": 1,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "UIEquipSoulWashPanel": _tools.RODict({
        "function": "UIEquipSoulWashPanel",
        "type": "equip_soulWash",
        "level": 30,
        "task": 86030038,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "Affiliate": _tools.RODict({
        "function": "Affiliate",
        "type": "welfare_affiliate",
        "level": 20,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    }),
    "MaterialSale": _tools.RODict({
        "function": "MaterialSale",
        "type": "pay_materialSale",
        "level": 20,
        "task": 86010002,
        "day": 0,
        "monthCard": 0,
        "secondPwd": 0,
        "switch": 0,
        "demon": 0
    })
})


UIBagPanel = 0
ChangeTarget = 1
UI_camera = 2
UI_cards = 3
UI_hp = 4
UI_level = 5
UI_score = 6
QuickSettings = 7
queueServer = 8
photograph = 9
shareBtn = 10
shareSystem = 11
Enemy = 12
Duel = 13
TenSign = 14
Meridian = 15
Attention = 16
phoneBind = 17
LevelReward = 18
Questionnaire = 19
PcLoginReward = 20
ResourceRecovery = 21
UIActivitiesPanel = 22
SevenSign = 23
UISkillSystemPanel = 24
UIRewardTaskPanel = 25
Stronger = 26
UIAppearancePanel = 27
UIDrawPetPanel = 28
UIPetPanel = 29
UIEquipTrainingPanel = 30
UIEquipMakePanel = 31
UIEquipWashPanel = 32
UITaskPanel = 33
UITaskInfoPanel = 34
Team = 35
UIWarehousePanel = 36
ExitDun = 37
UIAttributePanel = 38
UIFriendPanel = 39
GrowthGuide = 40
Chat = 41
UIAchievementPanel = 42
Line = 43
UIMailPanel = 44
UIMapPanel = 45
UIPayStorePanel = 46
UIPKProtectPanel = 47
UIPortableSetPanel = 48
Raid = 49
UIRankPanel = 50
DeathDrop = 51
AutoCombat = 52
AutoCollect = 53
UIRedPacketPanel = 54
MonthCard = 55
quickTips = 56
UIPracticePanel = 57
UIEquipIntensifyPage = 58
Guild = 59
UIGuildPanel = 60
UIGuildLobbyPanel = 61
Union = 62
UnionCrossServer = 63
UITeamDunPanel = 64
UISquarePanel = 65
UICollectionPanel = 66
UISynthesisSystemPanel = 67
UIPropMakePanel = 68
GuildBossChallenge = 69
UIBusinessPanel = 70
UIEquipClassPage = 71
UIWonderLandPanel = 72
UIEquipEnchantingPage = 73
UICrusadeSystemPanel = 74
UIEquipRunePage = 75
UIEquipBlessPage = 76
MineBattle = 77
UIMineBattleManagePanel = 78
UIRoleAuthorizationPanel = 79
CityBattle = 80
UICityBattlePanel = 81
UIAbyssPanel = 82
GeneralAttack = 83
Dodge = 84
Sprint = 85
Jump = 86
Fly = 87
MageSkill01 = 88
MageSkill02 = 89
MageSkill03 = 90
MageSkill04 = 91
MageSkill05 = 92
MageSkill06 = 93
MageSkill07 = 94
MageSkill08 = 95
MageSkill09 = 96
MageSkill10 = 97
MageSkill11 = 98
MageSkill12 = 99
MageSkillUlt = 100
TaoistSkill01 = 101
TaoistSkill02 = 102
TaoistSkill03 = 103
TaoistSkill04 = 104
TaoistSkill05 = 105
TaoistSkill06 = 106
TaoistSkill07 = 107
TaoistSkill08 = 108
TaoistSkill09 = 109
TaoistSkill10 = 110
TaoistSkill11 = 111
TaoistSkill12 = 112
TaoistSkillUlt = 113
WarriorSkill01 = 114
WarriorSkill02 = 115
WarriorSkill03 = 116
WarriorSkill04 = 117
WarriorSkill05 = 118
WarriorSkill06 = 119
WarriorSkill07 = 120
WarriorSkill08 = 121
WarriorSkill09 = 122
WarriorSkill10 = 123
WarriorSkill11 = 124
WarriorSkill12 = 125
WarriorSkillUlt = 126
xinyuanchengopentask = 127
tongxingguopentask = 128
feishayaosaiopentask = 129
jinglingcunopentask = 130
jinglingbaodianopentask = 131
shikuzoulangopentask = 132
xinyuanchenjiaoopentask = 133
zuke1Fopentask = 134
zuke2Fopentask = 135
zuke3Fopentask = 136
zuke4Fopentask = 137
zuke5Fopentask = 138
zuke6Fopentask = 139
yueguang1Fopentask = 140
yueguang2Fopentask = 141
yueguang3Fopentask = 142
yueguang4Fopentask = 143
yueguang5Fopentask = 144
wudu1Fopentask = 145
wudu2Fopentask = 146
wudu3Fopentask = 147
liusha1Fopentask = 148
liusha2Fopentask = 149
liusha3Fopentask = 150
liusha4Fopentask = 151
UISettingsPanel = 152
UIRedeemCodePanel = 153
UIMainMenu = 154
HotGift = 155
HolidayGift = 156
Rmb = 157
UIGrowthGuidePanel = 158
PKStateArea = 159
UISocialPanel = 160
Hotkey = 161
MountBtn = 162
CardChangeBtn = 163
UIDeathPunishmentPanel = 164
UIMainLockPanel = 165
CurrencyExchange = 166
worldLevel = 167
UIActivityNotice = 168
UIWorldBoss = 169
UIEquipSoul = 170
Rental = 171
UIReportPanel = 172
WorldTrumpet = 173
UIRoleAppearancePanel = 174
UIBountyPanel = 175
RefundRecharge = 176
UIActionVideoPanel = 177
Operation = 178
ModeChange = 179
UIPetReshapeTipPanel = 180
PowerRush = 181
VocabularyBlock = 182
secondPwd = 183
ReturnReward = 184
UIDrawMountsPanel = 185
UIBattlePassPanel = 186
phaseTask1 = 187
phaseTask2 = 188
phaseTask3 = 189
phaseTask4 = 190
phaseTask5 = 191
phaseTask6 = 192
phaseTask7 = 193
phaseTask8 = 194
phaseTask9 = 195
beginnerJourney = 196
UIEquipSoulWashPanel = 197
Affiliate = 198
MaterialSale = 199



funcDic = _tools.RODict({
    "UIBagPanel" : 0,
    "ChangeTarget" : 1,
    "UI_camera" : 2,
    "UI_cards" : 3,
    "UI_hp" : 4,
    "UI_level" : 5,
    "UI_score" : 6,
    "QuickSettings" : 7,
    "queueServer" : 8,
    "photograph" : 9,
    "shareBtn" : 10,
    "shareSystem" : 11,
    "Enemy" : 12,
    "Duel" : 13,
    "TenSign" : 14,
    "Meridian" : 15,
    "Attention" : 16,
    "phoneBind" : 17,
    "LevelReward" : 18,
    "Questionnaire" : 19,
    "PcLoginReward" : 20,
    "ResourceRecovery" : 21,
    "UIActivitiesPanel" : 22,
    "SevenSign" : 23,
    "UISkillSystemPanel" : 24,
    "UIRewardTaskPanel" : 25,
    "Stronger" : 26,
    "UIAppearancePanel" : 27,
    "UIDrawPetPanel" : 28,
    "UIPetPanel" : 29,
    "UIEquipTrainingPanel" : 30,
    "UIEquipMakePanel" : 31,
    "UIEquipWashPanel" : 32,
    "UITaskPanel" : 33,
    "UITaskInfoPanel" : 34,
    "Team" : 35,
    "UIWarehousePanel" : 36,
    "ExitDun" : 37,
    "UIAttributePanel" : 38,
    "UIFriendPanel" : 39,
    "GrowthGuide" : 40,
    "Chat" : 41,
    "UIAchievementPanel" : 42,
    "Line" : 43,
    "UIMailPanel" : 44,
    "UIMapPanel" : 45,
    "UIPayStorePanel" : 46,
    "UIPKProtectPanel" : 47,
    "UIPortableSetPanel" : 48,
    "Raid" : 49,
    "UIRankPanel" : 50,
    "DeathDrop" : 51,
    "AutoCombat" : 52,
    "AutoCollect" : 53,
    "UIRedPacketPanel" : 54,
    "MonthCard" : 55,
    "quickTips" : 56,
    "UIPracticePanel" : 57,
    "UIEquipIntensifyPage" : 58,
    "Guild" : 59,
    "UIGuildPanel" : 60,
    "UIGuildLobbyPanel" : 61,
    "Union" : 62,
    "UnionCrossServer" : 63,
    "UITeamDunPanel" : 64,
    "UISquarePanel" : 65,
    "UICollectionPanel" : 66,
    "UISynthesisSystemPanel" : 67,
    "UIPropMakePanel" : 68,
    "GuildBossChallenge" : 69,
    "UIBusinessPanel" : 70,
    "UIEquipClassPage" : 71,
    "UIWonderLandPanel" : 72,
    "UIEquipEnchantingPage" : 73,
    "UICrusadeSystemPanel" : 74,
    "UIEquipRunePage" : 75,
    "UIEquipBlessPage" : 76,
    "MineBattle" : 77,
    "UIMineBattleManagePanel" : 78,
    "UIRoleAuthorizationPanel" : 79,
    "CityBattle" : 80,
    "UICityBattlePanel" : 81,
    "UIAbyssPanel" : 82,
    "GeneralAttack" : 83,
    "Dodge" : 84,
    "Sprint" : 85,
    "Jump" : 86,
    "Fly" : 87,
    "MageSkill01" : 88,
    "MageSkill02" : 89,
    "MageSkill03" : 90,
    "MageSkill04" : 91,
    "MageSkill05" : 92,
    "MageSkill06" : 93,
    "MageSkill07" : 94,
    "MageSkill08" : 95,
    "MageSkill09" : 96,
    "MageSkill10" : 97,
    "MageSkill11" : 98,
    "MageSkill12" : 99,
    "MageSkillUlt" : 100,
    "TaoistSkill01" : 101,
    "TaoistSkill02" : 102,
    "TaoistSkill03" : 103,
    "TaoistSkill04" : 104,
    "TaoistSkill05" : 105,
    "TaoistSkill06" : 106,
    "TaoistSkill07" : 107,
    "TaoistSkill08" : 108,
    "TaoistSkill09" : 109,
    "TaoistSkill10" : 110,
    "TaoistSkill11" : 111,
    "TaoistSkill12" : 112,
    "TaoistSkillUlt" : 113,
    "WarriorSkill01" : 114,
    "WarriorSkill02" : 115,
    "WarriorSkill03" : 116,
    "WarriorSkill04" : 117,
    "WarriorSkill05" : 118,
    "WarriorSkill06" : 119,
    "WarriorSkill07" : 120,
    "WarriorSkill08" : 121,
    "WarriorSkill09" : 122,
    "WarriorSkill10" : 123,
    "WarriorSkill11" : 124,
    "WarriorSkill12" : 125,
    "WarriorSkillUlt" : 126,
    "xinyuanchengopentask" : 127,
    "tongxingguopentask" : 128,
    "feishayaosaiopentask" : 129,
    "jinglingcunopentask" : 130,
    "jinglingbaodianopentask" : 131,
    "shikuzoulangopentask" : 132,
    "xinyuanchenjiaoopentask" : 133,
    "zuke1Fopentask" : 134,
    "zuke2Fopentask" : 135,
    "zuke3Fopentask" : 136,
    "zuke4Fopentask" : 137,
    "zuke5Fopentask" : 138,
    "zuke6Fopentask" : 139,
    "yueguang1Fopentask" : 140,
    "yueguang2Fopentask" : 141,
    "yueguang3Fopentask" : 142,
    "yueguang4Fopentask" : 143,
    "yueguang5Fopentask" : 144,
    "wudu1Fopentask" : 145,
    "wudu2Fopentask" : 146,
    "wudu3Fopentask" : 147,
    "liusha1Fopentask" : 148,
    "liusha2Fopentask" : 149,
    "liusha3Fopentask" : 150,
    "liusha4Fopentask" : 151,
    "UISettingsPanel" : 152,
    "UIRedeemCodePanel" : 153,
    "UIMainMenu" : 154,
    "HotGift" : 155,
    "HolidayGift" : 156,
    "Rmb" : 157,
    "UIGrowthGuidePanel" : 158,
    "PKStateArea" : 159,
    "UISocialPanel" : 160,
    "Hotkey" : 161,
    "MountBtn" : 162,
    "CardChangeBtn" : 163,
    "UIDeathPunishmentPanel" : 164,
    "UIMainLockPanel" : 165,
    "CurrencyExchange" : 166,
    "worldLevel" : 167,
    "UIActivityNotice" : 168,
    "UIWorldBoss" : 169,
    "UIEquipSoul" : 170,
    "Rental" : 171,
    "UIReportPanel" : 172,
    "WorldTrumpet" : 173,
    "UIRoleAppearancePanel" : 174,
    "UIBountyPanel" : 175,
    "RefundRecharge" : 176,
    "UIActionVideoPanel" : 177,
    "Operation" : 178,
    "ModeChange" : 179,
    "UIPetReshapeTipPanel" : 180,
    "PowerRush" : 181,
    "VocabularyBlock" : 182,
    "secondPwd" : 183,
    "ReturnReward" : 184,
    "UIDrawMountsPanel" : 185,
    "UIBattlePassPanel" : 186,
    "phaseTask1" : 187,
    "phaseTask2" : 188,
    "phaseTask3" : 189,
    "phaseTask4" : 190,
    "phaseTask5" : 191,
    "phaseTask6" : 192,
    "phaseTask7" : 193,
    "phaseTask8" : 194,
    "phaseTask9" : 195,
    "beginnerJourney" : 196,
    "UIEquipSoulWashPanel" : 197,
    "Affiliate" : 198,
    "MaterialSale" : 199,
})
demonDic = _tools.RODict({
    "bag" : 1,
    "changeTarget" : 1,
})
typeToBitsDic = _tools.RODict({
    "bag" : _tools.RODict({
        1 : _tools.ROList([
            0,
        ]),
    }),
    "changeTarget" : _tools.RODict({
        1 : _tools.ROList([
            0,
        ]),
    }),
})
reverseFuncDic = _tools.RODict({
    0 : "UIBagPanel",
    1 : "ChangeTarget",
    2 : "UI_camera",
    3 : "UI_cards",
    4 : "UI_hp",
    5 : "UI_level",
    6 : "UI_score",
    7 : "QuickSettings",
    8 : "queueServer",
    9 : "photograph",
    10 : "shareBtn",
    11 : "shareSystem",
    12 : "Enemy",
    13 : "Duel",
    14 : "TenSign",
    15 : "Meridian",
    16 : "Attention",
    17 : "phoneBind",
    18 : "LevelReward",
    19 : "Questionnaire",
    20 : "PcLoginReward",
    21 : "ResourceRecovery",
    22 : "UIActivitiesPanel",
    23 : "SevenSign",
    24 : "UISkillSystemPanel",
    25 : "UIRewardTaskPanel",
    26 : "Stronger",
    27 : "UIAppearancePanel",
    28 : "UIDrawPetPanel",
    29 : "UIPetPanel",
    30 : "UIEquipTrainingPanel",
    31 : "UIEquipMakePanel",
    32 : "UIEquipWashPanel",
    33 : "UITaskPanel",
    34 : "UITaskInfoPanel",
    35 : "Team",
    36 : "UIWarehousePanel",
    37 : "ExitDun",
    38 : "UIAttributePanel",
    39 : "UIFriendPanel",
    40 : "GrowthGuide",
    41 : "Chat",
    42 : "UIAchievementPanel",
    43 : "Line",
    44 : "UIMailPanel",
    45 : "UIMapPanel",
    46 : "UIPayStorePanel",
    47 : "UIPKProtectPanel",
    48 : "UIPortableSetPanel",
    49 : "Raid",
    50 : "UIRankPanel",
    51 : "DeathDrop",
    52 : "AutoCombat",
    53 : "AutoCollect",
    54 : "UIRedPacketPanel",
    55 : "MonthCard",
    56 : "quickTips",
    57 : "UIPracticePanel",
    58 : "UIEquipIntensifyPage",
    59 : "Guild",
    60 : "UIGuildPanel",
    61 : "UIGuildLobbyPanel",
    62 : "Union",
    63 : "UnionCrossServer",
    64 : "UITeamDunPanel",
    65 : "UISquarePanel",
    66 : "UICollectionPanel",
    67 : "UISynthesisSystemPanel",
    68 : "UIPropMakePanel",
    69 : "GuildBossChallenge",
    70 : "UIBusinessPanel",
    71 : "UIEquipClassPage",
    72 : "UIWonderLandPanel",
    73 : "UIEquipEnchantingPage",
    74 : "UICrusadeSystemPanel",
    75 : "UIEquipRunePage",
    76 : "UIEquipBlessPage",
    77 : "MineBattle",
    78 : "UIMineBattleManagePanel",
    79 : "UIRoleAuthorizationPanel",
    80 : "CityBattle",
    81 : "UICityBattlePanel",
    82 : "UIAbyssPanel",
    83 : "GeneralAttack",
    84 : "Dodge",
    85 : "Sprint",
    86 : "Jump",
    87 : "Fly",
    88 : "MageSkill01",
    89 : "MageSkill02",
    90 : "MageSkill03",
    91 : "MageSkill04",
    92 : "MageSkill05",
    93 : "MageSkill06",
    94 : "MageSkill07",
    95 : "MageSkill08",
    96 : "MageSkill09",
    97 : "MageSkill10",
    98 : "MageSkill11",
    99 : "MageSkill12",
    100 : "MageSkillUlt",
    101 : "TaoistSkill01",
    102 : "TaoistSkill02",
    103 : "TaoistSkill03",
    104 : "TaoistSkill04",
    105 : "TaoistSkill05",
    106 : "TaoistSkill06",
    107 : "TaoistSkill07",
    108 : "TaoistSkill08",
    109 : "TaoistSkill09",
    110 : "TaoistSkill10",
    111 : "TaoistSkill11",
    112 : "TaoistSkill12",
    113 : "TaoistSkillUlt",
    114 : "WarriorSkill01",
    115 : "WarriorSkill02",
    116 : "WarriorSkill03",
    117 : "WarriorSkill04",
    118 : "WarriorSkill05",
    119 : "WarriorSkill06",
    120 : "WarriorSkill07",
    121 : "WarriorSkill08",
    122 : "WarriorSkill09",
    123 : "WarriorSkill10",
    124 : "WarriorSkill11",
    125 : "WarriorSkill12",
    126 : "WarriorSkillUlt",
    127 : "xinyuanchengopentask",
    128 : "tongxingguopentask",
    129 : "feishayaosaiopentask",
    130 : "jinglingcunopentask",
    131 : "jinglingbaodianopentask",
    132 : "shikuzoulangopentask",
    133 : "xinyuanchenjiaoopentask",
    134 : "zuke1Fopentask",
    135 : "zuke2Fopentask",
    136 : "zuke3Fopentask",
    137 : "zuke4Fopentask",
    138 : "zuke5Fopentask",
    139 : "zuke6Fopentask",
    140 : "yueguang1Fopentask",
    141 : "yueguang2Fopentask",
    142 : "yueguang3Fopentask",
    143 : "yueguang4Fopentask",
    144 : "yueguang5Fopentask",
    145 : "wudu1Fopentask",
    146 : "wudu2Fopentask",
    147 : "wudu3Fopentask",
    148 : "liusha1Fopentask",
    149 : "liusha2Fopentask",
    150 : "liusha3Fopentask",
    151 : "liusha4Fopentask",
    152 : "UISettingsPanel",
    153 : "UIRedeemCodePanel",
    154 : "UIMainMenu",
    155 : "HotGift",
    156 : "HolidayGift",
    157 : "Rmb",
    158 : "UIGrowthGuidePanel",
    159 : "PKStateArea",
    160 : "UISocialPanel",
    161 : "Hotkey",
    162 : "MountBtn",
    163 : "CardChangeBtn",
    164 : "UIDeathPunishmentPanel",
    165 : "UIMainLockPanel",
    166 : "CurrencyExchange",
    167 : "worldLevel",
    168 : "UIActivityNotice",
    169 : "UIWorldBoss",
    170 : "UIEquipSoul",
    171 : "Rental",
    172 : "UIReportPanel",
    173 : "WorldTrumpet",
    174 : "UIRoleAppearancePanel",
    175 : "UIBountyPanel",
    176 : "RefundRecharge",
    177 : "UIActionVideoPanel",
    178 : "Operation",
    179 : "ModeChange",
    180 : "UIPetReshapeTipPanel",
    181 : "PowerRush",
    182 : "VocabularyBlock",
    183 : "secondPwd",
    184 : "ReturnReward",
    185 : "UIDrawMountsPanel",
    186 : "UIBattlePassPanel",
    187 : "phaseTask1",
    188 : "phaseTask2",
    189 : "phaseTask3",
    190 : "phaseTask4",
    191 : "phaseTask5",
    192 : "phaseTask6",
    193 : "phaseTask7",
    194 : "phaseTask8",
    195 : "phaseTask9",
    196 : "beginnerJourney",
    197 : "UIEquipSoulWashPanel",
    198 : "Affiliate",
    199 : "MaterialSale",
})
levelDic = _tools.RODict({
    999 : _tools.ROList([
        14,
        63,
        80,
        81,
        174,
        176,
        177,
        181,
    ]),
    25 : _tools.ROList([
        19,
        72,
        95,
        108,
        121,
        133,
        171,
    ]),
    19 : _tools.ROList([
        25,
        71,
        187,
        196,
    ]),
    29 : _tools.ROList([
        32,
    ]),
    9 : _tools.ROList([
        54,
        55,
        56,
        173,
    ]),
    18 : _tools.ROList([
        59,
        60,
        61,
        62,
    ]),
    20 : _tools.ROList([
        65,
        70,
        94,
        107,
        120,
        172,
        175,
        179,
        184,
        198,
        199,
    ]),
    16 : _tools.ROList([
        67,
    ]),
    15 : _tools.ROList([
        68,
        93,
        106,
        119,
        165,
    ]),
    22 : _tools.ROList([
        73,
        141,
    ]),
    24 : _tools.ROList([
        74,
    ]),
    27 : _tools.ROList([
        75,
        189,
    ]),
    28 : _tools.ROList([
        76,
    ]),
    30 : _tools.ROList([
        77,
        78,
        79,
        96,
        109,
        122,
        138,
        143,
        144,
        168,
        169,
        190,
        197,
    ]),
    45 : _tools.ROList([
        82,
    ]),
    6 : _tools.ROList([
        91,
        104,
        117,
    ]),
    10 : _tools.ROList([
        92,
        105,
        118,
        140,
        158,
    ]),
    35 : _tools.ROList([
        97,
        110,
        123,
        129,
        132,
        186,
    ]),
    40 : _tools.ROList([
        98,
        111,
        124,
        139,
        145,
        195,
    ]),
    48 : _tools.ROList([
        99,
        112,
        125,
        147,
    ]),
    26 : _tools.ROList([
        134,
        135,
        136,
        137,
        142,
    ]),
    44 : _tools.ROList([
        146,
    ]),
    60 : _tools.ROList([
        148,
        149,
        150,
        151,
    ]),
    50 : _tools.ROList([
        167,
    ]),
    23 : _tools.ROList([
        170,
        188,
    ]),
    32 : _tools.ROList([
        191,
    ]),
    34 : _tools.ROList([
        192,
    ]),
    36 : _tools.ROList([
        193,
    ]),
    38 : _tools.ROList([
        194,
    ]),
})
taskDic = _tools.RODict({
    86010002 : _tools.ROList([
        1,
        2,
        9,
        10,
        11,
        14,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        26,
        34,
        35,
        36,
        37,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        49,
        50,
        51,
        53,
        54,
        55,
        56,
        79,
        87,
        155,
        156,
        157,
        158,
        160,
        164,
        173,
        176,
        181,
        184,
        186,
        198,
        199,
    ]),
    86010006 : _tools.ROList([
        7,
        48,
    ]),
    86030033 : _tools.ROList([
        15,
        57,
    ]),
    86030027 : _tools.ROList([
        24,
    ]),
    86030030 : _tools.ROList([
        27,
    ]),
    86030011 : _tools.ROList([
        28,
        163,
        185,
    ]),
    86030009 : _tools.ROList([
        29,
        180,
    ]),
    86030038 : _tools.ROList([
        30,
        32,
        58,
        71,
        73,
        75,
        76,
        170,
        197,
    ]),
    86030028 : _tools.ROList([
        31,
    ]),
    86060137 : _tools.ROList([
        47,
        127,
        159,
        179,
    ]),
    86030032 : _tools.ROList([
        52,
    ]),
    86010064 : _tools.ROList([
        64,
    ]),
    86010005 : _tools.ROList([
        66,
    ]),
    86060003 : _tools.ROList([
        85,
    ]),
    86060055 : _tools.ROList([
        88,
        101,
        114,
    ]),
    86060061 : _tools.ROList([
        89,
        102,
        115,
    ]),
    86060070 : _tools.ROList([
        90,
        103,
        116,
    ]),
    86060098 : _tools.ROList([
        100,
        113,
        126,
    ]),
    86010087 : _tools.ROList([
        130,
        131,
    ]),
    86010027 : _tools.ROList([
        162,
    ]),
})
dayDic = _tools.RODict({
    1 : _tools.ROList([
        167,
        187,
        188,
        196,
    ]),
    3 : _tools.ROList([
        186,
        191,
    ]),
    2 : _tools.ROList([
        189,
        190,
    ]),
    4 : _tools.ROList([
        192,
    ]),
    5 : _tools.ROList([
        193,
    ]),
    6 : _tools.ROList([
        194,
    ]),
    7 : _tools.ROList([
        195,
    ]),
})
maxBit = 199

typeToMain = {'UI_camera': 'UI', 'UI_cards': 'UI', 'UI_hp': 'UI', 'UI_level': 'UI', 'UI_score': 'UI', 'welfare_tenSign': 'welfare', 'welfare_attention': 'welfare', 'welfare_phoneBind': 'welfare', 'welfare_levelReward': 'welfare', 'welfare_pcLogin': 'welfare', 'welfare_resourceRecovery': 'welfare', 'welfare_sevenSign': 'welfare', 'equip_make': 'equip', 'equip_unbundle': 'equip', 'equip_strengthen': 'equip', 'guild_union': 'guild', 'guild_unionCrossServer': 'guild', 'equip_class': 'equip', 'equip_spirit': 'equip', 'equip_weaponGlyph': 'equip', 'equip_bless': 'equip', 'settings_giftKey': 'settings', 'pay_hotGift': 'pay', 'pay_holidayGift': 'pay', 'pay_rmb': 'pay', 'settings_hotKey': 'settings', 'equip_soul': 'equip', 'welfare_refundRecharge': 'welfare', 'settings_operation': 'settings', 'welfare_powerpankpanel': 'welfare', 'settings_secondPwd': 'settings', 'welfare_returnReward': 'welfare', 'equip_soulWash': 'equip', 'welfare_affiliate': 'welfare', 'pay_materialSale': 'pay'}
