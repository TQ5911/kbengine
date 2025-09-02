# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from commands.CMD_COMMON import *
import gzip
import json
import utils
import dataUtils
import gameconfig
import gameengine
import dropAward
import awardContext
import buff_buff as BBD
import base64
import importlib
import inspect
import ast
import time
import types
import fightProp_define as FDD
import skill_skill as SSD
import uiConfig_uiVisible as UCUVD
import actionContext
import gamerefresh
from test import dropTest

callApps = gmCommand._callApps
forwardCommand = gmCommand.forwardCommand


@gm_cmd('$getAllGMCmds', (), RONE, BASE, '获取所有指令', ALLSIDE, GOD_GROUPS)
def getAllGMCmds(su):
    if KBEngine.publish():
        su.onCommandResult(0, 'can not run in publish server', {})
        return
    data = utils.man_gm_cmds()
    su.onCommandResult(0, 'ok' , {"data": data})

@gm_cmd('$getAllPlayers', (), RONE, BASE, '获取所有在线用户', ALLSIDE, GOD_GROUPS)
def getAllPlayers(su):
    if KBEngine.publish():
        su.onCommandResult(0, 'can not run in publish server', {})
        return
    gameengine.callBaseApps("utils.getAllAvatarByGm", (su, gameglobal.localBaseApp))

@gm_cmd('$getAvatarAoiMonster', (Player("gbId/Id"),), RARG(0), CELL, '获取玩家AOI附近怪物', ALLSIDE, GOD_GROUPS)
def getAvatarAoiMonster(su, player):
    monsterdata = []
    for ent in player.entitiesInRange(30, 'Monster'):
        monsterdata.append({'entityId': ent.id, 'MonsterName': ent.name})
    for ent in player.entitiesInRange(30, 'Summon'):
        monsterdata.append({'entityId': ent.id, 'MonsterName': ent.name})
    return su.onCommandResult(0, 'ok' , {"data": monsterdata})

@gm_cmd('$getEntprop', (Player("gbId/Id"),Int('entid'),), RARG(0), CELL, '获取实体属性', ALLSIDE, GOD_GROUPS)
def getEntprop(su,player,entid):

    entprops = {}
    ent = KBEngine.entities.get(entid)
    for propName, propData in FDD.datas.items():
        if not hasattr(ent, propName):
            continue
        entprops[propName] = {
            "value": getattr(ent, propName),
            "name": propData['name']  
        }

    sorted_items = sorted(
    entprops.items(),
    key=lambda kv: 1 if kv[1]["value"] == 0 else 0
)
    entprops = {k: v for k, v in sorted_items}
    
    return su.onCommandResult(0, 'ok', {"data": entprops})

@gm_cmd('$setEntProp', (Player("gbId/Id"),Int('entid'),Str("propName"), Float("value"),), RARG(0), gameconst.CELL, '修改属性', ALLSIDE, GOD_GROUPS)
def setEntProp(su, player,entid,propName,value):
    ent = KBEngine.entities.get(entid)
    if not hasattr(ent, propName):
        return su.onCommandResult(0, f'Faild,{ent.name} 没有 {propName} 属性', {})
    else:
        curVal = ent.getProp(propName)
        if type(curVal) is int:
            newvalue = int(value)
        else:
            newvalue = float(value)
        ent.setProp(f'{propName}', newvalue, gameconst.SourceType.Default)
        return su.onCommandResult(0, f'ok,{ent.name} 的 {propName} 属性从 {curVal} 修改为 {value}',{} )

