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
    "UIAchievementPanel": _tools.RODict({
        "function": "UIAchievementPanel",
        "type": "achievement",
        "level": 0,
        "task": 86060115,
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
    "AutoCollect": _tools.RODict({
        "function": "AutoCollect",
        "type": "autoCollect",
        "level": 4,
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
    "UIBagPanel": _tools.RODict({
        "function": "UIBagPanel",
        "type": "bag",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "UIBusinessPanel": _tools.RODict({
        "function": "UIBusinessPanel",
        "type": "business",
        "level": 21,
        "task": 86010069,
        "day": 0,
        "switch": 0
    }),
    "ChangeTarget": _tools.RODict({
        "function": "ChangeTarget",
        "type": "changeTarget",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "Chat": _tools.RODict({
        "function": "Chat",
        "type": "chat",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 1
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
    "UICollectionPanel": _tools.RODict({
        "function": "UICollectionPanel",
        "type": "collection",
        "level": 19,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UICrusadeSystemPanel": _tools.RODict({
        "function": "UICrusadeSystemPanel",
        "type": "raidDungeon",
        "level": 27,
        "task": 86010077,
        "day": 0,
        "switch": 0
    }),
    "UIDrawPetPanel": _tools.RODict({
        "function": "UIDrawPetPanel",
        "type": "drawPet",
        "level": 0,
        "task": 86010037,
        "day": 0,
        "switch": 0
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
    "UIEquipIntensifyPanel": _tools.RODict({
        "function": "UIEquipIntensifyPanel",
        "type": "equip_strengthen",
        "level": 15,
        "task": 86010078,
        "day": 0,
        "switch": 0
    }),
    "UIEquipClassPanel": _tools.RODict({
        "function": "UIEquipClassPanel",
        "type": "equip_class",
        "level": 20,
        "task": 86010046,
        "day": 0,
        "switch": 0
    }),
    "UIEquipEnchantingPanel": _tools.RODict({
        "function": "UIEquipEnchantingPanel",
        "type": "equip_FuLing",
        "level": 25,
        "task": 86010079,
        "day": 0,
        "switch": 0
    }),
    "UIEquipRnuePanel": _tools.RODict({
        "function": "UIEquipRnuePanel",
        "type": "equip_weaponGlyph",
        "level": 28,
        "task": 86010080,
        "day": 0,
        "switch": 0
    }),
    "UIEquipBlessPanel": _tools.RODict({
        "function": "UIEquipBlessPanel",
        "type": "equip_Bless",
        "level": 31,
        "task": 86010082,
        "day": 0,
        "switch": 0
    }),
    "UIEquipUnbundlePanel": _tools.RODict({
        "function": "UIEquipUnbundlePanel",
        "type": "equip_Unbundle",
        "level": 0,
        "task": 86050006,
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
    "Guild": _tools.RODict({
        "function": "Guild",
        "type": "guild",
        "level": 18,
        "task": 86050036,
        "day": 0,
        "switch": 0
    }),
    "UIGuildPanel": _tools.RODict({
        "function": "UIGuildPanel",
        "type": "guild",
        "level": 18,
        "task": 86050036,
        "day": 0,
        "switch": 0
    }),
    "UIGuildLobbyPanel": _tools.RODict({
        "function": "UIGuildLobbyPanel",
        "type": "guild",
        "level": 18,
        "task": 86050036,
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
    "UIPetPanel": _tools.RODict({
        "function": "UIPetPanel",
        "type": "pet",
        "level": 0,
        "task": 86010037,
        "day": 0,
        "switch": 1
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
    "UIRedPacketPanel": _tools.RODict({
        "function": "UIRedPacketPanel",
        "type": "redPacket",
        "level": 9,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIRewardTaskPanel": _tools.RODict({
        "function": "UIRewardTaskPanel",
        "type": "rewardTask",
        "level": 0,
        "task": 86010018,
        "day": 0,
        "switch": 0
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
    "UISkillSystemPanel": _tools.RODict({
        "function": "UISkillSystemPanel",
        "type": "skillUpgrade",
        "level": 0,
        "task": 86010016,
        "day": 0,
        "switch": 1
    }),
    "UISquarePanel": _tools.RODict({
        "function": "UISquarePanel",
        "type": "square",
        "level": 0,
        "task": 86010070,
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
    "UITeamDunPanel": _tools.RODict({
        "function": "UITeamDunPanel",
        "type": "teamDungeon",
        "level": 16,
        "task": 86010068,
        "day": 0,
        "switch": 0
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
    "UIWarehousePanel": _tools.RODict({
        "function": "UIWarehousePanel",
        "type": "warehouse",
        "level": 0,
        "task": 86060115,
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
        "type": "welfare",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "UIWonderLandPanel": _tools.RODict({
        "function": "UIWonderLandPanel",
        "type": "wonderLand",
        "level": 26,
        "task": 86010081,
        "day": 0,
        "switch": 0
    }),
    "UIRoleAuthorizationPanel": _tools.RODict({
        "function": "UIRoleAuthorizationPanel",
        "type": "roleAuthorization",
        "level": 90,
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
    "DeathDrop": _tools.RODict({
        "function": "DeathDrop",
        "type": "deathDrop",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "QuickSettings": _tools.RODict({
        "function": "QuickSettings",
        "type": "quickSettings",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "TenSign": _tools.RODict({
        "function": "TenSign",
        "type": "welfare",
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
        "type": "welfare",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "phoneBind": _tools.RODict({
        "function": "phoneBind",
        "type": "welfare",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "LevelReward": _tools.RODict({
        "function": "LevelReward",
        "type": "welfare",
        "level": 0,
        "task": 86010003,
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
    "Questionnaire": _tools.RODict({
        "function": "Questionnaire",
        "type": "questionnaire",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "PcLoginReward": _tools.RODict({
        "function": "PcLoginReward",
        "type": "welfare",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "xinyuanchengopentask": _tools.RODict({
        "function": "xinyuanchengopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
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
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "jinglingcunopentask": _tools.RODict({
        "function": "jinglingcunopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "jinglingbaodianopentask": _tools.RODict({
        "function": "jinglingbaodianopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "shikuzoulangopentask": _tools.RODict({
        "function": "shikuzoulangopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "xinyuanchenjiaoopentask": _tools.RODict({
        "function": "xinyuanchenjiaoopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "zuke1Fopentask": _tools.RODict({
        "function": "zuke1Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "zuke2Fopentask": _tools.RODict({
        "function": "zuke2Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "zuke3Fopentask": _tools.RODict({
        "function": "zuke3Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "zuke4Fopentask": _tools.RODict({
        "function": "zuke4Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "zuke5Fopentask": _tools.RODict({
        "function": "zuke5Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "zuke6Fopentask": _tools.RODict({
        "function": "zuke6Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "yueguang1Fopentask": _tools.RODict({
        "function": "yueguang1Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "yueguang2Fopentask": _tools.RODict({
        "function": "yueguang2Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "yueguang3Fopentask": _tools.RODict({
        "function": "yueguang3Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "yueguang4Fopentask": _tools.RODict({
        "function": "yueguang4Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "yueguang5Fopentask": _tools.RODict({
        "function": "yueguang5Fopentask",
        "type": "mapTask",
        "level": 0,
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
    "queueServer": _tools.RODict({
        "function": "queueServer",
        "type": "queueServer",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    })
})


UIAchievementPanel = 0
UIAppearancePanel = 1
AutoCollect = 2
AutoCombat = 3
UIBagPanel = 4
UIBusinessPanel = 5
ChangeTarget = 6
Chat = 7
CityBattle = 8
UICityBattlePanel = 9
MineBattle = 10
UIMineBattleManagePanel = 11
UICollectionPanel = 12
UICrusadeSystemPanel = 13
UIDrawPetPanel = 14
UIEquipTrainingPanel = 15
UIEquipMakePanel = 16
UIEquipIntensifyPanel = 17
UIEquipClassPanel = 18
UIEquipEnchantingPanel = 19
UIEquipRnuePanel = 20
UIEquipBlessPanel = 21
UIEquipUnbundlePanel = 22
ExitDun = 23
UIFriendPanel = 24
GrowthGuide = 25
Guild = 26
UIGuildPanel = 27
UIGuildLobbyPanel = 28
Line = 29
UIMailPanel = 30
UIMapPanel = 31
UIPayStorePanel = 32
UIPetPanel = 33
UIPKProtectPanel = 34
UIPortableSetPanel = 35
Raid = 36
UIRankPanel = 37
UIRedPacketPanel = 38
UIRewardTaskPanel = 39
GeneralAttack = 40
Dodge = 41
Sprint = 42
Jump = 43
Fly = 44
MageSkill01 = 45
MageSkill02 = 46
MageSkill03 = 47
MageSkill04 = 48
MageSkill05 = 49
MageSkill06 = 50
MageSkill07 = 51
MageSkill08 = 52
MageSkill09 = 53
MageSkill10 = 54
MageSkill11 = 55
MageSkill12 = 56
MageSkillUlt = 57
TaoistSkill01 = 58
TaoistSkill02 = 59
TaoistSkill03 = 60
TaoistSkill04 = 61
TaoistSkill05 = 62
TaoistSkill06 = 63
TaoistSkill07 = 64
TaoistSkill08 = 65
TaoistSkill09 = 66
TaoistSkill10 = 67
TaoistSkill11 = 68
TaoistSkill12 = 69
TaoistSkillUlt = 70
WarriorSkill01 = 71
WarriorSkill02 = 72
WarriorSkill03 = 73
WarriorSkill04 = 74
WarriorSkill05 = 75
WarriorSkill06 = 76
WarriorSkill07 = 77
WarriorSkill08 = 78
WarriorSkill09 = 79
WarriorSkill10 = 80
WarriorSkill11 = 81
WarriorSkill12 = 82
WarriorSkillUlt = 83
UISkillSystemPanel = 84
UISquarePanel = 85
UISynthesisSystemPanel = 86
UIPropMakePanel = 87
UITaskInfoPanel = 88
Team = 89
UITeamDunPanel = 90
UI_camera = 91
UI_cards = 92
UI_hp = 93
UI_level = 94
UI_score = 95
UIWarehousePanel = 96
UIActivitiesPanel = 97
SevenSign = 98
UIWonderLandPanel = 99
UIRoleAuthorizationPanel = 100
UIPracticePanel = 101
DeathDrop = 102
QuickSettings = 103
TenSign = 104
Meridian = 105
Attention = 106
phoneBind = 107
LevelReward = 108
MonthCard = 109
Enemy = 110
Duel = 111
Questionnaire = 112
PcLoginReward = 113
xinyuanchengopentask = 114
tongxingguopentask = 115
feishayaosaiopentask = 116
jinglingcunopentask = 117
jinglingbaodianopentask = 118
shikuzoulangopentask = 119
xinyuanchenjiaoopentask = 120
zuke1Fopentask = 121
zuke2Fopentask = 122
zuke3Fopentask = 123
zuke4Fopentask = 124
zuke5Fopentask = 125
zuke6Fopentask = 126
yueguang1Fopentask = 127
yueguang2Fopentask = 128
yueguang3Fopentask = 129
yueguang4Fopentask = 130
yueguang5Fopentask = 131
GuildBossChallenge = 132
queueServer = 133



funcDic = _tools.RODict({
    "UIAchievementPanel" : 0,
    "UIAppearancePanel" : 1,
    "AutoCollect" : 2,
    "AutoCombat" : 3,
    "UIBagPanel" : 4,
    "UIBusinessPanel" : 5,
    "ChangeTarget" : 6,
    "Chat" : 7,
    "CityBattle" : 8,
    "UICityBattlePanel" : 9,
    "MineBattle" : 10,
    "UIMineBattleManagePanel" : 11,
    "UICollectionPanel" : 12,
    "UICrusadeSystemPanel" : 13,
    "UIDrawPetPanel" : 14,
    "UIEquipTrainingPanel" : 15,
    "UIEquipMakePanel" : 16,
    "UIEquipIntensifyPanel" : 17,
    "UIEquipClassPanel" : 18,
    "UIEquipEnchantingPanel" : 19,
    "UIEquipRnuePanel" : 20,
    "UIEquipBlessPanel" : 21,
    "UIEquipUnbundlePanel" : 22,
    "ExitDun" : 23,
    "UIFriendPanel" : 24,
    "GrowthGuide" : 25,
    "Guild" : 26,
    "UIGuildPanel" : 27,
    "UIGuildLobbyPanel" : 28,
    "Line" : 29,
    "UIMailPanel" : 30,
    "UIMapPanel" : 31,
    "UIPayStorePanel" : 32,
    "UIPetPanel" : 33,
    "UIPKProtectPanel" : 34,
    "UIPortableSetPanel" : 35,
    "Raid" : 36,
    "UIRankPanel" : 37,
    "UIRedPacketPanel" : 38,
    "UIRewardTaskPanel" : 39,
    "GeneralAttack" : 40,
    "Dodge" : 41,
    "Sprint" : 42,
    "Jump" : 43,
    "Fly" : 44,
    "MageSkill01" : 45,
    "MageSkill02" : 46,
    "MageSkill03" : 47,
    "MageSkill04" : 48,
    "MageSkill05" : 49,
    "MageSkill06" : 50,
    "MageSkill07" : 51,
    "MageSkill08" : 52,
    "MageSkill09" : 53,
    "MageSkill10" : 54,
    "MageSkill11" : 55,
    "MageSkill12" : 56,
    "MageSkillUlt" : 57,
    "TaoistSkill01" : 58,
    "TaoistSkill02" : 59,
    "TaoistSkill03" : 60,
    "TaoistSkill04" : 61,
    "TaoistSkill05" : 62,
    "TaoistSkill06" : 63,
    "TaoistSkill07" : 64,
    "TaoistSkill08" : 65,
    "TaoistSkill09" : 66,
    "TaoistSkill10" : 67,
    "TaoistSkill11" : 68,
    "TaoistSkill12" : 69,
    "TaoistSkillUlt" : 70,
    "WarriorSkill01" : 71,
    "WarriorSkill02" : 72,
    "WarriorSkill03" : 73,
    "WarriorSkill04" : 74,
    "WarriorSkill05" : 75,
    "WarriorSkill06" : 76,
    "WarriorSkill07" : 77,
    "WarriorSkill08" : 78,
    "WarriorSkill09" : 79,
    "WarriorSkill10" : 80,
    "WarriorSkill11" : 81,
    "WarriorSkill12" : 82,
    "WarriorSkillUlt" : 83,
    "UISkillSystemPanel" : 84,
    "UISquarePanel" : 85,
    "UISynthesisSystemPanel" : 86,
    "UIPropMakePanel" : 87,
    "UITaskInfoPanel" : 88,
    "Team" : 89,
    "UITeamDunPanel" : 90,
    "UI_camera" : 91,
    "UI_cards" : 92,
    "UI_hp" : 93,
    "UI_level" : 94,
    "UI_score" : 95,
    "UIWarehousePanel" : 96,
    "UIActivitiesPanel" : 97,
    "SevenSign" : 98,
    "UIWonderLandPanel" : 99,
    "UIRoleAuthorizationPanel" : 100,
    "UIPracticePanel" : 101,
    "DeathDrop" : 102,
    "QuickSettings" : 103,
    "TenSign" : 104,
    "Meridian" : 105,
    "Attention" : 106,
    "phoneBind" : 107,
    "LevelReward" : 108,
    "MonthCard" : 109,
    "Enemy" : 110,
    "Duel" : 111,
    "Questionnaire" : 112,
    "PcLoginReward" : 113,
    "xinyuanchengopentask" : 114,
    "tongxingguopentask" : 115,
    "feishayaosaiopentask" : 116,
    "jinglingcunopentask" : 117,
    "jinglingbaodianopentask" : 118,
    "shikuzoulangopentask" : 119,
    "xinyuanchenjiaoopentask" : 120,
    "zuke1Fopentask" : 121,
    "zuke2Fopentask" : 122,
    "zuke3Fopentask" : 123,
    "zuke4Fopentask" : 124,
    "zuke5Fopentask" : 125,
    "zuke6Fopentask" : 126,
    "yueguang1Fopentask" : 127,
    "yueguang2Fopentask" : 128,
    "yueguang3Fopentask" : 129,
    "yueguang4Fopentask" : 130,
    "yueguang5Fopentask" : 131,
    "GuildBossChallenge" : 132,
    "queueServer" : 133,
})
reverseFuncDic = _tools.RODict({
    0 : "UIAchievementPanel",
    1 : "UIAppearancePanel",
    2 : "AutoCollect",
    3 : "AutoCombat",
    4 : "UIBagPanel",
    5 : "UIBusinessPanel",
    6 : "ChangeTarget",
    7 : "Chat",
    8 : "CityBattle",
    9 : "UICityBattlePanel",
    10 : "MineBattle",
    11 : "UIMineBattleManagePanel",
    12 : "UICollectionPanel",
    13 : "UICrusadeSystemPanel",
    14 : "UIDrawPetPanel",
    15 : "UIEquipTrainingPanel",
    16 : "UIEquipMakePanel",
    17 : "UIEquipIntensifyPanel",
    18 : "UIEquipClassPanel",
    19 : "UIEquipEnchantingPanel",
    20 : "UIEquipRnuePanel",
    21 : "UIEquipBlessPanel",
    22 : "UIEquipUnbundlePanel",
    23 : "ExitDun",
    24 : "UIFriendPanel",
    25 : "GrowthGuide",
    26 : "Guild",
    27 : "UIGuildPanel",
    28 : "UIGuildLobbyPanel",
    29 : "Line",
    30 : "UIMailPanel",
    31 : "UIMapPanel",
    32 : "UIPayStorePanel",
    33 : "UIPetPanel",
    34 : "UIPKProtectPanel",
    35 : "UIPortableSetPanel",
    36 : "Raid",
    37 : "UIRankPanel",
    38 : "UIRedPacketPanel",
    39 : "UIRewardTaskPanel",
    40 : "GeneralAttack",
    41 : "Dodge",
    42 : "Sprint",
    43 : "Jump",
    44 : "Fly",
    45 : "MageSkill01",
    46 : "MageSkill02",
    47 : "MageSkill03",
    48 : "MageSkill04",
    49 : "MageSkill05",
    50 : "MageSkill06",
    51 : "MageSkill07",
    52 : "MageSkill08",
    53 : "MageSkill09",
    54 : "MageSkill10",
    55 : "MageSkill11",
    56 : "MageSkill12",
    57 : "MageSkillUlt",
    58 : "TaoistSkill01",
    59 : "TaoistSkill02",
    60 : "TaoistSkill03",
    61 : "TaoistSkill04",
    62 : "TaoistSkill05",
    63 : "TaoistSkill06",
    64 : "TaoistSkill07",
    65 : "TaoistSkill08",
    66 : "TaoistSkill09",
    67 : "TaoistSkill10",
    68 : "TaoistSkill11",
    69 : "TaoistSkill12",
    70 : "TaoistSkillUlt",
    71 : "WarriorSkill01",
    72 : "WarriorSkill02",
    73 : "WarriorSkill03",
    74 : "WarriorSkill04",
    75 : "WarriorSkill05",
    76 : "WarriorSkill06",
    77 : "WarriorSkill07",
    78 : "WarriorSkill08",
    79 : "WarriorSkill09",
    80 : "WarriorSkill10",
    81 : "WarriorSkill11",
    82 : "WarriorSkill12",
    83 : "WarriorSkillUlt",
    84 : "UISkillSystemPanel",
    85 : "UISquarePanel",
    86 : "UISynthesisSystemPanel",
    87 : "UIPropMakePanel",
    88 : "UITaskInfoPanel",
    89 : "Team",
    90 : "UITeamDunPanel",
    91 : "UI_camera",
    92 : "UI_cards",
    93 : "UI_hp",
    94 : "UI_level",
    95 : "UI_score",
    96 : "UIWarehousePanel",
    97 : "UIActivitiesPanel",
    98 : "SevenSign",
    99 : "UIWonderLandPanel",
    100 : "UIRoleAuthorizationPanel",
    101 : "UIPracticePanel",
    102 : "DeathDrop",
    103 : "QuickSettings",
    104 : "TenSign",
    105 : "Meridian",
    106 : "Attention",
    107 : "phoneBind",
    108 : "LevelReward",
    109 : "MonthCard",
    110 : "Enemy",
    111 : "Duel",
    112 : "Questionnaire",
    113 : "PcLoginReward",
    114 : "xinyuanchengopentask",
    115 : "tongxingguopentask",
    116 : "feishayaosaiopentask",
    117 : "jinglingcunopentask",
    118 : "jinglingbaodianopentask",
    119 : "shikuzoulangopentask",
    120 : "xinyuanchenjiaoopentask",
    121 : "zuke1Fopentask",
    122 : "zuke2Fopentask",
    123 : "zuke3Fopentask",
    124 : "zuke4Fopentask",
    125 : "zuke5Fopentask",
    126 : "zuke6Fopentask",
    127 : "yueguang1Fopentask",
    128 : "yueguang2Fopentask",
    129 : "yueguang3Fopentask",
    130 : "yueguang4Fopentask",
    131 : "yueguang5Fopentask",
    132 : "GuildBossChallenge",
    133 : "queueServer",
})
levelDic = _tools.RODict({
    4 : _tools.ROList([
        2,
        3,
    ]),
    21 : _tools.ROList([
        5,
    ]),
    999 : _tools.ROList([
        8,
        9,
    ]),
    30 : _tools.ROList([
        10,
        11,
        125,
    ]),
    19 : _tools.ROList([
        12,
        86,
        87,
        132,
    ]),
    27 : _tools.ROList([
        13,
    ]),
    15 : _tools.ROList([
        17,
        51,
        64,
        77,
    ]),
    20 : _tools.ROList([
        18,
        52,
        65,
        78,
    ]),
    25 : _tools.ROList([
        19,
    ]),
    28 : _tools.ROList([
        20,
    ]),
    31 : _tools.ROList([
        21,
    ]),
    18 : _tools.ROList([
        26,
        27,
        28,
    ]),
    9 : _tools.ROList([
        38,
        49,
        62,
        75,
        109,
    ]),
    6 : _tools.ROList([
        48,
        61,
        74,
    ]),
    12 : _tools.ROList([
        50,
        63,
        76,
    ]),
    26 : _tools.ROList([
        53,
        66,
        79,
        99,
    ]),
    32 : _tools.ROList([
        54,
        67,
        80,
    ]),
    40 : _tools.ROList([
        55,
        68,
        81,
    ]),
    48 : _tools.ROList([
        56,
        69,
        82,
    ]),
    16 : _tools.ROList([
        90,
    ]),
    90 : _tools.ROList([
        100,
    ]),
    10 : _tools.ROList([
        101,
    ]),
})
taskDic = _tools.RODict({
    86060115 : _tools.ROList([
        0,
        2,
        7,
        23,
        24,
        25,
        29,
        30,
        31,
        32,
        34,
        35,
        36,
        37,
        38,
        44,
        89,
        96,
        100,
        102,
        109,
    ]),
    86010027 : _tools.ROList([
        1,
    ]),
    86010069 : _tools.ROList([
        5,
    ]),
    86010083 : _tools.ROList([
        10,
        11,
    ]),
    86010077 : _tools.ROList([
        13,
    ]),
    86010037 : _tools.ROList([
        14,
        33,
    ]),
    86050006 : _tools.ROList([
        15,
        16,
        22,
    ]),
    86010078 : _tools.ROList([
        17,
    ]),
    86010046 : _tools.ROList([
        18,
    ]),
    86010079 : _tools.ROList([
        19,
    ]),
    86010080 : _tools.ROList([
        20,
    ]),
    86010082 : _tools.ROList([
        21,
    ]),
    86050036 : _tools.ROList([
        26,
        27,
        28,
    ]),
    86010018 : _tools.ROList([
        39,
    ]),
    86060055 : _tools.ROList([
        45,
        58,
        71,
    ]),
    86060061 : _tools.ROList([
        46,
        59,
        72,
    ]),
    86060089 : _tools.ROList([
        47,
        60,
        73,
    ]),
    86060090 : _tools.ROList([
        57,
        70,
        83,
    ]),
    86010016 : _tools.ROList([
        84,
    ]),
    86010070 : _tools.ROList([
        85,
    ]),
    86060104 : _tools.ROList([
        88,
    ]),
    86010068 : _tools.ROList([
        90,
    ]),
    86010003 : _tools.ROList([
        97,
        98,
        104,
        106,
        107,
        108,
        112,
        113,
    ]),
    86010081 : _tools.ROList([
        99,
    ]),
    86010005 : _tools.ROList([
        101,
        105,
    ]),
})
dayDic = _tools.RODict({
})
maxBit = 133

typeToMain = {'equip_make': 'equip', 'equip_strengthen': 'equip', 'equip_class': 'equip', 'equip_FuLing': 'equip', 'equip_weaponGlyph': 'equip', 'equip_Bless': 'equip', 'equip_Unbundle': 'equip', 'UI_camera': 'UI', 'UI_cards': 'UI', 'UI_hp': 'UI', 'UI_level': 'UI', 'UI_score': 'UI'}
