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
        "switch": 0
    }),
    "x": _tools.RODict({
        "function": "x",
        "type": "_",
        "level": 999,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIBagPanel": _tools.RODict({
        "function": "UIBagPanel",
        "type": "bag",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "ChangeTarget": _tools.RODict({
        "function": "ChangeTarget",
        "type": "changeTarget",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "UI_camera": _tools.RODict({
        "function": "UI_camera",
        "type": "UI_camera",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 2
    }),
    "UI_cards": _tools.RODict({
        "function": "UI_cards",
        "type": "UI_cards",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 2
    }),
    "UI_hp": _tools.RODict({
        "function": "UI_hp",
        "type": "UI_hp",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 2
    }),
    "UI_level": _tools.RODict({
        "function": "UI_level",
        "type": "UI_level",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 2
    }),
    "UI_score": _tools.RODict({
        "function": "UI_score",
        "type": "UI_score",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 2
    }),
    "QuickSettings": _tools.RODict({
        "function": "QuickSettings",
        "type": "quickSettings",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "queueServer": _tools.RODict({
        "function": "queueServer",
        "type": "queueServer",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "photograph": _tools.RODict({
        "function": "photograph",
        "type": "photograph",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "shareBtn": _tools.RODict({
        "function": "shareBtn",
        "type": "shareBtn",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "shareSystem": _tools.RODict({
        "function": "shareSystem",
        "type": "shareSystem",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "Enemy": _tools.RODict({
        "function": "Enemy",
        "type": "enemy",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "Duel": _tools.RODict({
        "function": "Duel",
        "type": "duel",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "TenSign": _tools.RODict({
        "function": "TenSign",
        "type": "welfare_tenSign",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "Meridian": _tools.RODict({
        "function": "Meridian",
        "type": "UIPracticePanel",
        "level": 0,
        "task": 86010005,
        "day": 0,
        "switch": 1
    }),
    "Attention": _tools.RODict({
        "function": "Attention",
        "type": "welfare_attention",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "phoneBind": _tools.RODict({
        "function": "phoneBind",
        "type": "welfare_phoneBind",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "LevelReward": _tools.RODict({
        "function": "LevelReward",
        "type": "welfare_levelReward",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "Questionnaire": _tools.RODict({
        "function": "Questionnaire",
        "type": "questionnaire",
        "level": 15,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "PcLoginReward": _tools.RODict({
        "function": "PcLoginReward",
        "type": "welfare_pcLogin",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "UIActivitiesPanel": _tools.RODict({
        "function": "UIActivitiesPanel",
        "type": "welfare",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "SevenSign": _tools.RODict({
        "function": "SevenSign",
        "type": "welfare_sevenSign",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "UISkillSystemPanel": _tools.RODict({
        "function": "UISkillSystemPanel",
        "type": "skillUpgrade",
        "level": 0,
        "task": 86010016,
        "day": 0,
        "switch": 1
    }),
    "UIRewardTaskPanel": _tools.RODict({
        "function": "UIRewardTaskPanel",
        "type": "rewardTask",
        "level": 0,
        "task": 86010018,
        "day": 0,
        "switch": 0
    }),
    "UIAppearancePanel": _tools.RODict({
        "function": "UIAppearancePanel",
        "type": "appearance",
        "level": 0,
        "task": 86010027,
        "day": 0,
        "switch": 1
    }),
    "UIDrawPetPanel": _tools.RODict({
        "function": "UIDrawPetPanel",
        "type": "drawPet",
        "level": 0,
        "task": 86010037,
        "day": 0,
        "switch": 0
    }),
    "UIPetPanel": _tools.RODict({
        "function": "UIPetPanel",
        "type": "pet",
        "level": 0,
        "task": 86010037,
        "day": 0,
        "switch": 1
    }),
    "UIEquipTrainingPanel": _tools.RODict({
        "function": "UIEquipTrainingPanel",
        "type": "equip",
        "level": 0,
        "task": 86050006,
        "day": 0,
        "switch": 0
    }),
    "UIEquipMakePanel": _tools.RODict({
        "function": "UIEquipMakePanel",
        "type": "equip_make",
        "level": 0,
        "task": 86050006,
        "day": 0,
        "switch": 0
    }),
    "UIEquipUnbundlePanel": _tools.RODict({
        "function": "UIEquipUnbundlePanel",
        "type": "equip_unbundle",
        "level": 0,
        "task": 86050006,
        "day": 0,
        "switch": 0
    }),
    "UITaskInfoPanel": _tools.RODict({
        "function": "UITaskInfoPanel",
        "type": "task",
        "level": 0,
        "task": 86060104,
        "day": 0,
        "switch": 2
    }),
    "Team": _tools.RODict({
        "function": "Team",
        "type": "team",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 2
    }),
    "UIWarehousePanel": _tools.RODict({
        "function": "UIWarehousePanel",
        "type": "warehouse",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "ExitDun": _tools.RODict({
        "function": "ExitDun",
        "type": "exitDun",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIAttributePanel": _tools.RODict({
        "function": "UIAttributePanel",
        "type": "myPage",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "UIFriendPanel": _tools.RODict({
        "function": "UIFriendPanel",
        "type": "friend",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 1
    }),
    "GrowthGuide": _tools.RODict({
        "function": "GrowthGuide",
        "type": "growth",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "Chat": _tools.RODict({
        "function": "Chat",
        "type": "chat",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 1
    }),
    "UIAchievementPanel": _tools.RODict({
        "function": "UIAchievementPanel",
        "type": "achievement",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "Line": _tools.RODict({
        "function": "Line",
        "type": "line",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIMailPanel": _tools.RODict({
        "function": "UIMailPanel",
        "type": "mail",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIMapPanel": _tools.RODict({
        "function": "UIMapPanel",
        "type": "map",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 1
    }),
    "UIPayStorePanel": _tools.RODict({
        "function": "UIPayStorePanel",
        "type": "pay",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIPKProtectPanel": _tools.RODict({
        "function": "UIPKProtectPanel",
        "type": "pkProtect",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIPortableSetPanel": _tools.RODict({
        "function": "UIPortableSetPanel",
        "type": "quickItem",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 1
    }),
    "Raid": _tools.RODict({
        "function": "Raid",
        "type": "raid",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 2
    }),
    "UIRankPanel": _tools.RODict({
        "function": "UIRankPanel",
        "type": "rank",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "DeathDrop": _tools.RODict({
        "function": "DeathDrop",
        "type": "deathDrop",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "AutoCombat": _tools.RODict({
        "function": "AutoCombat",
        "type": "autoCombat",
        "level": 4,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "AutoCollect": _tools.RODict({
        "function": "AutoCollect",
        "type": "autoCollect",
        "level": 4,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIRedPacketPanel": _tools.RODict({
        "function": "UIRedPacketPanel",
        "type": "redPacket",
        "level": 9,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "MonthCard": _tools.RODict({
        "function": "MonthCard",
        "type": "monthCard",
        "level": 9,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIPracticePanel": _tools.RODict({
        "function": "UIPracticePanel",
        "type": "UIPracticePanel",
        "level": 10,
        "task": 86010005,
        "day": 0,
        "switch": 1
    }),
    "UIEquipIntensifyPage": _tools.RODict({
        "function": "UIEquipIntensifyPage",
        "type": "equip_strengthen",
        "level": 15,
        "task": 86010078,
        "day": 0,
        "switch": 0
    }),
    "Guild": _tools.RODict({
        "function": "Guild",
        "type": "guild",
        "level": 16,
        "task": 86050035,
        "day": 0,
        "switch": 0
    }),
    "UIGuildPanel": _tools.RODict({
        "function": "UIGuildPanel",
        "type": "guild",
        "level": 16,
        "task": 86050035,
        "day": 0,
        "switch": 0
    }),
    "UIGuildLobbyPanel": _tools.RODict({
        "function": "UIGuildLobbyPanel",
        "type": "guild",
        "level": 16,
        "task": 86050035,
        "day": 0,
        "switch": 0
    }),
    "UITeamDunPanel": _tools.RODict({
        "function": "UITeamDunPanel",
        "type": "teamDungeon",
        "level": 17,
        "task": 86010068,
        "day": 0,
        "switch": 0
    }),
    "UISquarePanel": _tools.RODict({
        "function": "UISquarePanel",
        "type": "square",
        "level": 18,
        "task": 86010070,
        "day": 0,
        "switch": 0
    }),
    "UICollectionPanel": _tools.RODict({
        "function": "UICollectionPanel",
        "type": "collection",
        "level": 19,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UISynthesisSystemPanel": _tools.RODict({
        "function": "UISynthesisSystemPanel",
        "type": "synthesis",
        "level": 19,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIPropMakePanel": _tools.RODict({
        "function": "UIPropMakePanel",
        "type": "workshop",
        "level": 19,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "GuildBossChallenge": _tools.RODict({
        "function": "GuildBossChallenge",
        "type": "guildBossChallenge",
        "level": 19,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIBusinessPanel": _tools.RODict({
        "function": "UIBusinessPanel",
        "type": "business",
        "level": 19,
        "task": 86010069,
        "day": 0,
        "switch": 0
    }),
    "UIEquipClassPage": _tools.RODict({
        "function": "UIEquipClassPage",
        "type": "equip_class",
        "level": 20,
        "task": 86010046,
        "day": 0,
        "switch": 0
    }),
    "UIWonderLandPanel": _tools.RODict({
        "function": "UIWonderLandPanel",
        "type": "wonderLand",
        "level": 24,
        "task": 86010081,
        "day": 0,
        "switch": 0
    }),
    "UIEquipEnchantingPage": _tools.RODict({
        "function": "UIEquipEnchantingPage",
        "type": "equip_spirit",
        "level": 25,
        "task": 86010079,
        "day": 0,
        "switch": 0
    }),
    "UICrusadeSystemPanel": _tools.RODict({
        "function": "UICrusadeSystemPanel",
        "type": "raidDungeon",
        "level": 26,
        "task": 86010077,
        "day": 0,
        "switch": 0
    }),
    "UIEquipRunePage": _tools.RODict({
        "function": "UIEquipRunePage",
        "type": "equip_weaponGlyph",
        "level": 27,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIEquipBlessPage": _tools.RODict({
        "function": "UIEquipBlessPage",
        "type": "equip_bless",
        "level": 29,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "MineBattle": _tools.RODict({
        "function": "MineBattle",
        "type": "mineBattle",
        "level": 30,
        "task": 86010083,
        "day": 0,
        "switch": 0
    }),
    "UIMineBattleManagePanel": _tools.RODict({
        "function": "UIMineBattleManagePanel",
        "type": "mineBattle",
        "level": 30,
        "task": 86010083,
        "day": 0,
        "switch": 0
    }),
    "UIRoleAuthorizationPanel": _tools.RODict({
        "function": "UIRoleAuthorizationPanel",
        "type": "roleAuthorization",
        "level": 999,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "CityBattle": _tools.RODict({
        "function": "CityBattle",
        "type": "cityBattle",
        "level": 999,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "UICityBattlePanel": _tools.RODict({
        "function": "UICityBattlePanel",
        "type": "cityBattle",
        "level": 999,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "GeneralAttack": _tools.RODict({
        "function": "GeneralAttack",
        "type": "skill",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "Dodge": _tools.RODict({
        "function": "Dodge",
        "type": "skill",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "Sprint": _tools.RODict({
        "function": "Sprint",
        "type": "skill",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "Jump": _tools.RODict({
        "function": "Jump",
        "type": "skill",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "Fly": _tools.RODict({
        "function": "Fly",
        "type": "skill",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 1
    }),
    "MageSkill01": _tools.RODict({
        "function": "MageSkill01",
        "type": "skillMage",
        "level": 0,
        "task": 86060055,
        "day": 0,
        "switch": 1
    }),
    "MageSkill02": _tools.RODict({
        "function": "MageSkill02",
        "type": "skillMage",
        "level": 0,
        "task": 86060061,
        "day": 0,
        "switch": 1
    }),
    "MageSkill03": _tools.RODict({
        "function": "MageSkill03",
        "type": "skillMage",
        "level": 0,
        "task": 86060089,
        "day": 0,
        "switch": 1
    }),
    "MageSkill04": _tools.RODict({
        "function": "MageSkill04",
        "type": "skillMage",
        "level": 6,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill05": _tools.RODict({
        "function": "MageSkill05",
        "type": "skillMage",
        "level": 9,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill06": _tools.RODict({
        "function": "MageSkill06",
        "type": "skillMage",
        "level": 12,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill07": _tools.RODict({
        "function": "MageSkill07",
        "type": "skillMage",
        "level": 15,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill08": _tools.RODict({
        "function": "MageSkill08",
        "type": "skillMage",
        "level": 20,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill09": _tools.RODict({
        "function": "MageSkill09",
        "type": "skillMage",
        "level": 26,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill10": _tools.RODict({
        "function": "MageSkill10",
        "type": "skillMage",
        "level": 32,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill11": _tools.RODict({
        "function": "MageSkill11",
        "type": "skillMage",
        "level": 40,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill12": _tools.RODict({
        "function": "MageSkill12",
        "type": "skillMage",
        "level": 48,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkillUlt": _tools.RODict({
        "function": "MageSkillUlt",
        "type": "skillMage",
        "level": 0,
        "task": 86060090,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill01": _tools.RODict({
        "function": "TaoistSkill01",
        "type": "skillTaoist",
        "level": 0,
        "task": 86060055,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill02": _tools.RODict({
        "function": "TaoistSkill02",
        "type": "skillTaoist",
        "level": 0,
        "task": 86060061,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill03": _tools.RODict({
        "function": "TaoistSkill03",
        "type": "skillTaoist",
        "level": 0,
        "task": 86060089,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill04": _tools.RODict({
        "function": "TaoistSkill04",
        "type": "skillTaoist",
        "level": 6,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill05": _tools.RODict({
        "function": "TaoistSkill05",
        "type": "skillTaoist",
        "level": 9,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill06": _tools.RODict({
        "function": "TaoistSkill06",
        "type": "skillTaoist",
        "level": 12,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill07": _tools.RODict({
        "function": "TaoistSkill07",
        "type": "skillTaoist",
        "level": 15,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill08": _tools.RODict({
        "function": "TaoistSkill08",
        "type": "skillTaoist",
        "level": 20,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill09": _tools.RODict({
        "function": "TaoistSkill09",
        "type": "skillTaoist",
        "level": 26,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill10": _tools.RODict({
        "function": "TaoistSkill10",
        "type": "skillTaoist",
        "level": 32,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill11": _tools.RODict({
        "function": "TaoistSkill11",
        "type": "skillTaoist",
        "level": 40,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill12": _tools.RODict({
        "function": "TaoistSkill12",
        "type": "skillTaoist",
        "level": 48,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkillUlt": _tools.RODict({
        "function": "TaoistSkillUlt",
        "type": "skillTaoist",
        "level": 0,
        "task": 86060090,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill01": _tools.RODict({
        "function": "WarriorSkill01",
        "type": "skillWarrior",
        "level": 0,
        "task": 86060055,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill02": _tools.RODict({
        "function": "WarriorSkill02",
        "type": "skillWarrior",
        "level": 0,
        "task": 86060061,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill03": _tools.RODict({
        "function": "WarriorSkill03",
        "type": "skillWarrior",
        "level": 0,
        "task": 86060089,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill04": _tools.RODict({
        "function": "WarriorSkill04",
        "type": "skillWarrior",
        "level": 6,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill05": _tools.RODict({
        "function": "WarriorSkill05",
        "type": "skillWarrior",
        "level": 9,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill06": _tools.RODict({
        "function": "WarriorSkill06",
        "type": "skillWarrior",
        "level": 12,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill07": _tools.RODict({
        "function": "WarriorSkill07",
        "type": "skillWarrior",
        "level": 15,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill08": _tools.RODict({
        "function": "WarriorSkill08",
        "type": "skillWarrior",
        "level": 20,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill09": _tools.RODict({
        "function": "WarriorSkill09",
        "type": "skillWarrior",
        "level": 26,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill10": _tools.RODict({
        "function": "WarriorSkill10",
        "type": "skillWarrior",
        "level": 32,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill11": _tools.RODict({
        "function": "WarriorSkill11",
        "type": "skillWarrior",
        "level": 40,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill12": _tools.RODict({
        "function": "WarriorSkill12",
        "type": "skillWarrior",
        "level": 48,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkillUlt": _tools.RODict({
        "function": "WarriorSkillUlt",
        "type": "skillWarrior",
        "level": 0,
        "task": 86060090,
        "day": 0,
        "switch": 1
    }),
    "xinyuanchengopentask": _tools.RODict({
        "function": "xinyuanchengopentask",
        "type": "mapTask",
        "level": 0,
        "task": 86010024,
        "day": 0,
        "switch": 0
    }),
    "tongxingguopentask": _tools.RODict({
        "function": "tongxingguopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "feishayaosaiopentask": _tools.RODict({
        "function": "feishayaosaiopentask",
        "type": "mapTask",
        "level": 35,
        "task": 86010058,
        "day": 0,
        "switch": 0
    }),
    "jinglingcunopentask": _tools.RODict({
        "function": "jinglingcunopentask",
        "type": "mapTask",
        "level": 0,
        "task": 86010020,
        "day": 0,
        "switch": 0
    }),
    "jinglingbaodianopentask": _tools.RODict({
        "function": "jinglingbaodianopentask",
        "type": "mapTask",
        "level": 0,
        "task": 86010020,
        "day": 0,
        "switch": 0
    }),
    "shikuzoulangopentask": _tools.RODict({
        "function": "shikuzoulangopentask",
        "type": "mapTask",
        "level": 40,
        "task": 86010057,
        "day": 0,
        "switch": 0
    }),
    "xinyuanchenjiaoopentask": _tools.RODict({
        "function": "xinyuanchenjiaoopentask",
        "type": "mapTask",
        "level": 23,
        "task": 86010076,
        "day": 0,
        "switch": 0
    }),
    "zuke1Fopentask": _tools.RODict({
        "function": "zuke1Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 86010084,
        "day": 0,
        "switch": 0
    }),
    "zuke2Fopentask": _tools.RODict({
        "function": "zuke2Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 86010084,
        "day": 0,
        "switch": 0
    }),
    "zuke3Fopentask": _tools.RODict({
        "function": "zuke3Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 86010084,
        "day": 0,
        "switch": 0
    }),
    "zuke4Fopentask": _tools.RODict({
        "function": "zuke4Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 86010084,
        "day": 0,
        "switch": 0
    }),
    "zuke5Fopentask": _tools.RODict({
        "function": "zuke5Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 86010084,
        "day": 0,
        "switch": 0
    }),
    "zuke6Fopentask": _tools.RODict({
        "function": "zuke6Fopentask",
        "type": "mapTask",
        "level": 50,
        "task": 86010057,
        "day": 0,
        "switch": 0
    }),
    "yueguang1Fopentask": _tools.RODict({
        "function": "yueguang1Fopentask",
        "type": "mapTask",
        "level": 10,
        "task": 86010029,
        "day": 0,
        "switch": 0
    }),
    "yueguang2Fopentask": _tools.RODict({
        "function": "yueguang2Fopentask",
        "type": "mapTask",
        "level": 16,
        "task": 86010029,
        "day": 0,
        "switch": 0
    }),
    "yueguang3Fopentask": _tools.RODict({
        "function": "yueguang3Fopentask",
        "type": "mapTask",
        "level": 22,
        "task": 86010029,
        "day": 0,
        "switch": 0
    }),
    "yueguang4Fopentask": _tools.RODict({
        "function": "yueguang4Fopentask",
        "type": "mapTask",
        "level": 28,
        "task": 86010029,
        "day": 0,
        "switch": 0
    }),
    "yueguang5Fopentask": _tools.RODict({
        "function": "yueguang5Fopentask",
        "type": "mapTask",
        "level": 34,
        "task": 86010029,
        "day": 0,
        "switch": 0
    }),
    "wudu1Fopentask": _tools.RODict({
        "function": "wudu1Fopentask",
        "type": "mapTask",
        "level": 50,
        "task": 86010057,
        "day": 0,
        "switch": 0
    }),
    "wudu2Fopentask": _tools.RODict({
        "function": "wudu2Fopentask",
        "type": "mapTask",
        "level": 52,
        "task": 86010057,
        "day": 0,
        "switch": 0
    }),
    "wudu4Fopentask": _tools.RODict({
        "function": "wudu4Fopentask",
        "type": "mapTask",
        "level": 56,
        "task": 86010057,
        "day": 0,
        "switch": 0
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
UIActivitiesPanel = 21
SevenSign = 22
UISkillSystemPanel = 23
UIRewardTaskPanel = 24
UIAppearancePanel = 25
UIDrawPetPanel = 26
UIPetPanel = 27
UIEquipTrainingPanel = 28
UIEquipMakePanel = 29
UIEquipUnbundlePanel = 30
UITaskInfoPanel = 31
Team = 32
UIWarehousePanel = 33
ExitDun = 34
UIAttributePanel = 35
UIFriendPanel = 36
GrowthGuide = 37
Chat = 38
UIAchievementPanel = 39
Line = 40
UIMailPanel = 41
UIMapPanel = 42
UIPayStorePanel = 43
UIPKProtectPanel = 44
UIPortableSetPanel = 45
Raid = 46
UIRankPanel = 47
DeathDrop = 48
AutoCombat = 49
AutoCollect = 50
UIRedPacketPanel = 51
MonthCard = 52
UIPracticePanel = 53
UIEquipIntensifyPage = 54
Guild = 55
UIGuildPanel = 56
UIGuildLobbyPanel = 57
UITeamDunPanel = 58
UISquarePanel = 59
UICollectionPanel = 60
UISynthesisSystemPanel = 61
UIPropMakePanel = 62
GuildBossChallenge = 63
UIBusinessPanel = 64
UIEquipClassPage = 65
UIWonderLandPanel = 66
UIEquipEnchantingPage = 67
UICrusadeSystemPanel = 68
UIEquipRunePage = 69
UIEquipBlessPage = 70
MineBattle = 71
UIMineBattleManagePanel = 72
UIRoleAuthorizationPanel = 73
CityBattle = 74
UICityBattlePanel = 75
GeneralAttack = 76
Dodge = 77
Sprint = 78
Jump = 79
Fly = 80
MageSkill01 = 81
MageSkill02 = 82
MageSkill03 = 83
MageSkill04 = 84
MageSkill05 = 85
MageSkill06 = 86
MageSkill07 = 87
MageSkill08 = 88
MageSkill09 = 89
MageSkill10 = 90
MageSkill11 = 91
MageSkill12 = 92
MageSkillUlt = 93
TaoistSkill01 = 94
TaoistSkill02 = 95
TaoistSkill03 = 96
TaoistSkill04 = 97
TaoistSkill05 = 98
TaoistSkill06 = 99
TaoistSkill07 = 100
TaoistSkill08 = 101
TaoistSkill09 = 102
TaoistSkill10 = 103
TaoistSkill11 = 104
TaoistSkill12 = 105
TaoistSkillUlt = 106
WarriorSkill01 = 107
WarriorSkill02 = 108
WarriorSkill03 = 109
WarriorSkill04 = 110
WarriorSkill05 = 111
WarriorSkill06 = 112
WarriorSkill07 = 113
WarriorSkill08 = 114
WarriorSkill09 = 115
WarriorSkill10 = 116
WarriorSkill11 = 117
WarriorSkill12 = 118
WarriorSkillUlt = 119
xinyuanchengopentask = 120
tongxingguopentask = 121
feishayaosaiopentask = 122
jinglingcunopentask = 123
jinglingbaodianopentask = 124
shikuzoulangopentask = 125
xinyuanchenjiaoopentask = 126
zuke1Fopentask = 127
zuke2Fopentask = 128
zuke3Fopentask = 129
zuke4Fopentask = 130
zuke5Fopentask = 131
zuke6Fopentask = 132
yueguang1Fopentask = 133
yueguang2Fopentask = 134
yueguang3Fopentask = 135
yueguang4Fopentask = 136
yueguang5Fopentask = 137
wudu1Fopentask = 138
wudu2Fopentask = 139
wudu4Fopentask = 140



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
    "UIActivitiesPanel" : 21,
    "SevenSign" : 22,
    "UISkillSystemPanel" : 23,
    "UIRewardTaskPanel" : 24,
    "UIAppearancePanel" : 25,
    "UIDrawPetPanel" : 26,
    "UIPetPanel" : 27,
    "UIEquipTrainingPanel" : 28,
    "UIEquipMakePanel" : 29,
    "UIEquipUnbundlePanel" : 30,
    "UITaskInfoPanel" : 31,
    "Team" : 32,
    "UIWarehousePanel" : 33,
    "ExitDun" : 34,
    "UIAttributePanel" : 35,
    "UIFriendPanel" : 36,
    "GrowthGuide" : 37,
    "Chat" : 38,
    "UIAchievementPanel" : 39,
    "Line" : 40,
    "UIMailPanel" : 41,
    "UIMapPanel" : 42,
    "UIPayStorePanel" : 43,
    "UIPKProtectPanel" : 44,
    "UIPortableSetPanel" : 45,
    "Raid" : 46,
    "UIRankPanel" : 47,
    "DeathDrop" : 48,
    "AutoCombat" : 49,
    "AutoCollect" : 50,
    "UIRedPacketPanel" : 51,
    "MonthCard" : 52,
    "UIPracticePanel" : 53,
    "UIEquipIntensifyPage" : 54,
    "Guild" : 55,
    "UIGuildPanel" : 56,
    "UIGuildLobbyPanel" : 57,
    "UITeamDunPanel" : 58,
    "UISquarePanel" : 59,
    "UICollectionPanel" : 60,
    "UISynthesisSystemPanel" : 61,
    "UIPropMakePanel" : 62,
    "GuildBossChallenge" : 63,
    "UIBusinessPanel" : 64,
    "UIEquipClassPage" : 65,
    "UIWonderLandPanel" : 66,
    "UIEquipEnchantingPage" : 67,
    "UICrusadeSystemPanel" : 68,
    "UIEquipRunePage" : 69,
    "UIEquipBlessPage" : 70,
    "MineBattle" : 71,
    "UIMineBattleManagePanel" : 72,
    "UIRoleAuthorizationPanel" : 73,
    "CityBattle" : 74,
    "UICityBattlePanel" : 75,
    "GeneralAttack" : 76,
    "Dodge" : 77,
    "Sprint" : 78,
    "Jump" : 79,
    "Fly" : 80,
    "MageSkill01" : 81,
    "MageSkill02" : 82,
    "MageSkill03" : 83,
    "MageSkill04" : 84,
    "MageSkill05" : 85,
    "MageSkill06" : 86,
    "MageSkill07" : 87,
    "MageSkill08" : 88,
    "MageSkill09" : 89,
    "MageSkill10" : 90,
    "MageSkill11" : 91,
    "MageSkill12" : 92,
    "MageSkillUlt" : 93,
    "TaoistSkill01" : 94,
    "TaoistSkill02" : 95,
    "TaoistSkill03" : 96,
    "TaoistSkill04" : 97,
    "TaoistSkill05" : 98,
    "TaoistSkill06" : 99,
    "TaoistSkill07" : 100,
    "TaoistSkill08" : 101,
    "TaoistSkill09" : 102,
    "TaoistSkill10" : 103,
    "TaoistSkill11" : 104,
    "TaoistSkill12" : 105,
    "TaoistSkillUlt" : 106,
    "WarriorSkill01" : 107,
    "WarriorSkill02" : 108,
    "WarriorSkill03" : 109,
    "WarriorSkill04" : 110,
    "WarriorSkill05" : 111,
    "WarriorSkill06" : 112,
    "WarriorSkill07" : 113,
    "WarriorSkill08" : 114,
    "WarriorSkill09" : 115,
    "WarriorSkill10" : 116,
    "WarriorSkill11" : 117,
    "WarriorSkill12" : 118,
    "WarriorSkillUlt" : 119,
    "xinyuanchengopentask" : 120,
    "tongxingguopentask" : 121,
    "feishayaosaiopentask" : 122,
    "jinglingcunopentask" : 123,
    "jinglingbaodianopentask" : 124,
    "shikuzoulangopentask" : 125,
    "xinyuanchenjiaoopentask" : 126,
    "zuke1Fopentask" : 127,
    "zuke2Fopentask" : 128,
    "zuke3Fopentask" : 129,
    "zuke4Fopentask" : 130,
    "zuke5Fopentask" : 131,
    "zuke6Fopentask" : 132,
    "yueguang1Fopentask" : 133,
    "yueguang2Fopentask" : 134,
    "yueguang3Fopentask" : 135,
    "yueguang4Fopentask" : 136,
    "yueguang5Fopentask" : 137,
    "wudu1Fopentask" : 138,
    "wudu2Fopentask" : 139,
    "wudu4Fopentask" : 140,
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
    21 : "UIActivitiesPanel",
    22 : "SevenSign",
    23 : "UISkillSystemPanel",
    24 : "UIRewardTaskPanel",
    25 : "UIAppearancePanel",
    26 : "UIDrawPetPanel",
    27 : "UIPetPanel",
    28 : "UIEquipTrainingPanel",
    29 : "UIEquipMakePanel",
    30 : "UIEquipUnbundlePanel",
    31 : "UITaskInfoPanel",
    32 : "Team",
    33 : "UIWarehousePanel",
    34 : "ExitDun",
    35 : "UIAttributePanel",
    36 : "UIFriendPanel",
    37 : "GrowthGuide",
    38 : "Chat",
    39 : "UIAchievementPanel",
    40 : "Line",
    41 : "UIMailPanel",
    42 : "UIMapPanel",
    43 : "UIPayStorePanel",
    44 : "UIPKProtectPanel",
    45 : "UIPortableSetPanel",
    46 : "Raid",
    47 : "UIRankPanel",
    48 : "DeathDrop",
    49 : "AutoCombat",
    50 : "AutoCollect",
    51 : "UIRedPacketPanel",
    52 : "MonthCard",
    53 : "UIPracticePanel",
    54 : "UIEquipIntensifyPage",
    55 : "Guild",
    56 : "UIGuildPanel",
    57 : "UIGuildLobbyPanel",
    58 : "UITeamDunPanel",
    59 : "UISquarePanel",
    60 : "UICollectionPanel",
    61 : "UISynthesisSystemPanel",
    62 : "UIPropMakePanel",
    63 : "GuildBossChallenge",
    64 : "UIBusinessPanel",
    65 : "UIEquipClassPage",
    66 : "UIWonderLandPanel",
    67 : "UIEquipEnchantingPage",
    68 : "UICrusadeSystemPanel",
    69 : "UIEquipRunePage",
    70 : "UIEquipBlessPage",
    71 : "MineBattle",
    72 : "UIMineBattleManagePanel",
    73 : "UIRoleAuthorizationPanel",
    74 : "CityBattle",
    75 : "UICityBattlePanel",
    76 : "GeneralAttack",
    77 : "Dodge",
    78 : "Sprint",
    79 : "Jump",
    80 : "Fly",
    81 : "MageSkill01",
    82 : "MageSkill02",
    83 : "MageSkill03",
    84 : "MageSkill04",
    85 : "MageSkill05",
    86 : "MageSkill06",
    87 : "MageSkill07",
    88 : "MageSkill08",
    89 : "MageSkill09",
    90 : "MageSkill10",
    91 : "MageSkill11",
    92 : "MageSkill12",
    93 : "MageSkillUlt",
    94 : "TaoistSkill01",
    95 : "TaoistSkill02",
    96 : "TaoistSkill03",
    97 : "TaoistSkill04",
    98 : "TaoistSkill05",
    99 : "TaoistSkill06",
    100 : "TaoistSkill07",
    101 : "TaoistSkill08",
    102 : "TaoistSkill09",
    103 : "TaoistSkill10",
    104 : "TaoistSkill11",
    105 : "TaoistSkill12",
    106 : "TaoistSkillUlt",
    107 : "WarriorSkill01",
    108 : "WarriorSkill02",
    109 : "WarriorSkill03",
    110 : "WarriorSkill04",
    111 : "WarriorSkill05",
    112 : "WarriorSkill06",
    113 : "WarriorSkill07",
    114 : "WarriorSkill08",
    115 : "WarriorSkill09",
    116 : "WarriorSkill10",
    117 : "WarriorSkill11",
    118 : "WarriorSkill12",
    119 : "WarriorSkillUlt",
    120 : "xinyuanchengopentask",
    121 : "tongxingguopentask",
    122 : "feishayaosaiopentask",
    123 : "jinglingcunopentask",
    124 : "jinglingbaodianopentask",
    125 : "shikuzoulangopentask",
    126 : "xinyuanchenjiaoopentask",
    127 : "zuke1Fopentask",
    128 : "zuke2Fopentask",
    129 : "zuke3Fopentask",
    130 : "zuke4Fopentask",
    131 : "zuke5Fopentask",
    132 : "zuke6Fopentask",
    133 : "yueguang1Fopentask",
    134 : "yueguang2Fopentask",
    135 : "yueguang3Fopentask",
    136 : "yueguang4Fopentask",
    137 : "yueguang5Fopentask",
    138 : "wudu1Fopentask",
    139 : "wudu2Fopentask",
    140 : "wudu4Fopentask",
})
levelDic = _tools.RODict({
    15 : _tools.ROList([
        19,
        54,
        87,
        100,
        113,
    ]),
    4 : _tools.ROList([
        49,
        50,
    ]),
    9 : _tools.ROList([
        51,
        52,
        85,
        98,
        111,
    ]),
    10 : _tools.ROList([
        53,
        133,
    ]),
    16 : _tools.ROList([
        55,
        56,
        57,
        134,
    ]),
    17 : _tools.ROList([
        58,
    ]),
    18 : _tools.ROList([
        59,
    ]),
    19 : _tools.ROList([
        60,
        61,
        62,
        63,
        64,
    ]),
    20 : _tools.ROList([
        65,
        88,
        101,
        114,
    ]),
    24 : _tools.ROList([
        66,
    ]),
    25 : _tools.ROList([
        67,
    ]),
    26 : _tools.ROList([
        68,
        89,
        102,
        115,
    ]),
    27 : _tools.ROList([
        69,
    ]),
    29 : _tools.ROList([
        70,
    ]),
    30 : _tools.ROList([
        71,
        72,
        127,
        128,
        129,
        130,
        131,
    ]),
    999 : _tools.ROList([
        73,
        74,
        75,
    ]),
    6 : _tools.ROList([
        84,
        97,
        110,
    ]),
    12 : _tools.ROList([
        86,
        99,
        112,
    ]),
    32 : _tools.ROList([
        90,
        103,
        116,
    ]),
    40 : _tools.ROList([
        91,
        104,
        117,
        125,
    ]),
    48 : _tools.ROList([
        92,
        105,
        118,
    ]),
    35 : _tools.ROList([
        122,
    ]),
    23 : _tools.ROList([
        126,
    ]),
    50 : _tools.ROList([
        132,
        138,
    ]),
    22 : _tools.ROList([
        135,
    ]),
    28 : _tools.ROList([
        136,
    ]),
    34 : _tools.ROList([
        137,
    ]),
    52 : _tools.ROList([
        139,
    ]),
    56 : _tools.ROList([
        140,
    ]),
})
taskDic = _tools.RODict({
    86010003 : _tools.ROList([
        14,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
    ]),
    86010005 : _tools.ROList([
        15,
        53,
    ]),
    86010016 : _tools.ROList([
        23,
    ]),
    86010018 : _tools.ROList([
        24,
    ]),
    86010027 : _tools.ROList([
        25,
    ]),
    86010037 : _tools.ROList([
        26,
        27,
    ]),
    86050006 : _tools.ROList([
        28,
        29,
        30,
    ]),
    86060104 : _tools.ROList([
        31,
    ]),
    86060115 : _tools.ROList([
        32,
        33,
        34,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        50,
        51,
        52,
        73,
        80,
    ]),
    86010078 : _tools.ROList([
        54,
    ]),
    86050035 : _tools.ROList([
        55,
        56,
        57,
    ]),
    86010068 : _tools.ROList([
        58,
    ]),
    86010070 : _tools.ROList([
        59,
    ]),
    86010069 : _tools.ROList([
        64,
    ]),
    86010046 : _tools.ROList([
        65,
    ]),
    86010081 : _tools.ROList([
        66,
    ]),
    86010079 : _tools.ROList([
        67,
    ]),
    86010077 : _tools.ROList([
        68,
    ]),
    86010083 : _tools.ROList([
        71,
        72,
    ]),
    86060055 : _tools.ROList([
        81,
        94,
        107,
    ]),
    86060061 : _tools.ROList([
        82,
        95,
        108,
    ]),
    86060089 : _tools.ROList([
        83,
        96,
        109,
    ]),
    86060090 : _tools.ROList([
        93,
        106,
        119,
    ]),
    86010024 : _tools.ROList([
        120,
    ]),
    86010058 : _tools.ROList([
        122,
    ]),
    86010020 : _tools.ROList([
        123,
        124,
    ]),
    86010057 : _tools.ROList([
        125,
        132,
        138,
        139,
        140,
    ]),
    86010076 : _tools.ROList([
        126,
    ]),
    86010084 : _tools.ROList([
        127,
        128,
        129,
        130,
        131,
    ]),
    86010029 : _tools.ROList([
        133,
        134,
        135,
        136,
        137,
    ]),
})
dayDic = _tools.RODict({
})
maxBit = 140

typeToMain = {'UI_camera': 'UI', 'UI_cards': 'UI', 'UI_hp': 'UI', 'UI_level': 'UI', 'UI_score': 'UI', 'welfare_tenSign': 'welfare', 'welfare_attention': 'welfare', 'welfare_phoneBind': 'welfare', 'welfare_levelReward': 'welfare', 'welfare_pcLogin': 'welfare', 'welfare_sevenSign': 'welfare', 'equip_make': 'equip', 'equip_unbundle': 'equip', 'equip_strengthen': 'equip', 'equip_class': 'equip', 'equip_spirit': 'equip', 'equip_weaponGlyph': 'equip', 'equip_bless': 'equip'}