@gm_cmd('$getEntSkillDic', (Player("gbId/Id"),Int('entid')), RARG(0), gameconst.CELL, '获取实体技能信息', ALLSIDE, GOD_GROUPS)
def getEntSkillDic(su, player, entid):

    mod = importlib.import_module('skill_skill')
    ent = KBEngine.entities.get(entid)
    datas = getattr(mod, 'datas', None)
    if not hasattr(ent, 'skillDic'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", entid)} 没有 skillDic 方法', {})
    weight_map = {}
    if hasattr(ent, 'IsMonster') and hasattr(ent, 'skillPropInfo'):
        skill_ids, weights = ent.skillPropInfo
        weight_map = {sid: w for sid, w in zip(skill_ids, weights)}
    entskilldic = {}
    for skill_id, skill_obj in ent.skillDic.items():        
        # 获取技能action
        try:
            action_func = datas.get(skill_id, {}).get('action', None)
            if action_func:
                # 尝试获取源码
                try:
                    if hasattr(action_func, '__source_code__'):
                        # 动态函数，有源码属性
                        skillaction = action_func.__source_code__
                    else:
                        # 普通函数，用inspect获取源码
                        import inspect
                        skillaction = inspect.getsource(action_func).strip()
                except:
                    # 无法获取源码，显示函数名和类型
                    skillaction = f"<函数: {getattr(action_func, '__name__', 'unknown')} - {type(action_func).__name__}>"
            else:
                skillaction = "None"
        except Exception as e:
            skillaction = f"<获取失败: {str(e)}>"
        
        entskilldic[skill_id] = {
            'skillid': skill_id,
            'name': skill_obj.getSkillName(skill_id),
            'skilllevel': skill_obj.skillLv,
            'weight': weight_map.get(skill_id),
            'action': skillaction
        }
    return su.onCommandResult(0, 'ok', entskilldic)




@gm_cmd('$replaceMonsterSkill', (Player("gbId/Id"),Int('entid'),Str('skillList')), RARG(0), gameconst.CELL, '替换怪物技能', ALLSIDE, GOD_GROUPS)
def replaceMonsterSkill(su, player,entid,skillList):

    ent = KBEngine.entities.get(entid)
    if not hasattr(ent, 'skillDic'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", entid)} 没有 skillDic 方法', {})
    if not hasattr(ent, 'IsMonster'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", entid)} 不是怪物', {})
    newSkillList = ast.literal_eval(skillList)
    ent.changeAllSkill(newSkillList)
    return su.onCommandResult(0, 'ok,替换成功', ent.skillDic)

@gm_cmd('$getEntBuffinfo', (Player("gbId/Id"),Int('entid')), RARG(0), gameconst.CELL, '获取实体buff信息', ALLSIDE, GOD_GROUPS)
def getEntBuffinfo(su, player,entid):
    import utils
    entbuffdic = {}
    ent = KBEngine.entities.get(entid)
    mod = importlib.import_module('buff_buff')
    datas = getattr(mod, 'datas', None)
    if not hasattr(ent, 'buffDic'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", entid)} 没有 buffDic 方法', {})
    for buffid,buffmap in ent.buffDic.items():
        buffdict = buffmap.get(0)
        entbuffdic[buffid] = {
            'buffid': int(buffid),  # 确保是普通int
            'name': str(datas[buffid].get('name', None)) if datas[buffid].get('name') else None,
            'bufflv': int(buffdict.level),  # 确保是普通int
            'time': float(buffdict.getBuffDuration()),  # 确保是普通float
            'starttime': float(buffdict.tStartTime),  # 确保是普通float
            'servertime':int(utils.getNow())
            # 'effectlist': effectlist_normal
        }

    return su.onCommandResult(0, 'ok,获取实体buff信息成功', entbuffdic)

@gm_cmd('$GMtoolsaddEntBuff', (Int('entityid'), Int('buffId'), Int('lv'), Int('time')), RONE, CELL, 'GM工具给实体加buff', ALLSIDE, GOD_GROUPS,minArgs=3)
def GMtoolsaddEntBuff(su, entityid, buffId, buffLv,time=-1):
    ent = KBEngine.entities.get(entityid)
    if buffId in BBD.datas and ent:
        ent.addBuff(buffId, buffLv, entityid,time)
        return True, '执行成功'
    else:
        return False, '执行失败'
    
@gm_cmd('$delEntBuff', (Player("gbId/Id"),Int('entid'),Int('buffid')), RARG(0), gameconst.CELL, '删除实体buff', ALLSIDE, GOD_GROUPS)
def delEntBuff(su, player,entid,buffid):
    ent = KBEngine.entities.get(entid)
    if not hasattr(ent, 'buffDic'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", entid)} 没有 buffDic 方法', {})
    ent.removeBuff(buffid)
    return su.onCommandResult(0, 'ok,获取实体buff信息成功', {})
    
    

@gm_cmd('$unlockAllFunc', (Player("gbId/Id"),), RARG(0), BASE, '解锁所有功能', ALLSIDE, GOD_GROUPS)
def unlockAllFunc(su, player):
    import uiConfig_uiVisible as UCUVD
    import actionContext
    maxLv = 0
    forwardCommand(su,"$SkipNewbieTask", player.id)
    for _, data in UCUVD.datas.items():
        lvLimit = data.get('lvLimit', 0)
        taskId = data.get('missionID', 0)
        if taskId > 0:
            rootTaskId = dataUtils.getRootTaskId(taskId)
            player.baseTaskClaim(rootTaskId, actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrc.GM), needCheck=False)
            player.gmForceSubmitTask(taskId)
        if lvLimit > maxLv:
            maxLv = lvLimit
    if maxLv > 0:
        forwardCommand(su,"$setlv", player.id, maxLv)
    return True, '执行成功'


# 统计掉落 路由那边需要随便选一个stub来固定所在base，不然第二次来取cache的话可能会串
@gm_cmd('$statDropByDropId', (Int("dropId"), Int("count"), Int("Level"), Int("school"), Int("sex")), RSTUB('PlayerStub'), BASE, 
    '根据掉落id统计掉落', ALLSIDE, GOD_GROUPS, minArgs=2)
def statDropByDropId(su, playerStub, dropId, count, level=0, school=0, sex=0):
    from test import dropTest
    dropUnit = dropTest.DropUnit(su, count)
    ret, data, process_info = dropUnit.batchGenAward(dropId, level, school, sex)
    if ret:
        su.onCommandResult(0, 'ok', {'data': {f"{dropId}_{count}_{level}_{school}_{sex}": data}})
    else:
        su.onCommandResult(0, 'wait', {'msg': data, 'process_info': process_info})


@gm_cmd('$statDropByDunNo', (Int("dunNo"), Int("count")), RSTUB('PlayerStub'), BASE, 
    '根据副本编号统计掉落', ALLSIDE, GOD_GROUPS)
def statDropByDunNo(su, playerStub, dunNo, count):
    from test import dropTest
    dropUnit = dropTest.DropUnit(su, count)
    ret, content, process_info = dropUnit.getDunDrop(dunNo, count)
    if ret:
        content = gzip.compress(json.dumps(content).encode('utf-8'))
        su.onCommandResult(0, 'ok', {'data': str(content)})
    else:
        su.onCommandResult(0, 'wait', {'msg': content, 'process_info': process_info})


@gm_cmd('$refreshData', (Str('moduleName'),), RONE, BASE, '刷新表格数据', ALLSIDE, GOD_GROUPS, minArgs=0)
def refreshData(su, moduleName=None):
    """刷新表格数据，转发到所有进程"""
    # 转发到所有BaseApp和CellApp进程执行
    if moduleName:
        forwardCommand(su, '$refreshDataBase', moduleName)
        forwardCommand(su, '$refreshDataCell', moduleName)
        return su.onCommandResult(0, f'已转发刷新 {moduleName} 数据到所有进程', {})
    else:
        forwardCommand(su, '$refreshDataBase', '')
        forwardCommand(su, '$refreshDataCell', '')
        return su.onCommandResult(0, '已转发刷新所有数据到所有进程', {})

@gm_cmd('$refreshDataBase', (Str('moduleName'),), RALL, BASE, '在BaseApp进程中刷新表格数据', ALLSIDE, GOD_GROUPS)
def refreshDataBase(su, moduleName):
    """在BaseApp进程中刷新数据"""
    try:
        import gamerefresh
        if moduleName and moduleName.strip():
            gamerefresh.refreshData(moduleName)
            print(f'BaseApp进程 {KBEngine.getComponentGroupOrder()} 刷新 {moduleName} 数据成功')
            return True, f'BaseApp进程刷新 {moduleName} 数据成功'
        else:
            gamerefresh.refreshData()
            print(f'BaseApp进程 {KBEngine.getComponentGroupOrder()} 刷新所有数据成功')
            return True, 'BaseApp进程刷新所有数据成功'
    except Exception as e:
        print(f'BaseApp进程刷新数据失败: {e}')
        return False, f'BaseApp进程刷新数据失败: {e}'

@gm_cmd('$refreshDataCell', (Str('moduleName'),), RALL, CELL, '在CellApp进程中刷新表格数据', ALLSIDE, GOD_GROUPS)
def refreshDataCell(su, moduleName):
    """在CellApp进程中刷新数据"""
    try:
        import gamerefresh
        if moduleName and moduleName.strip():
            gamerefresh.refreshData(moduleName)
            print(f'CellApp进程 {KBEngine.getComponentGroupOrder()} 刷新 {moduleName} 数据成功')
            return True, f'CellApp进程刷新 {moduleName} 数据成功'
        else:
            gamerefresh.refreshData()
            print(f'CellApp进程 {KBEngine.getComponentGroupOrder()} 刷新所有数据成功')
            return True, 'CellApp进程刷新所有数据成功'
    except Exception as e:
        print(f'CellApp进程刷新数据失败: {e}')
        return False, f'CellApp进程刷新数据失败: {e}'

@gm_cmd('$setMemoryData', (Str('moduleName'), Str('key'), Str('attrName'), Str('value')), RONE, BASE, '修改内存数据(支持普通值和函数)', ALLSIDE, GOD_GROUPS)
def setMemoryData(su, moduleName, key, attrName, value):
    """修改内存数据，支持普通字段和函数表达式，转发到所有进程"""
    
    # 转发到所有BaseApp和CellApp进程执行
    forwardCommand(su, '$setMemoryDataBase', moduleName, key, attrName, value)
    forwardCommand(su, '$setMemoryDataCell', moduleName, key, attrName, value)
    
    return su.onCommandResult(0, f'已转发修改 {moduleName}[{key}].{attrName} 到所有进程', {})

def _setMemoryDataInProcess(moduleName, key, attrName, value, processType):
    """在指定进程中修改内存数据的公共逻辑"""
    try:
        # 导入模块
        mod = importlib.import_module(moduleName)
        datas = getattr(mod, 'datas', None)
        if datas is None:
            return False, f'{processType}进程: 模块 {moduleName} 没有 datas 属性'
        # 处理key类型
        if key.isdigit():
            key_cast = int(key)
        else:
            key_cast = key
            
        if key_cast not in datas:
            return False, f'{processType}进程: key {key} 不在 {moduleName}.datas 中'
        # 获取目标数据对象
        target_data = datas[key_cast]
        # 判断value类型并处理
        if value.startswith('base64:'):
            # 直接内存替换方案 - 不编译，直接创建函数对象
            try:
                from user_type.combatSkill import SkillBase
                SkillBase.clearAllCache()
                decoded_code = base64.b64decode(value[7:]).decode('utf-8')
                # 解析函数名
                import ast
                rootNode = ast.parse(decoded_code)
                funcName = None
                for node in ast.walk(rootNode):
                    if isinstance(node, ast.FunctionDef):
                        funcName = node.name
                        break
                
                if not funcName:
                    return False, f'{processType}进程: 未找到函数定义'
                
                # 在原模块的全局命名空间中编译函数，保留所有导入的模块
                exec(decoded_code, mod.__dict__)
                
                if funcName not in mod.__dict__:
                    return False, f'{processType}进程: 函数{funcName}编译失败'
                # 获取编译好的函数对象
                new_func = mod.__dict__[funcName]
                # 添加源码属性，用于getEntSkillDic获取源码
                new_func.__source_code__ = decoded_code
                if hasattr(target_data, '_data'):
                    # RODict类型，直接修改内部的_data
                    target_data._data[attrName] = new_func
                else:
                    # 普通字典
                    target_data[attrName] = new_func
            
                # 如果是技能，强制清除所有缓存和引用
                if moduleName == 'skill_skill' and attrName == 'action':
                    try:
                        # 强力清除所有可能的SkillBase缓存
                        import gc
                        import sys
                        cleared_count = 0
                        # 1. 清除所有SkillBase类对象的缓存
                        for obj in gc.get_objects():
                            if isinstance(obj, type) and obj.__name__ == 'SkillBase':
                                try:
                                    if hasattr(obj, 'clearAllCache'):
                                        obj.clearAllCache()
                                        cleared_count += 1
                                except Exception as e:
                                    pass  # 忽略清除失败
                        # 2. 清除模块级别的functools.lru_cache
                        if 'user_type.combatSkill' in sys.modules:
                            module = sys.modules['user_type.combatSkill']
                            for attr_name in dir(module):
                                attr = getattr(module, attr_name)
                                if hasattr(attr, 'cache_clear'):
                                    try:
                                        attr.cache_clear()
                                    except Exception as e:
                                        pass  # 忽略清除失败
                        # 3. 强制垃圾回收
                        gc.collect()
                    except Exception as e:
                        pass  # 忽略清除缓存失败
                
                return True, f'{processType}进程直接内存替换函数{funcName}成功'
                
            except Exception as e:
                return False, f'{processType}进程: 直接内存替换失败: {str(e)}'
        
        else:
            # 普通值，尝试eval转换类型
            try:
                # 先尝试eval，如果失败就作为字符串
                try:
                    parsed_value = eval(value)
                except:
                    parsed_value = value
                
                # 设置到数据中
                if hasattr(target_data, '_data'):
                    target_data._data[attrName] = parsed_value
                else:
                    target_data[attrName] = parsed_value
                    
                return True, f'{processType}进程修改普通值成功'
                
            except Exception as e:
                return False, f'{processType}进程: 值设置失败: {str(e)}'
                
    except Exception as e:
        return False, f'{processType}进程修改失败: {str(e)}'

@gm_cmd('$setMemoryDataBase', (Str('moduleName'), Str('key'), Str('attrName'), Str('value')), RALL, BASE, '在BaseApp进程中修改内存数据', ALLSIDE, GOD_GROUPS)
def setMemoryDataBase(su, moduleName, key, attrName, value):
    """在BaseApp进程中修改内存数据"""
    return _setMemoryDataInProcess(moduleName, key, attrName, value, 'BaseApp')

@gm_cmd('$setMemoryDataCell', (Str('moduleName'), Str('key'), Str('attrName'), Str('value')), RALL, CELL, '在CellApp进程中修改内存数据', ALLSIDE, GOD_GROUPS)
def setMemoryDataCell(su, moduleName, key, attrName, value):
    """在CellApp进程中修改内存数据"""
    return _setMemoryDataInProcess(moduleName, key, attrName, value, 'CellApp')

@gm_cmd('$reqWorkshopSetAutoMF', (Player("gbId/Id"), Int('autoMF')), RARG(0), gameconst.BASE, '测试开启自动合成制作', ALLSIDE, GOD_GROUPS)
def reqWorkshopSetAutoMF(su, player, autoMF):
    INFO_MSG("GM: reqWorkshopSetAutoMF ~ ", autoMF)
    return player.reqWorkshopSetAutoMF(autoMF)

@gm_cmd('$reqWorkshopMF', (Player("gbId/Id"), Int('itemID'), Int('batchCount')), RARG(0), gameconst.BASE, '测试合成制作', ALLSIDE, GOD_GROUPS)
def reqWorkshopMF(su, player, itemID, batchCount):
    INFO_MSG("GM: reqWorkshopMF ~ ", itemID, batchCount)
    return player.reqWorkshopMF(itemID, batchCount)

