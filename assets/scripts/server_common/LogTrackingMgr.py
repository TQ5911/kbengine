# -*- coding: utf-8 -*-
import json
import time
from enum import Enum
from KBEDebug import *
import KBEngine
import gamelog
import gameconfig
import utils
import gameglobal

class LogTrackingMgr:
    # 用户属性通用
    @staticmethod
    def Server_User_Set(GBID, distinctId, player_gid, player_obid, player_uid, channel, platform, server_id, gender, role_id, role_class, role_name, role_create_time, game_id, online, enemy_num, role_order, first_login_time, first_pay_time, last_login_time, last_pay_time, current_bind_yuanbao, current_copper, current_experience, current_guild_contribution, current_xuantie, current_yuanbao, current_guild_id, current_guild_name, current_level, current_map_id, current_power, current_level_rank, current_score_rank, current_achievement_rank, month_bcard_invoke, month_bcard_left, month_scard_invoke, month_scard_left, total_login_day, total_online_time, total_pay_amount, total_pay_count, friends_num, **kwargs):
        args = {}
        args["trackName"] = "Server_User_Set"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "user_set"
        args["#event_name"] = "Server_User_Set"
        args["player_gid"] = str(player_gid)
        args["player_obid"] = player_obid
        args["player_uid"] = player_uid
        args["channel"] = str(channel)
        args["platform"] = str(platform)
        args["server_id"] = server_id
        args["gender"] = gender
        args["role_id"] = role_id
        args["role_class"] = role_class
        args["role_name"] = role_name
        args["role_create_time"] = role_create_time
        args["game_id"] = str(game_id)
        args["online"] = online
        args["enemy_num"] = enemy_num
        args["role_order"] = role_order
        args["first_login_time"] = first_login_time
        args["first_pay_time"] = first_pay_time
        args["last_login_time"] = last_login_time
        args["last_pay_time"] = last_pay_time
        args["current_bind_yuanbao"] = current_bind_yuanbao
        args["current_copper"] = current_copper
        args["current_experience"] = current_experience
        args["current_guild_contribution"] = current_guild_contribution
        args["current_xuantie"] = current_xuantie
        args["current_yuanbao"] = current_yuanbao
        args["current_guild_id"] = current_guild_id
        args["current_guild_name"] = str(current_guild_name)
        args["current_level"] = current_level
        args["current_map_id"] = current_map_id
        args["current_power"] = current_power
        args["current_level_rank"] = current_level_rank
        args["current_score_rank"] = current_score_rank
        args["current_achievement_rank"] = current_achievement_rank
        args["month_bcard_invoke"] = month_bcard_invoke
        args["month_bcard_left"] = month_bcard_left
        args["month_scard_invoke"] = month_scard_invoke
        args["month_scard_left"] = month_scard_left
        args["total_login_day"] = total_login_day
        args["total_online_time"] = total_online_time
        args["total_pay_amount"] = total_pay_amount
        args["total_pay_count"] = total_pay_count
        args["friends_num"] = friends_num
        LogTrackingMgr.LOG(args, kwargs)

    # 充值完成事件
    @staticmethod
    def Server_Recharge_Complete(GBID, distinctId, account_id, role_id, item_type, item_id, price, order_id, **kwargs):
        args = {}
        args["trackName"] = "Server_Recharge_Complete"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Server_Recharge_Complete"
        args["account_id"] = str(account_id)
        args["role_id"] = str(role_id)
        args["item_type"] = str(item_type)
        args["item_id"] = str(item_id)
        args["price"] = price
        args["order_id"] = str(order_id)
        LogTrackingMgr.LOG(args, kwargs)

    # 设置用户帮会相关属性
    @staticmethod
    def Guild_User_Set(GBID, distinctId, job, **kwargs):
        args = {}
        args["trackName"] = "Guild_User_Set"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "user_set"
        args["#event_name"] = "Guild_User_Set"
        args["job"] = str(job)
        LogTrackingMgr.LOG(args, kwargs)

    # PCU事件
    @staticmethod
    def Server_Pcu(GBID, distinctId, server_id, pcu, **kwargs):
        args = {}
        args["trackName"] = "Server_Pcu"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Server_Pcu"
        args["server_id"] = server_id
        args["pcu"] = pcu
        LogTrackingMgr.LOG(args, kwargs)

    # 用户登出事件
    @staticmethod
    def Server_Logout(GBID, distinctId, account_id, device_model, ip_address, operating_system, channel_source, package_source, **kwargs):
        args = {}
        args["trackName"] = "Server_Logout"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Server_Logout"
        args["account_id"] = str(account_id)
        args["device_model"] = str(device_model)
        args["ip_address"] = str(ip_address)
        args["operating_system"] = str(operating_system)
        args["channel_source"] = str(channel_source)
        args["package_source"] = str(package_source)
        LogTrackingMgr.LOG(args, kwargs)

    # 用户登录事件
    @staticmethod
    def Server_Login(GBID, distinctId, account_id, device_model, ip_address, operating_system, account_type, channel_source, package_source, device, last_login_time, login_time, app_version, user_info_id, patch, **kwargs):
        args = {}
        args["trackName"] = "Server_Login"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Server_Login"
        args["account_id"] = str(account_id)
        args["device_model"] = str(device_model)
        args["ip_address"] = str(ip_address)
        args["operating_system"] = str(operating_system)
        args["account_type"] = str(account_type)
        args["channel_source"] = str(channel_source)
        args["package_source"] = str(package_source)
        args["device"] = str(device)
        args["last_login_time"] = last_login_time
        args["login_time"] = login_time
        args["app_version"] = str(app_version)
        args["user_info_id"] = str(user_info_id)
        args["patch"] = str(patch)
        LogTrackingMgr.LOG(args, kwargs)

    # 角色登录事件
    @staticmethod
    def Server_Role_Login(GBID, distinctId, account_id, gb_id, ob_id, school, name, level, game_id, user_info_id, create_timestamp, account_type, channel_source, package_source, log_type, score, experience, money, coin, map_id, **kwargs):
        args = {}
        args["trackName"] = "Server_Role_Login"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Server_Role_Login"
        args["account_id"] = str(account_id)
        args["gb_id"] = gb_id
        args["ob_id"] = ob_id
        args["school"] = school
        args["name"] = str(name)
        args["level"] = level
        args["game_id"] = str(game_id)
        args["user_info_id"] = str(user_info_id)
        args["create_timestamp"] = create_timestamp
        args["account_type"] = str(account_type)
        args["channel_source"] = str(channel_source)
        args["package_source"] = str(package_source)
        args["log_type"] = log_type
        args["score"] = score
        args["experience"] = experience
        args["money"] = money
        args["coin"] = coin
        args["map_id"] = map_id
        LogTrackingMgr.LOG(args, kwargs)

    # 角色登出事件
    @staticmethod
    def Server_Role_Logout(GBID, distinctId, account_id, gb_id, school, name, level, package_source, score, experience, money, coin, map_id, reason, **kwargs):
        args = {}
        args["trackName"] = "Server_Role_Logout"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Server_Role_Logout"
        args["account_id"] = str(account_id)
        args["gb_id"] = gb_id
        args["school"] = school
        args["name"] = str(name)
        args["level"] = level
        args["package_source"] = str(package_source)
        args["score"] = score
        args["experience"] = experience
        args["money"] = money
        args["coin"] = coin
        args["map_id"] = map_id
        args["reason"] = reason
        LogTrackingMgr.LOG(args, kwargs)

    # 创建角色事件
    @staticmethod
    def Server_Create_Role(GBID, distinctId, account_id, gb_id, school, name, game_id, user_info_id, create_timestamp, package_source, face_id, face_color_id, hair_id, hair_color_id, creation_order, sex, **kwargs):
        args = {}
        args["trackName"] = "Server_Create_Role"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Server_Create_Role"
        args["account_id"] = str(account_id)
        args["gb_id"] = gb_id
        args["school"] = school
        args["name"] = str(name)
        args["game_id"] = str(game_id)
        args["user_info_id"] = str(user_info_id)
        args["create_timestamp"] = create_timestamp
        args["package_source"] = str(package_source)
        args["face_id"] = face_id
        args["face_color_id"] = face_color_id
        args["hair_id"] = hair_id
        args["hair_color_id"] = hair_color_id
        args["creation_order"] = creation_order
        args["sex"] = sex
        LogTrackingMgr.LOG(args, kwargs)

    # 善恶值变化事件
    @staticmethod
    def Moral_Change(GBID, distinctId, gb_id, moral, delta, src_type, **kwargs):
        args = {}
        args["trackName"] = "Moral_Change"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Moral_Change"
        args["gb_id"] = gb_id
        args["moral"] = moral
        args["delta"] = delta
        args["src_type"] = src_type
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会排行榜
    @staticmethod
    def LeaderBoard_Guild(GBID, distinctId, type, rank, guild_uuid, guild_name, guild_level, guild_score, **kwargs):
        args = {}
        args["trackName"] = "LeaderBoard_Guild"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "LeaderBoard_Guild"
        args["type"] = type
        args["rank"] = rank
        args["guild_uuid"] = guild_uuid
        args["guild_name"] = str(guild_name)
        args["guild_level"] = guild_level
        args["guild_score"] = guild_score
        LogTrackingMgr.LOG(args, kwargs)

    # 玩家等级排行榜
    @staticmethod
    def LeaderBoard_Level(GBID, distinctId, type, rank, gb_id, name, level, school, guild_uuid, guild_name, **kwargs):
        args = {}
        args["trackName"] = "LeaderBoard_Level"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "LeaderBoard_Level"
        args["type"] = type
        args["rank"] = rank
        args["gb_id"] = gb_id
        args["name"] = str(name)
        args["level"] = level
        args["school"] = school
        args["guild_uuid"] = guild_uuid
        args["guild_name"] = str(guild_name)
        LogTrackingMgr.LOG(args, kwargs)

    # 玩家其他排行榜
    @staticmethod
    def LeaderBoard_Avatar(GBID, distinctId, type, rank, gb_id, name, level, score, school, guild_uuid, guild_name, **kwargs):
        args = {}
        args["trackName"] = "LeaderBoard_Avatar"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "LeaderBoard_Avatar"
        args["type"] = type
        args["rank"] = rank
        args["gb_id"] = gb_id
        args["name"] = str(name)
        args["level"] = level
        args["score"] = score
        args["school"] = school
        args["guild_uuid"] = guild_uuid
        args["guild_name"] = str(guild_name)
        LogTrackingMgr.LOG(args, kwargs)

    # 玩家成就排行榜
    @staticmethod
    def LeaderBoard_Achievement(GBID, distinctId, type, rank, gb_id, name, level, point, school, guild_uuid, guild_name, **kwargs):
        args = {}
        args["trackName"] = "LeaderBoard_Achievement"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "LeaderBoard_Achievement"
        args["type"] = type
        args["rank"] = rank
        args["gb_id"] = gb_id
        args["name"] = str(name)
        args["level"] = level
        args["point"] = point
        args["school"] = school
        args["guild_uuid"] = guild_uuid
        args["guild_name"] = str(guild_name)
        LogTrackingMgr.LOG(args, kwargs)

    # 合成道具事件
    @staticmethod
    def item_composite(GBID, distinctId, gb_id, item_composite_type, if_auto, get_item_info, desc, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "item_composite"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "item_composite"
        args["gb_id"] = gb_id
        args["item_composite_type"] = str(item_composite_type)
        args["if_auto"] = if_auto
        args["get_item_info"] = str(get_item_info)
        args["desc"] = str(desc)
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 矿战开启事件
    @staticmethod
    def mineBattle_start(GBID, distinctId, minebattle_area_id, minebattle_activity_start_time, core_belong_guild_id, **kwargs):
        args = {}
        args["trackName"] = "mineBattle_start"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "mineBattle_start"
        args["minebattle_area_id"] = str(minebattle_area_id)
        args["minebattle_activity_start_time"] = str(minebattle_activity_start_time)
        args["core_belong_guild_id"] = str(core_belong_guild_id)
        LogTrackingMgr.LOG(args, kwargs)

    # 矿战结束事件
    @staticmethod
    def mineBattle_end(GBID, distinctId, minebattle_area_id, minebattle_activity_end_time, core_belong_guild_id, core_belong_time, **kwargs):
        args = {}
        args["trackName"] = "mineBattle_end"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "mineBattle_end"
        args["minebattle_area_id"] = str(minebattle_area_id)
        args["minebattle_activity_end_time"] = str(minebattle_activity_end_time)
        args["core_belong_guild_id"] = str(core_belong_guild_id)
        args["core_belong_time"] = str(core_belong_time)
        LogTrackingMgr.LOG(args, kwargs)

    # 矿战结束后奖励事件
    @staticmethod
    def mineBattle_reward(GBID, distinctId, minebattle_area_id, activity_end_time, activity_rank, **kwargs):
        args = {}
        args["trackName"] = "mineBattle_reward"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "mineBattle_reward"
        args["minebattle_area_id"] = str(minebattle_area_id)
        args["activity_end_time"] = str(activity_end_time)
        args["activity_rank"] = str(activity_rank)
        LogTrackingMgr.LOG(args, kwargs)

    # 矿战分红事件
    @staticmethod
    def mineBattle_dividendedCurrency(GBID, distinctId, gb_id, mining_area_belong_guild_id, mining_area_output, dividended_player_id, dividended_currency_num, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "mineBattle_dividendedCurrency"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "mineBattle_dividendedCurrency"
        args["gb_id"] = gb_id
        args["mining_area_belong_guild_id"] = str(mining_area_belong_guild_id)
        args["mining_area_output"] = str(mining_area_output)
        args["dividended_player_id"] = str(dividended_player_id)
        args["dividended_currency_num"] = dividended_currency_num
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 矿战击杀旗帜事件
    @staticmethod
    def mineBattle_flagEvent(GBID, distinctId, minebattle_area_id, killer_guild_id, gb_id, flag_death_times, **kwargs):
        args = {}
        args["trackName"] = "mineBattle_flagEvent"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "mineBattle_flagEvent"
        args["minebattle_area_id"] = str(minebattle_area_id)
        args["killer_guild_id"] = str(killer_guild_id)
        args["gb_id"] = gb_id
        args["flag_death_times"] = str(flag_death_times)
        LogTrackingMgr.LOG(args, kwargs)

    # 矿战击杀水晶事件
    @staticmethod
    def mineBattle_coreEvent(GBID, distinctId, minebattle_area_id, killer_guild_id, gb_id, **kwargs):
        args = {}
        args["trackName"] = "mineBattle_coreEvent"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "mineBattle_coreEvent"
        args["minebattle_area_id"] = str(minebattle_area_id)
        args["killer_guild_id"] = str(killer_guild_id)
        args["gb_id"] = gb_id
        LogTrackingMgr.LOG(args, kwargs)

    # 好友操作事件
    @staticmethod
    def Friend_Opr(GBID, distinctId, gb_id, other_gb_id, friend_num, opr, other_school, other_score, **kwargs):
        args = {}
        args["trackName"] = "Friend_Opr"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Friend_Opr"
        args["gb_id"] = gb_id
        args["other_gb_id"] = other_gb_id
        args["friend_num"] = friend_num
        args["opr"] = opr
        args["other_school"] = other_school
        args["other_score"] = other_score
        LogTrackingMgr.LOG(args, kwargs)

    # 技能升级事件
    @staticmethod
    def Skill_Upgrade(GBID, distinctId, gb_id, id, cost_item_id, cost_item_num, cost_currency_id, cost_currency_num, level, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Skill_Upgrade"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Skill_Upgrade"
        args["gb_id"] = gb_id
        args["id"] = str(id)
        args["cost_item_id"] = cost_item_id
        args["cost_item_num"] = cost_item_num
        args["cost_currency_id"] = str(cost_currency_id)
        args["cost_currency_num"] = cost_currency_num
        args["level"] = level
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 发红包事件
    @staticmethod
    def Release_RedBag(GBID, distinctId, gb_id, send_type, send_channel, send_number, send_cost_item_id, send_cost_item_num, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Release_RedBag"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Release_RedBag"
        args["gb_id"] = gb_id
        args["send_type"] = send_type
        args["send_channel"] = send_channel
        args["send_number"] = send_number
        args["send_cost_item_id"] = str(send_cost_item_id)
        args["send_cost_item_num"] = send_cost_item_num
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 领红包事件
    @staticmethod
    def Fetch_RedBag(GBID, distinctId, gb_id, get_type, get_channel, get_item_id, get_item_num, claimed_remain_number, claimed_remain_item_id, claimed_remain_item_num, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Fetch_RedBag"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Fetch_RedBag"
        args["gb_id"] = gb_id
        args["get_type"] = get_type
        args["get_channel"] = get_channel
        args["get_item_id"] = str(get_item_id)
        args["get_item_num"] = get_item_num
        args["claimed_remain_number"] = claimed_remain_number
        args["claimed_remain_item_id"] = str(claimed_remain_item_id)
        args["claimed_remain_item_num"] = claimed_remain_item_num
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 退还红包事件
    @staticmethod
    def Return_RedBag(GBID, distinctId, gb_id, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Return_RedBag"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Return_RedBag"
        args["gb_id"] = gb_id
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 公会信息事件
    @staticmethod
    def Guild_Info(GBID, distinctId, guild_uuid, level, guild_exp, fund_num, gold_num, token_num, src, op_uuid, desc, **kwargs):
        args = {}
        args["trackName"] = "Guild_Info"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Guild_Info"
        args["guild_uuid"] = guild_uuid
        args["level"] = level
        args["guild_exp"] = guild_exp
        args["fund_num"] = fund_num
        args["gold_num"] = gold_num
        args["token_num"] = token_num
        args["src"] = src
        args["op_uuid"] = op_uuid
        args["desc"] = str(desc)
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会操作相关
    @staticmethod
    def Guild_Opr(GBID, distinctId, guild_uuid, gb_id, guild_member_num, guild_level, operation, **kwargs):
        args = {}
        args["trackName"] = "Guild_Opr"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Guild_Opr"
        args["guild_uuid"] = guild_uuid
        args["gb_id"] = gb_id
        args["guild_member_num"] = guild_member_num
        args["guild_level"] = guild_level
        args["operation"] = operation
        LogTrackingMgr.LOG(args, kwargs)

    # 公会练功场重置
    @staticmethod
    def Guild_Train_Reset(GBID, distinctId, gb_id, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Guild_Train_Reset"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Guild_Train_Reset"
        args["gb_id"] = gb_id
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 公会练功场事件
    @staticmethod
    def Guild_Train(GBID, distinctId, gb_id, train_id, train_level, train_prop, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Guild_Train"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Guild_Train"
        args["gb_id"] = gb_id
        args["train_id"] = train_id
        args["train_level"] = train_level
        args["train_prop"] = str(train_prop)
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 公会任务事件
    @staticmethod
    def Guild_Task(GBID, distinctId, gb_id, task_id, task_progress, task_state, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Guild_Task"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Guild_Task"
        args["gb_id"] = gb_id
        args["task_id"] = task_id
        args["task_progress"] = task_progress
        args["task_state"] = task_state
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 公会商店事件
    @staticmethod
    def Guild_Shop(GBID, distinctId, shop_sell_item_id, shop_sell_times, **kwargs):
        args = {}
        args["trackName"] = "Guild_Shop"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Guild_Shop"
        args["shop_sell_item_id"] = str(shop_sell_item_id)
        args["shop_sell_times"] = shop_sell_times
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会聚义楼协助
    @staticmethod
    def Guild_Assist(GBID, distinctId, guild_building_id, src_gb_id, guild_uuid, guild_building_level, exp, op_uuid, src, **kwargs):
        args = {}
        args["trackName"] = "Guild_Assist"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Guild_Assist"
        args["guild_building_id"] = guild_building_id
        args["src_gb_id"] = src_gb_id
        args["guild_uuid"] = guild_uuid
        args["guild_building_level"] = guild_building_level
        args["exp"] = exp
        args["op_uuid"] = op_uuid
        args["src"] = src
        LogTrackingMgr.LOG(args, kwargs)

    # 好友聊天事件
    @staticmethod
    def Friend_Msg(GBID, distinctId, gb_id, friend_gb_id, msg, is_online, is_friend, **kwargs):
        args = {}
        args["trackName"] = "Friend_Msg"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Friend_Msg"
        args["gb_id"] = gb_id
        args["friend_gb_id"] = friend_gb_id
        args["msg"] = str(msg)
        args["is_online"] = is_online
        args["is_friend"] = is_friend
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会军需处协助
    @staticmethod
    def Guild_QiXieAssist(GBID, distinctId, guild_war_equipment_id, src_gb_id, guild_uuid, guild_war_equipment_level, exp, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Guild_QiXieAssist"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Guild_QiXieAssist"
        args["guild_war_equipment_id"] = guild_war_equipment_id
        args["src_gb_id"] = src_gb_id
        args["guild_uuid"] = guild_uuid
        args["guild_war_equipment_level"] = guild_war_equipment_level
        args["exp"] = exp
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 魔方事件
    @staticmethod
    def Cube_Info(GBID, distinctId, gb_id, game_id, floor, map_id, cube_event, left_time, **kwargs):
        args = {}
        args["trackName"] = "Cube_Info"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Cube_Info"
        args["gb_id"] = gb_id
        args["game_id"] = str(game_id)
        args["floor"] = floor
        args["map_id"] = map_id
        args["cube_event"] = cube_event
        args["left_time"] = left_time
        LogTrackingMgr.LOG(args, kwargs)

    # 仙境事件
    @staticmethod
    def Wonderland_Info(GBID, distinctId, gb_id, game_id, floor, wonder_land_event, left_time, **kwargs):
        args = {}
        args["trackName"] = "Wonderland_Info"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Wonderland_Info"
        args["gb_id"] = gb_id
        args["game_id"] = str(game_id)
        args["floor"] = floor
        args["wonder_land_event"] = wonder_land_event
        args["left_time"] = left_time
        LogTrackingMgr.LOG(args, kwargs)

    # 成就事件
    @staticmethod
    def Achievement_Update(GBID, distinctId, account_id, gb_id, game_id, achieve_id, version, state, progress, sum_point, **kwargs):
        args = {}
        args["trackName"] = "Achievement_Update"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Achievement_Update"
        args["account_id"] = str(account_id)
        args["gb_id"] = gb_id
        args["game_id"] = str(game_id)
        args["achieve_id"] = str(achieve_id)
        args["version"] = str(version)
        args["state"] = state
        args["progress"] = progress
        args["sum_point"] = sum_point
        LogTrackingMgr.LOG(args, kwargs)

    # 道具事件
    @staticmethod
    def item_flow(GBID, distinctId, account_id, gb_id, game_id, item_id, unique_id, bag_type, bind_type, before_num, change_num, after_num, change_reason, op_uuid, desc, **kwargs):
        args = {}
        args["trackName"] = "item_flow"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "item_flow"
        args["account_id"] = str(account_id)
        args["gb_id"] = gb_id
        args["game_id"] = str(game_id)
        args["item_id"] = item_id
        args["unique_id"] = unique_id
        args["bag_type"] = bag_type
        args["bind_type"] = bind_type
        args["before_num"] = before_num
        args["change_num"] = change_num
        args["after_num"] = after_num
        args["change_reason"] = change_reason
        args["op_uuid"] = op_uuid
        args["desc"] = str(desc)
        LogTrackingMgr.LOG(args, kwargs)

    # 通用死亡事件
    @staticmethod
    def Common_Death(GBID, distinctId, map_id, killer_id, killer_type, death_location, **kwargs):
        args = {}
        args["trackName"] = "Common_Death"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Common_Death"
        args["map_id"] = map_id
        args["killer_id"] = killer_id
        args["killer_type"] = str(killer_type)
        args["death_location"] = str(death_location)
        LogTrackingMgr.LOG(args, kwargs)

    # 装备制造
    @staticmethod
    def equip_make(GBID, distinctId, op_uuid, gb_id, unique_id, equip_id, equip_name, equip_type, count, equip_grade, equip_quality, bind_value, make_type, base_attrs, upgrade_attrs, enhance_attrs, equip_power, equip_attrs, **kwargs):
        args = {}
        args["trackName"] = "equip_make"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "equip_make"
        args["op_uuid"] = op_uuid
        args["gb_id"] = gb_id
        args["unique_id"] = unique_id
        args["equip_id"] = equip_id
        args["equip_name"] = str(equip_name)
        args["equip_type"] = equip_type
        args["count"] = count
        args["equip_grade"] = equip_grade
        args["equip_quality"] = equip_quality
        args["bind_value"] = bind_value
        args["make_type"] = make_type
        args["base_attrs"] = str(base_attrs)
        args["upgrade_attrs"] = str(upgrade_attrs)
        args["enhance_attrs"] = str(enhance_attrs)
        args["equip_power"] = equip_power
        args["equip_attrs"] = str(equip_attrs)
        LogTrackingMgr.LOG(args, kwargs)

    # 装备强化
    @staticmethod
    def equip_enhancement(GBID, distinctId, op_uuid, gb_id, unique_id, equip_id, equip_name, equip_type, equip_grade, equip_quality, equip_belong_to, base_attrs_before, enhance_attrs_before, upgrade_attrs_before, base_attrs_after, enhance_attrs_after, upgrade_attrs_after, add_bind_value_before, add_bind_value_after, consumed_item_bind_value, enhance_level_before, enhance_level_after, enhance_result, equip_power, bind_value_before, bind_value_after, equip_attrs, equip_attrs_after, **kwargs):
        args = {}
        args["trackName"] = "equip_enhancement"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "equip_enhancement"
        args["op_uuid"] = op_uuid
        args["gb_id"] = gb_id
        args["unique_id"] = unique_id
        args["equip_id"] = equip_id
        args["equip_name"] = equip_name
        args["equip_type"] = equip_type
        args["equip_grade"] = equip_grade
        args["equip_quality"] = equip_quality
        args["equip_belong_to"] = equip_belong_to
        args["base_attrs_before"] = str(base_attrs_before)
        args["enhance_attrs_before"] = str(enhance_attrs_before)
        args["upgrade_attrs_before"] = str(upgrade_attrs_before)
        args["base_attrs_after"] = str(base_attrs_after)
        args["enhance_attrs_after"] = str(enhance_attrs_after)
        args["upgrade_attrs_after"] = str(upgrade_attrs_after)
        args["add_bind_value_before"] = add_bind_value_before
        args["add_bind_value_after"] = add_bind_value_after
        args["consumed_item_bind_value"] = consumed_item_bind_value
        args["enhance_level_before"] = enhance_level_before
        args["enhance_level_after"] = enhance_level_after
        args["enhance_result"] = enhance_result
        args["equip_power"] = equip_power
        args["bind_value_before"] = bind_value_before
        args["bind_value_after"] = bind_value_after
        args["equip_attrs"] = str(equip_attrs)
        args["equip_attrs_after"] = str(equip_attrs_after)
        LogTrackingMgr.LOG(args, kwargs)

    # 装备附灵
    @staticmethod
    def equip_spirit(GBID, distinctId, op_uuid, gb_id, unique_id, equip_id, equip_name, equip_type, equip_grade, equip_quality, equip_belong_to, equip_attrs, equip_attrs_after, add_bind_value_before, add_bind_value_after, consumed_item_bind_value, equip_power, spirit_ref_id, bind_value_before, bind_value_after, **kwargs):
        args = {}
        args["trackName"] = "equip_spirit"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "equip_spirit"
        args["op_uuid"] = op_uuid
        args["gb_id"] = gb_id
        args["unique_id"] = unique_id
        args["equip_id"] = equip_id
        args["equip_name"] = str(equip_name)
        args["equip_type"] = equip_type
        args["equip_grade"] = equip_grade
        args["equip_quality"] = equip_quality
        args["equip_belong_to"] = equip_belong_to
        args["equip_attrs"] = str(equip_attrs)
        args["equip_attrs_after"] = str(equip_attrs_after)
        args["add_bind_value_before"] = add_bind_value_before
        args["add_bind_value_after"] = add_bind_value_after
        args["consumed_item_bind_value"] = consumed_item_bind_value
        args["equip_power"] = equip_power
        args["spirit_ref_id"] = spirit_ref_id
        args["bind_value_before"] = bind_value_before
        args["bind_value_after"] = bind_value_after
        LogTrackingMgr.LOG(args, kwargs)

    # 装备升阶
    @staticmethod
    def equip_upgrade(GBID, distinctId, op_uuid, gb_id, unique_id, equip_id, equip_name, equip_type, equip_grade, equip_quality, equip_belong_to, base_attrs_before, enhance_attrs_before, upgrade_attrs_before, base_attrs_after, enhance_attrs_after, upgrade_attrs_after, equip_grade_before, equip_grade_after, bind_value_before, bind_value_after, equip_power, equip_attrs, equip_attrs_after, **kwargs):
        args = {}
        args["trackName"] = "equip_upgrade"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "equip_upgrade"
        args["op_uuid"] = op_uuid
        args["gb_id"] = gb_id
        args["unique_id"] = unique_id
        args["equip_id"] = equip_id
        args["equip_name"] = str(equip_name)
        args["equip_type"] = equip_type
        args["equip_grade"] = equip_grade
        args["equip_quality"] = equip_quality
        args["equip_belong_to"] = equip_belong_to
        args["base_attrs_before"] = str(base_attrs_before)
        args["enhance_attrs_before"] = str(enhance_attrs_before)
        args["upgrade_attrs_before"] = str(upgrade_attrs_before)
        args["base_attrs_after"] = str(base_attrs_after)
        args["enhance_attrs_after"] = str(enhance_attrs_after)
        args["upgrade_attrs_after"] = str(upgrade_attrs_after)
        args["equip_grade_before"] = equip_grade_before
        args["equip_grade_after"] = equip_grade_after
        args["bind_value_before"] = bind_value_before
        args["bind_value_after"] = bind_value_after
        args["equip_power"] = equip_power
        args["equip_attrs"] = str(equip_attrs)
        args["equip_attrs_after"] = str(equip_attrs_after)
        LogTrackingMgr.LOG(args, kwargs)

    # 装备铭文
    @staticmethod
    def equip_glyph(GBID, distinctId, op_uuid, gb_id, unique_id, equip_id, equip_name, equip_type, equip_grade, equip_quality, equip_belong_to, equip_attrs, equip_attrs_after, add_bind_value_before, add_bind_value_after, consumed_item_bind_value, equip_power, glyph_ref_id, glyph_pos, bind_value_before, bind_value_after, **kwargs):
        args = {}
        args["trackName"] = "equip_glyph"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "equip_glyph"
        args["op_uuid"] = op_uuid
        args["gb_id"] = gb_id
        args["unique_id"] = unique_id
        args["equip_id"] = equip_id
        args["equip_name"] = str(equip_name)
        args["equip_type"] = equip_type
        args["equip_grade"] = equip_grade
        args["equip_quality"] = equip_quality
        args["equip_belong_to"] = equip_belong_to
        args["equip_attrs"] = str(equip_attrs)
        args["equip_attrs_after"] = str(equip_attrs_after)
        args["add_bind_value_before"] = add_bind_value_before
        args["add_bind_value_after"] = add_bind_value_after
        args["consumed_item_bind_value"] = consumed_item_bind_value
        args["equip_power"] = equip_power
        args["glyph_ref_id"] = glyph_ref_id
        args["glyph_pos"] = glyph_pos
        args["bind_value_before"] = bind_value_before
        args["bind_value_after"] = bind_value_after
        LogTrackingMgr.LOG(args, kwargs)

    # 装备祝福
    @staticmethod
    def equip_bless(GBID, distinctId, op_uuid, gb_id, unique_id, equip_id, equip_name, equip_type, equip_grade, equip_quality, equip_belong_to, equip_attrs, equip_attrs_After, add_bind_value_before, add_bind_value_after, consumed_item_bind_value, bless_lv_rate_before, bless_lv_rate_after, bless_max_lv_before, bless_max_lv_after, equip_power, bind_data_before, bind_data_after, **kwargs):
        args = {}
        args["trackName"] = "equip_bless"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "equip_bless"
        args["op_uuid"] = op_uuid
        args["gb_id"] = gb_id
        args["unique_id"] = unique_id
        args["equip_id"] = equip_id
        args["equip_name"] = str(equip_name)
        args["equip_type"] = equip_type
        args["equip_grade"] = equip_grade
        args["equip_quality"] = equip_quality
        args["equip_belong_to"] = equip_belong_to
        args["equip_attrs"] = str(equip_attrs)
        args["equip_attrs_After"] = str(equip_attrs_After)
        args["add_bind_value_before"] = add_bind_value_before
        args["add_bind_value_after"] = add_bind_value_after
        args["consumed_item_bind_value"] = consumed_item_bind_value
        args["bless_lv_rate_before"] = bless_lv_rate_before
        args["bless_lv_rate_after"] = bless_lv_rate_after
        args["bless_max_lv_before"] = bless_max_lv_before
        args["bless_max_lv_after"] = bless_max_lv_after
        args["equip_power"] = equip_power
        args["bind_data_before"] = bind_data_before
        args["bind_data_after"] = bind_data_after
        LogTrackingMgr.LOG(args, kwargs)

    # 装备绑定值洗涤
    @staticmethod
    def Equip_BindValue_Washing(GBID, distinctId, op_uuid, gb_id, unique_id, equip_id, equip_belong_to, bind_value_washing_before, bind_value_washing_after, add_bind_value_status_before, add_bind_value_status_after, wash_count, **kwargs):
        args = {}
        args["trackName"] = "Equip_BindValue_Washing"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Equip_BindValue_Washing"
        args["op_uuid"] = op_uuid
        args["gb_id"] = gb_id
        args["unique_id"] = unique_id
        args["equip_id"] = equip_id
        args["equip_belong_to"] = equip_belong_to
        args["bind_value_washing_before"] = bind_value_washing_before
        args["bind_value_washing_after"] = bind_value_washing_after
        args["add_bind_value_status_before"] = add_bind_value_status_before
        args["add_bind_value_status_after"] = add_bind_value_status_after
        args["wash_count"] = wash_count
        LogTrackingMgr.LOG(args, kwargs)

    # 道具工坊
    @staticmethod
    def workshop(GBID, distinctId, op_uuid, gb_id, workshop_target_items, batch_count, workshop_normal_items, workshop_lucky_items, **kwargs):
        args = {}
        args["trackName"] = "workshop"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "workshop"
        args["op_uuid"] = op_uuid
        args["gb_id"] = gb_id
        args["workshop_target_items"] = str(workshop_target_items)
        args["batch_count"] = batch_count
        args["workshop_normal_items"] = str(workshop_normal_items)
        args["workshop_lucky_items"] = str(workshop_lucky_items)
        LogTrackingMgr.LOG(args, kwargs)

    # 等级有礼事件
    @staticmethod
    def Level_Reward(GBID, distinctId, gb_id, level, welfare_id, level_limit, school, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Level_Reward"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Level_Reward"
        args["gb_id"] = gb_id
        args["level"] = level
        args["welfare_id"] = welfare_id
        args["level_limit"] = level_limit
        args["school"] = school
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 七日签到事件
    @staticmethod
    def Welfare_SignInSevenDay(GBID, distinctId, gb_id, welfare_id, level, login_day, day_id, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Welfare_SignInSevenDay"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Welfare_SignInSevenDay"
        args["gb_id"] = gb_id
        args["welfare_id"] = welfare_id
        args["level"] = level
        args["login_day"] = login_day
        args["day_id"] = day_id
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 十日签到事件
    @staticmethod
    def Welfare_SignInTenDay(GBID, distinctId, gb_id, welfare_id, level, login_day, day_id, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Welfare_SignInTenDay"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Welfare_SignInTenDay"
        args["gb_id"] = gb_id
        args["welfare_id"] = welfare_id
        args["level"] = level
        args["login_day"] = login_day
        args["day_id"] = day_id
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 月卡事件
    @staticmethod
    def MonthCard_Invoke(GBID, distinctId, gb_id, level, invoke_time, expire_time, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "MonthCard_Invoke"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "MonthCard_Invoke"
        args["gb_id"] = gb_id
        args["level"] = level
        args["invoke_time"] = invoke_time
        args["expire_time"] = expire_time
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 月卡挂机事件
    @staticmethod
    def MonthCard_Afk(GBID, distinctId, gb_id, time_left, time_city, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "MonthCard_Afk"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "MonthCard_Afk"
        args["gb_id"] = gb_id
        args["time_left"] = time_left
        args["time_city"] = time_city
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 月卡离线挂机事件
    @staticmethod
    def MonthCard_Offline(GBID, distinctId, gb_id, time_left, time_offline, **kwargs):
        args = {}
        args["trackName"] = "MonthCard_Offline"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "MonthCard_Offline"
        args["gb_id"] = gb_id
        args["time_left"] = time_left
        args["time_offline"] = time_offline
        LogTrackingMgr.LOG(args, kwargs)

    # 月卡离线奖励领取
    @staticmethod
    def MonthCard_OfflineReward(GBID, distinctId, gb_id, afk_reward_type, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "MonthCard_OfflineReward"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "MonthCard_OfflineReward"
        args["gb_id"] = gb_id
        args["afk_reward_type"] = afk_reward_type
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 礼包购买
    @staticmethod
    def Gift_Buy(GBID, distinctId, gb_id, buy_package__id, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Gift_Buy"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Gift_Buy"
        args["gb_id"] = gb_id
        args["buy_package__id"] = buy_package__id
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 升级
    @staticmethod
    def Level_LevelUp(GBID, distinctId, gb_id, pre_level, curr_level, upgrade_exp, total_exp, exp_src, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Level_LevelUp"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Level_LevelUp"
        args["gb_id"] = gb_id
        args["pre_level"] = pre_level
        args["curr_level"] = curr_level
        args["upgrade_exp"] = upgrade_exp
        args["total_exp"] = total_exp
        args["exp_src"] = exp_src
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # GM指令
    @staticmethod
    def GM_GM(GBID, distinctId, src, command, gm_args, **kwargs):
        args = {}
        args["trackName"] = "GM_GM"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "GM_GM"
        args["src"] = str(src)
        args["command"] = str(command)
        args["gm_args"] = str(gm_args)
        LogTrackingMgr.LOG(args, kwargs)

    # 货币兑换
    @staticmethod
    def Currency_Exchange(GBID, distinctId, gb_id, exchange_id, op_uuid, daily_limit, daily_used_before, daily_used_after, **kwargs):
        args = {}
        args["trackName"] = "Currency_Exchange"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Currency_Exchange"
        args["gb_id"] = gb_id
        args["exchange_id"] = exchange_id
        args["op_uuid"] = op_uuid
        args["daily_limit"] = daily_limit
        args["daily_used_before"] = daily_used_before
        args["daily_used_after"] = daily_used_after
        LogTrackingMgr.LOG(args, kwargs)

    # 商店购买
    @staticmethod
    def Store_Buy(GBID, distinctId, gb_id, mall_id, mall_type, product_id, real_item_id, item_num, limit_type, limit_num, buy_num, cost_info, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Store_Buy"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Store_Buy"
        args["gb_id"] = gb_id
        args["mall_id"] = mall_id
        args["mall_type"] = mall_type
        args["product_id"] = product_id
        args["real_item_id"] = real_item_id
        args["item_num"] = item_num
        args["limit_type"] = limit_type
        args["limit_num"] = limit_num
        args["buy_num"] = buy_num
        args["cost_info"] = str(cost_info)
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 收集事件
    @staticmethod
    def collectible_detail(GBID, distinctId, collect_id, prop_change, status, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "collectible_detail"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "collectible_detail"
        args["collect_id"] = collect_id
        args["prop_change"] = str(prop_change)
        args["status"] = status
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 抽卡事件
    @staticmethod
    def DrawCard_Detail(GBID, distinctId, gb_id, pool_id, pool_group_id, roll_cost, real_roll_num, item_list, bef_pity_num, aft_pity_num, pity_pull_num, bef_guaranteed, aft_guaranteed, guaranteed_type, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "DrawCard_Detail"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "DrawCard_Detail"
        args["gb_id"] = gb_id
        args["pool_id"] = pool_id
        args["pool_group_id"] = pool_group_id
        args["roll_cost"] = roll_cost
        args["real_roll_num"] = real_roll_num
        args["item_list"] = item_list
        args["bef_pity_num"] = bef_pity_num
        args["aft_pity_num"] = aft_pity_num
        args["pity_pull_num"] = pity_pull_num
        args["bef_guaranteed"] = bef_guaranteed
        args["aft_guaranteed"] = aft_guaranteed
        args["guaranteed_type"] = guaranteed_type
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 抽卡保底
    @staticmethod
    def DrawCard_GuaranteedReward(GBID, distinctId, gb_id, pool_id, pool_group_id, pity_reward, guaranteed, guaranteed_type, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "DrawCard_GuaranteedReward"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "DrawCard_GuaranteedReward"
        args["gb_id"] = gb_id
        args["pool_id"] = pool_id
        args["pool_group_id"] = pool_group_id
        args["pity_reward"] = pity_reward
        args["guaranteed"] = guaranteed
        args["guaranteed_type"] = guaranteed_type
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 采集事件
    @staticmethod
    def Gather_Collection(GBID, distinctId, gb_id, collection_id, collection_type, start_time, end_time, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Gather_Collection"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Gather_Collection"
        args["gb_id"] = gb_id
        args["collection_id"] = collection_id
        args["collection_type"] = collection_type
        args["start_time"] = start_time
        args["end_time"] = end_time
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会副本开启
    @staticmethod
    def Guild_BossChallenge_Open(GBID, distinctId, op_uuid, guild_uuid, job, open_type, consume_type, consume_count, open_dungeon_id, open_time, opened_money_count, opened_fund_count, **kwargs):
        args = {}
        args["trackName"] = "Guild_BossChallenge_Open"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Guild_BossChallenge_Open"
        args["op_uuid"] = op_uuid
        args["guild_uuid"] = guild_uuid
        args["job"] = job
        args["open_type"] = open_type
        args["consume_type"] = consume_type
        args["consume_count"] = consume_count
        args["open_dungeon_id"] = open_dungeon_id
        args["open_time"] = open_time
        args["opened_money_count"] = opened_money_count
        args["opened_fund_count"] = opened_fund_count
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会副本取消开启
    @staticmethod
    def Guild_BossChallenge_Cancel(GBID, distinctId, op_uuid, guild_uuid, cancel_type, consume_type, consume_count, open_dungeon_id, open_time, opened_money_count, opened_fund_count, **kwargs):
        args = {}
        args["trackName"] = "Guild_BossChallenge_Cancel"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Guild_BossChallenge_Cancel"
        args["op_uuid"] = op_uuid
        args["guild_uuid"] = guild_uuid
        args["cancel_type"] = cancel_type
        args["consume_type"] = consume_type
        args["consume_count"] = consume_count
        args["open_dungeon_id"] = open_dungeon_id
        args["open_time"] = open_time
        args["opened_money_count"] = opened_money_count
        args["opened_fund_count"] = opened_fund_count
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会副本恢复回退
    @staticmethod
    def Guild_BossChallenge_Recover(GBID, distinctId, op_uuid, guild_uuid, cancel_type, consume_type, consume_count, open_dungeon_id, open_time, opened_money_count, opened_fund_count, **kwargs):
        args = {}
        args["trackName"] = "Guild_BossChallenge_Recover"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Guild_BossChallenge_Recover"
        args["op_uuid"] = op_uuid
        args["guild_uuid"] = guild_uuid
        args["cancel_type"] = cancel_type
        args["consume_type"] = consume_type
        args["consume_count"] = consume_count
        args["open_dungeon_id"] = open_dungeon_id
        args["open_time"] = open_time
        args["opened_money_count"] = opened_money_count
        args["opened_fund_count"] = opened_fund_count
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会副本创建
    @staticmethod
    def Guild_BossChallenge_CreateDungeon(GBID, distinctId, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Guild_BossChallenge_CreateDungeon"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Guild_BossChallenge_CreateDungeon"
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会副本倒计时开启
    @staticmethod
    def Guild_BossChallenge_CDOpen(GBID, distinctId, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Guild_BossChallenge_CDOpen"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Guild_BossChallenge_CDOpen"
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会副本副本结算
    @staticmethod
    def Guild_BossChallenge_Settlement(GBID, distinctId, op_uuid, gb_id, is_clear, dmg_score, dmg_rank, is_first_clear, first_pass_rewards, rank_rewards, **kwargs):
        args = {}
        args["trackName"] = "Guild_BossChallenge_Settlement"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Guild_BossChallenge_Settlement"
        args["op_uuid"] = op_uuid
        args["gb_id"] = gb_id
        args["is_clear"] = is_clear
        args["dmg_score"] = dmg_score
        args["dmg_rank"] = dmg_rank
        args["is_first_clear"] = is_first_clear
        args["first_pass_rewards"] = str(first_pass_rewards)
        args["rank_rewards"] = str(rank_rewards)
        LogTrackingMgr.LOG(args, kwargs)

    # 扩容（背包或者仓库）
    @staticmethod
    def Capacity_Expansion(GBID, distinctId, op_uuid, gb_id, type, capacity_before, expansion_count, capacity_after, player_level, consume_items, **kwargs):
        args = {}
        args["trackName"] = "Capacity_Expansion"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Capacity_Expansion"
        args["op_uuid"] = op_uuid
        args["gb_id"] = gb_id
        args["type"] = type
        args["capacity_before"] = capacity_before
        args["expansion_count"] = expansion_count
        args["capacity_after"] = capacity_after
        args["player_level"] = player_level
        args["consume_items"] = str(consume_items)
        LogTrackingMgr.LOG(args, kwargs)

    # 道具或者装备分解
    @staticmethod
    def Item_Disassembly(GBID, distinctId, op_uuid, gb_id, type, disassemble_items, reward_items, disassemble_settings, **kwargs):
        args = {}
        args["trackName"] = "Item_Disassembly"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Item_Disassembly"
        args["op_uuid"] = op_uuid
        args["gb_id"] = gb_id
        args["type"] = type
        args["disassemble_items"] = str(disassemble_items)
        args["reward_items"] = str(reward_items)
        args["disassemble_settings"] = disassemble_settings
        LogTrackingMgr.LOG(args, kwargs)

    # 传送
    @staticmethod
    def teleport(GBID, distinctId, from_map_id, to_map_id, **kwargs):
        args = {}
        args["trackName"] = "teleport"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "teleport"
        args["from_map_id"] = from_map_id
        args["to_map_id"] = to_map_id
        LogTrackingMgr.LOG(args, kwargs)

    # 怪物死亡
    @staticmethod
    def Kill_Monster(GBID, distinctId, monster_id, map_id, gid, suffix, **kwargs):
        args = {}
        args["trackName"] = "Kill_Monster"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Kill_Monster"
        args["monster_id"] = monster_id
        args["map_id"] = map_id
        args["gid"] = gid
        args["suffix"] = suffix
        LogTrackingMgr.LOG(args, kwargs)

    # 任务状态变更
    @staticmethod
    def Task_State_Change(GBID, distinctId, gb_id, task_id, task_state, task_type, task_map, player_level, **kwargs):
        args = {}
        args["trackName"] = "Task_State_Change"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Task_State_Change"
        args["gb_id"] = gb_id
        args["task_id"] = task_id
        args["task_state"] = task_state
        args["task_type"] = task_type
        args["task_map"] = task_map
        args["player_level"] = player_level
        LogTrackingMgr.LOG(args, kwargs)

    # pc引流奖励
    @staticmethod
    def Welfare_PcDrainage(GBID, distinctId, account_id, gb_id, device_model, claim_timestamp, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Welfare_PcDrainage"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Welfare_PcDrainage"
        args["account_id"] = str(account_id)
        args["gb_id"] = gb_id
        args["device_model"] = str(device_model)
        args["claim_timestamp"] = claim_timestamp
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 副本门票消耗
    @staticmethod
    def Dungeon_Ticket_Consume(GBID, distinctId, unique_id, dungeon_type, dungeon_id, ticket_type, enter_type, player_count, gb_id, score, player_level, **kwargs):
        args = {}
        args["trackName"] = "Dungeon_Ticket_Consume"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Dungeon_Ticket_Consume"
        args["unique_id"] = unique_id
        args["dungeon_type"] = dungeon_type
        args["dungeon_id"] = dungeon_id
        args["ticket_type"] = ticket_type
        args["enter_type"] = enter_type
        args["player_count"] = player_count
        args["gb_id"] = gb_id
        args["score"] = score
        args["player_level"] = player_level
        LogTrackingMgr.LOG(args, kwargs)

    # Boss出生
    @staticmethod
    def Dungeon_Boss_Born(GBID, distinctId, unique_id, dungeon_type, dungeon_id, space_uuid, space_no, monster_id, born_time, dungeon_start_time, **kwargs):
        args = {}
        args["trackName"] = "Dungeon_Boss_Born"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Dungeon_Boss_Born"
        args["unique_id"] = unique_id
        args["dungeon_type"] = dungeon_type
        args["dungeon_id"] = dungeon_id
        args["space_uuid"] = space_uuid
        args["space_no"] = space_no
        args["monster_id"] = monster_id
        args["born_time"] = born_time
        args["dungeon_start_time"] = dungeon_start_time
        LogTrackingMgr.LOG(args, kwargs)

    # Boss死亡
    @staticmethod
    def Dungeon_Boss_Dead(GBID, distinctId, unique_id, dungeon_type, dungeon_id, space_uuid, space_no, monster_id, born_time, dead_time, dungeon_start_time, **kwargs):
        args = {}
        args["trackName"] = "Dungeon_Boss_Dead"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Dungeon_Boss_Dead"
        args["unique_id"] = unique_id
        args["dungeon_type"] = dungeon_type
        args["dungeon_id"] = dungeon_id
        args["space_uuid"] = space_uuid
        args["space_no"] = space_no
        args["monster_id"] = monster_id
        args["born_time"] = born_time
        args["dead_time"] = dead_time
        args["dungeon_start_time"] = dungeon_start_time
        LogTrackingMgr.LOG(args, kwargs)

    # 副本结算
    @staticmethod
    def Dungeon_Settlement(GBID, distinctId, unique_id, dungeon_type, dungeon_id, space_uuid, space_no, gb_id, is_clear, is_first_clear, finish_time, is_win, reason_type, finished_player_count, dead_count, first_rewards, clear_rewards, gold_rewards, auto_battle_times, player_score, player_level, fight_score, **kwargs):
        args = {}
        args["trackName"] = "Dungeon_Settlement"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Dungeon_Settlement"
        args["unique_id"] = unique_id
        args["dungeon_type"] = dungeon_type
        args["dungeon_id"] = dungeon_id
        args["space_uuid"] = space_uuid
        args["space_no"] = space_no
        args["gb_id"] = gb_id
        args["is_clear"] = is_clear
        args["is_first_clear"] = is_first_clear
        args["finish_time"] = finish_time
        args["is_win"] = is_win
        args["reason_type"] = reason_type
        args["finished_player_count"] = finished_player_count
        args["dead_count"] = dead_count
        args["first_rewards"] = str(first_rewards)
        args["clear_rewards"] = str(clear_rewards)
        args["gold_rewards"] = str(gold_rewards)
        args["auto_battle_times"] = auto_battle_times
        args["player_score"] = player_score
        args["player_level"] = player_level
        args["fight_score"] = fight_score
        LogTrackingMgr.LOG(args, kwargs)

    # 更新经验
    @staticmethod
    def Update_Exp(GBID, distinctId, gb_id, delta_val, modify_val, op_uuid, src, space_no, level, **kwargs):
        args = {}
        args["trackName"] = "Update_Exp"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Update_Exp"
        args["gb_id"] = gb_id
        args["delta_val"] = delta_val
        args["modify_val"] = modify_val
        args["op_uuid"] = op_uuid
        args["src"] = src
        args["space_no"] = space_no
        args["level"] = level
        LogTrackingMgr.LOG(args, kwargs)

    # 装备掉装
    @staticmethod
    def drop_equip(GBID, distinctId, drop_player_id, drop_player_name, drop_player_gid, unique_id, drop_equip_id, drop_equip_quality, drop_equip_grade, drop_equip_scene, drop_equip_pos, **kwargs):
        args = {}
        args["trackName"] = "drop_equip"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "drop_equip"
        args["drop_player_id"] = drop_player_id
        args["drop_player_name"] = str(drop_player_name)
        args["drop_player_gid"] = str(drop_player_gid)
        args["unique_id"] = unique_id
        args["drop_equip_id"] = drop_equip_id
        args["drop_equip_quality"] = drop_equip_quality
        args["drop_equip_grade"] = drop_equip_grade
        args["drop_equip_scene"] = drop_equip_scene
        args["drop_equip_pos"] = drop_equip_pos
        LogTrackingMgr.LOG(args, kwargs)

    # 装备拾取
    @staticmethod
    def pickup_equip(GBID, distinctId, pickup_player_id, pickup_player_name, pickup_player_gid, unique_id, pickup_equip_id, pickup_equip_quality, pickup_equip_grade, pickup_equip_scene, pickup_equip_pos, **kwargs):
        args = {}
        args["trackName"] = "pickup_equip"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "pickup_equip"
        args["pickup_player_id"] = pickup_player_id
        args["pickup_player_name"] = str(pickup_player_name)
        args["pickup_player_gid"] = str(pickup_player_gid)
        args["unique_id"] = unique_id
        args["pickup_equip_id"] = pickup_equip_id
        args["pickup_equip_quality"] = pickup_equip_quality
        args["pickup_equip_grade"] = pickup_equip_grade
        args["pickup_equip_scene"] = pickup_equip_scene
        args["pickup_equip_pos"] = pickup_equip_pos
        LogTrackingMgr.LOG(args, kwargs)

    # 帮会关系
    @staticmethod
    def Guild_Relation(GBID, distinctId, guild_uuid1, guild_uuid2, operation, end_time, **kwargs):
        args = {}
        args["trackName"] = "Guild_Relation"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Guild_Relation"
        args["guild_uuid1"] = guild_uuid1
        args["guild_uuid2"] = guild_uuid2
        args["operation"] = operation
        args["end_time"] = end_time
        LogTrackingMgr.LOG(args, kwargs)

    # 物品移动
    @staticmethod
    def Item_Movement(GBID, distinctId, op_uuid, gb_id, unique_id, item_id, item_count, item_bind_type, move_type, **kwargs):
        args = {}
        args["trackName"] = "Item_Movement"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Item_Movement"
        args["op_uuid"] = op_uuid
        args["gb_id"] = gb_id
        args["unique_id"] = unique_id
        args["item_id"] = item_id
        args["item_count"] = item_count
        args["item_bind_type"] = item_bind_type
        args["move_type"] = move_type
        LogTrackingMgr.LOG(args, kwargs)

    # 经脉升级
    @staticmethod
    def Meridian_UpGrade(GBID, distinctId, op_uuid, gb_id, meridian_id, point_id, new_level, **kwargs):
        args = {}
        args["trackName"] = "Meridian_UpGrade"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Meridian_UpGrade"
        args["op_uuid"] = op_uuid
        args["gb_id"] = gb_id
        args["meridian_id"] = meridian_id
        args["point_id"] = point_id
        args["new_level"] = new_level
        LogTrackingMgr.LOG(args, kwargs)

    # 经脉强化
    @staticmethod
    def Meridian_Enhance(GBID, distinctId, op_uuid, gb_id, meridian_id, **kwargs):
        args = {}
        args["trackName"] = "Meridian_Enhance"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Meridian_Enhance"
        args["op_uuid"] = op_uuid
        args["gb_id"] = gb_id
        args["meridian_id"] = meridian_id
        LogTrackingMgr.LOG(args, kwargs)

    # 精灵获取
    @staticmethod
    def pet_get(GBID, distinctId, gb_id, op_uuid, pet_id, pet_quality, **kwargs):
        args = {}
        args["trackName"] = "pet_get"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "pet_get"
        args["gb_id"] = gb_id
        args["op_uuid"] = op_uuid
        args["pet_id"] = pet_id
        args["pet_quality"] = pet_quality
        LogTrackingMgr.LOG(args, kwargs)

    # 精灵升级
    @staticmethod
    def pet_levelup(GBID, distinctId, gb_id, op_uuid, pet_id, pet_quality, level_before, new_level, equip, add_power, **kwargs):
        args = {}
        args["trackName"] = "pet_levelup"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "pet_levelup"
        args["gb_id"] = gb_id
        args["op_uuid"] = op_uuid
        args["pet_id"] = pet_id
        args["pet_quality"] = pet_quality
        args["level_before"] = level_before
        args["new_level"] = new_level
        args["equip"] = str(equip)
        args["add_power"] = add_power
        LogTrackingMgr.LOG(args, kwargs)

    # 精灵编组
    @staticmethod
    def pet_make_team(GBID, distinctId, gb_id, player_level, pet_team_id, op_type, pet_id, pet_quality, pet_level, pet_equip, join_team_count, team_pet_count, pet_team_info, **kwargs):
        args = {}
        args["trackName"] = "pet_make_team"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "pet_make_team"
        args["gb_id"] = gb_id
        args["player_level"] = player_level
        args["pet_team_id"] = pet_team_id
        args["op_type"] = op_type
        args["pet_id"] = pet_id
        args["pet_quality"] = pet_quality
        args["pet_level"] = pet_level
        args["pet_equip"] = str(pet_equip)
        args["join_team_count"] = join_team_count
        args["team_pet_count"] = team_pet_count
        args["pet_team_info"] = str(pet_team_info)
        LogTrackingMgr.LOG(args, kwargs)

    # 精灵切换编组
    @staticmethod
    def pet_change_team(GBID, distinctId, gb_id, scene, pet_team_id, pet_team_info, **kwargs):
        args = {}
        args["trackName"] = "pet_change_team"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "pet_change_team"
        args["gb_id"] = gb_id
        args["scene"] = scene
        args["pet_team_id"] = pet_team_id
        args["pet_team_info"] = str(pet_team_info)
        LogTrackingMgr.LOG(args, kwargs)

    # 精灵跟随
    @staticmethod
    def pet_follow_change(GBID, distinctId, gb_id, scene, pet_id, pet_quality, pet_level, pet_equip, op_type, **kwargs):
        args = {}
        args["trackName"] = "pet_follow_change"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "pet_follow_change"
        args["gb_id"] = gb_id
        args["scene"] = scene
        args["pet_id"] = pet_id
        args["pet_quality"] = pet_quality
        args["pet_level"] = pet_level
        args["pet_equip"] = str(pet_equip)
        args["op_type"] = op_type
        LogTrackingMgr.LOG(args, kwargs)

    # 邮件发送
    @staticmethod
    def mail_send(GBID, distinctId, to_gbid, send_mail_id, mail_type, mail_gbid, src_type, src_sub_type, op_uuid, send_mail_source, send_get_item_info, **kwargs):
        args = {}
        args["trackName"] = "mail_send"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "mail_send"
        args["to_gbid"] = to_gbid
        args["send_mail_id"] = send_mail_id
        args["mail_type"] = mail_type
        args["mail_gbid"] = mail_gbid
        args["src_type"] = src_type
        args["src_sub_type"] = src_sub_type
        args["op_uuid"] = op_uuid
        args["send_mail_source"] = send_mail_source
        args["send_get_item_info"] = str(send_get_item_info)
        LogTrackingMgr.LOG(args, kwargs)

    # 邮件查看
    @staticmethod
    def mail_read(GBID, distinctId, to_gbid, from_gbid, check_mail_id, mail_gbid, global_mail_gbid, src_type, src_sub_type, op_uuid, check_mail_source, check_get_item_info, **kwargs):
        args = {}
        args["trackName"] = "mail_read"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "mail_read"
        args["to_gbid"] = to_gbid
        args["from_gbid"] = from_gbid
        args["check_mail_id"] = check_mail_id
        args["mail_gbid"] = mail_gbid
        args["global_mail_gbid"] = global_mail_gbid
        args["src_type"] = src_type
        args["src_sub_type"] = src_sub_type
        args["op_uuid"] = op_uuid
        args["check_mail_source"] = check_mail_source
        args["check_get_item_info"] = str(check_get_item_info)
        LogTrackingMgr.LOG(args, kwargs)

    # 邮件领取
    @staticmethod
    def mail_get(GBID, distinctId, to_gbid, from_gbid, receive_mail_id, mail_gbid, global_mail_gbid, src_type, src_sub_type, op_uuid, receive_mail_source, receive_get_item_info, **kwargs):
        args = {}
        args["trackName"] = "mail_get"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "mail_get"
        args["to_gbid"] = to_gbid
        args["from_gbid"] = from_gbid
        args["receive_mail_id"] = receive_mail_id
        args["mail_gbid"] = mail_gbid
        args["global_mail_gbid"] = global_mail_gbid
        args["src_type"] = src_type
        args["src_sub_type"] = src_sub_type
        args["op_uuid"] = op_uuid
        args["receive_mail_source"] = receive_mail_source
        args["receive_get_item_info"] = str(receive_get_item_info)
        LogTrackingMgr.LOG(args, kwargs)

    # 邮件删除
    @staticmethod
    def mail_delete(GBID, distinctId, to_gbid, from_gbid, delete_mail_id, mail_gbid, global_mail_gbid, src_type, src_sub_type, op_uuid, delete_mail_source, delete_get_item_info, delete_src_type, **kwargs):
        args = {}
        args["trackName"] = "mail_delete"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "mail_delete"
        args["to_gbid"] = to_gbid
        args["from_gbid"] = from_gbid
        args["delete_mail_id"] = delete_mail_id
        args["mail_gbid"] = mail_gbid
        args["global_mail_gbid"] = global_mail_gbid
        args["src_type"] = src_type
        args["src_sub_type"] = src_sub_type
        args["op_uuid"] = op_uuid
        args["delete_mail_source"] = delete_mail_source
        args["delete_get_item_info"] = str(delete_get_item_info)
        args["delete_src_type"] = delete_src_type
        LogTrackingMgr.LOG(args, kwargs)

    # 交易行出售
    @staticmethod
    def auction_item_sale(GBID, distinctId, player_gbid, op_uuid, auction_uuid, auction_item_id, auction_item_type, auction_item_num, auction_item_price, auction_item_price_total, is_publicity, **kwargs):
        args = {}
        args["trackName"] = "auction_item_sale"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "auction_item_sale"
        args["player_gbid"] = player_gbid
        args["op_uuid"] = op_uuid
        args["auction_uuid"] = auction_uuid
        args["auction_item_id"] = auction_item_id
        args["auction_item_type"] = auction_item_type
        args["auction_item_num"] = auction_item_num
        args["auction_item_price"] = auction_item_price
        args["auction_item_price_total"] = auction_item_price_total
        args["is_publicity"] = is_publicity
        LogTrackingMgr.LOG(args, kwargs)

    # 交易行购买
    @staticmethod
    def Auction_ItemBuy(GBID, distinctId, player_gbid, op_uuid, auction_uuid, item_id, auction_buy_item_num, price, **kwargs):
        args = {}
        args["trackName"] = "Auction_ItemBuy"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Auction_ItemBuy"
        args["player_gbid"] = player_gbid
        args["op_uuid"] = op_uuid
        args["auction_uuid"] = auction_uuid
        args["item_id"] = item_id
        args["auction_buy_item_num"] = auction_buy_item_num
        args["price"] = price
        LogTrackingMgr.LOG(args, kwargs)

    # 交易行下架
    @staticmethod
    def auction_item_cancel(GBID, distinctId, player_gbid, auction_uuid, auction_item_id, auction_item_type, auction_item_num, auction_item_price, auction_item_price_total, is_publicity, create_time, add_time, expire_time, auction_type, **kwargs):
        args = {}
        args["trackName"] = "auction_item_cancel"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "auction_item_cancel"
        args["player_gbid"] = player_gbid
        args["auction_uuid"] = auction_uuid
        args["auction_item_id"] = auction_item_id
        args["auction_item_type"] = auction_item_type
        args["auction_item_num"] = auction_item_num
        args["auction_item_price"] = auction_item_price
        args["auction_item_price_total"] = auction_item_price_total
        args["is_publicity"] = is_publicity
        args["create_time"] = create_time
        args["add_time"] = add_time
        args["expire_time"] = expire_time
        args["auction_type"] = auction_type
        LogTrackingMgr.LOG(args, kwargs)

    # 交易行成交
    @staticmethod
    def auction_item_deal(GBID, distinctId, player_gbid, op_uuid, auction_uuid, auction_item_id, auction_item_type, is_publicity, deal_item_num, deal_total_price, real_add_price, tax, from_role_id, from_role_name, from_gid, **kwargs):
        args = {}
        args["trackName"] = "auction_item_deal"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "auction_item_deal"
        args["player_gbid"] = player_gbid
        args["op_uuid"] = op_uuid
        args["auction_uuid"] = auction_uuid
        args["auction_item_id"] = auction_item_id
        args["auction_item_type"] = auction_item_type
        args["is_publicity"] = is_publicity
        args["deal_item_num"] = deal_item_num
        args["deal_total_price"] = deal_total_price
        args["real_add_price"] = real_add_price
        args["tax"] = tax
        args["from_role_id"] = from_role_id
        args["from_role_name"] = str(from_role_name)
        args["from_gid"] = str(from_gid)
        LogTrackingMgr.LOG(args, kwargs)

    # 交易行收藏
    @staticmethod
    def Auction_ItemCollect(GBID, distinctId, player_gbid, collect_data_type, collect_op_type, collect_id, **kwargs):
        args = {}
        args["trackName"] = "Auction_ItemCollect"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Auction_ItemCollect"
        args["player_gbid"] = player_gbid
        args["collect_data_type"] = collect_data_type
        args["collect_op_type"] = collect_op_type
        args["collect_id"] = collect_id
        LogTrackingMgr.LOG(args, kwargs)

    # 混沌回廊ticket事件
    @staticmethod
    def Cube_Ticket(GBID, distinctId, gb_id, src, delta, free, paid, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "Cube_Ticket"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Cube_Ticket"
        args["gb_id"] = gb_id
        args["src"] = src
        args["delta"] = delta
        args["free"] = free
        args["paid"] = paid
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 秘境峰ticket事件
    @staticmethod
    def WonderLand_Ticket(GBID, distinctId, gb_id, src, delta, num, paid, op_uuid, **kwargs):
        args = {}
        args["trackName"] = "WonderLand_Ticket"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "WonderLand_Ticket"
        args["gb_id"] = gb_id
        args["src"] = src
        args["delta"] = delta
        args["num"] = num
        args["paid"] = paid
        args["op_uuid"] = op_uuid
        LogTrackingMgr.LOG(args, kwargs)

    # 速度统计
    @staticmethod
    def Speed_Stat(GBID, distinctId, gb_id, entity_id, player_name, space_no, position, datas, **kwargs):
        args = {}
        args["trackName"] = "Speed_Stat"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Speed_Stat"
        args["gb_id"] = gb_id
        args["entity_id"] = entity_id
        args["player_name"] = str(player_name)
        args["space_no"] = space_no
        args["position"] = str(position)
        args["datas"] = str(datas)
        LogTrackingMgr.LOG(args, kwargs)

    # 非法速度统计
    @staticmethod
    def Illegal_Speed_Stat(GBID, distinctId, gb_id, entity_id, player_name, space_no, position, speed, over_rate, speed_check_window_size, speed_check_count_per_window, speed_check_continuous_unit, **kwargs):
        args = {}
        args["trackName"] = "Illegal_Speed_Stat"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "Illegal_Speed_Stat"
        args["gb_id"] = gb_id
        args["entity_id"] = entity_id
        args["player_name"] = str(player_name)
        args["space_no"] = space_no
        args["position"] = str(position)
        args["speed"] = speed
        args["over_rate"] = over_rate
        args["speed_check_window_size"] = speed_check_window_size
        args["speed_check_count_per_window"] = speed_check_count_per_window
        args["speed_check_continuous_unit"] = speed_check_continuous_unit
        LogTrackingMgr.LOG(args, kwargs)

    # 月卡过期时间设置
    @staticmethod
    def MonthCard_Expire_Time_Set(GBID, distinctId, expire_time, **kwargs):
        args = {}
        args["trackName"] = "MonthCard_Expire_Time_Set"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "MonthCard_Expire_Time_Set"
        args["expire_time"] = expire_time
        LogTrackingMgr.LOG(args, kwargs)

    # 付费奖励发放
    @staticmethod
    def item_issuance(GBID, distinctId, order_id, player_gbid, role_name, server_id, goods_id, stash_status, **kwargs):
        args = {}
        args["trackName"] = "item_issuance"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "item_issuance"
        args["order_id"] = str(order_id)
        args["player_gbid"] = player_gbid
        args["role_name"] = str(role_name)
        args["server_id"] = server_id
        args["goods_id"] = goods_id
        args["stash_status"] = stash_status
        LogTrackingMgr.LOG(args, kwargs)

    # 进保管箱
    @staticmethod
    def deposit_stash(GBID, distinctId, order_id, player_gbid, goods_id, deposit_time, **kwargs):
        args = {}
        args["trackName"] = "deposit_stash"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "deposit_stash"
        args["order_id"] = str(order_id)
        args["player_gbid"] = player_gbid
        args["goods_id"] = goods_id
        args["deposit_time"] = deposit_time
        LogTrackingMgr.LOG(args, kwargs)

    # 领取保管箱
    @staticmethod
    def withdraw_stash(GBID, distinctId, order_id, player_gbid, goods_id, withdraw_time, **kwargs):
        args = {}
        args["trackName"] = "withdraw_stash"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "withdraw_stash"
        args["order_id"] = str(order_id)
        args["player_gbid"] = player_gbid
        args["goods_id"] = goods_id
        args["withdraw_time"] = withdraw_time
        LogTrackingMgr.LOG(args, kwargs)

    # 删除保管箱记录
    @staticmethod
    def delete_stash(GBID, distinctId, order_id, player_gbid, goods_id, record_deleted, record_deleted_time, **kwargs):
        args = {}
        args["trackName"] = "delete_stash"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "delete_stash"
        args["order_id"] = str(order_id)
        args["player_gbid"] = player_gbid
        args["goods_id"] = goods_id
        args["record_deleted"] = record_deleted
        args["record_deleted_time"] = record_deleted_time
        LogTrackingMgr.LOG(args, kwargs)

    # 装备返还
    @staticmethod
    def equip_return(GBID, distinctId, return_player_id, return_player_name, return_player_gid, unique_id, return_equip_id, return_equip_quality, return_equip_grade, return_equip_money, return_equip_type, **kwargs):
        args = {}
        args["trackName"] = "equip_return"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "equip_return"
        args["return_player_id"] = return_player_id
        args["return_player_name"] = str(return_player_name)
        args["return_player_gid"] = str(return_player_gid)
        args["unique_id"] = unique_id
        args["return_equip_id"] = return_equip_id
        args["return_equip_quality"] = return_equip_quality
        args["return_equip_grade"] = return_equip_grade
        args["return_equip_money"] = return_equip_money
        args["return_equip_type"] = return_equip_type
        LogTrackingMgr.LOG(args, kwargs)

    # 资源找回
    @staticmethod
    def resource_recovery(GBID, distinctId, recovery_id, recovery_ticket_num, recovery_ticiet_duration_cost, **kwargs):
        args = {}
        args["trackName"] = "resource_recovery"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "resource_recovery"
        args["recovery_id"] = recovery_id
        args["recovery_ticket_num"] = recovery_ticket_num
        args["recovery_ticiet_duration_cost"] = recovery_ticiet_duration_cost
        LogTrackingMgr.LOG(args, kwargs)

    # 混沌回廊进入事件
    @staticmethod
    def cube_enter(GBID, distinctId, cube_enter_floor_id, cube_enter_time, cube_cost_ticket_id, cube_cost_ticket_num, **kwargs):
        args = {}
        args["trackName"] = "cube_enter"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "cube_enter"
        args["cube_enter_floor_id"] = cube_enter_floor_id
        args["cube_enter_time"] = cube_enter_time
        args["cube_cost_ticket_id"] = cube_cost_ticket_id
        args["cube_cost_ticket_num"] = cube_cost_ticket_num
        LogTrackingMgr.LOG(args, kwargs)

    # 混沌回廊离开事件
    @staticmethod
    def cube_leave(GBID, distinctId, cube_leave_time, cube_leave_reason, **kwargs):
        args = {}
        args["trackName"] = "cube_leave"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "cube_leave"
        args["cube_leave_time"] = cube_leave_time
        args["cube_leave_reason"] = cube_leave_reason
        LogTrackingMgr.LOG(args, kwargs)

    # 混沌回廊购买门票事件
    @staticmethod
    def cube_ticket_buy(GBID, distinctId, cube_buy_ticket_method, cube_buy_ticket_num, **kwargs):
        args = {}
        args["trackName"] = "cube_ticket_buy"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "cube_ticket_buy"
        args["cube_buy_ticket_method"] = cube_buy_ticket_method
        args["cube_buy_ticket_num"] = cube_buy_ticket_num
        LogTrackingMgr.LOG(args, kwargs)

    # 天劫崖进入事件
    @staticmethod
    def wonderland_enter(GBID, distinctId, wonderland_enter_floor_id, wonderland_enter_time, wonderland_cost_ticket_id, wonderland_cost_ticket_num, **kwargs):
        args = {}
        args["trackName"] = "wonderland_enter"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "wonderland_enter"
        args["wonderland_enter_floor_id"] = wonderland_enter_floor_id
        args["wonderland_enter_time"] = wonderland_enter_time
        args["wonderland_cost_ticket_id"] = wonderland_cost_ticket_id
        args["wonderland_cost_ticket_num"] = wonderland_cost_ticket_num
        LogTrackingMgr.LOG(args, kwargs)

    # 天劫崖离开事件
    @staticmethod
    def wonderland_leave(GBID, distinctId, wonderland_leave_time, wonderland_leave_reason, **kwargs):
        args = {}
        args["trackName"] = "wonderland_leave"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "wonderland_leave"
        args["wonderland_leave_time"] = wonderland_leave_time
        args["wonderland_leave_reason"] = wonderland_leave_reason
        LogTrackingMgr.LOG(args, kwargs)

    # 混沌回廊购买门票事件
    @staticmethod
    def wonderland_ticket_buy(GBID, distinctId, wonderland_buy_ticket_method, wonderland_buy_ticket_num, **kwargs):
        args = {}
        args["trackName"] = "wonderland_ticket_buy"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "wonderland_ticket_buy"
        args["wonderland_buy_ticket_method"] = wonderland_buy_ticket_method
        args["wonderland_buy_ticket_num"] = wonderland_buy_ticket_num
        LogTrackingMgr.LOG(args, kwargs)

    # 租赁上架
    @staticmethod
    def rent_item_sale(GBID, distinctId, rent_item_id, rent_item_uuid, rent_item_price, **kwargs):
        args = {}
        args["trackName"] = "rent_item_sale"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "rent_item_sale"
        args["rent_item_id"] = str(rent_item_id)
        args["rent_item_uuid"] = str(rent_item_uuid)
        args["rent_item_price"] = rent_item_price
        LogTrackingMgr.LOG(args, kwargs)

    # 租赁下架
    @staticmethod
    def rent_item_cancel(GBID, distinctId, rent_item_id, rent_item_uuid, rent_item_price, reason, **kwargs):
        args = {}
        args["trackName"] = "rent_item_cancel"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "rent_item_cancel"
        args["rent_item_id"] = str(rent_item_id)
        args["rent_item_uuid"] = str(rent_item_uuid)
        args["rent_item_price"] = rent_item_price
        args["reason"] = str(reason)
        LogTrackingMgr.LOG(args, kwargs)

    # 租赁成交
    @staticmethod
    def rent_item_deal(GBID, distinctId, rent_item_id, rent_item_uuid, deal_total_price, real_gold, real_bind_gold, from_role_id, from_gid, get_role_id, get_gid, **kwargs):
        args = {}
        args["trackName"] = "rent_item_deal"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "rent_item_deal"
        args["rent_item_id"] = str(rent_item_id)
        args["rent_item_uuid"] = str(rent_item_uuid)
        args["deal_total_price"] = deal_total_price
        args["real_gold"] = real_gold
        args["real_bind_gold"] = real_bind_gold
        args["from_role_id"] = from_role_id
        args["from_gid"] = from_gid
        args["get_role_id"] = get_role_id
        args["get_gid"] = get_gid
        LogTrackingMgr.LOG(args, kwargs)

    # 悬赏令
    @staticmethod
    def wantednotice(GBID, distinctId, order_publish_type, public_order_id, personal_order_id, public_order_amount, personal_order_amount, order_finish_type, public_order_finish_id, personal_order_finish_id, **kwargs):
        args = {}
        args["trackName"] = "wantednotice"
        args["#account_id"] = GBID
        args["#distinct_id"] = distinctId
        args["#type"] = "track"
        args["#event_name"] = "wantednotice"
        args["order_publish_type"] = str(order_publish_type)
        args["public_order_id"] = str(public_order_id)
        args["personal_order_id"] = str(personal_order_id)
        args["public_order_amount"] = public_order_amount
        args["personal_order_amount"] = personal_order_amount
        args["order_finish_type"] = order_finish_type
        args["public_order_finish_id"] = str(public_order_finish_id)
        args["personal_order_finish_id"] = str(personal_order_finish_id)
        LogTrackingMgr.LOG(args, kwargs)

    def ms_timestamp_to_datetime(ms_ts):
        """
        毫秒时间戳转 20xx-xx-xx HH:mm:ss.xxx 格式字符串
        """
        sec = ms_ts // 1000
        ms = ms_ts % 1000
        t = time.localtime(sec)
        return f"{t.tm_year}-{t.tm_mon:02d}-{t.tm_mday:02d} {t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}.{ms:03d}"
    
    @staticmethod
    def LOG(args, kwargs):
        res = {
            "properties": {}
        }
        for k, v in args.items():
            if k.startswith("#"):
                res[k] = v
            else:
                res["properties"][k] = v
        ip = "0.0.0.0"
        GBID = args["#account_id"]
        if GBID in gameglobal.roleGBIDToEntId:
            eid = gameglobal.roleGBIDToEntId[GBID]
            if eid in gameglobal.roleCache:
                ip = gameglobal.roleCache[eid].get("ip", "0.0.0.0")
        logData = {
            'server': gameconfig.serverId(),
            'log_id': "LogTracking",
            'sent_timestamp': utils.getTimestamp64(),
            'gameId': gameconfig.gameId(),
            '#time': LogTrackingMgr.ms_timestamp_to_datetime(utils.getTimestamp64()),
            '#ip': ip,
        }
        logData.update(res)
        # 固定的不能改
        fixedHeaders = list(logData.keys())
        for k, v in kwargs.items():
            if k in fixedHeaders:
                continue
            if type(v) is int:
                logData[k] = v
            else:
                logData[k] = str(v)
        gamelog.TLOG("", json.dumps(logData), True)
